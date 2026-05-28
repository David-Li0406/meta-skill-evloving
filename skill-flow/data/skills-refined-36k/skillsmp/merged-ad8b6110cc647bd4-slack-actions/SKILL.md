---
name: slack-actions
description: Use this skill when you need to control Slack from Clawdbot via the slack tool, including reacting to messages, managing pins, and sending/editing/deleting messages.
---

# Slack Actions

## Overview

Use `slack` to react, manage pins, send/edit/delete messages, and fetch member info. The tool uses the bot token configured for Clawdbot.

## Inputs to collect

- `channelId` and `messageId` (Slack message timestamp, e.g. `1712023032.1234`).
- For reactions, an `emoji` (Unicode or `:name:`).
- For message sends, a `to` target (`channel:<id>` or `user:<id>`) and `content`.

Message context lines include `slack message id` and `channel` fields you can reuse directly.

## Actions

### Action groups

| Action group | Default | Notes |
| --- | --- | --- |
| reactions | enabled | React + list reactions |
| messages | enabled | Read/send/edit/delete |
| pins | enabled | Pin/unpin/list |
| memberInfo | enabled | Member info |
| emojiList | enabled | Custom emoji list |

### React to a message

```json
{
  "action": "react",
  "channelId": "<channelId>",
  "messageId": "<messageId>",
  "emoji": "<emoji>"
}
```

### List reactions

```json
{
  "action": "reactions",
  "channelId": "<channelId>",
  "messageId": "<messageId>"
}
```

### Send a message

```json
{
  "action": "sendMessage",
  "to": "<to>",
  "content": "<content>"
}
```

### Edit a message

```json
{
  "action": "editMessage",
  "channelId": "<channelId>",
  "messageId": "<messageId>",
  "content": "<content>"
}
```

### Delete a message

```json
{
  "action": "deleteMessage",
  "channelId": "<channelId>",
  "messageId": "<messageId>"
}
```

### Read recent messages

```json
{
  "action": "readMessages",
  "channelId": "<channelId>",
  "limit": 20
}
```

### Pin a message

```json
{
  "action": "pinMessage",
  "channelId": "<channelId>",
  "messageId": "<messageId>"
}
```

### Unpin a message

```json
{
  "action": "unpinMessage",
  "channelId": "<channelId>",
  "messageId": "<messageId>"
}
```

### List pinned items

```json
{
  "action": "listPins",
  "channelId": "<channelId>"
}
```

### Member info

```json
{
  "action": "memberInfo",
  "userId": "<userId>"
}
```

### Emoji list

```json
{
  "action": "emojiList"
}
```

## Ideas to try

- React with ✅ to mark completed tasks.
- Pin key decisions or weekly status updates.