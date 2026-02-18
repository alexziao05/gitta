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

VALID_STYLES = ["conventional", "simple", "detailed"]

DEFAULT_MAX_DIFF_CHARS = 32000  # ~8k tokens, safe for most models

DEFAULT_MULTI_FILE = False