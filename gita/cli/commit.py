# cli/commit.py
# Purpose: Handles `gita commit`.
#
# Responsibilities:
#   - Parse flags
#   - Pass arguments to CommitService
#   - Handle CLI-level errors

import typer

from gita.core.commit_service import CommitService
from gita.config.settings import Settings
from gita.cli.confirm import confirm_and_commit
from gita.utils.console import print_error, print_info
from gita.utils.loading import show_loading

def commit_command(dry_run: bool = typer.Option(False, "--dry-run", help="Generate commit message without committing")):
    """
    Generate a commit message using AI.

    This command analyzes the staged changes in your Git repository and generates
    a commit message based on the code changes. It uses an AI model to understand
    the context of the changes and produce a meaningful commit message.

    Usage:
        gita commit
    """
    try:
        Settings().validate_api_key()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    service = CommitService()

    try:
        with show_loading("Generating commit message..."):
            message = service.run(dry_run=dry_run)
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    if dry_run:
        print_info(message)
        return

    confirm_and_commit(message)
