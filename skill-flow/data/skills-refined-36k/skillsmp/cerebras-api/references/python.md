# Cerebras Python SDK Reference

## Installation

```bash
pip install cerebras_cloud_sdk
```

For aiohttp async backend:
```bash
pip install 'cerebras_cloud_sdk[aiohttp]'
```

## Client Initialization

```python
from cerebras.cloud.sdk import Cerebras

# From environment variable (recommended)
client = Cerebras()  # Uses CEREBRAS_API_KEY

# Explicit API key
client = Cerebras(api_key="your-api-key")

# Full configuration
client = Cerebras(
    api_key="your-api-key",
    max_retries=3,           # Default: 2
    timeout=30.0,            # Default: 60s
    warm_tcp_connection=True # Default: True (reduces TTFT)
)
```

## Chat Completions

### Basic Request

```python
response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello"}
    ],
    temperature=0.7,
    max_completion_tokens=1000
)

print(response.choices[0].message.content)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

# Note: usage and time_info only in final chunk
```

### Multi-turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Alice."},
]

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=messages
)

# Add assistant response to history
messages.append({
    "role": "assistant",
    "content": response.choices[0].message.content
})

# Continue conversation
messages.append({"role": "user", "content": "What's my name?"})
response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=messages
)
```

## Text Completions

```python
completion = client.completions.create(
    model="llama3.1-8b",
    prompt="Once upon a time",
    max_tokens=100,
    temperature=0.8
)

print(completion.choices[0].text)
```

### Streaming Text Completions

```python
stream = client.completions.create(
    model="llama3.1-8b",
    prompt="The future of AI is",
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].text or "", end="")
```

## Async Client

```python
import asyncio
from cerebras.cloud.sdk import AsyncCerebras

client = AsyncCerebras()

async def main():
    response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### Async Streaming

```python
async def stream_response():
    stream = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Tell me a joke"}],
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

asyncio.run(stream_response())
```

### Aiohttp Backend (Better Concurrency)

```python
from cerebras.cloud.sdk import AsyncCerebras, DefaultAioHttpClient

async with AsyncCerebras(http_client=DefaultAioHttpClient()) as client:
    response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
```

## Tool Calling

### Single Tool

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "strict": True,
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"],
            "additionalProperties": False
        }
    }
}]

response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Call: {tool_call.function.name}")
    print(f"Args: {tool_call.function.arguments}")
```

### Multi-turn Tool Calling

```python
import json

messages = [{"role": "user", "content": "Weather in Tokyo?"}]

response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=messages,
    tools=tools
)

# Process tool calls
while response.choices[0].message.tool_calls:
    # Add assistant message with tool calls
    messages.append(response.choices[0].message)

    for tool_call in response.choices[0].message.tool_calls:
        # Execute tool (your implementation)
        result = execute_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )

        # Add tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Continue conversation
    response = client.chat.completions.create(
        model="zai-glm-4.7",
        messages=messages,
        tools=tools
    )

print(response.choices[0].message.content)
```

### Parallel Tool Calling

```python
# Enabled by default
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Weather in Tokyo and Paris?"}],
    tools=tools,
    parallel_tool_calls=True  # Default
)

# May return multiple tool_calls
for tool_call in response.choices[0].message.tool_calls:
    print(f"Tool: {tool_call.function.name}")
```

## Structured Outputs

### With JSON Schema

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "skills": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["name", "age", "skills"],
    "additionalProperties": False
}

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Create a developer profile"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "profile",
            "strict": True,
            "schema": schema
        }
    }
)

import json
data = json.loads(response.choices[0].message.content)
```

### With Pydantic

```python
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    email: str
    age: int
    address: Optional[Address] = None
    tags: List[str]

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Generate a person record"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "strict": True,
            "schema": Person.model_json_schema()
        }
    }
)

person = Person.model_validate_json(response.choices[0].message.content)
```

### JSON Mode (Less Strict)

