# cli/add.py
# Purpose: Handles `gitta add`.
#
# Responsibilities:
#   - Accept file paths
#   - Stage files via GitRepository
#   - Handle CLI-level errors

import typer

from gitta.git.repository import GitRepository
from gitta.core.commit_service import CommitService
from gitta.config.settings import Settings
from gitta.cli.confirm import confirm_and_commit, confirm_and_commit_groups
from gitta.utils.console import print_error, print_info, print_success, print_warning
from gitta.utils.loading import show_loading

def add_command(
    files: list[str] = typer.Argument(..., help="Files or paths to stage."),
    split: bool = typer.Option(None, "--split/--no-split", help="Split changes into multiple scoped commits"),
):
    """
    Stage files and generate a commit message.

    This command stages the specified files, then generates an AI-powered
    commit message based on the staged changes.

    Usage:
        gitta add <files>
        gitta add <files> --split
    """

    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    previously_staged = GitRepository.get_staged_files()

    try:
        GitRepository.stage_files(files)
    except RuntimeError as e:
        newly_staged = [f for f in GitRepository.get_staged_files() if f not in previously_staged]
        if newly_staged:
            GitRepository.unstage_files(newly_staged)
        print_error(f"Error: {e}")
        raise typer.Exit(code=1)

    staged = GitRepository.get_staged_files()
    print_success(f"Staged {len(staged)} file(s): {', '.join(staged)}")

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

        if len(grouped) == 1:
            committed = confirm_and_commit(grouped[0][1])
        else:
            committed = confirm_and_commit_groups(grouped)
    else:
        try:
            with show_loading("Generating commit message..."):
                message, was_truncated = service.run()
        except RuntimeError as e:
            print_error(f"Error: {e}")
            raise typer.Exit(code=1)

        if was_truncated:
            print_warning("Warning: Diff was too large and was truncated. The commit message may not cover all changes.")

        committed = confirm_and_commit(message)

    if not committed:
        GitRepository.unstage_files(staged)
        print_info("Staged files have been unstaged.")
