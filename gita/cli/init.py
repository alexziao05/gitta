# cli/init.py
# Purpose: Interactive setup wizard.
#
# Responsibilities:
#   - Prompt for provider
#   - Prompt for base URL
#   - Prompt for model
#   - Prompt for commit style
#   - Prompt for API key
#   - Call config storage layer

import typer
import click
import keyring

from gita.constants import CONFIG_FILE, KEYRING_SERVICE
from gita.config.storage import load_config, save_config
from gita.utils.console import print_info, print_success

def init_command():
    """
    Interactive setup wizard for Gita.

    This command guides the user through the initial configuration of Gita, including
    selecting an AI provider, entering API credentials, and setting preferences.

    Usage:
        gita init
    """

    existing = {}
    existing_key = None

    if CONFIG_FILE.exists():
        existing = load_config()
        existing_provider = existing.get("provider", "")
        existing_key = keyring.get_password(KEYRING_SERVICE, existing_provider) if existing_provider else None

        print_info("Existing configuration found.")

        action = typer.prompt(
            "Would you like to reset or edit the existing config?",
            type=click.Choice(["reset", "edit"]),
        )

        if action == "reset":
            existing = {}
            existing_key = None

    provider = typer.prompt("Enter provider name", default=existing.get("provider") or "")
    base_url = typer.prompt("Enter API base URL", default=existing.get("base_url") or "")
    model = typer.prompt("Enter model name", default=existing.get("model") or "")
    style = typer.prompt("Enter commit style (conventional/simple/detailed)", default=existing.get("style") or "")

    if existing_key:
        new_key = typer.prompt("Enter API key (leave blank to keep existing)", default="", hide_input=True)
        api_key = new_key if new_key else existing_key
    else:
        api_key = typer.prompt("Enter API key", hide_input=True)

    config_data = {
        "provider": provider,
        "base_url": base_url,
        "model": model,
        "style": style,
    }

    save_config(config_data)

    if api_key:
        keyring.set_password(KEYRING_SERVICE, provider, api_key)

    print_success("Configuration saved successfully!")