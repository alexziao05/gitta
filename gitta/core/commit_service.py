# core/commit_service.py
# Purpose: Main orchestration engine for commit workflow.
#
# Responsibilities:
#   - Ensure inside git repo
#   - Get staged diff
#   - Call generator
#   - Return generated message

from gitta.git.repository import GitRepository
from gitta.git.diff import get_staged_diff
from gitta.config.settings import Settings
from gitta.core.generator import generate_commit_message


class CommitService:
    """
    Orchestrates the commit workflow.
    """
    def run(self, dry_run: bool = False) -> tuple[str, bool]:
        """
        Executes the commit workflow.

        Returns:
            tuple: (generated_message, was_truncated)

        Raises:
            RuntimeError: If not inside a Git repository or if there are no staged changes.
        """

        if not GitRepository.is_git_repo():
            raise RuntimeError("Not a Git repository.")

        settings = Settings()
        diff, was_truncated = get_staged_diff(max_chars=settings.max_diff_chars)

        if not diff:
            raise RuntimeError("No staged changes to commit.")

        return generate_commit_message(diff), was_truncated
