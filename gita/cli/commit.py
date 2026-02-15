# cli/commit.py
# Purpose: Handles `gita commit`.
#
# Responsibilities:
#   - Parse flags
#   - Pass arguments to CommitService
#   - Handle CLI-level errors

import typer 
from gita.core.commit_service import CommitService

def commit_command():
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
        message = service.run()
    except RuntimeError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    
    typer.echo("Generated commit message:\n")
    typer.echo(message)
    