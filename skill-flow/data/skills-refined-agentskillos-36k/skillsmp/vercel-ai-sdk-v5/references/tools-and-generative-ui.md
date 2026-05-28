# Tools & Generative UI

Tool calling and dynamic UI generation patterns for AI SDK v5.

## Tool Types Overview

| Type | Has `execute` | Execution Location | Use Case |
|------|--------------|-------------------|----------|
| Server auto | ✅ | Server | API calls, DB operations |
| Client auto | ❌ | Client (`onToolCall`) | Browser APIs, local data |
| Human-in-the-loop | ❌ | Client (manual `addToolOutput`) | Confirmations, approvals |

## Server-Side Tools

Execute automatically on the server:

```typescript
// ai/tools.ts
import { tool, UIMessageStreamWriter } from 'ai'
import { z } from 'zod'

export const getWeather = tool({
  description: 'Get weather for a location',
  inputSchema: z.object({
    city: z.string().describe('City name'),
  }),
  execute: async ({ city }) => {
    const response = await fetch(`https://api.weather.com/${city}`)
    const data = await response.json()
    return { city, temperature: data.temp, condition: data.condition }
  },
})

export const tools = {
  getWeather,
}
```

## Client-Side Auto Tools

Execute automatically via `onToolCall`:

```typescript
// Client tool definition (no execute)
const getLocation = tool({
  description: 'Get user location',
  inputSchema: z.object({}),
  outputSchema: z.object({ location: z.string() }),
})

// Client-side handling
const { messages, sendMessage, addToolOutput } = useChat({
  transport: new DefaultChatTransport({ api: '/api/agent' }),
  
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
  
  async onToolCall({ toolCall }) {
    if (toolCall.dynamic) return // Skip dynamic tools
    
    if (toolCall.toolName === 'getLocation') {
      const position = await navigator.geolocation.getCurrentPosition()
      
      // No await - prevents deadlocks
      addToolOutput({
        tool: 'getLocation',
        toolCallId: toolCall.toolCallId,
        output: { location: `${position.coords.latitude}, ${position.coords.longitude}` },
      })
    }
  },
})
```

## Human-in-the-Loop Tools

Require user confirmation before execution:

```typescript
// Tool definition
export const confirmAction = tool({
  description: 'Ask user to confirm an action',
  inputSchema: z.object({
    action: z.string().describe('Action to confirm'),
    details: z.string().describe('Details about the action'),
  }),
  outputSchema: z.object({
    confirmed: z.boolean(),
    reason: z.string().optional(),
  }),
})

// Client-side rendering
function ChatMessage({ message }: { message: MyUIMessage }) {
  const { addToolOutput } = useChat()
  
  return (
    <div>
      {message.parts.map((part, idx) => {
        if (part.type === 'tool-confirmAction') {
          return (
            <ConfirmationUI
              key={part.toolCallId}
              part={part}
              onConfirm={(confirmed, reason) => {
                addToolOutput({
                  tool: 'confirmAction',
                  toolCallId: part.toolCallId,
                  output: { confirmed, reason },
                })
              }}
            />
          )
        }
        // ... other part types
      })}
    </div>
  )
}

// Confirmation component
function ConfirmationUI({ 
  part, 
  onConfirm 
}: { 
  part: ToolUIPart<'confirmAction'>
  onConfirm: (confirmed: boolean, reason?: string) => void 
}) {
  switch (part.state) {
    case 'input-streaming':
      return <div>Loading request...</div>
      
    case 'input-available':
      return (
        <div className="border p-4 rounded">
          <h3>Confirmation Required</h3>
          <p><strong>Action:</strong> {part.input.action}</p>
          <p>{part.input.details}</p>
          <div className="flex gap-2 mt-4">
            <button onClick={() => onConfirm(true)}>Confirm</button>
            <button onClick={() => onConfirm(false, 'User declined')}>Cancel</button>
          </div>
        </div>
      )
      
    case 'output-available':
      return (
        <div className={part.output.confirmed ? 'text-green-600' : 'text-red-600'}>
          {part.output.confirmed ? '✓ Confirmed' : '✗ Declined'}
          {part.output.reason && <span> - {part.output.reason}</span>}
        </div>
      )
      
    case 'output-error':
      return <div className="text-red-600">Error: {part.errorText}</div>
  }
}
```

## Tool States

Every tool part goes through these states:

```
input-streaming → input-available → output-available
                                  ↘ output-error
