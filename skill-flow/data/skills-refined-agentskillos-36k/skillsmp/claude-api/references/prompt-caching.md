# Prompt Caching

Prompt caching optimizes API usage by resuming from specific prefixes in prompts, reducing processing time and costs for repetitive tasks.

## Table of Contents

- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Pricing](#pricing)
- [Supported Models](#supported-models)
- [Implementation Guide](#implementation-guide)
- [Cache Limitations](#cache-limitations)
- [What Can Be Cached](#what-can-be-cached)
- [Cache Invalidation](#cache-invalidation)
- [Tracking Performance](#tracking-performance)
- [1-Hour Cache Duration](#1-hour-cache-duration)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## Quick Start

### Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing literary works."
        },
        {
            "type": "text",
            "text": "<the entire contents of 'Pride and Prejudice'>",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Analyze the major themes."}]
)

# First request output:
# {"cache_creation_input_tokens":188086,"cache_read_input_tokens":0,"input_tokens":21,"output_tokens":393}

# Second request (same cached content):
# {"cache_creation_input_tokens":0,"cache_read_input_tokens":188086,"input_tokens":21,"output_tokens":393}
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an AI assistant tasked with analyzing literary works."
    },
    {
      type: "text",
      text: "<the entire contents of 'Pride and Prejudice'>",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [{ role: "user", content: "Analyze the major themes." }]
});
```

---

## How It Works

1. System checks if a prompt prefix (up to a cache breakpoint) is already cached
2. If found, uses the cached version (reduced time and cost)
3. Otherwise, processes full prompt and caches the prefix

**Cache lifetime**: 5 minutes by default, refreshed each time cached content is used.

**Cache hierarchy**: `tools` → `system` → `messages` (in that order)

**Useful for**:
- Prompts with many examples
- Large context or background information
- Repetitive tasks with consistent instructions
- Long multi-turn conversations

---

## Pricing

| Model | Base Input | 5m Cache Write | 1h Cache Write | Cache Read | Output |
|-------|------------|----------------|----------------|------------|--------|
| Claude Opus 4.5 | $5/MTok | $6.25/MTok | $10/MTok | $0.50/MTok | $25/MTok |
| Claude Sonnet 4.5 | $3/MTok | $3.75/MTok | $6/MTok | $0.30/MTok | $15/MTok |
| Claude Haiku 4.5 | $1/MTok | $1.25/MTok | $2/MTok | $0.10/MTok | $5/MTok |

**Pricing multipliers**:
- 5-minute cache write: 1.25x base input price
- 1-hour cache write: 2x base input price
- Cache read: 0.1x base input price

---

## Supported Models

- Claude Opus 4.5, 4.1, 4
- Claude Sonnet 4.5, 4, 3.7
- Claude Haiku 4.5, 3.5, 3

---

## Implementation Guide

### Structuring Your Prompt

Place static content at the beginning. Mark reusable content with `cache_control`.

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[
        # ... tool definitions ...
        {
            "name": "last_tool",
            "description": "...",
            "input_schema": {...},
            "cache_control": {"type": "ephemeral"}  # Caches all tools
        }
    ],
    system=[
        {
            "type": "text",
            "text": "System instructions...",
            "cache_control": {"type": "ephemeral"}  # Cache breakpoint 2
        },
        {
            "type": "text",
            "text": "Large context document...",
            "cache_control": {"type": "ephemeral"}  # Cache breakpoint 3
        }
    ],
    messages=[
        {"role": "user", "content": "First question"},
        {"role": "assistant", "content": "First response"},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Follow-up question",
                    "cache_control": {"type": "ephemeral"}  # Cache breakpoint 4
                }
            ]
        }
    ]
)
```

### Automatic Prefix Checking

The system checks for cache hits by working backwards from your breakpoint (up to 20 blocks). You only need one breakpoint at the end of static content in most cases.

**Use multiple breakpoints when**:
- Content changes at different frequencies
- More than 20 blocks before your breakpoint
- Need explicit control over caching

---

## Cache Limitations

### Minimum Cacheable Tokens

| Model | Minimum Tokens |
|-------|----------------|
| Claude Opus 4.5, Haiku 4.5 | 4096 |
| Claude Sonnet 4.5, Sonnet 4, Opus 4.1, Opus 4 | 1024 |
| Claude Haiku 3.5, Haiku 3 | 2048 |

### Other Limits

- Max 4 cache breakpoints per request
- Cache entry available only after first response begins
- For parallel requests, wait for first response before sending others

---

## What Can Be Cached

**Cacheable**:
- Tool definitions (`tools` array)
- System messages (`system` array)
- Text messages (`messages.content`)
- Images and documents (in user turns)
- Tool use and tool results

**Cannot be cached directly**:
- Thinking blocks (but cached alongside other content in subsequent calls)
- Sub-content blocks (like citations) - cache the top-level block instead
- Empty text blocks

---

## Cache Invalidation

| Change | Tools Cache | System Cache | Messages Cache |
|--------|-------------|--------------|----------------|
| Tool definitions | Invalidated | Invalidated | Invalidated |
| Web search toggle | Valid | Invalidated | Invalidated |
| Citations toggle | Valid | Invalidated | Invalidated |
| Tool choice | Valid | Valid | Invalidated |
| Images added/removed | Valid | Valid | Invalidated |
| Thinking parameters | Valid | Valid | Invalidated |

---

## Tracking Performance

Monitor cache performance in the response `usage` field:

```python
response = client.messages.create(...)

print(response.usage.cache_creation_input_tokens)  # Tokens written to cache
print(response.usage.cache_read_input_tokens)      # Tokens read from cache
print(response.usage.input_tokens)                 # Tokens after last breakpoint
```

**Total input tokens**:
```
total = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

---

## 1-Hour Cache Duration

For longer cache lifetime:

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Long content to cache...",
            "cache_control": {
                "type": "ephemeral",
                "ttl": "1h"  # or "5m" for default
            }
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)
```

**When to use 1-hour cache**:
- Prompts used less frequently than every 5 minutes
- Agentic tasks taking longer than 5 minutes
- Long conversations where users may not respond within 5 minutes
- When latency is critical and follow-ups may exceed 5 minutes

**Mixing TTLs**: Longer TTL entries must appear before shorter ones.

---

## Best Practices

1. **Cache stable content**: System instructions, background info, tool definitions
2. **Place cached content first**: Better performance
3. **Use strategic breakpoints**: Separate content that changes at different frequencies
4. **Set breakpoints at conversation end**: Maximize cache hits
5. **Monitor cache hit rates**: Adjust strategy based on metrics

### Use Cases

| Use Case | Strategy |
|----------|----------|
| Conversational agents | Cache long instructions/documents |
| Coding assistants | Cache codebase summaries |
| Large document processing | Cache entire documents |
| Agentic tool use | Cache tool definitions and context |
| RAG applications | Cache retrieved documents |

---

## Examples

### Large Context Caching

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents."
        },
        {
            "type": "text",
            "text": "[Full text of 50-page legal agreement]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "What are the key terms?"}
    ]
)
```

### Caching Tool Definitions

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        },
        # ... more tools ...
        {
            "name": "last_tool",
            "description": "...",
            "input_schema": {...},
            "cache_control": {"type": "ephemeral"}  # Caches ALL tools
        }
    ],
    messages=[{"role": "user", "content": "What's the weather?"}]
)
```

### Multi-Turn Conversation

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "First question"},
        {"role": "assistant", "content": "First answer"},
        {"role": "user", "content": "Second question"},
        {"role": "assistant", "content": "Second answer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Third question",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
)
```

### Multiple Cache Breakpoints (All 4)

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[
        {"name": "search", "description": "...", "input_schema": {...}},
        {
            "name": "get_doc",
            "description": "...",
            "input_schema": {...},
            "cache_control": {"type": "ephemeral"}  # Breakpoint 1: Tools
        }
    ],
    system=[
        {
            "type": "text",
            "text": "Instructions (rarely change)...",
            "cache_control": {"type": "ephemeral"}  # Breakpoint 2: Instructions
        },
        {
            "type": "text",
            "text": "RAG documents (change daily)...",
            "cache_control": {"type": "ephemeral"}  # Breakpoint 3: Context
        }
    ],
    messages=[
        {"role": "user", "content": "Question 1"},
        {"role": "assistant", "content": [{"type": "tool_use", ...}]},
        {"role": "user", "content": [{"type": "tool_result", ...}]},
        {"role": "assistant", "content": "Response"},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Follow-up",
                    "cache_control": {"type": "ephemeral"}  # Breakpoint 4: Conversation
                }
            ]
        }
    ]
)
```

---

## Caching with Extended Thinking

Thinking blocks cannot be marked with `cache_control` directly, but they get cached automatically when passing them back in tool use flows.

**Cache invalidation with thinking**:
- Cache remains valid when only tool results are provided
- Cache invalidated when non-tool-result user content is added (thinking blocks stripped)

```python
# Request 1: Initial query with tool use
response1 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[{"role": "user", "content": "Question requiring tool"}]
)
# Response: [thinking_block] + [tool_use block]

# Request 2: Tool result - thinking blocks get cached
response2 = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[
        {"role": "user", "content": "Question requiring tool"},
        {"role": "assistant", "content": response1.content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "...",
                    "content": "result",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
)
```

---

## FAQ

**Q: Do cache breakpoints add cost?**
No. You only pay for cache writes (25% premium) and reads (90% discount).

**Q: How do I calculate total input tokens?**
```
total = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

**Q: What's the cache lifetime?**
5 minutes by default, refreshed on each use. 1-hour option available at additional cost.

**Q: How many breakpoints can I use?**
Up to 4.

**Q: Can I manually clear the cache?**
No. Caches expire automatically after 5 minutes of inactivity.

**Q: Is caching shared between organizations?**
No. Caches are organization-specific and require 100% identical prompts.
