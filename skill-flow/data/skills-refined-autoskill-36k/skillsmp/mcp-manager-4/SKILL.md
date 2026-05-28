---
name: mcp-manager
description: Manage MCP servers - add, list, enable, and disable. Use when users ask about MCP server configuration, want to add new servers, or need to enable/disable existing ones.
---

# MCP Manager

## Overview

Manage MCP (Model Context Protocol) servers in Claude Code. This skill helps with:
- Listing configured MCP servers
- Adding new MCP servers
- Enabling disabled servers
- Disabling servers without removing them

## When to Use This Skill

- User asks "what MCP servers do I have?"
- User wants to "add an MCP server"
- User needs to "enable" or "disable" a server
- User asks about MCP configuration

## Quick Reference

| Task | Command |
|------|---------|
| List servers | `claude mcp list` |
| Add HTTP server | `claude mcp add --transport http <name> <url>` |
| Add stdio server | `claude mcp add --transport stdio <name> -- <cmd>` |
| Get server details | `claude mcp get <name>` |
| Remove server | `claude mcp remove <name>` |
| Check status | `/mcp` (in Claude Code) |

## Scopes

MCP servers can be configured at different scopes:

| Scope | Flag | Description |
|-------|------|-------------|
| local | `--scope local` | Private to you, current project only (default) |
| project | `--scope project` | Shared via `.mcp.json`, version controlled |
| user | `--scope user` | Available across all your projects |

## Enable/Disable via Settings

Servers can be enabled/disabled without removing them:

```json
// In ~/.claude/settings.json or .claude/settings.json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["github", "sentry"],
  "disabledMcpjsonServers": ["filesystem"]
}
```

## Common Server Examples

### GitHub

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

### Sentry

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

### PostgreSQL Database

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

### Filesystem (Local)

```bash
claude mcp add --transport stdio filesystem -- npx -y @anthropics/mcp-filesystem
```

## Troubleshooting

1. **Server not connecting**: Check with `/mcp` command in Claude Code
2. **Permission denied**: May need to re-authenticate with `/mcp`
3. **Changes not applying**: Restart Claude Code after config changes
