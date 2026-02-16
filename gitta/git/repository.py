# git/repository.py
# Purpose: General git operations.
#
# Responsibilities:
#   - Check git repo
#   - Stage files
#   - Commit
#   - Push
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
            raise RuntimeError(result.stderr.strip())

    @staticmethod
    def revert_last_commit() -> None:
        result = subprocess.run(
            ["git", "reset", "--soft", "HEAD~1"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @staticmethod
    def get_current_branch() -> str:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip()

    @staticmethod
    def push() -> None:
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

    @staticmethod
    def get_default_branch() -> str:
        """Detect the default branch (main or master)."""
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split("/")[-1]

        for branch in ["main", "master"]:
            check = subprocess.run(
                ["git", "rev-parse", "--verify", f"refs/heads/{branch}"],
                capture_output=True,
                text=True
            )
            if check.returncode == 0:
                return branch

        raise RuntimeError("Could not detect default branch. Specify with --base.")

    @staticmethod
    def get_commits_between(base: str, head: str = "HEAD") -> str:
        """Get commit log between base and head."""
        result = subprocess.run(
            ["git", "log", "--oneline", f"{base}..{head}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip()

    @staticmethod
    def get_diff_between(base: str, head: str = "HEAD") -> str:
        """Get the full diff between base and head."""
        result = subprocess.run(
            ["git", "diff", f"{base}...{head}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip()

    @staticmethod
    def get_diff_stat(base: str, head: str = "HEAD") -> str:
        """Get a compact diffstat summary between base and head."""
        result = subprocess.run(
            ["git", "diff", "--stat", f"{base}...{head}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip()

    @staticmethod
    def push_with_upstream(branch: str) -> None:
        """Push and set upstream tracking."""
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
