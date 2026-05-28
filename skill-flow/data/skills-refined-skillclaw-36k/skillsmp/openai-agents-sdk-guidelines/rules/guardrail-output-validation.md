---
title: Validate Agent Output with Output Guardrails
impact: HIGH
impactDescription: Ensures response quality and safety
tags: guardrail, output, validation, quality
---

## Validate Agent Output with Output Guardrails

**Impact: HIGH (ensures response quality and safety)**

Output guardrails validate the agent's response before returning it to the user. Use them to check for quality, safety, or format compliance.

**Incorrect (no output validation):**

```python
from agents import Agent, Runner

agent = Agent(
    name="Content Writer",
    instructions="Write blog posts on any topic.",
)

# No validation - agent might produce inappropriate content
result = await Runner.run(agent, "Write about a controversial topic")
```

**Correct (output guardrail):**

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    RunContextWrapper,
    output_guardrail,
)
from agents.exceptions import OutputGuardrailTripwireTriggered

class ContentOutput(BaseModel):
    content: str

class SafetyCheck(BaseModel):
    is_safe: bool
    issues: list[str]

safety_agent = Agent(
    name="Safety Checker",
    model="gpt-4o-mini",
    instructions="Check if content is appropriate for all audiences.",
    output_type=SafetyCheck,
)

@output_guardrail
async def safety_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: ContentOutput,
) -> GuardrailFunctionOutput:
    result = await Runner.run(safety_agent, output.content, context=ctx.context)
    check = result.final_output
    
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.is_safe,
    )

writer_agent = Agent(
    name="Content Writer",
    instructions="Write helpful blog posts.",
    output_type=ContentOutput,
    output_guardrails=[safety_guardrail],
)

try:
    result = await Runner.run(writer_agent, "Write about healthy eating")
    print(result.final_output.content)
except OutputGuardrailTripwireTriggered as e:
    print(f"Content blocked: {e.guardrail_result.output.output_info.issues}")
```

**Important:** Output guardrails only run on the **last** agent in a workflow.

Reference: [Guardrails Documentation](https://openai.github.io/openai-agents-python/guardrails/)
