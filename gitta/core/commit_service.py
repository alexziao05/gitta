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
from gitta.core.generator import generate_commit_message, generate_grouped_commit_messages
from gitta.git.diff_parser import DiffGroup, parse_diff_by_file, group_diffs_by_module


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

    def run_split(self) -> tuple[list[tuple[DiffGroup, str]], bool]:
        """
        Run the split-commit workflow: parse diff by file, group by module,
        and generate one scoped commit message per group.

        Returns:
            tuple: (list of (DiffGroup, message) tuples, was_truncated)

        Raises:
            RuntimeError: If not inside a Git repository or no staged changes.
        """
        if not GitRepository.is_git_repo():
            raise RuntimeError("Not a Git repository.")

        settings = Settings()
        diff, was_truncated = get_staged_diff(max_chars=settings.max_diff_chars)

        if not diff:
            raise RuntimeError("No staged changes to commit.")

        file_diffs = parse_diff_by_file(diff)
        groups = group_diffs_by_module(file_diffs)

        # Single group: fall back to standard generation
        if len(groups) == 1:
            message = generate_commit_message(diff)
            return [(groups[0], message)], was_truncated

        return generate_grouped_commit_messages(groups), was_truncated
