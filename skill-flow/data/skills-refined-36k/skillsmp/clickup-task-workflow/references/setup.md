# ClickUp Integration Setup

This guide walks through obtaining credentials for the ClickUp MCP integration.

## Prerequisites

The task plugin uses the ClickUp HTTP MCP server at `https://mcp.clickup.com/mcp`. Authentication is handled via OAuth when you first use the MCP tools.

## Quick Start

1. **Install the plugin** - Add to your project's `.claude/settings.json`
2. **Use any /task command** - OAuth flow will prompt for ClickUp login
3. **Authorize access** - Grant Claude Code access to your ClickUp workspace

That's it - the HTTP MCP server handles authentication automatically.

## Manual API Setup (Alternative)

If you prefer environment variable authentication:

### Step 1: Generate API Token

1. Open ClickUp → Avatar → **Settings**
2. Navigate to **Apps** in sidebar
3. Scroll to **API Token** → Click **Generate**
4. Copy the token (starts with `pk_`)

### Step 2: Find Team ID

From any ClickUp URL: `https://app.clickup.com/{team_id}/...`

Or via API:
```bash
curl -s "https://api.clickup.com/api/v2/team" \
  -H "Authorization: pk_YOUR_TOKEN" | jq '.teams[0].id'
```

### Step 3: Set Environment Variables

**Fish:**
```fish
set -Ux CLICKUP_API_TOKEN "pk_..."
set -Ux CLICKUP_TEAM_ID "..."
```

**Bash/Zsh:**
```bash
export CLICKUP_API_TOKEN="pk_..."
export CLICKUP_TEAM_ID="..."
```

## Troubleshooting

### OAuth flow not appearing
- Restart Claude Code
- Check `.mcp.json` includes the clickup server

### "Invalid API token"
- Ensure token starts with `pk_`
- Check for trailing whitespace
- Try regenerating in ClickUp settings

### Rate limiting
- ClickUp API: 100 requests/minute (free plans)
- The subagent pattern minimizes API calls

## Security

1. **Never commit tokens** - Add `.env*` to `.gitignore`
2. **Use OAuth when possible** - More secure than API tokens
3. **Rotate tokens periodically**
