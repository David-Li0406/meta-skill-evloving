# Types

Type definitions and type safety patterns for AI SDK v5.

## Core Type Structure

```typescript
UIMessage<Metadata, DataParts, Tools>
```

- **Metadata**: Message-level data (tokens, timestamps, model info)
- **DataParts**: Custom data part schemas
- **Tools**: Tool definitions for typed tool parts

## Defining Custom Types

### 1. Metadata Schema

```typescript
// features/agents/types/metadata.ts
import { z } from 'zod'

export const metadataSchema = z.object({
  createdAt: z.number().optional(),
  model: z.string().optional(),
  inputTokens: z.number().optional(),
  outputTokens: z.number().optional(),
  totalTokens: z.number().optional(),
  finishReason: z.string().optional(),
})

export type MessageMetadata = z.infer<typeof metadataSchema>
```

### 2. Data Parts Schema

```typescript
// features/agents/types/data-parts.ts
import { z } from 'zod'

export const dataPartsSchema = z.object({
  proposal: z.object({
    status: z.enum(['loading', 'generating', 'complete', 'error']),
    title: z.string().optional(),
    content: z.any().optional(),
    error: z.string().optional(),
  }),
  
  status: z.object({
    message: z.string(),
    progress: z.number().min(0).max(100).optional(),
    level: z.enum(['info', 'warning', 'error']).optional(),
  }),
  
  analysis: z.object({
    type: z.string(),
    results: z.array(z.any()).optional(),
    confidence: z.number().optional(),
  }),
})

export type DataParts = z.infer<typeof dataPartsSchema>
```

### 3. Tools Definition

```typescript
// ai/tools.ts
import { tool, ToolSet, UIMessageStreamWriter, InferUITools } from 'ai'
import { z } from 'zod'

export const confirmAction = tool({
  description: 'Ask user to confirm an action',
  inputSchema: z.object({
    action: z.string(),
    details: z.string(),
    severity: z.enum(['low', 'medium', 'high']),
  }),
  outputSchema: z.object({
    confirmed: z.boolean(),
    reason: z.string().optional(),
  }),
})

export const generateReport = tool({
  description: 'Generate a report',
  inputSchema: z.object({
    type: z.enum(['summary', 'detailed', 'executive']),
    topic: z.string(),
  }),
  execute: async ({ type, topic }) => {
    // Server-side execution
    return { reportId: 'report-123', status: 'generated' }
  },
})

export const tools = {
  confirmAction,
  generateReport,
} satisfies ToolSet

// Infer tool types
export type MyTools = InferUITools<typeof tools>
```

### 4. Combined Message Type

```typescript
// features/agents/types/message.ts
import { UIMessage, UIMessagePart } from 'ai'
import type { MessageMetadata } from './metadata'
import type { DataParts } from './data-parts'
import type { MyTools } from '@/ai/tools'

export type MyUIMessage = UIMessage<MessageMetadata, DataParts, MyTools>

export type MyUIMessagePart = UIMessagePart<DataParts, MyTools>
```

## Type Inference Helpers

### InferUITool

Infer types from a single tool:

```typescript
import { InferUITool } from 'ai'

type ConfirmActionTool = InferUITool<typeof confirmAction>
// Result:
// {
//   input: { action: string; details: string; severity: 'low' | 'medium' | 'high' }
//   output: { confirmed: boolean; reason?: string }
// }
```

### InferUITools

Infer types from a tool set:

```typescript
import { InferUITools } from 'ai'

type MyTools = InferUITools<typeof tools>
// Result:
// {
//   confirmAction: { input: {...}; output: {...} }
//   generateReport: { input: {...}; output: {...} }
// }
```

## Using Typed Messages

### In useChat

```typescript
import { useChat } from '@ai-sdk/react'
import type { MyUIMessage } from '@/features/agents/types/message'

const { messages, sendMessage } = useChat<MyUIMessage>({
  // Full type safety for messages
})

// messages is MyUIMessage[]
// message.metadata is MessageMetadata | undefined
// message.parts includes typed tool parts
```

