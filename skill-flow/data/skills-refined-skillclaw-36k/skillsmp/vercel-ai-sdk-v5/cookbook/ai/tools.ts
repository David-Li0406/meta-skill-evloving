/**
 * AI tool definitions
 * Includes server-side, client-side, and human-in-the-loop tools
 */
import {
  tool,
  ToolSet,
  InferUITools,
  InferToolInput,
  InferToolOutput,
  UIMessageStreamWriter,
  UIMessage,
} from 'ai'
import { z } from 'zod'
import type { DataParts } from '../types/message'

// === Human-in-the-loop Tool ===
// No execute - requires user confirmation on client
export const confirmAction = tool({
  description: 'Ask the user to confirm an action before proceeding',
  inputSchema: z.object({
    action: z.string().describe('The action to confirm'),
    details: z.string().describe('Details about what will happen'),
    severity: z
      .enum(['low', 'medium', 'high'])
      .describe('How impactful is this action'),
  }),
  outputSchema: z.object({
    confirmed: z.boolean(),
    reason: z.string().optional(),
  }),
})

export type ConfirmActionInput = InferToolInput<typeof confirmAction>
export type ConfirmActionOutput = InferToolOutput<typeof confirmAction>

// === Server-side Tool with Data Streaming ===
// Streams progress via data parts
export const generateProposal = (
  writer: UIMessageStreamWriter<UIMessage<never, DataParts>>
) =>
  tool({
    description: 'Generate an insurance proposal for the user',
    inputSchema: z.object({
      coverage: z.string().describe('Type of coverage requested'),
      amount: z.number().describe('Coverage amount'),
      details: z.string().optional().describe('Additional details'),
    }),
    execute: async ({ coverage, amount, details }, { toolCallId }) => {
      // Initial loading state
      writer.write({
        type: 'data-proposal',
        id: toolCallId,
        data: {
          status: 'loading',
          title: `${coverage} Proposal`,
        },
      })

      // Simulate processing
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Update to generating
      writer.write({
        type: 'data-proposal',
        id: toolCallId,
        data: {
          status: 'generating',
          title: `${coverage} Proposal`,
        },
      })

      // Simulate generation
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Final result
      const proposalContent = {
        coverage,
        amount,
        details,
        premium: amount * 0.02,
        generatedAt: new Date().toISOString(),
      }

      writer.write({
        type: 'data-proposal',
        id: toolCallId,
        data: {
          status: 'complete',
          title: `${coverage} Proposal`,
          content: proposalContent,
        },
      })

      return {
        success: true,
        proposalId: toolCallId,
        summary: `Generated ${coverage} proposal for $${amount}`,
      }
    },
  })

export type GenerateProposalInput = InferToolInput<
  ReturnType<typeof generateProposal>
>
export type GenerateProposalOutput = InferToolOutput<
  ReturnType<typeof generateProposal>
>

// === Simple Server-side Tool ===
export const getWeatherInfo = tool({
  description: 'Get weather information for a location',
  inputSchema: z.object({
    location: z.string().describe('City or location name'),
  }),
  execute: async ({ location }) => {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 500))
    
    const conditions = ['sunny', 'cloudy', 'rainy', 'partly cloudy']
    const condition = conditions[Math.floor(Math.random() * conditions.length)]
    const temperature = Math.floor(Math.random() * 30) + 10

    return {
      location,
      condition,
      temperature,
      unit: 'celsius',
    }
  },
})

// === Client-side Tool (no execute) ===
// Handled via onToolCall on client
export const getUserLocation = tool({
  description: 'Get the user\'s current location',
  inputSchema: z.object({}),
  outputSchema: z.object({
    latitude: z.number(),
    longitude: z.number(),
    city: z.string().optional(),
  }),
})

// === Tool Factory ===
// Creates tools with writer for data streaming
export function createTools(
  writer: UIMessageStreamWriter<UIMessage<never, DataParts>>
) {
  return {
    confirmAction,
    generateProposal: generateProposal(writer),
    getWeatherInfo,
    getUserLocation,
  } satisfies ToolSet
}

// === Static Tools (for type inference) ===
export const tools = {
  confirmAction,
  generateProposal: generateProposal(
    // Dummy writer for type inference only
    { write: () => {}, merge: () => {} } as any
  ),
  getWeatherInfo,
  getUserLocation,
} satisfies ToolSet

// === Type Exports ===
export type MyTools = InferUITools<typeof tools>
