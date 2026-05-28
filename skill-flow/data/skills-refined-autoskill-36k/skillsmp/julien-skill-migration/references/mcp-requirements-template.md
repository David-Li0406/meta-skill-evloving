# MCP-REQUIREMENTS.md Template

This template is used by `migrate-skill.py` to generate `MCP-REQUIREMENTS.md` when a skill has `.mcp.json`.

## Generated Structure

```markdown
# MCP Requirements for {skill-name}

This skill requires MCP (Model Context Protocol) servers to function.

## Servers Required

### {server-name}
- **Package**: `{package-name}`
- **Command**: `{command}`
- **Environment**: {env-vars} (if any)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VAR_NAME` | *Set before use* | Yes |

## Installation

Add to your project's `.mcp.json` or copy the existing `.mcp.json` from this skill:

```json
{
  "mcpServers": {
    "server-name": { ... }
  }
}
```

## Commands Needed

- `npx`: Requires Node.js (npm install -g npx)
- `uvx`: Requires uv (pip install uv)
```

## Common MCP Servers

| Server | Package | Purpose |
|--------|---------|---------|
| playwright | `@tontoko/fast-playwright-mcp` | Browser automation (token-optimized) |
| playwright | `@anthropic/playwright-mcp` | Browser automation (vanilla) |
| notion | `@anthropic/notion-mcp` | Notion API access |
| filesystem | `@anthropic/filesystem-mcp` | File system access |
| github | `@anthropic/github-mcp` | GitHub API access |

## Token Optimization Note

For Playwright specifically, prefer `@tontoko/fast-playwright-mcp` over vanilla:
- 70-90% token reduction
- Diff mode for DOM changes
- Targeted snapshots
- Batch execute support