### In API Routes

```typescript
import type { MyUIMessage } from '@/features/agents/types/message'

export async function POST(req: Request) {
  const { message, agentId }: { message: MyUIMessage; agentId: string } = 
    await req.json()

  // message.parts is fully typed
}
```

### In createUIMessageStream

```typescript
import { createUIMessageStream } from 'ai'
import type { MyUIMessage } from '@/features/agents/types/message'

const stream = createUIMessageStream<MyUIMessage>({
  execute: ({ writer }) => {
    // writer.write() is type-safe
    writer.write({
      type: 'data-proposal', // autocomplete works
      id: 'p-1',
      data: { status: 'loading' }, // typed data
    })
  },
})
```

## Tool Part Types

Tool parts are typed as `tool-${toolName}`:

```typescript
// Checking part types
message.parts.map((part) => {
  switch (part.type) {
    case 'text':
      // part.text is string
      break
      
    case 'tool-confirmAction':
      // part.toolCallId is string
      // part.state is 'input-streaming' | 'input-available' | 'output-available' | 'output-error'
      // part.input is { action: string; details: string; severity: '...' }
      // part.output is { confirmed: boolean; reason?: string } (when state === 'output-available')
      break
      
    case 'tool-generateReport':
      // Fully typed based on tool definition
      break
      
    case 'data-proposal':
      // part.data is { status: '...'; title?: string; content?: any }
      break
  }
})
```

## Validation

Validate messages from database or external sources:

```typescript
import { validateUIMessages, TypeValidationError } from 'ai'
import { tools } from '@/ai/tools'
import { metadataSchema, dataPartsSchema } from '@/features/agents/types'

async function validateAndProcess(messages: unknown[]) {
  try {
    const validated = await validateUIMessages({
      messages,
      tools,
      metadataSchema,
      dataPartsSchema,
    })
    
    return validated // Typed as MyUIMessage[]
  } catch (error) {
    if (error instanceof TypeValidationError) {
      console.error('Validation errors:', error.errors)
      // Handle schema mismatch (e.g., tool definition changed)
    }
    throw error
  }
}
```

## Extending for Persistence

Type definitions for database mapping:

```typescript
// db/types.ts
import { parts } from './schema'

export type DBPart = typeof parts.$inferInsert
export type DBPartSelect = typeof parts.$inferSelect

// Ensure DB types align with UI types
export function assertPartTypesMatch(
  uiPart: MyUIMessagePart,
  dbPart: DBPartSelect
): void {
  // TypeScript will catch mismatches at compile time
}
```

## Provider Options Types

```typescript
import { AnthropicProviderOptions } from '@ai-sdk/anthropic'

const providerOptions: AnthropicProviderOptions = {
  thinking: { type: 'enabled', budgetTokens: 10000 },
  cacheControl: { type: 'ephemeral' },
}
```

## Complete Type File Example

```typescript
// features/agents/types/index.ts
import { UIMessage, UIMessagePart, InferUITools } from 'ai'
import { z } from 'zod'
import { tools } from '@/ai/tools'

// Metadata
export const metadataSchema = z.object({
  createdAt: z.number().optional(),
  model: z.string().optional(),
  inputTokens: z.number().optional(),
  outputTokens: z.number().optional(),
  totalTokens: z.number().optional(),
})
export type MessageMetadata = z.infer<typeof metadataSchema>

// Data Parts
export const dataPartsSchema = z.object({
  proposal: z.object({
    status: z.enum(['loading', 'complete', 'error']),
    content: z.any().optional(),
  }),
  status: z.object({
    message: z.string(),
    progress: z.number().optional(),
  }),
})
export type DataParts = z.infer<typeof dataPartsSchema>

// Tools
export type MyTools = InferUITools<typeof tools>

// Combined
export type MyUIMessage = UIMessage<MessageMetadata, DataParts, MyTools>
export type MyUIMessagePart = UIMessagePart<DataParts, MyTools>

// Re-export for convenience
export { tools }
export { metadataSchema, dataPartsSchema }
```
