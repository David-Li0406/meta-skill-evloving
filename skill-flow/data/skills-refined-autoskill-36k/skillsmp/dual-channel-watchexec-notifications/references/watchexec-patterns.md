**Skill**: [Dual-Channel Watchexec Notifications](../SKILL.md)

## watchexec Integration

### File Change Detection (macOS Compatible)

**DO** (works on macOS):

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Use stat to check modification time
NOW=$(date +%s)
FILE_MTIME=$(stat -f %m "$file" 2>/dev/null || echo "0")
AGE=$((NOW - FILE_MTIME))

if [[ $AGE -lt 60 ]]; then
    echo "File modified ${AGE}s ago"
fi
PREFLIGHT_EOF
```

**DON'T** (broken on macOS):

```bash
# find -newermt has different syntax on BSD/macOS
find . -newermt "60 seconds ago"  # ❌ Fails on macOS
```

### Restart Reason Detection

```bash
/usr/bin/env bash << 'WATCHEXEC_PATTERNS_SCRIPT_EOF'
# Determine why process restarted
if [[ ! -f "$FIRST_RUN_MARKER" ]]; then
    REASON="startup"
    touch "$FIRST_RUN_MARKER"
elif [[ $EXIT_CODE -ne 0 ]]; then
    REASON="crash"
else
    REASON="code_change"
fi
WATCHEXEC_PATTERNS_SCRIPT_EOF
```

## Message Archiving (Debugging)

Always save messages before sending for post-mortem debugging:

```bash
/usr/bin/env bash << 'WATCHEXEC_PATTERNS_SCRIPT_EOF_2'
MESSAGE_ARCHIVE_DIR="/path/to/logs/notification-archive"
mkdir -p "$MESSAGE_ARCHIVE_DIR"
MESSAGE_FILE="$MESSAGE_ARCHIVE_DIR/$(date '+%Y%m%d-%H%M%S')-$REASON-$PID.txt"

cat > "$MESSAGE_FILE" <<ARCHIVE_EOF
========================================================================
Timestamp: $TIMESTAMP
Reason: $REASON
Exit Code: $EXIT_CODE

--- TELEGRAM MESSAGE ---
$MESSAGE

--- CONTEXT ---
$(cat "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "Not available")
========================================================================
ARCHIVE_EOF
WATCHEXEC_PATTERNS_SCRIPT_EOF_2
```
