# utils/console.py
# Purpose: Standardized output formatting.
#
# Example:
#   def print_error(message: str):
#       console.print(f"[red]{message}[/red]")

from rich.console import Console

console = Console()

def print_error(message: str):
    """
    Prints an error message in red.

    Args:
        message (str): The error message to print.
    """
    console.print(f"[red]{message}[/red]")

def print_success(message: str):
    """
    Prints a success message in green.

    Args:
        message (str): The success message to print.
    """
    console.print(f"[green]{message}[/green]")

def print_info(message: str):
    """
    Prints an informational message in blue.

    Args:
        message (str): The informational message to print.
    """
    console.print(f"[blue]{message}[/blue]")