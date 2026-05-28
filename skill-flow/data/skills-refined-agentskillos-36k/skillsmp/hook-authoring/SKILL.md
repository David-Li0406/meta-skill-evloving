---
name: hook-authoring
description: |
  Writing and modifying Claude Code hooks. Auto-applies when editing files in
  hooks/, creating new hooks, or debugging hook behavior.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
---

# Hook Authoring Patterns

This skill auto-applies when you're working with Claude Code hooks. Follow these patterns for consistent, reliable hooks.

## Hook Lifecycle

```
Session Start
    │
    ├── SessionStart hook
    │
    ▼
┌─────────────────────────────────┐
│  User sends prompt              │
│      │                          │
│      ├── UserPromptSubmit hooks │
│      ▼                          │
│  Claude processes...            │
│      │                          │
│      ├── Stop hook              │
│      ▼                          │
│  (repeat)                       │
└─────────────────────────────────┘
    │
    ├── PreCompact hook
    │
    ▼
Session End
    │
    └── SessionEnd hook
```

## Required Patterns

### 1. Script Header

Always start with:

```bash
#!/bin/bash
set -euo pipefail
```

### 2. Consume stdin

**Critical:** All hooks MUST consume stdin to avoid broken pipe errors:

```bash
# Read stdin (required even if not used)
input=$(cat)

# Or if you need the JSON:
input=$(cat)
session_id=$(echo "$input" | jq -r '.session_id // empty')
```

### 3. Graceful Degradation

Hooks should work even when dependencies are missing:

```bash
# Check for jq
if ! command -v jq &>/dev/null; then
    exit 0  # Silent exit, don't break Claude
fi

# Check for event-bus-cli
if ! command -v event-bus-cli &>/dev/null; then
    cli_path="$HOME/.local/bin/event-bus-cli"
    [[ -x "$cli_path" ]] || exit 0
fi

# Check for tmux
if [[ -z "${TMUX:-}" ]]; then
    exit 0  # Not in tmux, skip tmux operations
fi
```

### 4. Exit Codes

- `exit 0` - Success (normal completion)
- Non-zero exits don't block Claude but may show error messages
- Prefer silent `exit 0` for graceful degradation

## Input JSON Format

All hooks receive JSON on stdin:

```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory"
}
```

Additional fields by trigger:
- **SessionStart:** `permission_mode`, `source` ("user" or "resume")
- **SessionEnd:** `permission_mode`, `reason`
- **PreCompact:** `trigger`

## Output Patterns

### Structured Data

Use XML tags for data Claude should parse:

```bash
echo "<recent-events>"
echo "$events"
echo "</recent-events>"
```

### Status Messages

Simple text output works:

```bash
echo "Hook completed successfully"
```

### Silent Hooks

For hooks that only have side effects (like tmux renaming):

```bash
# No output needed - tmux commands are the action
tmux rename-window "name"
```

## Tmux Integration

When modifying tmux state:

```bash
# Check if in tmux first
[[ -z "${TMUX:-}" ]] && exit 0

# Disable automatic rename before setting custom name
tmux set-window-option -q allow-rename off
tmux set-window-option -q automatic-rename off

# Now set custom name
tmux rename-window "$window_name"
```

For worktree paths, show `repo (branch)` format:

```bash
if [[ "$cwd" == */.worktrees/* ]]; then
    repo=$(basename "$(dirname "$(dirname "$cwd")")")
    branch=$(basename "$cwd")
    window_name="$repo ($branch)"
fi
```

## Event Bus Integration

For hooks that interact with the event bus:

```bash
# Find CLI
if command -v event-bus-cli &>/dev/null; then
    cli="event-bus-cli"
elif [[ -x "$HOME/.local/bin/event-bus-cli" ]]; then
    cli="$HOME/.local/bin/event-bus-cli"
else
    exit 0
fi

# Register session
"$cli" register --name "$session_name" --client-id "$session_id"

# Publish events
"$cli" publish --type "event_type" --payload "message" --session-id "$session_id"

# Get events with resume (incremental)
"$cli" events --resume --session-id "$session_id"
```

## Testing

Run `make test-hooks` to test all hooks. Tests verify:
- Script syntax is valid
- Scripts are executable
- Graceful degradation works (missing deps don't crash)

Add new test cases in `tests/test-hooks.sh`.

## Configuration

Register hooks in `settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "~/.claude/hooks/your-hook.sh" }] }]
  }
}
```

Available triggers:
- `SessionStart` - Session begins
- `SessionEnd` - Session ends
- `UserPromptSubmit` - User sends message
- `Stop` - Claude finishes response
- `PreCompact` - Before context summarization

## Reference

See existing hooks in `home/.claude/hooks/` for examples:
- `session-start.sh` - Event bus registration, tmux setup
- `session-end.sh` - Cleanup
- `prompt-events.sh` - Incremental event polling
- `tmux-status.sh` - Visual state indicator
- `pre-compact.sh` - WIP checkpointing
