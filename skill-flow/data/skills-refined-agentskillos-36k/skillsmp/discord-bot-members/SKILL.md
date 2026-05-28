---
name: discord-bot-members
description: "Sync Discord server members. Use when user asks to sync members, get member list, or fetch all members from Discord. Fetches complete member lists (100k+)."
---

# Discord Bot Members

Syncs complete Discord server member lists using bot token via HTTP API.
Optimized for large servers (100k+ members).

**Works alongside discord.py-self** - Uses direct HTTP API calls, no library conflicts.

## When to Use

- User asks to "sync members with bot token"
- User needs "fast member sync" for large servers
- User wants complete member lists (not just cached members)
- User has a bot token and needs official API compliance

## Prerequisites

- Bot token in `.env` as `DISCORD_BOT_TOKEN`
- Bot added to server with proper permissions
- SERVER MEMBERS INTENT enabled in Discord Developer Portal
- Python 3.11+ with `aiohttp` and `pyyaml` installed

**Note:** This plugin uses direct HTTP API calls via aiohttp. It works even when `discord.py-self` is installed (no namespace conflicts).

## How to Execute

### List servers the bot can access:

```bash
python {{PLUGIN_DIR}}/tools/member_sync.py --list
```

### Sync members from a server:

```bash
python {{PLUGIN_DIR}}/tools/member_sync.py --server SERVER_ID
```

### Include bot accounts:

```bash
python {{PLUGIN_DIR}}/tools/member_sync.py --server SERVER_ID --include-bots
```

## Output Location

All paths are relative to cwd (current working directory). Uses unified path shared with user-connector:

```
data/discord/servers/{server_id}-{slug}/members/current.yaml
data/discord/servers/{server_id}-{slug}/members/snapshots/
data/discord/servers/{server_id}-{slug}/members/sync_history.yaml
```

## Example Output

```
Connecting to Discord...
Syncing members from My Server (1234567890)...
Estimated members: 50,000

Syncing... [========================================] 50000/50000 (100.0%)

Sync complete in 75.4 seconds
- Total members: 50,000 (49,500 humans, 500 bots)

Data saved to: data/discord/servers/1234567890-my-server/members/
```

## Troubleshooting

**"Server not found" error:**
- Ensure the bot is added to the server
- Check the server ID is correct

**"Authentication failed" error:**
- Check your bot token in `.env`
- Make sure it's a bot token, not a user token

**"Forbidden" error:**
- Enable SERVER MEMBERS INTENT in Discord Developer Portal
- Go to your application → Bot → Privileged Gateway Intents
- Toggle "Server Members Intent" ON
- Make sure bot has "Read Members" permission in the server

**Only a few members returned:**
- This usually means SERVER MEMBERS INTENT is not enabled
- Or the bot doesn't have permission to view members

## Notes

- Uses HTTP API pagination (1000 members per request)
- Handles rate limiting automatically
- Bot token provides official API compliance
- No ToS concerns unlike user tokens
- For rich profiles (bio, pronouns), use `discord-user-connector` plugin instead
