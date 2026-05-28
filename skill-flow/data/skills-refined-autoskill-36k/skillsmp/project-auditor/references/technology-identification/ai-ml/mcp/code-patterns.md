# MCP Code Patterns

Code patterns for detecting Model Context Protocol implementation.

## Confidence

**Detection Confidence**: 85%

## Server Implementation Patterns

### JavaScript/TypeScript

| Pattern | Description |
|---------|-------------|
| `new Server(` | Server instantiation |
| `server.setRequestHandler(` | Request handler registration |
| `ListToolsRequestSchema` | Tool listing schema |
| `CallToolRequestSchema` | Tool calling schema |
| `ListResourcesRequestSchema` | Resource listing schema |
| `ReadResourceRequestSchema` | Resource reading schema |
| `ListPromptsRequestSchema` | Prompt listing schema |
| `GetPromptRequestSchema` | Prompt retrieval schema |
| `StdioServerTransport` | stdio transport |
| `SSEServerTransport` | SSE transport |
| `McpServer` | Server class reference |
| `server.tool(` | Tool definition |
| `server.resource(` | Resource definition |
| `server.prompt(` | Prompt definition |

### Python

| Pattern | Description |
|---------|-------------|
| `@server.list_tools(` | Tool listing decorator |
| `@server.call_tool(` | Tool calling decorator |
| `@server.list_resources(` | Resource listing decorator |
| `@server.read_resource(` | Resource reading decorator |
| `@server.list_prompts(` | Prompt listing decorator |
| `@server.get_prompt(` | Prompt retrieval decorator |
| `Server(name=` | Server instantiation |
| `stdio_server(` | stdio transport |
| `mcp.server.Server` | Server class reference |

## Client Implementation Patterns

### JavaScript/TypeScript

| Pattern | Description |
|---------|-------------|
| `new Client(` | Client instantiation |
| `client.connect(` | Connection establishment |
| `client.listTools(` | List available tools |
| `client.callTool(` | Execute a tool |
| `client.listResources(` | List available resources |
| `client.readResource(` | Read a resource |

### Python

| Pattern | Description |
|---------|-------------|
| `Client(` | Client instantiation |
| `client.list_tools(` | List available tools |
| `client.call_tool(` | Execute a tool |
| `client.list_resources(` | List available resources |
| `client.read_resource(` | Read a resource |

## Tool Definition Patterns

Common patterns in tool definitions:

| Pattern | Description |
|---------|-------------|
| `inputSchema` | JSON Schema for tool inputs |
| `parameters.*type.*object` | Parameter type definition |
| `tool.*name.*description` | Tool metadata |

## Example Server (JavaScript)

```javascript
const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "my_tool",
    description: "Does something useful",
    inputSchema: {
      type: "object",
      properties: {
        input: { type: "string" }
      }
    }
  }]
}));
```

## Example Server (Python)

```python
server = Server(name="my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="Does something useful",
            inputSchema={"type": "object", "properties": {"input": {"type": "string"}}}
        )
    ]
```
