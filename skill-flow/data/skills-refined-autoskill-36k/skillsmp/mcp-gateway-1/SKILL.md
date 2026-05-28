---
name: mcp-gateway
description: "Comprehensive management of MCP Gateway (gh-aw-mcpg) for running GitHub MCP servers. Use when: (1) Starting/stopping MCP Gateway containers with GitHub MCP server support, (2) Debugging gateway connection or authentication issues, (3) Configuring Copilot CLI to use MCP Gateway via HTTP, (4) Setting up gateway for use with AWF (Agentic Workflow Firewall), (5) Troubleshooting MCP server initialization or token passthrough problems, (6) Managing Docker-based MCP server lifecycle. Includes scripts for gateway startup, health checking, debugging, and Copilot CLI integration."
---

# MCP Gateway Management Skill

This skill provides comprehensive guidance for setting up, managing, and debugging the MCP Gateway (gh-aw-mcpg) for running GitHub MCP servers.

## What is MCP Gateway?

The MCP Gateway (`gh-aw-mcpg`) is a proxy server that:
- Routes requests to multiple MCP (Model Context Protocol) backend servers
- Manages MCP server lifecycle (start/stop containers)
- Provides HTTP/SSE transport for MCP protocol  
- Handles authentication and session management
- Supports both routed (`/mcp/<server>`) and unified (`/mcp`) modes

## Quick Start

### 1. Start the Gateway

```bash
python3 scripts/start-gateway.py
```

This will:
- Get GitHub token from `gh` CLI (or use `$GITHUB_PERSONAL_ACCESS_TOKEN`)
- Create MCP Gateway configuration
- Start gateway container on port 80
- Spawn GitHub MCP server container
- Display connection information

**Key Environment Variables:**
- `GATEWAY_VERSION` - Gateway version (default: v0.0.59)
- `GATEWAY_PORT` - Host port (default: 80)
- `GATEWAY_DOMAIN` - Gateway domain (default: localhost)
- `GATEWAY_API_KEY` - API authentication key (auto-generated)
- `GITHUB_PERSONAL_ACCESS_TOKEN` - GitHub PAT for MCP server

### 2. Verify Gateway is Running

```bash
curl http://127.0.0.1:80/health | jq .
```

Expected response:
```json
{
  "status": "healthy",
  "specVersion": "1.5.0",
  "gatewayVersion": "v0.0.59",
  "servers": {
    "github": {
      "status": "running",
      "uptime": 0
    }
  }
}
```

### 3. Debug Issues

```bash
python3 scripts/debug-gateway.py
```

Shows:
- Container status
- Health check results
- Gateway logs
- MCP server containers
- Common configuration issues

### 4. Stop the Gateway

```bash
python3 scripts/stop-gateway.py
```

Stops and removes the gateway container and any MCP server containers.

## Configuration

### Gateway Config Format (v0.0.59+)

The gateway requires JSON configuration via stdin:

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "container": "ghcr.io/github/github-mcp-server:latest",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      }
    }
  },
  "gateway": {
    "port": 8000,
    "domain": "localhost",
    "apiKey": "your-api-key"
  }
}
```

**Key Points:**
- `type: "stdio"` - Containerized stdio-based MCP server
- `container` - Docker image for the MCP server
- `env.GITHUB_PERSONAL_ACCESS_TOKEN` - Must be explicit value (not empty string)
- `gateway.domain` - Required field in v0.0.59+
- `gateway.apiKey` - Used for client authentication

### Required Environment Variables (Container)

When starting the container, you MUST set:
- `MCP_GATEWAY_PORT=8000` - Internal port (must match config)
- `MCP_GATEWAY_DOMAIN=localhost` - Gateway domain (must match config)
- `MCP_GATEWAY_API_KEY=xxx` - API key (must match config)
- `GITHUB_PERSONAL_ACCESS_TOKEN=xxx` - For token passthrough

### Starting the Container

**Important:** The container must be started with `-i` flag and config piped via stdin:

```bash
cat config.json | docker run -i \
  --name mcpg-gateway \
  -p 80:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e "GITHUB_PERSONAL_ACCESS_TOKEN=${TOKEN}" \
  -e "MCP_GATEWAY_PORT=8000" \
  -e "MCP_GATEWAY_DOMAIN=localhost" \
  -e "MCP_GATEWAY_API_KEY=${API_KEY}" \
  ghcr.io/githubnext/gh-aw-mcpg:v0.0.59
