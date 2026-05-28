# Agent Handoffs Reference

Create specialized agents that can hand off conversations to each other.

## Basic Handoff

```python
from agents import Agent, handoff
from agents.extensions.models.litellm_model import LitellmModel

# Specialized agents
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing and payment questions.",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key="..."),
)

support_agent = Agent(
    name="Support Agent",
    instructions="You handle technical support questions.",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key="..."),
)

# Triage agent with handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions="""Route users to the right agent:
- Billing Agent: payment, invoices, subscriptions
- Support Agent: technical issues, bugs, help""",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key="..."),
    handoffs=[billing_agent, support_agent],
)
```

## Using `handoff()` Function

For more control, wrap agents with `handoff()`:

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing Agent", ...)

# Basic handoff
handoff_obj = handoff(billing_agent)

# Handoff with callback
def on_billing_handoff(ctx):
    print(f"Handing off to billing: {ctx}")

handoff_obj = handoff(
    agent=billing_agent,
    on_handoff=on_billing_handoff,
)

# Handoff with custom tool name
handoff_obj = handoff(
    agent=billing_agent,
    tool_name_override="transfer_to_billing",
    tool_description_override="Transfer the user to billing support",
)

triage_agent = Agent(
    name="Triage",
    handoffs=[handoff_obj],
    ...
)
```

## Handoff Instructions

Use `prompt_with_handoff_instructions` for better handoff behavior:

```python
from agents import Agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

billing_agent = Agent(
    name="Billing Agent",
    instructions=prompt_with_handoff_instructions(
        """You are a billing specialist.

Handle:
- Payment processing
- Invoice questions
- Subscription management
- Refund requests

Be professional and helpful with financial matters."""
    ),
    model=model,
)
```

Or use the prefix directly:

```python
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

agent = Agent(
    name="Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Your specific instructions here...""",
)
```

## Handoff Input Filters

Control what context is passed during handoff:

```python
from agents import Agent, handoff
from agents.extensions import handoff_filters

# Remove all tool calls from history
clean_handoff = handoff(
    agent=billing_agent,
    input_filter=handoff_filters.remove_all_tools,
)

triage_agent = Agent(
    name="Triage",
    handoffs=[clean_handoff],
    ...
)
```

## Multi-Level Handoffs

Agents can hand off to agents that also have handoffs:

```python
# Level 3 - Specialists
refund_agent = Agent(
    name="Refund Specialist",
    instructions="Handle refund requests only.",
    model=model,
)

payment_agent = Agent(
    name="Payment Specialist",
    instructions="Handle payment processing only.",
    model=model,
)

# Level 2 - Department
billing_agent = Agent(
    name="Billing",
    instructions="Handle billing. Route to specialists as needed.",
    handoffs=[refund_agent, payment_agent],
    model=model,
)

# Level 1 - Triage
triage_agent = Agent(
    name="Triage",
    instructions="Route to appropriate department.",
    handoffs=[billing_agent, support_agent],
    model=model,
)
```

## Checking Handoff Results

```python
from agents import Runner

result = await Runner.run(triage_agent, "I need a refund")

# Check which agent handled the request
print(f"Final agent: {result.current_agent.name}")
# Output: "Refund Specialist"

print(result.final_output)
```

## Todo App Handoff Pattern

```python
from agents import Agent, handoff
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

# Task management agent
task_agent = Agent(
    name="Task Agent",
    instructions=prompt_with_handoff_instructions(
        """You specialize in task management.

Use MCP tools to:
- add_task: Create tasks
- list_tasks: View tasks
- complete_task: Mark done
- update_task: Modify tasks
- delete_task: Remove tasks

Always confirm actions with the user."""
    ),
    mcp_servers=[task_server],
    model=model,
)

# Help agent
help_agent = Agent(
    name="Help Agent",
    instructions=prompt_with_handoff_instructions(
        """You provide help about the todo app.

Explain:
- How to create tasks
- How to organize tasks
- How to use priorities
- Tips for productivity"""
    ),
    model=model,
)

# Main assistant
assistant = Agent(
    name="Todo Assistant",
    instructions=prompt_with_handoff_instructions(
        """You are the main todo app assistant.

Route users to:
- Task Agent: creating, viewing, updating tasks
- Help Agent: questions about how to use the app

For simple greetings, respond directly."""
    ),
    handoffs=[task_agent, help_agent],
    model=model,
)
```

## Best Practices

1. **Clear handoff criteria** - Define when to hand off in instructions
2. **Use specialized agents** - Each agent should excel at one thing
3. **Include handoff instructions** - Use `prompt_with_handoff_instructions`
4. **Test handoff paths** - Verify routing works as expected
5. **Keep hierarchies shallow** - 2-3 levels max for performance
6. **Pass necessary context** - Ensure agents have info they need
