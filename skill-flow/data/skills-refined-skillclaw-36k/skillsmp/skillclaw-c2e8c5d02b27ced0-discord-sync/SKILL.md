---
name: discord-sync
description: Use this skill to sync messages from Discord servers or DMs using either user or bot token authentication, depending on user needs.
---

# Discord Sync

Syncs messages from Discord servers and DMs using either user token or bot token authentication.

## When to Use

- Routed here by `community-agent:discord-sync` preflight check
- User explicitly requests "user token sync" for rich profile data or DMs
- User explicitly requests "bot token sync" for faster sync and higher rate limits
- User wants to sync messages from a specific server or DM

## When NOT to Use

- User just says "sync discord" - use `community-agent:discord-sync` instead (it will route here if appropriate)
- User wants to sync DMs but is using a bot token (bots cannot access DMs)

## Smart Defaults (Reduce Questions)

**When user is vague, apply these defaults instead of asking:**

| User Says | Default Action |
|-----------|----------------|
| "sync my Discord" | Sync the configured default server from agents.yaml |
| "sync [server name]" | Find server by name, sync with 7 days default |
| No --days specified | Default to 7 days |
| "sync everything" | List available servers and ask user to pick |

**Only ask for clarification when:**
- User's server name matches multiple servers
- User explicitly asks "which servers can I sync?"

## How to Execute

### Sync all channels in configured server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py
```

### Sync specific channel:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --channel CHANNEL_ID
```

### Sync specific server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID
```

### Sync with custom history range:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --days 7
```

### Full re-sync (ignore previous sync state):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --full
```

### Sync DMs

**DMs are included by default for user token sync.** Use `--no-dms` to sync servers only.

Sync all (servers + DMs):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py
```

Sync servers only (exclude DMs):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --no-dms
```

Sync a specific DM by channel ID:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --dm CHANNEL_ID
```

Sync DMs with custom message limit (default: 100):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --dm-limit 500
```

## Prerequisites for Bot Token Sync

- `.env` with `DISCORD_BOT_TOKEN` set
- Bot added to the target server with these permissions:
  - Read Message History
  - View Channels

## Output Location

Messages saved to: `./data/discord/{server_id}-{slug}/{channel_name}/messages.md`

This uses the same unified storage format, ensuring compatibility between user and bot token syncs.

## Limitations

- **Cannot sync DMs** when using a bot token.
- **Cannot send as user** - Messages sent by bot appear as bot.
- Requires bot to be added to each server for bot token sync.