```python
response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "Respond in JSON format"},
        {"role": "user", "content": "List 3 colors"}
    ],
    response_format={"type": "json_object"}
)
```

## Reasoning Models

### Parsed Format (Separate Field)

```python
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=[{"role": "user", "content": "What is 15% of 240?"}],
    reasoning_format="parsed"
)

print("Reasoning:", response.choices[0].message.reasoning)
print("Answer:", response.choices[0].message.content)
```

### Raw Format (In Content)

```python
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=[{"role": "user", "content": "Solve: 2x + 5 = 15"}],
    reasoning_format="raw"
)

# Content includes <think>...</think> tags for Qwen/GLM
print(response.choices[0].message.content)
```

### Hidden Format

```python
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=[{"role": "user", "content": "Complex problem"}],
    reasoning_format="hidden"  # Reasoning not returned but still computed
)
```

### GPT-OSS Reasoning Effort

```python
response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[{"role": "user", "content": "Prove the Pythagorean theorem"}],
    reasoning_effort="high"  # "low", "medium", "high"
)
```

### GLM Disable Reasoning

```python
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Quick answer needed"}],
    disable_reasoning=True
)
```

### Multi-turn with Reasoning Context

```python
# Preserve reasoning across turns by including in content
messages = [{"role": "user", "content": "Solve: x^2 - 5x + 6 = 0"}]

response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=messages,
    reasoning_format="raw"
)

# Include reasoning in assistant message for context
messages.append({
    "role": "assistant",
    "content": response.choices[0].message.content  # Includes <think> tags
})

messages.append({"role": "user", "content": "Now solve x^2 - 7x + 12 = 0"})

response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=messages,
    reasoning_format="raw"
)
```

## Error Handling

```python
import cerebras.cloud.sdk

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
except cerebras.cloud.sdk.APIConnectionError as e:
    print(f"Connection error: {e.__cause__}")
except cerebras.cloud.sdk.RateLimitError as e:
    print(f"Rate limited. Retry after: {e.response.headers.get('Retry-After')}")
except cerebras.cloud.sdk.AuthenticationError:
    print("Invalid API key")
except cerebras.cloud.sdk.BadRequestError as e:
    print(f"Bad request: {e.message}")
except cerebras.cloud.sdk.APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Response Objects

### ChatCompletion

```python
response = client.chat.completions.create(...)

# Access fields
response.id              # Completion ID
response.model           # Model used
response.created         # Unix timestamp
response.choices         # List of choices
response.usage           # Token usage

# Choice fields
choice = response.choices[0]
choice.index             # Choice index
choice.finish_reason     # "stop", "length", "tool_calls"
choice.message.role      # "assistant"
choice.message.content   # Response text
choice.message.tool_calls  # Tool calls (if any)
choice.message.reasoning   # Reasoning (if parsed format)

# Usage fields
response.usage.prompt_tokens
response.usage.completion_tokens
response.usage.total_tokens

# Serialize
json_str = response.to_json()
dict_repr = response.to_dict()
```

### Raw Response Access

```python
response = client.chat.completions.create(...)

# Access HTTP response
print(response.http_response.headers)
print(response.http_response.status_code)
```

## Configuration Options

### Per-Request Overrides

```python
# Override timeout
response = client.with_options(timeout=10.0).chat.completions.create(...)

# Override retries
response = client.with_options(max_retries=5).chat.completions.create(...)
```

### Granular Timeouts

```python
import httpx

client = Cerebras(
    timeout=httpx.Timeout(
        60.0,        # Total timeout
        connect=5.0, # Connection timeout
        read=30.0,   # Read timeout
        write=10.0   # Write timeout
    )
)
```

### Logging

```bash
export CEREBRAS_LOG=info   # or 'debug' for verbose
```

## Model Listing

```python
models = client.models.list()
for model in models:
    print(f"{model.id}: {model.owned_by}")

# Get specific model
model = client.models.retrieve("llama-3.3-70b")
```
