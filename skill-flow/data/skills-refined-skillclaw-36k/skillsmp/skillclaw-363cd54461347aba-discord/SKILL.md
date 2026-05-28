---
name: discord
description: Use this skill when you need to control Discord from a bot via the discord tool: send messages, react, post or upload stickers, upload emojis, run polls, manage threads, and handle moderation actions in Discord DMs or channels.
---

# Discord Actions

## Overview

Use `discord` to manage messages, reactions, threads, polls, and moderation. You can disable groups via `discord.actions.*` (defaults to enabled, except roles/moderation). The tool uses the bot token configured for your Discord bot.

## Inputs to collect

- For reactions: `channelId`, `messageId`, and an `emoji`.
- For fetching messages: `guildId`, `channelId`, `messageId`, or a `messageLink` like `https://discord.com/channels/<guildId>/<channelId>/<messageId>`.
- For stickers/polls/sendMessage: a `to` target (`channel:<id>` or `user:<id>`). Optional `content` text.
- Polls also need a `question` plus 2–10 `answers`.
- For media: `mediaUrl` with `file:///path` for local files or `https://...` for remote.
- For emoji uploads: `guildId`, `name`, `mediaUrl`, optional `roleIds` (limit 256KB, PNG/JPG/GIF).
- For sticker uploads: `guildId`, `name`, `description`, `tags`, `mediaUrl` (limit 512KB, PNG/APNG/Lottie JSON).

Message context lines include `discord message id` and `channel` fields you can reuse directly.

**Note:** `sendMessage` uses `to: "channel:<id>"` format, not `channelId`. Other actions like `react`, `readMessages`, `editMessage` use `channelId` directly. `fetchMessage` accepts message IDs or full links like `https://discord.com/channels/<guildId>/<channelId>/<messageId>`.

## Actions

### React to a message

```json
{
  "action": "react",
  "channelId": "123",
  "messageId": "456",
  "emoji": "✅"
}
```

### List reactions + users

```json
{
  "action": "reactions",
  "channelId": "123",
  "messageId": "456",
  "limit": 100
}
```

### Send a sticker

```json
{
  "action": "sticker",
  "to": "channel:123",
  "stickerIds": ["9876543210"],
  "content": "Nice work!"
}
```

- Up to 3 sticker IDs per message.
- `to` can be `user:<id>` for DMs.

### Upload a custom emoji

```json
{
  "action": "emojiUpload",
  "guildId": "999",
  "name": "party_blob",
  "mediaUrl": "file:///tmp/party.png",
  "roleIds": ["222"]
}
```

- Emoji images must be PNG/JPG/GIF and <= 256KB.
- `roleIds` is optional; omit to make the emoji available to everyone.

### Upload a sticker

```json
{
  "action": "stickerUpload",
  "guildId": "999",
  "name": "fun_sticker",
  "description": "A fun sticker",
  "tags": ["fun", "sticker"],
  "mediaUrl": "file:///tmp/fun_sticker.png"
}
```

- Sticker images must be <= 512KB and can be in PNG/APNG/Lottie JSON format.