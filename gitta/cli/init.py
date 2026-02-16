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

from gitta.constants import CONFIG_FILE, KEYRING_SERVICE, VALID_STYLES
from gitta.config.storage import load_config, save_config
from gitta.utils.console import print_error, print_info, print_success

def _prompt_required(label: str, default: str = "") -> str:
    while True:
        value = typer.prompt(label, default=default).strip()
        if value:
            return value
        print_error("This field cannot be empty.")

def init_command():
    """
    Interactive setup wizard for Gitta.

    This command guides the user through the initial configuration of Gitta, including
    selecting an AI provider, entering API credentials, and setting preferences.

    Usage:
        gitta init
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

    provider = _prompt_required("Enter provider name", default=existing.get("provider") or "")
    base_url = _prompt_required("Enter API base URL", default=existing.get("base_url") or "")
    model = _prompt_required("Enter model name", default=existing.get("model") or "")
    style = typer.prompt(
        "Enter commit style",
        default=existing.get("style") or "conventional",
        type=click.Choice(VALID_STYLES),
    )

    if existing_key:
        new_key = typer.prompt("Enter API key (leave blank to keep existing)", default="", hide_input=True)
        api_key = new_key if new_key else existing_key
    else:
        while True:
            api_key = typer.prompt("Enter API key", hide_input=True).strip()
            if api_key:
                break
            print_error("API key cannot be empty.")

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