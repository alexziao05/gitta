# core/generator.py
# Purpose: Convert diff into a commit message using AI client.
#
# Responsibilities:
#   - Build prompt
#   - Call AI client
#   - Return clean commit message

from gitta.ai.client import AIClient
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