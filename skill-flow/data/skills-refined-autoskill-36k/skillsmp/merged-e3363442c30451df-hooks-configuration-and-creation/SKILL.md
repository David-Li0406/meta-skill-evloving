---
name: hooks-configuration-and-creation
description: Use this skill when you need to configure, create, or troubleshoot Claude Code hooks, including setting up PreToolUse, PostToolUse, and UserPromptSubmit hooks for automation and validation.
---

# Claude Code Hooks

This document serves as a comprehensive guide for creating and configuring hooks in Claude Code. Hooks are event-driven automation scripts that execute at specific points in the workflow, allowing for validation, modification, and feedback.

## Hook Types

| Type              | Trigger                   | Use Cases                                      |
|-------------------|--------------------------|------------------------------------------------|
| `PreToolUse`      | Before tool execution     | Validate inputs, block operations, modify parameters |
| `PostToolUse`     | After tool completes      | Check results, run linters, provide feedback   |
| `UserPromptSubmit`| When user sends message   | Pre-process input, add context                 |
| `Stop`            | Session ends              | Cleanup, save state                             |
| `SubagentStop`    | Subagent completes        | Process results                                 |
| `PreCompact`      | Before context compaction | Save important state                            |
| `Notification`    | System notification       | Log events                                     |

## Configuration Locations

Hooks are configured in settings files, with the following hierarchy:

| Location                      | Scope               | Committed |
|-------------------------------|---------------------|-----------|
| `~/.claude/settings.json`     | User (all projects) | No        |
| `.claude/settings.json`       | Project             | Yes       |
| `.claude/settings.local.json` | Local project       | No        |
| Plugin hooks                  | Plugin-specific     | Yes       |

## Hook Structure

Hooks are defined in JSON format within the settings files. Here’s a basic structure:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Matcher Syntax

| Pattern             | Matches               | Example                      |
|---------------------|-----------------------|------------------------------|
| `Write`             | Exact tool name       | Only Write tool              |
| `Edit|Write`        | Regex OR              | Edit or Write                |
| `Notebook.*`        | Regex wildcard         | NotebookEdit, NotebookRead   |
| `mcp__memory__.*`   | MCP server tools      | All memory server tools      |
| `*` or `""`         | All tools             | Any tool                     |

**Note:** Matchers are case-sensitive and apply to `PreToolUse`, `PostToolUse`, and `PermissionRequest`.

## Hook Input and Output

### Input Format

All hooks receive JSON input via stdin, which includes common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "EventName"
}
```

### Output Format

**PreToolUse** - Control execution:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use gh cli instead"
  }
}
```

**PostToolUse** - Provide feedback:

```json
{
  "hookSpecificOutput": {
    "additionalContext": "Lint errors found..."
  }
}
```

## Environment Variables

Available in all hooks:

| Variable             | Description                          |
|----------------------|--------------------------------------|
| `CLAUDE_PROJECT_DIR` | Absolute path to project root        |
| `CLAUDE_PLUGIN_ROOT` | Absolute path to plugin directory    |
| `CLAUDE_ENV_FILE`    | File path for persisting env vars    |
| `CLAUDE_CODE_REMOTE` | `"true"` if running in web environment |

## Common Use Cases

### Auto-Format on File Write

Automatically format files after they are written:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh\""
          }
        ]
      }
    ]
  }
}
```

### Block Dangerous Commands

Prevent execution of harmful commands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'input=$(cat); if echo \"$input\" | jq -e \".tool_input.command | test(\\\"rm -rf\\\")\" >/dev/null 2>&1; then echo \"Blocked: Dangerous command\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

### Inject Context on Session Start

Load context when a session begins:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Git branch: $(git branch --show-current)\""
          }
        ]
      }
    ]
  }
}
```

## Debugging Hooks

To troubleshoot hooks, use the following commands:

- Check loaded hooks with `/hooks`.
- Run `claude --debug` to see detailed logs of hook execution.
- Validate JSON output using `jq`.

## Security Considerations

- Always validate and sanitize inputs.
- Quote shell variables to prevent injection attacks.
- Use absolute paths for scripts to avoid path traversal vulnerabilities.

## Conclusion

This guide provides a comprehensive overview of creating and managing hooks in Claude Code. For further assistance, consult the official documentation or use the Task tool with `subagent_type='claude-code-guide'`.