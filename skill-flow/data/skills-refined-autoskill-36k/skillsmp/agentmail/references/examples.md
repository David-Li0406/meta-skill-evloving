# AgentMail Advanced Examples

Advanced patterns for building email agents.

## Pattern 1: Event-Driven Agent (Webhook)

A complete agent that responds to incoming emails using webhooks.

```python
import os
import asyncio
from threading import Thread
from flask import Flask, request, Response
import ngrok
from agentmail import AgentMail
from agentmail_toolkit.openai import AgentMailToolkit
from agents import Agent, Runner

app = Flask(__name__)
client = AgentMail()
port = 8080

inbox_username = "support-agent"
inbox = f"{inbox_username}@agentmail.to"

# Setup infrastructure idempotently
client.inboxes.create(username=inbox_username, client_id=f"{inbox_username}-inbox")

listener = ngrok.forward(port, authtoken_from_env=True)
webhook_url = f"{listener.url()}/webhooks"
client.webhooks.create(
    url=webhook_url,
    event_types=["message.received"],
    client_id=f"{inbox_username}-webhook"
)

# Define agent
agent = Agent(
    name="Support Agent",
    instructions=f"""You are a helpful support agent. Your email is {inbox}.
    When you receive an email, respond helpfully and professionally.
    Always be concise and address the user's question directly.""",
    tools=AgentMailToolkit(client).get_tools()
)

messages = []

@app.route("/webhooks", methods=["POST"])
def receive_webhook():
    Thread(target=process_webhook, args=(request.json,)).start()
    return Response(status=200)

def process_webhook(payload):
    global messages
    email = payload["message"]
    
    prompt = f"""
    New email received:
    From: {email["from_"]}
    Subject: {email["subject"]}
    Body: {email["text"]}
    """
    
    response = asyncio.run(Runner.run(agent, messages + [{"role": "user", "content": prompt}]))
    
    # Reply to the email
    client.inboxes.messages.reply(
        inbox_id=inbox,
        message_id=email["message_id"],
        html=response.final_output
    )
    
    messages = response.to_input_list()

if __name__ == "__main__":
    print(f"Inbox: {inbox}")
    print(f"Webhook: {webhook_url}")
    app.run(port=port)
```

## Pattern 2: WebSocket Real-time Agent

No public URL required - uses persistent WebSocket connection.

```python
import asyncio
from agentmail import AsyncAgentMail, Subscribe, MessageReceivedEvent
from openai import OpenAI

client = AsyncAgentMail()
openai = OpenAI()
inbox = "realtime-agent@agentmail.to"

async def handle_email(event: MessageReceivedEvent):
    message = event.message
    
    # Generate response with OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful email assistant."},
            {"role": "user", "content": f"Reply to this email:\n\n{message.text}"}
        ]
    )
    
    reply_text = response.choices[0].message.content
    
    # Send reply
    await client.inboxes.messages.reply(
        inbox_id=inbox,
        message_id=message.message_id,
        text=reply_text
    )
    print(f"Replied to {message.from_}")

async def main():
    # Create inbox if needed
    await client.inboxes.create(username="realtime-agent", client_id="realtime-agent-inbox")
    
    async with client.websockets.connect() as socket:
        await socket.send_subscribe(Subscribe(inbox_ids=[inbox]))
        print(f"Listening for emails to {inbox}...")
        
        async for event in socket:
            if isinstance(event, MessageReceivedEvent):
                await handle_email(event)

asyncio.run(main())
```

## Pattern 3: Multi-Step Workflow with State

State management for complex workflows (e.g., collecting RSVPs).

