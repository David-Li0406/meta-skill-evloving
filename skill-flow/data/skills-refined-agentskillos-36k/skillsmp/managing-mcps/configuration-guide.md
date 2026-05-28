# MCP Configuration Guide

Reference for connecting and configuring MCP servers in Claude Code.

## CLI Commands (Primary Method)

### Add MCP Server

```bash
claude mcp add --transport [stdio|http|sse] [--scope local|project|user] [--env KEY=VALUE] [--header "Name: Value"] [name] [command/url]
```

**Available flags:**
- `--transport` - Required: stdio (local), http (remote), sse (deprecated)
- `--scope` - Optional: local (default), project, user
- `--env KEY=VALUE` - Optional: Environment variables (repeatable)
- `--header "Name: Value"` - Optional: HTTP headers for http/sse (repeatable)
- `--` - Required for stdio: Separates Claude flags from server command

**stdio transport (local servers):**
```bash
# Default scope (local)
claude mcp add --transport stdio my-server -- node /path/to/server.js

# Project scope (team-shared)
claude mcp add --transport stdio --scope project github -- npx -y @modelcontextprotocol/server-github

# With environment variables
claude mcp add --transport stdio --env API_KEY=secret my-server -- node server.js

# Multiple env vars
claude mcp add --transport stdio --env KEY1=val1 --env KEY2=val2 server -- python server.py

# Windows (native, not WSL): Use cmd /c wrapper for npx
claude mcp add --transport stdio github -- cmd /c npx -y @modelcontextprotocol/server-github
```

**Windows-specific requirement:**
Native Windows (not WSL) requires `cmd /c` wrapper for npx-based servers. Without it, servers fail with "Connection closed" errors. WSL and other platforms don't need this wrapper.

**http transport (remote servers, recommended):**
```bash
# Basic HTTP server
claude mcp add --transport http github https://api.githubcopilot.com/mcp

# With authentication header
claude mcp add --transport http api --header "Authorization: Bearer token" https://api.example.com/mcp

# Multiple headers
claude mcp add --transport http api --header "Auth: Bearer token" --header "X-Version: 1.0" https://api.example.com/mcp

# User scope (personal, cross-project)
claude mcp add --transport http --scope user my-api https://api.example.com/mcp
```

**sse transport (deprecated, avoid for new servers):**
```bash
claude mcp add --transport sse legacy-server https://old.example.com/sse
```

### List Servers

```bash
claude mcp list
```

Returns all configured MCP servers across all scopes.

### Get Server Details

```bash
claude mcp get [name]
```

Shows specific server configuration.

### Remove Server

```bash
claude mcp remove [name]
```

Deletes server configuration.

### Add from JSON

```bash
claude mcp add-json [json-string]
```

Add server from JSON configuration string.

### Import from Claude Desktop

```bash
claude mcp add-from-claude-desktop
```

Import existing Claude Desktop MCP server configurations.

### Reset Project Approvals

```bash
claude mcp reset-project-choices
```

Clear approval selections for project-scope MCP servers.

**Why this exists:** Project-scoped servers (from `.mcp.json` files) require explicit user approval before first use for security. Claude Code prompts users to approve or deny project servers when detected. This command clears those approval decisions, forcing re-prompting on next use.

### Run Claude Code as MCP Server

```bash
claude mcp serve
```

Runs Claude Code itself as an MCP server that other applications can connect to.

### In-Conversation Commands

**Check server status and authenticate:**
```
/mcp
```

Use within Claude Code conversation to:
- View connected servers
- Check connection status
- Trigger OAuth authentication for protected servers
- View available tools/resources/prompts

## Scope Levels

Three configuration tiers with priority: **Local > Project > User**

### Local Scope (Default)

- Personal, session-specific
- Not persisted to files
- Highest priority
- Use for temporary development servers

### Project Scope

- File: `.mcp.json` in project root
- Team-shared, commit to git
- Second priority
- Use for project-required MCPs

### User Scope

- Cross-project personal settings
- Lowest priority
- Use for personal tool MCPs used across projects

**Priority Resolution:**
If same server name configured in multiple scopes:
1. Local wins (if present)
2. Project wins over User
3. User is fallback

## .mcp.json Structure

When direct file manipulation needed (Read/Edit operations).

**Location:** Project root `.mcp.json`

