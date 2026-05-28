#!/bin/bash
# Hook Script Template
# Description: [What this hook does]
# Event: [PreToolUse/PostToolUse/SessionStart/etc]
# Matcher: [Tool name if applicable]

# Exit on error
set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

# Add configuration variables here
PROTECTED_FILES=(".env" "secrets.json")
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/logs/hook.log"

# ============================================================================
# INPUT PARSING
# ============================================================================

# Read JSON input from stdin
INPUT=$(cat)

# Parse fields from JSON
# Using basic string manipulation (jq is better if available)
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
SESSION_ID=$(echo "$INPUT" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
CWD=$(echo "$INPUT" | grep -o '"cwd":"[^"]*"' | cut -d'"' -f4)

# Tool-specific fields (uncomment as needed)
# FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
# COMMAND=$(echo "$INPUT" | grep -o '"command":"[^"]*"' | sed 's/"command":"//;s/"$//')

# Debug: Log parsed values (optional, comment out in production)
# echo "Tool: $TOOL_NAME" >&2
# echo "Session: $SESSION_ID" >&2

# ============================================================================
# VALIDATION
# ============================================================================

# Add validation logic here
# Example: Check if this is the right tool
# if [[ "$TOOL_NAME" != "Write" ]]; then
#   exit 0  # Not our target tool, allow operation
# fi

# Example: Validate required fields
# if [[ -z "$FILE_PATH" ]]; then
#   echo "Error: file_path not found in input" >&2
#   exit 0  # Fail safely
# fi

# ============================================================================
# SECURITY CHECKS
# ============================================================================

# Add security validation here
# Example: Block path traversal
# if [[ "$FILE_PATH" =~ \.\. ]]; then
#   echo "🚫 BLOCKED: Path traversal detected: $FILE_PATH" >&2
#   exit 2  # Block operation
# fi

# Example: Check for protected files
# for protected in "${PROTECTED_FILES[@]}"; do
#   if [[ "$FILE_PATH" == *"$protected"* ]]; then
#     echo "⚠️ WARNING: Accessing protected file: $FILE_PATH" >&2
#     # Decide: warn (exit 0) or block (exit 2)
#   fi
# done

# ============================================================================
# MAIN LOGIC
# ============================================================================

# Add your hook logic here
# Examples:
# - Validate input
# - Check conditions
# - Log operations
# - Transform data
# - Send notifications

# Example: Simple logging
# echo "$(date): Hook executed for $TOOL_NAME" >> "$LOG_FILE"

# Example: Conditional warning
# if [[ "$COMMAND" == *"rm -rf"* ]]; then
#   echo "⚠️ WARNING: Destructive command detected" >&2
# fi

# ============================================================================
# OUTPUT
# ============================================================================

# For PreToolUse hooks that need to modify input or provide context:
# You can output JSON to stdout (optional)
# Example:
# cat <<EOF
# {
#   "decision": "allow",
#   "additionalContext": "This is additional context for Claude"
# }
# EOF

# For blocking (PreToolUse only):
# echo "Operation blocked: [reason]" >&2
# exit 2

# For allowing operation (default):
exit 0

# ============================================================================
# NOTES
# ============================================================================
# - Use ">&2" to output to stderr (visible to user)
# - Quote all variables: "$VAR" not $VAR
# - Exit 0: Allow operation
# - Exit 2: Block operation (PreToolUse only)
# - Other exit codes: Non-blocking error
# - Use $CLAUDE_PROJECT_DIR for portable paths
# - Test independently: cat test-input.json | ./hook-script.sh
# - Check permissions: chmod +x hook-script.sh
