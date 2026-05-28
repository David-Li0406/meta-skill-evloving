# Deprecated Patterns and Migration Guide

Old MCP patterns and how to migrate to current approaches.

## Transport Deprecation: SSE

### Current Status

**SSE Transport:** Deprecated
**Recommended:** HTTP transport

### Why HTTP Over SSE

HTTP is:
- Better supported across cloud environments
- More reliable for remote servers
- Simpler to configure and debug
- Preferred by Anthropic and ecosystem

SSE:
- Worked for streaming responses
- Limited cloud support
- Being phased out

### Migration: SSE → HTTP

**Old Configuration (SSE - Deprecated):**
```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse \
  --header "Authorization: Bearer token"
```

**New Configuration (HTTP - Recommended):**
```bash
claude mcp add --transport http asana https://mcp.asana.com/http \
  --header "Authorization: Bearer token"
```

**Key Difference:**
- `--transport sse` → `--transport http`
- SSE URL (ends in `/sse`) → HTTP URL (ends in `/http` or just `/mcp`)
- Everything else identical

### In .mcp.json

**Old (SSE):**
```json
{
  "mcpServers": {
    "asana": {
      "type": "sse",
      "url": "https://mcp.asana.com/sse",
      "headers": {
        "Authorization": "Bearer token"
      }
    }
  }
}
```

**New (HTTP):**
```json
{
  "mcpServers": {
    "asana": {
      "type": "http",
      "url": "https://mcp.asana.com/http",
      "headers": {
        "Authorization": "Bearer token"
      }
    }
  }
}
```

## API Deprecation: mcp-client-2025-04-04

### Current Status

**Beta Header:** `mcp-client-2025-04-04`
**Status:** Deprecated (still works but will be removed)

**Latest Version:** `mcp-client-2025-11-20`
**Status:** Current standard

### What Changed

Tool configuration moved from server definition to separate toolset:

**Old Format (mcp-client-2025-04-04 - Deprecated):**
```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example.com/sse",
      "name": "example",
      "tool_configuration": {
        "enabled": true,
        "allowed_tools": ["tool1", "tool2"]
      }
    }
  ]
}
```

**New Format (mcp-client-2025-11-20 - Current):**
```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example.com/sse",
      "name": "example"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "example",
      "default_config": {
        "enabled": false
      },
      "configs": {
        "tool1": {"enabled": true},
        "tool2": {"enabled": true}
      }
    }
  ]
}
```

### Migration Steps

1. **Move to new beta header:**
   ```python
   betas=["mcp-client-2025-11-20"]
   ```

2. **Separate server from tool config:**
   - Server definition: just `type`, `url`, `name`, `authorization_token`
   - Tool config: new `tools` array with `mcp_toolset` objects

3. **Update tool configuration patterns:**
   - `allowed_tools` → `default_config.enabled: false` + `configs` for specific tools
   - `enabled: false` → `default_config.enabled: false`
   - See mcp-connector-api.md for full patterns

### Deprecation Timeline

- **mcp-client-2025-04-04**: Deprecated (still functional)
- **mcp-client-2025-11-20**: Current standard
- **Future**: Deprecated version will be removed

**Action:** Migrate to `mcp-client-2025-11-20` for new code

## Port and Encoding Defaults (Python SDK)

### Deprecated SDK Behavior

Older MCP Python SDK versions:
- Default port: Sometimes assumed 8080
- Encoding: Required explicit specification
- Runtime detection: Limited

### Current Best Practices

**Port Handling:**
```python
# Specify port explicitly
server = Server(host="localhost", port=8000)

# Or use environment variable
port = os.getenv("MCP_PORT", "8000")
server = Server(host="localhost", port=port)
```

**Encoding:**
```python
# Be explicit about UTF-8
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Configuration File Format

### Old .claude File Format

**Deprecated:** Custom `.claude` configuration file
**Replace with:** `.mcp.json` (standard format)

**Old pattern:**
```
# .claude (custom format - avoid)
[servers]
github=https://api.githubcopilot.com/mcp
```

**New pattern:**
```json
# .mcp.json (standard format)
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp"
    }
  }
}
```

## CLI Changes

### Old MCP Commands (Pre-v1.5)

Some older Claude Code versions used different CLI syntax.

**Old:**
```bash
claude mcp config add github https://api.githubcopilot.com/mcp
```

**Current:**
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp
```

**Key changes:**
- `config add` → `add`
- `--transport` flag required
- Explicit transport type (http, sse, stdio)

## Migration Checklist

### Transport Migration

- [ ] Inventory all SSE servers currently configured
- [ ] Check if HTTP endpoint available (usually same URL, `/sse` → `/http`)
- [ ] Update CLI commands or .mcp.json with HTTP transport
- [ ] Test connectivity to servers
- [ ] Remove SSE configurations once verified

### API Version Migration

- [ ] Update beta header to `mcp-client-2025-11-20`
- [ ] Review tool configuration patterns
- [ ] Migrate from `tool_configuration` to separate `tools` array
- [ ] Update MCPToolset patterns (see mcp-connector-api.md)
- [ ] Test with new beta version
- [ ] Remove deprecated code

### Configuration Format Migration

- [ ] Replace `.claude` files with `.mcp.json`
- [ ] Ensure `.mcp.json` in correct location (project root or `~/.claude`)
- [ ] Validate JSON syntax
- [ ] Test configuration loading

## Timeline and Support

**Current Support:**
- All current features on `mcp-client-2025-11-20` and latest SDK
- Limited support for deprecated patterns
- Bug fixes only for critical issues

**Deprecation Notice:**
- Deprecated patterns documented here for reference
- New code should use current standards
- Migration guides provided for all changes

## When You Encounter Old Code

If you find MCP configuration using deprecated patterns:

1. **Check age:** Might be from older projects
2. **Test first:** Still works if using compatible Claude Code version
3. **Plan migration:** Schedule update to current format
4. **Use this guide:** Reference migration steps above
5. **Update docs:** Help others by noting what changed

## Questions About Deprecation

If unclear about migrating:
1. Check mcp-connector-api.md for current patterns
2. Review examples in documentation
3. Test with current beta header first
4. Ask for documentation - I can fetch latest details
