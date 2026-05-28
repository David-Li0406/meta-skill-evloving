---
name: cursor-logs
description: Finding Cursor Logs
disable-model-invocation: true
---
# Finding Cursor Logs

Quick reference for locating Cursor logs and debugging issues.

## Main Log Location

Cursor stores logs in `~/.config/Cursor/logs/` with timestamped directories:
```
~/.config/Cursor/logs/{YYYYMMDDTHHMMSS}/window{N}/exthost/{extension-id}/
```

## Finding Logs

### Most Recent Logs
```bash
# Find most recent log directory
ls -lt ~/.config/Cursor/logs/ | head -5

# Find most recent MCP logs
ls -lt ~/.config/Cursor/logs/*/window*/exthost/anysphere.cursor-mcp/ | head -10
```

### MCP Logs
MCP logs follow the pattern: `MCP {server-name}.log`

```bash
# Find specific MCP server log (e.g., postgres)
find ~/.config/Cursor/logs -name "*MCP*postgres*.log" | sort -r | head -1

# Find all MCP logs
find ~/.config/Cursor/logs -path "*/anysphere.cursor-mcp/*.log"
```

### Extension Logs
```bash
# Find logs for a specific extension
find ~/.config/Cursor/logs -path "*/{extension-id}/*.log"

# Example: Prisma extension logs
find ~/.config/Cursor/logs -path "*/prisma.prisma*/*.log"
```

## MCP Server Directories

MCP server configurations and tool definitions are in:
```
~/.cursor/projects/{project-path}/mcps/{server-name}/
```

Example:
```
~/.cursor/projects/home-flesler-Code-vetbrain/mcps/project-0-vetbrain-postgres/
```

## Quick Debugging Commands

```bash
# View most recent MCP log
tail -f $(ls -t ~/.config/Cursor/logs/*/window*/exthost/anysphere.cursor-mcp/*.log | head -1)

# Search for errors in MCP logs
grep -i error ~/.config/Cursor/logs/*/window*/exthost/anysphere.cursor-mcp/*.log

# Find logs containing specific text
grep -r "postgres" ~/.config/Cursor/logs/*/window*/exthost/anysphere.cursor-mcp/

# Check MCP server status from logs
grep -i "successfully connected\|error\|failed" ~/.config/Cursor/logs/*/window*/exthost/anysphere.cursor-mcp/MCP\ project-0-vetbrain-postgres.log | tail -20
```

## Common Log Types

- **MCP Logs**: `anysphere.cursor-mcp/MCP {server-name}.log`
- **Extension Logs**: `{extension-id}/{Extension Name}.log`
- **Agent Logs**: `anysphere.cursor-agent-exec/Cursor Agent Exec.log`
- **Retrieval Logs**: `anysphere.cursor-retrieval/Cursor {Service}.log`

## Notes

- Cursor runs as an AppImage, so logs follow XDG config standards
- Log directories are timestamped: `YYYYMMDDTHHMMSS` format
- Multiple windows create separate log directories (`window1`, `window2`, etc.)
- MCP servers log to `anysphere.cursor-mcp/` directory
- Logs are rotated/archived over time, check timestamps for most recent
