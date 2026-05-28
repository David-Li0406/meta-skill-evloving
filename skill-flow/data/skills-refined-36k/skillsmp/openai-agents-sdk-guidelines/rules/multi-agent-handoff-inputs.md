---
title: Capture LLM Data During Handoffs with input_type
impact: MEDIUM
impactDescription: Enables data capture at handoff time
tags: multi-agent, handoffs, input-type, data-capture
---

## Capture LLM Data During Handoffs with input_type

**Impact: MEDIUM (enables data capture at handoff time)**

Use `input_type` with `handoff()` to have the LLM provide structured data when making a handoff.

**Incorrect (no data captured):**

```python
from agents import Agent

escalation_agent = Agent(name="Escalation Agent", instructions="Handle escalations")

triage = Agent(
    name="Triage",
    handoffs=[escalation_agent],  # No context about why escalation happened
)
```

**Correct (capturing handoff data):**

```python
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str
    priority: str
    customer_sentiment: str

async def on_escalation(ctx: RunContextWrapper[None], input_data: EscalationData):
    # Log the escalation with full context
    print(f"Escalation: {input_data.reason}")
    print(f"Priority: {input_data.priority}")
    print(f"Sentiment: {input_data.customer_sentiment}")
    # Could also trigger alerts, create tickets, etc.

escalation_agent = Agent(
    name="Escalation Agent",
    instructions="Handle escalated customer issues with care.",
)

triage = Agent(
    name="Triage Agent",
    instructions="Help customers. Escalate if they are upset or the issue is complex.",
    handoffs=[
        handoff(
            agent=escalation_agent,
            input_type=EscalationData,
            on_handoff=on_escalation,
        )
    ],
)
```

**Use cases:**

- Logging reasons for handoffs
- Triggering side effects (alerts, tickets)
- Passing structured context to the receiving agent
- Analytics on handoff patterns

Reference: [Handoffs Documentation - Handoff Inputs](https://openai.github.io/openai-agents-python/handoffs/#handoff-inputs)
