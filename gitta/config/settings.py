# config/settings.py
# Purpose: Load and validate configuration.
#
# Responsibilities:
#   - Read config file
#   - Validate required fields
#   - Return structured config object

from gitta.config.storage import load_config
from gitta.constants import DEFAULT_MAX_DIFF_CHARS, DEFAULT_MULTI_FILE, VALID_STYLES

REQUIRED_FIELDS = ["provider", "base_url", "model", "style"]


class Settings:
    def __init__(self):
        data = load_config()

        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            raise RuntimeError(
                f"Missing config field(s): {', '.join(missing)}. Run 'gitta init' to fix."
            )

        if data["style"] not in VALID_STYLES:
            raise RuntimeError(
                f"Invalid commit style '{data['style']}'. Must be one of: {', '.join(VALID_STYLES)}. Run 'gitta init' to fix."
            )

        self.provider = data["provider"]
        self.base_url = data["base_url"]
        self.model = data["model"]
        self.style = data["style"]
        self.api_key = data.get("api_key", "")
        self.max_diff_chars = int(data.get("max_diff_chars", DEFAULT_MAX_DIFF_CHARS))
        self.multi_file = bool(data.get("multi_file", DEFAULT_MULTI_FILE))

    def validate_api_key(self) -> None:
        """Check that an API key exists in the config."""
        if not self.api_key:
            raise RuntimeError(
                "API key not found. Run 'gitta init' to configure."
            )
