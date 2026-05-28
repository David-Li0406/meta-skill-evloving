# MCP Integration Reference

Model Context Protocol (MCP) server integration guide.

## Overview

MCP allows plugins to integrate external tools and services.

## File Format

`.mcp.json` (in plugin root directory)

## Template

```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse|stdio|http|websocket",
      "url": "server-url",
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      },
      "description": "Server description"
    }
  }
}
```

## Server Types

### 1. SSE (Server-Sent Events)

```json
{
  "mcpServers": {
    "my-sse-server": {
      "type": "sse",
      "url": "http://localhost:3000/sse",
      "description": "SSE server for real-time updates"
    }
  }
}
```

**Use cases:**
- Real-time data streaming
- Continuous monitoring
- Live updates

### 2. STDIO (Standard I/O)

```json
{
  "mcpServers": {
    "my-stdio-server": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "description": "STDIO server for local execution"
    }
  }
}
```

**Use cases:**
- Local script execution
- Command-line tools
- File processing

### 3. HTTP

```json
{
  "mcpServers": {
    "my-http-server": {
      "type": "http",
      "url": "http://localhost:3000/api",
      "description": "HTTP server for REST API"
    }
  }
}
```

**Use cases:**
- REST API integration
- Web services
- External APIs

### 4. WebSocket

```json
{
  "mcpServers": {
    "my-websocket-server": {
      "type": "websocket",
      "url": "ws://localhost:3000/ws",
      "description": "WebSocket server for bidirectional communication"
    }
  }
}
```

**Use cases:**
- Bidirectional communication
- Interactive sessions
- Real-time collaboration

## Configuration Options

### Environment Variables

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "http://localhost:3000",
      "env": {
        "API_KEY": "your-key-here",
        "API_VERSION": "v2"
      }
    }
  }
}
```

### Command Arguments

```json
{
  "mcpServers": {
    "python-server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "server", "--port", "3000"]
    }
  }
}
```

## Best Practices

### Security

1. **Never hardcode sensitive data**
   ```json
   {
     "env": {
       "API_KEY": "${API_KEY}"  // Use environment variables
     }
   }
   ```

2. **Validate server responses**
3. **Use HTTPS for external servers**
4. **Implement rate limiting**
5. **Log all external calls**

### Error Handling

```json
{
  "mcpServers": {
    "reliable-server": {
      "type": "http",
      "url": "http://localhost:3000",
      "timeout": 30000,
      "retries": 3
    }
  }
}
```

### Documentation

Always include clear descriptions:

```json
{
  "description": "Provides file system access for /data directory. Use when reading/writing data files."
}
```

## Common Patterns

### Pattern 1: External API Integration

```json
{
  "mcpServers": {
    "github-api": {
      "type": "http",
      "url": "https://api.github.com",
      "description": "GitHub API for repository operations",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Pattern 2: Local Tool Wrapper

```json
{
  "mcpServers": {
    "docker-wrapper": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "my-mcp-server"],
      "description": "Docker containerized MCP server"
    }
  }
}
```

### Pattern 3: Multiple Servers

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "http://localhost:3000/api",
      "description": "Main API server"
    },
    "websocket-server": {
      "type": "websocket",
      "url": "ws://localhost:3000/ws",
      "description": "WebSocket for real-time updates"
    },
    "local-processor": {
      "type": "stdio",
      "command": "python",
      "args": ["processor.py"],
      "description": "Local data processor"
    }
  }
}
```

## Testing MCP Servers

### Test HTTP Server

```bash
curl http://localhost:3000/health
```

### Test STDIO Server

```bash
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | python server.py
```

### Test WebSocket Server

```bash
wscat -c ws://localhost:3000/ws
```

## Troubleshooting

### Server Not Connecting

1. Check server is running
2. Verify URL/port is correct
3. Check firewall settings
4. Review server logs

### Authentication Issues

1. Verify environment variables are set
2. Check API token validity
3. Review server authentication requirements

### Performance Issues

1. Monitor server response times
2. Check for rate limiting
3. Optimize server queries
4. Consider caching

## Advanced Features

### Dynamic Configuration

Load servers from environment:

```bash
export MCP_SERVER_URL="http://localhost:3000"
```

### Conditional Servers

Use hooks to conditionally start servers:

```markdown
<!-- hooks/session-start/init-mcp.md -->
---
description: Initialize MCP servers if needed
---

Check if servers are running:
- If not, start required servers
- Verify connectivity
- Log status
```

## Validation Checklist

- [ ] Server type is valid (sse|stdio|http|websocket)
- [ ] URL/command is correct
- [ ] Environment variables use ${VAR} format
- [ ] Description is clear
- [ ] Timeout configured (if needed)
- [ ] Error handling considered
- [ ] Security reviewed (no hardcoded secrets)
- [ ] Server tested independently
- [ ] Documentation complete
