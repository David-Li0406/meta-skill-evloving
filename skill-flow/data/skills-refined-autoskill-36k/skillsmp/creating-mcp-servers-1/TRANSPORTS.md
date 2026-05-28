# MCP Transports

Detailed documentation for MCP transport types and when to use each.

## Transport Overview

| Transport | Type | Use Case | Auth Support |
|-----------|------|----------|--------------|
| **HTTP** | Remote | Cloud services, APIs | OAuth, Headers |
| **SSE** | Remote | Legacy streaming | OAuth, Headers |
| **stdio** | Local | Custom scripts, local tools | Environment vars |

## HTTP Transport (Recommended)

HTTP is the recommended transport for remote MCP servers. It uses standard HTTP/HTTPS requests.

### Advantages

- Most widely supported
- Standard HTTP authentication
- Works with OAuth 2.0
- Better error handling
- Firewall-friendly

### Basic Usage

```bash
# Simple HTTP server
claude mcp add --transport http myserver https://mcp.example.com

# With custom port
claude mcp add --transport http api https://api.example.com:8443/mcp
```

### With Authentication Headers

```bash
# Bearer token
claude mcp add --transport http secure https://api.example.com/mcp \
  --header "Authorization: Bearer your-token-here"

# API key header
claude mcp add --transport http private https://api.company.com/mcp \
  --header "X-API-Key: your-api-key"

# Multiple headers
claude mcp add --transport http complex https://api.example.com/mcp \
  --header "Authorization: Bearer token" \
  --header "X-Custom-Header: value"
```

### OAuth 2.0 Flow

For OAuth-enabled servers:

1. Add the server without auth:
   ```bash
   claude mcp add --transport http github https://api.githubcopilot.com/mcp/
   ```

2. Authenticate via `/mcp`:
   ```
   > /mcp
   # Select GitHub > Authenticate
   # Complete browser flow
   ```

3. Tokens are stored securely and refreshed automatically

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "http-server": {
      "type": "http",
      "url": "https://mcp.example.com",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-Custom": "value"
      }
    }
  }
}
```

### Environment Variable Expansion

```json
{
  "mcpServers": {
    "flexible-server": {
      "type": "http",
      "url": "${MCP_URL:-https://default.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_TOKEN}"
      }
    }
  }
}
```

## SSE Transport (Deprecated)

Server-Sent Events transport is deprecated. Use HTTP when available.

### When SSE is Still Used

- Legacy server implementations
- Some older third-party servers
- Real-time streaming requirements (rare)

### Usage

```bash
# Basic SSE
claude mcp add --transport sse asana https://mcp.asana.com/sse

# With authentication
claude mcp add --transport sse private https://api.company.com/sse \
  --header "X-API-Key: your-key"
```

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "sse-server": {
      "type": "sse",
      "url": "https://mcp.example.com/sse",
      "headers": {
        "Authorization": "Bearer ${TOKEN}"
      }
    }
  }
}
```

### Migration to HTTP

Most SSE servers are migrating to HTTP. Check your server's documentation for HTTP endpoints.

```bash
# Before (SSE)
claude mcp add --transport sse myserver https://api.example.com/sse

# After (HTTP)
claude mcp add --transport http myserver https://api.example.com/mcp
```

## stdio Transport (Local)

stdio transport runs local processes that communicate via standard input/output.

### Advantages

- Direct system access
- No network overhead
- Works offline
- Full local filesystem access
- Custom business logic

### Basic Usage

```bash
# NPM package
claude mcp add --transport stdio myserver -- npx -y some-mcp-package

# Python script
claude mcp add --transport stdio pyserver -- python /path/to/server.py

# Binary
claude mcp add --transport stdio binary -- /path/to/mcp-server
```

### With Environment Variables

```bash
# Single env var
claude mcp add --transport stdio --env API_KEY=xxx myserver -- npx -y package

# Multiple env vars
claude mcp add --transport stdio \
  --env API_KEY=xxx \
  --env DEBUG=true \
  --env CACHE_DIR=/tmp \
  myserver -- npx -y package

# Database connection
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

### Option Ordering (Important!)

All options MUST come BEFORE the server name:

```bash
# CORRECT: options before name
claude mcp add --transport stdio --env KEY=val --scope user myserver -- command

