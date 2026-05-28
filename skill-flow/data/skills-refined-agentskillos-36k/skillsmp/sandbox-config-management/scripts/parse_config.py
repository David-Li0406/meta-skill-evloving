#!/usr/bin/env python3
"""
Parse Sandbox.toml configuration file.

Usage:
    python3 parse_config.py /path/to/Sandbox.toml

Output: JSON representation of configuration
"""

import json
import sys
from pathlib import Path

try:
    import tomli as toml
except ImportError:
    try:
        import tomllib as toml
    except ImportError:
        import toml


def parse_config(config_path: str) -> dict:
    """
    Parse Sandbox.toml file.

    Args:
        config_path: Path to Sandbox.toml

    Returns:
        Dict with configuration
    """
    path = Path(config_path).resolve()

    if not path.exists():
        return {"error": f"File not found: {config_path}"}

    try:
        with open(path, "rb") as f:
            config = toml.load(f)
        return config
    except Exception as e:
        return {"error": f"Failed to parse TOML: {e}"}


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_config.py /path/to/Sandbox.toml", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]
    result = parse_config(config_path)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
