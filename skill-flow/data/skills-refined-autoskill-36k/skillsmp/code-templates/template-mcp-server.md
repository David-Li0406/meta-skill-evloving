---
name: template-mcp-server
description: "Generate Kailash MCP server template. Use when requesting 'MCP server template', 'create MCP server', 'MCP server boilerplate', 'Model Context Protocol server', or 'MCP server example'."
---

# MCP Server Template

Production-ready MCP server template using Kailash SDK's built-in MCP implementation.

> **Skill Metadata**
> Category: `cross-cutting` (code-generation)
> Priority: `MEDIUM`
> SDK Version: `0.9.25+` (MCP v0.6.6+)
> Related Skills: [`mcp-integration-guide`](../../06-cheatsheets/mcp-integration-guide.md)
> Related Subagents: `mcp-specialist` (enterprise MCP), `pattern-expert`

## Basic MCP Server Template

```python
"""Basic MCP Server using Kailash SDK"""

from kailash.mcp_server import MCPServer

# Create server
server = MCPServer("my-server")

# Register tools
@server.tool()
async def process_data(data: str, operation: str = "uppercase") -> dict:
    """Process data with specified operation."""
    if operation == "uppercase":
        result = data.upper()
    elif operation == "lowercase":
        result = data.lower()
    else:
        result = data

    return {
        "result": result,
        "operation": operation,
        "input_length": len(data)
    }

@server.tool()
async def search_database(query: str, limit: int = 10) -> dict:
    """Search database and return results."""
    # Implement your database search logic
    results = [
        {"id": 1, "title": f"Result for: {query}"},
        {"id": 2, "title": f"Another result for: {query}"}
    ]

    return {
        "results": results[:limit],
        "count": len(results),
        "query": query
    }

# Run server
if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```

## Production MCP Server Template

```python
"""Production MCP Server with Authentication and Monitoring"""

from kailash.mcp_server import MCPServer, APIKeyAuth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup authentication
auth = APIKeyAuth({
    "admin_key": {
        "permissions": ["admin", "tools", "resources"],
        "rate_limit": 1000
    },
    "user_key": {
        "permissions": ["tools"],
        "rate_limit": 100
    }
})

# Create server with enterprise features
server = MCPServer(
    "production-server",
    auth_provider=auth,
    enable_metrics=True,
    enable_cache=True,
    cache_ttl=600
)

# Register tools with permissions
@server.tool(required_permission="tools", cache_key="process_data", cache_ttl=300)
async def process_data(data: str) -> dict:
    """Process data with caching."""
    logger.info(f"Processing data: {data[:50]}...")
    return {"result": data.upper(), "cached": True}

@server.tool(required_permission="admin")
async def admin_operation(action: str) -> dict:
    """Admin-only operation."""
    logger.info(f"Admin action: {action}")
    return {"action": action, "status": "completed"}

# Run server
if __name__ == "__main__":
    import asyncio
    logger.info("Starting production MCP server...")
    asyncio.run(server.run())
```

## Related Patterns

- **MCP integration**: [`mcp-integration-guide`](../../06-cheatsheets/mcp-integration-guide.md)
- **MCP in workflows**: Use with LLMAgentNode
- **Advanced MCP**: [`mcp-advanced-features`](../../05-mcp/mcp-advanced-features.md)

## When to Escalate

Use `mcp-specialist` subagent when:
- Enterprise MCP architecture
- Multi-transport configuration
- Advanced features (structured tools, resources, progress)
- Production deployment

## Documentation References

### Primary Sources
- **MCP Specialist**: [`.claude/agents/frameworks/mcp-specialist.md` (lines 39-59)](../../../../.claude/agents/frameworks/mcp-specialist.md#L39-L59)
- **MCP Integration**: [`sdk-users/2-core-concepts/cheatsheet/025-mcp-integration.md`](../../../../sdk-users/2-core-concepts/cheatsheet/025-mcp-integration.md)
- **MCP Development**: [`sdk-users/3-development/17-mcp-development-guide.md`](../../../../sdk-users/3-development/17-mcp-development-guide.md)

## Quick Tips

- 💡 **Start simple**: Use basic template first, add features progressively
- 💡 **Authentication**: Enable in production
- 💡 **Caching**: Use for expensive operations
- 💡 **Logging**: Add comprehensive logging

<!-- Trigger Keywords: MCP server template, create MCP server, MCP server boilerplate, Model Context Protocol server, MCP server example, MCP template, production MCP server -->
