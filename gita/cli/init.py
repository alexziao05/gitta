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

def init_command():
    """
    Interactive setup wizard for Gita.

    This command guides the user through the initial configuration of Gita, including
    selecting an AI provider, entering API credentials, and setting preferences.

    Usage:
        gita init
    """
    