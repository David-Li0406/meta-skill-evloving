#!/bin/bash
# Log tool execution results
# This hook demonstrates PostToolUse logging for all tools

# Read the hook input from stdin
INPUT=$(cat)

# Extract tool info
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_result // {}')

# Log to stderr (doesn't affect hook result)
echo "skill-with-hooks: PostToolUse - tool=$TOOL_NAME" >&2

# Create a log file in /tmp for verification
LOG_FILE="/tmp/skill-hooks-test.log"
echo "$(date -Iseconds) POST $TOOL_NAME" >> "$LOG_FILE"

# Continue without blocking
exit 0
