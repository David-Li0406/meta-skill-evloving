---
name: hooks-reference
description: Claude Code hooks configuration reference. Use when creating hooks, understanding hook events (PreToolUse, PostToolUse, Stop, SessionStart, etc.), debugging hook behavior, or implementing automation.
---

# Claude Code Hooks Reference

Hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle, providing deterministic control over behavior.

## Quick Reference: Hook Events

| Event | When | Input | Can Control |
|-------|------|-------|-------------|
| `PreToolUse` | Before tool runs | Tool name, inputs | Block/modify tool |
| `PostToolUse` | After tool succeeds | Tool name, result | Feedback to Claude |
| `PostToolUseFailure` | After tool fails | Tool name, error | Error handling |
| `PermissionRequest` | Permission dialog shown | Details | Allow/deny |
| `UserPromptSubmit` | User submits prompt | User input | Modify prompt |
| `Notification` | Notification sent | Message | Custom notifications |
| `Stop` | Claude stops | Reason | Continue/stop |
| `SubagentStop` | Subagent completes | Result | Subagent behavior |
| `PreCompact` | Before compaction | Context | Modify context |
| `SessionStart` | Session begins | Session info | Env setup |
| `SessionEnd` | Session ends | Stats | Cleanup |

## Hook Configuration Location

```
~/.claude/settings.json          # User-level (all projects)
.claude/settings.json            # Project-level (team shared)
.claude/settings.local.json      # Project-local (gitignored)
```

## Basic Hook Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "your-script.sh"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `*` | All tools |
| `Bash` | Bash tool only |
| `Write\|Edit` | Write or Edit tools |
| `Read.*` | Read and any Read variants |

## Hook Types

### Command Hook
```json
{
  "type": "command",
  "command": "jq '.tool_input' >> /tmp/log.txt"
}
```

### Prompt Hook
```json
{
  "type": "prompt",
  "prompt": "Review the output: $ARGUMENTS"
}
```

### Agent Hook
```json
{
  "type": "agent",
  "prompt": "Verify the changes meet security requirements"
}
```

## Control Flow via Exit Codes

| Exit Code | Effect |
|-----------|--------|
| `0` | Success, continue |
| `2` | Block (PreToolUse only) |
| Non-zero | Error, continue with warning |

## Hook Output Format (stdout JSON)

```json
{
  "continue": true,
  "decision": "approve",
  "reason": "Looks good",
  "suppressOutput": false
}
```

## Common Patterns

### Auto-format on file write
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "jq -r '.tool_input.file_path' | xargs prettier --write"
    }]
  }]
}
```

### Block sensitive file edits
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "jq -e '.tool_input.file_path | test(\"\\\\.env|\\\\.git\")' && exit 2 || exit 0"
    }]
  }]
}
```

### Log all Bash commands
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
    }]
  }]
}
```

## Environment Variables in Hooks

| Variable | Value |
|----------|-------|
| `CLAUDE_PROJECT_DIR` | Project root directory |
| `CLAUDE_PLUGIN_ROOT` | Plugin installation path |

## Debugging Hooks

```bash
# View loaded hooks
/hooks

# Test hook manually with sample input
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | your-hook.sh

# Check exit code
echo $?
```

## Security Considerations

- Hooks run with your credentials
- Validate all input before use
- Don't log sensitive data
- Use absolute paths for scripts
- Test hooks in isolation first

---

For complete documentation including all event schemas, see:
- [hooks-full.md](hooks-full.md) - Complete hooks reference
- [hooks-howto.md](hooks-howto.md) - Step-by-step tutorials
