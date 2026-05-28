---
name: julien-mcp-windows-manager
description: "Manage MCP servers on Windows. Add, remove, list MCPs with proper cmd /c wrapper. Handles both global (~/.claude.json) and project (.mcp.json) configs."
version: "1.0.0"
license: Apache-2.0
metadata:
  author: "Julien"
  category: "infrastructure"
triggers:
  # Keywords (removed generic "mcp" - causes false positives when mentioning any MCP server by name)
  - "mcp server config"
  - "mcp windows"
  - "mcp.json"
  - ".mcp.json"
  # Action phrases
  - "add mcp"
  - "ajouter mcp"
  - "remove mcp"
  - "supprimer mcp"
  - "install mcp"
  - "installer mcp"
  - "configure mcp"
  - "configurer mcp"
  - "list mcp"
  - "lister mcp"
  # Problem phrases
  - "mcp connection closed"
  - "mcp doesn't work"
  - "mcp ne marche pas"
  - "npx mcp error"
  - "cmd /c mcp"
---

# MCP Windows Manager

Manage MCP (Model Context Protocol) servers on Windows with proper configuration.

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-mcp-windows-manager" activated
```

## Windows Specificity

**Critical**: On Windows, npx commands require `cmd /c` wrapper:

```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "package-name@latest"]
}
```

Without this, you get "Connection closed" errors.

## Configuration Files

| Scope | File | Use Case |
|-------|------|----------|
| **Global** | `~/.claude.json` → `mcpServers` | MCPs available in ALL projects |
| **Project** | `.mcp.json` (project root) | MCPs specific to this project |

**Priority**: Project `.mcp.json` overrides global for same server name.

## Quick Commands

### List MCPs

```bash
node -e "
const fs = require('fs');
const os = require('os');
const global = JSON.parse(fs.readFileSync(os.homedir() + '/.claude.json', 'utf-8'));
console.log('=== Global MCPs ===');
Object.keys(global.mcpServers || {}).forEach(n => console.log('  •', n));
try {
  const project = JSON.parse(fs.readFileSync('.mcp.json', 'utf-8'));
  console.log('=== Project MCPs ===');
  Object.keys(project.mcpServers || {}).forEach(n => console.log('  •', n));
} catch {}
"
```

### Add MCP (Global)

Use the script:
```bash
node ~/.claude/scripts/mcp-manager.js add <name> <npm-package>
```

Or manually edit `~/.claude.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@scope/package@latest"]
    }
  }
}
```

### Add MCP (Project)

Create/edit `.mcp.json` in project root:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "my-mcp-server@latest"]
    }
  }
}
```

### Remove MCP

```bash
node ~/.claude/scripts/mcp-manager.js remove <name> [--global|--project]
```

## Common MCP Configurations

### NPX-based (most common)
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:/path"]
}
```

### Python-based
```json
{
  "command": "python",
  "args": ["-m", "my_mcp_server"],
  "cwd": "C:/path/to/project",
  "env": { "PYTHONUNBUFFERED": "1" }
}
```

### Node direct
```json
{
  "command": "node",
  "args": ["C:/path/to/server/index.js"],
  "env": { "API_KEY": "..." }
}
```

### With reloaderoo (hot-reload)
```json
{
  "command": "reloaderoo",
  "args": ["proxy", "--", "node", "C:/path/to/index.js"]
}
```

## Troubleshooting

### "Connection closed" error
**Cause**: Missing `cmd /c` wrapper on Windows
**Fix**: Change `"command": "npx"` to `"command": "cmd"` with `"args": ["/c", "npx", ...]`

### MCP not loading
1. Check JSON syntax: `node -e "JSON.parse(require('fs').readFileSync('.mcp.json'))"`
2. Restart Claude Code after changes
3. Check MCP logs: `/mcp` command in Claude Code

### Environment variables not working
Use `env` field in config:
```json
{
  "command": "...",
  "args": [...],
  "env": {
    "API_KEY": "your-key",
    "DEBUG": "true"
  }
}
```

## CLI Alternative

Claude Code CLI also supports adding MCPs:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

## Skill Chaining

### Skills Required Before
- None

### Input Expected
- MCP server name
- NPM package name (for add)
- Scope: global or project

### Output Produced
- Updated config file
- Confirmation message

### Compatible Skills After
- Restart Claude Code to load new MCP

### Tools Used
- `Bash` (run node scripts, edit JSON)

## Sources

- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
- [Windows MCP Guide](https://github.com/BunPrinceton/claude-mcp-windows-guide)
- [Issue #9594](https://github.com/anthropics/claude-code/issues/9594) - Windows npx wrapper
