/**
 * Database schema for AI agent persistence
 * Uses prefix-based columns for message parts
 */
import {
  check,
  index,
  integer,
  jsonb,
  pgTable,
  real,
  text,
  timestamp,
  varchar,
} from 'drizzle-orm/pg-core'
import { generateId } from 'ai'
import { sql } from 'drizzle-orm'
import type { MyUIMessage, MyProviderMetadata } from '../types/message'
import type {
  ConfirmActionInput,
  ConfirmActionOutput,
  GenerateProposalInput,
  GenerateProposalOutput,
} from '../ai/tools'

// Main agents table (renamed from chats)
export const agents = pgTable('agents', {
  id: varchar()
    .primaryKey()
    .$defaultFn(() => generateId()),
  title: varchar(),
  createdAt: timestamp().defaultNow().notNull(),
  updatedAt: timestamp().defaultNow().notNull(),
})

// Messages table
export const messages = pgTable(
  'messages',
  {
    id: varchar()
      .primaryKey()
      .$defaultFn(() => generateId()),
    agentId: varchar()
      .references(() => agents.id, { onDelete: 'cascade' })
      .notNull(),
    createdAt: timestamp().defaultNow().notNull(),
    role: varchar().$type<MyUIMessage['role']>().notNull(),
  },
  (table) => [
    index('messages_agent_id_idx').on(table.agentId),
    index('messages_agent_id_created_at_idx').on(table.agentId, table.createdAt),
  ]
)

// Parts table with prefix-based columns
export const parts = pgTable(
  'parts',
  {
    id: varchar()
      .primaryKey()
      .$defaultFn(() => generateId()),
    messageId: varchar()
      .references(() => messages.id, { onDelete: 'cascade' })
      .notNull(),
    type: varchar().$type<MyUIMessage['parts'][0]['type']>().notNull(),
    createdAt: timestamp().defaultNow().notNull(),
    order: integer().notNull().default(0),

    // === Text parts ===
    text_text: text(),

    // === Reasoning parts ===
    reasoning_text: text(),

    // === Source URL parts ===
    source_url_sourceId: varchar(),
    source_url_url: varchar(),
    source_url_title: varchar(),

    // === Shared tool columns ===
    tool_toolCallId: varchar(),
    tool_state: varchar().$type<'input-streaming' | 'input-available' | 'output-available' | 'output-error'>(),
    tool_errorText: varchar(),

    // === Tool: confirmAction ===
    tool_confirmAction_input: jsonb().$type<ConfirmActionInput>(),
    tool_confirmAction_output: jsonb().$type<ConfirmActionOutput>(),

    // === Tool: generateProposal ===
    tool_generateProposal_input: jsonb().$type<GenerateProposalInput>(),
    tool_generateProposal_output: jsonb().$type<GenerateProposalOutput>(),

    // === Data part: proposal ===
    data_proposal_id: varchar().$defaultFn(() => generateId()),
    data_proposal_status: varchar().$type<'loading' | 'generating' | 'complete' | 'error'>(),
    data_proposal_title: varchar(),
    data_proposal_content: jsonb(),

    // === Data part: status (typically transient, but can be persisted) ===
    data_status_message: varchar(),
    data_status_progress: real(),

    // === Provider metadata ===
    providerMetadata: jsonb().$type<MyProviderMetadata>(),
  },
  (t) => [
    // Indexes
    index('parts_message_id_idx').on(t.messageId),
    index('parts_message_id_order_idx').on(t.messageId, t.order),

    // Check constraints for data integrity
    check(
      'text_required_if_type_text',
      sql`CASE WHEN ${t.type} = 'text' THEN ${t.text_text} IS NOT NULL ELSE TRUE END`
    ),
    check(
      'reasoning_required_if_type_reasoning',
      sql`CASE WHEN ${t.type} = 'reasoning' THEN ${t.reasoning_text} IS NOT NULL ELSE TRUE END`
    ),
    check(
      'tool_confirmAction_required',
      sql`CASE WHEN ${t.type} = 'tool-confirmAction' THEN ${t.tool_toolCallId} IS NOT NULL AND ${t.tool_state} IS NOT NULL ELSE TRUE END`
    ),
    check(
      'tool_generateProposal_required',
      sql`CASE WHEN ${t.type} = 'tool-generateProposal' THEN ${t.tool_toolCallId} IS NOT NULL AND ${t.tool_state} IS NOT NULL ELSE TRUE END`
    ),
    check(
      'data_proposal_required',
      sql`CASE WHEN ${t.type} = 'data-proposal' THEN ${t.data_proposal_status} IS NOT NULL ELSE TRUE END`
    ),
  ]
)

// Type exports
export type DBPart = typeof parts.$inferInsert
export type DBPartSelect = typeof parts.$inferSelect
export type DBMessage = typeof messages.$inferInsert
export type DBAgent = typeof agents.$inferInsert
