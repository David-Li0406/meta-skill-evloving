---
name: mcp-transports-quick
description: "MCP transport configuration patterns (STDIO, HTTP, WebSocket). Use when asking 'MCP transport', 'stdio mcp', 'websocket mcp', 'HTTP transport', 'mcp connection', or 'mcp server setup'."
---

# MCP Transports Quick Reference

Configure MCP server connections using STDIO, HTTP, or WebSocket transports.

> **Skill Metadata**
> Category: `mcp`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md), [`mcp-authentication`](mcp-authentication.md)
> Related Subagents: `mcp-specialist` (server implementation, troubleshooting)

## Quick Reference

- **STDIO**: Local process communication (fastest, recommended for development)
- **HTTP**: Remote servers, production deployments (stateless)
- **WebSocket**: Real-time bidirectional communication (stateful connections)
- **Transport Selection**: Choose based on deployment model and latency requirements

## Transport Patterns

### STDIO Transport (Recommended for Local Development)

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# STDIO: Launch MCP server as subprocess
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get weather for NYC"}],
    "mcp_servers": [{
        "name": "weather",
        "transport": "stdio",
        "command": "python",
        "args": ["-m", "weather_mcp_server"]
    }],
    "auto_discover_tools": True
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

**When to Use STDIO:**
- Local development and testing
- Desktop applications
- CLI tools
- Single-machine deployments
- Lowest latency requirements

### HTTP Transport (Production Deployments)

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search documents"}],
    "mcp_servers": [{
        "name": "doc_search",
        "transport": "http",
        "url": "https://api.company.com/mcp/search",
        "headers": {
            "Authorization": "Bearer ${API_TOKEN}",
            "X-Tenant-ID": "tenant_123"
        },
        "timeout": 30
    }],
    "auto_discover_tools": True
})
```

**When to Use HTTP:**
- Production deployments
- Microservices architecture
- Cloud-hosted MCP servers
- Load-balanced environments
- Stateless operations

### WebSocket Transport (Real-Time Communication)

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Monitor system metrics"}],
    "mcp_servers": [{
        "name": "metrics",
        "transport": "websocket",
        "url": "wss://metrics.company.com/mcp",
        "connection_params": {
            "heartbeat_interval": 30,
            "reconnect_attempts": 3,
            "reconnect_delay": 5
        }
    }],
    "auto_discover_tools": True
})
```

**When to Use WebSocket:**
- Real-time streaming data
- Long-running operations with progress updates
- Bidirectional communication
- Event-driven architectures

## Configuration Patterns

### Multiple Transports in One Workflow

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Analyze weather and documents"}],
    "mcp_servers": [
        {
            "name": "weather",
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "weather_mcp"]
        },
        {
            "name": "docs",
            "transport": "http",
            "url": "https://api.company.com/mcp/docs",
            "headers": {"Authorization": "Bearer ${API_TOKEN}"}
        },
        {
            "name": "metrics",
            "transport": "websocket",
            "url": "wss://metrics.company.com/mcp"
        }
    ],
    "auto_discover_tools": True
})
```

### Transport with Retry Configuration

```python
# HTTP with retry logic
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search"}],
    "mcp_servers": [{
        "name": "search",
        "transport": "http",
        "url": "https://api.company.com/mcp/search",
        "retry_config": {
            "max_retries": 3,
            "backoff_factor": 2.0,
            "retry_on": [502, 503, 504]
        },
        "timeout": 60
    }]
})
```

### Environment-Based Transport Configuration

```python
import os

# Use environment variable to switch transports
transport_config = {
    "development": {
        "transport": "stdio",
        "command": "python",
        "args": ["-m", "mcp_server"]
    },
    "production": {
        "transport": "http",
        "url": os.getenv("MCP_SERVER_URL"),
        "headers": {"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"}
    }
}

