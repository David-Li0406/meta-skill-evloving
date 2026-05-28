# Implementation Reference

Detailed implementation notes for dual-channel watchexec notifications.

## Directory Structure

```
your-project/
├── notify-restart.sh      # Dual-channel notification script
├── bot-wrapper.sh         # watchexec wrapper with restart detection
├── your-app.py            # Your main application
└── logs/
    ├── bot-notifications.log              # Notification execution log
    └── notification-archive/              # Pre-send message archives
        └── YYYYMMDD-HHMMSS-reason-PID.txt
```

## Complete Example Scripts

All examples are available in this skill's `examples/` directory:

- `examples/notify-restart.sh` - Dual-channel notification script
- `examples/bot-wrapper.sh` - watchexec wrapper
- `examples/setup-example.sh` - Complete setup guide

## notify-restart.sh Deep Dive

### Script Architecture

```
Arguments → Parse watchexec info → Build HTML message → Archive → Send (Telegram + Pushover)
```

### Key Implementation Details

#### 1. HTML Escaping Function

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF'
# Escape only 3 characters for HTML: & < >
ESCAPED=$(echo "$text" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
REFERENCE_SCRIPT_EOF
```

**Why this works**:

- HTML only treats `&`, `<`, `>` as special
- Markdown requires escaping 40+ chars (`.`, `-`, `_`, `*`, etc.)
- Simpler = more reliable

#### 2. Heredoc Variable Expansion

**WRONG** (literal `$MESSAGE` sent):

```bash
cat > "$FILE" <<'MSGEOF'
$MESSAGE
MSGEOF
```

**CORRECT** (variable expanded):

```bash
cat > "$FILE" <<MSGEOF
$MESSAGE
MSGEOF
```

**Rule**: Unquoted heredoc delimiter (`<<MSGEOF`) allows variable expansion, quoted (`<<'MSGEOF'`) treats as literal.

#### 3. Python Telegram API Call

```python
# Read message from temp file (avoids shell escaping hell)
with open(sys.argv[1], 'r') as f:
    message = f.read()

data = {
    'chat_id': chat_id,
    'text': message,
    'parse_mode': 'HTML'  # Key: HTML mode
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
```

**Why Python + temp file**:

- Avoids bash quote escaping complexity
- Handles Unicode properly
- Reliable JSON encoding

#### 4. Priority and Sound Mapping

```bash
case "$REASON" in
    startup)
        EMOJI="🚀"
        PUSHOVER_SOUND="cosmic"
        PUSHOVER_PRIORITY=0  # Normal
        ;;
    code_change)
        EMOJI="🔄"
        PUSHOVER_SOUND="bike"
        PUSHOVER_PRIORITY=0  # Normal
        ;;
    crash)
        EMOJI="💥"
        PUSHOVER_SOUND="siren"
        PUSHOVER_PRIORITY=1  # High (bypasses quiet hours)
        ;;
esac
```

**Pushover Priority Levels**:

- `0`: Normal (respects quiet hours, default sound)
- `1`: High (bypasses quiet hours, requires acknowledgment)
- `2`: Emergency (repeats until acknowledged)

#### 5. Message Archiving

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_2'
MESSAGE_ARCHIVE_FILE="$MESSAGE_ARCHIVE_DIR/$(date '+%Y%m%d-%H%M%S')-$REASON-$PID.txt"

cat > "$MESSAGE_ARCHIVE_FILE" <<ARCHIVE_EOF
========================================================================
Notification Archive
========================================================================
Timestamp: $TIMESTAMP
Reason: $REASON

--- TELEGRAM MESSAGE ---
$MESSAGE

--- WATCHEXEC INFO FILE ---
$(cat "$WATCHEXEC_INFO_FILE" 2>/dev/null || echo "Not available")

--- CRASH CONTEXT FILE ---
$(cat "$CRASH_CONTEXT_FILE" 2>/dev/null || echo "Not available")
========================================================================
ARCHIVE_EOF
REFERENCE_SCRIPT_EOF_2
```

**Why archive**:

- Post-mortem debugging (what was actually sent?)
- Audit trail
- Reproducing Telegram 400 errors
- ~5ms overhead per notification

## bot-wrapper.sh Deep Dive

### Restart Detection Logic

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_3'
FIRST_RUN_MARKER="/tmp/watchexec_first_run_$$"

if [[ ! -f "$FIRST_RUN_MARKER" ]]; then
    REASON="startup"
    touch "$FIRST_RUN_MARKER"
else
    REASON="code_change"
fi

# Run process
EXIT_CODE=0
python3 "$MAIN_SCRIPT" || EXIT_CODE=$?

