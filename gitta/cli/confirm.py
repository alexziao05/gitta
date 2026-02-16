# cli/confirm.py
# Purpose: Shared commit confirmation flow for CLI commands.
#
# Responsibilities:
#   - Display generated commit message
#   - Prompt user to confirm, cancel, or edit
#   - Commit via GitRepository

import typer

from gitta.git.repository import GitRepository
from gitta.core.commit_service import CommitService
from gitta.utils.editor import open_editor_with_message
from gitta.utils.console import print_error, print_success, print_info


def confirm_and_commit(message: str) -> bool:
    """
    Show the commit message and prompt the user to confirm, cancel, or edit.

    Args:
        message: The generated commit message.

    Returns:
        True if the commit was made, False if cancelled.
    """

    print_success("\nGenerated commit message:\n")
    print_info(message)

    while True:
        choice = typer.prompt(
            "\nCommit with this message? [y/n/e]",
            default="y"
        ).strip().lower()

        if choice == "y":
            GitRepository.commit(message)
            print_success("\nCommit successful.")
            return True

        elif choice == "n":
            print_error("\nCommit cancelled.")
            return False

        elif choice == "e":
            message = open_editor_with_message(message)

            if not message.strip():
                print_error("\nCommit message cannot be empty.")
                service = CommitService()
                message, _ = service.run(dry_run=True)

            print_success("\nUpdated commit message:\n")
            print_info(message)

        else:
            print_error("\nInvalid option. Enter y, n, or e.\n\n")
