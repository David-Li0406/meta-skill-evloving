#!/usr/bin/env python3
"""
Validates hook configuration JSON structure.
Usage: python3 validate_hook.py <hook_event> <hook_config_json>
"""

import json
import sys
from typing import Dict, Any, List

VALID_EVENTS = [
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
    "SubagentStop",
    "SessionStart",
    "SessionEnd",
    "Notification",
    "PreCompact",
]

EVENTS_WITH_MATCHERS = ["PreToolUse", "PostToolUse"]
EVENTS_WITH_SOURCE_MATCHER = ["SessionStart"]
EVENTS_WITH_TRIGGER_MATCHER = ["PreCompact"]

def validate_hook_event(event: str) -> List[str]:
    """Validate hook event name."""
    errors = []
    if event not in VALID_EVENTS:
        errors.append(f"Invalid hook event: {event}. Must be one of: {', '.join(VALID_EVENTS)}")
    return errors

def validate_matcher(event: str, matcher: str) -> List[str]:
    """Validate matcher configuration."""
    errors = []

    if event in EVENTS_WITH_MATCHERS:
        # Matcher should match tool names or patterns
        if not matcher:
            errors.append("Matcher can be empty string or '*' to match all tools")
    elif event in EVENTS_WITH_SOURCE_MATCHER:
        valid_sources = ["startup", "resume", "clear", "compact"]
        if matcher and matcher not in valid_sources:
            errors.append(f"Invalid SessionStart matcher: {matcher}. Must be one of: {', '.join(valid_sources)}")
    elif event in EVENTS_WITH_TRIGGER_MATCHER:
        valid_triggers = ["manual", "auto"]
        if matcher and matcher not in valid_triggers:
            errors.append(f"Invalid PreCompact matcher: {matcher}. Must be one of: {', '.join(valid_triggers)}")
    else:
        if matcher:
            errors.append(f"Event {event} does not support matchers. Remove the matcher field.")

    return errors

def validate_hook_config(event: str, config: Dict[str, Any]) -> List[str]:
    """Validate complete hook configuration structure."""
    errors = []

    # Check for required 'hooks' array
    if "hooks" not in config:
        errors.append("Missing required 'hooks' array in configuration")
        return errors

    hooks_array = config["hooks"]
    if not isinstance(hooks_array, list):
        errors.append("'hooks' must be an array")
        return errors

    # Validate each hook
    for i, hook in enumerate(hooks_array):
        if not isinstance(hook, dict):
            errors.append(f"Hook {i} must be an object")
            continue

        # Check required fields
        if "type" not in hook:
            errors.append(f"Hook {i}: Missing required 'type' field")
        elif hook["type"] != "command":
            errors.append(f"Hook {i}: Only 'command' type is currently supported")

        if "command" not in hook:
            errors.append(f"Hook {i}: Missing required 'command' field")
        elif not isinstance(hook["command"], str):
            errors.append(f"Hook {i}: 'command' must be a string")

        # Check optional timeout
        if "timeout" in hook:
            if not isinstance(hook["timeout"], (int, float)):
                errors.append(f"Hook {i}: 'timeout' must be a number")
            elif hook["timeout"] <= 0:
                errors.append(f"Hook {i}: 'timeout' must be positive")

    # Validate matcher if present
    if "matcher" in config:
        matcher_errors = validate_matcher(event, config["matcher"])
        errors.extend(matcher_errors)

    return errors

def validate_full_hooks_config(hooks_config: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate complete hooks configuration from settings.json."""
    all_errors = {}

    for event, event_configs in hooks_config.items():
        event_errors = validate_hook_event(event)
        if event_errors:
            all_errors[event] = event_errors
            continue

        if not isinstance(event_configs, list):
            all_errors[event] = ["Event configuration must be an array"]
            continue

        for i, config in enumerate(event_configs):
            config_errors = validate_hook_config(event, config)
            if config_errors:
                all_errors[f"{event}[{i}]"] = config_errors

    return all_errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_hook.py <hooks_config_json>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print('  python3 validate_hook.py \'{"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo test"}]}]}\'', file=sys.stderr)
        sys.exit(1)

    hooks_json = sys.argv[1]

    try:
        hooks_config = json.loads(hooks_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_full_hooks_config(hooks_config)

    if errors:
        print("❌ Validation failed:\n", file=sys.stderr)
        for location, error_list in errors.items():
            print(f"{location}:", file=sys.stderr)
            for error in error_list:
                print(f"  • {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ Hook configuration is valid")
        sys.exit(0)

if __name__ == "__main__":
    main()
