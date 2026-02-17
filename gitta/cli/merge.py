# cli/merge.py
# Purpose: Handles `gitta merge`.
#
# Responsibilities:
#   - Show PR status for the current branch
#   - Merge the PR via gh CLI

import subprocess

import typer

from gitta.git.repository import GitRepository
from gitta.utils.console import print_error, print_info, print_success


def merge_command(
    squash: bool = typer.Option(False, "--squash", "-s", help="Squash and merge"),
    rebase: bool = typer.Option(False, "--rebase", "-r", help="Rebase and merge"),
    delete_branch: bool = typer.Option(True, "--delete-branch/--no-delete-branch", "-d/-D", help="Delete branch after merge"),
):
    """
    Merge the pull request for the current branch.

    Finds the open PR for your current branch and merges it via the GitHub CLI.

    Usage:
        gitta merge
        gitta merge --squash
        gitta merge --rebase
        gitta merge --no-delete-branch
    """
    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    if not _gh_available():
        print_error("Error: 'gh' CLI not found. Install it from https://cli.github.com/")
        raise typer.Exit(code=1)

    branch = GitRepository.get_current_branch()
    if branch == "HEAD":
        print_error("Error: Cannot merge from a detached HEAD.")
        raise typer.Exit(code=1)

    # Show PR info
    result = subprocess.run(
        ["gh", "pr", "view", "--json", "title,number,state,url"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print_error(f"No open PR found for branch '{branch}'.")
        raise typer.Exit(code=1)

    import json
    pr = json.loads(result.stdout)

    if pr["state"] != "OPEN":
        print_error(f"PR #{pr['number']} is already {pr['state'].lower()}.")
        raise typer.Exit(code=1)

    print_info(f"PR #{pr['number']}: {pr['title']}")
    print_info(f"  {pr['url']}")

    # Build merge command
    gh_args = ["gh", "pr", "merge"]

    if squash:
        gh_args.append("--squash")
    elif rebase:
        gh_args.append("--rebase")
    else:
        gh_args.append("--merge")

    if delete_branch:
        gh_args.append("--delete-branch")

    # Confirm
    choice = typer.prompt(
        "\nMerge this PR? [y/n]",
        default="y",
    ).strip().lower()

    if choice != "y":
        print_error("\nMerge cancelled.")
        return

    result = subprocess.run(gh_args, capture_output=True, text=True)
    if result.returncode != 0:
        print_error(f"Error merging PR: {result.stderr.strip()}")
        raise typer.Exit(code=1)

    print_success(f"\nPR #{pr['number']} merged successfully.")


def _gh_available() -> bool:
    """Check if the gh CLI is installed."""
    result = subprocess.run(
        ["gh", "--version"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
