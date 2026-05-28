---
name: claude-sdk
description: Use the Anthropic Claude SDK for programmatic API access. Enables spawning sub-agents, parallel processing, batch operations, and custom Claude interactions via Python. Use when tasks need multiple Claude instances, background processing, or direct API control.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Claude SDK Skill

**Enables programmatic access to Claude's API for sub-agents, parallel processing, and advanced workflows.**

## Prerequisites

The Anthropic Python SDK is pre-installed. Ensure `ANTHROPIC_API_KEY` is set:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Basic Usage

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)

print(response.content[0].text)
```

## Use Cases

### 1. Spawn a Sub-Agent

Delegate a focused task to a separate Claude instance:

```python
from anthropic import Anthropic

def spawn_sub_agent(task: str, context: str = "") -> str:
    """Spawn a sub-agent for a focused task."""
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="You are a focused sub-agent. Complete the task directly and concisely.",
        messages=[
            {"role": "user", "content": f"Context:\n{context}\n\nTask:\n{task}"}
        ]
    )
    return response.content[0].text

# Example: Delegate code review
result = spawn_sub_agent(
    task="Review this function for bugs and suggest improvements",
    context=open("myfile.py").read()
)
print(result)
```

### 2. Parallel Processing

Process multiple items concurrently:

```python
from anthropic import Anthropic
from concurrent.futures import ThreadPoolExecutor

def process_item(item: str) -> str:
    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Analyze: {item}"}]
    )
    return response.content[0].text

items = ["item1", "item2", "item3"]
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_item, items))
```

### 3. Streaming Responses

Stream long responses for real-time output:

```python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a long story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 4. Multi-Turn Conversations

Maintain conversation context:

```python
from anthropic import Anthropic

client = Anthropic()
messages = []

def chat(user_message: str) -> str:
    messages.append({"role": "user", "content": user_message})
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages
    )
    
    assistant_message = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_message})
    return assistant_message

# Multi-turn conversation
chat("What is Python?")
chat("Show me an example")
chat("How do I run it?")
```

### 5. Tool Use (Function Calling)

Let Claude call your functions:

```python
from anthropic import Anthropic

client = Anthropic()

tools = [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Check if Claude wants to use a tool
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
```

## Models

| Model | Best For |
|-------|----------|
| `claude-sonnet-4-20250514` | Balanced performance/cost |
| `claude-opus-4-20250514` | Complex reasoning |
| `claude-3-5-haiku-20241022` | Fast, cheap tasks |

## Rate Limits

Be mindful of API rate limits when spawning multiple sub-agents. Use exponential backoff:

```python
import time
from anthropic import RateLimitError

def call_with_retry(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** i
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

## Cost Awareness

API calls cost money. Estimate before large operations:
- **Sonnet**: ~$3/M input, ~$15/M output tokens
- **Opus**: ~$15/M input, ~$75/M output tokens
- **Haiku**: ~$0.25/M input, ~$1.25/M output tokens
