# cli/pr.py
# Purpose: Handles `gitta pr`.
#
# Responsibilities:
#   - Gather commits and diff vs base branch
#   - Generate PR title + description via AI
#   - Optionally create PR via gh CLI

import subprocess

import typer

from gitta.ai.client import AIClient
from gitta.git.repository import GitRepository
from gitta.config.settings import Settings
from gitta.constants import DEFAULT_MAX_DIFF_CHARS
from gitta.utils.console import print_error, print_info, print_success, print_warning
from gitta.utils.editor import open_editor_with_message
from gitta.utils.loading import show_loading

PR_SEPARATOR = "---BODY---"


def pr_command(
    base: str = typer.Option(None, "--base", "-b", help="Base branch to compare against (default: auto-detect)"),
    create: bool = typer.Option(False, "--create", "-c", help="Create the PR on GitHub using gh CLI"),
    draft: bool = typer.Option(False, "--draft", "-d", help="Create as draft PR (requires --create)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Generate PR description without creating"),
):
    """
    Generate a PR title and description from branch commits.

    Analyzes all commits on the current branch vs the base branch and
    generates a PR title and markdown description using AI.

    Usage:
        gitta pr
        gitta pr --base main
        gitta pr --create
        gitta pr --create --draft
    """
    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    branch = GitRepository.get_current_branch()
    if branch == "HEAD":
        print_error("Error: Cannot create PR from a detached HEAD.")
        raise typer.Exit(code=1)

    # Detect base branch
    if not base:
        try:
            base = GitRepository.get_default_branch()
        except RuntimeError as e:
            print_error(f"Error: {e}")
            raise typer.Exit(code=1)

    if branch == base:
        print_error(f"Error: Current branch '{branch}' is the same as base branch '{base}'.")
        raise typer.Exit(code=1)

    # Check gh availability early so we don't waste an API call
    if create and not _gh_available():
        print_error("Error: 'gh' CLI not found. Install it from https://cli.github.com/")
        raise typer.Exit(code=1)

    try:
        Settings().validate_api_key()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    # Gather commits, stat, and diff
    try:
        commits = GitRepository.get_commits_between(base)
    except RuntimeError as e:
        print_error(f"Error getting commits: {e}")
        raise typer.Exit(code=1)

    if not commits:
        print_info(f"No commits found between '{base}' and '{branch}'.")
        raise typer.Exit(code=0)

    try:
        stat = GitRepository.get_diff_stat(base)
    except RuntimeError as e:
        print_error(f"Error getting diff stat: {e}")
        raise typer.Exit(code=1)

    try:
        diff = GitRepository.get_diff_between(base)
    except RuntimeError as e:
        print_error(f"Error getting diff: {e}")
        raise typer.Exit(code=1)

    # Truncate diff if too large (stat + commits still provide full coverage)
    settings = Settings()
    max_chars = settings.max_diff_chars
    was_truncated = False
    if len(diff) > max_chars:
        diff = diff[:max_chars]
        was_truncated = True

    # Generate PR description
    try:
        with show_loading("Generating PR description..."):
            client = AIClient()
            title, body = client.generate_pr_description(
                branch=branch,
                commits=commits,
                stat=stat,
                diff=diff,
            )
    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    if was_truncated:
        print_warning("Warning: Diff was too large and was truncated. File stats and commits were used for full coverage.")

    # Display the result
    _display_pr(title, body)

    if dry_run:
        return

    if not create:
        print_info("\nUse --create to create this PR on GitHub.")
        return

    # Confirm/edit loop before creating
    while True:
        choice = typer.prompt(
            "\nCreate this PR? [y/n/e]",
            default="y"
        ).strip().lower()

        if choice == "y":
            break

        elif choice == "n":
            print_error("\nPR creation cancelled.")
            return

        elif choice == "e":
            combined = f"{title}\n{PR_SEPARATOR}\n{body}"
            edited = open_editor_with_message(combined)

            if PR_SEPARATOR in edited:
                title_part, body_part = edited.split(PR_SEPARATOR, 1)
                title = title_part.strip()
                body = body_part.strip()
            else:
                # If separator was removed, first line is title, rest is body
                lines = edited.split("\n", 1)
                title = lines[0].strip()
                body = lines[1].strip() if len(lines) > 1 else ""

            if not title:
                print_error("\nPR title cannot be empty.")
                continue

            _display_pr(title, body)

        else:
            print_error("\nInvalid option. Enter y, n, or e.\n")

    # Push branch if needed
    try:
        GitRepository.push_with_upstream(branch)
        print_success(f"\nPushed '{branch}' to origin.")
    except RuntimeError as e:
        print_error(f"Error pushing: {e}")
        raise typer.Exit(code=1)

    # Create the PR
    gh_args = ["gh", "pr", "create", "--base", base, "--title", title, "--body", body]
    if draft:
        gh_args.append("--draft")

    result = subprocess.run(gh_args, capture_output=True, text=True)
    if result.returncode != 0:
        print_error(f"Error creating PR: {result.stderr.strip()}")
        raise typer.Exit(code=1)

    pr_url = result.stdout.strip()
    print_success(f"\nPR created: {pr_url}")


def _display_pr(title: str, body: str) -> None:
    """Display a PR title and body."""
    print_success("\nPR Title:")
    print_info(f"  {title}\n")
    print_success("PR Body:")
    print_info(body)


def _gh_available() -> bool:
    """Check if the gh CLI is installed."""
    result = subprocess.run(
        ["gh", "--version"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
