**Skill**: [Dual-Channel Watchexec Notifications](../SKILL.md)

## Credential Loading (Canonical Source)

**Load from Doppler** (notifications/dev):

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Canonical source for Pushover credentials
export PUSHOVER_APP_TOKEN=$(doppler secrets get PUSHOVER_APP_TOKEN \
  --project notifications \
  --config dev \
  --plain)
export PUSHOVER_USER_KEY=$(doppler secrets get PUSHOVER_USER_KEY \
  --project notifications \
  --config dev \
  --plain)
CONFIG_EOF
```

See: `credential-management.md` for fallback patterns (JSON config, local override)

---

## API Call Pattern

```bash
curl -s \
  --form-string "token=$PUSHOVER_APP_TOKEN" \
  --form-string "user=$PUSHOVER_USER_KEY" \
  --form-string "device=device_name" \
  --form-string "title=$TITLE" \
  --form-string "message=$MESSAGE" \
  --form-string "sound=$SOUND" \
  --form-string "priority=$PRIORITY" \
  https://api.pushover.net/1/messages.json
```

**Priority Levels**:

- `0`: Normal (default sound, respects quiet hours)
- `1`: High (bypasses quiet hours, alert sound)

**Sounds**: `cosmic`, `bike`, `siren`, etc.

### CRITICAL: Pushover Does NOT Support HTML

**Pushover uses plain text only** - MUST strip HTML tags before sending:

```bash
/usr/bin/env bash << 'PUSHOVER_INTEGRATION_SCRIPT_EOF'
# ❌ WRONG - Pushover will display literal HTML tags
PUSHOVER_MESSAGE="<b>Alert</b>: <code>file.py</code>"
# User sees: <b>Alert</b>: <code>file.py</code>

# ✅ CORRECT - Strip HTML tags for plain text
CHANGED_FILES_PLAIN=$(echo "$CHANGED_FILES" | sed 's/<[^>]*>//g')
PUSHOVER_MESSAGE="Alert: $CHANGED_FILES_PLAIN"
# User sees: Alert: file.py
PUSHOVER_INTEGRATION_SCRIPT_EOF
```

**Why This Matters**:

- Telegram uses HTML mode for formatting
- Pushover does NOT interpret HTML
- Sending HTML to Pushover shows ugly `<code>`, `<b>` tags in notification
- Always strip tags: `sed 's/<[^>]*>//g'`

**Pattern**: Build message in HTML for Telegram, then strip tags for Pushover:

```bash
/usr/bin/env bash << 'PUSHOVER_INTEGRATION_SCRIPT_EOF_2'
# 1. Build HTML message for Telegram
MESSAGE_HTML="<b>File</b>: <code>handler_classes.py</code>"

# 2. Strip HTML for Pushover
MESSAGE_PLAIN=$(echo "$MESSAGE_HTML" | sed 's/<[^>]*>//g')
# Result: "File: handler_classes.py"
PUSHOVER_INTEGRATION_SCRIPT_EOF_2
```
