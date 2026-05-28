# Claude API Skill

> **Install:** `npx skills add diskd-ai/claude-api` | [skills.sh](https://skills.sh)

Integration skill for building AI-powered applications with Anthropic's Claude API.

---

## Scope and Purpose

This skill provides guidance and patterns for working with Anthropic's Claude API, covering:

* Chat completions via Messages API
* Tool use and function calling
* Vision and image inputs
* Streaming responses
* Token counting
* Prompt caching
* Extended thinking
* PDF processing and citations
* Message batches

---

## When to Use This Skill

**Triggers:**

* Mentions of Anthropic, Claude API, or Claude SDK
* Working with Messages API or Claude models
* Using Python SDK (`anthropic`) or TypeScript SDK (`@anthropic-ai/sdk`)
* Tasks involving Claude-specific features (prompt caching, extended thinking, batches)

**Use cases:**

* Implementing chat completions with Claude models
* Adding vision capabilities with image inputs
* Building agents with tool use and function calling
* Streaming responses for real-time output
* Optimizing costs with token counting and prompt caching

---

## Quick Reference

### Installation

```bash
# Python
pip install anthropic

# TypeScript/JavaScript
npm install @anthropic-ai/sdk
```

### Environment

```bash
export ANTHROPIC_API_KEY=<your-api-key>
```

### Basic Usage

**Python:**

```python
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(message.content[0].text)
```

**TypeScript:**

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();  // Uses ANTHROPIC_API_KEY env var

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(message.content[0].text);
```

---

## Model Selection Guide

| Use Case | Model | Model ID |
|----------|-------|----------|
| Balanced (recommended) | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| Fast and lightweight | Claude Haiku 4.5 | `claude-haiku-4-5-20251001` |
| Maximum intelligence | Claude Opus 4.5 | `claude-opus-4-5-20251101` |

See [references/models.md](references/models.md) for complete model details, platform IDs, and pricing.

---

## Skill Structure

```
claude-api/
  SKILL.md          # Full API reference and patterns
  README.md         # This file (overview)
  references/       # Supporting documentation
    api-overview.md # Endpoints, auth, rate limits, platforms
    models.md       # Complete model list and pricing
    messages-api.md # Request/response structure
    python-sdk.md   # Python SDK reference
    typescript-sdk.md # TypeScript SDK reference
    streaming.md    # SSE events and deltas
    vision.md       # Image inputs and limits
    token-counting.md # Token counting endpoint
    context-windows.md # Context limits, 1M beta, context awareness
    extended-thinking.md # Step-by-step reasoning, interleaved thinking
    citations.md      # Document citations, source verification
    prompt-caching.md # Cache system prompts and tools
    advanced-features.md # Batches, PDFs
```

---

## Key Patterns

### Streaming Responses

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Vision (Image from URL)

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image", "source": {
                "type": "url",
                "url": "https://example.com/image.jpg"
            }}
        ]
    }]
)
```

### Tool Use

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
}]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

### Token Counting

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(f"Input tokens: {count.input_tokens}")
```

---

## Error Handling

Errors should be captured at the adapter layer and converted to typed Result values per functional architecture conventions.

```python
from dataclasses import dataclass
from typing import Union
from anthropic import Anthropic, RateLimitError, APIConnectionError, APIStatusError

@dataclass(frozen=True)
class Ok:
    value: object

@dataclass(frozen=True)
class Err:
    error: str

Result = Union[Ok, Err]

def send_message(client: Anthropic, content: str) -> Result:
    """Adapter function that converts exceptions to Result values."""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": content}]
        )
        return Ok(response.content[0].text)
    except RateLimitError:
        return Err("RateLimitError")
    except APIConnectionError:
        return Err("ConnectionError")
    except APIStatusError as e:
        return Err(f"APIError: {e.status_code}")
```

---

## Resources

* **Full skill reference**: [SKILL.md](SKILL.md)
* **API overview**: [references/api-overview.md](references/api-overview.md)
* **Models and pricing**: [references/models.md](references/models.md)
* **Messages API**: [references/messages-api.md](references/messages-api.md)
* **Python SDK**: [references/python-sdk.md](references/python-sdk.md)
* **TypeScript SDK**: [references/typescript-sdk.md](references/typescript-sdk.md)
* **Streaming**: [references/streaming.md](references/streaming.md)
* **Vision**: [references/vision.md](references/vision.md)
* **Token counting**: [references/token-counting.md](references/token-counting.md)
* **Prompt caching**: [references/prompt-caching.md](references/prompt-caching.md)
* **Extended thinking**: [references/extended-thinking.md](references/extended-thinking.md)
* **Citations**: [references/citations.md](references/citations.md)
* **Advanced features**: [references/advanced-features.md](references/advanced-features.md)
* **Official docs**: https://docs.anthropic.com
* **Python SDK**: https://github.com/anthropics/anthropic-sdk-python
* **TypeScript SDK**: https://github.com/anthropics/anthropic-sdk-typescript

---

## License

MIT
