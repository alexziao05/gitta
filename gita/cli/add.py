# cli/add.py
# Purpose: Handles `gita add`.
#
# Responsibilities:
#   - Accept file paths
#   - Stage files via GitRepository
#   - Handle CLI-level errors

import typer

from gita.git.repository import GitRepository
from gita.core.commit_service import CommitService
from gita.utils.console import print_error, print_info, print_success
from gita.utils.loading import show_loading

def add_command(
    files: list[str] = typer.Argument(..., help="Files or paths to stage."),
):
    """
    Stage files and generate a commit message.

    This command stages the specified files, then generates an AI-powered
    commit message based on the staged changes.

    Usage:
        gita add <files>
    """

    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    try:
        GitRepository.stage_files(files)
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    staged = GitRepository.get_staged_files()
    print_success(f"Staged {len(staged)} file(s): {', '.join(staged)}")

    service = CommitService()

    try:
        with show_loading("Generating commit message..."):
            message = service.run()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    committed = service.confirm_commit(dry_run=False, message=message)

    if not committed:
        GitRepository.unstage_files(staged)
        print_info("Staged files have been unstaged.")
