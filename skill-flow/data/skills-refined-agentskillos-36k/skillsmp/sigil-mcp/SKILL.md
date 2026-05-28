---
name: sigil-mcp
description: Model Context Protocol server for Sigil MPC signing. Use for deploying Sigil as a universal agent-compatible signing server that works with Claude Desktop, VS Code, and any MCP-compliant client.
allowed-tools: Read, Bash, Glob, Grep
---

# Sigil MCP Server

The Sigil MCP server implements the Model Context Protocol (MCP) specification, enabling any MCP-compatible AI agent to securely sign blockchain transactions using Sigil's MPC infrastructure.

## Quick Start

### Building

```bash
# Build the MCP server
cargo build -p sigil-mcp --release

# Binary located at: target/release/sigil-mcp
```

### Running

```bash
# Start with stdio transport (for Claude Desktop, VS Code)
sigil-mcp --transport stdio

# With verbose logging
sigil-mcp --transport stdio --log-level debug
```

## Integration with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "sigil": {
      "command": "/path/to/sigil-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

## Available Tools

The MCP server exposes the following tools:

| Tool | Description |
|------|-------------|
| `sigil_check_disk` | Check if a signing disk is inserted and valid |
| `sigil_sign_evm` | Sign EVM transactions (Ethereum, Polygon, etc.) |
| `sigil_sign_frost` | Sign with FROST (Bitcoin Taproot, Solana, Zcash) |
| `sigil_get_address` | Get the signing address for the current disk |
| `sigil_update_tx_hash` | Record transaction hash in audit log |
| `sigil_list_schemes` | List supported signature schemes |
| `sigil_get_presig_count` | Get remaining presignatures |

## Available Resources

| Resource URI | Description |
|--------------|-------------|
| `sigil://disk/status` | Real-time disk status |
| `sigil://presigs/info` | Presignature statistics |
| `sigil://supported-chains` | List of supported blockchains |
| `sigil://children/{id}` | Child disk information |

## Available Prompts

| Prompt | Description |
|--------|-------------|
| `sign_evm_transfer` | Guided EVM transfer workflow |
| `sign_bitcoin_taproot` | Guided Bitcoin Taproot signing |
| `sign_solana_transfer` | Guided Solana transfer |
| `troubleshoot_disk` | Diagnose disk issues |
| `check_signing_readiness` | Verify system readiness |

## MCP Protocol

The server implements MCP version 2025-11-25 with:

- **Transport**: stdio (newline-delimited JSON-RPC 2.0)
- **Capabilities**: tools, resources (with subscriptions), prompts, logging

### Example Initialize Handshake

**Client Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {
      "name": "my-agent",
      "version": "1.0.0"
    }
  }
}
```

**Server Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true, "listChanged": true },
      "prompts": { "listChanged": false },
      "logging": {}
    },
    "serverInfo": {
      "name": "sigil-mcp",
      "version": "0.1.0"
    }
  }
}
```

### Example Tool Call

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "sigil_check_disk",
    "arguments": {}
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{
      "type": "text",
      "text": "Disk detected (sigil_7a3f2c1b)\n├─ Presigs: 847/1000 remaining\n├─ Scheme: ecdsa\n├─ Expires: 12 days\n└─ Status: ✓ Valid"
    }],
    "structuredContent": {
      "detected": true,
      "child_id": "7a3f2c1b",
      "scheme": "ecdsa",
      "presigs_remaining": 847,
      "presigs_total": 1000,
      "days_until_expiry": 12,
      "is_valid": true
    }
  }
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI AGENT HOST                            │
│  (Claude Desktop, VS Code, Custom Agent)                    │
│                                                              │
│         ┌─────────────────┐                                 │
│         │   MCP CLIENT    │                                 │
│         └────────┬────────┘                                 │
└──────────────────┼──────────────────────────────────────────┘
                   │ stdio (JSON-RPC 2.0)
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                   SIGIL-MCP SERVER                           │
│                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │   TOOLS     │  │  RESOURCES  │  │   PROMPTS   │        │
│   │ • sign_evm  │  │ • disk://   │  │ • sign_*    │        │
│   │ • sign_frost│  │ • presigs://│  │ • troubl... │        │
│   └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│   ┌────────────────────────────────────────────────────┐    │
│   │              SIGIL CORE LAYER                       │    │
│   │   DiskState • ToolContext • Signing Logic          │    │
│   └────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## CLI Options

```
sigil-mcp [OPTIONS]

Options:
  -t, --transport <TRANSPORT>  Transport mechanism [default: stdio] [possible: stdio, http]
  -p, --port <PORT>           Port for HTTP transport [default: 3000]
  -v, --verbose               Enable verbose logging (to stderr)
      --mock                  Use mock disk state (for testing)
      --log-level <LEVEL>     Log level [default: info] [possible: trace, debug, info, warn, error]
  -h, --help                  Print help
  -V, --version               Print version
```

## Development

### Running Tests

```bash
cargo test -p sigil-mcp
```

### Testing with MCP Inspector

```bash
npx @anthropic/mcp-inspector /path/to/sigil-mcp --transport stdio
```

## Future Enhancements

- [ ] HTTP + SSE transport for web clients
- [ ] Direct integration with sigil-daemon
- [ ] Resource subscriptions for real-time disk updates
- [ ] Rate limiting and authentication
- [ ] Metrics and telemetry

## Reference

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Integration Plan](../../../documentation/MCP_INTEGRATION_PLAN.md)