# Update reason if crashed
if [[ $EXIT_CODE -ne 0 ]]; then
    REASON="crash"
    # Send crash notification
    "$NOTIFY_SCRIPT" "crash" "$EXIT_CODE" "$INFO_FILE" "$CRASH_CONTEXT" &
fi
REFERENCE_SCRIPT_EOF_3
```

**State transitions**:

1. First run: `startup` → notify, create marker
1. watchexec restart (exit=0): `code_change` → notify
1. Process crash (exit≠0): `crash` → notify with context

### File Change Detection (macOS Compatible)

**Problem**: `find -newermt` syntax differs on BSD (macOS) vs GNU (Linux)

**Solution**: Use `stat` to check modification time directly

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_4'
NOW=$(date +%s)
FILE_MTIME=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null)
AGE=$((NOW - FILE_MTIME))

if [[ $AGE -lt 60 ]]; then
    echo "File modified ${AGE}s ago"
fi
REFERENCE_SCRIPT_EOF_4
```

**Platform compatibility**:

- macOS: `stat -f %m` (BSD stat)
- Linux: `stat -c %Y` (GNU stat)
- Fallback with `||` ensures portability

### Crash Context Capture

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_5'
CRASH_CONTEXT="/tmp/crash_context_$$.txt"

# Last 20 lines of main log
tail -20 "$BOT_LOG" > "$CRASH_CONTEXT"

# Last 10 lines of stderr
if [[ -f "$CRASH_LOG" ]]; then
    echo "--- STDERR ---" >> "$CRASH_CONTEXT"
    tail -10 "$CRASH_LOG" >> "$CRASH_CONTEXT"
fi

# Send in background (non-blocking)
"$NOTIFY_SCRIPT" "crash" "$EXIT_CODE" "$INFO_FILE" "$CRASH_CONTEXT" &
REFERENCE_SCRIPT_EOF_5
```

**Why last N lines**:

- Crash often has error at end of log
- Keeps notification message short
- Full logs available on server for deep debugging

## Credential Management Patterns

### Pattern 1: Environment Variables (Simple)

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_6'
# ~/.bashrc or ~/.zshrc
export TELEGRAM_BOT_TOKEN="1234567890:ABC..."
export TELEGRAM_CHAT_ID="-1001234567890"
export PUSHOVER_APP_TOKEN="azGDORePK8gMa..."
export PUSHOVER_USER_KEY="uQiRzpo4DXghD..."

# In script
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
    echo "Error: TELEGRAM_BOT_TOKEN not set"
    exit 1
fi
REFERENCE_SCRIPT_EOF_6
```

**Pros**: Simple, works everywhere
**Cons**: Visible in `ps`, stored in shell history

### Pattern 2: Doppler (Recommended for Production)

**For Pushover** (notifications/dev):
```bash
/usr/bin/env bash << 'SETUP_EOF'
# Install Doppler CLI
brew install dopplerhq/cli/doppler

# Load Pushover credentials from dedicated project
export PUSHOVER_APP_TOKEN=$(doppler secrets get PUSHOVER_APP_TOKEN \
  --project notifications \
  --config dev \
  --plain)
export PUSHOVER_USER_KEY=$(doppler secrets get PUSHOVER_USER_KEY \
  --project notifications \
  --config dev \
  --plain)

# Run with Doppler
doppler run --project notifications --config dev -- \
  watchexec --restart -- ./bot-wrapper.sh
SETUP_EOF
```

**For Telegram** (generic):
```bash
/usr/bin/env bash << 'DOPPLER_EOF'
# Set secrets
doppler secrets set TELEGRAM_BOT_TOKEN --value "..."
doppler secrets set TELEGRAM_CHAT_ID --value "..."

# Load in script
export TELEGRAM_BOT_TOKEN=$(doppler secrets get TELEGRAM_BOT_TOKEN --plain)
export TELEGRAM_CHAT_ID=$(doppler secrets get TELEGRAM_CHAT_ID --plain)
DOPPLER_EOF
```

**Pros**: Encrypted, team sync, audit trail, rotation
**Cons**: Requires Doppler account

### Pattern 3: macOS Keychain

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_7'
# Store secret
security add-generic-password \
    -s 'telegram-bot-token' \
    -a "$USER" \
    -w 'your_token_here'

# Load in script
TELEGRAM_BOT_TOKEN=$(security find-generic-password \
    -s 'telegram-bot-token' \
    -a "$USER" \
    -w)
REFERENCE_SCRIPT_EOF_7
```

**Pros**: OS-level encryption, native macOS
**Cons**: macOS only, no team sync

### Pattern 4: systemd Environment File (Linux)

```bash
# /etc/systemd/system/myapp.service.d/env.conf
[Service]
EnvironmentFile=/etc/myapp/secrets.env

