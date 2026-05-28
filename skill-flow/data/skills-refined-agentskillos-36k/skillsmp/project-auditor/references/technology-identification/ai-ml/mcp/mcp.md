# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables AI applications to connect to external data sources and tools. It provides a standardized way for AI assistants to access context from files, databases, APIs, and other services.

## Technology Details

| Attribute | Value |
|-----------|-------|
| Category | AI/ML - Protocols |
| Subcategory | AI Integration |
| First Released | 2024 |
| Maintained By | Anthropic |
| License | MIT |
| Website | https://modelcontextprotocol.io |

## Detection Patterns

### Package Patterns

#### NPM (JavaScript/TypeScript)
```
@modelcontextprotocol/sdk
@modelcontextprotocol/server
@modelcontextprotocol/client
@modelcontextprotocol/server-*
mcp-server-*
```

#### PyPI (Python)
```
mcp
modelcontextprotocol
mcp-server
mcp-client
```

### Import Patterns

#### JavaScript/TypeScript
```javascript
import { Server } from "@modelcontextprotocol/sdk/server"
import { Client } from "@modelcontextprotocol/sdk/client"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio"
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse"
from "@modelcontextprotocol/sdk"
from "@modelcontextprotocol/server"
```

#### Python
```python
from mcp import Server
from mcp import Client
from mcp.server import Server
from mcp.client import Client
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
import mcp
import mcp.server
import mcp.client
```

### Configuration Patterns

#### Claude Desktop Config (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "*": {
      "command": "*",
      "args": ["*"]
    }
  }
}
```

#### MCP Server Manifest
```json
{
  "name": "*",
  "version": "*",
  "description": "*",
  "protocol_version": "2024-11-05"
}
```

### Code Patterns

#### Server Implementation
```javascript
// MCP Server setup
server.setRequestHandler(ListToolsRequestSchema, async () => {
server.setRequestHandler(CallToolRequestSchema, async (request) => {
new Server({ name: "*", version: "*" })
McpServer
StdioServerTransport
SSEServerTransport
```

#### Python Server
```python
@server.list_tools()
@server.call_tool()
@server.list_resources()
@server.read_resource()
Server(name="*")
stdio_server()
```

### Environment Variables
```
MCP_SERVER_*
MCP_DEBUG
MCP_LOG_LEVEL
```

### File Patterns
```
mcp.json
mcp-config.json
claude_desktop_config.json
.mcp/
mcp-server.js
mcp-server.py
mcp_server.py
```

## Security Considerations

### Risk Level: MEDIUM-HIGH

MCP servers can:
- Access local filesystem
- Execute system commands
- Connect to databases and APIs
- Expose sensitive data to AI models

### Security Audit Points

1. **Tool Permissions**: Review what tools/capabilities each MCP server exposes
2. **Data Access**: Check what resources (files, databases) servers can access
3. **Network Access**: Identify external API connections
4. **Command Execution**: Look for servers that execute shell commands
5. **Authentication**: Verify how servers authenticate to external services
6. **Input Validation**: Check for command injection vulnerabilities

### Common Vulnerabilities

- **Path Traversal**: MCP file servers without path validation
- **Command Injection**: Servers passing unsanitized input to shell
- **Credential Exposure**: API keys in server configurations
- **Overprivileged Access**: Servers with broader access than needed
- **Unvalidated Tool Arguments**: Direct use of AI-provided parameters

## Organizational Impact

### Governance Concerns

1. **Shadow AI**: MCP servers may be installed without IT approval
2. **Data Leakage**: Sensitive data exposed to AI models
3. **Compliance**: AI access to regulated data (PII, PHI, financial)
4. **Audit Trail**: Limited logging of AI-data interactions
5. **Access Control**: MCP may bypass normal access controls

### Detection Priority

Organizations should scan for MCP to:
- Inventory AI integrations
- Assess data exposure risk
- Ensure compliance with AI policies
- Identify unauthorized AI tool usage

## Related Technologies

- Claude Desktop
- Claude Code (CLI)
- Anthropic Claude API
- LangChain MCP integration
- OpenAI function calling (alternative approach)
- Tool Use / Function Calling patterns
