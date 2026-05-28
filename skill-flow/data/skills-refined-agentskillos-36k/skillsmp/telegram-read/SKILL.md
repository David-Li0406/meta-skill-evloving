---
name: telegram-read
description: "Read and search synced Telegram messages. Use when user asks about Telegram conversations, wants to see messages, or search for specific content."
---

# telegram-read

Read and search synced Telegram messages.

## Trigger Phrases

- "read Telegram messages"
- "what's in the Telegram group"
- "search Telegram for [keyword]"
- "show Telegram messages"
- "telegram read"

## Description

This skill reads messages from locally synced Telegram data. It can show recent messages, search for keywords, or filter by date.

## Usage

Read all messages from default group:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py
```

Read from specific group:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --group 1234567890
```

Show last N messages:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --last 20
```

Search for keyword:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --search "meeting"
```

Filter by date:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --date 2026-01-06
```

Read specific topic:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --group 1234567890 --topic announcements
```

Output as JSON:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_read.py --json
```

## Output Format

### Markdown Output (default)

```markdown
# My Group

Group: My Group (1234567890)
Type: supergroup
Last synced: 2026-01-06T12:00:00Z

---

## 2026-01-06

### 10:30 AM - @alice (123456)
Hello everyone!

### 10:31 AM - @bob (789012)
↳ replying to @alice:
Hey Alice!
```

### JSON Output (--json)

```json
{
  "group_id": 1234567890,
  "topic": "general",
  "message_count": 50,
  "messages": [
    {
      "date": "2026-01-06",
      "time": "10:30 AM",
      "author": "@alice (123456)",
      "content": "Hello everyone!"
    }
  ]
}
```

## Search Mode

When using `--search`, only messages containing the keyword are returned:

```bash
python telegram_read.py --search "Python"
```

Output:
```
Found 3 messages matching 'Python':

### 10:30 AM - @alice (123456)
I love Python programming!

----------------------------------------

### 2:15 PM - @charlie (456789)
Python is great for automation

----------------------------------------
```

## Reading Tips

1. **Start with recent messages**: Use `--last 20` to see the latest activity
2. **Search specific topics**: Combine `--topic` with `--search` for targeted searches
3. **Export for analysis**: Use `--json` to get structured data for further processing

## Prerequisites

You must sync messages before reading:
```bash
python plugins/telegram-agent/tools/telegram_sync.py --group 1234567890
```

## Exit Codes

- `0` - Success
- `1` - No synced data found
- `2` - Configuration error

## Related Skills

- `telegram-sync` - Sync messages from Telegram
- `telegram-list` - List groups and topics
- `telegram-send` - Send messages to Telegram