```

| State | Description | Available Properties |
|-------|-------------|---------------------|
| `input-streaming` | Receiving input | `toolCallId`, partial `input` |
| `input-available` | Input complete | `toolCallId`, `input` |
| `output-available` | Execution complete | `toolCallId`, `input`, `output` |
| `output-error` | Execution failed | `toolCallId`, `input`, `errorText` |

## Automatic Submission

Use `sendAutomaticallyWhen` to auto-submit after tool results:

```typescript
import { lastAssistantMessageIsCompleteWithToolCalls } from 'ai'

const { messages } = useChat({
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
  // ...
})
```

This triggers another model call when all tool results are available.

## Multi-Step Server Tools

Allow multiple tool calls with `stepCountIs`:

```typescript
import { stepCountIs } from 'ai'

const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: convertToModelMessages(messages),
  tools,
  stopWhen: stepCountIs(5), // Max 5 tool call rounds
})
```

## Generative UI Pattern

Render different components based on tool type:

```typescript
function MessageParts({ parts }: { parts: MyUIMessagePart[] }) {
  return (
    <>
      {parts.map((part, idx) => {
        switch (part.type) {
          case 'text':
            return <p key={idx}>{part.text}</p>
            
          case 'reasoning':
            return (
              <details key={idx} className="text-gray-500">
                <summary>Thinking...</summary>
                <pre>{part.text}</pre>
              </details>
            )
            
          case 'tool-getWeather':
            return <WeatherCard key={part.toolCallId} part={part} />
            
          case 'tool-confirmAction':
            return <ConfirmationUI key={part.toolCallId} part={part} />
            
          case 'data-proposal':
            return <ProposalCard key={part.id} data={part.data} />
            
          case 'step-start':
            return idx > 0 ? <hr key={idx} className="my-4" /> : null
            
          default:
            return null
        }
      })}
    </>
  )
}
```

## Error Handling

Handle tool execution errors:

```typescript
// Client-side error handling
async onToolCall({ toolCall }) {
  if (toolCall.toolName === 'riskyOperation') {
    try {
      const result = await performRiskyOperation(toolCall.input)
      addToolOutput({
        tool: 'riskyOperation',
        toolCallId: toolCall.toolCallId,
        output: result,
      })
    } catch (error) {
      addToolOutput({
        tool: 'riskyOperation',
        toolCallId: toolCall.toolCallId,
        state: 'output-error',
        errorText: error instanceof Error ? error.message : 'Unknown error',
      })
    }
  }
}

// Server-side error handling
return result.toUIMessageStreamResponse({
  onError: (error) => {
    if (error instanceof Error) return error.message
    return 'An error occurred'
  },
})
```

## Tools with Data Streaming

Combine tools with custom data parts for progressive UI:

```typescript
export const generateProposal = (writer: UIMessageStreamWriter<MyUIMessage>) =>
  tool({
    description: 'Generate an insurance proposal',
    inputSchema: z.object({
      coverage: z.string(),
      amount: z.number(),
    }),
    execute: async ({ coverage, amount }, { toolCallId }) => {
      // Initial loading state
      writer.write({
        type: 'data-proposal',
        id: toolCallId,
        data: { status: 'loading', content: null },
      })

      // Generate proposal
      const proposal = await generateProposalContent(coverage, amount)

      // Update with complete data (reconciliation by ID)
      writer.write({
        type: 'data-proposal',
        id: toolCallId,
        data: { status: 'complete', content: proposal },
      })

      return { success: true, proposalId: toolCallId }
    },
  })

// Usage in route
const stream = createUIMessageStream({
  execute: ({ writer }) => {
    const result = streamText({
      model: anthropic('claude-sonnet-4-20250514'),
      messages: convertToModelMessages(messages),
      tools: {
        generateProposal: generateProposal(writer),
      },
    })
    
    writer.merge(result.toUIMessageStream())
  },
})
```
