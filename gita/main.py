# main.py
# Purpose: CLI entry point. Registers commands using Typer.
#
# Responsibilities:
#   - Create Typer app
#   - Attach subcommands
#   - No business logic

import typer

from gita.cli.add import add_command
from gita.cli.commit import commit_command
from gita.cli.doctor import doctor_command
from gita.cli.init import init_command
from gita.cli.ship import ship_command

app = typer.Typer(help="Gita - AI-powered Git commit message generator")

app.command(name="add")(add_command)
app.command(name="commit")(commit_command)
app.command(name="doctor")(doctor_command)
app.command(name="init")(init_command)
app.command(name="ship")(ship_command)

if __name__ == "__main__":
    app()