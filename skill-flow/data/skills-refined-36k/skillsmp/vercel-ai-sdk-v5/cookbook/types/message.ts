/**
 * Type definitions for AI agent messages
 */
import { UIMessage, UIMessagePart, JSONValue } from 'ai'
import { z } from 'zod'
import type { MyTools } from '../ai/tools'

// === Metadata Schema ===
export const metadataSchema = z.object({
  createdAt: z.number().optional(),
  model: z.string().optional(),
  inputTokens: z.number().optional(),
  outputTokens: z.number().optional(),
  totalTokens: z.number().optional(),
  finishReason: z.string().optional(),
})

export type MessageMetadata = z.infer<typeof metadataSchema>

// === Data Parts Schema ===
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
  }),
})

export type DataParts = z.infer<typeof dataPartsSchema>

// === Combined Message Types ===
export type MyUIMessage = UIMessage<MessageMetadata, DataParts, MyTools>

export type MyUIMessagePart = UIMessagePart<DataParts, MyTools>

// === Provider Metadata ===
export type MyProviderMetadata = Record<string, Record<string, JSONValue>>

// === Re-exports for convenience ===
export { metadataSchema, dataPartsSchema }
