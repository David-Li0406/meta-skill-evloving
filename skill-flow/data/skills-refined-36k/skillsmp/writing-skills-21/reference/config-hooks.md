# Hooks in Skills

Define PreToolUse, PostToolUse, Stop handlers scoped to skill lifecycle.

## How It Works

Hooks run shell commands at specific events. Only these three hook types work in skills:

- `PreToolUse` - Before tool executes (validation, security)
- `PostToolUse` - After tool succeeds (linting, formatting)
- `Stop` - When skill finishes (cleanup)

## Hook Response (JSON from script)

```json
{
  "continue": true,
  "suppressOutput": true,
  "systemMessage": "Warning",
  "stopReason": "reason"
}
```

| Field            | Purpose                       |
| ---------------- | ----------------------------- |
| `continue`       | Allow/block execution         |
| `suppressOutput` | Hide stdout from transcript   |
| `systemMessage`  | Show message to user          |
| `stopReason`     | Reason if `continue` is false |

## Examples

**Security check before bash:**

```yaml
---
name: safe-shell
description: Runs shell commands with security validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

`scripts/security-check.sh`:

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if [[ "$COMMAND" == *"rm -rf"* ]]; then
  echo '{"continue": false, "stopReason": "Dangerous command blocked"}'
  exit 0
fi
echo '{"continue": true}'
```

**Auto-format after writes:**

```yaml
---
name: formatted-writer
description: Writes files with automatic formatting
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "npx prettier --write $TOOL_INPUT_FILE_PATH"
---
```

## Links

- Docs: https://code.claude.com/docs/en/hooks.md
- Guide: https://code.claude.com/docs/en/hooks-guide.md
- Issues:
  - [#4084](https://github.com/anthropics/claude-code/issues/4084) - Hook output visibility blocked
  - [#12031](https://github.com/anthropics/claude-code/issues/12031) - PreToolUse hooks strip AskUserQuestion data
