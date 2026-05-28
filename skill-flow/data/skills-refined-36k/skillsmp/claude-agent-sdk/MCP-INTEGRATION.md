# MCP Integration Reference

Complete guide for integrating Model Context Protocol (MCP) servers with Claude Agent SDK.

## Overview

MCP (Model Context Protocol) allows extending Claude Agent SDK with custom tools. This enables:

- **Custom tool integration** - Add domain-specific tools
- **External service access** - Database, API, cloud services
- **Reusable tool packages** - Share tools across agents

## MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Agent SDK                      │
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ Built-in    │    │ MCP Server  │    │ MCP Server  │  │
│  │ Tools       │    │ (stdio)     │    │ (HTTP)      │  │
│  │             │    │             │    │             │  │
│  │ - Read      │    │ - Database  │    │ - Cloud API │  │
│  │ - Write     │    │ - Git       │    │ - External  │  │
│  │ - Bash      │    │ - Custom    │    │ - Service   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Connecting MCP Servers

### Python

```python
from claude_sdk import ClaudeSDKClient
from claude_sdk.mcp import MCPStdioServer, MCPHTTPServer

# Stdio-based MCP server (local process)
postgres_mcp = MCPStdioServer(
    name="postgres",
    command="uvx",
    args=["mcp-server-postgres"],
    env={"DATABASE_URL": "postgresql://user:pass@localhost/db"}
)

# HTTP-based MCP server (remote)
cloud_mcp = MCPHTTPServer(
    name="cloud-tools",
    url="https://mcp.example.com",
    api_key="your-api-key"
)

# Use with client
client = ClaudeSDKClient(
    mcp_servers=[postgres_mcp, cloud_mcp]
)
```

### TypeScript

```typescript
import { ClaudeSDKClient, MCPStdioServer, MCPHTTPServer } from '@anthropic/claude-sdk';

// Stdio-based MCP server
const postgresMcp = new MCPStdioServer({
  name: "postgres",
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-postgres"],
  env: { DATABASE_URL: "postgresql://user:pass@localhost/db" }
});

// HTTP-based MCP server
const cloudMcp = new MCPHTTPServer({
  name: "cloud-tools",
  url: "https://mcp.example.com",
  apiKey: "your-api-key"
});

// Use with client
const client = new ClaudeSDKClient({
  mcpServers: [postgresMcp, cloudMcp]
});
```

---

## MCPStdioServer

For MCP servers running as local processes.

### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Server identifier |
| `command` | string | Command to run (e.g., "uvx", "npx") |
| `args` | string[] | Command arguments |
| `env` | dict | Environment variables |
| `cwd` | string | Working directory |
| `timeout` | int | Connection timeout (seconds) |

### Common MCP Servers

```python
# PostgreSQL
postgres = MCPStdioServer(
    name="postgres",
    command="uvx",
    args=["mcp-server-postgres"],
    env={"DATABASE_URL": os.getenv("DATABASE_URL")}
)

# SQLite
sqlite = MCPStdioServer(
    name="sqlite",
    command="uvx",
    args=["mcp-server-sqlite", "--db-path", "./data.db"]
)

# Git
git = MCPStdioServer(
    name="git",
    command="uvx",
    args=["mcp-server-git"],
    cwd="/path/to/repo"
)

# Filesystem (extended)
filesystem = MCPStdioServer(
    name="filesystem",
    command="uvx",
    args=["mcp-server-filesystem", "/allowed/path"]
)

# GitHub
github = MCPStdioServer(
    name="github",
    command="uvx",
    args=["mcp-server-github"],
    env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
)

# Slack
slack = MCPStdioServer(
    name="slack",
    command="uvx",
    args=["mcp-server-slack"],
    env={"SLACK_TOKEN": os.getenv("SLACK_TOKEN")}
)

# Puppeteer (browser automation)
puppeteer = MCPStdioServer(
    name="browser",
    command="npx",
    args=["-y", "@anthropic/mcp-server-puppeteer"]
)
```

