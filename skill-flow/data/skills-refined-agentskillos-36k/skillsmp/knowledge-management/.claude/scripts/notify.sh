#!/bin/bash
# Claude Code Notification Script
# Sends macOS notifications when Claude needs attention

set -e

# Sanitize string for AppleScript (escape backslashes and double quotes)
sanitize_for_applescript() {
    local input="$1"
    # Remove any characters that could break AppleScript
    # Allow only alphanumeric, spaces, and basic punctuation
    echo "$input" | tr -cd '[:alnum:][:space:]._-:()' | cut -c1-100
}

# Validate notification type (whitelist approach)
validate_notification_type() {
    local type="$1"
    case "$type" in
        idle_prompt|permission_prompt|auth_success|elicitation_dialog)
            echo "$type"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Read JSON input from stdin
INPUT=$(cat)

# Parse and validate notification type from hook input
RAW_TYPE=$(echo "$INPUT" | jq -r '.notification_type // "unknown"')
NOTIFICATION_TYPE=$(validate_notification_type "$RAW_TYPE")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' | cut -c1-8 | tr -cd '[:alnum:]')

# Get current working directory name for context
CWD=$(echo "$INPUT" | jq -r '.cwd // ""')
RAW_PROJECT_NAME=$(basename "$CWD" 2>/dev/null || echo "Claude Code")
PROJECT_NAME=$(sanitize_for_applescript "$RAW_PROJECT_NAME")

# Notification messages based on type
case "$NOTIFICATION_TYPE" in
    "idle_prompt")
        TITLE="Claude Code - $PROJECT_NAME"
        MESSAGE="Waiting for your input (session: $SESSION_ID)"
        SOUND="Ping"
        ;;
    "permission_prompt")
        TITLE="Claude Code - Permission Required"
        MESSAGE="$PROJECT_NAME needs your approval"
        SOUND="Basso"
        ;;
    "auth_success")
        TITLE="Claude Code"
        MESSAGE="Authentication successful"
        SOUND="Glass"
        ;;
    "elicitation_dialog")
        TITLE="Claude Code - Input Needed"
        MESSAGE="MCP tool requires additional information"
        SOUND="Purr"
        ;;
    *)
        TITLE="Claude Code - $PROJECT_NAME"
        MESSAGE="Needs your attention"
        SOUND="Ping"
        ;;
esac

# Sanitize message and title before sending to osascript
SAFE_TITLE=$(sanitize_for_applescript "$TITLE")
SAFE_MESSAGE=$(sanitize_for_applescript "$MESSAGE")

# Send macOS notification
osascript -e "display notification \"$SAFE_MESSAGE\" with title \"$SAFE_TITLE\" sound name \"$SOUND\""

# Optional: Also send to terminal-notifier if available (for better action support)
if command -v terminal-notifier &> /dev/null; then
    terminal-notifier -title "$SAFE_TITLE" -message "$SAFE_MESSAGE" -sound "$SOUND" -group "claude-code-$SESSION_ID"
fi

exit 0
