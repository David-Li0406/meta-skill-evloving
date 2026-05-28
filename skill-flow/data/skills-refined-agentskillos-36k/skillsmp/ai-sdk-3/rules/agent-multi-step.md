---
title: Multi-Step Agent Pattern
impact: HIGH
tags: agent, multi-step, stopWhen, steps
---

## Multi-Step Agent Pattern

**Impact: HIGH**

Complete pattern for multi-step agentic workflows where the model makes multiple tool calls.

**Full agent pattern:**

```typescript
import { generateText, stepCountIs, tool, type ModelMessage } from 'ai'
import { z } from 'zod'

const agentTools = {
  lookupUser: tool({
    description: 'Look up customer account',
    inputSchema: z.object({
      email: z.string().email(),
    }),
    execute: async ({ email }) => {
      return { found: true, name: 'John' }
    },
  }),
  draftResponse: tool({
    description: 'Draft response to send',
    inputSchema: z.object({
      body: z.string(),
    }),
    execute: async ({ body }) => {
      return { drafted: true, body }
    },
  }),
}

async function runAgent(message: string) {
  const messages: ModelMessage[] = [
    { role: 'user', content: message },
  ]

  const result = await generateText({
    model: 'anthropic/claude-opus-4-5',
    system: 'You are a helpful support agent.',
    messages,
    tools: agentTools,
    stopWhen: stepCountIs(5),  // Max 5 steps
  })

  // Extract tool calls with results
  const toolCalls = result.steps.flatMap((step) => {
    const resultsMap = new Map(
      (step.toolResults || []).map((r) => [r.toolCallId, r.output])
    )
    return (step.toolCalls || []).map((tc) => ({
      name: tc.toolName,
      args: tc.input,
      result: resultsMap.get(tc.toolCallId),
    }))
  })

  return {
    response: result.text,
    toolCalls,
    stepCount: result.steps.length,
  }
}
```

Reference: [Multi-Step Calls](https://sdk.vercel.ai/docs/ai-sdk-core/generating-text#multi-step-calls)
