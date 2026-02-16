# cli/log.py
# Purpose: Handles `gitta log`.
#
# Responsibilities:
#   - Show recent git commits with formatted output

import subprocess
import typer

from gitta.git.repository import GitRepository
from gitta.utils.console import console, print_error

from rich.table import Table


def log_command(
    count: int = typer.Option(10, "--count", "-n", help="Number of commits to show."),
):
    """Show recent commits in a formatted table."""

    if not GitRepository.is_git_repo():
        print_error("Error: Not inside a Git repository.")
        raise typer.Exit(code=1)

    result = subprocess.run(
        ["git", "log", f"-{count}", "--pretty=format:%h|%s|%an|%ar"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print_error(f"Error: {result.stderr.strip()}")
        raise typer.Exit(code=1)

    lines = result.stdout.strip().split("\n")
    if not lines or lines == [""]:
        print_error("No commits found.")
        raise typer.Exit(code=0)

    table = Table(title="Recent Commits", show_lines=False)
    table.add_column("Hash", style="yellow", width=8)
    table.add_column("Message", style="white")
    table.add_column("Author", style="cyan")
    table.add_column("When", style="green")

    for line in lines:
        parts = line.split("|", 3)
        if len(parts) == 4:
            table.add_row(parts[0], parts[1], parts[2], parts[3])

    console.print(table)