# /etc/myapp/secrets.env (chmod 600)
TELEGRAM_BOT_TOKEN=1234567890:ABC...
TELEGRAM_CHAT_ID=-1001234567890
```

**Pros**: systemd integration, file permissions
**Cons**: Linux only, manual rotation

## watchexec Configuration

### Basic Usage

```bash
# Watch ./src directory, restart on .py file changes
watchexec --restart --watch ./src --exts py -- ./bot-wrapper.sh
```

### Advanced Options

```bash
# Watch multiple directories
watchexec \
    --restart \
    --watch ./src \
    --watch ./lib \
    --watch ./config \
    --exts py,yaml \
    --ignore '*.pyc' \
    --ignore '__pycache__' \
    -- ./bot-wrapper.sh
```

### Diagnostic Output

```bash
# Export watchexec events to JSON (for debugging)
watchexec \
    --restart \
    --watch ./src \
    --emit-events-to json \
    -- ./bot-wrapper.sh
```

### With Delay (Debouncing)

```bash
# Wait 2s after file change before restarting (debounce rapid edits)
watchexec \
    --restart \
    --watch ./src \
    --debounce 2000 \
    -- ./bot-wrapper.sh
```

## HTML Message Construction

### HTML Tags Supported by Telegram

| Tag           | Purpose      | Example                          |
|---------------|--------------|----------------------------------|
| `<b>`         | Bold         | `<b>Alert</b>`                   |
| `<strong>`    | Bold (alt)   | `<strong>Alert</strong>`         |
| `<i>`         | Italic       | `<i>monitoring</i>`              |
| `<em>`        | Italic (alt) | `<em>monitoring</em>`            |
| `<code>`      | Inline code  | `<code>file.py</code>`           |
| `<pre>`       | Code block   | `<pre>error log</pre>`           |
| `<a href="">` | Link         | `<a href="https://...">Link</a>` |

**Not supported**: `<h1>`, `<div>`, `<span>`, CSS, JavaScript

### HTML Entity Escaping

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_8'
# Required escaping
&  → &amp;   # Must be first to avoid double-escaping
<  → &lt;
>  → &gt;

# Escaping function
escape_html() {
    echo "$1" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g'
}

# Usage
FILENAME=$(basename "$file" | escape_html)
MESSAGE="Modified: <code>$FILENAME</code>"
REFERENCE_SCRIPT_EOF_8
```

**Order matters**: Always escape `&` first, otherwise you'll double-escape the `&` in `&lt;` and `&gt;`.

### Message Template

```bash
MESSAGE="$EMOJI <b>Service $STATUS</b>

<b>Host</b>: <code>$HOSTNAME</code>
<b>Time</b>: $TIMESTAMP
<b>Exit Code</b>: $EXIT_CODE

<b>Trigger</b>: <code>$TRIGGER_PATH</code>
<b>Action</b>: $CHANGED_FILES

<i>Monitoring: watchexec</i>"
```

## Pushover Message Format

Pushover uses **plain text** (no HTML or Markdown):

```bash
PUSHOVER_MESSAGE="Host: $HOSTNAME
Time: $TIMESTAMP
Exit: $EXIT_CODE
File: $CHANGED_FILE"
```

**To strip HTML tags from Telegram message**:

```bash
/usr/bin/env bash << 'REFERENCE_SCRIPT_EOF_9'
# Remove all <tag> and </tag>
PLAIN_TEXT=$(echo "$HTML_MESSAGE" | sed 's/<[^>]*>//g')
REFERENCE_SCRIPT_EOF_9
```

## Testing Procedures

### 1. Test Notification Script Directly

```bash
# Startup notification
./notify-restart.sh startup 0

# Code change notification
./notify-restart.sh code_change 0

# Crash notification (with fake context)
echo "Error: Something went wrong" > /tmp/crash_context.txt
./notify-restart.sh crash 1 "" /tmp/crash_context.txt
```

### 2. Test HTML Rendering

```bash
# Message with special characters
MESSAGE="<b>Test</b>: <code>handler_classes.py</code> & <i>special_chars</i>"

# Should render correctly with underscores visible
```

### 3. Test watchexec Integration

```bash
# Start watchexec
watchexec --restart --watch ./src --exts py -- ./bot-wrapper.sh

# In another terminal, trigger change
touch ./src/test.py

# Check logs
tail -f ./logs/bot-notifications.log
```

### 4. Test Crash Handling

```bash
# Create script that crashes
cat > ./crash-test.py <<EOF
import sys
print("About to crash...")
sys.exit(1)
EOF

# Run wrapper
MAIN_SCRIPT=./crash-test.py ./bot-wrapper.sh

# Should send crash notification with exit code 1
```