env = os.getenv("ENV", "development")

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Process data"}],
    "mcp_servers": [{
        "name": "processor",
        **transport_config[env]
    }]
})
```

## Transport Comparison

| Feature | STDIO | HTTP | WebSocket |
|---------|-------|------|-----------|
| **Latency** | Lowest | Medium | Low-Medium |
| **Scalability** | Single machine | High | Medium |
| **State** | Process-bound | Stateless | Stateful |
| **Best For** | Local dev | Production | Real-time |
| **Complexity** | Low | Medium | High |
| **Load Balancing** | No | Yes | Limited |
| **Reconnection** | Process restart | Per-request | Automatic |

## Common Patterns

### Pattern 1: Development to Production

```python
# Development: STDIO for fast iteration
dev_config = {
    "transport": "stdio",
    "command": "python",
    "args": ["-m", "mcp_server", "--debug"]
}

# Production: HTTP with authentication
prod_config = {
    "transport": "http",
    "url": "https://mcp.company.com/api",
    "headers": {"Authorization": f"Bearer {os.getenv('MCP_TOKEN')}"},
    "timeout": 30
}

config = prod_config if os.getenv("ENV") == "production" else dev_config
```

### Pattern 2: Graceful Fallback

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get data"}],
    "mcp_servers": [
        {
            "name": "primary",
            "transport": "http",
            "url": "https://primary.api.com/mcp",
            "timeout": 5
        },
        {
            "name": "fallback",
            "transport": "http",
            "url": "https://backup.api.com/mcp",
            "timeout": 10
        }
    ]
})
# IterativeLLMAgentNode automatically tries fallback if primary fails
```

## Troubleshooting

### STDIO Issues

```python
# Issue: Process not found
# Solution: Use absolute paths
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "server",
        "transport": "stdio",
        "command": "/usr/bin/python3",  # Absolute path
        "args": ["-m", "mcp_server"],
        "env": {"PYTHONPATH": "/path/to/modules"}  # Set environment
    }]
})
```

### HTTP Issues

```python
# Issue: Connection timeout
# Solution: Increase timeout and add retry
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "server",
        "transport": "http",
        "url": "https://slow-api.com/mcp",
        "timeout": 120,  # Longer timeout
        "retry_config": {
            "max_retries": 5,
            "backoff_factor": 3.0
        }
    }]
})
```

### WebSocket Issues

```python
# Issue: Connection drops
# Solution: Configure reconnection
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "server",
        "transport": "websocket",
        "url": "wss://api.com/mcp",
        "connection_params": {
            "heartbeat_interval": 15,  # More frequent heartbeat
            "reconnect_attempts": 10,
            "reconnect_delay": 2,
            "ping_timeout": 5
        }
    }]
})
```

## Best Practices

1. **Use STDIO for development** - Fastest iteration, easier debugging
2. **Use HTTP for production** - Scalable, load-balanced, stateless
3. **Use WebSocket for streaming** - Real-time data, progress updates
4. **Always set timeouts** - Prevent hanging workflows
5. **Configure retries** - Handle transient failures gracefully
6. **Use environment variables** - Keep credentials secure
7. **Test transport switching** - Ensure dev/prod parity

## Related Patterns

- **MCP Integration**: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)
- **Authentication**: [`mcp-authentication`](mcp-authentication.md)
- **Testing**: [`mcp-testing-patterns`](mcp-testing-patterns.md)

## When to Escalate to Subagent

Use `mcp-specialist` subagent when:
- Implementing custom MCP server with multiple transports
- Troubleshooting transport-specific connection issues
- Configuring production load balancing and failover
- Implementing custom transport protocols
- Performance tuning for high-throughput scenarios

## Documentation References

### Primary Sources
- **MCP Integration**: [`sdk-users/1-getting-started/mcp-integration.md`](../../../../sdk-users/1-getting-started/mcp-integration.md)
- **IterativeLLMAgentNode**: [`sdk-users/2-core-concepts/nodes/02-ai-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/02-ai-nodes.md)

## Quick Tips

- Start with STDIO in development for fastest iteration
- Switch to HTTP for production deployments
- Use WebSocket only when real-time bidirectional communication is required
- Always configure timeouts to prevent hanging
- Test transport failover scenarios

## Version Notes

- **v0.9.25+**: Real MCP tool execution in IterativeLLMAgentNode
- **v0.6.5+**: Enhanced MCP transport support

<!-- Trigger Keywords: MCP transport, stdio, websocket, HTTP transport, mcp connection, mcp server setup, mcp stdio, mcp http, mcp websocket, transport configuration, mcp deployment -->
