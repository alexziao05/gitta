# cli/doctor.py
# Purpose: Handles `gita doctor`.
#
# Responsibilities:
#   - Check git installation
#   - Check config file
#   - Check API key
#   - Check provider connectivity
#   - Check model availability

import shutil
import keyring

from gita.constants import CONFIG_FILE, KEYRING_SERVICE
from gita.config.storage import load_config
from gita.git.repository import GitRepository
from gita.utils.console import print_error, print_info, print_success

def doctor_command():
    """
    Diagnose common issues with your Gita setup.

    Checks git, configuration, API key, provider connectivity,
    and model availability.

    Usage:
        gita doctor
    """

    print_info("Running diagnostics...\n")
    all_passed = True

    # 1. Check git is installed
    if shutil.which("git"):
        print_success("[OK] Git is installed")
    else:
        print_error("[FAIL] Git is not installed")
        all_passed = False

    # 2. Check inside a git repo
    if GitRepository.is_git_repo():
        print_success("[OK] Inside a Git repository")
    else:
        print_error("[FAIL] Not inside a Git repository")
        all_passed = False

    # 3. Check config file exists
    if not CONFIG_FILE.exists():
        print_error("[FAIL] Config file not found. Run 'gita init' to set up.")
        all_passed = False
        return

    print_success(f"[OK] Config file found at {CONFIG_FILE}")

    # 4. Load and validate config
    try:
        config = load_config()
    except Exception as e:
        print_error(f"[FAIL] Could not read config: {e}")
        return

    required_fields = ["provider", "base_url", "model", "style"]
    for field in required_fields:
        if config.get(field):
            print_success(f"[OK] Config field '{field}' is set: {config[field]}")
        else:
            print_error(f"[FAIL] Config field '{field}' is missing or empty")
            all_passed = False

    # 5. Check API key in keyring
    provider = config.get("provider", "")
    api_key = keyring.get_password(KEYRING_SERVICE, provider) if provider else None

    if api_key:
        print_success(f"[OK] API key found in keyring for '{provider}'")
    else:
        print_error(f"[FAIL] No API key found in keyring for '{provider}'. Run 'gita init'.")
        all_passed = False
        return

    # 6. Check provider connectivity and model availability
    base_url = config.get("base_url", "")
    model = config.get("model", "")

    if base_url and model and api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=base_url)
            client.models.retrieve(model)
            print_success(f"[OK] Model '{model}' is available from provider")
        except Exception as e:
            print_error(f"[FAIL] Could not reach provider or model: {e}")
            all_passed = False

    # Summary
    if all_passed:
        print_success("\nAll checks passed!")
    else:
        print_error("\nSome checks failed. Review the issues above.")
