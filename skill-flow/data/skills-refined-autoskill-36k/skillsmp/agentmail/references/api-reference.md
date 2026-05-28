# AgentMail API Reference

Complete method signatures for all AgentMail resources.

## Client Initialization

```python
# Python - Sync
from agentmail import AgentMail
client = AgentMail(api_key="...")  # or uses AGENTMAIL_API_KEY env

# Python - Async
from agentmail import AsyncAgentMail
client = AsyncAgentMail()
```

```typescript
// TypeScript
import { AgentMailClient } from "agentmail";
const client = new AgentMailClient({ apiKey: "..." });
```

## Inboxes

| Method | Description |
|--------|-------------|
| `client.inboxes.list(limit?, page_token?)` | List all inboxes |
| `client.inboxes.get(inbox_id)` | Get inbox by ID |
| `client.inboxes.create(username?, domain?, display_name?, client_id?)` | Create inbox |
| `client.inboxes.update(inbox_id, display_name)` | Update inbox |
| `client.inboxes.delete(inbox_id)` | Delete inbox |

### Create Inbox Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `username` | string? | Username part (random if not specified) |
| `domain` | string? | Domain (default: `agentmail.to`) |
| `display_name` | string? | Display name for From header |
| `client_id` | string? | Idempotency key |

### Inbox Object

