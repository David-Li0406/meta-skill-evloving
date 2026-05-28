---
title: v6 Uses stopWhen Not maxSteps
impact: CRITICAL
tags: agent, multi-step, stopWhen, v6, breaking-change
---

## v6 Uses stopWhen Not maxSteps

**Impact: CRITICAL**

AI SDK v6 replaced `maxSteps` with `stopWhen: stepCountIs(N)` for multi-step agent loops.

**Incorrect (v5 pattern - will fail in v6):**

```typescript
const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  messages,
  tools: agentTools,
  maxSteps: 5,  // ❌ WRONG - v5 syntax
})
```

**Correct (v6 pattern):**

```typescript
import { generateText, stepCountIs } from 'ai'

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  messages,
  tools: agentTools,
  stopWhen: stepCountIs(5),  // ✅ CORRECT - v6 syntax
})
```

**Available stop conditions:**
- `stepCountIs(n)` - Stop after n steps
- `hasToolCall('toolName')` - Stop when specific tool is called
- Custom function: `({ steps }) => boolean`

Reference: [Multi-Step Calls](https://sdk.vercel.ai/docs/ai-sdk-core/generating-text#multi-step-calls)
