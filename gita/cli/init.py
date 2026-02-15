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
import keyring

from gita.constants import KEYRING_SERVICE
from gita.config.storage import save_config

def init_command():
    """
    Interactive setup wizard for Gita.

    This command guides the user through the initial configuration of Gita, including
    selecting an AI provider, entering API credentials, and setting preferences.

    Usage:
        gita init
    """

    provider = typer.prompt("Enter provider name")
    base_url = typer.prompt("Enter API base URL")
    model = typer.prompt("Enter model name")
    style = typer.prompt("Enter commit style (conventional/simple/detailed)")

    api_key = typer.prompt("Enter API key", hide_input=True)

    config_data = {
        "provider": provider,
        "base_url": base_url,
        "model": model,
        "style": style,
    }

    save_config(config_data)

    keyring.set_password(KEYRING_SERVICE, provider, api_key)

    typer.echo("Configuration saved successfully!")