## Troubleshooting

### Telegram 400 Bad Request

**Symptoms**: HTTP 400 error, no message received

**Common causes**:

1. Unescaped HTML entities (`&`, `<`, `>`)
1. Unclosed HTML tags (`<b>text` without `</b>`)
1. Unsupported HTML tags (`<div>`, `<h1>`)
1. Message too long (>4096 chars)

**Debug**:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Check archived message
cat logs/notification-archive/$(ls -t logs/notification-archive/ | head -1)

# Validate HTML structure
echo "$MESSAGE" | grep -E '<[^>]*$'  # Check for unclosed tags
PREFLIGHT_EOF
```

### File Detection Not Working

**Symptoms**: Empty Trigger/Action fields

**Check**:

```bash
# Test stat command
stat -f %m ./src/test.py  # macOS
stat -c %Y ./src/test.py  # Linux

# Check watchexec info file
cat /tmp/watchexec_info_*.json

# Verify time window (default 60s)
# File must be modified within last 60s
```

### Credentials Not Loading

**Check environment**:

```bash
# Are variables set?
echo "$TELEGRAM_BOT_TOKEN"
env | grep TELEGRAM

# Test Doppler
doppler secrets get TELEGRAM_BOT_TOKEN --plain

# Test keychain
security find-generic-password -s 'telegram-bot-token' -a "$USER" -w
```

### No Notifications Received

**Check**:

```bash
# Telegram bot token valid?
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# Chat ID correct?
# Should be negative for groups: -1001234567890

# Pushover credentials valid?
curl -s \
    --form-string "token=$PUSHOVER_APP_TOKEN" \
    --form-string "user=$PUSHOVER_USER_KEY" \
    --form-string "message=Test" \
    https://api.pushover.net/1/messages.json
```

## Performance Metrics

From production deployment (2025-10-29):

| Operation          | Latency       | Notes               |
|--------------------|---------------|---------------------|
| Message archiving  | ~5ms          | File write to logs/ |
| HTML escaping      | \<1ms         | sed operations      |
| Telegram API call  | 200-500ms     | Network dependent   |
| Pushover API call  | 100-300ms     | Network dependent   |
| **Total overhead** | **300-800ms** | Per notification    |

**Fire-and-forget**: Notifications run in background (`&`), so process restart not delayed.

## Security Best Practices

1. **Never log credentials**: Secrets should only exist in memory
1. **Restrict archive permissions**: `chmod 700 logs/notification-archive/`
1. **No secrets in filenames**: File paths appear in messages
1. **Use read-only API scopes**: Limit bot permissions
1. **Rotate credentials**: Use Doppler or similar for automated rotation
1. **Validate inputs**: Sanitize any user-provided data before archiving

## Real-World Output Example

### Telegram Message (HTML Rendered)

```
🔄 Service Restarted (code change)

Host: myserver
Time: 2025-10-29 22:58:21 PDT
PID: 31307
Exit Code: 0

Trigger: /app/lib/format_utils.py
Action: Modified: format_utils.py

Monitoring: watchexec
```

### Archived Message File

```
========================================================================
Notification Archive
========================================================================
Timestamp: 2025-10-29 22:58:21 PDT
Reason: code_change
Exit Code: 0
Host: myserver
PID: 31307

--- TELEGRAM MESSAGE ---
🔄 <b>Service Restarted (code change)</b>

<b>Host</b>: <code>myserver</code>
<b>Time</b>: 2025-10-29 22:58:21 PDT
<b>PID</b>: 31307
<b>Exit Code</b>: 0

<b>Trigger</b>: <code>/app/lib/format_utils.py</code>
<b>Action</b>: Modified: <code>format_utils.py</code>

<i>Monitoring: watchexec</i>

--- WATCHEXEC INFO FILE ---
{
  "timestamp": "2025-10-30T05:58:21Z",
  "watchexec": {
    "written_path": "/app/lib/format_utils.py"
  }
}
========================================================================
```

## Success Metrics

Production deployment results:

- ✅ 100+ notifications sent successfully
- ✅ 0 formatting errors (after HTML migration)
- ✅ 100% dual-channel delivery
- ✅ File detection: 95% accuracy (5% missing due to rapid restart \<60s window)
- ✅ Average latency: 400ms per notification
- ✅ Zero blocking (fire-and-forget background execution)

## Further Reading

- Telegram Bot API: https://core.telegram.org/bots/api#html-style
- Pushover API: https://pushover.net/api
- watchexec: https://github.com/watchexec/watchexec
- Doppler: https://docs.doppler.com/docs/cli
