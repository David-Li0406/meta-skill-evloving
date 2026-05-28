---
name: send-discord-notification
description: Use this skill when you need to send notifications to Discord about status changes, alerts, or reports using the Discord MCP server.
---

# Skill body

## When to Use

- Need to notify humans about status changes or alerts
- Want to post rich formatted messages with embeds
- Sending health reports, issue alerts, or investigation results

## Prerequisites

Before applying this skill, verify:

- [ ] DISCORD_MCP_URL environment variable is set (or use default)
- [ ] Target channel exists in the Discord server
- [ ] Message content or embed data is available

## Input Schema

```json
{
  "type": "string - Notification type: health | issue | investigation | success | failure | escalation",
  "title": "string - Notification title",
  "description": "string - Main message content",
  "channel_name": "string - Target channel (default: kubani-alerts)",
  "resource": "string - Optional resource identifier",
  "namespace": "string - Optional Kubernetes namespace",
  "severity": "string - Optional severity: low | medium | high | critical",
  "fields": "array - Optional additional fields [{name, value, inline}]"
}
```

## Actions

### 1. Determine Notification Type and Color

Map notification type to Discord embed color:

| Type            | Color  | Hex      |
|-----------------|--------|----------|
| health          | Green  | 0x57F287 |
| success         | Green  | 0x57F287 |
| issue           | Orange | 0xF39C12 |
| investigation    | Blue   | 0x5865F2 |
| failure         | Red    | 0xED4245 |
| escalation      | Red    | 0xED4245 |

### 2. Build Discord Embed

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  embed:
    title: $title
    description: $description
    color: $type_color
    fields: $fields
    footer:
      text: "Kubani AI Agent"
    timestamp: $current_timestamp
timeout: 30s
on_error: retry
```

### 3. Send Message

Use the Discord MCP server to send the formatted message.

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  message: $embed
timeout: 30s
on_error: retry
```