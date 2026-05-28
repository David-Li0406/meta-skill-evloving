#!/usr/bin/env python3
"""
Agent Script LSP Validation Hook
================================

This PostToolUse hook validates .agent files after Write/Edit operations
using the Agent Script Language Server.

Behavior (Auto-fix loop):
- Outputs errors to Claude so it can automatically fix them
- Repeats until valid or max attempts reached
- Uses LSP only (fast ~50ms) for real-time feedback

Usage:
    Triggered automatically by hooks.json configuration
    Input: JSON from stdin with tool_name and tool_input
    Output: Diagnostic messages to stdout (or empty if valid)
"""

import json
import os
import sys
from pathlib import Path

# Add shared lsp-engine to path
SCRIPT_DIR = Path(__file__).parent
PLUGIN_ROOT = SCRIPT_DIR.parent.parent
LSP_ENGINE_PATH = PLUGIN_ROOT.parent / "shared" / "lsp-engine"
sys.path.insert(0, str(LSP_ENGINE_PATH))

# Track validation attempts to prevent infinite loops
ATTEMPT_FILE = Path("/tmp/agentscript_lsp_attempts.json")
MAX_ATTEMPTS = 3


def get_attempt_count(file_path: str) -> int:
    """Get the current attempt count for a file."""
    try:
        if ATTEMPT_FILE.exists():
            with open(ATTEMPT_FILE, "r") as f:
                attempts = json.load(f)
                return attempts.get(file_path, 0)
    except Exception:
        pass
    return 0


def increment_attempt_count(file_path: str) -> int:
    """Increment and return the attempt count for a file."""
    attempts = {}
    try:
        if ATTEMPT_FILE.exists():
            with open(ATTEMPT_FILE, "r") as f:
                attempts = json.load(f)
    except Exception:
        pass

    attempts[file_path] = attempts.get(file_path, 0) + 1
    count = attempts[file_path]

    try:
        with open(ATTEMPT_FILE, "w") as f:
            json.dump(attempts, f)
    except Exception:
        pass

    return count


def reset_attempt_count(file_path: str):
    """Reset attempt count when validation succeeds."""
    try:
        if ATTEMPT_FILE.exists():
            with open(ATTEMPT_FILE, "r") as f:
                attempts = json.load(f)
            if file_path in attempts:
                del attempts[file_path]
                with open(ATTEMPT_FILE, "w") as f:
                    json.dump(attempts, f)
    except Exception:
        pass


def main():
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No input or invalid JSON - skip validation
        sys.exit(0)

    # Extract file path
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Only validate .agent files
    if not file_path.endswith(".agent"):
        sys.exit(0)

    # Check if file exists
    if not os.path.exists(file_path):
        sys.exit(0)

    # Track attempts
    current_attempt = increment_attempt_count(file_path)

    # If max attempts exceeded, skip validation to avoid infinite loop
    if current_attempt > MAX_ATTEMPTS:
        print(f"⚠️ LSP validation: Maximum attempts ({MAX_ATTEMPTS}) exceeded for {file_path}")
        print("   Manual review may be required.")
        reset_attempt_count(file_path)  # Reset for next edit session
        sys.exit(0)

    # Try to import LSP engine
    try:
        from lsp_client import get_diagnostics, is_lsp_available
        from diagnostics import format_diagnostics_for_claude
    except ImportError as e:
        # LSP engine not available - skip validation silently
        # This allows the plugin to work even without LSP
        sys.exit(0)

    # Check if LSP is available
    if not is_lsp_available():
        # LSP not available - skip validation silently
        sys.exit(0)

    # Validate the file
    try:
        result = get_diagnostics(file_path)
    except Exception as e:
        # LSP error - report but don't block
        print(f"⚠️ LSP validation error: {e}")
        sys.exit(0)

    # Format output for Claude
    output = format_diagnostics_for_claude(
        result,
        file_path=file_path,
        max_attempts=MAX_ATTEMPTS,
        current_attempt=current_attempt,
    )

    # If valid, reset attempt counter
    if result.get("success", False):
        reset_attempt_count(file_path)

    # Output diagnostics (empty = success)
    if output:
        print(output)

    # Always exit 0 for auto-fix loop (don't block)
    sys.exit(0)


if __name__ == "__main__":
    main()
