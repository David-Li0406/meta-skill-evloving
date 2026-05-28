/**
 * Drizzle ORM relations for agent persistence
 */
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
