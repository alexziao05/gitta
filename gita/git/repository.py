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
    def get_staged_files() -> list[str]:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True
        )
        return [f for f in result.stdout.strip().split("\n") if f]

    @staticmethod
    def unstage_files(files: list[str]) -> None:
        result = subprocess.run(
            ["git", "reset", "HEAD", "--"] + files,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @staticmethod
    def stage_files(files: list[str]) -> None:
        result = subprocess.run(
            ["git", "add"] + files,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @staticmethod
    def commit(message: str) -> None:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Error: {result.stderr}")
