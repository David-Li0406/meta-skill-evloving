# Agent Creation Reference

Create AI agents with custom instructions, tools, and model configurations.

## Basic Agent

```python
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner
from agents.run import RunConfig
import os

# Setup provider and model
external_provider = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_provider,
    model="gemini-2.0-flash-exp",
)

config = RunConfig(
    model=model,
    model_provider=external_provider,
    tracing_disabled=True
)

# Create agent (no model specified - uses config)
agent = Agent(
    name="My Agent",
    instructions="You are a helpful assistant.",
)

# Run with config
result = await Runner.run(agent, "Hello!", config=config)
```

## Agent Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Agent name (required) |
| `instructions` | str | System prompt for the agent |
| `model` | Model | LLM model to use |
| `tools` | list | Function tools available to agent |
| `mcp_servers` | list | MCP servers to connect |
| `handoffs` | list | Agents to hand off to |
| `model_settings` | ModelSettings | Model configuration |
| `handoff_description` | str | Description for handoff tool |

## Agent with All Options

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"

agent = Agent(
    name="Full Agent",
    instructions="""You are a comprehensive assistant.

Available capabilities:
- Use tools to perform actions
- Hand off to specialists when needed
- Access MCP server resources""",
    tools=[my_tool],
    mcp_servers=[],  # Add MCP servers here
    handoffs=[],     # Add handoff agents here
    model_settings=ModelSettings(
        include_usage=True,
        tool_choice="auto",
    ),
    handoff_description="A general-purpose assistant",
)

# Note: Model is specified in RunConfig, not in Agent
```

## Running Agents

### Basic Run

```python
from agents import Runner

# Always pass config for non-OpenAI providers
result = await Runner.run(agent, "Hello, how are you?", config=config)
print(result.final_output)
```

### Run with Context

```python
result = await Runner.run(
    agent,
    input="Process this request",
    config=config,
    context_variables={"user_id": "user123"},
)
```

### Streamed Run

```python
result = Runner.run_streamed(agent, "Generate a story", config=config)

async for event in result.stream_events():
    if event.type == "run_item_stream_event":
        print(event.item, end="", flush=True)

print("\n" + result.final_output)
```

## Model Configuration

### Direct Gemini Integration

```python
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Gemini Flash (fast, efficient)
external_provider = AsyncOpenAI(
    api_key="your-google-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_provider,
    model="gemini-2.0-flash-exp",  # or "gemini-1.5-pro"
)

config = RunConfig(
    model=model,
    model_provider=external_provider,
    tracing_disabled=True
)
```

### Model Settings

```python
from agents import ModelSettings

settings = ModelSettings(
    include_usage=True,     # Track token usage
    tool_choice="auto",     # auto, required, none
    temperature=0.7,        # Creativity level
    max_tokens=1000,        # Max response length
)

agent = Agent(
    name="Agent",
    model_settings=settings,  # Model specified in RunConfig
)
```

## Conversation Management

### Multi-turn Conversations

```python
from agents import Runner

# First turn
result = await Runner.run(agent, "My name is Alice", config=config)

# Continue conversation with history
result = await Runner.run(
    agent,
    "What's my name?",
    config=config,
    context=result.context,  # Pass previous context
)
```

### Access Agent State

```python
result = await Runner.run(agent, "Hello", config=config)

# Check which agent responded
print(f"Agent: {result.current_agent.name}")

# Get token usage (if enabled)
if result.context_wrapper.usage:
    print(f"Tokens: {result.context_wrapper.usage.total_tokens}")
```

## Agent Instructions Best Practices

```python
agent = Agent(
    name="Task Assistant",
    instructions="""You are a task management assistant.

## Your Role
Help users create, organize, and complete tasks efficiently.

## Available Tools
- add_task: Create new tasks with title, description, priority
- list_tasks: View tasks filtered by status or priority
- complete_task: Mark tasks as done
- delete_task: Remove tasks

## Guidelines
1. Always confirm actions with the user
2. Summarize changes after performing actions
3. Suggest task organization when appropriate
4. Be concise but helpful

## Response Style
- Use bullet points for lists
- Keep responses focused and actionable
- Ask for clarification if needed""",
)
```

## Error Handling

```python
from agents import Runner

try:
    result = await Runner.run(agent, "Hello", config=config)
    print(result.final_output)
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

## Disable Tracing

```python
from agents.run import RunConfig

# Disable tracing in RunConfig
config = RunConfig(
    model=model,
    model_provider=external_provider,
    tracing_disabled=True  # Disable tracing
)
```
