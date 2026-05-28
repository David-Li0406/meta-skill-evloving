# Messages API Reference

The Messages API is the primary interface for interacting with Claude models. This reference covers request/response structure, content types, and common patterns.

## Table of Contents

- [Basic Request](#basic-request)
- [Request Parameters](#request-parameters)
- [Response Structure](#response-structure)
- [Content Types](#content-types)
- [System Prompts](#system-prompts)
- [Multi-turn Conversations](#multi-turn-conversations)
- [Streaming](#streaming)
- [Stop Reasons](#stop-reasons)
- [Usage Tracking](#usage-tracking)

---

## Basic Request

### Python

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Hello, Claude!" }
  ]
});

console.log(message.content[0].text);
```

### cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude!"}
    ]
  }'
```

---

## Request Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., `claude-sonnet-4-5-20250929`) |
| `max_tokens` | integer | Maximum tokens in response (1-64000 depending on model) |
| `messages` | array | Array of message objects with `role` and `content` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `system` | string or array | - | System prompt(s) |
| `temperature` | float | 1.0 | Randomness (0.0-1.0) |
| `top_p` | float | - | Nucleus sampling threshold |
| `top_k` | int | - | Top-k sampling |
| `stop_sequences` | array | - | Custom stop sequences |
| `stream` | boolean | false | Enable streaming |
| `tools` | array | - | Tool definitions |
| `tool_choice` | object | - | Tool selection mode |
| `metadata` | object | - | Request metadata |

### Temperature Guidelines

| Temperature | Use Case |
|-------------|----------|
| 0.0 | Deterministic, factual responses |
| 0.3-0.5 | Balanced creativity/consistency |
| 0.7-1.0 | Creative writing, brainstorming |

---

## Response Structure

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I help you today?"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 15
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique message ID (`msg_...`) |
| `type` | string | Always `"message"` |
| `role` | string | Always `"assistant"` |
| `content` | array | Array of content blocks |
| `model` | string | Model that generated response |
| `stop_reason` | string | Why generation stopped |
| `stop_sequence` | string | Matched stop sequence (if any) |
| `usage` | object | Token usage statistics |

### Accessing Response Content

```python
# Single text response
text = message.content[0].text

# Multiple content blocks
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
```

---

## Content Types

Messages can contain various content types in the `content` array.

### Text Content

```python
# Simple string (shorthand)
{"role": "user", "content": "Hello"}

# Explicit text block
{"role": "user", "content": [
    {"type": "text", "text": "Hello"}
]}
```

### Image Content

```python
# Base64 encoded
{"role": "user", "content": [
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": "<base64_data>"
        }
    },
    {"type": "text", "text": "Describe this image"}
]}

# URL (publicly accessible)
{"role": "user", "content": [
    {
        "type": "image",
        "source": {
            "type": "url",
            "url": "https://example.com/image.png"
        }
    },
    {"type": "text", "text": "What's in this image?"}
]}
```

### Document Content (PDFs)

```python
{"role": "user", "content": [
    {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": "<base64_pdf_data>"
        }
    },
    {"type": "text", "text": "Summarize this document"}
]}
```

### Tool Use Content

```python
# Assistant's tool use
{"role": "assistant", "content": [
    {
        "type": "tool_use",
        "id": "toolu_01A09q90qw90lq917835lgs",
        "name": "get_weather",
        "input": {"location": "San Francisco"}
    }
]}

# User's tool result
{"role": "user", "content": [
    {
        "type": "tool_result",
        "tool_use_id": "toolu_01A09q90qw90lq917835lgs",
        "content": "72°F, sunny"
    }
]}
```

---

## System Prompts

System prompts set context and instructions for the conversation.

### Simple String

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant that speaks like a pirate.",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Multiple System Blocks

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "You are a helpful assistant."},
        {"type": "text", "text": "Here is context: <context>...</context>"}
    ],
    messages=[{"role": "user", "content": "Summarize the context"}]
)
```

### System with Cache Control

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "Instructions..."},
        {
            "type": "text",
            "text": "<large_document>...</large_document>",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question about document"}]
)
```

---

## Multi-turn Conversations

Build conversations by including the full message history.

### Python

```python
messages = [
    {"role": "user", "content": "My name is Alice."},
    {"role": "assistant", "content": "Hello Alice! Nice to meet you."},
    {"role": "user", "content": "What's my name?"}
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)

# Continue conversation
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": "Tell me a joke about my name."})

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

### TypeScript

```typescript
const messages: Anthropic.MessageParam[] = [
  { role: "user", content: "My name is Alice." },
  { role: "assistant", content: "Hello Alice! Nice to meet you." },
  { role: "user", content: "What's my name?" }
];

const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages
});
```

### Message Ordering Rules

1. Messages must alternate between `user` and `assistant`
2. First message must be from `user`
3. Last message must be from `user`

---

## Streaming

Stream responses for real-time output.

### Python

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Python Async

```python
async with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
```

### TypeScript

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a story" }]
});

for await (const text of stream.textStream) {
  process.stdout.write(text);
}

// Get final message
const finalMessage = await stream.finalMessage();
```

### Stream Events

```python
with client.messages.stream(...) as stream:
    for event in stream:
        if event.type == "message_start":
            print(f"Started: {event.message.id}")
        elif event.type == "content_block_start":
            print(f"Block type: {event.content_block.type}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="")
        elif event.type == "message_delta":
            print(f"\nStop: {event.delta.stop_reason}")
        elif event.type == "message_stop":
            print("Done")
```

### Event Types

| Event | Description |
|-------|-------------|
| `message_start` | Message creation started |
| `content_block_start` | New content block started |
| `content_block_delta` | Content block update |
| `content_block_stop` | Content block finished |
| `message_delta` | Message-level updates (stop_reason, usage) |
| `message_stop` | Message complete |

---

## Stop Reasons

The `stop_reason` field indicates why generation stopped.

| Value | Description |
|-------|-------------|
| `end_turn` | Natural completion |
| `max_tokens` | Hit `max_tokens` limit |
| `stop_sequence` | Hit a stop sequence |
| `tool_use` | Model wants to use a tool |

### Handling Stop Reasons

```python
response = client.messages.create(...)

if response.stop_reason == "end_turn":
    print("Complete response")
elif response.stop_reason == "max_tokens":
    print("Response truncated - increase max_tokens")
elif response.stop_reason == "tool_use":
    # Handle tool use
    tool_use = next(b for b in response.content if b.type == "tool_use")
    print(f"Tool requested: {tool_use.name}")
elif response.stop_reason == "stop_sequence":
    print(f"Stopped at: {response.stop_sequence}")
```

---

## Usage Tracking

Track token usage for cost estimation.

### Basic Usage

```python
response = client.messages.create(...)

print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
```

### With Caching

```python
# Cache-related fields
print(f"Cache creation: {response.usage.cache_creation_input_tokens}")
print(f"Cache read: {response.usage.cache_read_input_tokens}")

# Total input calculation
total_input = (
    response.usage.cache_read_input_tokens +
    response.usage.cache_creation_input_tokens +
    response.usage.input_tokens
)
```

### Cost Estimation

```python
# Example pricing (check current rates)
INPUT_COST_PER_MTOK = 3.00  # Claude Sonnet 4.5
OUTPUT_COST_PER_MTOK = 15.00
CACHE_WRITE_COST_PER_MTOK = 3.75
CACHE_READ_COST_PER_MTOK = 0.30

def estimate_cost(usage):
    input_cost = (usage.input_tokens / 1_000_000) * INPUT_COST_PER_MTOK
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_COST_PER_MTOK

    cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
    cache_read = getattr(usage, 'cache_read_input_tokens', 0)

    cache_write_cost = (cache_write / 1_000_000) * CACHE_WRITE_COST_PER_MTOK
    cache_read_cost = (cache_read / 1_000_000) * CACHE_READ_COST_PER_MTOK

    return input_cost + output_cost + cache_write_cost + cache_read_cost
```

---

## Beta Features

Enable beta features using headers.

### Python

```python
# 1M context window (Claude Sonnet 4.5)
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    extra_headers={"anthropic-beta": "context-1m-2025-08-07"},
    messages=[{"role": "user", "content": very_long_content}]
)

# 128K output (Claude Sonnet 3.7)
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=128000,
    extra_headers={"anthropic-beta": "output-128k-2025-02-19"},
    messages=[{"role": "user", "content": "..."}]
)
```

### TypeScript

```typescript
const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [...],
}, {
  headers: { "anthropic-beta": "context-1m-2025-08-07" }
});
```

---

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
    response = client.messages.create(...)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    retry_after = e.response.headers.get("retry-after", 60)
    print(f"Rate limited. Retry after {retry_after}s")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
except APIConnectionError:
    print("Network error - check connection")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid request | Check parameters |
| 401 | Invalid API key | Verify `ANTHROPIC_API_KEY` |
| 429 | Rate limit | Implement backoff/retry |
| 500 | Server error | Retry with backoff |
| 529 | Overloaded | Retry after delay |
