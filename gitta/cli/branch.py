# cli/branch.py
# Purpose: Handles `gitta branch`.
#
# Responsibilities:
#   - Accept a natural language description
#   - Generate a branch name via AI
#   - Optionally create and checkout the branch

import subprocess

import typer

from gitta.ai.client import AIClient
from gitta.config.settings import Settings
from gitta.git.repository import GitRepository
from gitta.utils.console import print_error, print_info, print_success
from gitta.utils.loading import show_loading


def branch_command(
    description: str = typer.Argument(..., help="Natural language description of the branch"),
    checkout: bool = typer.Option(False, "--checkout", "-c", help="Create and checkout the branch"),
):
    """
    Generate a branch name from a natural language description.

    Uses AI to convert a description into a conventional branch name.

    Usage:
        gitta branch "fix login timeout"
        gitta branch "add user avatar upload" --checkout
    """
    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    try:
        Settings().validate_api_key()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    try:
        with show_loading("Generating branch name..."):
            client = AIClient()
            branch_name = client.generate_branch_name(description)
    except Exception as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    print_success(f"\n  {branch_name}")

    if not checkout:
        print_info("\nUse --checkout to create and switch to this branch.")
        return

    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"Error creating branch: {result.stderr.strip()}")
        raise typer.Exit(code=1)

    print_success(f"\nSwitched to new branch '{branch_name}'.")
