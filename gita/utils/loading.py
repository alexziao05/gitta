from contextlib import contextmanager
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

console = Console()

@contextmanager
def show_loading(text: str = "Loading..."):
    """
    Displays a spinner while executing a block of code.

    Usage:
        with show_loading("Generating..."):
            do_something()
    """
    spinner = Spinner("dots", text=text)

    with Live(spinner, refresh_per_second=12, console=console):
        yield
