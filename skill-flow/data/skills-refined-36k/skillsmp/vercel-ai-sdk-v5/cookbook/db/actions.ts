/**
 * Server actions for agent CRUD operations
 */
'use server'

import { and, eq, gt } from 'drizzle-orm'
import { db } from '@/db'
import { agents, messages, parts } from './schema'
import type { MyUIMessage } from '../types/message'
import {
  mapUIPartsToDBParts,
  mapDBPartToUIPart,
} from '../utils/message-mapping'

/**
 * Create a new agent session
 */
export async function createAgent(): Promise<string> {
  const [{ id }] = await db.insert(agents).values({}).returning()
  return id
}

/**
 * Get all agents (for listing)
 */
export async function getAgents() {
  return db.select().from(agents).orderBy(agents.updatedAt)
}

/**
 * Insert or update a message with its parts
 * Uses transaction for atomicity
 */
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
    // Upsert message
    await tx
      .insert(messages)
      .values({
        agentId,
        role: message.role,
        id,
      })
      .onConflictDoUpdate({
        target: messages.id,
        set: { agentId },
      })

    // Replace all parts (delete + insert for simplicity)
    await tx.delete(parts).where(eq(parts.messageId, id))
    
    if (dbParts.length > 0) {
      await tx.insert(parts).values(dbParts)
    }
  })

  // Update agent timestamp
  await db
    .update(agents)
    .set({ updatedAt: new Date() })
    .where(eq(agents.id, agentId))
}

/**
 * Load all messages for an agent
 */
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

/**
 * Delete an agent and all associated data (cascade)
 */
export async function deleteAgent(agentId: string) {
  await db.delete(agents).where(eq(agents.id, agentId))
}

/**
 * Delete a message and all subsequent messages
 * Useful for "edit and regenerate" functionality
 */
export async function deleteMessage(messageId: string) {
  await db.transaction(async (tx) => {
    // Find the target message
    const [target] = await tx
      .select()
      .from(messages)
      .where(eq(messages.id, messageId))
      .limit(1)

    if (!target) return

    // Delete all messages after this one in the same agent
    await tx.delete(messages).where(
      and(
        eq(messages.agentId, target.agentId),
        gt(messages.createdAt, target.createdAt)
      )
    )

    // Delete the target message (parts cascade)
    await tx.delete(messages).where(eq(messages.id, messageId))
  })
}

/**
 * Update agent title (e.g., from first message)
 */
export async function updateAgentTitle(agentId: string, title: string) {
  await db
    .update(agents)
    .set({ title, updatedAt: new Date() })
    .where(eq(agents.id, agentId))
}
