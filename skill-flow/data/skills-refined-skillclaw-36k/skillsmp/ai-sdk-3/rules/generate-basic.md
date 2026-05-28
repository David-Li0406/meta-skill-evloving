---
title: Basic generateText Pattern
impact: HIGH
tags: generate, text, basic
---

## Basic generateText Pattern

**Impact: HIGH**

The core pattern for generating text with AI SDK v6.

**Basic usage:**

```typescript
import { generateText } from 'ai'

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  prompt: 'What is 2 + 2?',
})

console.log(result.text)  // "2 + 2 equals 4"
```

**With system message and messages array:**

```typescript
import { generateText, type ModelMessage } from 'ai'

const messages: ModelMessage[] = [
  { role: 'user', content: 'What is TypeScript?' }
]

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  system: 'You are a helpful assistant.',
  messages,
  temperature: 0.7,
  maxTokens: 1024,
})
```

**Result properties:**
- `result.text` - Generated text
- `result.usage` - Token usage (`inputTokens`, `outputTokens`)
- `result.finishReason` - Why generation stopped (`'stop'`, `'length'`, `'tool-calls'`)

Reference: [generateText](https://sdk.vercel.ai/docs/reference/ai-sdk-core/generate-text)
