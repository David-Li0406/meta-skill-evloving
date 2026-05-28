---
name: mcporter
description: "Direct MCP access via MCPorter. Use for MCPs not covered by specific skills, or for advanced/ad-hoc MCP operations. Supports any configured MCP server."
allowed-tools: Bash(npx:*) Bash(./scripts/*) Read Glob Grep
context: fork
---

# MCPorter - Generic MCP Access

MCPorter provides direct access to any Model Context Protocol (MCP) server configured on your system.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| discover | `./scripts/mcporter.sh discover` | List all configured MCP servers |
| list | `./scripts/mcporter.sh list <server>` | List tools available on a server |
| call | `./scripts/mcporter.sh call <server>.<tool> [args...]` | Call an MCP tool |
| help | `./scripts/mcporter.sh help` | Show usage help |

## How to Use

### Natural Language
- "What MCP servers are available?"
- "List tools on the firecrawl server"
- "Call the scrape tool on firecrawl with url=https://example.com"

### Script Commands
```bash
# Discover available MCPs
./scripts/mcporter.sh discover

# List tools on a specific server
./scripts/mcporter.sh list context7
./scripts/mcporter.sh list firecrawl

# Call a tool with arguments
./scripts/mcporter.sh call firecrawl.scrape url=https://example.com
./scripts/mcporter.sh call chrome-devtools.screenshot url=https://example.com
```

## Available Actions

### discover
List all MCP servers configured on the system.

**Parameters:** None

**Example:**
```bash
./scripts/mcporter.sh discover
```

### list
List all tools available on a specific MCP server.

**Parameters:**
- `server` (required): Name of the MCP server

**Example:**
```bash
./scripts/mcporter.sh list firecrawl
```

### call
Call a specific tool on an MCP server.

**Parameters:**
- `server.tool` (required): Server name and tool name separated by a dot
- `args...` (optional): Key=value arguments for the tool

**Example:**
```bash
./scripts/mcporter.sh call firecrawl.scrape url=https://example.com format=markdown
```

## Prerequisites

- Node.js 18+ installed
- **Option A:** Install MCPorter via Homebrew: `brew tap steipete/tap && brew install mcporter`
- **Option B:** Use via npx (no install required): `npx mcporter`
- MCP servers configured in OpenCode, Cursor, Claude, or other supported tools

## Notes

- For library documentation, prefer the `context7-docs` skill instead
- MCPorter auto-discovers MCP configurations from multiple sources
- Use `discover` first to see what servers are available
- Tool arguments use key=value format
