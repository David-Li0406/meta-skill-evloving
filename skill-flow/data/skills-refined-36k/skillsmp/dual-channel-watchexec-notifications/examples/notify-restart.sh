#!/usr/bin/env bash
# Dual-Channel Notification Script (Telegram + Pushover)
# Usage: notify-restart.sh <reason> [exit_code] [watchexec_info_file] [crash_context_file]
#
# This is a self-contained example demonstrating the pattern.
# Adapt paths and credentials loading for your project.

set -euo pipefail

# ============================================================================
# IDEMPOTENCY HELPERS
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
# ============================================================================

# Log rotation - keep last N logs to prevent unbounded growth
LOG_ROTATION_KEEP_COUNT=5
rotate_log() {
    local log_file="$1"
    local keep_count="${2:-$LOG_ROTATION_KEEP_COUNT}"

    if [ -f "$log_file" ]; then
        mv "$log_file" "${log_file}.$(date +%s)"
        # Keep only last N logs
        ls -t "${log_file}."* 2>/dev/null | tail -n +$((keep_count + 1)) | xargs rm -f 2>/dev/null || true
    fi
}

# Trap for cleanup - will be set after MESSAGE_FILE is created
MESSAGE_FILE=""
cleanup() {
    [[ -n "$MESSAGE_FILE" ]] && rm -f "$MESSAGE_FILE"
}
trap cleanup EXIT

# ============================================================================
# CONFIGURATION - Adapt these for your project
# ============================================================================

# Log output location
NOTIFICATION_LOG="${NOTIFICATION_LOG:-./logs/bot-notifications.log}"
mkdir -p "$(dirname "$NOTIFICATION_LOG")"
rotate_log "$NOTIFICATION_LOG" "$LOG_ROTATION_KEEP_COUNT"
exec >> "$NOTIFICATION_LOG" 2>&1

# Message archive directory
MESSAGE_ARCHIVE_DIR="${MESSAGE_ARCHIVE_DIR:-./logs/notification-archive}"
mkdir -p "$MESSAGE_ARCHIVE_DIR"

# ============================================================================
# ARGUMENTS
# ============================================================================

REASON="${1:-unknown}"
EXIT_CODE="${2:-0}"
WATCHEXEC_INFO_FILE="${3:-}"
CRASH_CONTEXT_FILE="${4:-}"

# ============================================================================
# METADATA
# ============================================================================

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
HOSTNAME_SHORT="$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo 'unknown')"
PID="$$"

echo "========================================================================"
echo "🔔 Notification - $TIMESTAMP"
echo "========================================================================"

# ============================================================================
# PARSE WATCHEXEC INFO (if available)
# ============================================================================

WATCHEXEC_DETAILS=""
CHANGED_FILES=""

