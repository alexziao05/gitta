# cli/explain.py
# Purpose: Handles `gitta explain`.
#
# Responsibilities:
#   - Accept a commit hash or file path
#   - Retrieve the relevant diff
#   - Generate a plain English explanation via AI

import subprocess

import typer

from gitta.ai.client import AIClient
from gitta.config.settings import Settings
from gitta.constants import DEFAULT_MAX_DIFF_CHARS
from gitta.git.repository import GitRepository
from gitta.utils.console import print_error, print_info, print_warning
from gitta.utils.loading import show_loading


def explain_command(
    target: str = typer.Argument(..., help="A commit hash (e.g. abc1234) or file path to explain"),
):
    """
    Explain what a commit or file change does in plain English.

    Accepts a commit hash or a file path. For commits, explains the full
    change. For files, explains the uncommitted diff.

    Usage:
        gitta explain abc1234
        gitta explain src/main.py
    """
    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    try:
        Settings().validate_api_key()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    diff, context = _get_diff(target)

    if not diff:
        print_info("No changes found to explain.")
        raise typer.Exit(code=0)

    # Truncate if too large
    settings = Settings()
    max_chars = settings.max_diff_chars
    was_truncated = False
    if len(diff) > max_chars:
        diff = diff[:max_chars]
        was_truncated = True

    try:
        with show_loading("Generating explanation..."):
            client = AIClient()
            explanation = client.generate_explanation(diff=diff, context=context)
    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    if was_truncated:
        print_warning("Warning: Diff was too large and was truncated.")

    print_info(f"\n{explanation}")


def _get_diff(target: str) -> tuple[str, str]:
    """
    Resolve the target to a diff and context string.

    Tries commit hash first, then falls back to file path.
    Returns (diff, context).
    """
    # Try as a commit hash
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{target}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        # It's a valid commit
        msg_result = subprocess.run(
            ["git", "log", "-1", "--format=%s", target],
            capture_output=True,
            text=True,
        )
        commit_message = msg_result.stdout.strip() if msg_result.returncode == 0 else ""

        diff_result = subprocess.run(
            ["git", "show", "--format=", target],
            capture_output=True,
            text=True,
        )
        if diff_result.returncode != 0:
            raise RuntimeError(f"Failed to get diff for commit {target}")

        context = f"Commit: {target}\nMessage: {commit_message}" if commit_message else f"Commit: {target}"
        return diff_result.stdout.strip(), context

    # Try as a file path (uncommitted changes: staged + unstaged)
    diff_result = subprocess.run(
        ["git", "diff", "HEAD", "--", target],
        capture_output=True,
        text=True,
    )
    if diff_result.returncode == 0 and diff_result.stdout.strip():
        return diff_result.stdout.strip(), f"File: {target}"

    # Try staged-only diff for new files
    diff_result = subprocess.run(
        ["git", "diff", "--cached", "--", target],
        capture_output=True,
        text=True,
    )
    if diff_result.returncode == 0 and diff_result.stdout.strip():
        return diff_result.stdout.strip(), f"File: {target} (staged)"

    return "", ""