```

**Note:** Do not use `-d` (detached) with `-i` - run in background using `&` instead:
```bash
(cat config.json | docker run -i ...) > /tmp/gateway.log 2>&1 &
```

## Using with Copilot CLI

### Setup

```bash
python3 scripts/setup-copilot.py
```

This creates `/tmp/mcp-gateway-config.json`:

```json
{
  "mcpServers": {
    "github-gateway": {
      "type": "http",
      "url": "http://host.docker.internal:80/mcp/github",
      "headers": {
        "Authorization": "your-api-key"
      },
      "tools": ["*"]
    }
  }
}
```

### Usage (Direct)

```bash
npx @github/copilot \
  --disable-builtin-mcps \
  --additional-mcp-config @/tmp/mcp-gateway-config.json \
  --allow-all-tools \
  --prompt "List 3 recent issues from githubnext/gh-aw"
```

### Usage (With AWF)

```bash
sudo -E awf \
  --enable-host-access \
  --mount /tmp:/tmp:rw \
  --allow-domains 'host.docker.internal,api.github.com,*.githubusercontent.com' \
  -- npx -y @github/copilot \
    --disable-builtin-mcps \
    --additional-mcp-config @/tmp/mcp-gateway-config.json \
    --allow-all-tools \
    --prompt "Your prompt here"
```

**Key Flags:**
- `--enable-host-access` - Enables `host.docker.internal` resolution
- `--mount /tmp:/tmp:rw` - Makes MCP config accessible in container
- `--disable-builtin-mcps` - Prevents Copilot from spawning its own MCP server
- `--additional-mcp-config` - Uses HTTP-based gateway config

## Troubleshooting

### Gateway Won't Start

**Symptom:** Container immediately exits or restarts

**Check:**
1. Are all required env vars set? (`MCP_GATEWAY_PORT`, `MCP_GATEWAY_DOMAIN`, `MCP_GATEWAY_API_KEY`)
2. Is config being piped via stdin? (container must use `-i` flag)
3. Is config format valid JSON?

**Debug:**
```bash
docker logs mcpg-gateway
```

Look for:
- "Required environment variables not set"
- "Container was not started with -i flag"
- "Configuration validation error"

### GitHub MCP Server Fails to Launch

**Symptom:** Logs show "failed to register tools from github"

**Check:**
1. Is `GITHUB_PERSONAL_ACCESS_TOKEN` explicitly set in config (not empty string)?
2. Is the token valid and has required scopes?
3. Is Docker socket mounted (`-v /var/run/docker.sock:/var/run/docker.sock`)?

**Debug:**
```bash
docker logs mcpg-gateway 2>&1 | grep -A5 'GITHUB_PERSONAL_ACCESS_TOKEN'
```

Look for:
- "✗ WARNING: Env passthrough for GITHUB_PERSONAL_ACCESS_TOKEN requested but NOT FOUND"
- "❌ MCP Connection Failed"

**Fix:** Use explicit token value in config instead of variable expansion:
```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_actualtoken123"
  }
}
```

### Copilot Can't Connect to Gateway

**Symptom:** "fetch failed" or "ECONNREFUSED" errors

**Check:**
1. Is gateway running? `curl http://127.0.0.1:80/health`
2. Is `--enable-host-access` flag set (for AWF)?
3. Is `host.docker.internal` in allowed domains?
4. Is MCP config file path correct and mounted?

**Debug:**
```bash
# From within AWF container
curl -v http://host.docker.internal:80/health
```

### "method is invalid during session initialization"

**Symptom:** Tool calls fail with initialization error

**Cause:** HTTP sessions are stateless - each request creates a new session

**Solution:** This is expected behavior for HTTP transport. The gateway handles initialization automatically for each request. If you see persistent errors, check:
1. Is the Authorization header correct?
2. Is the MCP Gateway version latest?

