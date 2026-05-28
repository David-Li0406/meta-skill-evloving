---
name: discord-sync
description: "Sync Discord server messages using BOT TOKEN. Faster with higher rate limits. Use when routed here by community-agent:discord-sync or user explicitly requests bot token sync."
---

# Discord Bot Token Sync

Syncs messages from Discord servers using bot token for higher rate limits and official API compliance.

## When to Use

- Routed here by `community-agent:discord-sync` preflight check
- User explicitly asks for "bot token sync"
- User wants "faster sync" or "higher rate limits"
- Syncing large servers where rate limits matter

## When NOT to Use

- User just says "sync discord" - use `community-agent:discord-sync` instead (it will route here if appropriate)
- User wants to sync DMs (bots cannot access DMs)
- User needs rich profile data (bio, pronouns)

## Prerequisites

- `.env` with `DISCORD_BOT_TOKEN` set
- Bot added to the target server with these permissions:
  - Read Message History
  - View Channels

## How to Execute

### Sync all channels in a server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID
```

### Sync with custom history range:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID --days 7
```

### Quick sync (limited messages per channel):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID --quick
```

### Full re-sync:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID --full
```

## Output Location

Messages saved to: `./data/discord/{server_id}-{slug}/{channel_name}/messages.md`

This uses the same unified storage format as `discord-user-connector`, so messages from either connector are compatible.

## Comparison with discord-user-connector:discord-sync

| Feature | discord-bot-connector | discord-user-connector |
|---------|----------------------|------------------------|
| Token | Bot Token | User Token |
| Rate Limits | Higher (official API) | Lower (user API) |
| Server Messages | Yes | Yes |
| DM Access | No | Yes |
| ToS Compliant | Yes | Gray area |

## Limitations

- **Cannot sync DMs** - Bots cannot access user direct messages
- **Cannot send as user** - Messages sent by bot appear as bot
- Requires bot to be added to each server
