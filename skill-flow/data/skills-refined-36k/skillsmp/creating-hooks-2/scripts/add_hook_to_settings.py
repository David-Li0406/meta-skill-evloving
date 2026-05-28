#!/usr/bin/env python3
"""
Safely adds hook configuration to settings.json file.
Usage: python3 add_hook_to_settings.py <settings_path> <hook_event> <hook_config_json>
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

def load_settings(settings_path: Path) -> Dict[str, Any]:
    """Load existing settings or return empty dict."""
    if settings_path.exists():
        try:
            with open(settings_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {settings_path}: {e}", file=sys.stderr)
            sys.exit(1)
    return {}

def save_settings(settings_path: Path, settings: Dict[str, Any]) -> None:
    """Save settings with proper formatting."""
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
        f.write('\n')  # Add trailing newline

def add_hook(settings: Dict[str, Any], event: str, hook_config: Dict[str, Any]) -> Dict[str, Any]:
    """Add hook configuration to settings."""
    if "hooks" not in settings:
        settings["hooks"] = {}

    if event not in settings["hooks"]:
        settings["hooks"][event] = []

    # Add the new hook configuration
    settings["hooks"][event].append(hook_config)

    return settings

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 add_hook_to_settings.py <settings_path> <hook_event> <hook_config_json>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print('  python3 add_hook_to_settings.py ~/.claude/settings.json PreToolUse \'{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo test"}]}\'', file=sys.stderr)
        sys.exit(1)

    settings_path = Path(sys.argv[1]).expanduser()
    event = sys.argv[2]
    hook_config_json = sys.argv[3]

    try:
        hook_config = json.loads(hook_config_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid hook configuration JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate hook config structure
    if "hooks" not in hook_config:
        print("ERROR: Hook configuration must contain 'hooks' array", file=sys.stderr)
        sys.exit(1)

    # Load existing settings
    print(f"Loading settings from {settings_path}...")
    settings = load_settings(settings_path)

    # Add hook
    print(f"Adding {event} hook...")
    settings = add_hook(settings, event, hook_config)

    # Save settings
    print(f"Saving settings to {settings_path}...")
    save_settings(settings_path, settings)

    print(f"✅ Successfully added {event} hook to {settings_path}")
    print("\nNote: Restart Claude Code or run /hooks to reload hook configuration")

if __name__ == "__main__":
    main()
