---
name: session-logs
description: Use this skill when you need to search and analyze your complete conversation history stored in session JSONL files, especially when referencing older or parent conversations.
---

# Skill body

## Trigger

Use this skill when the user asks about prior chats, parent conversations, or historical context that isn’t in memory files.

## Location

Session logs live at: `~/.<agentType>/agents/<agentId>/sessions/` (use the `agent=<id>` value from the system prompt Runtime line).

- **`sessions.json`** - Index mapping session keys to session IDs
- **`<session-id>.jsonl`** - Full conversation transcript per session

## Structure

Each `.jsonl` file contains messages with:
- `type`: "session" (metadata) or "message"
- `timestamp`: ISO timestamp
- `message.role`: "user", "assistant", or "toolResult"
- `message.content[]`: Text, thinking, or tool calls (filter `type=="text"` for human-readable content)
- `message.usage.cost.total`: Cost per response

## Common Queries

### List all sessions by date and size
```bash
for f in ~/.<agentType>/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$date $size $(basename $f)"
done | sort -r
```

### Find sessions from a specific day
```bash
for f in ~/.<agentType>/agents/<agentId>/sessions/*.jsonl; do
  head -1 "$f" | jq -r '.timestamp' | grep -q "2026-01-06" && echo "$f"
done
```

### Extract user messages from a session
```bash
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

### Search for keyword in assistant responses
```bash
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl | rg -i "keyword"
```

### Get total cost for a session
```bash
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl
```

### Daily cost summary
```bash
for f in ~/.<agentType>/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r
```

### Count messages and tokens in a session
```bash
jq -s '{
  messages: length,
  user: [.[] | select(.message.role == "user")]
}' <session>.jsonl
```