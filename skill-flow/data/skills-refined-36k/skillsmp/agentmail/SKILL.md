---
name: agentmail
description: Build email agents using AgentMail API. Use when creating email automation, building AI email agents, setting up webhooks for email notifications, integrating email into AI workflows, or when the user asks about AgentMail, inboxes, or email agents.
---

# AgentMail

AgentMail is an API-first email platform for AI agents. Unlike traditional email services, it's designed for two-way conversations, allowing agents to send, receive, and reply to emails autonomously.

## Quick Start

### Installation

```bash
# Python
pip install agentmail

# Node.js
npm install agentmail
```

### Initialize Client

```python
from agentmail import AgentMail

client = AgentMail()  # Uses AGENTMAIL_API_KEY from environment
```

```typescript
import { AgentMailClient } from "agentmail";

const client = new AgentMailClient();  // Uses AGENTMAIL_API_KEY from environment
```

### Create Inbox and Send Email

```python
# Create inbox (use client_id for idempotency)
inbox = client.inboxes.create(
    username="my-agent",
    client_id="my-agent-inbox"
)
print(f"Created: {inbox.inbox_id}")  # e.g., my-agent@agentmail.to

# Send email (always include both text and html)
client.inboxes.messages.send(
    inbox_id=inbox.inbox_id,
    to=["user@example.com"],
    subject="Hello from my agent",
    text="Plain text version",
    html="<p>HTML version</p>",
    labels=["outreach"]
)
```

```typescript
const inbox = await client.inboxes.create({
  username: "my-agent",
  clientId: "my-agent-inbox"
});

await client.inboxes.messages.send(inbox.inboxId, {
  to: ["user@example.com"],
  subject: "Hello from my agent",
  text: "Plain text version",
  html: "<p>HTML version</p>",
  labels: ["outreach"]
});
```

## Resource Hierarchy

```
Organization (top-level container)
└── Pod (optional, for multi-tenancy)
    └── Inbox (email account, e.g., agent@agentmail.to)
        └── Thread (conversation, auto-created)
            └── Message (individual email)
                └── Attachment (files)
```

## Core Concepts

| Resource | Purpose |
|----------|---------|
| **Organization** | Top-level container for all resources |
| **Inbox** | Email account (e.g., `agent@agentmail.to`) |
| **Message** | Individual email with text, html, attachments |
| **Thread** | Conversation grouping (auto-created) |
| **Webhook** | Event notifications via HTTP POST |
| **WebSocket** | Persistent bidirectional connection |
| **Pod** | Multi-tenant isolation (optional) |
| **Domain** | Custom domain with SPF/DKIM/DMARC |
| **Draft** | Unsent message for review |
| **Labels** | String tags for filtering and state management |

## Common Workflows

### 1. Reply to Email

```python
client.inboxes.messages.reply(
    inbox_id="agent@agentmail.to",
    message_id="msg_xxx",
    text="Thanks for your message!",
    html="<p>Thanks for your message!</p>"
)
```

```typescript
await client.inboxes.messages.reply("agent@agentmail.to", "msg_xxx", {
  text: "Thanks for your message!",
  html: "<p>Thanks for your message!</p>"
});
```

### 2. List Messages with Label Filter

```python
messages = client.inboxes.messages.list(
    inbox_id="agent@agentmail.to",
    labels=["unread", "important"]
)
for msg in messages.messages:
    print(f"{msg.subject} from {msg.from_}")
```

### 3. Update Labels on Message

```python
client.inboxes.messages.update(
    inbox_id="agent@agentmail.to",
    message_id="msg_xxx",
    add_labels=["processed"],
    remove_labels=["unread"]
)
```

### 4. List Threads Org-Wide

```python
# Query all threads across all inboxes (for supervisor agents)
all_threads = client.threads.list()

# Or per inbox
inbox_threads = client.inboxes.threads.list(inbox_id="agent@agentmail.to")
```

### 5. Send Attachment

```python
import base64

with open("report.pdf", "rb") as f:
    content = base64.b64encode(f.read()).decode()

client.inboxes.messages.send(
    inbox_id="agent@agentmail.to",
    to=["user@example.com"],
    subject="Report attached",
    text="Please see attached.",
    attachments=[{
        "content": content,
        "filename": "report.pdf",
        "content_type": "application/pdf"
    }]
)
```

## Webhook Setup (Flask + ngrok)

Webhooks notify your agent in real-time when events occur (e.g., new email received).

### Complete Example

```python
import os
from threading import Thread
from flask import Flask, request, Response
import ngrok
from agentmail import AgentMail

app = Flask(__name__)
client = AgentMail()
port = 8080

# Start ngrok tunnel
listener = ngrok.forward(port, authtoken_from_env=True)
webhook_url = f"{listener.url()}/webhooks"

# Create inbox and webhook idempotently
client.inboxes.create(username="webhook-agent", client_id="webhook-agent-inbox")
client.webhooks.create(
    url=webhook_url,
    event_types=["message.received"],
    client_id="webhook-agent-webhook"
)

@app.route("/webhooks", methods=["POST"])
def receive_webhook():
    # Return 200 immediately, process in background
    Thread(target=process_webhook, args=(request.json,)).start()
    return Response(status=200)

def process_webhook(payload):
    event_type = payload["event_type"]
    if event_type == "message.received":
        message = payload["message"]
        print(f"New email from {message['from_']}: {message['subject']}")
        
        # Reply to the message
        client.inboxes.messages.reply(
            inbox_id=message["inbox_id"],
            message_id=message["message_id"],
            text="Thanks for your email! I'll get back to you soon."
        )

if __name__ == "__main__":
    print(f"Webhook URL: {webhook_url}")
    app.run(port=port)
```

