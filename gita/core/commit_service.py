# core/commit_service.py
# Purpose: Main orchestration engine for commit workflow.
#
# Responsibilities:
#   - Ensure inside git repo
#   - Get staged diff
#   - Call generator
#   - Show preview
#   - Confirm
#   - Commit

import typer

from gita.git.repository import GitRepository
from gita.git.diff import get_staged_diff
from gita.core.generator import generate_commit_message
from gita.utils.editor import open_editor_with_message
from gita.utils.console import print_error, print_success, print_info


class CommitService:
    """
    Orchestrates the commit workflow. 
    """
    def run(self, dry_run: bool = False) -> str:
        """
        Executes the commit workflow.

        Returns:
            str: The staged diff.

        Raises:
            RuntimeError: If not inside a Git repository or if there are no staged changes. 
        """

        if not GitRepository.is_git_repo():
            raise RuntimeError("Error: Not a Git repository.")
        
        diff = get_staged_diff()

        if not diff:
            raise RuntimeError("No staged changes to commit.")
        
        message = generate_commit_message(diff)

        if dry_run:
            return message
        
        return message
    
    def commit(self, message: str) -> None:
        """
        Commits the staged changes with the provided message.

        Args:
            message (str): The commit message to use.

        Raises:
            RuntimeError: If the commit command fails.
        """
        GitRepository.commit(message)

    def confirm_commit(self, dry_run: bool, message: str):
        """
        Asks the user to confirm the commit message.

        Args:
            message (str): The commit message to confirm.

        """

        print_success("\nGenerated commit message:\n")
        print_info(message)

        if dry_run:
            return

        while True:
            choice = typer.prompt(
                "\nCommit with this message? [y/n/e]",
                default="y"
            ).strip().lower()

            if choice == "y":
                GitRepository.commit(message)
                print_success("\nCommit successful.")
                break

            elif choice == "n":
                print_error("\nCommit cancelled.")
                break

            elif choice == "e":
                message = open_editor_with_message(message)

                if not message.strip():
                    print_error("\nCommit message cannot be empty.")
                    message = self.run(dry_run=True)  # Regenerate original message

            else:
                print_error("\nInvalid option. Enter y, n, or e.\n\n")


