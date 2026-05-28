# AI SDK v6 Features

Advanced features introduced in Vercel AI SDK v6.

## ToolLoopAgent

```typescript
// lib/agents/tool-loop-agent.ts
import { streamText, tool } from 'ai'
import { openai } from '@ai-sdk/openai'
import { z } from 'zod'

export async function runToolLoopAgent(userMessage: string) {
  const tools = {
    search: tool({
      description: 'Search for information',
      inputSchema: z.object({ query: z.string() }),
      execute: async ({ query }) => await search(query),
    }),
    calculate: tool({
      description: 'Perform calculations',
      inputSchema: z.object({ expression: z.string() }),
      execute: async ({ expression }) => eval(expression),
    }),
  }

  let messages = [{ role: 'user' as const, content: userMessage }]
  let iteration = 0
  const maxIterations = 10

  while (iteration < maxIterations) {
    const result = await streamText({
      model: openai('gpt-4o'),
      messages,
      tools,
    })

    const response = await result.text
    const toolCalls = await result.toolCalls

    if (toolCalls.length === 0) {
      return response  // No more tool calls, return final response
    }

    // Add assistant message with tool calls
    messages.push({
      role: 'assistant',
      content: response,
      toolCalls,
    })

    // Execute tools and add results
    for (const toolCall of toolCalls) {
      const toolResult = await tools[toolCall.toolName].execute(toolCall.args)
      messages.push({
        role: 'tool',
        toolCallId: toolCall.toolCallId,
        content: JSON.stringify(toolResult),
      })
    }

    iteration++
  }

  throw new Error('Max iterations reached')
}
```

## Output Patterns (v6)

```typescript
// generateObject and streamObject deprecated
// Use Output.object({ schema }) instead

import { streamText, Output } from 'ai'
import { openai } from '@ai-sdk/openai'
import { z } from 'zod'

const productSchema = z.object({
  name: z.string(),
  description: z.string(),
  price: z.number(),
  features: z.array(z.string()),
})

const result = await streamText({
  model: openai('gpt-4o'),
  prompt: 'Generate a product description for a smartwatch',
  output: Output.object({ schema: productSchema }),
})

const product = await result.object  // Typed as Product
```

## Structured Output with Enum

```typescript
const sentimentSchema = z.object({
  sentiment: z.enum(['positive', 'negative', 'neutral']),
  confidence: z.number().min(0).max(1),
  reasoning: z.string(),
})

const result = await streamText({
  model: openai('gpt-4o'),
  prompt: 'Analyze the sentiment: "This product is amazing!"',
  output: Output.object({ schema: sentimentSchema }),
})

const { sentiment, confidence, reasoning } = await result.object
```

## Array Output

```typescript
const itemsSchema = z.array(z.object({
  title: z.string(),
  summary: z.string(),
  priority: z.enum(['high', 'medium', 'low']),
}))

const result = await streamText({
  model: openai('gpt-4o'),
  prompt: 'List 5 action items from this meeting transcript...',
  output: Output.object({ schema: z.object({ items: itemsSchema }) }),
})

const { items } = await result.object
```

## Streaming Objects

```typescript
import { experimental_streamObject as streamObject } from 'ai'

const result = await streamObject({
  model: openai('gpt-4o'),
  schema: productSchema,
  prompt: 'Generate a product description',
})

for await (const partialObject of result.partialObjectStream) {
  console.log('Partial:', partialObject)
  // { name: 'Smar' }
  // { name: 'Smart', description: 'A' }
  // { name: 'Smart', description: 'A cutting-edge...' }
}

const finalObject = await result.object
```

---

Version: 1.0.0
Source: jikime-library-vercel-ai-sdk SKILL.md
