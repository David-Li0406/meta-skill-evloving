---
title: AI Gateway Model Strings
impact: CRITICAL
tags: provider, gateway, model, setup
---

## AI Gateway Model Strings

**Impact: CRITICAL**

Use AI Gateway for simplified model access. Pass model as a string, no provider imports needed.

**Incorrect (unnecessary provider import):**

```typescript
import { anthropic } from '@ai-sdk/anthropic'

const result = await generateText({
  model: anthropic('claude-opus-4-5'),
  prompt: 'Hello',
})
```

**Correct (AI Gateway string):**

```typescript
import { generateText } from 'ai'

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',  // AI Gateway handles auth
  prompt: 'Hello',
})
```

**Configuration:**
- Set `AI_GATEWAY_API_KEY` environment variable
- Model format: `provider/model-name` (e.g., `anthropic/claude-opus-4-5`, `openai/gpt-4o`)

Reference: [AI Gateway](https://sdk.vercel.ai/docs/ai-sdk-core/provider-management)
