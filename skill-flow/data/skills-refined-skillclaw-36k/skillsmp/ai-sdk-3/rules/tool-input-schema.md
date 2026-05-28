---
title: v6 Uses inputSchema Not parameters
impact: CRITICAL
tags: tool, inputSchema, v6, breaking-change
---

## v6 Uses inputSchema Not parameters

**Impact: CRITICAL**

AI SDK v6 changed the tool() function to use `inputSchema` instead of `parameters`. This is a breaking change from v5.

**Incorrect (v5 pattern - will fail in v6):**

```typescript
const myTool = tool({
  description: 'Get weather',
  parameters: z.object({  // ❌ WRONG - v5 syntax
    location: z.string(),
  }),
  execute: async ({ location }) => {
    return { temperature: 72 }
  },
})
```

**Correct (v6 pattern):**

```typescript
const myTool = tool({
  description: 'Get weather',
  inputSchema: z.object({  // ✅ CORRECT - v6 syntax
    location: z.string().describe('City name'),
  }),
  execute: async ({ location }) => {
    return { temperature: 72 }
  },
})
```

Reference: [Tool Definition](https://sdk.vercel.ai/docs/ai-sdk-core/tools-and-tool-calling)