# WRONG: options after name
claude mcp add myserver --transport stdio -- command  # Will fail!
```

The `--` separates Claude's options from the server command's arguments:

```bash
claude mcp add --transport stdio myserver -- python server.py --port 8080
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^^^^^^
#              Claude Code's options          Server command + its args
```

### Windows Considerations

On Windows (not WSL), wrap npx commands with `cmd /c`:

```bash
# Windows (PowerShell or CMD)
claude mcp add --transport stdio myserver -- cmd /c npx -y package

# Linux/macOS/WSL
claude mcp add --transport stdio myserver -- npx -y package
```

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "local-db": {
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "postgresql://localhost/db"],
      "env": {
        "PGPASSWORD": "${PGPASSWORD}"
      }
    },
    "custom-script": {
      "command": "python",
      "args": ["/path/to/server.py", "--config", "./config.json"],
      "env": {
        "DEBUG": "true"
      }
    }
  }
}
```

### Plugin Path Variables

For plugin-bundled servers:

```json
{
  "mcpServers": {
    "plugin-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DATA_DIR": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

## Choosing the Right Transport

### Decision Tree

```
Need remote access?
    |
    YES --> Cloud service with OAuth?
    |           |
    |          YES --> Use HTTP with OAuth
    |           |
    |          NO --> Use HTTP with headers
    |
    NO --> Local script/binary?
            |
           YES --> Use stdio
            |
           NO --> Reconsider requirements
```

### Transport Comparison

| Factor | HTTP | SSE | stdio |
|--------|------|-----|-------|
| Network latency | Yes | Yes | No |
| Offline support | No | No | Yes |
| OAuth support | Yes | Yes | No |
| System access | No | No | Yes |
| Firewall friendly | Yes | Partial | N/A |
| Team shareable | Yes | Yes | Partial |
| Maintenance | Provider | Provider | You |

### Performance Considerations

- **HTTP**: ~50-200ms per request (network + server)
- **SSE**: Similar to HTTP, with persistent connection
- **stdio**: <10ms (local process)

For high-frequency tool calls, consider stdio for performance.

## Timeout Configuration

Set startup timeout with environment variable:

```bash
# 10 second timeout
MCP_TIMEOUT=10000 claude

# 30 second timeout for slow servers
MCP_TIMEOUT=30000 claude
```

Default timeout varies by transport:
- HTTP: 30 seconds
- SSE: 30 seconds
- stdio: 60 seconds

## Security Considerations

### HTTP/SSE

- Always use HTTPS in production
- Store tokens in environment variables, not in committed files
- Use OAuth when available over static tokens
- Rotate tokens periodically

### stdio

- Validate all inputs in your server
- Run with minimal privileges
- Sandbox if handling untrusted data
- Log access for audit trails

### Credential Storage

```bash
# Good: Environment variable
claude mcp add --transport http api https://api.example.com \
  --header "Authorization: Bearer ${API_TOKEN}"

# Bad: Hardcoded in command (visible in process list)
claude mcp add --transport http api https://api.example.com \
  --header "Authorization: Bearer sk-1234567890"  # Don't do this!
```

## Debugging Transport Issues

### HTTP/SSE

```bash
# Test endpoint directly
curl -I https://mcp.example.com/mcp

# Check in Claude Code
/mcp  # View connection status
```

### stdio

```bash
# Test server manually
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | npx -y package

# Run with debug output
DEBUG=mcp* claude
```

### Common Issues

| Issue | Transport | Solution |
|-------|-----------|----------|
| Connection refused | HTTP/SSE | Check URL, firewall |
| CORS errors | HTTP | Server-side configuration |
| Timeout | All | Increase `MCP_TIMEOUT` |
| "Command not found" | stdio | Use absolute paths |
| Permission denied | stdio | Check file permissions |
