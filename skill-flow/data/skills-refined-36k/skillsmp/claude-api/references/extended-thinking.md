# Extended Thinking Reference

Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, providing transparency into its step-by-step thought process before delivering a final answer.

## Table of Contents

- [Supported Models](#supported-models)
- [How It Works](#how-it-works)
- [Basic Usage](#basic-usage)
- [Extended Thinking with Tool Use](#extended-thinking-with-tool-use)
- [Interleaved Thinking](#interleaved-thinking)
- [Extended Thinking with Prompt Caching](#extended-thinking-with-prompt-caching)
- [Redacted Thinking](#redacted-thinking)
- [Streaming Extended Thinking](#streaming-extended-thinking)
- [Guidelines and Constraints](#guidelines-and-constraints)

---

## Supported Models

| Model | Model ID |
|-------|----------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` |
| Claude Opus 4.1 | `claude-opus-4-1-20250805` |
| Claude Opus 4 | `claude-opus-4-20250514` |

**Note:** API behavior differs across Claude 3.7 and Claude 4 models, but API shapes remain the same.

---

## How It Works

When extended thinking is enabled, Claude creates `thinking` content blocks with internal reasoning before crafting a final response.

**Response structure:**

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem..."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

---

## Basic Usage

### Python

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }]
)

for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

### TypeScript

```typescript
const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000,
  },
  messages: [{
    role: "user",
    content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
  }],
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`Thinking: ${block.thinking}`);
  } else if (block.type === "text") {
    console.log(`Response: ${block.text}`);
  }
}
```

### cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 16000,
    "thinking": {
      "type": "enabled",
      "budget_tokens": 10000
    },
    "messages": [
      {"role": "user", "content": "Solve this complex problem..."}
    ]
  }'
```

---

## Extended Thinking with Tool Use

When Claude uses tools with thinking enabled, thinking blocks require special handling.

### Turn-by-Turn Flow

**Turn 1 (Initial request):**
- Output: `[thinking_block, tool_use_block]`

**Turn 2 (Tool result):**
- Input: Must include thinking block + tool_use block + tool_result
- Output: `[text_block]` (no new thinking until next user message)

**Turn 3 (New user message):**
- Input: Previous thinking stripped automatically
- Output: `[new_thinking_block, text_block]`

### Code Example

```python
# Turn 1: Initial request with tools
response1 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather?"}]
)
# Response: [thinking_block, tool_use_block]

# Turn 2: Return tool result WITH thinking block (required!)
response2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather?"},
        {"role": "assistant", "content": response1.content},  # Includes thinking!
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "...", "content": "72F sunny"}
        ]}
    ]
)
# Response: [text_block] (no new thinking)
```

### Preserving Thinking Blocks

**Critical rules:**

1. **Must preserve during tool use**: Include unmodified thinking blocks when posting tool results
2. **Don't modify**: System uses cryptographic signatures to verify authenticity
3. **API auto-strips later**: For subsequent non-tool turns, API automatically ignores previous thinking blocks

**Recommendation:** Always pass back all thinking blocks. The API will:
- Automatically filter provided thinking blocks
- Use relevant blocks to preserve reasoning
- Only bill for input tokens actually shown to Claude

---

## Interleaved Thinking

Claude 4 models support thinking between tool calls for more sophisticated reasoning.

### Enabling Interleaved Thinking

Add beta header `interleaved-thinking-2025-05-14`:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[...],
    betas=["interleaved-thinking-2025-05-14"]
)
```

### Without vs With Interleaved Thinking

**Without interleaved thinking:**
```
Turn 1: [thinking] -> [tool_use: calculator]
  -> tool result
Turn 2: [tool_use: database_query]  <- no thinking
  -> tool result
Turn 3: [text]  <- no thinking
```

**With interleaved thinking:**
```
Turn 1: [thinking] -> [tool_use: calculator]
  -> tool result
Turn 2: [thinking] -> [tool_use: database_query]  <- thinks about result!
  -> tool result
Turn 3: [thinking] -> [text]  <- thinks before final answer
```

### Considerations

- `budget_tokens` can exceed `max_tokens` (represents total budget across all thinking blocks)
- Only supported for Claude 4 models
- On third-party platforms (Bedrock, Vertex AI), only works with Opus 4.5, Opus 4.1, Opus 4, Sonnet 4

---

## Extended Thinking with Prompt Caching

### Key Behaviors

| Aspect | Behavior |
|--------|----------|
| **Thinking block removal** | Previous thinking blocks removed from context for caching |
| **Cache invalidation** | Changing thinking parameters (enabled/disabled, budget) invalidates message cache |
| **System prompt caching** | System prompts and tools remain cached despite thinking changes |
| **Tool use caching** | Thinking blocks cached and count as input tokens when read from cache |

### Cache-Friendly Pattern

```python
# Keep system prompt cached, thinking in messages
SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": "You are an expert analyst.",
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": LARGE_CONTEXT,
        "cache_control": {"type": "ephemeral"}
    }
]

# Same thinking parameters = cache hit
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 4000},  # Keep consistent!
    system=SYSTEM_PROMPT,
    messages=messages
)
```

**Tip:** Use 1-hour cache duration for extended thinking tasks that take longer than 5 minutes.

---

## Redacted Thinking

Some thinking content may be redacted for safety reasons, appearing as `redacted_thinking` blocks:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze...",
      "signature": "..."
    },
    {
      "type": "redacted_thinking",
      "data": "EmwKAhgBEgy3va3pzix/LafPsn4..."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

**Important:**
- Redacted thinking blocks are normal and expected
- Claude can still use redacted reasoning to inform responses
- Include redacted blocks when passing thinking back to API
- Both `thinking` and `redacted_thinking` count toward token usage

**Test trigger:** Use this string to test redacted thinking handling:
```
ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB
```

---

## Streaming Extended Thinking

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Complex problem..."}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                print("Thinking started...")
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="")
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="")
```

---

## Guidelines and Constraints

### Parameter Requirements

| Parameter | Requirement |
|-----------|-------------|
| `budget_tokens` | Minimum 1024 tokens |
| `max_tokens` | Must be > `budget_tokens` |
| `temperature` | Must be 1 (default) when thinking enabled |

### Best Practices

1. **Use for complex tasks**: Best suited for math, coding, analysis requiring step-by-step reasoning
2. **Don't remove thinking blocks**: API handles context management automatically
3. **Preserve during tool use**: Always include thinking blocks with tool results
4. **Keep parameters consistent**: Changing thinking parameters invalidates cache

### When to Use Extended Thinking

- Mathematical proofs and calculations
- Complex coding problems
- Multi-step analysis
- Reasoning-heavy tasks
- Problems requiring chain-of-thought
