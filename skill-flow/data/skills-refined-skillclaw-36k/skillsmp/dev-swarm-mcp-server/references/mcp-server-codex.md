# MCP Server Configuration - OpenAI Codex CLI

Codex CLI supports MCP servers configured at the user level.

## Basic Commands

```bash
# List MCP servers
codex mcp list

# Add MCP server
codex mcp add <server-name> -- <stdio-server-command>

# Add with environment variables
codex mcp add <server-name> --env VAR1=VALUE1 --env VAR2=VALUE2 -- <stdio-server-command>

# Example
codex mcp add context7 -- npx -y @upstash/context7-mcp

# Remove a server
codex mcp remove <server-name>
```

## Configuration File

- **Location**: `~/.codex/config.toml`
- The CLI and IDE extension share this configuration
- Configuration format uses TOML with `[mcp_servers.<server-name>]` tables

**Configuration Options:**
- `command` (required): The command that starts the server
- `startup_timeout_sec` (optional): Timeout in seconds for server startup (default: 10)
- `enabled` (optional): Set to false to disable without deleting

**Example TOML Configuration:**

```toml
[mcp_servers.context7]
command = "npx -y @upstash/context7-mcp"

[mcp_servers.github]
command = "npx -y @modelcontextprotocol/server-github"
startup_timeout_sec = 15
enabled = true
```

**Note**: Codex does not support project-level MCP configuration. All servers are configured at the user level.
