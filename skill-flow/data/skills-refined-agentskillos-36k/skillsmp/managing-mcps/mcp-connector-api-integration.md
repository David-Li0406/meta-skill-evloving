# MCP Connector API Integration

Complete workflow for using MCP servers via the Anthropic Messages API (not Claude Code CLI).

## When to Use This Workflow

Use MCP Connector API when:
- Building applications with Claude + MCP tools
- Integrating remote MCP servers programmatically
- API-based workflows requiring MCP capabilities
- No Claude Code CLI available/desired

**Do NOT use for:** Claude Code CLI usage (use Workflows 5 and 7 in SKILL.md instead)

## Overview

The MCP Connector enables connecting to remote MCP servers via Messages API using two components:
1. **mcp_servers** array: Server connection definitions (URL, authentication)
2. **tools** array with **MCPToolset**: Tool configuration (enable/disable, defer loading)

## Required Beta Header

```python
betas=["mcp-client-2025-11-20"]
```

**Current Version**: `mcp-client-2025-11-20`
**Deprecated Version**: `mcp-client-2025-04-04` (see deprecation-notes.md for migration)

## Basic Integration Pattern

### Step 1: Define MCP Server

```python
mcp_servers=[
    {
        "type": "url",
        "url": "https://example-server.modelcontextprotocol.io/sse",
        "name": "example-mcp",
        "authorization_token": "YOUR_TOKEN"  # Optional
    }
]
```

**Fields:**
- `type`: Always "url" (only option currently)
- `url`: MCP server endpoint (must be https://)
- `name`: Unique identifier (referenced by MCPToolset)
- `authorization_token`: OAuth token if required (optional)

### Step 2: Configure MCPToolset

```python
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "example-mcp",
        "default_config": {
            "enabled": true,
            "defer_loading": false
        },
        "configs": {
            "specific_tool": {
                "enabled": true,
                "defer_loading": true
            }
        }
    }
]
```

**Fields:**
- `type`: Always "mcp_toolset"
- `mcp_server_name`: Must match server name from mcp_servers
- `default_config`: Applied to all tools (optional)
- `configs`: Per-tool overrides (optional)

**Tool Configuration Options:**
- `enabled`: Whether tool is available (default: true)
- `defer_loading`: Defer description loading for Tool Search (default: false)

### Step 3: Make API Request

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What tools do you have available?"
        }
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://example-server.modelcontextprotocol.io/sse",
            "name": "example-mcp",
            "authorization_token": "YOUR_TOKEN"
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "example-mcp"
        }
    ],
    betas=["mcp-client-2025-11-20"]
)
```

## Tool Configuration Patterns

### Pattern 1: Enable All Tools (Default)

Simplest pattern - all tools enabled:

```python
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "calendar-mcp"
    }
]
```

### Pattern 2: Allowlist (Selective Enable)

Enable only specific tools:

```python
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "calendar-mcp",
        "default_config": {
            "enabled": false
        },
        "configs": {
            "search_events": {"enabled": true},
            "create_event": {"enabled": true}
        }
    }
]
```

### Pattern 3: Denylist (Selective Disable)

Disable only specific tools:

```python
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "calendar-mcp",
        "configs": {
            "delete_all_events": {"enabled": false},
            "share_calendar_publicly": {"enabled": false}
        }
    }
]
```

### Pattern 4: Mixed (Allowlist + Per-Tool Config)

Combine allowlisting with custom configuration:

```python
tools=[
    {
        "type": "mcp_toolset",
        "mcp_server_name": "calendar-mcp",
        "default_config": {
            "enabled": false,
            "defer_loading": true
        },
        "configs": {
            "search_events": {
                "enabled": true,
                "defer_loading": false
            },
            "list_events": {
                "enabled": true
            }
        }
    }
]
```

Result:
- `search_events`: enabled, defer_loading: false
- `list_events`: enabled, defer_loading: true (inherited)
- All other tools: disabled

## Multiple MCP Servers

Connect to multiple servers in single request:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[...],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://calendar-mcp.example.com/sse",
            "name": "calendar",
            "authorization_token": "TOKEN1"
        },
        {
            "type": "url",
            "url": "https://email-mcp.example.com/sse",
            "name": "email",
            "authorization_token": "TOKEN2"
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "calendar"
        },
        {
            "type": "mcp_toolset",
            "mcp_server_name": "email",
            "default_config": {
                "defer_loading": true
            }
        }
    ],
    betas=["mcp-client-2025-11-20"]
)
```

