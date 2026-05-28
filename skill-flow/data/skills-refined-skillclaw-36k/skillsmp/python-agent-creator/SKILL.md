---
name: python-agent-creator
description: This skill helps create Python agents using the openai-agents package, following best practices for agent definition and configuration.
---

# Python Agent Creator

This skill helps create Python agents using the openai-agents package, following best practices for agent definition and configuration.

## Usage Instructions

When a user needs to create agents for their Python project, use this skill to generate:

1. Agent definitions with proper configuration
2. Function tools with appropriate decorators
3. System instructions for agent behavior
4. Tool integration and model selection
5. Agent handoff configurations when needed

## Best Practices to Follow

- Import `Agent` and `function_tool` from the `agents` package
- Use the `@function_tool` decorator for functions that should be available as tools
- Provide clear, descriptive docstrings for all tools
- Use appropriate type hints for function parameters and return values
- Choose descriptive names for agents that reflect their purpose
- Select appropriate models based on use case requirements
- Include comprehensive instructions that define the agent's role and behavior
- Organize tools in a list and attach them to the agent
- Use proper error handling in tool functions

## Template Structure

### Basic Agent:
```python
from agents import Agent, function_tool

@function_tool
def tool_name(param: type) -> type:
    """Clear description of what the tool does.

    Args:
        param (type): Description of parameter

    Returns:
        type: Description of return value
    """
    # Tool implementation
    return result

agent = Agent(
    name="Agent Name",
    model="model-identifier",
    tools=[tool_name],
    instructions="System instructions for the agent"
)
```

### Advanced Agent with Handoffs:
```python
from agents import Agent, function_tool

@function_tool
def example_tool(param: int) -> str:
    """Example tool description."""
    return f"Processed: {param}"

secondary_agent = Agent(
    name="Secondary Agent",
    model="model-identifier",
    tools=[example_tool],
    handoff_description="Description for when to hand off to this agent"
)

primary_agent = Agent(
    name="Primary Agent",
    model="model-identifier",
    tools=[example_tool],
    handoffs=[secondary_agent],
    instructions="System instructions for the primary agent"
)
```

### Agent with Guardrails:
```python
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
)
from typing import Any

@input_guardrail
async def input_guard(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    # Add your input validation logic here
    return GuardrailFunctionOutput(
        output_info=input,  # Return the input as is or modified
        tripwire_triggered=True if "block_this" in str(input) else False  # Set to True to block, False to allow
    )

@output_guardrail
async def output_guard(context: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    # Add your output validation logic here
    return GuardrailFunctionOutput(
        output_info=output,  # Return the output as is or modified
        tripwire_triggered=True if "block_this" in str(output) else False  # Set to True to block, False to allow
    )

agent = Agent(
    name="Agent with Guardrails",
    model="model-identifier",
    tools=[],
    input_guardrails=[input_guard],
    output_guardrails=[output_guard],
    instructions="System instructions for the agent"
)

# Running the agent
try:
    result = Runner.run_sync(starting_agent=agent, input="Your input here")
    print(f"Agent response: {result}")
except InputGuardrailTripwireTriggered:
    print("Input was blocked by guardrails")
except OutputGuardrailTripwireTriggered:
    print("Output was blocked by guardrails")
```

## Common Agent Categories

- Customer support assistants
- Educational tutors
- Data analysis agents
- Content creation assistants
- Task management helpers
- Research assistants
- Technical support agents

## Tool Creation Guidelines

- Tools should be self-contained functions
- Use descriptive names that clearly indicate the tool's purpose
- Include comprehensive docstrings with Args and Returns sections
- Handle potential errors gracefully within tools
- Keep tool functionality focused and single-purpose
- Use appropriate type hints for all parameters and return values

## Output Requirements

1. Generate complete, working agent definitions
2. Include properly decorated function tools
3. Add helpful comments explaining agent configuration
4. Follow the exact patterns shown in the templates
5. Ensure agents are easily extensible with additional tools
