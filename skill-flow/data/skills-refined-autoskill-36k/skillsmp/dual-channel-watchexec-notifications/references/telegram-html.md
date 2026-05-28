**Skill**: [Dual-Channel Watchexec Notifications](../SKILL.md)

## Telegram: Use HTML Mode (NOT Markdown)

### Why HTML Mode

**Industry Best Practice**:

- Markdown/MarkdownV2 requires escaping 40+ special characters (`.`, `-`, `_`, etc.)
- HTML only requires escaping 3 characters: `&`, `<`, `>`
- More reliable, simpler, less error-prone

### HTML Formatting

```python
# Python API call
data = {
    'chat_id': chat_id,
    'text': message,
    'parse_mode': 'HTML'  # NOT 'Markdown' or 'MarkdownV2'
}
```

**HTML Tags**:

- Bold: `<b>text</b>`
- Code: `<code>text</code>`
- Italic: `<i>text</i>`
- Code blocks: `<pre>text</pre>`

**HTML Escaping** (Bash):

```bash
/usr/bin/env bash << 'TELEGRAM_HTML_SCRIPT_EOF'
# Escape special chars before sending
ESCAPED=$(echo "$text" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
MESSAGE="<b>Alert</b>: <code>$ESCAPED</code>"
TELEGRAM_HTML_SCRIPT_EOF
```

### Message Template

**Simplified format**:

```bash
/usr/bin/env bash << 'TELEGRAM_HTML_SCRIPT_EOF_2'
# Build session debug line
SESSION_DEBUG_LINE="session=$CLAUDE_SESSION_ID | debug=~/.claude/debug/\${session}.txt"

# Normal restart (code change or startup)
MESSAGE="$EMOJI <b>Bot $STATUS</b>

<b>Directory</b>: <code>$WORKING_DIR</code>
<b>Branch</b>: <code>$GIT_BRANCH</code>
<code>$SESSION_DEBUG_LINE</code>
$WATCHEXEC_DETAILS"

# Crash (includes exit code and error details)
MESSAGE="$EMOJI <b>Bot Crashed</b>

<b>Directory</b>: <code>$WORKING_DIR</code>
<b>Branch</b>: <code>$GIT_BRANCH</code>
<code>$SESSION_DEBUG_LINE</code>

<b>Exit Code</b>: $EXIT_CODE
$CRASH_INFO"
TELEGRAM_HTML_SCRIPT_EOF_2
```

**Why this format**:

- Consistent with other Telegram messages (workflow completions, notifications)
- Removes unnecessary info (host, monitoring system, timestamp)
- Adds context (session ID, branch, directory)
- Exit code only shown for crashes (not for normal restarts with exit code 0)
