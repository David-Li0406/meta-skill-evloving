# Hook Visibility Patterns

Detailed documentation on how Claude Code processes hook output.

## The Core Problem

PostToolUse hooks execute successfully but their stdout is not visible to Claude. This is **by design** - Claude Code only surfaces hook output when specific conditions are met.

## Exit Code Behavior

| Exit Code | stdout Processing                       | stderr Processing     | Claude Visibility             |
| --------- | --------------------------------------- | --------------------- | ----------------------------- |
| **0**     | JSON parsed, shown in verbose mode only | Ignored               | Only if `"decision": "block"` |
| **2**     | Ignored entirely                        | Shown to Claude       | stderr visible                |
| **Other** | Ignored                                 | Shown in verbose mode | Not visible to Claude         |

### Exit Code 0: The Default Path

When hook exits with code 0:

1. stdout is expected to be JSON
2. JSON is parsed but NOT shown to Claude by default
3. Only the `reason` field is shown IF `decision` equals `"block"`
4. The operation continues normally (despite the "blocking" terminology)

### Exit Code 2: Hard Block Path

When hook exits with code 2:

1. stdout is completely ignored
2. stderr is shown to Claude and user
3. Operation is blocked (user must confirm to proceed)
4. Use for genuine blocking scenarios (security issues, invalid state)

## JSON Output Schema

Full schema for exit code 0 hooks:

```json
{
  "decision": "block",
  "reason": "Message visible to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra context (informational only, not shown to Claude)"
  },
  "continue": true,
  "suppressOutput": true,
  "systemMessage": "Optional warning shown to user"
}
```

### Required Fields for Visibility

| Field      | Required | Purpose                      |
| ---------- | -------- | ---------------------------- |
| `decision` | Yes      | Must be `"block"` for output |
| `reason`   | Yes      | The message Claude sees      |

### Optional Fields

| Field                | Default | Purpose                               |
| -------------------- | ------- | ------------------------------------- |
| `continue`           | `true`  | Whether to continue after hook        |
| `suppressOutput`     | `false` | Hide tool output from user            |
| `systemMessage`      | `null`  | Warning message for user (not Claude) |
| `hookSpecificOutput` | `null`  | Additional context (logged only)      |

## Why "decision: block" When Not Blocking?

This is a known UX issue documented in [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983).

The terminology is misleading:

- `"decision": "block"` does NOT block the operation
- It just means "show this to Claude"
- The operation continues normally with exit code 0

Think of it as: **"block" = "break into Claude's attention"** rather than "block the operation"

## Working Example

From `chezmoi-sync-reminder.sh`:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/usr/bin/env bash
set -euo pipefail

PAYLOAD=$(cat)
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')

[[ -z "$FILE_PATH" ]] && exit 0

# Expand ~ to absolute path
ABSOLUTE_PATH=$(eval echo "$FILE_PATH")

# Check if file is chezmoi-managed
if grep -qxF "$ABSOLUTE_PATH" "$CACHE_FILE" 2>/dev/null; then
    REL_PATH="${ABSOLUTE_PATH/#$HOME/~}"

    # Output JSON with decision:block - REQUIRED for Claude to see
    jq -n \
        --arg reason "[CHEZMOI] $REL_PATH is tracked. Sync with: chezmoi add $REL_PATH" \
        '{decision: "block", reason: $reason}'
fi

exit 0
PREFLIGHT_EOF
```

## What Claude Sees

When this hook fires, Claude receives a system-reminder like:

```
PostToolUse:Edit hook blocking error from command: "...chezmoi-sync-reminder.sh":
[CHEZMOI] ~/.gitconfig is tracked. Sync with: chezmoi add ~/.gitconfig
```

The "blocking error" label is cosmetic - the edit operation completed successfully.

## References

- [ADR: PostToolUse Hook Visibility](../../../../../docs/adr/2025-12-17-posttooluse-hook-visibility.md)
- [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
