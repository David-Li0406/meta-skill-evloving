#!/bin/bash
#
# Push Session Start Hook for Claude Code
#
# This hook runs at the start of each Claude Code session and checks
# for active tasks from the Push iOS app.
#
# Updates are handled automatically by Claude Code's marketplace system.
#

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Check for active tasks
COUNT=$(python3 "$PLUGIN_DIR/scripts/check_tasks.py" 2>/dev/null)

# If script failed (e.g., no API key configured), exit silently
if [ $? -ne 0 ]; then
    exit 0
fi

# Only output if there are tasks
if [ -n "$COUNT" ] && [ "$COUNT" -gt 0 ]; then
    if [ "$COUNT" -eq 1 ]; then
        echo "[Push] You have 1 active task from your iPhone. Say 'push-todo' to see it."
    else
        echo "[Push] You have $COUNT active tasks from your iPhone. Say 'push-todo' to see them."
    fi
fi
