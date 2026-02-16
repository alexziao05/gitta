# git/diff.py
# Purpose: Retrieve git diffs.
#
# Responsibilities:
#   - Get staged diff
#   - Get last commit diff

import subprocess

from gitta.constants import DEFAULT_MAX_DIFF_CHARS


def get_staged_diff(max_chars: int = DEFAULT_MAX_DIFF_CHARS) -> tuple[str, bool]:
    """
    Get the diff of staged changes, truncating if too large.

    Returns:
        tuple: (diff_text, was_truncated)
    """
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    diff = result.stdout.strip()
    if len(diff) > max_chars:
        return diff[:max_chars], True
    return diff, False