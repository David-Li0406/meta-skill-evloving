---
title: Use Sessions for Automatic Conversation History
impact: MEDIUM
impactDescription: Simplified multi-turn conversation handling
tags: conversation, sessions, history, automatic
---

## Use Sessions for Automatic Conversation History

**Impact: MEDIUM (simplified multi-turn conversation handling)**

Use Sessions to automatically store and retrieve conversation history without manually calling `to_input_list()`.

**Without sessions (manual management):**

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="Reply concisely.")

# Must manually track conversation
result = await Runner.run(agent, "Hello")
conversation = result.to_input_list() + [{"role": "user", "content": "How are you?"}]
result = await Runner.run(agent, conversation)
```

**With SQLiteSession (automatic management):**

```python
from agents import Agent, Runner, SQLiteSession

agent = Agent(name="Assistant", instructions="Reply concisely.")

# Create session with unique ID
session = SQLiteSession("conversation_123")

# First turn - history automatically stored
result = await Runner.run(agent, "Hello", session=session)
print(result.final_output)

# Second turn - history automatically retrieved and updated
result = await Runner.run(agent, "How are you?", session=session)
print(result.final_output)  # Agent remembers the conversation

# Later, same session ID retrieves the history
session = SQLiteSession("conversation_123")
result = await Runner.run(agent, "What did I say first?", session=session)
# Agent can recall "Hello"
```

**Sessions automatically:**

- Retrieve conversation history before each run
- Store new messages after each run
- Maintain separate conversations by session ID

**Available session types:**

```python
from agents import SQLiteSession

# SQLite (default, good for development/single-instance)
session = SQLiteSession("conversation_id")

# Custom sessions can be implemented for:
# - Redis (distributed)
# - Database (PostgreSQL, MySQL)
# - In-memory (testing)
```

**Combining with tracing:**

```python
from agents.tracing import trace

session = SQLiteSession(user_id)

with trace(workflow_name="CustomerChat", group_id=user_id):
    result = await Runner.run(agent, message, session=session)
```

Reference: [Sessions Documentation](https://openai.github.io/openai-agents-python/sessions/)
