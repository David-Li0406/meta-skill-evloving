# Persistence

Database persistence for AI SDK v5 using Drizzle ORM with PostgreSQL.

## Schema Design

Use prefix-based columns for message parts to avoid complex polymorphic relationships:

```typescript
// db/schema.ts
import { pgTable, varchar, timestamp, integer, text, jsonb, index, check } from 'drizzle-orm/pg-core'
import { generateId } from 'ai'
import { sql } from 'drizzle-orm'

export const agents = pgTable('agents', {
  id: varchar().primaryKey().$defaultFn(() => generateId()),
  createdAt: timestamp().defaultNow().notNull(),
})

export const messages = pgTable('messages', {
  id: varchar().primaryKey().$defaultFn(() => generateId()),
  agentId: varchar().references(() => agents.id, { onDelete: 'cascade' }).notNull(),
  createdAt: timestamp().defaultNow().notNull(),
  role: varchar().$type<'user' | 'assistant'>().notNull(),
}, (table) => [
  index('messages_agent_id_idx').on(table.agentId),
  index('messages_agent_id_created_at_idx').on(table.agentId, table.createdAt),
])

export const parts = pgTable('parts', {
  id: varchar().primaryKey().$defaultFn(() => generateId()),
  messageId: varchar().references(() => messages.id, { onDelete: 'cascade' }).notNull(),
  type: varchar().notNull(),
  order: integer().notNull().default(0),
  createdAt: timestamp().defaultNow().notNull(),

  // Text parts
  text_text: text(),

  // Reasoning parts
  reasoning_text: text(),

  // Tool parts (shared columns)
  tool_toolCallId: varchar(),
  tool_state: varchar().$type<'input-streaming' | 'input-available' | 'output-available' | 'output-error'>(),
  tool_errorText: varchar(),

  // Tool-specific inputs/outputs (add per tool)
  tool_confirmAction_input: jsonb(),
  tool_confirmAction_output: jsonb(),

  // Custom data parts
  data_proposal_id: varchar(),
  data_proposal_status: varchar(),
  data_proposal_content: jsonb(),

  // Provider metadata
  providerMetadata: jsonb(),
}, (t) => [
  index('parts_message_id_idx').on(t.messageId),
  index('parts_message_id_order_idx').on(t.messageId, t.order),
  
  // Constraints ensure data integrity
  check('text_required', sql`CASE WHEN ${t.type} = 'text' THEN ${t.text_text} IS NOT NULL ELSE TRUE END`),
  check('reasoning_required', sql`CASE WHEN ${t.type} = 'reasoning' THEN ${t.reasoning_text} IS NOT NULL ELSE TRUE END`),
])

export type DBPart = typeof parts.$inferInsert
export type DBPartSelect = typeof parts.$inferSelect
```

## Relations

```typescript
// db/relations.ts
import { relations } from 'drizzle-orm'
import { agents, messages, parts } from './schema'

export const agentsRelations = relations(agents, ({ many }) => ({
  messages: many(messages),
}))

export const messagesRelations = relations(messages, ({ one, many }) => ({
  agent: one(agents, {
    fields: [messages.agentId],
    references: [agents.id],
  }),
  parts: many(parts),
}))

export const partsRelations = relations(parts, ({ one }) => ({
  message: one(messages, {
    fields: [parts.messageId],
    references: [messages.id],
  }),
}))
```

## Database Actions

```typescript
// db/actions.ts
'use server'

import { eq, and, gt } from 'drizzle-orm'
import { db } from '@/db'
import { agents, messages, parts } from '@/db/schema'
import type { MyUIMessage } from '@/features/agents/types/message'
import { mapUIPartsToDBParts, mapDBPartToUIPart } from '@/lib/message-mapping'

export async function createAgent(): Promise<string> {
  const [{ id }] = await db.insert(agents).values({}).returning()
  return id
}

export async function upsertMessage({
  agentId,
  id,
  message,
}: {
  agentId: string
  id: string
  message: MyUIMessage
}) {
  const dbParts = mapUIPartsToDBParts(message.parts, id)

  await db.transaction(async (tx) => {
    await tx
      .insert(messages)
      .values({ agentId, role: message.role, id })
      .onConflictDoUpdate({
        target: messages.id,
        set: { agentId },
      })

    // Delete existing parts and insert new ones
    await tx.delete(parts).where(eq(parts.messageId, id))
    if (dbParts.length > 0) {
      await tx.insert(parts).values(dbParts)
    }
  })
}

export async function loadAgent(agentId: string): Promise<MyUIMessage[]> {
  const result = await db.query.messages.findMany({
    where: eq(messages.agentId, agentId),
    with: {
      parts: {
        orderBy: (parts, { asc }) => [asc(parts.order)],
      },
    },
    orderBy: (messages, { asc }) => [asc(messages.createdAt)],
  })

  return result.map((message) => ({
    id: message.id,
    role: message.role,
    parts: message.parts.map(mapDBPartToUIPart),
  }))
}

export async function deleteAgent(agentId: string) {
  await db.delete(agents).where(eq(agents.id, agentId))
}

export async function deleteMessage(messageId: string) {
  await db.transaction(async (tx) => {
    const [target] = await tx
      .select()
      .from(messages)
      .where(eq(messages.id, messageId))
      .limit(1)

    if (!target) return

    // Delete this message and all subsequent messages
    await tx.delete(messages).where(
      and(
        eq(messages.agentId, target.agentId),
        gt(messages.createdAt, target.createdAt)
      )
    )
    await tx.delete(messages).where(eq(messages.id, messageId))
  })
}
```

