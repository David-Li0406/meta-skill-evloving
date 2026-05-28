---
title: Use Agents-as-Tools for Centralized Orchestration
impact: CRITICAL
impactDescription: Manager agent retains conversation control
tags: multi-agent, manager, orchestration, agents-as-tools
---

## Use Agents-as-Tools for Centralized Orchestration

**Impact: CRITICAL (manager agent retains conversation control)**

In the manager pattern, a central orchestrator invokes specialized agents as tools. The manager retains control of the conversation throughout.

**When to use:** When you need a single agent to coordinate multiple specialists while maintaining conversation context.

**Incorrect (no orchestration):**

```python
from agents import Agent, Runner

# Separate agents with no coordination
booking_agent = Agent(name="Booking", instructions="Handle bookings")
refund_agent = Agent(name="Refund", instructions="Handle refunds")

# User must manually decide which agent to call
result = await Runner.run(booking_agent, user_input)
```

**Correct (manager pattern with agents-as-tools):**

```python
from agents import Agent, Runner

booking_agent = Agent(
    name="Booking Agent",
    instructions="Handle booking requests. Return confirmation details.",
)

refund_agent = Agent(
    name="Refund Agent", 
    instructions="Handle refund requests. Return refund status.",
)

# Manager orchestrates specialists as tools
customer_facing_agent = Agent(
    name="Customer Service",
    instructions=(
        "Handle all customer interactions. "
        "Call booking_expert for reservations, refund_expert for refunds."
    ),
    tools=[
        booking_agent.as_tool(
            tool_name="booking_expert",
            tool_description="Handles booking questions and requests.",
        ),
        refund_agent.as_tool(
            tool_name="refund_expert",
            tool_description="Handles refund questions and requests.",
        ),
    ],
)

# Single entry point for all customer queries
result = await Runner.run(customer_facing_agent, "I want to cancel my booking")
```

**Benefits:**

- Manager maintains conversation context
- Centralized control over workflow
- Clear routing based on tool descriptions
- Sub-agents don't see full conversation history

Reference: [Agents Documentation - Manager Pattern](https://openai.github.io/openai-agents-python/agents/#manager-agents-as-tools)