if [[ -f "$WATCHEXEC_INFO_FILE" ]]; then
    echo "📊 Watchexec diagnostic info available"

    # Extract file change information using jq
    if command -v jq >/dev/null 2>&1; then
        COMMON_PATH=$(jq -r '.watchexec.common_path // ""' "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "")
        WRITTEN_PATH=$(jq -r '.watchexec.written_path // ""' "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "")
        CREATED_PATH=$(jq -r '.watchexec.created_path // ""' "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "")
        REMOVED_PATH=$(jq -r '.watchexec.removed_path // ""' "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "")

        # Build file change summary (HTML format - escape <, >, &)
        if [[ -n "$WRITTEN_PATH" ]]; then
            FILENAME=$(basename "$WRITTEN_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
            CHANGED_FILES="Modified: <code>$FILENAME</code>"
            TRIGGER_PATH="$WRITTEN_PATH"
        elif [[ -n "$CREATED_PATH" ]]; then
            FILENAME=$(basename "$CREATED_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
            CHANGED_FILES="Created: <code>$FILENAME</code>"
            TRIGGER_PATH="$CREATED_PATH"
        elif [[ -n "$REMOVED_PATH" ]]; then
            FILENAME=$(basename "$REMOVED_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
            CHANGED_FILES="Deleted: <code>$FILENAME</code>"
            TRIGGER_PATH="$REMOVED_PATH"
        elif [[ -n "$COMMON_PATH" ]]; then
            FILENAME=$(basename "$COMMON_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
            CHANGED_FILES="Changed: <code>$FILENAME</code>"
            TRIGGER_PATH="$COMMON_PATH"
        else
            CHANGED_FILES="Watchexec detected change (file not identified)"
            TRIGGER_PATH="(file detection failed)"
        fi

        # HTML escape the full path
        TRIGGER_PATH_ESCAPED=$(echo "$TRIGGER_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

        WATCHEXEC_DETAILS="
<b>Trigger</b>: <code>$TRIGGER_PATH_ESCAPED</code>
<b>Action</b>: $CHANGED_FILES"
    else
        WATCHEXEC_DETAILS="
<i>Watchexec info available (jq not installed)</i>"
    fi
fi

# ============================================================================
# EXTRACT CRASH CONTEXT (if available)
# ============================================================================

CRASH_INFO=""
if [[ -f "$CRASH_CONTEXT_FILE" ]]; then
    echo "💥 Crash context available"

    # Read last error lines and HTML escape them
    CRASH_PREVIEW=$(tail -5 "$CRASH_CONTEXT_FILE" 2>/dev/null | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' || echo "(no context)")

    CRASH_INFO="

<b>Last Log Lines</b>:
<pre>$CRASH_PREVIEW</pre>"
fi

# ============================================================================
# DETERMINE RESTART TYPE AND EMOJI
# ============================================================================

if [[ "$REASON" == "startup" ]]; then
    EMOJI="🚀"
    STATUS="Started"
    PRIORITY="normal"
    PUSHOVER_SOUND="cosmic"
    PUSHOVER_PRIORITY=0
elif [[ "$REASON" == "code_change" ]]; then
    EMOJI="🔄"
    STATUS="Restarted (code change)"
    PRIORITY="normal"
    PUSHOVER_SOUND="bike"
    PUSHOVER_PRIORITY=0
elif [[ "$REASON" == "crash" ]]; then
    EMOJI="💥"
    STATUS="Restarted (crash)"
    PRIORITY="high"
    PUSHOVER_SOUND="siren"
    PUSHOVER_PRIORITY=1  # High priority, bypasses quiet hours
else
    EMOJI="⚠️"
    STATUS="Restarted ($REASON)"
    PRIORITY="normal"
    PUSHOVER_SOUND="cosmic"
    PUSHOVER_PRIORITY=0
fi

# ============================================================================
# BUILD TELEGRAM MESSAGE (HTML FORMAT)
# ============================================================================

# Use HTML parse mode - only need to escape 3 chars: & < >
MESSAGE="$EMOJI <b>Service $STATUS</b>

<b>Host</b>: <code>$HOSTNAME_SHORT</code>
<b>Time</b>: $TIMESTAMP
<b>PID</b>: $PID
<b>Exit Code</b>: $EXIT_CODE$WATCHEXEC_DETAILS$CRASH_INFO

<i>Monitoring: watchexec</i>"

# ============================================================================
# ARCHIVE MESSAGE (for debugging)
# ============================================================================

# Nanosecond precision to prevent filename collisions
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
MESSAGE_ARCHIVE_FILE="$MESSAGE_ARCHIVE_DIR/$(date '+%Y%m%d-%H%M%S-%N')-$REASON-$PID.txt"

cat > "$MESSAGE_ARCHIVE_FILE" <<ARCHIVE_EOF
========================================================================
Notification Archive
========================================================================
Timestamp: $TIMESTAMP
Reason: $REASON
Exit Code: $EXIT_CODE
Host: $HOSTNAME_SHORT
PID: $PID

--- TELEGRAM MESSAGE ---
$MESSAGE

--- VARIABLES ---
WATCHEXEC_DETAILS: ${WATCHEXEC_DETAILS:-<empty>}
CRASH_INFO: ${CRASH_INFO:-<empty>}
CHANGED_FILES: ${CHANGED_FILES:-<empty>}

--- WATCHEXEC INFO FILE ---
$(cat "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "Not available")

--- CRASH CONTEXT FILE ---
$(cat "$CRASH_CONTEXT_FILE" 2>/dev/null || echo "Not available")
========================================================================
ARCHIVE_EOF

echo "📝 Message archived: $MESSAGE_ARCHIVE_FILE"

# ============================================================================
# SEND TO TELEGRAM (HTML MODE)
# ============================================================================

if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]] && [[ -n "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "📱 Sending Telegram notification..."

    # Create temp file using mktemp to avoid race conditions
    # ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
    MESSAGE_FILE=$(mktemp /tmp/telegram_message.XXXXXX)
    cat > "$MESSAGE_FILE" <<MSGEOF
$MESSAGE
MSGEOF

    # Use Python for reliable Telegram API call with HTML parse mode
    python3 - "$MESSAGE_FILE" <<'EOF'
import os
import urllib.request
import urllib.parse
import json
import sys

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

# Read message from file to avoid shell escaping issues
with open(sys.argv[1], 'r') as f:
    message = f.read()

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    'chat_id': chat_id,
    'text': message,
    'parse_mode': 'HTML'  # Use HTML mode (NOT Markdown)
}

try:
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result.get('ok'):
            print('   ✅ Telegram notification sent')
        else:
            print(f'   ❌ Telegram API error: {result}')
            print(f'   Message preview: {message[:200]}...')
except Exception as e:
    print(f'   ❌ Failed to send Telegram notification: {e}')
    print(f'   Message preview: {message[:200]}...')
EOF

    rm -f "$MESSAGE_FILE"
else
    echo "   ⏭️  Skipping Telegram (TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set)"
fi

# ============================================================================
# SEND TO PUSHOVER
# ============================================================================

if [[ -n "${PUSHOVER_APP_TOKEN:-}" ]] && [[ -n "${PUSHOVER_USER_KEY:-}" ]]; then
    echo "📲 Sending Pushover notification..."

    PUSHOVER_TITLE="Service $STATUS"

    # Build Pushover message (plain text, no HTML)
    PUSHOVER_MESSAGE="Host: $HOSTNAME_SHORT
Time: $TIMESTAMP
PID: $PID
Exit: $EXIT_CODE"

    # Add file change info if available (strip HTML tags for Pushover)
    if [[ -n "$CHANGED_FILES" ]]; then
        CHANGED_FILES_PLAIN=$(echo "$CHANGED_FILES" | sed 's/<[^>]*>//g')
        PUSHOVER_MESSAGE="$PUSHOVER_MESSAGE

File: $CHANGED_FILES_PLAIN"
    fi

    # Add crash preview if available (first 2 lines only)
    if [[ -f "$CRASH_CONTEXT_FILE" ]]; then
        CRASH_SHORT=$(tail -2 "$CRASH_CONTEXT_FILE" 2>/dev/null | tr '\n' ' ' || echo "")
        if [[ -n "$CRASH_SHORT" ]]; then
            PUSHOVER_MESSAGE="$PUSHOVER_MESSAGE

Error: ${CRASH_SHORT:0:200}"
        fi
    fi

    # Send with curl
    DEVICE_NAME="${PUSHOVER_DEVICE:-default}"

    curl -s \
        --form-string "token=$PUSHOVER_APP_TOKEN" \
        --form-string "user=$PUSHOVER_USER_KEY" \
        --form-string "device=$DEVICE_NAME" \
        --form-string "title=$PUSHOVER_TITLE" \
        --form-string "message=$PUSHOVER_MESSAGE" \
        --form-string "sound=$PUSHOVER_SOUND" \
        --form-string "priority=$PUSHOVER_PRIORITY" \
        https://api.pushover.net/1/messages.json >/dev/null 2>&1

    if [[ $? -eq 0 ]]; then
        echo "   ✅ Pushover notification sent (priority: $PUSHOVER_PRIORITY, sound: $PUSHOVER_SOUND)"
    else
        echo "   ❌ Pushover notification failed"
    fi
else
    echo "   ⏭️  Skipping Pushover (PUSHOVER_APP_TOKEN or PUSHOVER_USER_KEY not set)"
fi

echo "✅ Notification completed"
