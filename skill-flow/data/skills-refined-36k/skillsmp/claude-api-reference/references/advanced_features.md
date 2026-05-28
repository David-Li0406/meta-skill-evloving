# Advanced Features Guide

## Streaming Responses

### Basic Streaming

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Async Streaming

```python
import asyncio
from anthropic import AsyncAnthropic

async def main():
    client = AsyncAnthropic()
    
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(main())
```

### Handling Complete Events

```python
with client.messages.stream(...) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print("Starting generation...")
        elif event.type == "content_block_delta":
            print(event.delta.text, end="")
        elif event.type == "message_stop":
            print("\nComplete")
```

### Getting Final Message

```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="")
    
    # Get complete Message object
    final_message = stream.get_final_message()
    print(f"\nTokens: {final_message.usage}")
```

---

## Extended Thinking

Allow Claude to perform deeper reasoning before answering:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Thinking token budget
    },
    messages=[{"role": "user", "content": "Solve this complex math problem..."}]
)

# Response includes thinking and text blocks
for block in message.content:
    if block.type == "thinking":
        print(f"Thinking process: {block.thinking}")
    elif block.type == "text":
        print(f"Final answer: {block.text}")
```

### Limits

- `budget_tokens` minimum: 1024
- `budget_tokens` must be less than `max_tokens`
- Thinking tokens count toward `max_tokens` limit

---

## Batch Processing

50% cost discount, suitable for large non-real-time requests:

### Create Batch

```python
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Question 1"}]
            }
        },
        {
            "custom_id": "request-2",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Question 2"}]
            }
        }
    ]
)

print(f"Batch ID: {batch.id}")
```

### Check Status

```python
batch = client.messages.batches.retrieve(batch.id)
print(f"Status: {batch.processing_status}")
```

### Get Results

```python
if batch.processing_status == "ended":
    results = client.messages.batches.results(batch.id)
    for entry in results:
        if entry.result.type == "succeeded":
            print(f"{entry.custom_id}: {entry.result.message.content}")
```

---

## Prompt Caching

Reduce costs for repeated tokens:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "This is a very long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)

# Check cache usage
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

### Cache Lifetime

- `ephemeral`: 5 minutes
- Timer refreshes on each use

---

## Token Counting

Estimate costs before sending:

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Content to count"}]
)

print(f"Input tokens: {count.input_tokens}")
```

---

## System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a professional technical consultant specializing in Azure and data architecture.",
    messages=[{"role": "user", "content": "Question"}]
)
```

### Multi-block System Prompt

```python
system = [
    {"type": "text", "text": "You are an assistant."},
    {"type": "text", "text": "Please follow these rules:...", "cache_control": {"type": "ephemeral"}}
]
```

---

## Stop Sequences

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    stop_sequences=["END", "STOP", "---"],
    messages=[{"role": "user", "content": "..."}]
)

# Check stop reason
print(f"Stop reason: {message.stop_reason}")  # "stop_sequence" or "end_turn"
print(f"Stop sequence: {message.stop_sequence}")  # Triggered sequence
```

---

## Temperature Control

```python
# Lower temperature - more deterministic, consistent
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=0.0,  # 0.0 - 1.0
    messages=[...]
)

# Higher temperature - more creative, diverse
message = client.messages.create(
    ...,
    temperature=0.8,
    ...
)
```

---

## Error Handling

```python
import anthropic

try:
    message = client.messages.create(...)
except anthropic.APIConnectionError as e:
    print(f"Connection error: {e}")
except anthropic.RateLimitError as e:
    print(f"Rate limit: {e}")
except anthropic.APIStatusError as e:
    print(f"API error: {e.status_code}")
    print(f"Response: {e.response}")
```

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad request format |
| 401 | Authentication failed |
| 403 | Permission denied |
| 404 | Resource not found |
| 413 | Request too large |
| 429 | Rate limited |
| 500 | Server error |

---

## Retry Logic

SDK has built-in auto-retry:

```python
client = anthropic.Anthropic(
    max_retries=3,  # Default 2
    timeout=60.0    # Default 10 minutes
)
```

### Manual Retry

```python
import time
from anthropic import RateLimitError

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)
```