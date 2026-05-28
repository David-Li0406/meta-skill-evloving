---
name: meta:hook-creator
description: Create event hooks for Claude Code that trigger on specific events. Generate hooks with proper JSON configuration for automating workflows. Use when creating hooks, setting up event triggers, automating on file saves or tool calls.
---

# Hook Creator

## Quick Start

Add a hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File written!'"
          }
        ]
      }
    ]
  }
}
```

Use `/hooks` command to manage hooks interactively.

## Choosing an Approach

| Approach                 | Best For                      | Setup                          |
| ------------------------ | ----------------------------- | ------------------------------ |
| **Hookify** (`/hookify`) | Pattern-based warn/block      | Markdown files, no code        |
| **Python hooks**         | Complex logic, external tools | Python scripts + settings.json |
| **Inline bash**          | Simple one-liners             | settings.json only             |

### Decision Tree

```text
Need to detect a pattern and warn/block?
  └─ Yes → Use hookify (/hookify "Don't use console.log")
  └─ No, need complex logic?
       └─ Yes → Use Python hook script
       └─ No, just a simple command?
            └─ Yes → Inline in settings.json
```

### When to Use Hookify

- Block/warn based on regex pattern matching
- Quick setup without writing code
- Personal rules (`.local.md` files aren't committed)

```markdown
# .claude/hookify.warn-console-log.local.md

---

