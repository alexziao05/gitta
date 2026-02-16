# cli/commit.py
# Purpose: Handles `gita commit`.
#
# Responsibilities:
#   - Parse flags
#   - Pass arguments to CommitService
#   - Handle CLI-level errors

import typer 
from gita.core.commit_service import CommitService
from gita.utils.editor import open_editor_with_message

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
        message = service.run()
    except RuntimeError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    
    typer.echo("Generated commit message:\n")
    typer.echo(message)

    if dry_run:
        return
    
    while True: 
        choice = typer.prompt(
            '\nCommit with this message? [y/n/e] (y = yes, n = no, e = edit message)',
            default="y"
        ).strip().lower()

        if choice == 'y':
            try:
                service.commit(message)
                typer.echo("Commit successful!")
                break
            except RuntimeError as e:
                typer.echo(f"Error: {e}")
                raise typer.Exit(code=1)
            break 

        elif choice == 'n':
            typer.echo("Commit aborted.")
            break

        elif choice == 'e':
            message = open_editor_with_message(message)

            if not message.strip():
                typer.echo("Commit message cannot be empty.")
                message = service.run(dry_run=True)  # Regenerate original
        else:
            typer.echo("Invalid choice. Please enter 'y', 'n', or 'e'.")
