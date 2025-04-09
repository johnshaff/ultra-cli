import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".ultra")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
APP_WORKING_DIR = '/Users/johnshaff/Documents/dev'

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    ensure_config_dir()
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config_dict):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

def get_api_key(provider_name="openai"):
    """
    Fetches the API key from config, environment, or user prompt.
    """
    config = load_config()
    key = config.get(provider_name, {}).get("api_key")

    # Check environment variable, e.g. OPENAI_API_KEY
    env_key = os.getenv("OPENAI_API_KEY") if provider_name == "openai" else None
    if env_key:
        key = env_key

    # If not found, prompt the user
    if not key:
        key = input(f"Enter your API key for {provider_name}: ").strip()
        # Optionally store it in config for future use
        config.setdefault(provider_name, {})["api_key"] = key
        save_config(config)

    return key