# Sending Messages

## Send Message
```
POST /v3/grants/{grant_id}/messages/send
```

**Timeout**: 150 seconds (Exchange can take 2 minutes)

```json
{
  "subject": "string",
  "body": "string (HTML supported)",
  "to": [{"name": "string", "email": "string"}],
  "cc": [{"name": "string", "email": "string"}],
  "bcc": [{"name": "string", "email": "string"}],
  "from": [{"name": "string", "email": "string"}],
  "reply_to": [{"name": "string", "email": "string"}],
  "reply_to_message_id": "string (for threading)",
  "attachments": [{
    "content": "base64-encoded",
    "content_type": "string",
    "filename": "string"
  }],
  "custom_headers": [{"name": "string", "value": "string"}],
  "tracking_options": {
    "opens": true,
    "links": true,
    "thread_replies": true,
    "label": "string"
  }
}
```

**Limits:**
- Instant send: 10MB max attachment
- Scheduled send: 3MB max attachment
- Non-ASCII emails cause 402 errors

---

## Scheduled Send

Add to send request:
```json
{
  "send_at": "unix_timestamp",
  "use_draft": true  // Store on provider (unlimited future time)
}
```

Without `use_draft`: 2 minutes to 30 days in future (Nylas storage).

**Manage Scheduled:**
```
GET /v3/grants/{grant_id}/messages/schedules
GET /v3/grants/{grant_id}/messages/schedules/{schedule_id}
DELETE /v3/grants/{grant_id}/messages/schedules/{schedule_id}
```

---

## Google One-Click Unsubscribe

Required for 5000+ daily messages to Google:
```json
{
  "custom_headers": [
    {"name": "List-Unsubscribe-Post", "value": "List-Unsubscribe=One-Click"},
    {"name": "List-Unsubscribe", "value": "<mailto:unsubscribe@example.com>"}
  ]
}
```

**Note**: Microsoft Graph and iCloud do NOT support these headers.

---

## Attachments in Messages

**Inline (< 3MB):**
```json
{
  "attachments": [{
    "content": "base64-encoded-content",
    "content_type": "application/pdf",
    "filename": "document.pdf",
    "content_id": "cid123"  // For inline images
  }]
}
```

**Large files (> 3MB):** Use `multipart/form-data` content type.
