---
title: Validate User Input with Input Guardrails
impact: HIGH
impactDescription: Prevents misuse and saves costs
tags: guardrail, input, validation, security
---

## Validate User Input with Input Guardrails

**Impact: HIGH (prevents misuse and saves costs)**

Input guardrails validate user input before the main agent runs. They can block inappropriate requests, saving expensive model calls.

**Incorrect (no input validation):**

```python
from agents import Agent, Runner

# No validation - any input goes to expensive model
agent = Agent(
    name="Customer Support",
    model="gpt-4o",  # Expensive model
    instructions="Help customers with product questions.",
)

# Malicious user could ask unrelated questions, wasting resources
result = await Runner.run(agent, "Help me with my math homework")
```

**Correct (input guardrail):**

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    Runner,
    RunContextWrapper,
    input_guardrail,
)
from agents.exceptions import InputGuardrailTripwireTriggered

class TopicCheck(BaseModel):
    is_on_topic: bool
    reasoning: str

guardrail_agent = Agent(
    name="Topic Checker",
    model="gpt-4o-mini",  # Cheap model for validation
    instructions="Check if the query is about our products or customer service.",
    output_type=TopicCheck,
)

@input_guardrail
async def topic_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str,
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    output = result.final_output
    
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=not output.is_on_topic,
    )

main_agent = Agent(
    name="Customer Support",
    model="gpt-4o",
    instructions="Help customers with product questions.",
    input_guardrails=[topic_guardrail],
)

try:
    result = await Runner.run(main_agent, "Help me with math homework")
except InputGuardrailTripwireTriggered:
    print("Sorry, I can only help with product-related questions.")
```

**Important:** Input guardrails only run on the **first** agent in a workflow.

Reference: [Guardrails Documentation](https://openai.github.io/openai-agents-python/guardrails/)
