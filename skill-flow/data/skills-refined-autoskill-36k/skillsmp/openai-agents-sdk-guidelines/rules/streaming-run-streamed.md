---
title: Use run_streamed() for Real-Time Updates
impact: MEDIUM
impactDescription: Better UX with progressive output
tags: streaming, real-time, events, run_streamed
---

## Use run_streamed() for Real-Time Updates

**Impact: MEDIUM (better UX with progressive output)**

Use `Runner.run_streamed()` to receive events as the agent runs, enabling real-time UI updates and progress indicators.

**Basic streaming:**

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Storyteller",
        instructions="Tell engaging stories.",
    )
    
    result = Runner.run_streamed(agent, "Tell me a short story")
    
    async for event in result.stream_events():
        print(f"Event type: {event.type}")
    
    # After streaming, access final result
    print(f"Final output: {result.final_output}")

asyncio.run(main())
```

**Stream text tokens to user:**

```python
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def stream_response(agent: Agent, user_input: str):
    result = Runner.run_streamed(agent, user_input)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                # Print each token as it arrives
                print(event.data.delta, end="", flush=True)
    
    print()  # Newline after streaming
    return result.final_output
```

**Event types:**

| Type | Description |
|------|-------------|
| `raw_response_event` | Low-level LLM tokens |
| `run_item_stream_event` | High-level items (tool calls, messages) |
| `agent_updated_stream_event` | Agent changed (handoff occurred) |

**Streaming with tools:**

```python
from agents import Agent, Runner, ItemHelpers, function_tool

@function_tool
def get_data(query: str) -> str:
    """Fetch data."""
    return f"Data for {query}"

agent = Agent(name="Agent", tools=[get_data])
result = Runner.run_streamed(agent, "Get data for sales")

async for event in result.stream_events():
    if event.type == "run_item_stream_event":
        if event.item.type == "tool_call_item":
            print("Tool being called...")
        elif event.item.type == "tool_call_output_item":
            print(f"Tool output: {event.item.output}")
        elif event.item.type == "message_output_item":
            print(f"Message: {ItemHelpers.text_message_output(event.item)}")
```

Reference: [Streaming Documentation](https://openai.github.io/openai-agents-python/streaming/)
