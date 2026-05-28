#!/bin/bash
# Validate bash commands before execution
# This hook demonstrates PreToolUse validation for Bash tool

# Read the hook input from stdin
INPUT=$(cat)

# Extract the command from the input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
    # No command found, allow
    exit 0
fi

# Log that we're validating
echo "skill-with-hooks: Validating bash command" >&2

# Check for dangerous patterns (example validation)
DANGEROUS_PATTERNS=(
    "rm -rf /"
    ":(){ :|:& };:"
    "> /dev/sda"
    "mkfs"
    "dd if=/dev/zero"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        # Block dangerous command
        echo '{"decision": "block", "reason": "skill-with-hooks: Blocked potentially dangerous command pattern"}'
        exit 2
    fi
done

# Command is safe, continue
exit 0