### Port 80 Already in Use

**Symptom:** "address already in use" when starting container

**Solution:** Use different host port:
```bash
GATEWAY_PORT=8080 python3 scripts/start-gateway.py
```

Then update Copilot config to use port 8080.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    HOST MACHINE                      │
│                                                      │
│  ┌──────────────────┐                               │
│  │  MCP Gateway     │                               │
│  │  Container       │                               │
│  │  Port 80:8000    │                               │
│  └────────┬─────────┘                               │
│           │ spawns via docker socket                │
│           ▼                                          │
│  ┌──────────────────┐                               │
│  │  GitHub MCP      │                               │
│  │  Server          │                               │
│  │  Container       │                               │
│  └──────────────────┘                               │
│                                                      │
│  Client connects to http://127.0.0.1:80/mcp/github  │
└──────────────────────────────────────────────────────┘
```

**With AWF:**
```
┌─────────────────────────────────────────────────────┐
│                    HOST                              │
│  ┌──────────────┐                                    │
│  │ MCP Gateway  │◄──────────┐                        │
│  │ Port 80      │           │                        │
│  └──────────────┘           │                        │
│                             │                        │
│  ┌──────────────────────────┼──────────────┐         │
│  │        AWF Network       │              │         │
│  │  ┌────────┐    ┌─────────┴──┐          │         │
│  │  │ Agent  │───▶│ Squid      │          │         │
│  │  │        │    │ Proxy      │──────────┘         │
│  │  │Copilot │    │            │ CONNECT to         │
│  │  │  CLI   │    │host.docker.│ host:80            │
│  │  └────────┘    │ internal   │                    │
│  │                └────────────┘                    │
│  └───────────────────────────────────────┘         │
└─────────────────────────────────────────────────────┘
```

## Version Differences

### v0.0.59 (Latest)

**New Requirements:**
- Config via stdin with `-i` flag (not file mount)
- Three required env vars: `MCP_GATEWAY_PORT`, `MCP_GATEWAY_DOMAIN`, `MCP_GATEWAY_API_KEY`
- `gateway.domain` field required in config
- Explicit token values (variable expansion `${VAR}` may not work reliably)

### v0.0.10 (Older)

**Simpler startup:**
- No stdin config required
- Fewer env vars needed
- Default configuration works out of the box

**Recommendation:** Use v0.0.59+ for latest features and security improvements.

## Best Practices

1. **Token Management**
   - Use `gh auth token` to get current GitHub token
   - Store API key securely (don't commit to repo)
   - Rotate tokens regularly

2. **Container Lifecycle**
   - Run gateway in background with `&` not `-d`
   - Redirect logs to file for debugging
   - Use `--restart unless-stopped` for production

3. **Networking**
   - Use port 80 for simplicity (or custom port if needed)
   - Always use `host.docker.internal` from containers
   - Add to AWF allowed domains

4. **Debugging**
   - Always check health endpoint first
   - Use debug script for comprehensive diagnostics
   - Check both gateway and MCP server logs

5. **Security**
   - Only use `--enable-host-access` with trusted workloads
   - Keep API keys secret
   - Use restrictive domain whitelists in AWF

## Common Commands

```bash
# Start gateway
python3 scripts/start-gateway.py

# Check status
curl http://127.0.0.1:80/health | jq .

# View logs
docker logs mcpg-gateway -f

# Debug issues
python3 scripts/debug-gateway.py

# Setup Copilot
python3 scripts/setup-copilot.py

# Stop gateway
python3 scripts/stop-gateway.py

# Restart gateway
docker restart mcpg-gateway

# Check MCP servers
docker ps | grep mcp

# Clean up everything
docker stop mcpg-gateway && docker rm mcpg-gateway
docker ps -a | grep mcp | awk '{print $1}' | xargs -r docker rm -f
```

## Additional Resources

- [MCP Gateway Repository](https://github.com/githubnext/gh-aw-mcpg)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [AWF Documentation](https://github.com/githubnext/gh-aw-firewall)
