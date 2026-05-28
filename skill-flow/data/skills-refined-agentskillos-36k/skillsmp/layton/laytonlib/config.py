"""Configuration loading and management.

Config is stored at .layton/config.json relative to git root (or cwd if not in git).
Implements a simple key-value store with dot-notation access.
"""

import json
import subprocess
from pathlib import Path
from typing import Any

from laytonlib.formatters import OutputFormatter


def find_git_root() -> Path | None:
    """Find the git repository root, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_layton_dir() -> Path:
    """Get the .layton directory path (in git root or cwd)."""
    git_root = find_git_root()
    base = git_root if git_root else Path.cwd()
    return base / ".layton"


def get_config_path() -> Path:
    """Get the config.json path."""
    return get_layton_dir() / "config.json"


def get_default_config() -> dict:
    """Get default configuration values."""
    # Try to detect system timezone
    try:
        from datetime import datetime

        tz = datetime.now().astimezone().tzinfo
        timezone = str(tz) if tz else "UTC"
    except Exception:
        timezone = "UTC"

    return {
        "timezone": timezone,
        "work": {
            "schedule": {
                "start": "09:00",
                "end": "17:00",
            }
        },
    }


def load_config() -> dict | None:
    """Load config from file. Returns None if not found."""
    config_path = get_config_path()
    if not config_path.exists():
        return None
    try:
        with open(config_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_config(config: dict) -> bool:
    """Save config to file. Returns True on success."""
    config_path = get_config_path()
    layton_dir = get_layton_dir()

    try:
        layton_dir.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except OSError:
        return False


def get_nested(data: dict, key: str) -> Any:
    """Get a value using dot-notation.

    Args:
        data: The config dictionary
        key: Dot-notation key (e.g., "work.schedule.start")

    Returns:
        The value at the key path

    Raises:
        KeyError: If key not found
    """
    parts = key.split(".")
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(f"Key not found: {key}")

    return current


def set_nested(data: dict, key: str, value: Any) -> None:
    """Set a value using dot-notation, creating nested dicts as needed.

    Args:
        data: The config dictionary (modified in place)
        key: Dot-notation key (e.g., "work.schedule.start")
        value: The value to set
    """
    parts = key.split(".")
    current = data

    # Navigate/create path to parent
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        elif not isinstance(current[part], dict):
            # Replace non-dict value with dict
            current[part] = {}
        current = current[part]

    # Set the final key
    current[parts[-1]] = value


def collect_keys(data: dict, prefix: str = "") -> list[str]:
    """Collect all dot-notation paths in a nested dict.

    Args:
        data: The config dictionary
        prefix: Current path prefix

    Returns:
        List of all dot-notation paths
    """
    keys = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            # Recurse into nested dict
            keys.extend(collect_keys(value, full_key))
        else:
            # Leaf node
            keys.append(full_key)
    return keys


def parse_value(value_str: str) -> Any:
    """Parse a value string, attempting JSON if possible.

    Args:
        value_str: The string value

    Returns:
        Parsed value (JSON object/array/bool/number) or original string
    """
    # Try to parse as JSON
    try:
        return json.loads(value_str)
    except json.JSONDecodeError:
        # Return as string
        return value_str


def run_config(
    formatter: OutputFormatter,
    command: str,
    key: str | None = None,
    value: str | None = None,
    force: bool = False,
) -> int:
    """Run a config subcommand.

    Args:
        formatter: Output formatter
        command: Subcommand (init, show, keys, get, set)
        key: Key for get/set commands
        value: Value for set command
        force: Force overwrite for init

    Returns:
        Exit code (0=success, 1=error)
    """
    if command == "init":
        return _config_init(formatter, force)
    elif command == "show":
        return _config_show(formatter)
    elif command == "keys":
        return _config_keys(formatter)
    elif command == "get":
        return _config_get(formatter, key)
    elif command == "set":
        return _config_set(formatter, key, value)
    else:
        formatter.error("UNKNOWN_COMMAND", f"Unknown config command: {command}")
        return 1


def _config_init(formatter: OutputFormatter, force: bool) -> int:
    """Create config with defaults."""
    config_path = get_config_path()

    if config_path.exists() and not force:
        formatter.error(
            "CONFIG_EXISTS",
            f"Config already exists at {config_path}",
            next_steps=["Use --force to overwrite"],
        )
        return 1

    config = get_default_config()
    if save_config(config):
        formatter.success(
            {"created": str(config_path), "config": config},
            next_steps=["Run 'layton config show' to view config"],
        )
        return 0
    else:
        formatter.error(
            "WRITE_FAILED",
            f"Failed to write config to {config_path}",
        )
        return 1


def _config_show(formatter: OutputFormatter) -> int:
    """Display entire config."""
    config = load_config()
    if config is None:
        formatter.error(
            "CONFIG_MISSING",
            "Config not found. Run 'layton config init' to create it.",
            next_steps=["layton config init"],
        )
        return 1

    formatter.success({"config": config})
    return 0


def _config_keys(formatter: OutputFormatter) -> int:
    """List all config keys in dot-notation."""
    config = load_config()
    if config is None:
        formatter.error(
            "CONFIG_MISSING",
            "Config not found. Run 'layton config init' to create it.",
            next_steps=["layton config init"],
        )
        return 1

    keys = collect_keys(config)
    formatter.success({"keys": sorted(keys)})
    return 0


def _config_get(formatter: OutputFormatter, key: str | None) -> int:
    """Get a config value."""
    if not key:
        formatter.error("MISSING_KEY", "Key is required for 'config get'")
        return 1

    config = load_config()
    if config is None:
        formatter.error(
            "CONFIG_MISSING",
            "Config not found. Run 'layton config init' to create it.",
            next_steps=["layton config init"],
        )
        return 1

    try:
        value = get_nested(config, key)
        formatter.success({"key": key, "value": value})
        return 0
    except KeyError:
        formatter.error(
            "KEY_NOT_FOUND",
            f"Key '{key}' not found in config",
            next_steps=["Run 'layton config keys' to see available keys"],
        )
        return 1


def _config_set(formatter: OutputFormatter, key: str | None, value: str | None) -> int:
    """Set a config value."""
    if not key:
        formatter.error("MISSING_KEY", "Key is required for 'config set'")
        return 1
    if value is None:
        formatter.error("MISSING_VALUE", "Value is required for 'config set'")
        return 1

    config = load_config()
    if config is None:
        formatter.error(
            "CONFIG_MISSING",
            "Config not found. Run 'layton config init' to create it.",
            next_steps=["layton config init"],
        )
        return 1

    # Parse value (JSON if valid, otherwise string)
    parsed_value = parse_value(value)

    # Set the value
    set_nested(config, key, parsed_value)

    # Save
    if save_config(config):
        formatter.success(
            {"key": key, "value": parsed_value, "config": config},
        )
        return 0
    else:
        formatter.error("WRITE_FAILED", "Failed to write config")
        return 1
