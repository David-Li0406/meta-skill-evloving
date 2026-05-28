# AgentMail Webhook Events

Complete webhook event types and payload structures.

## Event Structure

All webhook payloads follow this structure:

```json
{
  "type": "event",
  "event_type": "message.received",
  "event_id": "evt_xxx"
  // ... event-specific data
}
```

## Message Events

### message.received

Triggered when a new email is received. **This is the only event that includes full Thread + Message data.**

```json
{
  "type": "event",
  "event_type": "message.received",
  "event_id": "evt_xxx",
  "message": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "from_": ["sender@example.com"],
    "to": ["agent@agentmail.to"],
    "cc": [],
    "bcc": [],
    "reply_to": [],
    "subject": "Hello",
    "preview": "Short preview...",
    "text": "Full email text",
    "html": "<p>Full email HTML</p>",
    "labels": ["received"],
    "attachments": [
      {
        "attachment_id": "att_xxx",
        "filename": "document.pdf",
        "content_type": "application/pdf",
        "size": 123456,
        "inline": false
      }
    ],
    "in_reply_to": "msg_parent",
    "references": ["msg_1", "msg_2"],
    "timestamp": "2024-01-01T10:00:00Z",
    "created_at": "2024-01-01T10:00:00Z"
  },
  "thread": {
    "thread_id": "thd_xxx",
    "inbox_id": "agent@agentmail.to",
    "subject": "Hello",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

### message.sent

Triggered when a message is successfully sent.

```json
{
  "type": "event",
  "event_type": "message.sent",
  "event_id": "evt_xxx",
  "send": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "timestamp": "2024-01-01T10:05:00Z",
    "recipients": ["recipient@example.com"]
  }
}
```

### message.delivered

Triggered when recipient's mail server accepts the message.

```json
{
  "type": "event",
  "event_type": "message.delivered",
  "event_id": "evt_xxx",
  "delivery": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "timestamp": "2024-01-01T10:06:00Z",
    "recipients": ["recipient@example.com"]
  }
}
```

**Note:** `message.delivered` means the receiving server accepted it, NOT that it landed in inbox (could still go to spam).

### message.bounced

Triggered when a message fails to deliver.

```json
{
  "type": "event",
  "event_type": "message.bounced",
  "event_id": "evt_xxx",
  "bounce": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "timestamp": "2024-01-01T10:07:00Z",
    "type": "Permanent",
    "sub_type": "General",
    "recipients": [
      {
        "address": "invalid@example.com",
        "status": "bounced"
      }
    ]
  }
}
```

**Warning:** Bounced addresses are permanently blocked. Keep bounce rate < 4%.

### message.complained

Triggered when recipient marks email as spam.

```json
{
  "type": "event",
  "event_type": "message.complained",
  "event_id": "evt_xxx",
  "complaint": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "timestamp": "2024-01-01T10:08:00Z",
    "type": "abuse",
    "sub_type": "spam",
    "recipients": ["complainer@example.com"]
  }
}
```

**Warning:** Complained addresses are permanently blocked.

### message.rejected

Triggered when a message is rejected before sending (e.g., validation error, blocked address).

```json
{
  "type": "event",
  "event_type": "message.rejected",
  "event_id": "evt_xxx",
  "reject": {
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "timestamp": "2024-01-01T10:09:00Z",
    "reason": "Recipient address is blocked"
  }
}
```

## Domain Events

### domain.verified

Triggered when a custom domain is successfully verified.

```json
{
  "type": "event",
  "event_type": "domain.verified",
  "event_id": "evt_xxx",
  "domain": {
    "domain_id": "example.com",
    "status": "verified",
    "feedback_enabled": true,
    "records": [
      {
        "type": "TXT",
        "name": "_dmarc.example.com",
        "value": "v=DMARC1; p=none",
        "status": "VALID"
      }
    ],
    "created_at": "2024-01-01T09:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
}
```

## Creating Webhooks

### Subscribe to Specific Events

```python
client.webhooks.create(
    url="https://example.com/webhooks",
    event_types=["message.received", "message.bounced"],
    client_id="my-webhook"
)
```

### Filter by Inbox

```python
client.webhooks.create(
    url="https://example.com/webhooks",
    event_types=["message.received"],
    inbox_ids=["agent@agentmail.to"],
    client_id="inbox-specific-webhook"
)
```

### Filter by Pod

```python
client.webhooks.create(
    url="https://example.com/webhooks",
    event_types=["message.received"],
    pod_ids=["pod_xxx"],
    client_id="pod-specific-webhook"
)
```

## Handling Webhooks

### Best Practice Pattern

```python
from flask import Flask, request, Response
from threading import Thread

app = Flask(__name__)

@app.route("/webhooks", methods=["POST"])
def webhook():
    # Return 200 immediately
    Thread(target=process, args=(request.json,)).start()
    return Response(status=200)

def process(payload):
    event_type = payload["event_type"]
    
    if event_type == "message.received":
        handle_received(payload["message"])
    elif event_type == "message.bounced":
        handle_bounce(payload["bounce"])
    elif event_type == "message.complained":
        handle_complaint(payload["complaint"])

def handle_received(message):
    print(f"New email from {message['from_']}")

def handle_bounce(bounce):
    print(f"Bounce for {bounce['recipients']}")
    # Remove bounced addresses from your list

def handle_complaint(complaint):
    print(f"Complaint from {complaint['recipients']}")
    # Remove complaining addresses from your list
```

## Field Reference

### Common Fields

| Field | Description |
|-------|-------------|
| `from_` | Sender address (underscore to avoid Python keyword) |
| `to` | Recipient addresses |
| `inbox_id` | Email address of the inbox |
| `thread_id` | Conversation ID |
| `message_id` | Unique message ID |
| `timestamp` | When the event occurred |

### Attachment Fields

| Field | Description |
|-------|-------------|
| `attachment_id` | Use to download via `get_attachment()` |
| `filename` | Original filename |
| `content_type` | MIME type |
| `size` | Size in bytes |
| `inline` | Whether embedded in HTML |
