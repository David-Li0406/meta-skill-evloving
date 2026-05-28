/**
 * Bidirectional message mapping between UI and DB formats
 */
import type { MyUIMessagePart } from '../types/message'
import type { DBPart, DBPartSelect } from '../db/schema'

/**
 * Convert UI message parts to database format
 */
export function mapUIPartsToDBParts(
  parts: MyUIMessagePart[],
  messageId: string
): DBPart[] {
  return parts.map((part, index) => {
    const base = { messageId, order: index, type: part.type }

    switch (part.type) {
      case 'text':
        return {
          ...base,
          text_text: part.text,
        }

      case 'reasoning':
        return {
          ...base,
          reasoning_text: part.text,
          providerMetadata: part.providerMetadata,
        }

      case 'source-url':
        return {
          ...base,
          source_url_sourceId: part.sourceId,
          source_url_url: part.url,
          source_url_title: part.title,
          providerMetadata: part.providerMetadata,
        }

      case 'step-start':
        return base

      case 'tool-confirmAction':
        return {
          ...base,
          tool_toolCallId: part.toolCallId,
          tool_state: part.state,
          tool_confirmAction_input:
            part.state === 'input-available' ||
            part.state === 'output-available' ||
            part.state === 'output-error'
              ? part.input
              : undefined,
          tool_confirmAction_output:
            part.state === 'output-available' ? part.output : undefined,
          tool_errorText:
            part.state === 'output-error' ? part.errorText : undefined,
        }

      case 'tool-generateProposal':
        return {
          ...base,
          tool_toolCallId: part.toolCallId,
          tool_state: part.state,
          tool_generateProposal_input:
            part.state === 'input-available' ||
            part.state === 'output-available' ||
            part.state === 'output-error'
              ? part.input
              : undefined,
          tool_generateProposal_output:
            part.state === 'output-available' ? part.output : undefined,
          tool_errorText:
            part.state === 'output-error' ? part.errorText : undefined,
        }

      case 'tool-getWeatherInfo':
        // Simple tool - just store state and result
        return {
          ...base,
          tool_toolCallId: part.toolCallId,
          tool_state: part.state,
        }

      case 'tool-getUserLocation':
        return {
          ...base,
          tool_toolCallId: part.toolCallId,
          tool_state: part.state,
        }

      case 'data-proposal':
        return {
          ...base,
          data_proposal_id: part.id,
          data_proposal_status: part.data.status,
          data_proposal_title: part.data.title,
          data_proposal_content: part.data.content,
        }

      default:
        // Handle unknown types gracefully
        console.warn(`Unknown part type: ${(part as any).type}`)
        return base
    }
  })
}

/**
 * Convert database part to UI format
 */
export function mapDBPartToUIPart(part: DBPartSelect): MyUIMessagePart {
  switch (part.type) {
    case 'text':
      return {
        type: 'text',
        text: part.text_text!,
      }

    case 'reasoning':
      return {
        type: 'reasoning',
        text: part.reasoning_text!,
        providerMetadata: part.providerMetadata ?? undefined,
      }

    case 'source-url':
      return {
        type: 'source-url',
        sourceId: part.source_url_sourceId!,
        url: part.source_url_url!,
        title: part.source_url_title,
        providerMetadata: part.providerMetadata ?? undefined,
      }

    case 'step-start':
      return { type: 'step-start' }

    case 'tool-confirmAction':
      return mapToolPart(part, 'confirmAction', {
        inputKey: 'tool_confirmAction_input',
        outputKey: 'tool_confirmAction_output',
      })

    case 'tool-generateProposal':
      return mapToolPart(part, 'generateProposal', {
        inputKey: 'tool_generateProposal_input',
        outputKey: 'tool_generateProposal_output',
      })

    case 'tool-getWeatherInfo':
    case 'tool-getUserLocation':
      // These tools may not have persisted input/output in this example
      return {
        type: part.type as any,
        toolCallId: part.tool_toolCallId!,
        state: part.tool_state!,
      } as any

    case 'data-proposal':
      return {
        type: 'data-proposal',
        id: part.data_proposal_id!,
        data: {
          status: part.data_proposal_status as any,
          title: part.data_proposal_title,
          content: part.data_proposal_content,
        },
      }

    default:
      throw new Error(`Unknown part type: ${part.type}`)
  }
}

/**
 * Helper to map tool parts with proper state handling
 */
function mapToolPart<T extends string>(
  part: DBPartSelect,
  toolName: T,
  keys: { inputKey: keyof DBPartSelect; outputKey: keyof DBPartSelect }
): MyUIMessagePart {
  const baseToolPart = {
    type: `tool-${toolName}` as const,
    toolCallId: part.tool_toolCallId!,
  }

  const input = part[keys.inputKey]
  const output = part[keys.outputKey]

  switch (part.tool_state) {
    case 'input-streaming':
      return {
        ...baseToolPart,
        state: 'input-streaming',
        input,
      } as any

    case 'input-available':
      return {
        ...baseToolPart,
        state: 'input-available',
        input: input!,
      } as any

    case 'output-available':
      return {
        ...baseToolPart,
        state: 'output-available',
        input: input!,
        output: output!,
      } as any

    case 'output-error':
      return {
        ...baseToolPart,
        state: 'output-error',
        input: input!,
        errorText: part.tool_errorText!,
      } as any

    default:
      throw new Error(`Unknown tool state: ${part.tool_state}`)
  }
}
