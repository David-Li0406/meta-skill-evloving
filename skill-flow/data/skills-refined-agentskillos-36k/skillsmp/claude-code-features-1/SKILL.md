---
name: claude-code-features
description: Comprehensive reference of Claude Code features. Use when asking about Claude Code capabilities, hooks, skills, agents, plugins, or configuration.
---

# Claude Code Feature Reference

Comprehensive list of Claude Code features as of January 2026.

## Configuration Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project memory, read at session start |
| `.claude/settings.json` | Hook configuration, permissions |
| `.claude/settings.local.json` | Personal overrides (gitignored) |
| `.mcp.json` | MCP server configuration |
| `.lsp.json` | LSP server configuration |

## Hooks (13 Types)

| Hook | Trigger |
|------|---------|
| `SessionStart` | Session begins |
| `SessionEnd` | Session ends |
| `UserPromptSubmit` | User submits prompt |
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After tool succeeds |
| `PostToolUseFailure` | After tool fails |
| `PermissionRequest` | Permission requested |
| `Notification` | Notification sent |
| `Stop` | Agent stopping |
| `SubagentStart` | Subagent begins |
| `SubagentStop` | Subagent completes |
| `PreCompact` | Before context compaction |
| `Setup` | Repository init/maintenance |

### Hook Types
- `command` - Execute shell command
- `prompt` - Inject prompt (Stop/SubagentStop only)

### Hook Response Format
```json
{
  "continue": true,
  "stopReason": "string",
  "systemMessage": "string",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask"
  }
}
```

## Skills

### Required Frontmatter
- `name` - Lowercase, hyphens, max 64 chars
- `description` - When to use, max 1024 chars

### Optional Frontmatter
- `allowed-tools` - Tools allowed without permission
- `model` - Specific model to use
- `context: fork` - Isolated sub-agent context
- `agent` - Agent type for fork context
- `hooks` - Lifecycle hooks
- `user-invocable` - Slash command visibility

## Subagents

### Required Frontmatter
- `name` - Lowercase with hyphens
- `description` - When to delegate

### Optional Frontmatter
- `tools` - Available tools
- `disallowedTools` - Denied tools
- `model` - sonnet, opus, haiku, inherit
- `permissionMode` - default, acceptEdits, dontAsk, bypassPermissions, plan
- `skills` - Skills to load
- `hooks` - Lifecycle hooks

### Built-in Agents
- Explore - Fast read-only (Haiku)
- Plan - Research for planning
- general-purpose - Complex tasks
- Bash - Terminal commands

## Plugins

### Structure
```
plugin/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/hooks.json
├── .mcp.json
└── .lsp.json
```

## Permissions

```json
{
  "permissions": {
    "allow": ["Bash(git diff:*)"],
    "ask": ["Bash(git push:*)"],
    "deny": ["Read(./.env)"]
  }
}
```

## MCP Servers

```json
{
  "mcpServers": {
    "name": {
      "command": "npx",
      "args": ["-y", "@package/name"],
      "env": {}
    }
  }
}
```

---

*Last verified: January 2026*
