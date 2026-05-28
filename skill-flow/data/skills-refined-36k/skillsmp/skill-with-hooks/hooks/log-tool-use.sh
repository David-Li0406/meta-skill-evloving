#!/bin/bash
# Log tool invocations
# This hook demonstrates PreToolUse logging for all tools

# Read the hook input from stdin
INPUT=$(cat)

# Extract tool info
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')

# Log to stderr (doesn't affect hook result)
echo "skill-with-hooks: PreToolUse - tool=$TOOL_NAME session=$SESSION_ID" >&2

# Create a log file in /tmp for verification
LOG_FILE="/tmp/skill-hooks-test.log"
echo "$(date -Iseconds) PRE  $TOOL_NAME" >> "$LOG_FILE"

# Continue without blocking
exit 0
