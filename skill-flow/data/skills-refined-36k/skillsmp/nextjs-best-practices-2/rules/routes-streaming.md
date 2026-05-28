---
title: Use Streaming for Long Operations
impact: MEDIUM
impactDescription: Progressive response instead of waiting for entire operation
tags: streaming, routes, performance, ux
---

## Use Streaming for Long Operations

Stream responses for long-running operations or large payloads. Users see progress immediately instead of waiting for the entire response.

**Incorrect (blocking response):**

```typescript
// app/api/export/route.ts
export async function GET() {
  // ❌ User waits for entire dataset
  const data = await generateLargeExport() // 30 seconds
  return Response.json(data)
}

// app/api/ai/route.ts
export async function POST(request: Request) {
  const { prompt } = await request.json()
  // ❌ User waits for complete AI response
  const response = await generateAIResponse(prompt) // 10 seconds
  return Response.json({ response })
}
```

**Correct (streaming response):**

```typescript
// app/api/export/route.ts
export async function GET() {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      const items = await db.items.findMany()

      for (const item of items) {
        const processed = await processItem(item)
        controller.enqueue(
          encoder.encode(JSON.stringify(processed) + '\n')
        )
      }

      controller.close()
    },
  })

  return new Response(stream, {
    headers: { 'Content-Type': 'application/x-ndjson' },
  })
}

// app/api/ai/route.ts
export async function POST(request: Request) {
  const { prompt } = await request.json()

  const stream = new ReadableStream({
    async start(controller) {
      const response = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: prompt }],
        stream: true,
      })

      for await (const chunk of response) {
        const text = chunk.choices[0]?.delta?.content || ''
        controller.enqueue(new TextEncoder().encode(text))
      }

      controller.close()
    },
  })

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
```

**Client consumption:**

```typescript
'use client'

async function streamResponse() {
  const response = await fetch('/api/ai', {
    method: 'POST',
    body: JSON.stringify({ prompt: 'Hello' }),
  })

  const reader = response.body?.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader!.read()
    if (done) break

    const text = decoder.decode(value)
    setOutput(prev => prev + text) // Progressive update
  }
}
```

**With AI SDK:**

```typescript
import { OpenAIStream, StreamingTextResponse } from 'ai'

export async function POST(request: Request) {
  const { messages } = await request.json()

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages,
    stream: true,
  })

  const stream = OpenAIStream(response)
  return new StreamingTextResponse(stream)
}
```

Reference: [Route Handlers Streaming](https://nextjs.org/docs/app/building-your-application/routing/route-handlers#streaming)
