---
title: Use Pydantic Models for Structured Outputs
impact: CRITICAL
impactDescription: Enables type-safe structured responses
tags: agent, output, pydantic, structured-outputs
---

## Use Pydantic Models for Structured Outputs

**Impact: CRITICAL (enables type-safe structured responses)**

When you need structured data from an agent, use `output_type` with a Pydantic model. This enables structured outputs from the LLM.

**Incorrect (parsing unstructured text):**

```python
from agents import Agent, Runner

agent = Agent(
    name="Event Extractor",
    instructions="Extract calendar events from text. Return as JSON.",
)

result = await Runner.run(agent, "Meeting with John tomorrow at 2pm")
# result.final_output is a string that needs manual parsing
import json
event = json.loads(result.final_output)  # Error-prone
```

**Correct (using output_type):**

```python
from pydantic import BaseModel
from agents import Agent, Runner

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Event Extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)

result = await Runner.run(agent, "Meeting with John tomorrow at 2pm")
event = result.final_output  # Already a CalendarEvent instance
print(event.name, event.date, event.participants)
```

**Supported types:**

- Pydantic `BaseModel` subclasses
- `dataclasses`
- `TypedDict`
- Any type wrappable in Pydantic `TypeAdapter`

Reference: [Agents Documentation - Output Types](https://openai.github.io/openai-agents-python/agents/#output-types)
