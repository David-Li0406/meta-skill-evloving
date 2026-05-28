# Streaming

Custom data streaming, reconciliation, and advanced stream patterns.

## Stream Creation Options

### Option 1: Simple (streamText only)

```typescript
const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: convertToModelMessages(messages),
})

return result.toUIMessageStreamResponse({
  originalMessages: messages,
  onFinish: ({ messages }) => saveMessages(messages),
})
```

### Option 2: Custom Data Parts (createUIMessageStream)

```typescript
const stream = createUIMessageStream<MyUIMessage>({
  execute: ({ writer }) => {
    // Write custom data
    writer.write({
      type: 'data-status',
      id: 'status-1',
      data: { message: 'Processing...', progress: 0 },
    })

    const result = streamText({
      model: anthropic('claude-sonnet-4-20250514'),
      messages: convertToModelMessages(messages),
    })

    // Merge model stream
    writer.merge(result.toUIMessageStream())
  },
  originalMessages: messages,
  onFinish: ({ responseMessage }) => {
    saveMessage(responseMessage)
  },
})

return createUIMessageStreamResponse({ stream })
```

### Option 3: Full Control (manual start)

```typescript
const stream = createUIMessageStream<MyUIMessage>({
  execute: ({ writer }) => {
    // Manual message start
    writer.write({
      type: 'start',
      messageId: generateId(),
    })
    writer.write({ type: 'start-step' })

    // Custom data before model response
    writer.write({
      type: 'data-context',
      id: 'ctx-1',
      data: { loaded: true },
    })

    const result = streamText({ ... })
    
    // Merge without start event (we already sent it)
    writer.merge(result.toUIMessageStream({ sendStart: false }))
  },
})
```

## Data Part Types

### Persistent Data Parts

Added to `message.parts` and persisted:

```typescript
writer.write({
  type: 'data-proposal',
  id: 'proposal-123', // Required for reconciliation
  data: {
    status: 'loading',
    title: 'Insurance Proposal',
    content: null,
  },
})
```

### Transient Data Parts

Only available in `onData` callback, never persisted:

```typescript
// Server
writer.write({
  type: 'data-notification',
  data: { message: 'Processing step 1...', level: 'info' },
  transient: true, // Won't be in message.parts
})

// Client - only accessible via onData
const { messages } = useChat<MyUIMessage>({
  onData: (dataPart) => {
    if (dataPart.type === 'data-notification') {
      showToast(dataPart.data.message, dataPart.data.level)
    }
  },
})
```

### Sources

For RAG implementations:

```typescript
writer.write({
  type: 'source',
  value: {
    type: 'source',
    sourceType: 'url',
    id: 'source-1',
    url: 'https://docs.example.com/article',
    title: 'Relevant Documentation',
  },
})
```

## Data Part Reconciliation

Same `id` = update existing part (enables progressive loading):

```typescript
execute: async ({ writer }) => {
  const id = generateId()

  // Step 1: Loading state
  writer.write({
    type: 'data-analysis',
    id,
    data: { status: 'loading', result: null },
  })

  // Step 2: Partial result
  const partial = await getPartialAnalysis()
  writer.write({
    type: 'data-analysis',
    id, // Same ID = updates the part
    data: { status: 'processing', result: partial },
  })

  // Step 3: Complete
  const final = await getFinalAnalysis()
  writer.write({
    type: 'data-analysis',
    id, // Same ID = final update
    data: { status: 'complete', result: final },
  })
}
```

Client sees smooth transitions:
```
{ status: 'loading' } → { status: 'processing', result: {...} } → { status: 'complete', result: {...} }
```

## Message Metadata

For message-level info (not part of content):

```typescript
return result.toUIMessageStreamResponse({
  originalMessages: messages,
  messageMetadata: ({ part }) => {
    if (part.type === 'start') {
      return {
        createdAt: Date.now(),
        model: 'claude-sonnet-4-20250514',
      }
    }
    if (part.type === 'finish') {
      return {
        inputTokens: part.totalUsage.inputTokens,
        outputTokens: part.totalUsage.outputTokens,
        totalTokens: part.totalUsage.totalTokens,
      }
    }
  },
})
```

Access on client:
```typescript
{messages.map(m => (
  <div key={m.id}>
    {m.metadata?.totalTokens && (
      <span className="text-xs">{m.metadata.totalTokens} tokens</span>
    )}
  </div>
))}
```

## Reasoning/Thinking Streams

Forward reasoning to client:

```typescript
return result.toUIMessageStreamResponse({
  sendReasoning: true, // Include reasoning parts
})

// Client rendering
{part.type === 'reasoning' && (
  <details className="text-gray-500 text-sm">
    <summary>Thinking...</summary>
    <pre className="whitespace-pre-wrap">{part.text}</pre>
  </details>
)}
```

## Error Handling

```typescript
const stream = createUIMessageStream({
  execute: ({ writer }) => {
    // ...
  },
  onError: (error) => {
    // Return string to send to client
    if (error instanceof Error) return error.message
    return 'An unexpected error occurred'
  },
})
```

## Complete Streaming Example

```typescript
// app/api/agent/route.ts
import {
  streamText,
  createUIMessageStream,
  createUIMessageStreamResponse,
  convertToModelMessages,
  generateId,
} from 'ai'
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic'
import type { MyUIMessage } from '@/features/agents/types/message'

export async function POST(req: Request) {
  const { message, agentId } = await req.json()

  await upsertMessage({ agentId, id: message.id, message })
  const messages = await loadAgent(agentId)

  const stream = createUIMessageStream<MyUIMessage>({
    execute: ({ writer }) => {
      // Start message
      const messageId = generateId()
      writer.write({ type: 'start', messageId })
      writer.write({ type: 'start-step' })

      // Initial status (transient)
      writer.write({
        type: 'data-status',
        data: { message: 'Analyzing request...', progress: 0 },
        transient: true,
      })

      const result = streamText({
        model: anthropic('claude-sonnet-4-20250514'),
        messages: convertToModelMessages(messages),
        providerOptions: {
          anthropic: {
            thinking: { type: 'enabled', budgetTokens: 10000 },
          } satisfies AnthropicProviderOptions,
        },
        tools,
        stopWhen: stepCountIs(5),
      })

      result.consumeStream() // Handle disconnects

      writer.merge(result.toUIMessageStream({ sendStart: false }))
    },
    originalMessages: messages,
    onFinish: async ({ responseMessage }) => {
      await upsertMessage({
        agentId,
        id: responseMessage.id,
        message: responseMessage,
      })
    },
    onError: (error) => error instanceof Error ? error.message : 'Error',
  })

  return createUIMessageStreamResponse({
    stream,
    headers: {
      'X-Agent-Id': agentId,
    },
  })
}
```

## Client Processing

```typescript
const { messages, status } = useChat<MyUIMessage>({
  id: agentId,
  messages: initialMessages,
  transport: new DefaultChatTransport({
    api: '/api/agent',
    prepareSendMessagesRequest: ({ messages, id }) => ({
      body: { message: messages.at(-1), agentId: id },
    }),
  }),
  onData: (dataPart) => {
    // Handle transient parts
    if (dataPart.type === 'data-status') {
      setStatus(dataPart.data)
    }
  },
  onFinish: ({ message }) => {
    // Access final metadata
    console.log('Tokens used:', message.metadata?.totalTokens)
  },
  onError: (error) => {
    toast.error(error.message)
  },
})
```
