#!/bin/bash
#
# validate-index-hook.sh - PostToolUse hook to validate INDEX.md after edits
#
# This hook runs after Write/Edit operations and validates INDEX.md
# if it was the file being modified.
#
# Environment variables from Claude Code:
#   TOOL_NAME - The tool that was used (Write, Edit)
#   TOOL_INPUT - JSON of tool parameters
#   TOOL_OUTPUT - JSON of tool result
#   CLAUDE_PLUGIN_ROOT - Plugin root directory
#

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATE_SCRIPT="$SCRIPT_DIR/../scripts/validate-index.sh"

# Check if we have tool input
if [[ -z "${TOOL_INPUT:-}" ]]; then
  exit 0
fi

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' || echo "")

# Only validate if the file is INDEX.md
if [[ ! "$FILE_PATH" =~ tasks/INDEX\.md$ ]]; then
  exit 0
fi

# Check if the file exists
if [[ ! -f "$FILE_PATH" ]]; then
  exit 0
fi

# Run validation
VALIDATION_OUTPUT=$("$VALIDATE_SCRIPT" "$FILE_PATH" 2>&1) || VALIDATION_FAILED=true

if [[ "${VALIDATION_FAILED:-}" == "true" ]]; then
  # Output warning for the agent
  cat << 'EOF'

⚠️  INDEX.md VALIDATION WARNING
═══════════════════════════════════════════════════════════════════

The INDEX.md file you just edited has validation issues.
Please review and fix before continuing.

EOF
  echo "$VALIDATION_OUTPUT"
  cat << 'EOF'

═══════════════════════════════════════════════════════════════════

Expected INDEX.md format:

| ID | Title | Status | Dependencies | Worktree |
|----|-------|--------|--------------|----------|
| PREFIX-001 | Task title | Ready | - | - |

Valid statuses: Ready, In Progress, In Review, Complete, Blocked, Changes Requested
Task IDs must match pattern: PREFIX-NNN (e.g., MKT-001, CRANE-042)

EOF
fi

exit 0
