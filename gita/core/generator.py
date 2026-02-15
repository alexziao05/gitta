# core/generator.py
# Purpose: Convert diff into a commit message using AI client.
#
# Responsibilities:
#   - Build prompt
#   - Call AI client
#   - Return clean commit message

def generate_commit_message(diff: str) -> str:
    """
    Generate a commit message from a git diff using an AI client.

    Args:
        diff (str): The git diff representing the staged changes.

    Returns:
        str: The generated commit message.
    """
   
    lines_changed = len(diff.splitlines())

    return f"chore: update {lines_changed} lines of code"