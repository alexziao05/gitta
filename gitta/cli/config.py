# cli/config.py
# Purpose: Handles `gitta config`.
#
# Responsibilities:
#   - List all config values
#   - Get a single config value
#   - Set a single config value

import typer

from gitta.config.storage import load_config, save_config
from gitta.constants import CONFIG_FILE, VALID_STYLES
from gitta.utils.console import print_error, print_info, print_success

config_app = typer.Typer(help="View or update configuration.")


ALLOWED_KEYS = ["provider", "base_url", "model", "style", "api_key", "max_diff_chars"]


@config_app.command(name="list")
def config_list():
    """Show all configuration values."""
    if not CONFIG_FILE.exists():
        print_error("No configuration found. Run 'gitta init' first.")
        raise typer.Exit(code=1)

    data = load_config()
    for key, value in data.items():
        if key == "api_key":
            masked = "*" * (len(value) - 4) + value[-4:] if len(value) > 4 else "****"
            print_info(f"{key} = {masked}")
        else:
            print_info(f"{key} = {value}")


@config_app.command(name="get")
def config_get(key: str = typer.Argument(..., help="Config key to read.")):
    """Get a single configuration value."""
    if not CONFIG_FILE.exists():
        print_error("No configuration found. Run 'gitta init' first.")
        raise typer.Exit(code=1)

    data = load_config()
    if key not in data:
        print_error(f"Unknown config key: '{key}'. Available keys: {', '.join(ALLOWED_KEYS)}")
        raise typer.Exit(code=1)

    if key == "api_key":
        api_key = data.get("api_key", "")
        if api_key:
            masked = "*" * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else "****"
            print_info(f"api_key = {masked}")
        else:
            print_error("No API key found.")
        return

    print_info(f"{key} = {data[key]}")


@config_app.command(name="set")
def config_set(
    key: str = typer.Argument(..., help="Config key to update."),
    value: str = typer.Argument(..., help="New value."),
):
    """Set a single configuration value."""
    if not CONFIG_FILE.exists():
        print_error("No configuration found. Run 'gitta init' first.")
        raise typer.Exit(code=1)

    if key not in ALLOWED_KEYS:
        print_error(f"Unknown config key: '{key}'. Available keys: {', '.join(ALLOWED_KEYS)}")
        raise typer.Exit(code=1)

    if key == "style" and value not in VALID_STYLES:
        print_error(f"Invalid style '{value}'. Must be one of: {', '.join(VALID_STYLES)}")
        raise typer.Exit(code=1)

    if key == "max_diff_chars":
        try:
            int_val = int(value)
            if int_val <= 0:
                raise ValueError
        except ValueError:
            print_error("max_diff_chars must be a positive integer.")
            raise typer.Exit(code=1)

    data = load_config()
    data[key] = int(value) if key == "max_diff_chars" else value
    save_config(data)
    print_success(f"{key} updated.")