```python
from flask import Flask, request, Response
from threading import Thread
from agentmail import AgentMail

app = Flask(__name__)
client = AgentMail()

# In-memory state (use database in production)
events = {}

def create_event(organizer_email, details):
    event_id = f"event_{len(events)}"
    events[event_id] = {
        "state": "collecting",  # collecting | ready | completed
        "organizer": organizer_email,
        "details": details,
        "rsvps": [],
        "target_count": 5
    }
    return event_id

def handle_rsvp(event_id, from_email, response):
    event = events.get(event_id)
    if not event or event["state"] != "collecting":
        return
    
    event["rsvps"].append({"email": from_email, "response": response})
    
    # Check if we hit the target
    yes_count = len([r for r in event["rsvps"] if r["response"] == "yes"])
    if yes_count >= event["target_count"]:
        event["state"] = "ready"
        notify_organizer(event)

def notify_organizer(event):
    client.inboxes.messages.send(
        inbox_id="event-agent@agentmail.to",
        to=[event["organizer"]],
        subject="Your event is ready!",
        text=f"You have {len(event['rsvps'])} RSVPs."
    )

@app.route("/webhooks", methods=["POST"])
def webhook():
    Thread(target=process, args=(request.json,)).start()
    return Response(status=200)

def process(payload):
    message = payload["message"]
    subject = message.get("subject", "")
    text = message.get("text", "").lower()
    from_email = message["from_"]
    
    # Parse event ID from subject (e.g., "Re: [event_123] Dinner Invitation")
    if "[event_" in subject:
        event_id = subject.split("[")[1].split("]")[0]
        
        if "yes" in text:
            handle_rsvp(event_id, from_email, "yes")
        elif "no" in text:
            handle_rsvp(event_id, from_email, "no")

if __name__ == "__main__":
    app.run(port=8080)
```

## Pattern 4: Human-in-the-Loop with Drafts

Agent creates drafts for human approval before sending.

```python
from agentmail import AgentMail

client = AgentMail()
inbox = "sales-agent@agentmail.to"

def create_outreach_draft(prospect_email, personalization):
    """Agent creates draft, human reviews and sends."""
    
    draft = client.inboxes.drafts.create(
        inbox_id=inbox,
        to=[prospect_email],
        subject="Quick question about your company",
        text=f"""Hi,

{personalization}

Would you be open to a quick call this week?

Best,
Sales Agent""",
        labels=["pending-review", "outreach"]
    )
    
    print(f"Draft created: {draft.draft_id}")
    return draft.draft_id

def list_pending_drafts():
    """Human reviews drafts."""
    drafts = client.drafts.list(labels=["pending-review"])
    for draft in drafts.drafts:
        print(f"To: {draft.to}, Subject: {draft.subject}")
    return drafts

def approve_and_send(draft_id):
    """Human approves, agent sends."""
    # Update labels
    client.inboxes.drafts.update(
        inbox_id=inbox,
        draft_id=draft_id,
        add_labels=["approved"],
        remove_labels=["pending-review"]
    )
    
    # Send the draft
    result = client.inboxes.drafts.send(inbox_id=inbox, draft_id=draft_id)
    print(f"Sent as message: {result.message_id}")
```

## Pattern 5: Label-Based Workflow

Using labels for state machine and filtering.

```python
from agentmail import AgentMail

client = AgentMail()
inbox = "workflow@agentmail.to"

# Label conventions:
# - status:new, status:in-progress, status:resolved
# - priority:high, priority:low
# - category:billing, category:technical, category:general

def process_new_tickets():
    """Process all new tickets."""
    new_messages = client.inboxes.messages.list(
        inbox_id=inbox,
        labels=["status:new"]
    )
    
    for msg in new_messages.messages:
        # Classify and update
        category = classify_email(msg.text)
        priority = assess_priority(msg.text)
        
        client.inboxes.messages.update(
            inbox_id=inbox,
            message_id=msg.message_id,
            add_labels=[f"category:{category}", f"priority:{priority}", "status:in-progress"],
            remove_labels=["status:new"]
        )

def get_high_priority():
    """Get high priority items."""
    return client.inboxes.threads.list(
        inbox_id=inbox,
        labels=["priority:high", "status:in-progress"]
    )

def resolve_ticket(message_id, resolution):
    """Mark ticket as resolved."""
    # Send resolution
    client.inboxes.messages.reply(
        inbox_id=inbox,
        message_id=message_id,
        text=resolution
    )
    
    # Update status
    client.inboxes.messages.update(
        inbox_id=inbox,
        message_id=message_id,
        add_labels=["status:resolved"],
        remove_labels=["status:in-progress"]
    )

def classify_email(text):
    # Use AI or rules to classify
    if "invoice" in text.lower() or "payment" in text.lower():
        return "billing"
    elif "error" in text.lower() or "bug" in text.lower():
        return "technical"
    return "general"

def assess_priority(text):
    if "urgent" in text.lower() or "asap" in text.lower():
        return "high"
    return "low"
```

## Pattern 6: Multi-Tenant with Pods

