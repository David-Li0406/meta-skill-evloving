#!/usr/bin/env bash
# watchexec Wrapper Script with Restart Detection
# Wraps a process to detect restart reasons and send notifications
#
# Usage: watchexec --restart -- ./bot-wrapper.sh
#
# This is a self-contained example. Adapt for your project.

set -euo pipefail

# ============================================================================
# CONFIGURATION - Adapt these for your project
# ============================================================================

# Path to your main script/process
MAIN_SCRIPT="${MAIN_SCRIPT:-./bot.py}"

# Path to notification script
NOTIFY_SCRIPT="${NOTIFY_SCRIPT:-./notify-restart.sh}"

# Log files
BOT_LOG="${BOT_LOG:-./logs/bot.log}"
CRASH_LOG="${CRASH_LOG:-./logs/crash.log}"

# Runtime state
FIRST_RUN_MARKER="/tmp/watchexec_first_run_$$"
WATCHEXEC_INFO_FILE="/tmp/watchexec_info_$$.json"

# Directories to watch for file changes
WATCH_DIRS=(
    ./src
    ./lib
)

mkdir -p "$(dirname "$BOT_LOG")"
mkdir -p "$(dirname "$CRASH_LOG")"

# ============================================================================
# FILE CHANGE DETECTION (macOS Compatible)
# ============================================================================

# Get current time in seconds since epoch
NOW=$(date +%s)

# Find most recently modified file in watched directories
MOST_RECENT_FILE=""
MOST_RECENT_TIME=0

for dir in "${WATCH_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        while IFS= read -r file; do
            if [[ -f "$file" ]]; then
                # Get file modification time (macOS: -f %m, Linux: -c %Y)
                FILE_MTIME=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null || echo "0")
                AGE=$((NOW - FILE_MTIME))

                # If file was modified in last 60 seconds and is newer than current best
                if [[ $AGE -lt 60 ]] && [[ $FILE_MTIME -gt $MOST_RECENT_TIME ]]; then
                    MOST_RECENT_FILE="$file"
                    MOST_RECENT_TIME=$FILE_MTIME
                    echo "📝 Found recently modified file: $(basename "$file") (${AGE}s ago)"
                fi
            fi
        done < <(find "$dir" -name "*.py" -o -name "*.sh" -type f 2>/dev/null)
    fi
done

if [[ -n "$MOST_RECENT_FILE" ]]; then
    CHANGED_FILE=$(basename "$MOST_RECENT_FILE")
    RECENT_CHANGE_FULL="$MOST_RECENT_FILE"
    AGE=$((NOW - MOST_RECENT_TIME))
    echo "✅ Detected file change: $CHANGED_FILE (${AGE}s ago, path: $RECENT_CHANGE_FULL)"

    # Create watchexec info JSON - atomic write using mktemp + mv
    # ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
    tmp=$(mktemp)
    cat > "$tmp" <<WATCHEXEC_EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "watchexec": {
    "common_path": "$RECENT_CHANGE_FULL",
    "created_path": "",
    "removed_path": "",
    "renamed_path": "",
    "written_path": "$RECENT_CHANGE_FULL",
    "meta_changed_path": "",
    "otherwise_changed_path": ""
  },
  "environment": {
    "user": "$(whoami)",
    "shell": "$SHELL",
    "pwd": "$(pwd)"
  }
}
WATCHEXEC_EOF
    mv "$tmp" "$WATCHEXEC_INFO_FILE"
else
    echo "⚠️  No recently modified files detected (checked last 60s)"
    # Create empty watchexec info - atomic write
    tmp=$(mktemp)
    echo "{}" > "$tmp"
    mv "$tmp" "$WATCHEXEC_INFO_FILE"
fi

# ============================================================================
# DETERMINE RESTART REASON
# ============================================================================

# Atomic first-run check using mkdir (mkdir is atomic, fails if exists)
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
if mkdir "$FIRST_RUN_MARKER" 2>/dev/null; then
    REASON="startup"
    echo "🚀 First run - sending startup notification"
    "$NOTIFY_SCRIPT" "$REASON" 0 "$WATCHEXEC_INFO_FILE" "" &
else
    # After first run, assume code_change (watchexec restart)
    # Will be updated to "crash" if exit code != 0
    REASON="code_change"
    echo "🔄 Code change detected - restarting process"
    "$NOTIFY_SCRIPT" "$REASON" 0 "$WATCHEXEC_INFO_FILE" "" &
fi

# ============================================================================
# RUN THE MAIN PROCESS
# ============================================================================

echo "▶️  Starting process: $MAIN_SCRIPT"

# Clear previous crash log - safe truncation with existence check
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
: > "$CRASH_LOG"  # ':' is a no-op, ensures file exists and is truncated

# Run the main script and capture exit code and stderr
EXIT_CODE=0
if [[ "$MAIN_SCRIPT" == *.py ]]; then
    # Python script
    python3 "$MAIN_SCRIPT" 2> >(tee -a "$CRASH_LOG" >&2) || EXIT_CODE=$?
elif [[ "$MAIN_SCRIPT" == *.sh ]]; then
    # Shell script
    bash "$MAIN_SCRIPT" 2> >(tee -a "$CRASH_LOG" >&2) || EXIT_CODE=$?
else
    # Generic executable
    "$MAIN_SCRIPT" 2> >(tee -a "$CRASH_LOG" >&2) || EXIT_CODE=$?
fi

# ============================================================================
# HANDLE CRASH (if exit code != 0)
# ============================================================================

if [[ $EXIT_CODE -ne 0 ]]; then
    echo "💥 Process crashed with exit code: $EXIT_CODE"

    # Capture crash context - atomic write using mktemp + mv
    # ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
    CRASH_CONTEXT="/tmp/crash_context_$$.txt"
    tmp=$(mktemp)
    {
        # Last 20 lines of bot log
        if [[ -f "$BOT_LOG" ]]; then
            echo "--- BOT LOG (last 20 lines) ---"
            tail -20 "$BOT_LOG" 2>/dev/null || true
        fi
        # Stderr from crash
        if [[ -f "$CRASH_LOG" && -s "$CRASH_LOG" ]]; then
            echo "--- STDERR ---"
            tail -10 "$CRASH_LOG" 2>/dev/null || true
        fi
    } > "$tmp"
    mv "$tmp" "$CRASH_CONTEXT"

    # Send crash notification (background, non-blocking)
    "$NOTIFY_SCRIPT" "crash" "$EXIT_CODE" "$WATCHEXEC_INFO_FILE" "$CRASH_CONTEXT" &

    # Wait for background notification to complete before exit
    # ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
    wait

    # Exit with same code (watchexec will restart)
    exit $EXIT_CODE
fi

echo "✅ Process exited cleanly (exit code: 0)"

# Wait for any background notifications to complete
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
wait
