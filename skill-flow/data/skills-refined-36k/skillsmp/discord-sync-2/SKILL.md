---
name: discord-sync
description: "Smart Discord sync - automatically detects tokens and permissions to choose the optimal sync method. Use when user asks to sync Discord messages."
---

# Discord Sync (Smart Router)

Automatically detects available tokens and bot permissions to route to the optimal sync connector.

## When to Use

- User asks to "sync Discord messages"
- User asks to "pull messages from Discord"
- User wants to "get Discord history"
- User wants to "update Discord data"
- User wants to "download Discord messages"
- User asks to "fetch messages from #channel"

## How It Works

This skill runs a preflight check before syncing:

1. **Token Detection** - Checks which tokens are configured in `.env`
2. **Token Validation** - Verifies tokens are valid by calling Discord API
3. **Permission Check** - For bot token, verifies server access and required permissions
4. **Smart Routing** - Recommends the optimal connector based on results

## Routing Logic

| Scenario | Connector Used | Reason |
|----------|----------------|--------|
| Syncing DMs | `discord-user-connector` | Bots cannot access DMs |
| Bot token valid + has permissions | `discord-bot-connector` | Faster, higher rate limits |
| Bot token valid but lacks permissions | `discord-user-connector` | Fallback |
| Only user token available | `discord-user-connector` | Only option |
| Only bot token available | `discord-bot-connector` | Only option (no DMs) |
| No valid tokens | Error | Configuration needed |

## How to Execute

### Step 1: Run Preflight Check

```bash
# Check for specific server
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_preflight.py --server SERVER_ID

# Check for DM sync
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_preflight.py --dms

# JSON output for programmatic use
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_preflight.py --server SERVER_ID --json
```

### Step 2: Route Based on Result

The preflight check returns a recommendation. Execute the recommended skill:

**If recommendation is `discord-bot-connector:discord-sync`:**
```
Skill(skill: "discord-bot-connector:discord-sync")
```

**If recommendation is `discord-user-connector:discord-sync`:**
```
Skill(skill: "discord-user-connector:discord-sync")
```

## Example Preflight Output

```
==================================================
Discord Sync Preflight Check
==================================================

Token Status:
  User Token: valid
  Bot Token:  valid

Bot Permissions:
  Server: My Community Server
  Has Access: Yes
  View Channels: Yes
  Read History: Yes

Recommendation:
  Use: discord-bot-connector:discord-sync
  Reason: Bot has access to My Community Server with required permissions (faster sync)
```

## Preflight JSON Output

```json
{
  "user_token": {"configured": true, "valid": true, "error": null},
  "bot_token": {"configured": true, "valid": true, "error": null},
  "bot_permissions": {
    "server_id": "123456789",
    "server_name": "My Community Server",
    "has_access": true,
    "can_view_channels": true,
    "can_read_history": true,
    "error": null
  },
  "wants_dms": false,
  "recommendation": "discord-bot-connector:discord-sync",
  "reason": "Bot has access to My Community Server with required permissions (faster sync)"
}
```

## Smart Defaults

When user is vague, use these defaults:

| User Says | Action |
|-----------|--------|
| "sync discord" | Run preflight with default server from config |
| "sync my DMs" | Run preflight with `--dms` flag |
| "sync [server name]" | Find server ID, run preflight, then sync |

## Prerequisites

- `.env` file with at least one Discord token:
  - `DISCORD_USER_TOKEN` - For user token sync (servers + DMs)
  - `DISCORD_BOT_TOKEN` - For bot token sync (servers only, faster)
- `aiohttp` library installed for API calls

## Connector Comparison

| Feature | Bot Connector | User Connector |
|---------|---------------|----------------|
| Rate Limits | Higher (official API) | Lower |
| Server Messages | Yes | Yes |
| DM Access | No | Yes |
| Rich Profiles | No | Yes |
| ToS Compliant | Yes | Gray area |

## Troubleshooting

**Bot token valid but "lacks permissions":**
- Ensure bot has "Read Message History" permission in Discord
- Check if bot role is above restricted channels
- Try re-inviting bot with correct permissions

**User token invalid:**
- Token may have expired - get a new one
- Ensure token is copied correctly (no extra spaces)

**No tokens configured:**
- Create `.env` file in project root
- Add `DISCORD_USER_TOKEN=your_token` or `DISCORD_BOT_TOKEN=your_token`
