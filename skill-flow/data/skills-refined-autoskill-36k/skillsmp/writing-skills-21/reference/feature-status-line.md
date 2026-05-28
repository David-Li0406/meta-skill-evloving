# Status Line

Persistent status display at bottom of terminal. **User-level config**, not skill-controlled.

## How It Works

| Aspect            | Behavior                                                           |
| ----------------- | ------------------------------------------------------------------ |
| **Trigger**       | Runs after conversation messages update (reactive, not periodic)   |
| **Refresh rate**  | Max every 300ms, throttled                                         |
| **Config timing** | Loaded at CC boot - changes require restart                        |
| **Script input**  | Rich JSON via stdin (session_id, model, cost, context_window, cwd) |

## Configuration

In `settings.json` (user or project level):

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

## Script Input (stdin)

```json
{
  "hook_event_name": "Status",
  "session_id": "abc123...",
  "cwd": "/current/working/directory",
  "model": { "id": "claude-opus-4-1", "display_name": "Opus" },
  "cost": { "total_cost_usd": 0.01234 },
  "context_window": {
    "total_input_tokens": 15234,
    "context_window_size": 200000
  }
}
```

## Script Output

First line of stdout becomes status text. ANSI colors supported.

```bash
#!/bin/bash
INPUT=$(cat)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name')
TOKENS=$(echo "$INPUT" | jq -r '.context_window.total_input_tokens')
echo -e "\033[36m$MODEL\033[0m | Tokens: $TOKENS"
```

## Examples

**Model and cost display:**

```bash
#!/bin/bash
INPUT=$(cat)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name')
COST=$(echo "$INPUT" | jq -r '.cost.total_cost_usd // 0')
echo -e "\033[36m$MODEL\033[0m | \$${COST}"
```

**Git branch + context usage:**

```bash
#!/bin/bash
INPUT=$(cat)
BRANCH=$(git branch --show-current 2>/dev/null || echo "?")
USED=$(echo "$INPUT" | jq -r '.context_window.total_input_tokens')
MAX=$(echo "$INPUT" | jq -r '.context_window.context_window_size')
PCT=$((USED * 100 / MAX))
echo -e "\033[33m$BRANCH\033[0m | Context: ${PCT}%"
```

## Limitation: Skills Cannot Trigger Refresh

**Important:** There is no API for skills to trigger a status line refresh.

- Status line only updates after conversation messages change
- If a skill writes state to a file, status line won't see it until next user interaction
- [#5685](https://github.com/anthropics/claude-code/issues/5685) requests `refreshIntervalSeconds` but not implemented

**Status line is NOT suitable for:**

- Real-time skill progress indicators
- Phase transitions that should display immediately
- Any state that changes mid-turn

**Status line IS suitable for:**

- Displaying model/cost info (provided via stdin)
- Git branch (reads from filesystem, updates on next message)
- Context window usage (provided via stdin)

## Links

- Docs: https://code.claude.com/docs/en/statusline.md
- Issues:
  - [#5685](https://github.com/anthropics/claude-code/issues/5685) - Request for interval refresh (not implemented)
  - [#15226](https://github.com/anthropics/claude-code/issues/15226) - Status bar crosstalk in multi-session
