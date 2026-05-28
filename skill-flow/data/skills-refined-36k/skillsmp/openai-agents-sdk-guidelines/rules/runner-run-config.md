---
title: Configure Global Settings with RunConfig
impact: MEDIUM
impactDescription: Centralized configuration for agent runs
tags: runner, config, settings, tracing
---

## Configure Global Settings with RunConfig

**Impact: MEDIUM (centralized configuration for agent runs)**

Use `RunConfig` to set global options that apply to all agents in a run, including model overrides, guardrails, and tracing.

**Basic usage:**

```python
from agents import Agent, Runner, RunConfig

agent = Agent(name="Assistant", model="gpt-4o-mini")

result = await Runner.run(
    agent,
    "Hello",
    run_config=RunConfig(
        model="gpt-4o",  # Override agent's model
        tracing_disabled=True,  # Disable tracing for this run
    ),
)
```

**Key RunConfig options:**

```python
from agents import RunConfig, ModelSettings

config = RunConfig(
    # Model overrides
    model="gpt-4o",  # Override all agents' models
    model_settings=ModelSettings(temperature=0.5),  # Override settings
    
    # Guardrails
    input_guardrails=[global_input_check],  # Add to all runs
    output_guardrails=[global_output_check],
    
    # Handoff configuration
    handoff_input_filter=my_filter,  # Global handoff filter
    
    # Tracing
    tracing_disabled=False,
    workflow_name="CustomerSupport",  # Name in trace viewer
    trace_id="trace_123",  # Custom trace ID
    group_id="session_456",  # Group related traces
    trace_include_sensitive_data=False,  # Redact inputs/outputs
    
    # History handling
    call_model_input_filter=trim_history,  # Edit input before LLM
)
```

**Workflow naming for traces:**

```python
# Named workflows are easier to find in the trace viewer
config = RunConfig(
    workflow_name="OrderProcessing",
    group_id=f"user_{user_id}",  # Group by user session
)

result = await Runner.run(agent, input, run_config=config)
```

**Input filter for history trimming:**

```python
from agents import RunConfig
from agents.run import CallModelData, ModelInputData

def keep_recent_history(data: CallModelData) -> ModelInputData:
    """Keep only the last 10 messages."""
    return ModelInputData(
        input=data.model_data.input[-10:],
        instructions=data.model_data.instructions,
    )

config = RunConfig(call_model_input_filter=keep_recent_history)
```

Reference: [Running Agents Documentation - Run Config](https://openai.github.io/openai-agents-python/running_agents/#run-config)
