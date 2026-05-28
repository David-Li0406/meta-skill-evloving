---
title: Use to_input_list() for Manual Conversation Management
impact: MEDIUM
impactDescription: Full control over conversation history
tags: conversation, history, manual, to_input_list
---

## Use to_input_list() for Manual Conversation Management

**Impact: MEDIUM (full control over conversation history)**

Use `result.to_input_list()` to get the conversation history and append new user messages for multi-turn conversations.

**Single turn (no history needed):**

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="Help users")
result = await Runner.run(agent, "What is 2+2?")
print(result.final_output)  # "4"
```

**Multi-turn with manual history:**

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="Reply concisely.")

# First turn
result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
print(result.final_output)  # "San Francisco"

# Second turn - include history
conversation = result.to_input_list() + [
    {"role": "user", "content": "What state is it in?"}
]
result = await Runner.run(agent, conversation)
print(result.final_output)  # "California"

# Third turn - continue building history
conversation = result.to_input_list() + [
    {"role": "user", "content": "What's the population?"}
]
result = await Runner.run(agent, conversation)
print(result.final_output)  # "~875,000 in the city proper"
```

**With tracing for the conversation:**

```python
from agents import Agent, Runner
from agents.tracing import trace

agent = Agent(name="Assistant", instructions="Reply concisely.")
thread_id = "conversation_123"

with trace(workflow_name="Chat", group_id=thread_id):
    # First turn
    result = await Runner.run(agent, "Hello!")
    
    # Second turn
    conversation = result.to_input_list() + [
        {"role": "user", "content": "How are you?"}
    ]
    result = await Runner.run(agent, conversation)
```

**When to use manual management:**

- Full control over history
- Custom history trimming/filtering
- Integration with existing conversation stores
- Debugging conversation flow

Reference: [Running Agents Documentation - Conversations](https://openai.github.io/openai-agents-python/running_agents/#conversationschat-threads)
