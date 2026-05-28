---
name: mcp-server-creator
description: Build production-ready Model Context Protocol (MCP) servers using the official MCP SDK. Scaffold, configure, secure, and deploy MCP servers with best practices for security, monitoring, and reliability. Use for creating robust MCP servers that integrate with Claude Code.
---

# Production MCP Server Builder

Build production-ready Model Context Protocol (MCP) servers using the official MCP SDK with security, monitoring, and and deployment best practices.

## Quick Start

### Install the Official MCP SDK
```bash
# Using pip
pip install mcp

# Using uv
uv add mcp
```

### Create New MCP Server
```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="My Production Server",
    json_response=True,
    host="127.0.0.1",
    port=8080
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    return f"Write a {style} greeting for someone named {name}."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

### Run the Server
```bash
# Run with uv
uv run --with mcp server.py

# Or with pip
python server.py
```

### Connect with MCP Inspector
```bash
npx -y @modelcontextprotocol/inspector
```

## Architecture Overview

Production MCP servers follow these key principles:

1. **Transport Layer**: Use `streamable-http` for production (vs `stdio` for development)
2. **Authentication**: Implement OAuth or API key validation
3. **Security**: Apply input validation, rate limiting, and access controls
4. **Monitoring**: Include health checks, metrics, and logging
5. **Reliability**: Implement graceful error handling and shutdown

## Core Concepts

The MCP SDK provides three core primitives:

1. **Tools**: Functions that can be called remotely
2. **Resources**: Named pieces of data that can be retrieved
3. **Prompts**: Templates for generating prompts for LLMs

## Development Workflow

1. **Install**: Install the official `mcp` package
2. **Create**: Initialize a FastMCP server instance
3. **Define**: Add tools, resources, and prompts using decorators
4. **Run**: Start the server with appropriate transport
5. **Test**: Verify functionality with MCP Inspector
6. **Deploy**: Push to production with monitoring

## Production Best Practices

### Security
- Use HTTPS in production
- Implement proper authentication
- Validate all inputs
- Sanitize all outputs
- Apply rate limiting

### Reliability
- Implement health checks (`/health` endpoint)
- Add graceful shutdown handling
- Include comprehensive error handling
- Use structured logging

### Monitoring
- Expose metrics endpoint
- Log key operations
- Monitor performance
- Set up alerts

## Tool Definition Patterns

### Basic Tool
```python
@mcp.tool()
def my_tool(param1: str, param2: int) -> dict:
    """Description of what this tool does."""
    # Tool implementation
    return {"result": "success"}
```

### Resource Definition
```python
@mcp.resource("my-resource://{identifier}")
def get_resource(identifier: str) -> str:
    """Define a retrievable resource."""
    return f"Resource content for {identifier}"
```

### Prompt Definition
```python
@mcp.prompt()
def my_prompt(context: str, style: str = "professional") -> str:
    """Define a prompt template."""
    return f"Write a {style} response about: {context}"
```

### Tool with Error Handling
```python
import logging
logger = logging.getLogger(__name__)

@mcp.tool()
def secure_tool(input_data: str) -> str:
    """Tool with proper error handling and validation."""
    try:
        # Validate input
        if len(input_data) > MAX_INPUT_LENGTH:
            raise ValueError("Input too long")

        # Process data
        result = process_input(input_data)
        return result

    except ValueError as e:
        # Log error
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {e}")
        raise RuntimeError("An error occurred processing your request")
```

## Server Configuration

### Transport Options
- `stdio`: Standard input/output, typically for Claude integration
- `streamable-http`: HTTP-based transport, recommended for production
- `sse`: Server-sent events (alternative for streaming)

### Running with Different Transports
```python
# For production
mcp.run(transport="streamable-http")

# For development
mcp.run(transport="stdio")
```

## Validation

Validate your server implementation:
- Use MCP Inspector to test connectivity
- Verify all tools respond correctly
- Check resource and prompt definitions
- Test error handling paths

## Deployment

### Environment Variables
```bash
# For production configuration
MCP_SERVER_NAME=my-server
MCP_SERVER_PORT=8000
```

## Monitoring and Health Checks

### Health Endpoint
Implement a health check endpoint in your application:
```python
from starlette.responses import JSONResponse
from starlette.requests import Request
from datetime import datetime

# Add custom endpoints to your FastMCP server
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "my-mcp-server",
        "version": "1.0.0"
    })

# You can also add other custom endpoints
```

### Custom Routes
The `custom_route` decorator allows you to add additional HTTP endpoints to your MCP server beyond the standard MCP protocol endpoints. This is useful for:
- Health checks (`/health`, `/status`)
- Metrics (`/metrics`, `/stats`)

The handler function must accept a Starlette Request parameter and return a Response.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server won't start | Check port availability and dependencies |
| Tools not appearing | Verify decorators are correctly applied |
| Connection issues | Ensure transport and firewall settings are correct |
| Performance problems | Profile slow tools and optimize |

## References

For detailed information on specific topics, see:
- [resources/tools-usage.md](./resources/tools-usage.md) - Tools usage guide
- [resources/prompts-usage.md](./resources/prompts-usage.md) - Prompts usage guide
- [resources/resources-usage.md](./resources/resources-usage.md) - Resources usage guide
- [resources/fastmcp-arguments.md](./resources/fastmcp-arguments.md) - FastMCP constructor arguments documentation
- [references/testing-guide.md](./references/testing-guide.md) - Testing guide for MCP servers
- [references/mcp-architecture.md](./references/mcp-architecture.md) - Architecture patterns
- [references/monitoring-guide.md](./references/monitoring-guide.md) - Monitoring and observability
- [references/security-best-practices.md](./references/security-best-practices.md) - Security guidelines
- [references/tool-definition-patterns.md](./references/tool-definition-patterns.md) - Tool implementation patterns
