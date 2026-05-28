# Message Tracking

**Not available for Sandbox/trial applications.**

## Enable Tracking

Add to Send Message or Create Draft request:
```json
{
  "tracking_options": {
    "opens": true,       // Inserts 1x1 transparent pixel
    "links": true,       // Rewrites links for click tracking
    "thread_replies": true,
    "label": "campaign-name"
  }
}
```

## Required Scopes
- Google: `gmail.send`
- Microsoft: `Mail.ReadWrite`, `Mail.Send`

## Link Tracking Requirements
- Max 20 tracked links per message
- Must use valid HTML anchor tags: `<a href="https://...">text</a>`
- Supported URI schemes: `https`, `mailto`, `tel`
- Links with credentials are ignored (not rewritten)

## Webhook Events

### message.opened
```json
{
  "type": "message.opened",
  "data": {
    "object": {
      "message_id": "string",
      "message_data": {"count": "number", "timestamp": "number"},
      "recents": [{"ip": "string", "timestamp": "number", "user_agent": "string"}]
    }
  }
}
```

### message.link_clicked
```json
{
  "type": "message.link_clicked",
  "data": {
    "object": {
      "message_id": "string",
      "link_data": [{"count": "number", "url": "string"}],
      "recents": [{"ip": "string", "link_index": "number", "timestamp": "number"}]
    }
  }
}
```

### thread.replied
```json
{
  "type": "thread.replied",
  "data": {
    "object": {
      "message_id": "string",
      "thread_id": "string",
      "reply_data": {"count": "number"}
    }
  }
}
```
