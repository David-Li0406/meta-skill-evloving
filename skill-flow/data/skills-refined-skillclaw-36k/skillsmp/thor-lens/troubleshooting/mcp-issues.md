# MCP Issues

Troubleshooting MCP (Model Context Protocol) connection problems with Claude Code.

## Quick Diagnosis

### Check Server is Running

For HTTP mode:
```bash
curl http://localhost:8080/api/meta | jq .
```

For stdio mode: The server only runs when Claude Code spawns it.

### Check MCP Config Syntax

```bash
cat .mcp.json | jq .
# Should parse without error
```

## Stdio Mode Issues

### Claude Code Shows No Tools

**Cause 1: Config not loaded**

- Restart Claude Code after adding `.mcp.json`
- Check file is in project root or `~/.claude.json`

**Cause 2: Binary path is wrong**

```json
{
  "mcpServers": {
    "thor-lens": {
      "command": "/absolute/path/to/thorlens",
      "args": ["serve", "--case", "/absolute/path/to/cases/mycase", "--mcp-stdio"]
    }
  }
}
```

Use absolute paths, not relative.

**Cause 3: Binary not executable**

```bash
chmod +x /path/to/thorlens
```

**Cause 4: Case doesn't exist**

```bash
ls -la /path/to/cases/mycase/
# Must contain meta.json and events/
```

### "spawn ENOENT" or Similar Error

Binary not found. Verify:

```bash
# Binary exists
ls -la /path/to/thorlens

# Binary is executable
file /path/to/thorlens

# Binary runs
/path/to/thorlens --version
```

### Tools Show But Don't Work

**Cause: Case is empty or invalid**

```bash
cat /path/to/cases/mycase/meta.json | jq '.event_count'
# Should be > 0
```

## HTTP Mode Issues

### Can't Connect

**Check server is running:**
```bash
curl http://localhost:8080/api/meta
```

**Check port matches config:**
```json
{
  "mcpServers": {
    "thor-lens": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**Check endpoint is correct:**
- Use `/mcp` not `/mcp/sse`
- Include the `/mcp` path

### Connection Refused

1. Server not running
2. Wrong port
3. Firewall blocking connection
4. Server crashed

Check server output for errors.

### Timeout Errors

**Large case causing slow queries:**
- Consider using stdio mode instead
- Check if case has too many events

## Configuration Examples

### Correct Stdio Config

```json
{
  "mcpServers": {
    "thor-lens": {
      "command": "/home/user/thor-lens/thorlens",
      "args": ["serve", "--case", "/home/user/cases/demo", "--mcp-stdio"]
    }
  }
}
```

### Correct HTTP Config

```json
{
  "mcpServers": {
    "thor-lens": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

### Common Config Mistakes

**Wrong: Relative paths**
```json
"command": "./thorlens"  // BAD
"command": "/full/path/to/thorlens"  // GOOD
```

**Wrong: Missing --mcp-stdio**
```json
"args": ["serve", "--case", "./cases/demo"]  // BAD - no MCP
"args": ["serve", "--case", "./cases/demo", "--mcp-stdio"]  // GOOD
```

**Wrong: Using /mcp/sse for HTTP transport**
```json
"url": "http://localhost:8080/mcp/sse"  // BAD
"url": "http://localhost:8080/mcp"  // GOOD
```

## Debugging Steps

### 1. Test Binary Directly

```bash
# Should show help or run
/path/to/thorlens --help

# Should start MCP server
/path/to/thorlens serve --case /path/to/case --mcp-stdio
# Press Ctrl+C to exit
```

### 2. Test Case Validity

```bash
ls -la /path/to/cases/mycase/
cat /path/to/cases/mycase/meta.json | jq .
```

### 3. Check Claude Code Logs

Look for MCP-related errors in Claude Code's debug output.

### 4. Simplify Config

Remove other MCP servers temporarily to isolate the issue:

```json
{
  "mcpServers": {
    "thor-lens": {
      "command": "/path/to/thorlens",
      "args": ["serve", "--case", "/path/to/cases/demo", "--mcp-stdio"]
    }
  }
}
```

## Security Notes

**Never expose MCP HTTP endpoint publicly:**
- MCP has no authentication
- Anyone with access can read case data
- Anyone with access can modify annotations

**For local use only:**
- Bind to 127.0.0.1 (default)
- Use firewall to block external access
- Prefer stdio mode when possible
