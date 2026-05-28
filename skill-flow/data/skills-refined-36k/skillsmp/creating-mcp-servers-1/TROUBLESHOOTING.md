# MCP Server Troubleshooting

Common issues and solutions when working with MCP servers in Claude Code.

## Quick Diagnostics

```bash
# Check server status in Claude Code
/mcp

# List configured servers
claude mcp list

# Get server details
claude mcp get <name>

# Run Claude with debug logging
claude --debug
```

## Server Not Connecting

### Symptoms
- `/mcp` shows server as disconnected
- "Connection refused" or "Connection closed" errors
- Server not appearing in tool list

### Solutions

#### HTTP/SSE Servers

1. **Verify URL is correct**
   ```bash
   # Test endpoint manually
   curl -I https://mcp.example.com/mcp
   ```

2. **Check HTTPS certificate**
   ```bash
   # SSL certificate issues
   curl -v https://mcp.example.com/mcp 2>&1 | grep -i ssl
   ```

3. **Firewall/network issues**
   - Check if URL is accessible from your machine
   - VPN may block certain endpoints
   - Corporate firewalls may require proxy

4. **CORS issues (browser-based)**
   - Server must return proper CORS headers
   - Check browser console for CORS errors

#### stdio Servers

1. **Command not found**
   ```bash
   # Verify command exists
   which npx
   which node
   which python

   # Use absolute paths
   claude mcp add --transport stdio myserver -- /usr/local/bin/node /path/to/server.js
   ```

2. **Permission denied**
   ```bash
   # Make script executable
   chmod +x /path/to/server.js

   # Check file permissions
   ls -la /path/to/server.js
   ```

3. **Windows npx issues**
   ```bash
   # WRONG: Direct npx on Windows
   claude mcp add --transport stdio myserver -- npx -y package

   # CORRECT: Use cmd wrapper
   claude mcp add --transport stdio myserver -- cmd /c npx -y package
   ```

4. **Server crashes immediately**
   ```bash
   # Test manually
   npx -y @your/package

   # Check for missing dependencies
   npm list

   # Check for environment variables
   env | grep REQUIRED_VAR
   ```

### Timeout Issues

1. **Increase timeout**
   ```bash
   # 30 second timeout
   MCP_TIMEOUT=30000 claude

   # 60 second timeout for slow servers
   MCP_TIMEOUT=60000 claude
   ```

2. **Check server startup time**
   - Some servers need time to initialize
   - Database connections may delay startup
   - First-time npm package downloads

## OAuth Flow Problems

### Symptoms
- Browser doesn't open for authentication
- "Authentication required" persists after login
- Token refresh failures

### Solutions

1. **Browser doesn't open**
   ```bash
   # Copy URL manually from /mcp output
   # Paste in browser
   ```

2. **Stuck authentication**
   ```bash
   # Clear authentication and retry
   /mcp
   # Select server > Clear authentication
   # Then re-authenticate
   ```

3. **Token expired**
   - Most OAuth tokens auto-refresh
   - If issues persist, clear and re-authenticate

4. **Wrong OAuth redirect**
   - Check callback URL configuration in OAuth provider
   - Localhost callbacks may need specific ports

## Tools Not Appearing

### Symptoms
- Server connected but no tools visible
- Can't call MCP tools
- `/mcp` shows connection but tools count is 0

### Solutions

1. **Restart Claude Code**
   ```bash
   # Exit and restart
   exit
   claude
   ```

2. **Check tool listing**
   ```bash
   # In debug mode, look for tool list
   claude --debug
   # Search for "ListTools" in output
   ```

3. **Server capabilities**
   - Server must declare `tools` capability
   - Check server implementation

4. **list_changed not handled**
   - Claude Code 2.1.0+ supports `list_changed`
   - Older versions need restart for tool changes

5. **Permission issues**
   - Check if tools are blocked by permissions
   - `/permissions` to view current settings

## Permission Errors

### Symptoms
- "Permission denied" when calling tools
- Tools blocked by policy
- Cannot add certain servers

### Solutions

1. **Check permissions**
   ```bash
   /permissions
   ```

2. **Allow specific MCP tools**
   ```json
   // settings.json
   {
     "permissions": {
       "allow": ["mcp__myserver__*"]
     }
   }
   ```

3. **Enterprise restrictions**
   - Check `managed-mcp.json` if exists
   - Contact IT for allowed servers list
   - Server may need to be on allowlist

4. **Project scope approval**
   ```bash
   # Reset project MCP approvals
   claude mcp reset-project-choices
   ```

## Output Too Large

### Symptoms
- "Output exceeds limit" warnings
- Truncated responses from MCP tools
- Memory issues

### Solutions

