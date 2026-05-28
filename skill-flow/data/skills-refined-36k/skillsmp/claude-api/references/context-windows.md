# Context Windows Reference

The context window is Claude's "working memory" - the total amount of text (measured in tokens) that Claude can look back on and reference when generating new text, plus the new text it generates. This is different from the large corpus of data Claude was trained on.

A larger context window allows Claude to understand and respond to more complex and lengthy prompts, while a smaller context window may limit the ability to handle longer prompts or maintain coherence over extended conversations.

## Table of Contents

- [Basic Context Window](#basic-context-window)
- [Context Window Sizes](#context-window-sizes)
- [Context with Extended Thinking](#context-with-extended-thinking)
- [Context with Extended Thinking and Tool Use](#context-with-extended-thinking-and-tool-use)
- [1M Token Context Window](#1m-token-context-window)
- [Context Awareness](#context-awareness)
- [Context Management](#context-management)

---

## Basic Context Window

Each conversation turn accumulates within the context window. Previous turns are preserved completely.

**Key concepts:**

- **Linear growth pattern**: Context usage grows linearly with each turn
- **200K token capacity**: Standard context window (200,000 tokens) for most models
- **Input-output flow**: Each turn consists of:
  - **Input phase**: All previous conversation history + current user message
  - **Output phase**: Generated response that becomes part of future input

**Token calculation:**
```
context_used = input_tokens + output_tokens
```

---

## Context Window Sizes

| Model | Standard Context | Extended Context |
|-------|-----------------|------------------|
| Claude Sonnet 4.5 | 200K tokens | 1M tokens (beta) |
| Claude Haiku 4.5 | 200K tokens | - |
| Claude Opus 4.5 | 200K tokens | - |
| Claude Sonnet 4 | 200K tokens | 1M tokens (beta) |
| Claude Opus 4.1 | 200K tokens | - |
| Claude Opus 4 | 200K tokens | - |

**Approximate capacity:**
- 200K tokens ≈ 150K words ≈ 680K unicode characters
- 1M tokens ≈ 750K words ≈ 3.4M unicode characters

---

## Context with Extended Thinking

When using extended thinking, all tokens (including thinking) count toward the context window limit, with important nuances for multi-turn conversations.

**Key behaviors:**

1. **Thinking budget**: Subset of `max_tokens` parameter, billed as output tokens
2. **Automatic stripping**: Previous thinking blocks are automatically removed from context for subsequent turns
3. **Token efficiency**: Thinking blocks are billed only once during generation

**Token calculation with thinking:**
```
context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens
```

**Example flow:**

```
Turn 1:
  Input: user message (100 tokens)
  Output: thinking (5000 tokens) + response (500 tokens)
  Total billed output: 5500 tokens

Turn 2:
  Input: previous user (100) + previous response (500) + new user (100)
         Note: thinking (5000) automatically stripped
  Output: new thinking (3000 tokens) + response (400 tokens)
  Total billed output: 3400 tokens
```

**Important:** You don't need to strip thinking blocks yourself. The API does this automatically if you pass them back.

---

## Context with Extended Thinking and Tool Use

When combining extended thinking with tool use, thinking blocks have special handling requirements.

### Turn-by-Turn Flow

**Turn 1 (Initial request):**
- Input: Tools configuration + user message
- Output: Thinking + text + tool_use request
- All components count toward context window

**Turn 2 (Tool result):**
- Input: ALL blocks from Turn 1 (including thinking) + tool_result
- Output: Text only (no new thinking until next user message)
- **Critical**: Thinking block MUST be returned with tool results

**Turn 3 (Continue conversation):**
- Input: Previous turns (thinking now stripped) + new user message
- Output: New thinking + response
- Previous thinking automatically stripped

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
# Response contains: [thinking_block, tool_use_block]

# Turn 2: Return tool result WITH thinking block
response2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather?"},
        {"role": "assistant", "content": response1.content},  # Includes thinking!
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "...", "content": "72°F sunny"}
        ]}
    ]
)
# Response contains: [text_block] (no new thinking)

# Turn 3: New user message - thinking can now be stripped
response3 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather?"},
        {"role": "assistant", "content": response1.content},  # API strips thinking
        {"role": "user", "content": [{"type": "tool_result", ...}]},
        {"role": "assistant", "content": response2.content},
        {"role": "user", "content": "Thanks! What about tomorrow?"}
    ]
)
# Response contains: [new_thinking_block, text_block]
```

### Important Rules

1. **Preserve thinking during tool use**: Include unmodified thinking blocks when posting tool results
2. **Don't modify thinking blocks**: System uses cryptographic signatures to verify authenticity; modified blocks cause API errors
3. **Interleaved thinking**: Claude 4 models support thinking between tool calls for more sophisticated reasoning after receiving tool results
4. **Claude 3.7 limitation**: No interleaved thinking - requires non-tool_result user turn between

**Token calculation with tool use:**
```
context_window = input_tokens + current_turn_tokens
```

---

## 1M Token Context Window

Claude Sonnet 4 and 4.5 support 1M token context window (beta).

### Enabling 1M Context

**Python:**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Process this large document..."}],
    betas=["context-1m-2025-08-07"]
)
```

