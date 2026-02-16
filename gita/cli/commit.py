# cli/commit.py
# Purpose: Handles `gita commit`.
#
# Responsibilities:
#   - Parse flags
#   - Pass arguments to CommitService
#   - Handle CLI-level errors

import typer 
from rich.console import Console

from gita.core.commit_service import CommitService
from gita.utils.editor import open_editor_with_message
from gita.utils.loading import show_loading

console = Console()

def commit_command(dry_run: bool = typer.Option(False, "--dry-run", help="Generate commit message without committing")):
    """
    Generate a commit message using AI.

    This command analyzes the staged changes in your Git repository and generates
    a commit message based on the code changes. It uses an AI model to understand
    the context of the changes and produce a meaningful commit message.

    Usage:
        gita commit
    """
    service = CommitService()

    try:
        with show_loading("Generating commit message..."):
            message = service.run(dry_run=dry_run)
    except RuntimeError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    if dry_run:
        return
    
    service.confirm_commit(dry_run=dry_run, message=message)
    
    