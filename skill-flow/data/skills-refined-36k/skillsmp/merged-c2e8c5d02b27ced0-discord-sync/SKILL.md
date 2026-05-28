---
name: discord-sync
description: Use this skill to sync messages from Discord servers and DMs using either a user token for rich profile data or a bot token for faster syncs with higher rate limits.
---

# Discord Message Sync

Syncs messages from Discord servers and DMs using either user token or bot token authentication.

## When to Use

- Routed here by `community-agent:discord-sync` preflight check
- User explicitly requests "user token sync" for rich profile data or "bot token sync" for faster syncs
- User wants to sync DMs (user token only) or large servers (bot token preferred)

## When NOT to Use

- User just says "sync discord" - use `community-agent:discord-sync` instead
- User wants faster sync with bot token but does not need DMs - use `discord-bot-connector:discord-sync`
- User needs rich profile data but prefers bot token - use user token instead

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

### Sync all channels in a configured server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --server SERVER_ID
```

### Sync specific channel:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --channel CHANNEL_ID
```

### Sync with custom history range:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --days <number_of_days>
```

### Full re-sync (ignore previous sync state):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --full
```

### Sync DMs (user token only)

**DMs are included by default.** Use `--no-dms` to sync servers only.

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
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_sync.py --dm-limit <limit>
```

## Output Location

All paths are relative to cwd (current working directory):

### Server Messages
Messages saved to: `./data/{server_id}/{channel_name}/messages.md`

### DM Messages
DM messages saved to: `./dms/discord/{user_id}-{username}/messages.md`

## Prerequisites

- For user token: `./.env` file with `DISCORD_USER_TOKEN` set and `./config/agents.yaml` with `discord.default_server_id` configured.
- For bot token: `.env` with `DISCORD_BOT_TOKEN` set and bot added to the target server with necessary permissions.

## Limitations

- **User Token**: Can sync DMs and provides rich profile data.
- **Bot Token**: Faster sync with higher rate limits but cannot access DMs.

## Next Steps

After syncing, use discord-read skill to view or search messages.