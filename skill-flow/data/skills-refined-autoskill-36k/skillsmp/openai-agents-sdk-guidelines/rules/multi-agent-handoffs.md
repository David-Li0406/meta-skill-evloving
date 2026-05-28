---
title: Use Handoffs for Decentralized Agent Delegation
impact: CRITICAL
impactDescription: Enables modular, specialized agent workflows
tags: multi-agent, handoffs, delegation, routing
---

## Use Handoffs for Decentralized Agent Delegation

**Impact: CRITICAL (enables modular, specialized agent workflows)**

Handoffs transfer control from one agent to another. The receiving agent takes over the conversation and sees the full history.

**When to use:** When specialized agents should fully take over conversations in their domain.

**Incorrect (manual routing logic):**

```python
from agents import Agent, Runner

billing_agent = Agent(name="Billing", instructions="Handle billing")
support_agent = Agent(name="Support", instructions="Handle support")

# Manual routing - error-prone and doesn't scale
if "billing" in user_input.lower():
    result = await Runner.run(billing_agent, user_input)
else:
    result = await Runner.run(support_agent, user_input)
```

**Correct (using handoffs):**

```python
from agents import Agent, Runner

billing_agent = Agent(
    name="Billing Agent",
    handoff_description="Specialist for billing and payment questions",
    instructions="You handle all billing inquiries. Be precise about amounts.",
)

support_agent = Agent(
    name="Support Agent",
    handoff_description="Specialist for technical support",
    instructions="You handle technical issues. Ask for error messages.",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Route customers to the right specialist. "
        "Hand off to Billing Agent for payment issues, "
        "Support Agent for technical problems."
    ),
    handoffs=[billing_agent, support_agent],
)

# Triage automatically routes based on conversation
result = await Runner.run(triage_agent, "My payment didn't go through")
print(result.last_agent.name)  # "Billing Agent"
```

**Key differences from manager pattern:**

- Receiving agent takes full control
- Full conversation history is passed
- Decentralized decision making
- Handoffs are represented as tools (e.g., `transfer_to_billing_agent`)

Reference: [Handoffs Documentation](https://openai.github.io/openai-agents-python/handoffs/)
