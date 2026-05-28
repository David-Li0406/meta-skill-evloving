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

# Get terminal identifier for distinguishing between tabs
TTY_NAME=$(tty 2>/dev/null | sed 's|/dev/||' || echo "")
# Try to get relative path for more context
SHORT_PATH=$(echo "$CWD" | sed "s|^$HOME|~|" 2>/dev/null || echo "$CWD")
SHORT_PATH=$(sanitize_for_applescript "$SHORT_PATH")

# Build terminal identifier (configurable via CLAUDE_NOTIFY_FORMAT)
# Formats: tty (default), path, both
NOTIFY_FORMAT="${CLAUDE_NOTIFY_FORMAT:-tty}"
case "$NOTIFY_FORMAT" in
    path)
        TERMINAL_ID="$SHORT_PATH"
        ;;
    both)
        TERMINAL_ID="$SHORT_PATH ($TTY_NAME)"
        ;;
    *)
        TERMINAL_ID="${TTY_NAME:-$SESSION_ID}"
        ;;
esac

# Notification messages based on type
case "$NOTIFICATION_TYPE" in
    "idle_prompt")
        TITLE="Claude Code - $PROJECT_NAME"
        MESSAGE="Waiting for your input ($TERMINAL_ID)"
        SOUND="Ping"
        ;;
    "permission_prompt")
        TITLE="Claude Code - Permission Required"
        MESSAGE="$PROJECT_NAME needs your approval ($TERMINAL_ID)"
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
    # Detect terminal app for click-to-focus
    TERM_APP="${TERM_PROGRAM:-}"
    ACTIVATE_ARG=""
    case "$TERM_APP" in
        iTerm.app)  ACTIVATE_ARG="-activate com.googlecode.iterm2" ;;
        Apple_Terminal) ACTIVATE_ARG="-activate com.apple.Terminal" ;;
        WezTerm)    ACTIVATE_ARG="-activate com.github.wez.wezterm" ;;
    esac

    terminal-notifier -title "$SAFE_TITLE" -message "$SAFE_MESSAGE" -sound "$SOUND" \
        -group "claude-code-$SESSION_ID" $ACTIVATE_ARG
fi

exit 0
