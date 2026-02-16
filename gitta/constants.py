# constants.py
# Purpose: Stores static values used throughout the project.
#
# Must NOT contain:
#   - Business logic
#   - Function definitions
#   - File I/O

from pathlib import Path

APP_NAME = "gitta"

CONFIG_DIR = Path.home() / ".gitta"
CONFIG_FILE = CONFIG_DIR / "config.toml"

KEYRING_SERVICE = "gitta"

VALID_STYLES = ["conventional", "simple", "detailed"]