### Basic Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["/absolute/path/to/server.js"],
      "env": {
        "API_KEY": "${API_KEY}",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

**Required fields:**
- `mcpServers`: Object containing all server configs
- `server-name`: Unique identifier (your choice)
- Transport config: Either `command`+`args` (stdio) OR `url` (http/sse)

**Optional fields:**
- `env`: Environment variables
- `disabled`: Set `true` to temporarily disable

### stdio Transport

```json
{
  "mcpServers": {
    "local-server": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"]
    },
    "python-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    },
    "npm-package": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    }
  }
}
```

**Key points:**
- Use absolute paths for reliability
- `command` must be in PATH or absolute path
- Server runs as child process
- Lifecycle tied to Claude Code session

### HTTP Transport

```json
{
  "mcpServers": {
    "remote-api": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-Client-Version": "1.0.0"
      }
    }
  }
}
```

**Recommended for:**
- Cloud-based services
- Remote servers
- Production deployments

### SSE Transport (Deprecated)

```json
{
  "mcpServers": {
    "legacy-server": {
      "url": "https://old.example.com/sse"
    }
  }
}
```

**Avoid for new servers.** Use HTTP instead.

### Multiple Servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "remote-api": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

## Environment Variables

### Variable Expansion

**System variable expansion:**
```json
{
  "env": {
    "API_KEY": "${API_KEY}",
    "DATABASE_URL": "${DATABASE_URL}"
  }
}
```

Claude Code expands `${VAR}` from system environment.

**Fallback values:**
```json
{
  "env": {
    "LOG_LEVEL": "${LOG_LEVEL:-info}",
    "TIMEOUT": "${TIMEOUT:-30000}",
    "DEBUG": "${DEBUG:-false}"
  }
}
```

Syntax: `${VAR:-default}` - uses `default` if `VAR` not set.

**Expansion works in all fields:**
Variable expansion is supported in: `command`, `args`, `env`, `url`, and `headers` fields.

```json
{
  "mcpServers": {
    "dynamic-server": {
      "command": "${SERVER_COMMAND:-node}",
      "args": ["${SERVER_PATH}/server.js", "${PORT:-3000}"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    },
    "dynamic-http": {
      "url": "${API_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${TOKEN}"
      }
    }
  }
}
```

This enables team-shared `.mcp.json` files with machine-specific values.

### Security

**Never commit secrets:**
```json
{
  "env": {
    "API_KEY": "${API_KEY}"  // Good: expands from system
  }
}
```

**Bad practice:**
```json
{
  "env": {
    "API_KEY": "sk-actual-secret"  // Bad: hardcoded
  }
}
```

**For team configs:**
- Use variable expansion: `${VAR}`
- Document required variables in README
- Provide example values (non-functional)

## Authentication

### OAuth 2.0 Workflow

For OAuth-protected MCP servers:

1. Configure server (CLI or .mcp.json)
2. Start Claude Code
3. In conversation, type: `/mcp`
4. Follow OAuth prompts
5. Tokens stored securely, auto-refresh

**No manual token management needed.**

### Bearer Tokens (HTTP)

For static bearer tokens:

```json
{
  "url": "https://api.example.com/mcp",
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

Store token in system environment variable.

## In-Conversation Usage

### Reference MCP Resources

**Syntax:**
```
@server:protocol://resource/path
```

**Examples:**
```
@github:api://repo/anthropics/claude-code/issues
@filesystem:file:///workspace/src/main.ts
@database:db://production/users/12345
```

Use in conversation to reference server-provided resources.

### Invoke MCP Prompts

MCP prompts become slash commands:

**Syntax:**
```
/mcp__servername__promptname [arguments]
```

**Examples:**
```
/mcp__github__analyze-pr 123
/mcp__database__query-schema users
```

Tab completion available for MCP slash commands.

## Output Limits

**Token limits:**
- Warning threshold: 10,000 tokens
- Maximum output: 25,000 tokens
- Large outputs truncated

**Configure behavior:**
```bash
MAX_MCP_OUTPUT_TOKENS=50000 claude  # Increase output limit to 50K tokens
MCP_TIMEOUT=10000 claude            # Set 10 second server startup timeout
```

Set environment variables before launching Claude Code.

## Verification

### Check Configuration

**List all servers:**
```bash
claude mcp list
```

**Get specific server:**
```bash
claude mcp get server-name
```

**In-conversation status:**
```
/mcp
```

### Test Connection

1. Restart Claude Code (config loaded on startup)
2. Type `/mcp` to check connection status
3. Verify tools appear in available tools
4. Test tool invocation

### Diagnose Issues

**Server not connecting:**
```bash
# Verify command exists
which node
which python

# Test server standalone
node /path/to/server.js

# Test with Inspector
npx @modelcontextprotocol/inspector node /path/to/server.js

# Check server details
claude mcp get server-name
```

**Tools not appearing:**
```bash
# Verify server connected
claude mcp list

# Check in conversation
/mcp

# Test with Inspector
npx @modelcontextprotocol/inspector node /path/to/server.js
```

## Enterprise Configuration

**Managed MCP servers** (admin-controlled, system-wide):

**macOS:**
```
/Library/Application Support/ClaudeCode/managed-mcp.json
```

**Windows:**
```
C:\ProgramData\ClaudeCode\managed-mcp.json
```

**Linux:**
```
/etc/claude-code/managed-mcp.json
```

**Priority:** Managed configs cannot be overridden by user/project/local.

**Structure:** Same as `.mcp.json`

## Popular Official Servers

**Installation pattern:**
```bash
claude mcp add --transport stdio [name] -- npx -y [package]
```

**Available servers:**

**Development:**
- `@modelcontextprotocol/server-filesystem` - File operations
- `@modelcontextprotocol/server-github` - GitHub API (requires GITHUB_TOKEN)
- `@modelcontextprotocol/server-gitlab` - GitLab API
- `@modelcontextprotocol/server-git` - Git operations

**Data:**
- `@modelcontextprotocol/server-gdrive` - Google Drive
- `@modelcontextprotocol/server-postgres` - PostgreSQL
- `@modelcontextprotocol/server-sqlite` - SQLite

**Communication:**
- `@modelcontextprotocol/server-slack` - Slack (requires SLACK_BOT_TOKEN)
- `@modelcontextprotocol/server-gmail` - Gmail

**See:** https://github.com/modelcontextprotocol/servers for full list.

## Remote MCP Servers

40+ third-party remote servers available via HTTP transport.

**Categories:**

**Project Management:**
- Asana, Atlassian (Jira/Confluence), ClickUp, Linear, Notion, Monday

**Payments:**
- PayPal, Plaid, Square, Stripe

**Design/Media:**
- Figma, Canva, Cloudinary, invideo

**Infrastructure:**
- Cloudflare, Netlify, Stytch, Vercel

**Data:**
- Airtable, HubSpot, Daloopa

**Automation:**
- Workato, Zapier

**Development:**
- Hugging Face, Jam, Intercom, Box, Fireflies

**Connection:**
1. Review server documentation (each server has specific setup)
2. Obtain authentication credentials
3. Add via CLI with http transport
4. Authenticate with `/mcp` command

**Security warnings:**
- **Use at your own risk:** Anthropic has not verified the correctness or security of third-party MCP servers
- **Trust only known sources:** Only connect to servers from trusted providers
- **Prompt injection risk:** MCP servers that fetch untrusted content (web pages, user input, external APIs) can expose you to prompt injection attacks where malicious content manipulates Claude's behavior
- **Review before connecting:** Check server documentation, security practices, and terms of service
- **Credential access:** Servers with authentication can access and use your credentials for their services

## Troubleshooting

### Server not appearing

```bash
# Validate .mcp.json syntax
cat .mcp.json | python -m json.tool

# Check server configured
claude mcp list

# Restart Claude Code
```

### Environment variables not working

```bash
# Verify system variable set
echo $API_KEY
echo %API_KEY%  # Windows

# Check expansion syntax
# Correct: ${VAR} or ${VAR:-default}
# Wrong: $VAR or {VAR}
```

### Path issues (Windows)

**Use forward slashes:**
```json
{
  "args": ["C:/Users/Name/server/build/index.js"]
}
```

**Or escape backslashes:**
```json
{
  "args": ["C:\\Users\\Name\\server\\build\\index.js"]
}
```

### Server crashes immediately

```bash
# Run server directly to see errors
node /path/to/server.js

# Check dependencies installed
cd /path/to/server && npm install

# Verify environment variables set
echo $REQUIRED_VAR
```

## Tool Usage Patterns

**When configuring MCP connection:**

1. **Primary method - CLI:**
   ```bash
   claude mcp add --transport stdio name -- node /path/to/server.js
   ```

2. **Direct file manipulation when needed:**
   - Use Read to load `.mcp.json`
   - Use Edit to modify configuration
   - User must restart Claude Code (cannot automate)

3. **Verification:**
   ```bash
   claude mcp list
   claude mcp get name
   ```

4. **In-conversation:**
   ```
   /mcp
   ```

**When troubleshooting:**

1. Use Bash with verification commands
2. Use Read to examine `.mcp.json`
3. Use Bash with Inspector for server testing
4. Direct user to restart Claude Code

## Reference

**Official documentation:**
- https://code.claude.com/docs/en/mcp
- https://docs.claude.com/en/docs/agents-and-tools/mcp-connector
- https://docs.claude.com/en/docs/agents-and-tools/remote-mcp-servers

**MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector [command] [args]
```

Opens browser interface for testing MCP servers before connecting to Claude Code.