```python
{
    "inbox_id": "agent@agentmail.to",
    "pod_id": "pod_xxx",
    "display_name": "My Agent",
    "client_id": "my-client-id",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

## Messages

| Method | Description |
|--------|-------------|
| `client.inboxes.messages.list(inbox_id, limit?, page_token?, labels?, before?, after?, ascending?, include_spam?)` | List messages |
| `client.inboxes.messages.get(inbox_id, message_id)` | Get message |
| `client.inboxes.messages.send(inbox_id, to?, cc?, bcc?, subject?, text?, html?, attachments?, headers?, labels?, reply_to?)` | Send message |
| `client.inboxes.messages.reply(inbox_id, message_id, to?, cc?, bcc?, reply_all?, text?, html?, attachments?, headers?, labels?, reply_to?)` | Reply to message |
| `client.inboxes.messages.reply_all(inbox_id, message_id, text?, html?, attachments?, headers?, labels?, reply_to?)` | Reply all |
| `client.inboxes.messages.update(inbox_id, message_id, add_labels?, remove_labels?)` | Update labels |
| `client.inboxes.messages.get_attachment(inbox_id, message_id, attachment_id)` | Get attachment bytes |
| `client.inboxes.messages.get_raw(inbox_id, message_id)` | Get raw MIME |

### Send Message Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `to` | string \| string[] | Recipient(s) |
| `cc` | string \| string[]? | CC recipient(s) |
| `bcc` | string \| string[]? | BCC recipient(s) |
| `subject` | string? | Subject line |
| `text` | string? | Plain text body |
| `html` | string? | HTML body |
| `attachments` | Attachment[]? | File attachments |
| `headers` | dict? | Custom headers |
| `labels` | string[]? | Labels to apply |
| `reply_to` | string \| string[]? | Reply-to address |

### Attachment Object (for sending)

```python
{
    "content": "base64-encoded-content",
    "filename": "report.pdf",
    "content_type": "application/pdf"
}
```

### Message Object

```python
{
    "inbox_id": "agent@agentmail.to",
    "thread_id": "thd_xxx",
    "message_id": "msg_xxx",
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "cc": [],
    "bcc": [],
    "subject": "Hello",
    "text": "Full email text with quotes",
    "html": "<p>Full email HTML</p>",
    "extracted_text": "Just the new reply content",
    "extracted_html": "<p>Just the new reply</p>",
    "preview": "Short preview...",
    "labels": ["received"],
    "attachments": [...],
    "in_reply_to": "msg_parent",
    "references": ["msg_1", "msg_2"],
    "timestamp": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

## Threads

| Method | Description |
|--------|-------------|
| `client.threads.list(limit?, page_token?, labels?, before?, after?, ascending?, include_spam?)` | List all threads (org-wide) |
| `client.threads.get(thread_id)` | Get thread with messages |
| `client.threads.get_attachment(thread_id, attachment_id)` | Get attachment |
| `client.inboxes.threads.list(inbox_id, ...)` | List threads in inbox |
| `client.inboxes.threads.get(inbox_id, thread_id)` | Get thread in inbox |
| `client.inboxes.threads.delete(inbox_id, thread_id)` | Delete thread |

### Thread Object

```python
{
    "thread_id": "thd_xxx",
    "inbox_id": "agent@agentmail.to",
    "subject": "Conversation subject",
    "messages": [...],  # List of MessageItem
    "labels": ["important"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

## Webhooks

| Method | Description |
|--------|-------------|
| `client.webhooks.list(limit?, page_token?)` | List webhooks |
| `client.webhooks.get(webhook_id)` | Get webhook |
| `client.webhooks.create(url, event_types, pod_ids?, inbox_ids?, client_id?)` | Create webhook |
| `client.webhooks.delete(webhook_id)` | Delete webhook |

### Create Webhook Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | Webhook endpoint URL |
| `event_types` | string[] | Events to subscribe to |
| `pod_ids` | string[]? | Filter by pods |
| `inbox_ids` | string[]? | Filter by inboxes |
| `client_id` | string? | Idempotency key |

### Event Types

- `message.received`
- `message.sent`
- `message.delivered`
- `message.bounced`
- `message.complained`
- `message.rejected`
- `domain.verified`

## WebSockets

```python
# Sync
with client.websockets.connect() as socket:
    socket.send_subscribe(Subscribe(inbox_ids=["agent@agentmail.to"]))
    for event in socket:
        if isinstance(event, MessageReceivedEvent):
            print(event.message.subject)

# Async
async with client.websockets.connect() as socket:
    await socket.send_subscribe(Subscribe(inbox_ids=["agent@agentmail.to"]))
    async for event in socket:
        ...
```

### Subscribe Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `inbox_ids` | string[]? | Subscribe to specific inboxes |
| `pod_ids` | string[]? | Subscribe to specific pods |
| `event_types` | string[]? | Filter event types |

### Event Types

| Python | TypeScript | Description |
|--------|------------|-------------|
| `Subscribed` | `AgentMail.Subscribed` | Subscription confirmed |
| `MessageReceivedEvent` | `AgentMail.MessageReceivedEvent` | New email |
| `MessageSentEvent` | `AgentMail.MessageSentEvent` | Email sent |
| `MessageDeliveredEvent` | `AgentMail.MessageDeliveredEvent` | Email delivered |
| `MessageBouncedEvent` | `AgentMail.MessageBouncedEvent` | Email bounced |
| `MessageComplainedEvent` | `AgentMail.MessageComplainedEvent` | Spam complaint |
| `MessageRejectedEvent` | `AgentMail.MessageRejectedEvent` | Email rejected |
| `DomainVerifiedEvent` | `AgentMail.DomainVerifiedEvent` | Domain verified |

## Domains

| Method | Description |
|--------|-------------|
| `client.domains.list(limit?, page_token?)` | List domains |
| `client.domains.get(domain_id)` | Get domain with DNS records |
| `client.domains.create(domain, feedback_enabled)` | Create domain |
| `client.domains.delete(domain_id)` | Delete domain |
| `client.domains.verify(domain_id)` | Trigger verification |
| `client.domains.get_zone_file(domain_id)` | Get BIND zone file |

### Domain Object

```python
{
    "domain_id": "example.com",
    "pod_id": "pod_xxx",
    "status": "VERIFIED",  # NOT_STARTED, PENDING, INVALID, FAILED, VERIFYING, VERIFIED
    "feedback_enabled": True,
    "records": [
        {"type": "TXT", "name": "_dmarc.example.com", "value": "...", "status": "VALID"},
        {"type": "TXT", "name": "mail.example.com", "value": "...", "status": "VALID"},
        {"type": "MX", "name": "example.com", "value": "...", "priority": 10, "status": "VALID"}
    ],
    "created_at": "2024-01-01T00:00:00Z"
}
```

## Pods

| Method | Description |
|--------|-------------|
| `client.pods.list(limit?, page_token?)` | List pods |
| `client.pods.get(pod_id)` | Get pod |
| `client.pods.create(name?, client_id?)` | Create pod |
| `client.pods.delete(pod_id)` | Delete pod (must be empty) |
| `client.pods.inboxes.list(pod_id)` | List inboxes in pod |
| `client.pods.threads.list(pod_id)` | List threads in pod |
| `client.pods.drafts.list(pod_id)` | List drafts in pod |
| `client.pods.domains.list(pod_id)` | List domains in pod |

## Drafts

| Method | Description |
|--------|-------------|
| `client.drafts.list(limit?, page_token?, labels?, before?, after?, ascending?)` | List all drafts (org-wide) |
| `client.drafts.get(draft_id)` | Get draft |
| `client.inboxes.drafts.list(inbox_id, ...)` | List drafts in inbox |
| `client.inboxes.drafts.get(inbox_id, draft_id)` | Get draft |
| `client.inboxes.drafts.create(inbox_id, to?, cc?, bcc?, subject?, text?, html?, attachments?)` | Create draft |
| `client.inboxes.drafts.update(inbox_id, draft_id, ...)` | Update draft |
| `client.inboxes.drafts.send(inbox_id, draft_id)` | Send draft |
| `client.inboxes.drafts.delete(inbox_id, draft_id)` | Delete draft |

## API Keys

| Method | Description |
|--------|-------------|
| `client.api_keys.list(limit?, page_token?)` | List API keys |
| `client.api_keys.create(name)` | Create API key |
| `client.api_keys.delete(api_key)` | Delete API key |

## Metrics

| Method | Description |
|--------|-------------|
| `client.metrics.list(start_timestamp, end_timestamp, event_types?)` | Get org metrics |
| `client.inboxes.metrics.list(inbox_id, start_timestamp, end_timestamp, event_types?)` | Get inbox metrics |

## Organizations

| Method | Description |
|--------|-------------|
| `client.organizations.get()` | Get organization info |

## Error Types

| Error | Status | Description |
|-------|--------|-------------|
| `NotFoundError` | 404 | Resource not found |
| `ValidationError` | 400 | Invalid request |
| `MessageRejectedError` | 403 | Message rejected (e.g., blocked address) |
| `IsTakenError` | 409 | Resource already exists |

## Pagination

All list endpoints support pagination:

```python
# First page
response = client.inboxes.list(limit=10)

# Next page
if response.next_page_token:
    next_page = client.inboxes.list(limit=10, page_token=response.next_page_token)
```
