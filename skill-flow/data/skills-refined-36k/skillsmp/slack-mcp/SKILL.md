---
name: slack-mcp
permissionMode: bypassPermissions
description: Slack Integration via MCP Hub. Lese Kanäle, sende Nachrichten, durchsuche Konversationen. Posts erscheinen mit der konfigurierten Bot-Identität.
---

# Slack MCP Integration

Kommuniziere mit Slack über den MCP Hub.

## Verfügbare Tools

| Tool | Beschreibung |
|------|-------------|
| `channels_list` | Alle Kanäle auflisten |
| `conversations_add_message` | Nachricht in Kanal/DM senden |
| `conversations_history` | Nachrichten-Verlauf eines Kanals |
| `conversations_replies` | Thread-Antworten abrufen |
| `conversations_search_messages` | Nachrichten durchsuchen |

## Hub Slack Tools

### Kanäle auflisten (channels_list)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_slack_mcp_tool',
    arguments: {
      name: 'channels_list',
      arguments: {
        channel_types: 'public_channel,private_channel',
        limit: 100
      }
    }
  }
})
```

### Nachricht senden (conversations_add_message)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_slack_mcp_tool',
    arguments: {
      name: 'conversations_add_message',
      arguments: {
        channel_id: 'C01234567',
        payload: 'Hello from the Hub!',
        content_type: 'text/markdown'  // or 'text/plain'
      }
    }
  }
})
```

### Channel-Historie lesen (conversations_history)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_slack_mcp_tool',
    arguments: {
      name: 'conversations_history',
      arguments: {
        channel_id: 'C01234567',
        limit: '1d'  // Time-based: '1d', '1w', '30d' or count: '50'
      }
    }
  }
})
```

### Thread-Antworten (conversations_replies)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_slack_mcp_tool',
    arguments: {
      name: 'conversations_replies',
      arguments: {
        channel_id: 'C01234567',
        thread_ts: '1234567890.123456',
        limit: '20'
      }
    }
  }
})
```

### Nachrichten suchen (conversations_search_messages)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_slack_mcp_tool',
    arguments: {
      name: 'conversations_search_messages',
      arguments: {
        search_query: 'deployment issues',
        limit: 20
      }
    }
  }
})
```

## Workflow-Beispiele

### Nachricht posten
```
1. channels_list → Ziel-Kanal finden (channel_id)
2. conversations_add_message → Nachricht senden
```

### Konversation lesen
```
1. channels_list → Kanal finden
2. conversations_history → Letzte Nachrichten
3. conversations_replies → Thread-Details (wenn ts vorhanden)
```

### Thema recherchieren
```
1. conversations_search_messages → Relevante Nachrichten finden
2. conversations_history → Kontext der Kanäle
3. conversations_replies → Thread-Tiefe
```

## Wichtige Hinweise

- **Channel-Zugriff**: Nur Kanäle wo der Bot Mitglied ist
- **Rate Limits**: Slack API hat Limits, bei Bulk-Operationen Pausen einbauen

## Tool-Referenz

| Aktion | Hub Tool | Slack MCP Tool |
|--------|----------|----------------|
| Kanäle | invoke_slack_mcp_tool | channels_list |
| Senden | invoke_slack_mcp_tool | conversations_add_message |
| Historie | invoke_slack_mcp_tool | conversations_history |
| Threads | invoke_slack_mcp_tool | conversations_replies |
| Suchen | invoke_slack_mcp_tool | conversations_search_messages |

## Configuration

Set `SLACK_BOT_TOKEN` in your `.env` file to enable Slack integration.
