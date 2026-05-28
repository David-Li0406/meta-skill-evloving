---
title: Use Server-Managed Conversations for Stateless Apps
impact: MEDIUM
impactDescription: No local state storage needed
tags: conversation, server-managed, stateless, conversation_id
---

## Use Server-Managed Conversations for Stateless Apps

**Impact: MEDIUM (no local state storage needed)**

Let OpenAI's servers manage conversation state using `conversation_id` or `previous_response_id`, eliminating local storage requirements.

**Using conversation_id:**

```python
from agents import Agent, Runner
from openai import AsyncOpenAI

client = AsyncOpenAI()
agent = Agent(name="Assistant", instructions="Reply concisely.")

# Create a server-managed conversation
conversation = await client.conversations.create()
conv_id = conversation.id

# All turns use the same conversation_id
result = await Runner.run(agent, "Hello", conversation_id=conv_id)
print(result.final_output)

result = await Runner.run(agent, "How are you?", conversation_id=conv_id)
print(result.final_output)  # Server maintains history

# Works across restarts - just keep the conv_id
```

**Using previous_response_id (response chaining):**

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="Reply concisely.")
previous_response_id = None

# First turn
result = await Runner.run(
    agent,
    "Hello",
    previous_response_id=previous_response_id,
    auto_previous_response_id=True,  # Enable chaining
)
previous_response_id = result.last_response_id

# Second turn - chains from previous
result = await Runner.run(
    agent,
    "How are you?",
    previous_response_id=previous_response_id,
    auto_previous_response_id=True,
)
previous_response_id = result.last_response_id
```

**Comparison:**

| Method | Storage | Use case |
|--------|---------|----------|
| `to_input_list()` | Client | Full control, custom filtering |
| `Sessions` | Local DB | Persistent, single instance |
| `conversation_id` | OpenAI servers | Stateless apps, distributed |
| `previous_response_id` | None | Lightweight chaining |

**When to use server-managed:**

- Stateless/serverless deployments
- Distributed systems (multiple instances)
- Don't want to manage conversation storage
- Long conversations (avoid large payloads)

Reference: [OpenAI Conversation State Guide](https://platform.openai.com/docs/guides/conversation-state?api-mode=responses)
