# Python API Reference

## Installation

```bash
pip install agent-framework --pre
```

Sub-packages:
- `agent-framework-core` - Core abstractions
- `agent-framework-openai` - OpenAI/compatible models
- `agent-framework-azure` - Azure AI services
- `agent-framework-workflows` - Workflow orchestration

---

## ChatAgent

Primary agent class. DO NOT subclass or create alternatives.

```python
from agent_framework import ChatAgent

class ChatAgent:
    def __init__(
        self,
        chat_client,                    # Required: IChatClient implementation
        instructions: str = None,       # System prompt
        name: str = None,               # Agent identifier
        tools: list = None,             # List of callable tools
        middleware: list = None,        # Request/response interceptors
        context_providers: list = None  # Dynamic context injection
    )
    
    async def run(
        self,
        input: str | ChatMessage,       # User input
        tools: list = None,             # Override tools for this call
        tool_choice: str | dict = None, # "auto", "required", "none", or specific
        thread: AgentThread = None      # Conversation state
    ) -> AgentResult
    
    async def run_streaming(
        self,
        input: str | ChatMessage,
        **kwargs
    ) -> AsyncIterator[StreamingUpdate]
    
    def as_tool(
        self,
        name: str,
        description: str,
        arg_name: str = "request",
        arg_description: str = None
    ) -> AITool  # Convert agent to callable tool
```

### Context Manager Pattern (Required for cleanup)

```python
async with ChatAgent(...) as agent:
    result = await agent.run("query")
```

---

## AgentResult

```python
class AgentResult:
    text: str                    # Full text response
    messages: list[ChatMessage]  # All messages in conversation
    tool_calls: list[ToolCall]   # Tools that were invoked
    usage: UsageStats            # Token usage
```

---

## AgentThread

State management for multi-turn conversations.

```python
from agent_framework import AgentThread

thread = AgentThread()

# Thread maintains conversation history across calls
result1 = await agent.run("Hello", thread=thread)
result2 = await agent.run("What did I just say?", thread=thread)
```

---

## ChatMessage

```python
from agent_framework import ChatMessage, TextContent, UriContent, Role

message = ChatMessage(
    role=Role.USER,  # USER, ASSISTANT, SYSTEM, TOOL
    contents=[
        TextContent(text="Analyze this image"),
        UriContent(
            uri="https://example.com/image.jpg",
            media_type="image/jpeg"
        )
    ]
)

result = await agent.run(message)
```

---

## Model Clients

### OpenAIChatClient (for OpenAI or compatible APIs)

```python
from agent_framework.openai import OpenAIChatClient

# Standard OpenAI
client = OpenAIChatClient(
    api_key="sk-...",
    model_id="gpt-4o"
)

# Local/self-hosted model (OpenAI-compatible)
client = OpenAIChatClient(
    base_url="http://localhost:8000/v1",
    api_key="not-required",
    model_id="local-model"
)

agent = ChatAgent(chat_client=client, instructions="...")
# Or use factory:
agent = client.create_agent(instructions="...", tools=[...])
```

### AzureAIAgentClient

```python
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async with AzureCliCredential() as credential:
    client = AzureAIAgentClient(
        async_credential=credential,
        # Or set via environment:
        # AZURE_AI_PROJECT_ENDPOINT
        # AZURE_AI_MODEL_DEPLOYMENT_NAME
    )
```

### AzureOpenAIResponsesClient

```python
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

client = AzureOpenAIResponsesClient(
    endpoint="https://your-resource.openai.azure.com",
    deployment_name="gpt-4o",
    credential=AzureCliCredential()
)
```

---

## Function Tools

Define tools as functions with type annotations:

```python
from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="City name")],
    units: Annotated[str, Field(description="celsius or fahrenheit")] = "celsius"
) -> str:
    """Get current weather for a location."""  # Docstring = tool description
    # Implementation
    return f"Weather in {location}: 22°{units[0].upper()}"

# Async tools supported
async def fetch_data(
    url: Annotated[str, Field(description="URL to fetch")]
) -> str:
    """Fetch data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

agent = ChatAgent(
    chat_client=client,
    tools=[get_weather, fetch_data]
)
```

---

## MCP Tools

### MCPStdioTool (Local process)

```python
from agent_framework import MCPStdioTool

async with MCPStdioTool(
    name="filesystem",
    command="uvx",
    args=["mcp-server-filesystem", "/allowed/path"]
) as mcp:
    # Use with agent
    result = await agent.run("List files", tools=mcp)
    
    # Or get functions for combining
    all_tools = [*mcp.functions, other_tool]
```

### MCPStreamableHTTPTool (Remote HTTP/SSE)

```python
from agent_framework import MCPStreamableHTTPTool

async with MCPStreamableHTTPTool(
    name="remote-service",
    url="https://api.example.com/mcp/sse"
) as mcp:
    result = await agent.run("Query", tools=mcp)
```

### MCPWebsocketTool

```python
from agent_framework import MCPWebsocketTool

async with MCPWebsocketTool(
    name="realtime",
    url="wss://api.example.com/mcp/ws"
) as mcp:
    result = await agent.run("Stream data", tools=mcp)
```

### Combining Multiple MCP Servers

```python
async with (
    MCPStdioTool(name="search", command="uvx", args=["mcp-search"]) as search,
    MCPStdioTool(name="fetch", command="uvx", args=["mcp-fetch"]) as fetch,
):
    combined_tools = [*search.functions, *fetch.functions]
    
    agent = ChatAgent(
        chat_client=client,
        tools=combined_tools
    )
```

---

## Middleware

Intercept agent requests/responses:

```python
from agent_framework import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def invoke(self, context: MiddlewareContext, next):
        print(f"Input: {context.input}")
        result = await next(context)
        print(f"Output: {result.text}")
        return result

class RateLimitMiddleware(Middleware):
    async def invoke(self, context: MiddlewareContext, next):
        await self.check_rate_limit()
        return await next(context)

agent = ChatAgent(
    chat_client=client,
    middleware=[LoggingMiddleware(), RateLimitMiddleware()]
)
```

---

## Context Providers

Inject dynamic context into agent:

```python
from agent_framework import ContextProvider

class UserContextProvider(ContextProvider):
    async def get_context(self, input, **kwargs) -> str:
        user_id = kwargs.get("user_id")
        user = await self.db.get_user(user_id)
        return f"User: {user.name}, Role: {user.role}"

agent = ChatAgent(
    chat_client=client,
    instructions="You are a personal assistant.",
    context_providers=[UserContextProvider()]
)

# Context injected automatically
result = await agent.run("What's my schedule?", user_id="123")
```

---

## Error Handling

```python
from agent_framework import AgentError, ToolExecutionError

try:
    result = await agent.run("Do something")
except ToolExecutionError as e:
    print(f"Tool {e.tool_name} failed: {e.message}")
except AgentError as e:
    print(f"Agent error: {e}")
```
