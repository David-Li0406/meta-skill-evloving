---
name: new-mcp
description: Create a new MCP server for external service integration. Use when adding MCP server, creating MCP integration, scaffolding MCP, or when the user mentions "new MCP", "add MCP server", "create integration", or "MCP for [service]".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(uv:*)
---

# Create New MCP Server

This skill scaffolds a new MCP (Model Context Protocol) server following the established patterns.

## Prerequisites

Before creating an MCP server, gather:
1. **Service name** (lowercase with hyphens, e.g., `slack`, `discord`)
2. **External API** being integrated
3. **Required credentials** (API keys, OAuth, etc.)
4. **Port number** (check [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md) for next available)

## Directory Structure

Create `MCPS/{name}/` with this structure:

```
MCPS/{name}/
├── src/
│   ├── __init__.py
│   ├── server.py      # FastMCP server + FastAPI endpoints
│   ├── client.py      # External API wrapper
│   └── models.py      # Pydantic models
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Steps

### 1. Create Directory Structure

```bash
mkdir -p MCPS/{name}/src
touch MCPS/{name}/src/__init__.py
```

### 2. Create Files

Use templates from [STRUCTURE.md](STRUCTURE.md):
- `pyproject.toml` - Dependencies
- `src/server.py` - FastMCP + FastAPI server
- `src/client.py` - API client wrapper
- `src/models.py` - Pydantic models
- `Dockerfile` - Container configuration

### 3. Update Infrastructure

Follow [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md) to update:
- `docker-compose.yml`
- `Jenkinsfile`
- `DOCUMENTATION/DEPLOYMENT.md`
- `.env.example`

### 4. Create Agent (Optional)

If this MCP server needs a dedicated agent, use the `new-agent` skill.

## Port Allocation

Current ports in use:
- 8080: Telegram MCP (internal)
- 8081: Motion MCP (internal), Telegram MCP (external)
- 8082: Motion MCP (external)
- 8083: GitHub MCP
- 8084: Google Calendar MCP
- 8085: Gmail MCP
- **8086+**: Available for new services

## Checklist

After creation, verify:

- [ ] `pyproject.toml` has correct dependencies
- [ ] `server.py` has FastMCP tools and FastAPI endpoints
- [ ] Health check endpoint at `/health`
- [ ] Dockerfile builds for ARM64
- [ ] Docker Compose entry added
- [ ] Jenkinsfile updated with build/deploy stages
- [ ] `DOCUMENTATION/DEPLOYMENT.md` updated
- [ ] `.env.example` has new environment variables
- [ ] README.md documents the MCP server

## Reference

- [STRUCTURE.md](STRUCTURE.md) - File templates
- [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md) - Infrastructure updates
- `.claude/rules/mcp-servers/fastmcp.md` - MCP patterns
- `.claude/rules/infrastructure/orange-pi.md` - ARM64 requirements
