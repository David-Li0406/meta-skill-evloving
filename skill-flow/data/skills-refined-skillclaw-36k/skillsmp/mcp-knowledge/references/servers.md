# MCP Server Configuration

## Table of Contents

- [🚨 MANDATORY: Read BEFORE Configuration](#mandatory-read-before-configuration)
- [Official MCP Servers](#official-mcp-servers)
- [Transport Mechanisms](#transport-mechanisms)
- [Configuration File Locations](#configuration-file-locations)
- [Security Considerations](#security-considerations)
- [Multi-Server Setup](#multi-server-setup)
- [Testing Configuration](#testing-configuration)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

Configure, deploy, and manage MCP servers for Claude Code integration.

## 🚨 MANDATORY: Read BEFORE Configuration

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official MCP Guide**: https://code.claude.com/docs/en/mcp
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any MCP server configuration
  - **Content**: MCP integration patterns, configuration options
  - **Cache**: 15 minutes minimum

- **[MUST READ] MCP Specification**: https://modelcontextprotocol.io/
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before custom server implementation
  - **Content**: Protocol specification, transport mechanisms
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding MCP primitives
- **MUST validate** transport mechanism before configuration
- **REQUIRED** to understand security considerations

## Official MCP Servers

### 1. Context7
Knowledge base integration with document ingestion and semantic search.

**Configuration**:
```json
{
  "context7": {
    "command": "context7-server",
    "args": ["--path", "./docs"]
  }
}
```

**Features**:
- Document ingestion and indexing
- Semantic search capabilities
- Multi-format support (PDF, MD, TXT)
- Context-aware retrieval

**Use Cases**:
- Documentation search
- Knowledge base queries
- Research assistance

### 2. DeepWiki
Documentation analysis with automatic parsing and API discovery.

**Configuration**:
```json
{
  "deepwiki": {
    "command": "deepwiki-server",
    "args": ["--repo", "https://github.com/org/repo"]
  }
}
```

**Features**:
- Automatic documentation parsing
- API endpoint discovery
- Code example extraction
- Wiki generation

**Use Cases**:
- API documentation analysis
- Codebase understanding
- Technical documentation review

### 3. DuckDuckGo
Privacy-focused web search with real-time results.

**Configuration**:
```json
{
  "duckduckgo": {
    "command": "ddg-mcp-server"
  }
}
```

**Features**:
- Privacy-focused search
- Real-time web results
- No API key required
- Instant answers

**Use Cases**:
- Web research
- Current information lookup
- General search queries

## Transport Mechanisms

### stdio Configuration
Local process execution via standard input/output.

```json
{
  "server-name": {
    "command": "node",
    "args": ["server.js"],
    "env": {
      "API_KEY": "${API_KEY}"
    }
  }
}
```

**When to Use**:
- Local MCP server implementation
- Process-based integration
- Development/testing scenarios
- Single-user environments

### Streamable HTTP Configuration
Hosted services with bidirectional streaming.

```json
{
  "server-name": {
    "type": "streamable-http",
    "url": "https://mcp.example.com/server",
    "headers": {
      "Authorization": "Bearer ${TOKEN}"
    }
  }
}
```

**When to Use**:
- Cloud-based MCP servers
- Shared server instances
- Production deployments
- High-availability scenarios

## Configuration File Locations

### Plugin Configuration
Create `.mcp.json` in plugin root:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "server-command",
      "args": ["--arg1", "value1"]
    }
  }
}
```

### Inline Plugin Configuration
Add to `plugin.json`:

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "server-name": {
      "command": "server-command"
    }
  }
}
```

### User Settings
Create `.claude/mcp-servers.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "server-command"
    }
  }
}
```

## Security Considerations

### Authentication
Always secure MCP servers:

```json
{
  "secure-server": {
    "type": "streamable-http",
    "url": "https://mcp.example.com/api",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

### Environment Variables
Use environment variables for sensitive data:

```json
{
  "server-name": {
    "command": "server",
    "env": {
      "API_KEY": "${API_KEY}",
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

### HTTPS Requirement
Never use unencrypted HTTP for production.

## Multi-Server Setup

Configure multiple servers:

```json
{
  "mcpServers": {
    "search": {
      "command": "search-server"
    },
    "database": {
      "type": "streamable-http",
      "url": "https://db.example.com/mcp"
    },
    "filesystem": {
      "command": "fs-server",
      "args": ["--root", "./data"]
    }
  }
}
```

## Testing Configuration

### Verify Server Starts
```bash
# Test stdio server
./server.js

# Test HTTP server
curl https://your-mcp-server.com/health
```

### Check Tool Discovery
- Tools appear in Claude Code
- Resources are accessible
- Prompts are available

## Troubleshooting

### Server Not Starting
1. Check server binary exists
2. Verify dependencies installed
3. Test server independently
4. Check environment variables

### Tools Not Discovered
1. Verify tools/list handler
2. Check tool schema validity
3. Restart Claude Code
4. Validate MCP configuration

### Connection Timeout
1. Check network connectivity
2. Verify server is running
3. Test with curl/netcat
4. Review firewall settings

## Next Steps

After configuration:
- See **[tools.md](tools.md)** to develop custom tools
- See **[resources.md](resources.md)** for resources and prompts
- Test integration thoroughly before production use
