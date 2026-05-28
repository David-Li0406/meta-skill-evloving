---
name: agentio-gchat
description: Use when interacting with Google Chat - send messages, list messages, or get message details. Requires agentio CLI with a configured Google Chat profile (webhook or OAuth).
---

# Google Chat Operations with agentio

Use `agentio gchat` commands to interact with Google Chat. Multiple profiles can be configured - the default profile is used unless you specify `--profile <name>`.

Profiles can be either:
- **Webhook**: Send-only, simple setup
- **OAuth**: Full access (send, list, get messages)

## Send a Message

```bash
agentio gchat send <message> [options]
```

Or pipe via stdin:
```bash
echo "Message content" | agentio gchat send
```

Options:
- `--profile <name>`: Use specific profile
- `--space <id>`: Space ID (required for OAuth profiles)
- `--thread <id>`: Thread ID to reply to (optional)
- `--json [file]`: Send rich message from JSON file (or stdin)

## List Messages (OAuth only)

```bash
agentio gchat list --space <id> [--limit N]
```

Options:
- `--space <id>`: Space ID (required)
- `--limit <n>`: Number of messages (default: 10)

## Get a Message (OAuth only)

```bash
agentio gchat get <message-id> --space <id>
```

## Examples

Simple message (webhook):
```bash
agentio gchat send "Deployment complete"
```

Message to specific space (OAuth):
```bash
agentio gchat send "Status update" --space spaces/AAAA1234
```

Rich message with JSON:
```bash
agentio gchat send --json message.json
```

Or via stdin:
```bash
cat <<EOF | agentio gchat send --json
{
  "text": "Build status",
  "cards": [{"header": {"title": "CI/CD"}}]
}
EOF
```
