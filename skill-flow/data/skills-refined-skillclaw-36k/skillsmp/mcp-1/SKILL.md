---
name: mcp
description: "Kailash MCP (Model Context Protocol) - production-ready MCP server implementation for AI agent integration. Use when asking about 'MCP', 'Model Context Protocol', 'MCP server', 'MCP client', 'MCP tools', 'MCP resources', 'MCP prompts', 'MCP authentication', 'MCP transports', 'stdio transport', 'SSE transport', 'HTTP transport', 'MCP testing', 'progress reporting', or 'structured tools'."
---

# Kailash MCP - Model Context Protocol Integration

Production-ready MCP server implementation built into Kailash Core SDK for seamless AI agent integration.

## Overview

Kailash's MCP module provides:

- **Full MCP Specification**: Complete implementation of Model Context Protocol
- **Multiple Transports**: stdio, SSE, HTTP support
- **Structured Tools**: Type-safe tool definitions
- **Resource Management**: Expose data sources to AI agents
- **Authentication**: Secure MCP server access
- **Progress Reporting**: Real-time operation status
- **Testing Support**: Comprehensive testing utilities

## Quick Start

```python
from kailash.mcp_server import MCPServer

# Create MCP server
server = MCPServer(name="my-server")

# Register workflow as MCP tool
@server.tool("summarize")
def summarize_tool(text: str) -> str:
    """Summarize the given text."""
    # Execute workflow
    workflow = create_summary_workflow()
    results = runtime.execute(workflow.build())
    return results["summary"]["result"]

# Run server (stdio transport by default)
server.run()
```

## Reference Documentation

### Getting Started
- **[mcp-transports-quick](mcp-transports-quick.md)** - Transport configuration (stdio, SSE, HTTP)
- **[mcp-structured-tools](mcp-structured-tools.md)** - Defining MCP tools
- **[mcp-resources](mcp-resources.md)** - Exposing resources to agents

### Security & Operations
- **[mcp-authentication](mcp-authentication.md)** - Authentication and authorization
- **[mcp-progress-reporting](mcp-progress-reporting.md)** - Progress updates for long operations
- **[mcp-testing-patterns](mcp-testing-patterns.md)** - Testing MCP servers and tools

## Key Concepts

### MCP Protocol
The Model Context Protocol enables AI agents to:
- **Tools**: Call structured functions
- **Resources**: Access data sources
- **Prompts**: Use pre-defined templates
- **Sampling**: Request LLM completions

### Transports
MCP supports multiple transport mechanisms:
- **stdio**: Standard input/output (default, simplest)
- **SSE**: Server-Sent Events (for web clients)
- **HTTP**: RESTful API (for HTTP clients)

### Structured Tools
Tools are type-safe functions exposed to AI agents:
- Automatic schema generation from Python type hints
- Input validation
- Error handling
- Progress reporting

### Resources
Resources expose data to AI agents:
- File systems
- Databases
- APIs
- Custom data sources

## When to Use This Skill

Use MCP when you need to:
- Expose workflows as tools for AI agents
- Build MCP servers for Claude Desktop or other clients
- Integrate Kailash workflows with AI assistants
- Provide structured tools to language models
- Expose resources for RAG applications
- Build custom MCP integrations

## Integration Patterns

### With Core SDK (Workflow Tools)
```python
from kailash.mcp_server import MCPServer
from kailash.workflow.builder import WorkflowBuilder

server = MCPServer(name="workflow-server")

@server.tool("process_data")
def process_tool(input: str) -> dict:
    workflow = WorkflowBuilder()
    # Build workflow
    results = runtime.execute(workflow.build())
    return results["output"]["result"]
```

### With Nexus (Multi-Channel with MCP)
```python
from nexus import Nexus

# Nexus automatically creates MCP channel
nexus = Nexus(workflows)
nexus.run()  # Includes MCP server
```

### With DataFlow (Database Access)
```python
from kailash.mcp_server import MCPServer
from dataflow import DataFlow

server = MCPServer(name="db-server")
db = DataFlow(...)

@server.resource("users")
def get_users():
    # Expose database via MCP resource
    return db.query_users()
```

### With Kaizen (Agent Tools)
```python
from kailash.mcp_server import MCPServer
from kaizen.base import BaseAgent

server = MCPServer(name="agent-server")

@server.tool("analyze")
def analyze_tool(text: str) -> str:
    agent = AnalysisAgent()
    return agent(text=text).result
```

## Critical Rules

- ✅ Use stdio transport for local development
- ✅ Define clear tool schemas with type hints
- ✅ Implement progress reporting for long operations
- ✅ Test MCP servers with real MCP clients
- ✅ Use authentication for production servers
- ❌ NEVER expose sensitive data without authentication
- ❌ NEVER skip input validation
- ❌ NEVER mock MCP protocol in tests (use real transports)

## Transport Selection

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Local tools, CLI | Simple, reliable | Local only |
| **SSE** | Web apps | Real-time updates | Complex setup |
| **HTTP** | APIs, services | Standard protocol | No streaming |

## Version Compatibility

- **Core SDK Version**: 0.9.25+
- **MCP Specification**: Latest
- **Python**: 3.8+
- **Transports**: stdio, SSE, HTTP

## Related Skills

- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core workflow patterns
- **[03-nexus](../nexus/SKILL.md)** - Nexus includes MCP channel
- **[04-kaizen](../kaizen/SKILL.md)** - AI agents as MCP tools
- **[02-dataflow](../dataflow/SKILL.md)** - Database resources

## Support

For MCP-specific questions, invoke:
- `mcp-specialist` - MCP server implementation
- `testing-specialist` - MCP testing strategies
- `framework-advisor` - MCP integration architecture
