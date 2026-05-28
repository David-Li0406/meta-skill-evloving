#!/usr/bin/env bash
# pretool-commit-validator.sh - Validate commit config before skill loads
#
# PreToolUse hook that validates commit YAML config BEFORE the commit skill is loaded.
# This hook is registered in hooks.json and runs for ALL Skill tool invocations,
# but filters to only process the commit skill.
#
# - Blocks with permissionDecision: "deny" if config is invalid
# - Passes through silently if config is missing (uses defaults)
# - Blocks if config has type errors (treats warnings as errors for PreToolUse)
#
# No external dependencies (pure bash, no jq required)

set -euo pipefail

#------------------------------------------------------------------------------
# Pure bash JSON helpers (for single-line, predictable JSON structures)
#------------------------------------------------------------------------------

# Extract a top-level string/number/boolean value from JSON
json_get() {
    local json="$1"
    local key="$2"
    local match
    match=$(echo "$json" | grep -oE "\"$key\"[[:space:]]*:[[:space:]]*(\"[^\"]*\"|[0-9]+|true|false|null)" | head -1)
    if [[ -z "$match" ]]; then
        return
    fi
    local value="${match#*:}"
    value="${value#"${value%%[![:space:]]*}"}"
    if [[ "$value" == \"*\" ]]; then
        value="${value:1:${#value}-2}"
    fi
    echo "$value"
}

# Extract a nested field value (one level deep)
json_get_nested() {
    local json="$1"
    local parent="$2"
    local key="$3"
    local parent_content
    parent_content=$(echo "$json" | grep -oE "\"$parent\"[[:space:]]*:[[:space:]]*\{[^}]*\}" | head -1)
    if [[ -n "$parent_content" ]]; then
        json_get "$parent_content" "$key"
    fi
}

# Check if a JSON object has a non-null field
json_has() {
    local json="$1"
    local key="$2"
    if echo "$json" | grep -qE "\"$key\"[[:space:]]*:[[:space:]]*null"; then
        return 1
    fi
    echo "$json" | grep -qE "\"$key\"[[:space:]]*:"
}

# Count warnings array length
json_count_warnings() {
    local json="$1"
    local count
    count=$(echo "$json" | grep -cE '\{"field"') || count=0
    echo "$count"
}

# Get all warning messages as a list
json_get_warning_messages() {
    local json="$1"
    echo "$json" | grep -oE '\{"field":"[^"]*","message":"[^"]*"\}' | while read -r warning; do
        local field msg
        field=$(json_get "$warning" "field")
        msg=$(json_get "$warning" "message")
        echo "- $field: $msg"
    done
}

# Build JSON output with permissionDecision deny
json_output_deny() {
    local message="$1"

    # Escape special JSON characters
    message="${message//\\/\\\\}"
    message="${message//\"/\\\"}"
    message="${message//$'\n'/\\n}"
    message="${message//$'\t'/\\t}"
    message="${message//$'\r'/\\r}"

    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"$message\"}}"
}

#------------------------------------------------------------------------------
# Main hook logic
#------------------------------------------------------------------------------

INPUT=$(cat)

# Extract skill name from tool_input - this hook runs for ALL Skill tool invocations
SKILL_NAME=$(echo "$INPUT" | grep -oE '"skill"[[:space:]]*:[[:space:]]*"[^"]*"' | \
             sed 's/.*"skill"[[:space:]]*:[[:space:]]*"//; s/"$//' || echo "")

# Only process commit skill (short form or fully qualified)
if [[ "$SKILL_NAME" != "commit" && "$SKILL_NAME" != "claude-skills:commit" ]]; then
    exit 0
fi

# Get paths - script is now in skills/commit/scripts/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

VALIDATOR="$PLUGIN_ROOT/skills/commit/scripts/validate-config.sh"
CONFIG_FILE="$PROJECT_DIR/.claude/commit.yaml"

# If validator doesn't exist, allow (can't validate)
if [[ ! -x "$VALIDATOR" ]]; then
    exit 0
fi

# Run validator (use || true to prevent set -e from exiting)
RESULT=$("$VALIDATOR" "$CONFIG_FILE" 2>/dev/null || true)

# If validator returned empty result, allow
if [[ -z "$RESULT" ]]; then
    exit 0
fi

# Check if valid
IS_VALID=$(json_get "$RESULT" "valid")

# Block if invalid
if [[ "$IS_VALID" == "false" ]]; then
    ERROR_MSG=$(json_get_nested "$RESULT" "error" "message")
    ERROR_LINE=$(json_get_nested "$RESULT" "error" "line")

    if [[ -n "$ERROR_LINE" && "$ERROR_LINE" != "null" ]]; then
        DENY_MSG="Commit config validation failed at line $ERROR_LINE: $ERROR_MSG

Please fix .claude/commit.yaml before using /commit."
    else
        DENY_MSG="Commit config validation failed: $ERROR_MSG

Please fix .claude/commit.yaml before using /commit."
    fi

    json_output_deny "$DENY_MSG"
    exit 0
fi

# Check for warnings (type errors are reported as warnings but should block in PreToolUse)
WARN_COUNT=$(json_count_warnings "$RESULT")
if [[ "$WARN_COUNT" -gt 0 ]]; then
    # Get warning messages
    WARNINGS=$(json_get_warning_messages "$RESULT")

    DENY_MSG="Commit config has validation issues:
$WARNINGS

Please fix .claude/commit.yaml before using /commit."

    json_output_deny "$DENY_MSG"
    exit 0
fi

# Config is valid with no warnings - allow the skill to proceed
exit 0
