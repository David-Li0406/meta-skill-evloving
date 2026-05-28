---
title: v6 Uses ModelMessage Not CoreMessage
impact: HIGH
tags: message, ModelMessage, CoreMessage, v6, breaking-change
---

## v6 Uses ModelMessage Not CoreMessage

**Impact: HIGH**

AI SDK v6 renamed `CoreMessage` to `ModelMessage`. The old import will fail.

**Incorrect (v5 pattern):**

```typescript
import { type CoreMessage } from 'ai'  // ❌ Not exported in v6

const messages: CoreMessage[] = [
  { role: 'user', content: 'Hello' }
]
```

**Correct (v6 pattern):**

```typescript
import { type ModelMessage } from 'ai'  // ✅ v6 type

const messages: ModelMessage[] = [
  { role: 'user', content: 'Hello' },
  { role: 'assistant', content: 'Hi there!' },
]
```

Reference: [Messages](https://sdk.vercel.ai/docs/ai-sdk-core/generating-text#messages)
