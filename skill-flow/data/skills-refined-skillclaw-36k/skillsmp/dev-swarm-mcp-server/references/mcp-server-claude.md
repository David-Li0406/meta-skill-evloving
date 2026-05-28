# MCP Server Configuration - Claude Code CLI

Claude Code supports MCP servers with multiple configuration scopes.

## Basic Commands

```bash
# List all MCP servers
claude mcp list

# Add MCP server (local scope by default)
claude mcp add <server-name> -- <command> [args...]

# Add with environment variables
claude mcp add <server-name> --env VAR1=VALUE1 --env VAR2=VALUE2 -- <command>

# Add HTTP/SSE transport server
claude mcp add --transport http <name> <URL> --scope user
claude mcp add --transport sse <name> <URL> --scope user

# Add stdio server example
claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY -- pnpm dlx airtable-mcp-server

# Add HTTP transport server with Authorization header
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer YOUR_GITHUB_PAT"

# Remove a server
claude mcp remove <server-name>

# Add JSON configuration directly
claude mcp add-json
```

## Configuration Scopes

1. **Local Scope** (default): Available across projects, stored in `~/.claude.json`
2. **Project Scope** (`--scope project`): Team-wide, stored in `.mcp.json` at project root
3. **User/Global Scope** (`--scope user`): Available across projects, stored in `~/.claude.json`

**Examples:**

```bash
# Project scope (shared with team)
claude mcp add playwright --scope project -- npx -y @playwright/mcp-server

# User scope (global)
claude mcp add github --scope user --env GITHUB_TOKEN=token -- npx -y @modelcontextprotocol/server-github
```

## Configuration File Locations

- **User/Global**: `~/.claude.json`
- **Project**: `.mcp.json` (in project root)

## Advanced Features

- **Timeout Configuration**: Set `MCP_TIMEOUT` (e.g., `MCP_TIMEOUT=10000 claude` for 10-second timeout)
- **Enterprise Control**: Supports managed configurations with `managed-mcp.json`

**Important**: Restart Claude Code after making configuration changes.
