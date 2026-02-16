# constants.py
# Purpose: Stores static values used throughout the project.
#
# Must NOT contain:
#   - Business logic
#   - Function definitions
#   - File I/O

from pathlib import Path

APP_NAME = "gita"

CONFIG_DIR = Path.home() / ".gita"
CONFIG_FILE = CONFIG_DIR / "config.toml"

KEYRING_SERVICE = "gita"

VALID_STYLES = ["conventional", "simple", "detailed"]