name: warn-console-log
enabled: true
event: file
pattern: console\.log\(
action: warn

---

Remove console.log before committing.
```

### When to Use Python Hooks

- Check file existence or conditions
- Run external validators
- Parse and analyze content
- Call APIs or external tools

```python
#!/usr/bin/env -S uv run --quiet --script
# .claude/hooks/schema-change.py
import json, sys

input_data = json.loads(sys.stdin.read())
file_path = input_data.get("tool_input", {}).get("file_path", "")

if "src/modules/db/schema" in file_path:
    print("📦 Schema modified. Run: pnpm db:generate")
```

## Hook Locations

| Location                      | Scope               | Committed |
| ----------------------------- | ------------------- | --------- |
| `.claude/settings.json`       | Project             | Yes       |
| `.claude/settings.local.json` | Project (personal)  | No        |
| `~/.claude/settings.json`     | User (all projects) | N/A       |
| Managed policy                | Enterprise          | N/A       |

## Event Types

| Event               | Trigger                   | Matcher   | Use Case          |
| ------------------- | ------------------------- | --------- | ----------------- |
| `PreToolUse`        | Before tool executes      | Tool name | Block/validate    |
| `PostToolUse`       | After tool completes      | Tool name | Format/cleanup    |
| `PermissionRequest` | Permission dialog shown   | Tool name | Auto-approve/deny |
| `UserPromptSubmit`  | User sends message        | N/A       | Transform input   |
| `Notification`      | Claude sends notification | Type      | Custom alerts     |
| `Stop`              | Main agent finishes       | N/A       | Continue/cleanup  |
| `SubagentStop`      | Subagent completes        | N/A       | Process results   |
| `SessionStart`      | Session begins            | Source    | Initialization    |
| `SessionEnd`        | Session ends              | N/A       | Final cleanup     |
| `PreCompact`        | Before compaction         | Trigger   | Pre-compact logic |

### Notification Matchers

| Matcher              | Trigger                  |
| -------------------- | ------------------------ |
| `permission_prompt`  | Permission request       |
| `idle_prompt`        | Waiting for input (60s+) |
| `auth_success`       | Authentication success   |
| `elicitation_dialog` | MCP tool elicitation     |

### SessionStart Matchers

| Matcher   | Trigger                             |
| --------- | ----------------------------------- |
| `startup` | New session                         |
| `resume`  | `--resume`, `--continue`, `/resume` |
| `clear`   | `/clear` command                    |
| `compact` | Auto or manual compact              |

## Exit Codes

| Code | Meaning | Effect                                            |
| ---- | ------- | ------------------------------------------------- |
| `0`  | Success | Continue normally                                 |
| `1`  | Error   | Show error to user                                |
| `2`  | Block   | Block action (PreToolUse, PermissionRequest only) |

## Hook Types

### Command Hook

Executes a shell command:

```json
{
  "type": "command",
  "command": "your-shell-command",
  "timeout": 30
}
```

### Prompt Hook (LLM-based)

Uses an LLM to evaluate (Stop/SubagentStop only):

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS",
  "timeout": 30
}
```

## Environment Variables

| Variable             | Available In      | Purpose                    |
| -------------------- | ----------------- | -------------------------- |
| `CLAUDE_PROJECT_DIR` | All hooks         | Project root path          |
| `CLAUDE_ENV_FILE`    | SessionStart only | Persist env variables      |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks      | Plugin directory           |
| `CLAUDE_CODE_REMOTE` | All hooks         | `"true"` if remote session |

### Persist Environment (SessionStart)

```sh
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

## Matcher Patterns

| Pattern             | Matches              |
| ------------------- | -------------------- |
| `"Write"`           | Specific tool        |
| `"Edit\|Write"`     | Multiple tools (OR)  |
| `"Bash.*"`          | Regex pattern        |
| `"*"`               | All tools            |
| `""`                | Events without tools |
| `"mcp__github__.*"` | MCP server tools     |

## Hook Configuration

```json
{
  "hooks": {
    "<EventType>": [
      {
        "matcher": "<pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hooks in Components

Skills, agents, and commands can define hooks in frontmatter:

```yaml
---
name: secure-operations
hooks:
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: './scripts/security-check.sh'
          once: true
---
```

Supported events: `PreToolUse`, `PostToolUse`, `Stop`

The `once: true` option runs the hook only once per session (skills/commands only).

## Common Templates

### Block Dangerous Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'input=$(cat); if echo \"$input\" | jq -e \".tool_input.command | test(\\\"rm -rf|--force\\\"; \\\"i\\\")\" >/dev/null 2>&1; then echo \"Blocked: Dangerous command\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

### Protect Files

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'input=$(cat); path=$(echo \"$input\" | jq -r \".tool_input.file_path // empty\"); if [[ \"$path\" == *.env* ]]; then echo \"Blocked: Protected file\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

### Auto-Format TypeScript

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'input=$(cat); file=$(echo \"$input\" | jq -r \".tool_input.file_path // empty\"); if [[ \"$file\" == *.ts ]]; then npx prettier --write \"$file\" 2>/dev/null; fi'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Desktop Notification

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs permission\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

## Script-Based Hooks

For complex logic, use Python scripts with uv instead of inline bash. See [reference.md](reference.md#script-based-hooks) for templates and examples.

## Common Mistakes

| Mistake                          | Impact                     | Correct Pattern                    |
| -------------------------------- | -------------------------- | ---------------------------------- |
| Using settings.json for patterns | Overly complex             | Use hookify for pattern matching   |
| Exit 1 in PreToolUse             | Shows error, doesn't block | Use exit 2 to block                |
| Complex inline bash              | Hard to maintain           | Use Python script with uv          |
| No timeout                       | Hangs on slow commands     | Set reasonable timeout             |
| Missing `$CLAUDE_PROJECT_DIR`    | Path errors                | Quote: `"$CLAUDE_PROJECT_DIR"/...` |
| Not testing stdin parsing        | Runtime failures           | Test: `echo '{}' \| script.py`     |

## Validation

**Run validation after every hook change:**

```sh
uv run .claude/skills/meta-hook-creator/scripts/validate-hook.py .claude/settings.json
```

### Checklist

- [ ] Hook defined in settings.json
- [ ] Event type is valid
- [ ] Matcher pattern correct for event
- [ ] Command handles stdin JSON properly
- [ ] Exit codes match intended behavior
- [ ] Timeout set appropriately
- [ ] External scripts are executable

## Delegation

- **After creating/modifying hooks**: Run `uv run .claude/skills/meta-hook-creator/scripts/validate-hook.py .claude/settings.json`
- **Pattern discovery**: For existing hook patterns, use `Explore` agent

## Additional Resources

- For advanced JSON output, MCP integration, security: [reference.md](reference.md)
- For complete Python hook examples: [examples.md](examples.md)

## References

- Official Hooks Reference: [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
- Hooks Guide: [code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)
- jq Manual: [stedolan.github.io/jq/manual](https://stedolan.github.io/jq/manual/)
