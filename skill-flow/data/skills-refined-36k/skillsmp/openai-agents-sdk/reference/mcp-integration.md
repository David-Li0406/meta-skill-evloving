# MCP Server Integration Reference

Connect OpenAI Agents to MCP (Model Context Protocol) servers to access tools, resources, and prompts.

## Overview

```
┌─────────────────┐          ┌─────────────────┐
│  OpenAI Agent   │  ──────▶ │   MCP Server    │
│  (Gemini/LLM)   │  tools   │  (FastMCP)      │
└─────────────────┘          └─────────────────┘
                                    │
                                    ▼
                             ┌─────────────────┐
                             │   Database      │
                             └─────────────────┘
```

## Connection Types

| Type | Class | Use Case |
|------|-------|----------|
| Streamable HTTP | `MCPServerStreamableHttp` | Production, REST APIs |
| SSE | `MCPServerSse` | Real-time, web clients |
| Stdio | `MCPServerStdio` | Local subprocess |
| Hosted | `HostedMCPTool` | OpenAI-hosted MCP |

## Streamable HTTP Connection (Recommended)

```python
import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.extensions.models.litellm_model import LitellmModel

async def main():
    async with MCPServerStreamableHttp(
        name="Todo Server",
        params={
            "url": "http://localhost:8000/api/mcp",
            "timeout": 30,
            # Optional authentication
            # "headers": {"Authorization": f"Bearer {token}"},
        },
        cache_tools_list=True,  # Cache for performance
        max_retry_attempts=3,    # Retry on failure
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="Use MCP tools to manage tasks.",
            model=LitellmModel(
                model="gemini/gemini-2.0-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
            ),
            mcp_servers=[server],
        )

        result = await Runner.run(agent, "List my tasks")
        print(result.final_output)

asyncio.run(main())
```

## SSE Connection

```python
from agents.mcp import MCPServerSse

async with MCPServerSse(
    name="SSE Server",
    params={
        "url": "http://localhost:8000/sse",
        "headers": {"X-User-ID": "user123"},
    },
    cache_tools_list=True,
) as server:
    agent = Agent(
        name="Assistant",
        mcp_servers=[server],
        # ...
    )
```

## Stdio Connection (Local Process)

```python
from pathlib import Path
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
    name="Local Server",
    params={
        "command": "python",
        "args": ["mcp_server.py"],
        "cwd": str(Path.cwd()),
    },
) as server:
    agent = Agent(
        name="Assistant",
        mcp_servers=[server],
        # ...
    )
```

## Multiple MCP Servers

```python
async with MCPServerStreamableHttp(
    name="Tasks",
    params={"url": "http://localhost:8000/tasks/mcp"},
) as tasks_server, MCPServerStreamableHttp(
    name="Calendar",
    params={"url": "http://localhost:8000/calendar/mcp"},
) as calendar_server:
    agent = Agent(
        name="Assistant",
        instructions="Manage tasks and calendar events.",
        mcp_servers=[tasks_server, calendar_server],
        # ...
    )
```

## Tool Filtering

### Static Filter

```python
from agents.mcp import MCPServerStreamableHttp, create_static_tool_filter

async with MCPServerStreamableHttp(
    name="Server",
    params={"url": "http://localhost:8000/mcp"},
    # Only allow specific tools
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["add_task", "list_tasks"],
    ),
) as server:
    # Agent can only use add_task and list_tasks
    ...
```

### Dynamic Filter

```python
from agents.mcp import MCPServerStreamableHttp, ToolFilterContext

async def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    """Filter tools based on context."""
    # Block dangerous tools for certain agents
    if context.agent.name == "Read-Only" and tool.name.startswith("delete_"):
        return False
    return True

async with MCPServerStreamableHttp(
    name="Server",
    params={"url": "http://localhost:8000/mcp"},
    tool_filter=context_aware_filter,
) as server:
    ...
```

## Tool Choice Settings

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="Assistant",
    mcp_servers=[server],
    model_settings=ModelSettings(
        tool_choice="required",  # Force tool usage
        # tool_choice="auto",    # Let model decide
        # tool_choice="none",    # No tools
    ),
)
```

## Passing User Context to MCP Tools

MCP tools often need user identification. Pass it in the conversation:

```python
# Option 1: In system instructions
agent = Agent(
    name="Assistant",
    instructions=f"""You are helping user {user_id}.
Always pass user_id="{user_id}" to MCP tools.""",
    mcp_servers=[server],
)

# Option 2: In the input message
result = await Runner.run(
    agent,
    f"[User ID: {user_id}] Show my tasks",
)
```

## Handling MCP Errors

```python
import asyncio
from agents import Runner

async def run_with_mcp():
    try:
        async with MCPServerStreamableHttp(
            name="Server",
            params={"url": "http://localhost:8000/mcp"},
            max_retry_attempts=3,
        ) as server:
            agent = Agent(name="Assistant", mcp_servers=[server], ...)
            result = await Runner.run(agent, "Hello")
            return result.final_output

    except ConnectionError:
        return "Could not connect to MCP server"
    except TimeoutError:
        return "MCP server timed out"
    except Exception as e:
        return f"Error: {e}"
```

## Best Practices

1. **Use `cache_tools_list=True`** for production performance
2. **Set appropriate timeouts** based on tool complexity
3. **Use tool filtering** to limit exposure
4. **Handle connection errors** gracefully
5. **Pass user context** consistently to tools
6. **Use streamable HTTP** for most production use cases
