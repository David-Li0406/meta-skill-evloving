# MCP Management Guide

Guide for managing Model Context Protocol (MCP) servers with agent-deck.

## Overview

MCPs extend Claude's capabilities. Agent-deck supports:

- **LOCAL** - Project-specific (`.mcp.json` file)
- **GLOBAL** - All projects (`~/.claude-work/.claude.json`)

## When to Use Which

### Use LOCAL when:
- MCP is specific to this project
- Different projects need different configurations

### Use GLOBAL when:
- MCP is useful across all projects
- MCP provides general-purpose functionality

## Commands

```bash
# List available MCPs
agent-deck mcp list

# Check what's attached
agent-deck mcp attached my-project

# Attach locally (default)
agent-deck mcp attach my-project exa

# Attach globally
agent-deck mcp attach my-project memory -global

# Attach and restart to load immediately
agent-deck mcp attach my-project playwright -restart

# Detach
agent-deck mcp detach my-project exa
agent-deck mcp detach my-project memory -global
```

## MCP Configuration

MCPs are defined in `~/.agent-deck/config.toml`:

```toml
[mcps.exa]
command = "npx"
args = ["-y", "exa-mcp-server"]
env = { EXA_API_KEY = "your-key" }
description = "Web search via Exa AI"
```

## Best Practices

1. **Start Local, Promote to Global** - Test locally first
2. **Use Restart Flag** - For immediate effect: `-restart`
3. **Check Attached MCPs** - Before debugging tool access issues

## Troubleshooting

**MCP Not Available:**
```bash
agent-deck mcp attached my-project  # Check if attached
agent-deck session restart my-project  # Reload MCPs
```

**Changes Not Taking Effect:**
```bash
agent-deck session restart my-project
```
