---
name: agentio-telegram
description: Use when sending messages to Telegram channels. Requires agentio CLI with a configured Telegram bot profile.
---

# Telegram Operations with agentio

Use `agentio telegram` commands to send messages to Telegram channels. Multiple profiles can be configured - the default profile is used unless you specify `--profile <name>`.

## Send a Message

```bash
agentio telegram send <message> [options]
```

Or pipe via stdin:
```bash
echo "Message content" | agentio telegram send
```

Options:
- `--profile <name>`: Use specific profile
- `--parse-mode <mode>`: Message format - `html` or `markdown`
- `--silent`: Send without notification

## Examples

Simple message:
```bash
agentio telegram send "Hello from agentio"
```

HTML formatted:
```bash
agentio telegram send "<b>Bold</b> and <i>italic</i>" --parse-mode html
```

Markdown formatted:
```bash
agentio telegram send "*Bold* and _italic_" --parse-mode markdown
```

Silent notification:
```bash
agentio telegram send "Update completed" --silent
```
