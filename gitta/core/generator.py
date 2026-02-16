# core/generator.py
# Purpose: Convert diff into a commit message using AI client.
#
# Responsibilities:
#   - Build prompt
#   - Call AI client
#   - Return clean commit message

from gitta.ai.client import AIClient
from gitta.git.diff_parser import DiffGroup


def generate_commit_message(diff: str) -> str:
    """
    Generate a commit message from a git diff using an AI client.

    Args:
        diff (str): The git diff representing the staged changes.

    Returns:
        str: The generated commit message.
    """

    client = AIClient()
    return client.generate_commit_message(diff)


def generate_grouped_commit_messages(groups: list[DiffGroup]) -> list[tuple[DiffGroup, str]]:
    """
    Generate one commit message per DiffGroup.

    Args:
        groups: List of DiffGroup objects to generate messages for.

    Returns:
        List of (group, message) tuples.
    """
    client = AIClient()
    results = []
    for group in groups:
        message = client.generate_scoped_commit_message(
            scope=group.scope,
            files=group.files,
            diff=group.combined_diff,
        )
        results.append((group, message))
    return results