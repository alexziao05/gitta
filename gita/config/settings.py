# config/settings.py
# Purpose: Load and validate configuration.
#
# Responsibilities:
#   - Read config file
#   - Validate required fields
#   - Return structured config object

from gita.config.storage import load_config


class Settings:
    def __init__(self):
        data = load_config()

        self.provider = data["provider"]
        self.base_url = data["base_url"]
        self.model = data["model"]
        self.style = data["style"]
