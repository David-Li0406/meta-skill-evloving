---
name: mcporter
description: Use this skill for interacting with MCP (Model Context Protocol) servers via the mcporter CLI, including server discovery, tool calls, authentication, and configuration management.
---

# mcporter

Utilize the `mcporter` CLI to interact with MCP servers directly through HTTP or stdio.

## Quick Start

1. List available servers: `mcporter list`
2. View tools for a server: `mcporter list <server> --schema`
3. Call a tool: `mcporter call <server.tool> key=value`

## Calling Tools

Multiple syntaxes are supported for calling MCP tools:

### Selector syntax
```bash
mcporter call <server.tool> key=value
```

### Function syntax
```bash
mcporter call "<server.tool(arg: \"value\")>"
```

### Full URL
```bash
mcporter call https://api.example.com/mcp.fetch url:https://example.com
```

### Stdio mode (ad-hoc servers)
```bash
mcporter call --stdio "bun run ./server.ts" <tool_name> key=value
```

### JSON payload
```bash
mcporter call <server.tool> --args '{"key":"value"}'
```

## Authentication and Configuration

### OAuth authentication
```bash
mcporter auth <server | url>        # Authenticate with a server
mcporter auth <server> --reset      # Reset authentication
```

### Configuration management
```bash
mcporter config list                # List all configured servers
mcporter config get <key>           # Get a config value
mcporter config add <server>        # Add a server
mcporter config remove <server>     # Remove a server
mcporter config import <file>       # Import configuration
mcporter config login                # Login to mcporter cloud
mcporter config logout               # Logout from mcporter cloud
```

## Daemon Management

```bash
mcporter daemon start               # Start the daemon
mcporter daemon status              # Check daemon status
mcporter daemon stop                # Stop the daemon
mcporter daemon restart             # Restart the daemon
```

## Code Generation

### Generate CLI wrapper
```bash
mcporter generate-cli --server <name>
mcporter generate-cli --command <url>
```

### Inspect generated CLI
```bash
mcporter inspect-cli <path>
mcporter inspect-cli <path> --json  # JSON output
```

### Generate TypeScript types
```bash
mcporter emit-ts <server> --mode client   # Generate client code
mcporter emit-ts <server> --mode types    # Generate type definitions
```

## Tips

- Configuration file defaults to `./config/mcporter.json`. Override with `--config <path>`.
- Use `--output json` for machine-readable output when parsing results programmatically.
- When calling tools, both `key=value` and `key:value` syntaxes work for arguments.

## Common Workflows

### List tools
```bash
mcporter list <server>
mcporter describe <server>            # alias of list
mcporter list <server> --all-parameters
mcporter list <server> --schema
```

### Troubleshooting
```bash
mcporter config list
mcporter config get <name>
```