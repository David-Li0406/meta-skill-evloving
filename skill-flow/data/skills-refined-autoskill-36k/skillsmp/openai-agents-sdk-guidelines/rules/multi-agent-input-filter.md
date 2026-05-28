---
title: Filter Conversation History on Handoffs
impact: MEDIUM
impactDescription: Controls what context the next agent sees
tags: multi-agent, handoffs, input-filter, history
---

## Filter Conversation History on Handoffs

**Impact: MEDIUM (controls what context the next agent sees)**

Use `input_filter` to modify the conversation history before passing it to the next agent on handoff.

**Default behavior (full history passed):**

```python
from agents import Agent

specialist = Agent(name="Specialist", instructions="Handle specialized tasks")
triage = Agent(
    name="Triage",
    handoffs=[specialist],  # Specialist sees entire conversation
)
```

**Correct (filtering history):**

```python
from agents import Agent, handoff
from agents.extensions import handoff_filters

# Remove all tool calls from history
specialist = Agent(name="Specialist", instructions="Handle tasks")

triage = Agent(
    name="Triage",
    handoffs=[
        handoff(
            agent=specialist,
            input_filter=handoff_filters.remove_all_tools,
        )
    ],
)
```

**Custom input filter:**

```python
from agents import Agent, handoff
from agents.handoffs import HandoffInputData

def custom_filter(input_data: HandoffInputData) -> HandoffInputData:
    # Keep only the last 5 messages
    filtered_history = input_data.history[-5:] if input_data.history else []
    return HandoffInputData(
        history=filtered_history,
        pre_handoff_items=input_data.pre_handoff_items,
        new_items=input_data.new_items,
    )

specialist = Agent(name="Specialist", instructions="Handle tasks")

triage = Agent(
    name="Triage",
    handoffs=[
        handoff(agent=specialist, input_filter=custom_filter)
    ],
)
```

**Built-in filters in `agents.extensions.handoff_filters`:**

- `remove_all_tools`: Removes tool calls from history
- More filters available for common patterns

Reference: [Handoffs Documentation - Input Filters](https://openai.github.io/openai-agents-python/handoffs/#input-filters)