---

## MCPHTTPServer

For MCP servers accessible via HTTP.

### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Server identifier |
| `url` | string | Server URL |
| `api_key` | string | Authentication key |
| `headers` | dict | Additional headers |
| `timeout` | int | Request timeout |

### Example

```python
from claude_sdk.mcp import MCPHTTPServer

# Remote MCP server
remote_mcp = MCPHTTPServer(
    name="enterprise-tools",
    url="https://mcp.company.com",
    api_key=os.getenv("MCP_API_KEY"),
    headers={"X-Tenant-ID": "tenant-123"}
)
```

---

## Creating Custom MCP Servers

### Python MCP Server

```python
# my_mcp_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("my-custom-tools")

@app.tool()
async def calculate_revenue(
    start_date: str,
    end_date: str
) -> str:
    """Calculate total revenue between dates."""
    # Your implementation
    revenue = await fetch_revenue(start_date, end_date)
    return f"Total revenue: ${revenue:,.2f}"

@app.tool()
async def send_notification(
    channel: str,
    message: str
) -> str:
    """Send notification to specified channel."""
    # Your implementation
    await notify(channel, message)
    return f"Notification sent to {channel}"

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

### TypeScript MCP Server

```typescript
// my-mcp-server.ts
import { Server, Tool } from "@modelcontextprotocol/sdk";

const server = new Server("my-custom-tools");

server.addTool({
  name: "calculate_revenue",
  description: "Calculate total revenue between dates",
  inputSchema: {
    type: "object",
    properties: {
      start_date: { type: "string" },
      end_date: { type: "string" }
    },
    required: ["start_date", "end_date"]
  },
  handler: async ({ start_date, end_date }) => {
    const revenue = await fetchRevenue(start_date, end_date);
    return { content: [{ type: "text", text: `Total revenue: $${revenue}` }] };
  }
});

server.run();
```

### Using Custom Server

```python
from claude_sdk.mcp import MCPStdioServer

custom_mcp = MCPStdioServer(
    name="my-tools",
    command="python",
    args=["my_mcp_server.py"]
)

client = ClaudeSDKClient(mcp_servers=[custom_mcp])

result = await client.query(
    "Calculate revenue for Q4 2024 and send a summary to #sales"
)
# Agent uses calculate_revenue and send_notification tools
```

---

## MCP Server Lifecycle

### Automatic Management

```python
# Servers start automatically when client is used
client = ClaudeSDKClient(mcp_servers=[postgres_mcp])

async with client.create_session() as session:
    # MCP servers are connected
    await session.query("Query the database")
    # MCP servers stay connected

# Servers are stopped when client is done
```

### Manual Management

```python
# Manual connection control
await postgres_mcp.connect()

# Check status
if postgres_mcp.is_connected:
    tools = await postgres_mcp.list_tools()
    print(f"Available tools: {[t.name for t in tools]}")

# Execute tool directly
result = await postgres_mcp.execute_tool(
    "query",
    {"sql": "SELECT * FROM users LIMIT 10"}
)

# Disconnect
await postgres_mcp.disconnect()
```

---

## Tool Discovery

### List Available Tools

```python
client = ClaudeSDKClient(mcp_servers=[postgres_mcp, github_mcp])

# Get all tools from all MCP servers
tools = await client.list_mcp_tools()

for tool in tools:
    print(f"Server: {tool.server}")
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Schema: {tool.input_schema}")
    print("---")
```

### Filter Tools by Server

```python
# Get tools from specific server
postgres_tools = await client.list_mcp_tools(server="postgres")
```

---

## Error Handling

```python
from claude_sdk.mcp import (
    MCPError,
    MCPConnectionError,
    MCPToolError,
    MCPTimeoutError
)

try:
    client = ClaudeSDKClient(mcp_servers=[postgres_mcp])
    await client.connect()
except MCPConnectionError as e:
    print(f"Failed to connect to MCP server: {e.server_name}")
    print(f"Command: {e.command}")
    print(f"Error: {e.message}")
