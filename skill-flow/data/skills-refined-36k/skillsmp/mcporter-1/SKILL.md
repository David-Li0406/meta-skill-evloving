---
name: mcporter
description: "MCP (Model Context Protocol) CLI workflows via MCPorter. Use for MCP servers, tool listing/calls, ad-hoc MCP endpoints, auth/OAuth flows, and config management."
---

# MCPorter

Use MCPorter to list MCP servers, call tools, and manage MCP config. Prefer `bun x mcporter` (fallback: `npx --yes mcporter`).

## When to use

- MCP discovery: list configured servers/tools
- Schema checks: confirm required params and types
- Auth/OAuth setup for HTTP servers
- Ad-hoc servers (HTTP/SSE/stdio)

## Discovery checklist

```bash
mcporter list                         # configured servers
mcporter list <server> --schema       # required params + enums
mcporter config list                  # config entries
```

## Quick start

```bash
mcporter list
mcporter list <server>

mcporter call <server.tool> key=value
mcporter call '<server.tool(arg: "value")>'

mcporter auth <server|url>
```

## Common workflows

### List tools

```bash
mcporter list <server>
mcporter describe <server>            # alias of list
mcporter list <server> --all-parameters
mcporter list <server> --schema
```

### Call tools

```bash
mcporter call <server.tool> key=value
mcporter call '<server.tool(arg: "value")>'

# Structured output (best for agents)
mcporter call <server.tool> key=value --output json
```

### Ad-hoc MCP servers

```bash
# HTTP/SSE
mcporter list --http-url https://example.com/mcp --name example
mcporter call --http-url https://example.com/mcp example_tool key=value

# Stdio
mcporter call --stdio "bun run ./server.ts" --name local-tools tool_name key=value
```

### OAuth / Auth

```bash
mcporter auth <server|url>
```

Use when the server requires OAuth. If an ad-hoc HTTP server returns 401/403, MCPorter can auto-promote it to OAuth during auth.

## Troubleshooting

```bash
mcporter config list
mcporter config get <name>
```
