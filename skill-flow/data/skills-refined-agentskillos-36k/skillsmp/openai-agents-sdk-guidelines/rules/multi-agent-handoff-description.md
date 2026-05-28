---
title: Add handoff_description for Better Routing
impact: HIGH
impactDescription: Improves LLM handoff decisions
tags: multi-agent, handoffs, routing, description
---

## Add handoff_description for Better Routing

**Impact: HIGH (improves LLM handoff decisions)**

Set `handoff_description` on specialist agents to help the triage agent make better routing decisions.

**Incorrect (no handoff description):**

```python
from agents import Agent

# LLM only sees agent names, routing may be inconsistent
math_agent = Agent(
    name="Math Tutor",
    instructions="Help with math problems",
)

history_agent = Agent(
    name="History Tutor",
    instructions="Help with history questions",
)

triage = Agent(
    name="Triage",
    instructions="Route to the appropriate tutor",
    handoffs=[math_agent, history_agent],
)
```

**Correct (with handoff descriptions):**

```python
from agents import Agent

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist for math problems including algebra, calculus, and geometry",
    instructions="Help with math problems. Show step-by-step solutions.",
)

history_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist for historical questions about events, dates, and figures",
    instructions="Help with history questions. Provide context and dates.",
)

triage = Agent(
    name="Triage Agent",
    instructions="Route students to the appropriate tutor based on their question",
    handoffs=[math_agent, history_agent],
)
```

**The handoff_description:**

- Appears in the tool description for the handoff
- Helps the LLM understand when to route to each agent
- Should be concise but specific about the agent's specialty
- Complements (doesn't replace) good instructions

Reference: [Handoffs Documentation](https://openai.github.io/openai-agents-python/handoffs/)
