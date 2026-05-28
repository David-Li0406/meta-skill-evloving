# Python SDK Reference

## Installation

```bash
pip install anthropic
```

## Client Initialization

```python
from anthropic import Anthropic

# Uses ANTHROPIC_API_KEY env var by default
client = Anthropic()

# Or explicit key
client = Anthropic(api_key="sk-ant-...")
```

## Messages API

### Basic Message

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content[0].text)
```

### Multi-turn Conversation

```python
messages = [
    {"role": "user", "content": "My name is Alice."},
    {"role": "assistant", "content": "Hello Alice! Nice to meet you."},
    {"role": "user", "content": "What's my name?"}
]
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

### System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant that speaks like a pirate.",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Async Client

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def main():
    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
    return message

# Async streaming
async def stream_response():
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a story"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
```

## Vision / Images

### Base64 Image

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)
```

### URL Image

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/image.png"
                }
            },
            {"type": "text", "text": "What's in this image?"}
        ]
    }]
)
```

### Multiple Images

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img1_data}},
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img2_data}},
            {"type": "text", "text": "Compare these two images"}
        ]
    }]
)
```

## Tool Use

### Define Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]
```

### Tool Use Flow

```python
# Step 1: Send message with tools
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Boston?"}]
)

# Step 2: Check if Claude wants to use a tool
if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")
    tool_name = tool_use.name
    tool_input = tool_use.input

    # Step 3: Execute tool and get result
    tool_result = execute_tool(tool_name, tool_input)  # Your implementation

    # Step 4: Send tool result back
    final_response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Boston?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": tool_result
                }]
            }
        ]
    )
```

### Tool Choice

```python
# Force Claude to use a specific tool
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "get_weather"},
    messages=[{"role": "user", "content": "Boston"}]
)

# Let Claude decide (default)
tool_choice={"type": "auto"}

# Force Claude to use any tool
tool_choice={"type": "any"}

# Prevent tool use
tool_choice={"type": "none"}
```

### Streaming with Tools

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Weather in NYC?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if hasattr(event.content_block, "type"):
                if event.content_block.type == "tool_use":
                    print(f"Tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if hasattr(event.delta, "partial_json"):
                print(event.delta.partial_json, end="")
```

## Response Structure

```python
message = client.messages.create(...)

# Response fields
message.id           # "msg_..."
message.type         # "message"
message.role         # "assistant"
message.content      # List of content blocks
message.model        # Model used
message.stop_reason  # "end_turn", "max_tokens", "tool_use", "stop_sequence"
message.usage.input_tokens
message.usage.output_tokens

# Content blocks
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        print(block.name, block.input)
```

## Error Handling

```python
from anthropic import (
    APIError,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    BadRequestError,
)

try:
    message = client.messages.create(...)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.response.headers.get('retry-after')}")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
except APIConnectionError:
    print("Network error")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Available Models

| Model | Model ID |
|-------|----------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` |

## Parameters Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Required. Model ID |
| `max_tokens` | int | Required. Max output tokens |
| `messages` | list | Required. Conversation history |
| `system` | string | System prompt |
| `temperature` | float | 0.0-1.0, default 1.0 |
| `top_p` | float | Nucleus sampling |
| `top_k` | int | Top-k sampling |
| `stop_sequences` | list | Custom stop sequences |
| `tools` | list | Tool definitions |
| `tool_choice` | dict | Tool selection mode |
| `metadata` | dict | Request metadata |
