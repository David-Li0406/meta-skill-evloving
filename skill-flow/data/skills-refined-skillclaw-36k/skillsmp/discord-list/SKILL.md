---
name: discord-list
description: "List Discord servers and channels. Use when user asks about available servers, channels, or wants to discover what's accessible."
---

# Discord List

Lists Discord servers, channels, and DMs accessible with your user token.

## When to Use

- User asks "what Discord servers do I have?"
- User asks "what channels are in [server]?"
- User wants to "list my Discord servers"
- User wants to "show me Discord channels"
- User needs to find server or channel IDs
- User asks "list my Discord DMs"
- User wants to find DM channel IDs

## How to Execute

### List all servers (includes DMs by default):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --servers
```

### List servers only (exclude DMs):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --servers --no-dms
```

### List channels in a specific server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --channels SERVER_ID
```

Replace `SERVER_ID` with the actual Discord server ID.

### List DMs only:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --dms
```

## Output

Returns a formatted table of:
- **Servers**: ID, name, member count
- **Channels**: ID, name, category
- **DMs**: Channel ID, User ID, Username, Display Name

## Prerequisites

- `./.env` file with `DISCORD_USER_TOKEN` set (in cwd)
- Network access to Discord

## Next Steps

After listing channels, suggest syncing messages with discord-sync skill.
