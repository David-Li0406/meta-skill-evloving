# Streaming Messages Reference

Stream responses incrementally using server-sent events (SSE) by setting `"stream": true`.

## Table of Contents

- [SDK Streaming](#sdk-streaming)
- [Event Types](#event-types)
- [Delta Types](#delta-types)
- [Raw HTTP Streaming](#raw-http-streaming)
- [Streaming Examples](#streaming-examples)
- [Error Recovery](#error-recovery)

---

## SDK Streaming

### Python Sync

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Python Async

```python
import anthropic

client = anthropic.AsyncAnthropic()

async with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }]
});

for await (const text of stream.textStream) {
  process.stdout.write(text);
}

// Get final message after stream completes
const finalMessage = await stream.finalMessage();
```

### TypeScript with Callbacks

```typescript
client.messages
  .stream({
    model: "claude-sonnet-4-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }]
  })
  .on("text", (text) => process.stdout.write(text))
  .on("message", (message) => console.log("\nDone:", message.usage))
  .on("error", (error) => console.error(error));
```

---

## Event Types

A stream response contains these events in order:

| Event | Description |
|-------|-------------|
| `message_start` | Initial message object with metadata |
| `content_block_start` | Start of a content block (text, tool_use, thinking) |
| `content_block_delta` | Incremental updates to content block |
| `content_block_stop` | End of current content block |
| `message_delta` | Top-level message updates (stop_reason, usage) |
| `message_stop` | Stream complete |
| `ping` | Keep-alive events (can appear anywhere) |
| `error` | Error during streaming |

### Event Flow

```
message_start
├── content_block_start (index 0)
│   ├── content_block_delta
│   ├── content_block_delta
│   └── content_block_stop
├── content_block_start (index 1)
│   ├── content_block_delta
│   └── content_block_stop
├── message_delta
└── message_stop
```

### Error Events

Errors may be sent during streaming (e.g., during high usage):

```json
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

### Important Notes

- The `usage` field in `message_delta` events contains *cumulative* token counts
- New event types may be added in the future - your code should handle unknown event types gracefully
- `ping` events can appear anywhere in the stream for keep-alive

---

## Delta Types

Each `content_block_delta` contains a `delta` object with type-specific content.

### Text Delta

```json
{
  "type": "content_block_delta",
  "index": 0,
  "delta": {"type": "text_delta", "text": "Hello world"}
}
```

### Input JSON Delta (Tool Use)

Tool input is streamed as partial JSON strings. Accumulate and parse when you receive `content_block_stop`.

```json
{
  "type": "content_block_delta",
  "index": 1,
  "delta": {"type": "input_json_delta", "partial_json": "{\"location\": \"San Fra"}
}
```

**Notes:**
- Models emit one complete key-value pair at a time - there may be delays between events while the model works
- Use partial JSON parsing libraries (like Pydantic) or SDK helpers to access incremental values
- Fine-grained tool streaming is available as a beta feature for more granular parameter value streaming

### Thinking Delta (Extended Thinking)

```json
{
  "type": "content_block_delta",
  "index": 0,
  "delta": {"type": "thinking_delta", "thinking": "Let me solve this step by step..."}
}
```

### Signature Delta

Sent before `content_block_stop` for thinking blocks to verify integrity:

```json
{
  "type": "content_block_delta",
  "index": 0,
  "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3h..."}
}
```

---

## Raw HTTP Streaming

For direct API integration without SDKs.

### Basic Request

```bash
curl https://api.anthropic.com/v1/messages \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 256,
    "stream": true,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Response Format

```
event: message_start
data: {"type": "message_start", "message": {"id": "msg_...", "type": "message", "role": "assistant", "content": [], "model": "claude-sonnet-4-5", "stop_reason": null, "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "!"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}
```

---

## Streaming Examples

### Basic Text Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Streaming with Tool Use

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City and state"}
            },
            "required": ["location"]
        }
    }
]

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"\nTool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="")
            elif event.delta.type == "input_json_delta":
                print(event.delta.partial_json, end="")
```

### Streaming with Extended Thinking

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 16000},
    messages=[{"role": "user", "content": "What is 27 * 453?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                print("--- Thinking ---")
            elif event.content_block.type == "text":
                print("\n--- Response ---")
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```

### TypeScript Streaming with Events

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }]
});

for await (const event of stream) {
  if (event.type === "content_block_start") {
    console.log(`Block ${event.index}: ${event.content_block.type}`);
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    } else if (event.delta.type === "input_json_delta") {
      process.stdout.write(event.delta.partial_json);
    }
  } else if (event.type === "message_delta") {
    console.log(`\nStop reason: ${event.delta.stop_reason}`);
  }
}
```

### Streaming with Web Search

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ],
    messages=[{"role": "user", "content": "What's the weather in NYC today?"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## Error Recovery

When a streaming request is interrupted, you can resume from where it stopped.

### Recovery Strategy

1. **Capture partial response**: Save all content received before the error
2. **Construct continuation request**: Include partial response as assistant message prefix
3. **Resume streaming**: Continue receiving the rest of the response

### Python Example

```python
import anthropic

client = anthropic.Anthropic()

def stream_with_recovery(messages, max_retries=3):
    partial_content = ""

    for attempt in range(max_retries):
        try:
            # If we have partial content, include it as assistant prefix
            request_messages = messages.copy()
            if partial_content:
                request_messages.append({
                    "role": "assistant",
                    "content": partial_content
                })

            with client.messages.stream(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                messages=request_messages
            ) as stream:
                for text in stream.text_stream:
                    partial_content += text
                    print(text, end="", flush=True)

            # Success - return complete content
            return partial_content

        except anthropic.APIConnectionError:
            print(f"\nConnection error, retrying ({attempt + 1}/{max_retries})...")
            continue

    raise Exception("Max retries exceeded")

# Usage
result = stream_with_recovery([
    {"role": "user", "content": "Write a long story"}
])
```

### Best Practices

1. **Use SDK features**: Leverage built-in message accumulation and error handling
2. **Handle all content types**: Messages can contain `text`, `tool_use`, and `thinking` blocks
3. **Resume from text blocks**: Tool use and thinking blocks cannot be partially recovered - resume from the most recent text block
4. **Implement exponential backoff**: For retries, increase wait time between attempts
5. **Save checkpoints**: For very long responses, periodically save progress

### TypeScript Example

```typescript
async function streamWithRecovery(
  messages: Anthropic.MessageParam[],
  maxRetries = 3
): Promise<string> {
  let partialContent = "";

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const requestMessages = [...messages];
      if (partialContent) {
        requestMessages.push({
          role: "assistant",
          content: partialContent
        });
      }

      const stream = client.messages.stream({
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        messages: requestMessages
      });

      for await (const text of stream.textStream) {
        partialContent += text;
        process.stdout.write(text);
      }

      return partialContent;

    } catch (error) {
      if (error instanceof Anthropic.APIConnectionError) {
        console.log(`\nConnection error, retrying (${attempt + 1}/${maxRetries})...`);
        continue;
      }
      throw error;
    }
  }

  throw new Error("Max retries exceeded");
}
```
