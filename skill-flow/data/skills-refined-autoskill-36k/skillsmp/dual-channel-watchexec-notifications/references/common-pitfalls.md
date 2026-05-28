**Skill**: [Dual-Channel Watchexec Notifications](../SKILL.md)

## Common Pitfalls

### Pitfall 1: Pushover Shows HTML Tags (CRITICAL)

**Problem**: Pushover displays literal `<code>`, `<b>`, `</code>` in notifications

**Cause**: Pushover uses **plain text only** - does NOT interpret HTML

**Solution**: Strip HTML tags before sending to Pushover

```bash
/usr/bin/env bash << 'COMMON_PITFALLS_SCRIPT_EOF'
# ❌ WRONG - Sends HTML to Pushover
PUSHOVER_MESSAGE="Modified: <code>handler_classes.py</code>"
# User sees: Modified: <code>handler_classes.py</code>

# ✅ CORRECT - Strip HTML tags
CHANGED_FILES_PLAIN=$(echo "$CHANGED_FILES" | sed 's/<[^>]*>//g')
PUSHOVER_MESSAGE="Modified: $CHANGED_FILES_PLAIN"
# User sees: Modified: handler_classes.py
COMMON_PITFALLS_SCRIPT_EOF
```

**Remember**: Telegram = HTML, Pushover = Plain Text

### Pitfall 2: Markdown Escaping Hell

**Problem**: Files with underscores (`handler_classes.py`) display as `handlerclasses.py`

**Cause**: Markdown treats `_` as italic marker

**Solution**: Use HTML mode, wrap in `<code>` tags

```bash
/usr/bin/env bash << 'COMMON_PITFALLS_SCRIPT_EOF_2'
# ❌ WRONG (Markdown)
MESSAGE="Modified: handler_classes.py"  # Renders: handlerclasses.py

# ✅ CORRECT (HTML)
FILENAME=$(basename "$file" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
MESSAGE="Modified: <code>$FILENAME</code>"  # Renders: handler_classes.py
COMMON_PITFALLS_SCRIPT_EOF_2
```

### Pitfall 3: Literal Variable Names Sent

**Problem**: Telegram receives literal text `"$MESSAGE"` instead of content

**Cause**: Heredoc with quotes prevents variable expansion

**Solution**: Use heredoc WITHOUT quotes

```bash
# ❌ WRONG
cat > "$FILE" <<'MSGEOF'
$MESSAGE
MSGEOF

# ✅ CORRECT
cat > "$FILE" <<MSGEOF
$MESSAGE
MSGEOF
```

### Pitfall 4: macOS File Detection Failures

**Problem**: Empty Trigger/Action fields, no file detected

**Cause**: `find -newermt` syntax differs on BSD (macOS) vs GNU (Linux)

**Solution**: Use `stat` instead of `find -newermt`

```bash
/usr/bin/env bash << 'COMMON_PITFALLS_SCRIPT_EOF_3'
# ✅ CORRECT (portable)
FILE_MTIME=$(stat -f %m "$file" 2>/dev/null || echo "0")  # macOS
# For Linux: stat -c %Y "$file"
COMMON_PITFALLS_SCRIPT_EOF_3
```

### Pitfall 5: Telegram 400 Bad Request

**Problem**: HTTP 400 errors with "Bad Request"

**Causes**:

1. Missing HTML escaping (`&`, `<`, `>`)
2. Unclosed HTML tags
3. Invalid HTML structure

**Solution**: Always escape special chars, validate HTML structure

```bash
# Test message before sending
echo "$MESSAGE" | grep -E '<[^>]*$'  # Check for unclosed tags
```

### Pitfall 6: Hardcoded Credentials

**Problem**: Secrets leaked in git, exposed in logs

**Solution**: Use Doppler (canonical), env vars, or keychain

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
# ❌ WRONG - Hardcoded secrets
PUSHOVER_APP_TOKEN="aej7osoja3x8nvxgi96up2poxdjmfj"
TELEGRAM_BOT_TOKEN="1234567890:ABC..."

# ✅ CORRECT - Load from Doppler (canonical source)
# For Pushover (notifications/dev):
PUSHOVER_APP_TOKEN=$(doppler secrets get PUSHOVER_APP_TOKEN \
  --project notifications --config dev --plain)
PUSHOVER_USER_KEY=$(doppler secrets get PUSHOVER_USER_KEY \
  --project notifications --config dev --plain)

# For Telegram (claude-config/dev):
TELEGRAM_BOT_TOKEN=$(doppler secrets get TELEGRAM_BOT_TOKEN \
  --project claude-config --config dev --plain)

# ✅ ALSO CORRECT - Validate env vars are set
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
if [[ -z "$TELEGRAM_BOT_TOKEN" ]]; then
    echo "Error: TELEGRAM_BOT_TOKEN not set"
    exit 1
fi
VALIDATE_EOF
```

See: `credential-management.md` for complete patterns