## Message Mapping

Bidirectional conversion between UI messages and database rows:

```typescript
// lib/message-mapping.ts
import type { MyUIMessagePart } from '@/features/agents/types/message'
import type { DBPart, DBPartSelect } from '@/db/schema'

export function mapUIPartsToDBParts(
  parts: MyUIMessagePart[],
  messageId: string
): DBPart[] {
  return parts.map((part, index) => {
    const base = { messageId, order: index, type: part.type }

    switch (part.type) {
      case 'text':
        return { ...base, text_text: part.text }

      case 'reasoning':
        return {
          ...base,
          reasoning_text: part.text,
          providerMetadata: part.providerMetadata,
        }

      case 'tool-confirmAction':
        return {
          ...base,
          tool_toolCallId: part.toolCallId,
          tool_state: part.state,
          tool_confirmAction_input:
            part.state !== 'input-streaming' ? part.input : undefined,
          tool_confirmAction_output:
            part.state === 'output-available' ? part.output : undefined,
          tool_errorText:
            part.state === 'output-error' ? part.errorText : undefined,
        }

      case 'data-proposal':
        return {
          ...base,
          data_proposal_id: part.id,
          data_proposal_status: part.data.status,
          data_proposal_content: part.data.content,
        }

      case 'step-start':
        return base

      default:
        throw new Error(`Unsupported part type: ${(part as any).type}`)
    }
  })
}

export function mapDBPartToUIPart(part: DBPartSelect): MyUIMessagePart {
  switch (part.type) {
    case 'text':
      return { type: 'text', text: part.text_text! }

    case 'reasoning':
      return {
        type: 'reasoning',
        text: part.reasoning_text!,
        providerMetadata: part.providerMetadata ?? undefined,
      }

    case 'tool-confirmAction':
      // Handle different tool states
      const baseToolPart = {
        type: 'tool-confirmAction' as const,
        toolCallId: part.tool_toolCallId!,
      }

      switch (part.tool_state) {
        case 'input-streaming':
          return { ...baseToolPart, state: 'input-streaming', input: part.tool_confirmAction_input }
        case 'input-available':
          return { ...baseToolPart, state: 'input-available', input: part.tool_confirmAction_input! }
        case 'output-available':
          return {
            ...baseToolPart,
            state: 'output-available',
            input: part.tool_confirmAction_input!,
            output: part.tool_confirmAction_output!,
          }
        case 'output-error':
          return {
            ...baseToolPart,
            state: 'output-error',
            input: part.tool_confirmAction_input!,
            errorText: part.tool_errorText!,
          }
        default:
          throw new Error(`Unknown tool state: ${part.tool_state}`)
      }

    case 'data-proposal':
      return {
        type: 'data-proposal',
        id: part.data_proposal_id!,
        data: {
          status: part.data_proposal_status as 'loading' | 'complete',
          content: part.data_proposal_content,
        },
      }

    case 'step-start':
      return { type: 'step-start' }

    default:
      throw new Error(`Unsupported part type: ${part.type}`)
  }
}
```

## Send Only Last Message Pattern

Optimize bandwidth by sending only the last message:

```typescript
// Client-side transport configuration
const { messages, sendMessage } = useChat<MyUIMessage>({
  id: agentId,
  messages: initialMessages,
  transport: new DefaultChatTransport({
    api: '/api/agent',
    prepareSendMessagesRequest: ({ messages, id }) => ({
      body: {
        message: messages.at(-1),
        agentId: id,
      },
    }),
  }),
})

// Server-side: Load and merge
export async function POST(req: Request) {
  const { message, agentId } = await req.json()

  // Persist user message immediately
  await upsertMessage({ agentId, id: message.id, message })

  // Load full history
  const messages = await loadAgent(agentId)

  const result = streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    messages: convertToModelMessages(messages),
  })

  result.consumeStream() // Handle disconnects

  return result.toUIMessageStreamResponse({
    originalMessages: messages,
    onFinish: async ({ responseMessage }) => {
      await upsertMessage({
        agentId,
        id: responseMessage.id,
        message: responseMessage,
      })
    },
  })
}
```

## Validation

Validate messages loaded from database before processing:

```typescript
import { validateUIMessages, TypeValidationError } from 'ai'

try {
  const validatedMessages = await validateUIMessages({
    messages: [...previousMessages, newMessage],
    tools,
    metadataSchema,
    dataPartsSchema,
  })
} catch (error) {
  if (error instanceof TypeValidationError) {
    console.error('Validation failed:', error)
    // Handle migration or filtering
  }
  throw error
}
```