1. **Increase output limit**
   ```bash
   MAX_MCP_OUTPUT_TOKENS=50000 claude
   ```

2. **Paginate in server**
   - Implement pagination in your MCP server
   - Return summary instead of full data
   - Offer "get more" tool

3. **Filter data**
   - Add filtering parameters to tools
   - Return only necessary fields

## Configuration Issues

### Symptoms
- Server config not loading
- Wrong scope applied
- Environment variables not working

### Solutions

1. **Check config location**
   ```bash
   # View where configs are stored
   cat ~/.claude.json | grep -A 20 mcpServers
   cat .mcp.json
   ```

2. **Scope precedence** (highest to lowest)
   - Local (`~/.claude.json` under project path)
   - Project (`.mcp.json`)
   - User (`~/.claude.json`)

3. **Environment variable expansion**
   ```json
   // Environment vars only expand in .mcp.json
   {
     "mcpServers": {
       "server": {
         "type": "http",
         "url": "${BASE_URL}/mcp",
         "headers": {
           "Authorization": "Bearer ${TOKEN}"
         }
       }
     }
   }
   ```

   Set variables before running:
   ```bash
   export BASE_URL=https://api.example.com
   export TOKEN=your-token
   claude
   ```

4. **JSON syntax errors**
   ```bash
   # Validate JSON
   cat .mcp.json | python -m json.tool
   ```

## Server Development Issues

### Server Doesn't Receive Requests

1. **Check stdin/stdout**
   ```typescript
   // Log to stderr, not stdout
   console.error("Debug message");  // Correct
   console.log("Debug message");    // Wrong - interferes with MCP
   ```

2. **JSON-RPC format**
   ```bash
   # Test manually
   echo '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}' | node server.js
   ```

3. **Proper initialization**
   ```typescript
   // Must respond to initialize request
   server.setRequestHandler(InitializeRequestSchema, async () => {
     return {
       protocolVersion: "2024-11-05",
       capabilities: { tools: {} },
       serverInfo: { name: "server", version: "1.0.0" }
     };
   });
   ```

### Resources Not Loading

1. **Capability declaration**
   ```typescript
   // Must declare resources capability
   new Server(info, { capabilities: { resources: {} } });
   ```

2. **URI format**
   ```typescript
   // Resources need valid URIs
   {
     uri: "myscheme://path/to/resource",
     name: "Resource Name",
     mimeType: "application/json"
   }
   ```

### Prompts Not Working

1. **Capability declaration**
   ```typescript
   // Must declare prompts capability
   new Server(info, { capabilities: { prompts: {} } });
   ```

2. **Argument handling**
   ```typescript
   // Arguments are optional
   server.setRequestHandler(GetPromptRequestSchema, async (request) => {
     const args = request.params.arguments || {};
     // Handle missing arguments gracefully
   });
   ```

## Debug Logging

### Enable Detailed Logging

```bash
# Claude Code debug mode
claude --debug

# MCP SDK debug (for your server)
DEBUG=mcp* node server.js

# Combined
DEBUG=mcp* claude --debug
```

### Log Locations

- Claude Code logs: Check terminal output with `--debug`
- Server logs: `console.error()` output (stderr)
- System logs: `/var/log/` or Event Viewer (Windows)

### What to Look For

1. **Connection lifecycle**
   - "Connecting to MCP server..."
   - "MCP server connected"
   - "MCP server disconnected"

2. **Tool calls**
   - Request: `{"method": "tools/call", ...}`
   - Response: `{"result": {...}}`

3. **Errors**
   - Stack traces
   - Error codes
   - "Connection closed" reasons

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Connection refused" | Server not running or wrong port | Verify URL/command |
| "Connection closed" | Server crashed or invalid protocol | Check server logs |
| "Timeout" | Slow startup or network | Increase MCP_TIMEOUT |
| "Permission denied" | Policy or file permissions | Check permissions |
| "Unknown tool" | Tool not registered | Check server capabilities |
| "Parse error" | Invalid JSON | Check stdin/stdout handling |
| "Method not found" | Missing handler | Implement required methods |

## Getting Help

1. **Check documentation**
   - [MCP Protocol](https://modelcontextprotocol.io/)
   - [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)

2. **Debug systematically**
   - Test server manually first
   - Add logging to server
   - Check each component separately

3. **Report bugs**
   - Use `/bug` in Claude Code
   - Include debug output
   - Include server version and configuration

## Checklist: Server Not Working

- [ ] URL/command is correct
- [ ] Server runs manually (`node server.js`)
- [ ] Network is accessible (for HTTP/SSE)
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Permissions allow server/tools
- [ ] JSON config is valid
- [ ] Claude Code restarted after changes
- [ ] Timeout is sufficient
