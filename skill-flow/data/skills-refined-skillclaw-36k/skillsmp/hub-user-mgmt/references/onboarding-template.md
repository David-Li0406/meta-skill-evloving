# Onboarding Message Template

Replace placeholders: `{{USER}}`, `{{USER_TITLE}}`, `{{TOOLS_LIST}}`, `{{TOOLS_EXCLUDED}}`, `{{HUB_URL}}`

## Template (Markdown)

```
# MCP Hub Access - {{USER}}

---

## IDE Access (Claude Code, Cursor)

**JWT Location:**
- Environment variable: `MCP_HUB_TOKEN`
- Or secure storage (1Password, etc.)

**Claude Code Setup** (`~/.claude.json`):
```json
"my-hub": {
  "type": "sse",
  "url": "{{HUB_URL}}/mcp/{{USER}}-sse",
  "headers": { "Authorization": "Bearer <JWT>" }
}
```

**Tip:** Give this message to an AI agent - it can set up the MCP client automatically.

---

## Available Tools

{{TOOLS_LIST}}
- _Not available:_ {{TOOLS_EXCLUDED}}

---

## Links
- Health: {{HUB_URL}}/mcp/{{USER}}-health
- Config: `clients/{{USER}}/`

_User: {{USER}}_
```

## Tool List Examples

**Admin (blacklist mode):**
```
- Notion, n8n Workflows
- Slack (messages, search)
- All meta tools (ping, list_tools)
```

**Standard User (whitelist mode):**
```
- n8n Workflows (list, execute)
- Meta tools (ping, list_tools)
```

**Minimal User:**
```
- Meta tools only (ping, list_tools)
```

## Excluded Tools Examples

- Admin: `None`
- User: `Notion, Agent Execute`
- Minimal: `Notion, n8n, Slack, Agent`
