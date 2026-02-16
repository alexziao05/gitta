# config/settings.py
# Purpose: Load and validate configuration.
#
# Responsibilities:
#   - Read config file
#   - Validate required fields
#   - Return structured config object

import keyring

from gita.config.storage import load_config
from gita.constants import KEYRING_SERVICE, VALID_STYLES

REQUIRED_FIELDS = ["provider", "base_url", "model", "style"]


class Settings:
    def __init__(self):
        data = load_config()

        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            raise RuntimeError(
                f"Missing config field(s): {', '.join(missing)}. Run 'gita init' to fix."
            )

        if data["style"] not in VALID_STYLES:
            raise RuntimeError(
                f"Invalid commit style '{data['style']}'. Must be one of: {', '.join(VALID_STYLES)}. Run 'gita init' to fix."
            )

        self.provider = data["provider"]
        self.base_url = data["base_url"]
        self.model = data["model"]
        self.style = data["style"]

    def validate_api_key(self) -> None:
        """Check that an API key exists in keyring for this provider."""
        api_key = keyring.get_password(KEYRING_SERVICE, self.provider)
        if not api_key:
            raise RuntimeError(
                f"API key not found for '{self.provider}'. Run 'gita init' to configure."
            )