**TypeScript:**
```typescript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Process this large document..." }],
  betas: ["context-1m-2025-08-07"]
});
```

**cURL:**
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: context-1m-2025-08-07" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "..."}]
  }'
```

### Requirements and Limitations

| Requirement | Details |
|-------------|---------|
| **Models** | Claude Sonnet 4, Claude Sonnet 4.5 only |
| **Usage tier** | Tier 4 or custom rate limits required |
| **Availability** | Claude API, Microsoft Foundry, AWS Bedrock, Google Vertex AI |
| **Status** | Beta - features/pricing may change |

### Pricing

Requests exceeding 200K tokens use premium pricing:
- **Input tokens**: 2x standard rate
- **Output tokens**: 1.5x standard rate

Example for Claude Sonnet 4.5:
- Standard: $3/MTok input, $15/MTok output
- Long context (>200K): $6/MTok input, $22.50/MTok output

---

## Context Awareness

Claude Sonnet 4.5 and Haiku 4.5 feature **context awareness** - the ability to track remaining context window throughout a conversation.

### How It Works

**Initial budget notification:**
```
<budget:token_budget>200000</budget:token_budget>
```

**After each tool call:**
```
<system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>
```

Budget values:
- 200K tokens (standard)
- 500K tokens (Claude.ai Enterprise)
- 1M tokens (beta, eligible organizations)

### Benefits

Context awareness enables:
- **Better task persistence**: Claude continues until completion rather than guessing remaining capacity
- **Long-running agents**: Sustained focus across extended sessions
- **Multi-window workflows**: Effective state transitions
- **Token management**: Claude can plan output based on remaining capacity

### Models with Context Awareness

- Claude Sonnet 4.5
- Claude Haiku 4.5

---

## Context Management

### Validation Behavior

Starting with Claude Sonnet 3.7, if prompt + output tokens exceeds context window, the API returns a validation error instead of silently truncating.

```python
from anthropic import BadRequestError

try:
    response = client.messages.create(...)
except BadRequestError as e:
    if "context window" in str(e):
        print("Request exceeds context window")
```

### Token Counting

Use the token counting API to estimate usage before sending:

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": large_content}],
    system="System prompt..."
)

print(f"Estimated tokens: {count.input_tokens}")

# Check if within limits
if count.input_tokens + expected_output < 200000:
    response = client.messages.create(...)
```

### Best Practices

1. **Monitor token usage**: Track `usage` in responses
2. **Plan for output**: Reserve tokens for Claude's response
3. **Use token counting**: Estimate before sending large requests
4. **Consider caching**: Use prompt caching for repeated large contexts
5. **Summarize when needed**: For very long conversations, summarize older turns

### Calculating Available Output

```python
context_limit = 200000  # or 1M for extended context
input_tokens = response.usage.input_tokens
available_for_output = context_limit - input_tokens

# Set max_tokens accordingly
safe_max_tokens = min(64000, available_for_output - 1000)  # Leave buffer
```
