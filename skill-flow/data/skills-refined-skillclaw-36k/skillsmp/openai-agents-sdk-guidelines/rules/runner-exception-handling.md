---
title: Handle SDK Exceptions Properly
impact: HIGH
impactDescription: Robust error handling for production apps
tags: runner, exceptions, error-handling, production
---

## Handle SDK Exceptions Properly

**Impact: HIGH (robust error handling for production apps)**

The SDK raises specific exceptions for different error conditions. Handle them appropriately for robust applications.

**Key exceptions to handle:**

```python
from agents import Agent, Runner
from agents.exceptions import (
    AgentsException,          # Base class for all SDK exceptions
    MaxTurnsExceeded,         # Agent exceeded max_turns limit
    ModelBehaviorError,       # LLM produced invalid output
    UserError,                # SDK usage error (your code)
    InputGuardrailTripwireTriggered,   # Input guardrail failed
    OutputGuardrailTripwireTriggered,  # Output guardrail failed
)

async def run_agent_safely(agent: Agent, user_input: str):
    try:
        result = await Runner.run(agent, user_input, max_turns=10)
        return result.final_output
        
    except InputGuardrailTripwireTriggered as e:
        # User input was blocked by guardrail
        return f"I can't help with that: {e.guardrail_result.output.output_info}"
        
    except OutputGuardrailTripwireTriggered as e:
        # Agent output was blocked
        return "I generated a response but it was flagged for review."
        
    except MaxTurnsExceeded as e:
        # Agent took too long
        # Could access partial results via e.last_result
        return "This request is taking too long. Please try a simpler question."
        
    except ModelBehaviorError as e:
        # LLM produced malformed output (bad JSON, unexpected format)
        # Log for debugging, return user-friendly message
        logger.error(f"Model behavior error: {e}")
        return "I had trouble processing that. Please try again."
        
    except UserError as e:
        # SDK was used incorrectly (your bug)
        logger.error(f"SDK usage error: {e}")
        raise  # Re-raise - this should be fixed in code
        
    except AgentsException as e:
        # Catch-all for other SDK exceptions
        logger.error(f"Agent error: {e}")
        return "Something went wrong. Please try again."
```

**Accessing partial results:**

```python
try:
    result = await Runner.run(agent, input, max_turns=5)
except MaxTurnsExceeded as e:
    # Access what was completed before hitting the limit
    partial = e.last_result
    print(f"Completed items: {len(partial.new_items)}")
    print(f"Last agent: {partial.last_agent.name}")
```

**When each exception occurs:**

| Exception | Cause |
|-----------|-------|
| `MaxTurnsExceeded` | Agent loop exceeded `max_turns` |
| `ModelBehaviorError` | LLM returned malformed JSON or invalid tool calls |
| `UserError` | Invalid SDK usage (wrong types, missing params) |
| `InputGuardrailTripwireTriggered` | Input guardrail blocked the request |
| `OutputGuardrailTripwireTriggered` | Output guardrail blocked the response |

Reference: [Running Agents Documentation - Exceptions](https://openai.github.io/openai-agents-python/running_agents/#exceptions)
