---
title: Choose run() vs run_sync() Appropriately
impact: MEDIUM
impactDescription: Match execution style to your application
tags: runner, async, sync, execution
---

## Choose run() vs run_sync() Appropriately

**Impact: MEDIUM (match execution style to your application)**

The SDK provides three ways to run agents. Choose based on your application's async requirements.

**`Runner.run()` - Async (recommended for most cases):**

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="Help users")
    
    # Async - use in async applications
    result = await Runner.run(agent, "Hello")
    print(result.final_output)

asyncio.run(main())
```

**`Runner.run_sync()` - Sync wrapper:**

```python
from agents import Agent, Runner

# Sync - convenient for scripts, notebooks, simple apps
agent = Agent(name="Assistant", instructions="Help users")
result = Runner.run_sync(agent, "Hello")  # Blocks until complete
print(result.final_output)
```

**`Runner.run_streamed()` - Async with streaming:**

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="Help users")
    
    # Streaming - for real-time updates
    result = Runner.run_streamed(agent, "Tell me a story")
    
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            # Handle streaming tokens
            pass
    
    print(result.final_output)

asyncio.run(main())
```

**When to use each:**

| Method | Use case |
|--------|----------|
| `run()` | FastAPI, async web frameworks, concurrent operations |
| `run_sync()` | Scripts, Jupyter notebooks, sync frameworks |
| `run_streamed()` | Real-time UI updates, progress indicators |

**Note:** `run_sync()` internally calls `run()`, so it has the same capabilities.

Reference: [Running Agents Documentation](https://openai.github.io/openai-agents-python/running_agents/)
