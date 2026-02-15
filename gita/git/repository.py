# git/repository.py
# Purpose: General git operations.
#
# Responsibilities:
#   - Check git repo
#   - Stage files
#   - Commit
#   - Amend

import subprocess

class GitRepository:
    
    @staticmethod
    def is_git_repo() -> bool:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    @staticmethod
    def commit(message: str) -> None:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Error: {result.stderr}")