except MCPTimeoutError as e:
    print(f"MCP server timed out: {e.server_name}")

try:
    result = await session.query("Query the database")
except MCPToolError as e:
    print(f"MCP tool failed: {e.tool_name}")
    print(f"Server: {e.server_name}")
    print(f"Error: {e.message}")
```

---

## MCP + Hooks Integration

### Audit MCP Tool Calls

```python
from claude_sdk import Hook, HookResult

class MCPAuditHook(Hook):
    """Audit all MCP tool calls."""

    async def on_tool_call(self, context):
        if context.tool_source == "mcp":
            logger.info(
                f"MCP Tool: {context.mcp_server}/{context.tool_name}",
                extra={
                    "server": context.mcp_server,
                    "tool": context.tool_name,
                    "args": context.args
                }
            )
        return HookResult.ALLOW
```

### Restrict MCP Access

```python
class MCPSecurityHook(Hook):
    """Restrict MCP tool access by server."""

    def __init__(self, allowed_servers: list):
        self.allowed_servers = set(allowed_servers)

    async def on_tool_call(self, context):
        if context.tool_source == "mcp":
            if context.mcp_server not in self.allowed_servers:
                return HookResult.reject(
                    f"MCP server '{context.mcp_server}' is not allowed"
                )
        return HookResult.ALLOW
```

---

## Configuration

### Environment Variables

```bash
# MCP server paths
MCP_POSTGRES_URL=postgresql://user:pass@localhost/db
MCP_GITHUB_TOKEN=ghp_xxxx
MCP_SLACK_TOKEN=xoxb-xxxx

# MCP settings
MCP_CONNECT_TIMEOUT=30
MCP_TOOL_TIMEOUT=120
```

### Configuration File

```yaml
# claude-sdk.yaml
mcp_servers:
  - name: postgres
    type: stdio
    command: uvx
    args: [mcp-server-postgres]
    env:
      DATABASE_URL: ${MCP_POSTGRES_URL}

  - name: github
    type: stdio
    command: uvx
    args: [mcp-server-github]
    env:
      GITHUB_TOKEN: ${MCP_GITHUB_TOKEN}

  - name: enterprise
    type: http
    url: https://mcp.company.com
    api_key: ${MCP_ENTERPRISE_KEY}
```

---

## Best Practices

### 1. Use Environment Variables for Secrets

```python
# Good
postgres_mcp = MCPStdioServer(
    name="postgres",
    command="uvx",
    args=["mcp-server-postgres"],
    env={"DATABASE_URL": os.getenv("DATABASE_URL")}
)

# Avoid
postgres_mcp = MCPStdioServer(
    name="postgres",
    command="uvx",
    args=["mcp-server-postgres"],
    env={"DATABASE_URL": "postgresql://user:password@localhost/db"}  # Hardcoded!
)
```

### 2. Handle Connection Failures

```python
async def create_client_with_fallback():
    servers = []

    # Try to connect to each server
    for server_config in MCP_SERVERS:
        try:
            server = MCPStdioServer(**server_config)
            await server.connect()
            servers.append(server)
        except MCPConnectionError as e:
            logger.warning(f"Failed to connect to {server_config['name']}: {e}")

    return ClaudeSDKClient(mcp_servers=servers)
```

### 3. Use Specific Tools

```python
# Good - specify which MCP tools to use
result = await query(
    prompt="Get user statistics",
    mcp_tools=["postgres:query", "postgres:describe_table"]
)

# Avoid - allow all tools
result = await query(
    prompt="Get user statistics",
    mcp_tools="all"  # May use unexpected tools
)
```

### 4. Monitor MCP Server Health

```python
async def health_check(client: ClaudeSDKClient):
    for server in client.mcp_servers:
        try:
            tools = await server.list_tools()
            print(f"✓ {server.name}: {len(tools)} tools available")
        except MCPError as e:
            print(f"✗ {server.name}: {e}")
```
