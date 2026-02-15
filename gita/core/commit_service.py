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

from gita.git.repository import GitRepository
from gita.git.diff import get_staged_diff
from gita.core.generator import generate_commit_message

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