## Response Handling

MCP tool calls produce special content block types:

### MCP Tool Use Block

```python
{
    "type": "mcp_tool_use",
    "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
    "name": "search_events",
    "server_name": "calendar",
    "input": {
        "query": "weekly sync",
        "date_range": "this week"
    }
}
```

### MCP Tool Result Block

```python
{
    "type": "mcp_tool_result",
    "tool_use_id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
    "is_error": false,
    "content": [
        {
            "type": "text",
            "text": "Found 3 events..."
        }
    ]
}
```

## Validation Rules

The API enforces these validation rules:
- **Server must exist**: mcp_server_name in MCPToolset must match a server in mcp_servers
- **Server must be used**: Every MCP server must be referenced by exactly one MCPToolset
- **Unique toolset per server**: Each server can only be referenced by one MCPToolset
- **Unknown tool names**: If tool name in configs doesn't exist, backend logs warning but no error

## OAuth Authentication

### Obtaining Access Token for Testing

Use MCP Inspector to obtain OAuth token:

```bash
npx @modelcontextprotocol/inspector
```

1. Select "HTTP" or "SSE" transport
2. Enter server URL
3. Click "Open Auth Settings" → "Quick OAuth Flow"
4. Authorize in browser
5. Copy `access_token` value
6. Use in `authorization_token` field

### Using Access Token

```python
mcp_servers=[
    {
        "type": "url",
        "url": "https://example-server.modelcontextprotocol.io/sse",
        "name": "authenticated-server",
        "authorization_token": "YOUR_ACCESS_TOKEN_HERE"
    }
]
```

**Token Management:**
- API consumers must handle OAuth flow
- Obtain access token before API call
- Refresh tokens as needed
- See MCP specification for OAuth flow details

## Complete Example

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Example: Calendar integration with selective tools
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What events do I have this week?"
        }
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://calendar-mcp.example.com/sse",
            "name": "calendar",
            "authorization_token": "YOUR_CALENDAR_TOKEN"
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "calendar",
            "default_config": {
                "enabled": false
            },
            "configs": {
                "search_events": {"enabled": true},
                "list_events": {"enabled": true}
            }
        }
    ],
    betas=["mcp-client-2025-11-20"]
)

# Process response
for block in response.content:
    if hasattr(block, 'type'):
        if block.type == 'mcp_tool_use':
            print(f"Using MCP tool: {block.name} from {block.server_name}")
        elif block.type == 'mcp_tool_result':
            print(f"MCP tool result: {block.content}")
        elif block.type == 'text':
            print(f"Response: {block.text}")
```

## Use Cases

**API Automation**: Connect to REST APIs via OpenAPI schema MCP
**Database Queries**: Query databases via database MCPs
**Third-party Integration**: Access Jira, Salesforce, Notion via MCP
**Internal Tools**: Connect to company-internal MCP servers
**Multi-service Workflows**: Coordinate across multiple MCP services in single API call

## Migration from Deprecated Version

If using `mcp-client-2025-04-04`, see deprecation-notes.md for migration guide. Key changes:
- Tool configuration moved from mcp_servers to separate tools array
- `tool_configuration` replaced with `default_config` + `configs`
- `allowed_tools` becomes allowlist pattern

## Troubleshooting

**Server not connecting:**
- Verify URL is accessible via HTTPS
- Check authorization_token is valid
- Ensure server supports HTTP or SSE transport
- Verify server is running and responding

**Tools not appearing:**
- Check mcp_server_name matches server name exactly
- Verify MCPToolset references the server
- Ensure tools are enabled in configs
- Check beta header is correct

**Authentication errors:**
- Verify authorization_token is current
- Check token has required scopes
- Test token with MCP Inspector first
- Refer to server's OAuth documentation

## Reference

**Official Documentation:**
- https://docs.claude.com/en/docs/agents-and-tools/mcp-connector

**MCP Specification:**
- https://modelcontextprotocol.io/specification/2025-06-18
- https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
