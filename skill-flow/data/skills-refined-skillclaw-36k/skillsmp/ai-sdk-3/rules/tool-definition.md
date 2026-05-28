---
title: Tool Definition with tool()
impact: HIGH
tags: tool, definition, inputSchema, execute
---

## Tool Definition with tool()

**Impact: HIGH**

Define tools using the `tool()` function with `inputSchema` and `execute`.

**Complete tool definition:**

```typescript
import { tool } from 'ai'
import { z } from 'zod'

const lookupUser = tool({
  description: 'Look up a user by email',
  inputSchema: z.object({
    email: z.string().email().describe('User email address'),
    includeOrders: z.boolean().optional().describe('Include order history'),
  }),
  execute: async ({ email, includeOrders = false }) => {
    const user = await db.users.findUnique({ where: { email } })
    if (!user) {
      return { found: false, message: 'User not found' }
    }
    return {
      found: true,
      user,
      orders: includeOrders ? await getOrders(user.id) : undefined,
    }
  },
})
```

**Multiple tools:**

```typescript
const agentTools = {
  lookupUser: tool({ ... }),
  searchKnowledge: tool({ ... }),
  draftResponse: tool({ ... }),
}

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  messages,
  tools: agentTools,
})
```

Reference: [Tools](https://sdk.vercel.ai/docs/ai-sdk-core/tools-and-tool-calling)
