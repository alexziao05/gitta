# cli/commit.py
# Purpose: Handles `gitta commit`.
#
# Responsibilities:
#   - Parse flags
#   - Pass arguments to CommitService
#   - Handle CLI-level errors

import typer

from gitta.core.commit_service import CommitService
from gitta.config.settings import Settings
from gitta.cli.confirm import confirm_and_commit, confirm_and_commit_groups
from gitta.utils.console import print_error, print_info, print_warning
from gitta.utils.loading import show_loading

def commit_command(
    dry_run: bool = typer.Option(False, "--dry-run", help="Generate commit message without committing"),
    split: bool = typer.Option(None, "--split/--no-split", help="Split changes into multiple scoped commits"),
):
    """
    Generate a commit message using AI.

    This command analyzes the staged changes in your Git repository and generates
    a commit message based on the code changes. It uses an AI model to understand
    the context of the changes and produce a meaningful commit message.

    Usage:
        gitta commit
        gitta commit --split
    """
    try:
        settings = Settings()
        settings.validate_api_key()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    use_split = split if split is not None else settings.multi_file
    service = CommitService()

    if use_split:
        try:
            with show_loading("Analyzing changes and generating commit messages..."):
                grouped, was_truncated = service.run_split()
        except RuntimeError as e:
            print_error(f"Error: {e}")
            raise typer.Exit(code=1)

        if was_truncated:
            print_warning("Warning: Diff was too large and was truncated. The commit messages may not cover all changes.")

        if dry_run:
            for group, message in grouped:
                print_info(f"({group.scope}) {message}\n")
            return

        # Single group falls through to normal confirm flow
        if len(grouped) == 1:
            confirm_and_commit(grouped[0][1])
        else:
            confirm_and_commit_groups(grouped)
    else:
        try:
            with show_loading("Generating commit message..."):
                message, was_truncated = service.run(dry_run=dry_run)
        except RuntimeError as e:
            print_error(f"Error: {e}")
            raise typer.Exit(code=1)

        if was_truncated:
            print_warning("Warning: Diff was too large and was truncated. The commit message may not cover all changes.")

        if dry_run:
            print_info(message)
            return

        confirm_and_commit(message)
