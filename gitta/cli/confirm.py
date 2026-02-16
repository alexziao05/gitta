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
from gitta.git.diff_parser import DiffGroup
from gitta.utils.editor import open_editor_with_message
from gitta.utils.console import print_error, print_success, print_info, print_warning


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


def confirm_and_commit_groups(grouped_messages: list[tuple[DiffGroup, str]]) -> bool:
    """
    Present multiple scoped commits for user review and execute them.

    Displays all proposed commits, then prompts the user to:
      [a]ll  - commit each group as a separate commit
      [m]erge - combine all messages into a single commit
      [c]ancel - abort without committing

    For 'all' mode, files are unstaged and restaged per group to create
    separate commits with only the relevant files in each.

    Args:
        grouped_messages: List of (DiffGroup, message) tuples.

    Returns:
        True if any commits were made, False if cancelled.
    """
    print_success(f"\nGenerated {len(grouped_messages)} scoped commit(s):\n")

    for i, (group, message) in enumerate(grouped_messages, 1):
        files_str = ", ".join(group.files)
        print_info(f"[{i}] ({group.scope}) {files_str}")
        print_info(f"    {message}\n")

    while True:
        choice = typer.prompt(
            "\n[a]ll as separate commits / [m]erge into one / [c]ancel",
            default="a"
        ).strip().lower()

        if choice == "a":
            return _commit_groups_separately(grouped_messages)

        elif choice == "m":
            merged = "\n\n".join(msg for _, msg in grouped_messages)
            GitRepository.commit(merged)
            print_success("\nCommit successful (merged).")
            return True

        elif choice == "c":
            print_error("\nCommit cancelled.")
            return False

        else:
            print_error("\nInvalid option. Enter a, m, or c.\n")


def _commit_groups_separately(grouped_messages: list[tuple[DiffGroup, str]]) -> bool:
    """Commit each group as a separate commit via unstage/restage cycle."""
    all_staged = GitRepository.get_staged_files()
    committed_count = 0

    for i, (group, message) in enumerate(grouped_messages, 1):
        try:
            # Unstage everything, then stage only this group's files
            remaining_staged = GitRepository.get_staged_files()
            if remaining_staged:
                GitRepository.unstage_files(remaining_staged)
            GitRepository.stage_files(group.files)
            GitRepository.commit(message)
            committed_count += 1
            print_success(f"  [{i}/{len(grouped_messages)}] Committed: {message.splitlines()[0]}")
        except RuntimeError as e:
            print_error(f"\n  [{i}/{len(grouped_messages)}] Failed: {e}")
            # Restage remaining files so user can retry
            remaining_files = []
            for _, (g, _) in enumerate(grouped_messages[i:]):
                remaining_files.extend(g.files)
            if remaining_files:
                try:
                    GitRepository.stage_files(remaining_files)
                except RuntimeError:
                    pass
            print_warning(f"\n{committed_count} commit(s) succeeded. Remaining files are still staged.")
            return committed_count > 0

    print_success(f"\nAll {committed_count} commit(s) successful.")
    return True
