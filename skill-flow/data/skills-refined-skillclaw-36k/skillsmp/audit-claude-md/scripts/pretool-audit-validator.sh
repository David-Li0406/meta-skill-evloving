#!/usr/bin/env bash
# pretool-audit-validator.sh - Validate audit-claude-md config before skill loads
#
# PreToolUse hook that validates audit-claude-md YAML config BEFORE the skill is loaded.
# This hook is registered in hooks.json and runs for ALL Skill tool invocations,
# but filters to only process the audit-claude-md skill.
#
# - Blocks with permissionDecision: "deny" if config is invalid
# - Passes through silently if config is missing (uses defaults)
# - Blocks if config has type errors (treats warnings as errors for PreToolUse)
#
# No external dependencies (pure bash, no jq required)

set -euo pipefail

#------------------------------------------------------------------------------
# Pure bash JSON helpers
#------------------------------------------------------------------------------

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

json_has() {
    local json="$1"
    local key="$2"
    if echo "$json" | grep -qE "\"$key\"[[:space:]]*:[[:space:]]*null"; then
        return 1
    fi
    echo "$json" | grep -qE "\"$key\"[[:space:]]*:"
}

json_count_warnings() {
    local json="$1"
    local count
    count=$(echo "$json" | grep -cE '\{"field"') || count=0
    echo "$count"
}

json_get_warning_messages() {
    local json="$1"
    echo "$json" | grep -oE '\{"field":"[^"]*","message":"[^"]*"\}' | while read -r warning; do
        local field msg
        field=$(json_get "$warning" "field")
        msg=$(json_get "$warning" "message")
        echo "- $field: $msg"
    done
}

json_output_deny() {
    local message="$1"

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

# Extract skill name from tool_input
SKILL_NAME=$(echo "$INPUT" | grep -oE '"skill"[[:space:]]*:[[:space:]]*"[^"]*"' | \
             sed 's/.*"skill"[[:space:]]*:[[:space:]]*"//; s/"$//' || echo "")

# Only process audit-claude-md skill (short form or fully qualified)
if [[ "$SKILL_NAME" != "audit-claude-md" && "$SKILL_NAME" != "claude-skills:audit-claude-md" ]]; then
    exit 0
fi

# Get paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

VALIDATOR="$PLUGIN_ROOT/skills/audit-claude-md/scripts/validate-config.sh"
CONFIG_FILE="$PROJECT_DIR/.claude/audit-claude-md.yaml"

# If validator doesn't exist, allow
if [[ ! -x "$VALIDATOR" ]]; then
    exit 0
fi

# Run validator
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
        DENY_MSG="Audit config validation failed at line $ERROR_LINE: $ERROR_MSG

Please fix .claude/audit-claude-md.yaml before using /audit-claude-md."
    else
        DENY_MSG="Audit config validation failed: $ERROR_MSG

Please fix .claude/audit-claude-md.yaml before using /audit-claude-md."
    fi

    json_output_deny "$DENY_MSG"
    exit 0
fi

# Check for warnings
WARN_COUNT=$(json_count_warnings "$RESULT")
if [[ "$WARN_COUNT" -gt 0 ]]; then
    WARNINGS=$(json_get_warning_messages "$RESULT")

    DENY_MSG="Audit config has validation issues:
$WARNINGS

Please fix .claude/audit-claude-md.yaml before using /audit-claude-md."

    json_output_deny "$DENY_MSG"
    exit 0
fi

# Config is valid - allow
exit 0
