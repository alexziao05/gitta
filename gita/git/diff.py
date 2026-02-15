# git/diff.py
# Purpose: Retrieve git diffs.
#
# Responsibilities:
#   - Get staged diff
#   - Get last commit diff

import subprocess

def get_staged_diff() -> str:
    """
    Get the diff of staged changes.

    This function retrieves the diff of changes that have been staged for commit.
    It uses the `git diff --cached` command to get the relevant information.

    Returns:
        str: The diff of staged changes.
    """
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error: {result.stderr}")
    return result.stdout.strip()