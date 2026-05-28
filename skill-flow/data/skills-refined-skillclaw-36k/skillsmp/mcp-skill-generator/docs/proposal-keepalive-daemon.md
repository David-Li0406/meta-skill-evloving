# Proposal: Keep-Alive Daemon for Stateful MCP Servers

**Status**: Proposed
**Created**: 2026-01-20
**Priority**: Medium

## Problem

Current `mcp-caller.mjs` spawns a new MCP server process for each call. For stateful servers like `chrome-devtools-mcp`, this means:

- Each call starts a new Chrome instance
- No continuity between operations
- Resource waste from repeated process startup/shutdown

## Reference

[steipete/mcporter](https://github.com/steipete/mcporter) implements a "Keep-Alive Daemon" that maintains persistent connections to stateful MCP servers.

## Proposed Solution

```
┌─────────────────┐    Unix Socket    ┌─────────────────┐    stdio    ┌─────────────────┐
│  mcp-caller.mjs │ ───────────────▶  │  mcp-daemon.mjs │ ─────────▶  │  MCP Server     │
│    (client)     │                   │    (daemon)     │              │  (Chrome etc)   │
└─────────────────┘                   └─────────────────┘              └─────────────────┘
```

### New Files

| File | Description |
|------|-------------|
| `scripts/mcp-daemon.mjs` | Daemon process maintaining MCP connection |

### Config Changes

```toml
# config.toml
transport = "stdio"
command = "npx"
args = ["chrome-devtools-mcp@0.13.0", "--isolated"]
daemon = true  # NEW: enable daemon mode
```

### New Commands

```bash
node mcp-caller.mjs daemon start   # Start daemon
node mcp-caller.mjs daemon stop    # Stop daemon
node mcp-caller.mjs daemon status  # Check status
node mcp-caller.mjs call ...       # Auto-routes through daemon if enabled
```

## Implementation Notes

- Socket file: `/tmp/mcp-daemon-{skill-name}.sock`
- Daemon auto-starts on first call if `daemon = true`
- Graceful shutdown on `daemon stop` or process exit
- Timeout/heartbeat to detect stale daemons

## Scope

- Only affects stateful MCP servers (chrome-devtools, puppeteer, etc.)
- No impact on stateless servers (filesystem, fetch, etc.)
- Backward compatible, daemon mode off by default

## Estimate

~200-300 lines of code
