---
name: hub-customize
description: Interactive fork setup wizard for MCP Hub Boilerplate. Use when users want to customize, rebrand, configure services, or set up the hub for their company.
---

# Hub Customize

Interactive fork setup wizard for MCP Hub Boilerplate.

## References

**IMPORTANT:** Before running this wizard, review the documentation:

| Doc | Purpose |
|-----|---------|
| `docs/CUSTOMIZATION.md` | Main customization guide |
| `docs/DNS_SETUP.md` | Domain and HTTPS setup |
| `docs/OAUTH_SETUP.md` | OAuth for cloud clients |
| `docs/N8N_SETUP.md` | n8n integration |

See `references/docs-index.md` for full documentation map.

## Trigger

User asks to:
- Customize or rebrand the hub
- Set up for their company
- Configure services
- Fork and personalize

## Instructions

### 1. Gather Information

Ask the user about their setup:

**Company Name** (required)
- Used for: JWT issuer, branding, file names
- Format: lowercase-with-hyphens for technical names
- Example: "Acme Corp" → `acme-corp`

**Domain** (required for production)
- Used for: HUB_PUBLIC_URL, OAuth callbacks, Caddy config
- Example: `hub.acme-corp.com`

**Services to Enable** (optional)
- Notion integration: Yes/No (requires NOTION_TOKEN)
- Agent Worker: Yes/No (requires ANTHROPIC_API_KEY_LIMITED)
- Dashboard: Yes/No
- OAuth (Scalekit): Yes/No (for cloud clients)

### 2. Generate Configuration

Based on answers, generate:

#### .env file

```bash
NODE_ENV=production
PORT=8080

JWT_SECRET=<generate-random-64-char>
JWT_ALG=HS256
JWT_ISSUER={company-name}-hub
JWT_AUDIENCE=mcp-clients

NOTION_ENABLED={yes/no}
AGENT_WORKER_ENABLED={yes/no}
DASHBOARD_ENABLED={yes/no}

HUB_PUBLIC_URL=https://{domain}
```

#### User Naming Recommendation

Ask: "Do you want to keep the Götterboten names (hermes, iris, etc.) or use a different scheme?"

Options:
1. Keep existing (recommended for quick start)
2. Rename to team members
3. Use generic (user1, user2, etc.)

### 3. Apply Changes

Guide user through:

1. **Update .env**
   - Show diff of changes
   - Ask for confirmation

2. **Rename files (if requested)**
   - Provide sed commands for bulk rename
   - Update config.json files

3. **Update documentation**
   - README.md title and description
   - CLAUDE.md project context

4. **Generate tokens**
   - Run generate-token.js for primary admin user

### 4. Verification

After changes:

1. Restart hub: `docker compose restart hub`
2. Check health: `curl http://localhost:8080/health`
3. Test connection with new token
4. Verify OAuth discovery (if enabled)

### 5. Next Steps Checklist

Provide personalized checklist:

- [ ] Set JWT_SECRET to secure value
- [ ] Configure domain DNS (see DNS_SETUP.md)
- [ ] Set up HTTPS with Caddy
- [ ] Add Notion token (if using)
- [ ] Add Anthropic API key (if using Agent Worker)
- [ ] Configure Scalekit (if using OAuth)
- [ ] Test IDE connection
- [ ] Document custom configurations

## Tools Available

- Read (for reading current config)
- Write (for updating config files)
- Bash (for running commands)

## Example Flow

```
User: I want to set up this hub for my company

AI: Great! Let me help you customize the MCP Hub. I'll need a few details:

1. What's your company name?
   (This will be used for branding and the JWT issuer)

User: Acme Corp

AI: Perfect! And what domain will you use for the hub?

User: hub.acme.com

AI: Got it. Which services do you want to enable?
   - [ ] Notion integration (requires API token)
   - [ ] Agent Worker (requires Anthropic API key)
   - [ ] Dashboard (health monitoring UI)
   - [ ] OAuth (for Claude.ai/ChatGPT access)

User: Notion and Dashboard

AI: Here's your configuration:
[Shows generated .env]

Want me to apply these changes? I'll:
1. Update .env with these settings
2. Generate a secure JWT_SECRET
3. Create a token for your admin user

User: Yes, apply them

AI: [Makes changes]
Done! Here's your admin token: [token]

Next steps:
1. Point hub.acme.com to your server
2. Set up Caddy for HTTPS (see docs/DNS_SETUP.md)
3. Add your Notion token when ready
4. Restart with: docker compose restart hub
```

## Notes

- Always confirm before making changes
- Generate cryptographically secure JWT_SECRET
- Warn about production security requirements
- Keep backup of original .env before changes
