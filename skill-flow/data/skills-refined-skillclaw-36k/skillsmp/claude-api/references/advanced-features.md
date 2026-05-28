# Advanced Features Reference

## Table of Contents

- [Prompt Caching](#prompt-caching)
- [Message Batches](#message-batches)
- [Token Counting](#token-counting)
- [Extended Thinking](#extended-thinking)
- [PDF Support](#pdf-support)
- [Citations](#citations)

---

## Prompt Caching

Cache frequently used context to reduce latency and costs. For comprehensive documentation, see [prompt-caching.md](prompt-caching.md).

### Quick Example

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert on the following documentation:\n\n" + long_docs,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Summarize the key points"}]
)

# Check cache usage
print(f"Cache read: {message.usage.cache_read_input_tokens}")
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
```

### Key Points

| Feature | Details |
|---------|---------|
| **Minimum tokens** | 1024 (Sonnet), 4096 (Opus 4.5, Haiku 4.5), 2048 (Haiku 3) |
| **Default TTL** | 5 minutes (refreshed on use) |
| **Max breakpoints** | 4 per request |
| **Cache order** | `tools` → `system` → `messages` |
| **Pricing** | Write: 1.25x base, Read: 0.1x base |

### What Can Be Cached

- System prompts and tool definitions
- Large documents and context
- Conversation history (multi-turn)
- Images and PDFs (in user turns)

---

## Message Batches

Process many requests asynchronously at 50% reduced cost.

### Python

```python
# Create batch
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello"}]
            }
        },
        {
            "custom_id": "request-2",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hi there"}]
            }
        }
    ]
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")

# Poll for completion
import time
while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

# Get results
for result in client.messages.batches.results(batch.id):
    print(f"{result.custom_id}: {result.result.message.content[0].text}")
```

### TypeScript

```typescript
// Create batch
const batch = await client.messages.batches.create({
  requests: [
    {
      custom_id: "request-1",
      params: {
        model: "claude-sonnet-4-5-20250929",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello" }],
      },
    },
    {
      custom_id: "request-2",
      params: {
        model: "claude-sonnet-4-5-20250929",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hi there" }],
      },
    },
  ],
});

console.log(`Batch ID: ${batch.id}`);

// Poll for completion
let status = batch.processing_status;
while (status !== "ended") {
  await new Promise((resolve) => setTimeout(resolve, 60000));
  const updated = await client.messages.batches.retrieve(batch.id);
  status = updated.processing_status;
}

// Get results
for await (const result of client.messages.batches.results(batch.id)) {
  if (result.result.type === "succeeded") {
    console.log(`${result.custom_id}: ${result.result.message.content[0].text}`);
  }
}
```

### Batch Operations

```python
# List batches
batches = client.messages.batches.list(limit=10)

# Cancel batch
client.messages.batches.cancel(batch_id)
```

### Batch Limits

- Max 100,000 requests per batch
- Max 256 MB per batch
- Results available for 29 days
- Processing time: minutes to hours depending on load

---

## Token Counting

Count tokens before sending requests.

### Python

```python
# Count message tokens
count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)
print(f"Input tokens: {count.input_tokens}")

# With system prompt
count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Hello"}]
)

# With tools
count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather?"}]
)
```

### TypeScript

```typescript
const count = await client.messages.countTokens({
  model: "claude-sonnet-4-5-20250929",
  messages: [{ role: "user", content: "Hello, how are you?" }],
});

console.log(`Input tokens: ${count.input_tokens}`);
```

---

## Extended Thinking

Enable Claude to think through complex problems step-by-step.

For comprehensive documentation including tool use, interleaved thinking, and prompt caching, see [extended-thinking.md](extended-thinking.md).

### Quick Example

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{"role": "user", "content": "Solve this complex math problem..."}]
)

for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

### Guidelines

| Requirement | Value |
|-------------|-------|
| `budget_tokens` | Minimum 1024 |
| `max_tokens` | Must be > `budget_tokens` |
| `temperature` | Must be 1 (default) |

### Supported Models

All Claude 4 family models and Claude Sonnet 3.7 support extended thinking

---

## PDF Support

Send PDFs directly to Claude for analysis.

### Python - Base64

```python
import base64

with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data
                }
            },
            {"type": "text", "text": "Summarize this document"}
        ]
    }]
)
```

### Python - URL

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "url",
                    "url": "https://example.com/document.pdf"
                }
            },
            {"type": "text", "text": "What are the key findings?"}
        ]
    }]
)
```

### TypeScript

```typescript
import * as fs from "fs";

const pdfData = fs.readFileSync("document.pdf").toString("base64");

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: pdfData,
          },
        },
        { type: "text", text: "Summarize this document" },
      ],
    },
  ],
});
```

### PDF Limits

- Max 100 pages per PDF
- Max ~32MB file size
- Each page counts as ~1500 tokens
- Supports text, images, charts, and tables within PDFs

---

## Citations

Get source references for Claude's responses with document citations.

For comprehensive documentation including document types, citation types, streaming, and token costs, see [citations.md](citations.md).

### Quick Example

```python
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "text",
                    "media_type": "text/plain",
                    "data": "The grass is green. The sky is blue."
                },
                "citations": {"enabled": True}
            },
            {"type": "text", "text": "What colors are mentioned?"}
        ]
    }]
)

for block in message.content:
    if block.type == "text" and hasattr(block, "citations") and block.citations:
        for citation in block.citations:
            print(f"Cited: {citation.cited_text}")
```

### Document Types

| Type | Source | Citation Type |
|------|--------|---------------|
| Plain text | `type: "text"` | `char_location` (0-indexed) |
| PDF | `type: "base64"` or `"url"` | `page_location` (1-indexed) |
| Custom | `type: "content"` | `content_block_location` (0-indexed) |

**Note:** Citations and Structured Outputs are incompatible - using both returns a 400 error.
