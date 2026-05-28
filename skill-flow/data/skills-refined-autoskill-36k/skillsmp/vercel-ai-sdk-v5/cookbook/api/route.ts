/**
 * API Route for AI agent conversations
 * 
 * Features:
 * - Send only last message pattern
 * - Anthropic with extended thinking
 * - Custom data streaming
 * - Message persistence
 * - Disconnect handling
 */
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic'
import {
  streamText,
  createUIMessageStream,
  createUIMessageStreamResponse,
  convertToModelMessages,
  generateId,
  stepCountIs,
} from 'ai'
import { loadAgent, upsertMessage } from '../db/actions'
import { createTools } from '../ai/tools'
import type { MyUIMessage } from '../types/message'

export const maxDuration = 60 // Allow up to 60 seconds

export async function POST(req: Request) {
  const { message, agentId }: { message: MyUIMessage; agentId: string } =
    await req.json()

  // 1. Persist user message immediately
  await upsertMessage({ agentId, id: message.id, message })

  // 2. Load full conversation history
  const messages = await loadAgent(agentId)

  // 3. Create stream with custom data support
  const stream = createUIMessageStream<MyUIMessage>({
    execute: ({ writer }) => {
      // Start message with server-generated ID
      const messageId = generateId()
      writer.write({ type: 'start', messageId })
      writer.write({ type: 'start-step' })

      // Send transient status (not persisted)
      writer.write({
        type: 'data-status',
        data: { message: 'Analyzing your request...', progress: 0 },
        transient: true,
      })

      // Create tools with writer for data streaming
      const tools = createTools(writer)

      // Stream from Anthropic with reasoning
      const result = streamText({
        model: anthropic('claude-sonnet-4-20250514'),
        system: `You are an AI assistant for insurance proposals.
                 
When asked to create a proposal, use the generateProposal tool.
When about to perform any important action, use confirmAction first.
Think through complex requests carefully using your reasoning capabilities.`,
        messages: convertToModelMessages(messages),
        tools,
        stopWhen: stepCountIs(5), // Max 5 tool call rounds
        providerOptions: {
          anthropic: {
            thinking: { type: 'enabled', budgetTokens: 10000 },
          } satisfies AnthropicProviderOptions,
        },
        headers: {
          // Enable fine-grained tool streaming
          'anthropic-beta': 'fine-grained-tool-streaming-2025-05-14',
        },
      })

      // Consume stream to handle disconnects
      result.consumeStream()

      // Merge model stream (without start since we sent our own)
      writer.merge(result.toUIMessageStream({ sendStart: false }))
    },
    originalMessages: messages,
    onFinish: async ({ responseMessage }) => {
      // Persist assistant response
      await upsertMessage({
        agentId,
        id: responseMessage.id,
        message: responseMessage,
      })
    },
    onError: (error) => {
      console.error('Stream error:', error)
      return error instanceof Error ? error.message : 'An error occurred'
    },
  })

  return createUIMessageStreamResponse({
    stream,
    headers: {
      'X-Agent-Id': agentId,
    },
  })
}

/**
 * Alternative: Simple route without custom streaming
 * Use when you don't need data parts or custom start
 */
export async function POST_simple(req: Request) {
  const { message, agentId }: { message: MyUIMessage; agentId: string } =
    await req.json()

  await upsertMessage({ agentId, id: message.id, message })
  const messages = await loadAgent(agentId)

  const result = streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    messages: convertToModelMessages(messages),
    providerOptions: {
      anthropic: {
        thinking: { type: 'enabled', budgetTokens: 10000 },
      } satisfies AnthropicProviderOptions,
    },
  })

  result.consumeStream()

  return result.toUIMessageStreamResponse({
    originalMessages: messages,
    sendReasoning: true,
    messageMetadata: ({ part }) => {
      if (part.type === 'start') {
        return { createdAt: Date.now(), model: 'claude-sonnet-4-20250514' }
      }
      if (part.type === 'finish') {
        return {
          inputTokens: part.totalUsage.inputTokens,
          outputTokens: part.totalUsage.outputTokens,
          totalTokens: part.totalUsage.totalTokens,
          finishReason: part.finishReason,
        }
      }
    },
    onFinish: async ({ responseMessage }) => {
      await upsertMessage({
        agentId,
        id: responseMessage.id,
        message: responseMessage,
      })
    },
  })
}
