# cli/ship.py
# Purpose: Handles `gita ship`.
#
# Responsibilities:
#   - Stage all files
#   - Generate commit message
#   - Confirm and commit
#   - Push to current branch

import typer

from gita.git.repository import GitRepository
from gita.core.commit_service import CommitService
from gita.cli.confirm import confirm_and_commit
from gita.utils.console import print_error, print_info, print_success
from gita.utils.loading import show_loading

def ship_command():
    """
    Stage all changes, generate a commit message, and push.

    This command stages all files, generates an AI-powered commit message,
    confirms with the user, commits, and pushes to the current branch.

    Usage:
        gita ship
    """

    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    try:
        GitRepository.stage_files(["."])
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    staged = GitRepository.get_staged_files()

    if not staged:
        print_info("No changes to stage.")
        raise typer.Exit(code=0)

    print_success(f"Staged {len(staged)} file(s): {', '.join(staged)}")

    service = CommitService()

    try:
        with show_loading("Generating commit message..."):
            message = service.run()
    except RuntimeError as e:
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    committed = confirm_and_commit(message)

    if not committed:
        GitRepository.unstage_files(staged)
        print_info("Staged files have been unstaged.")
        return

    branch = GitRepository.get_current_branch()

    try:
        GitRepository.push()
        print_success(f"Pushed to '{branch}'.")
    except RuntimeError as e:
        print_error(f"Error pushing: {e}")
        GitRepository.revert_last_commit()
        print_info("Commit has been reverted. Changes are still staged.")
        raise typer.Exit(code=1)
