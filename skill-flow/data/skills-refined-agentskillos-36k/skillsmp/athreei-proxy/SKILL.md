---
name: athreei-proxy
description: Invoke athreei MCP server tools through the local gateway
allowed-tools:
  - mcp__athreei__*
  - Bash
---

# athreei Proxy Skill

Route tool calls through the athreei gateway to access configured MCP servers.

## Available Tools

The athreei gateway exposes tools from all configured MCP servers in your organization.
Tools are namespaced as `athreei__<server>__<tool>`.

## Usage

When the user wants to:

- Access browser automation tools
- Call external service APIs through athreei
- Use any MCP server configured in their athreei organization

## Gateway Status

Before using athreei tools, verify the gateway is running:

```bash
athreei gateway status
```

If not running, start it:

```bash
athreei gateway start
```

## Tool Discovery

To list available tools from an MCP server:

```bash
athreei mcp tools <server-id>
```

## Error Handling

If tools are unavailable:

1. Check gateway status
2. Verify MCP server configuration
3. Check authentication status