### Webhook Event Types

- `message.received` - New email arrived (includes full Thread + Message data)
- `message.sent` - Email was sent
- `message.delivered` - Email was delivered to recipient's server
- `message.bounced` - Email failed to deliver
- `message.complained` - Recipient marked as spam
- `message.rejected` - Email rejected before sending
- `domain.verified` - Custom domain verified

See [references/webhook-events.md](references/webhook-events.md) for payload structures.

## WebSocket Real-time Events

WebSockets provide real-time events without needing a public URL.

### Async Pattern

```python
import asyncio
from agentmail import AsyncAgentMail, Subscribe, MessageReceivedEvent

client = AsyncAgentMail()

async def main():
    async with client.websockets.connect() as socket:
        await socket.send_subscribe(Subscribe(
            inbox_ids=["agent@agentmail.to"]
        ))
        
        async for event in socket:
            if isinstance(event, MessageReceivedEvent):
                print(f"New email: {event.message.subject}")

asyncio.run(main())
```

```typescript
const socket = await client.websockets.connect();

socket.on("open", () => {
  socket.sendSubscribe({
    type: "subscribe",
    inboxIds: ["agent@agentmail.to"]
  });
});

socket.on("message", (event) => {
  if (event.type === "message_received") {
    console.log(`New email: ${event.message.subject}`);
  }
});
```

## AI Agent Integration

Use `agentmail-toolkit` to give AI agents email capabilities.

### Installation

```bash
pip install agentmail-toolkit
```

### OpenAI Agents

```python
from agentmail import AgentMail
from agentmail_toolkit.openai import AgentMailToolkit
from agents import Agent, Runner

client = AgentMail()
toolkit = AgentMailToolkit(client)

agent = Agent(
    name="Email Agent",
    instructions=f"""You are an email agent. Your inbox is agent@agentmail.to.
    You can send, receive, and reply to emails.""",
    tools=toolkit.get_tools()
)

response = Runner.run(agent, [{"role": "user", "content": "Send a hello email to user@example.com"}])
```

### Langchain

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agentmail_toolkit.langchain import AgentMailToolkit

agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o"),
    tools=AgentMailToolkit().get_tools()
)
```

## Best Practices

### Idempotency

Always use `client_id` on create operations to prevent duplicates:

```python
# Safe to run multiple times - won't create duplicates
inbox = client.inboxes.create(
    username="my-agent",
    client_id="user-123-primary-inbox"
)

webhook = client.webhooks.create(
    url="https://example.com/webhooks",
    event_types=["message.received"],
    client_id="user-123-webhook"
)
```

### Email Deliverability

1. **Warm-up inboxes**: Start with 10 emails/inbox on day 1, gradually increase
2. **Diversify sending**: 100 emails from 100 inboxes > 10,000 from 1 inbox
3. **Always send both HTML + text**: Improves deliverability
4. **No images in first email**: Triggers spam filters
5. **No links in first email**: Wait for reply, then send CTA
6. **Use custom domains**: Better reputation control

### Webhook Handling

Always return 200 immediately and process in background:

```python
@app.route("/webhooks", methods=["POST"])
def webhook():
    Thread(target=process, args=(request.json,)).start()
    return Response(status=200)  # Return immediately!
```

### Reply Extraction

Use `extracted_text` / `extracted_html` fields for clean reply content (removes quoted text):

```python
message = client.inboxes.messages.get(inbox_id, message_id)
clean_reply = message.extracted_text  # Just the new content
full_email = message.text  # Includes quoted replies
```

Or use Talon library for more control:

```python
from talon import quotations
clean = quotations.extract_from_plain(email_text)
```

## Critical Gotchas

1. **Bounced/complained addresses are permanently blocked** - AgentMail prevents sending to them to protect your reputation

2. **Keep bounce rate < 4%** - Or your account goes under review

3. **AWS Route 53 DKIM records** - Must split into two quoted strings with NO space:
   ```
   Correct: "first-part""second-part"
   Wrong:   "first-part" "second-part"  (space breaks it)
   ```

4. **Only one SPF record per domain** - Merge multiple services:
   ```
   v=spf1 include:spf.agentmail.to include:other.com ~all
   ```

5. **`message.received` is the only webhook with full Thread + Message data** - Other events have minimal metadata

6. **Pods cannot be deleted with existing resources** - Delete all inboxes/domains in the pod first

7. **Inboxes cannot be moved between pods** - Create new inbox in target pod

## IMAP/SMTP Access

For email client integration:

| Protocol | Host | Port | Auth |
|----------|------|------|------|
| IMAP | `imap.agentmail.to` | 993 (SSL) | inbox email + API key |
| SMTP | `smtp.agentmail.to` | 465 (SSL) | inbox email + API key |

## Additional Resources

- [API Reference](references/api-reference.md) - Complete method signatures
- [Webhook Events](references/webhook-events.md) - Event payloads
- [Advanced Examples](references/examples.md) - Agent patterns
- [Official Docs](https://docs.agentmail.to)
- [Console](https://console.agentmail.to)