Isolating resources per customer.

```python
from agentmail import AgentMail

client = AgentMail()

def onboard_customer(customer_id, domain):
    """Set up isolated email infrastructure for a customer."""
    
    # Create pod for isolation
    pod = client.pods.create(
        name=f"Customer {customer_id}",
        client_id=f"pod-{customer_id}"
    )
    
    # Create inbox in pod
    inbox = client.pods.inboxes.create(
        pod_id=pod.pod_id,
        username="support",
        domain=domain,
        client_id=f"inbox-{customer_id}-support"
    )
    
    # Add custom domain (optional)
    domain_obj = client.pods.domains.create(
        pod_id=pod.pod_id,
        domain=domain,
        feedback_enabled=True
    )
    
    return {
        "pod_id": pod.pod_id,
        "inbox": inbox.inbox_id,
        "domain_status": domain_obj.status
    }

def get_customer_threads(pod_id):
    """Get all threads for a customer."""
    return client.pods.threads.list(pod_id=pod_id)

def offboard_customer(pod_id):
    """Clean up customer resources."""
    # Must delete resources before pod
    
    # Delete inboxes
    inboxes = client.pods.inboxes.list(pod_id=pod_id)
    for inbox in inboxes.inboxes:
        client.inboxes.delete(inbox.inbox_id)
    
    # Delete domains
    domains = client.pods.domains.list(pod_id=pod_id)
    for domain in domains.domains:
        client.domains.delete(domain.domain_id)
    
    # Now delete pod
    client.pods.delete(pod_id)
```

## Pattern 7: Attachment Processing

Download and process email attachments.

```python
from agentmail import AgentMail
import base64

client = AgentMail()
inbox = "processor@agentmail.to"

def process_incoming_attachments(message_id):
    """Download and process all attachments from a message."""
    
    message = client.inboxes.messages.get(inbox_id=inbox, message_id=message_id)
    
    results = []
    for attachment in message.attachments or []:
        # Download attachment
        content = client.inboxes.messages.get_attachment(
            inbox_id=inbox,
            message_id=message_id,
            attachment_id=attachment.attachment_id
        )
        
        # Save to file
        with open(attachment.filename, "wb") as f:
            for chunk in content:
                f.write(chunk)
        
        results.append({
            "filename": attachment.filename,
            "size": attachment.size,
            "type": attachment.content_type
        })
        
        print(f"Downloaded: {attachment.filename}")
    
    return results

def send_with_multiple_attachments(to, files):
    """Send email with multiple attachments."""
    
    attachments = []
    for filepath in files:
        with open(filepath, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        
        filename = filepath.split("/")[-1]
        attachments.append({
            "content": content,
            "filename": filename,
            "content_type": guess_mime_type(filename)
        })
    
    client.inboxes.messages.send(
        inbox_id=inbox,
        to=[to],
        subject="Files attached",
        text="Please see the attached files.",
        attachments=attachments
    )

def guess_mime_type(filename):
    ext = filename.split(".")[-1].lower()
    types = {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "csv": "text/csv",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
    return types.get(ext, "application/octet-stream")
```

## Pattern 8: TypeScript Examples

### Webhook Handler (Express)

```typescript
import express from "express";
import { AgentMailClient } from "agentmail";

const app = express();
const client = new AgentMailClient();

app.use(express.json());

app.post("/webhooks", async (req, res) => {
  res.status(200).send();  // Return immediately
  
  const { event_type, message } = req.body;
  
  if (event_type === "message.received") {
    await client.inboxes.messages.reply(message.inbox_id, message.message_id, {
      text: "Thanks for your email!"
    });
  }
});

app.listen(8080);
```

### WebSocket Listener

```typescript
import { AgentMailClient, AgentMail } from "agentmail";

const client = new AgentMailClient();

async function main() {
  const socket = await client.websockets.connect();
  
  socket.on("open", () => {
    socket.sendSubscribe({
      type: "subscribe",
      inboxIds: ["agent@agentmail.to"]
    });
  });
  
  socket.on("message", async (event: AgentMail.MessageReceivedEvent) => {
    if (event.type === "message_received") {
      console.log(`New email: ${event.message.subject}`);
      
      await client.inboxes.messages.reply(
        event.message.inboxId,
        event.message.messageId,
        { text: "Got it!" }
      );
    }
  });
}

main();
```
