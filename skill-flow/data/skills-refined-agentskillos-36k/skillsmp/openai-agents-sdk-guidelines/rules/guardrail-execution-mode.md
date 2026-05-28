---
title: Choose Parallel vs Blocking Guardrail Execution
impact: MEDIUM
impactDescription: Trade-off between latency and cost
tags: guardrail, execution-mode, parallel, blocking
---

## Choose Parallel vs Blocking Guardrail Execution

**Impact: MEDIUM (trade-off between latency and cost)**

Input guardrails can run in parallel with the agent (faster) or block until complete (cheaper if guardrail fails).

**Parallel execution (default - lower latency):**

```python
from agents import Agent, InputGuardrail, input_guardrail

@input_guardrail
async def fast_check(ctx, agent, input):
    # Runs concurrently with main agent
    ...

agent = Agent(
    name="Assistant",
    input_guardrails=[
        InputGuardrail(
            guardrail_function=fast_check,
            run_in_parallel=True,  # Default - guardrail and agent run together
        )
    ],
)
# If guardrail fails, agent may have already consumed tokens
```

**Blocking execution (cost optimization):**

```python
from agents import Agent, InputGuardrail, input_guardrail

@input_guardrail
async def strict_check(ctx, agent, input):
    # Runs BEFORE main agent starts
    ...

agent = Agent(
    name="Assistant",
    model="gpt-4o",  # Expensive model
    input_guardrails=[
        InputGuardrail(
            guardrail_function=strict_check,
            run_in_parallel=False,  # Blocking - agent waits for guardrail
        )
    ],
)
# If guardrail fails, expensive model never runs - saves money
```

**When to use each:**

| Mode | Use when |
|------|----------|
| Parallel (`True`) | Guardrail usually passes, latency matters |
| Blocking (`False`) | High failure rate, expensive main model, tool side-effects |

**Note:** Output guardrails always run after the agent completes, so they don't have this option.

Reference: [Guardrails Documentation - Execution Modes](https://openai.github.io/openai-agents-python/guardrails/#execution-modes)
