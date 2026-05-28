#!/bin/bash
#
# progress-logger.sh - PostToolUse hook for progress logging reminders
#
# Triggers after Write/Edit operations to remind agents to update PROGRESS.md
# when working on tasks.
#
# Input: JSON via stdin with tool_name, tool_input, tool_result
# Output: JSON with optional systemMessage
#

set -euo pipefail

# Read JSON input from stdin
INPUT=$(cat)

# Extract relevant fields
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Only process Write and Edit operations
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  echo '{}'
  exit 0
fi

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
  echo '{}'
  exit 0
fi

# Skip temporary files, cache files, and non-significant changes
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
  *.tmp|*.log|*.cache|*.bak|.DS_Store|*.swp|*.pyc)
    echo '{}'
    exit 0
    ;;
esac

# Skip if file is in node_modules, .git, or other non-source directories
case "$FILE_PATH" in
  *node_modules*|*.git/*|*__pycache__*|*.cache/*|*dist/*|*build/*)
    echo '{}'
    exit 0
    ;;
esac

# Skip PROGRESS.md itself to avoid recursive reminders
if [[ "$BASENAME" == "PROGRESS.md" ]]; then
  echo '{}'
  exit 0
fi

# Skip PROMPT.md (session file)
if [[ "$BASENAME" == "PROMPT.md" ]]; then
  echo '{}'
  exit 0
fi

# Check if PROMPT.md exists (indicates task context)
PROMPT_FILE="$CWD/PROMPT.md"
if [[ ! -f "$PROMPT_FILE" ]]; then
  # Not in a task context, no reminder needed
  echo '{}'
  exit 0
fi

# Extract task directory from PROMPT.md
TASK_DIR=$(grep -oE 'tasks/[A-Z]+-[0-9]+-[^/]+/' "$PROMPT_FILE" 2>/dev/null | head -1 || true)

if [[ -z "$TASK_DIR" ]]; then
  echo '{}'
  exit 0
fi

# Check if PROGRESS.md exists for the task
PROGRESS_FILE="$CWD/$TASK_DIR/PROGRESS.md"
if [[ ! -f "$PROGRESS_FILE" ]]; then
  echo '{}'
  exit 0
fi

# Count significant file changes in this session
# This is a simple heuristic - track via environment or temp file in production
CHANGE_COUNT="${PROGRESS_LOGGER_CHANGE_COUNT:-0}"
CHANGE_COUNT=$((CHANGE_COUNT + 1))

# Only remind every 3-5 significant changes to avoid noise
if [[ $((CHANGE_COUNT % 4)) -ne 0 ]]; then
  echo '{}'
  exit 0
fi

# Build the system message
RELATIVE_PATH="${FILE_PATH#$CWD/}"
TASK_ID=$(echo "$TASK_DIR" | grep -oE '[A-Z]+-[0-9]+' | head -1)

cat << EOF
{
  "systemMessage": "Progress reminder: You've made several file changes including '$RELATIVE_PATH'. Consider updating PROGRESS.md for task $TASK_ID with your current checkpoint. Include: what was just completed, what comes next, and any blockers encountered."
}
EOF
