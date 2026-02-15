# config/storage.py
# Purpose: Handle filesystem operations for configuration.
#
# Responsibilities:
#   - Create config directory
#   - Save config file
#   - Delete config
#   - Set file permissions

import tomllib 
import tomli_w
from gita.constants import CONFIG_DIR, CONFIG_FILE

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def save_config(data: dict):
    """Save configuration data to the config file."""
    ensure_config_dir()
    with open (CONFIG_FILE, "wb") as f:
        f.write(tomli_w.dumps(data).encode())

def load_config() -> dict:
    """Load configuration data from the config file."""
    if not CONFIG_FILE.exists():
        raise RuntimeError("Configuration file not found. Please run 'gita init' to set up your configuration.")
    
    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)