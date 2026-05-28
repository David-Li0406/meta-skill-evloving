/**
 * Chat client component
 * 
 * Features:
 * - Send only last message
 * - Human-in-the-loop tool handling
 * - Auto-submit after tool results
 * - Client-side tool execution
 * - Generative UI rendering
 */
'use client'

import { useChat } from '@ai-sdk/react'
import {
  DefaultChatTransport,
  lastAssistantMessageIsCompleteWithToolCalls,
} from 'ai'
import { useState, useRef, useEffect } from 'react'
import type { MyUIMessage } from '../types/message'
import { deleteAgent, deleteMessage } from '../db/actions'
import { useRouter } from 'next/navigation'

// Import generative UI components
import { ConfirmationCard } from './generative-ui/confirmation-card'
import { ProposalCard } from './generative-ui/proposal-card'
import { WeatherCard } from './generative-ui/weather-card'

interface ChatProps {
  agentId: string
  initialMessages: MyUIMessage[]
}

export function Chat({ agentId, initialMessages }: ChatProps) {
  const router = useRouter()
  const inputRef = useRef<HTMLInputElement>(null)
  const [input, setInput] = useState('')
  const [statusMessage, setStatusMessage] = useState<string | null>(null)

  const {
    messages,
    setMessages,
    sendMessage,
    addToolOutput,
    status,
    error,
    stop,
    reload,
  } = useChat<MyUIMessage>({
    id: agentId,
    messages: initialMessages,
    
    transport: new DefaultChatTransport({
      api: '/api/agent',
      // Send only the last message (server loads history)
      prepareSendMessagesRequest: ({ messages, id }) => ({
        body: {
          message: messages.at(-1),
          agentId: id,
        },
      }),
    }),

    // Auto-submit when all tool results are available
    sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,

    // Handle client-side tools
    async onToolCall({ toolCall }) {
      // Skip dynamic tools
      if (toolCall.dynamic) return

      // Client-side tool: getUserLocation
      if (toolCall.toolName === 'getUserLocation') {
        try {
          const position = await new Promise<GeolocationPosition>(
            (resolve, reject) => {
              navigator.geolocation.getCurrentPosition(resolve, reject)
            }
          )

          // No await - prevents deadlocks
          addToolOutput({
            tool: 'getUserLocation',
            toolCallId: toolCall.toolCallId,
            output: {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              city: 'Current Location', // Would normally reverse geocode
            },
          })
        } catch (err) {
          addToolOutput({
            tool: 'getUserLocation',
            toolCallId: toolCall.toolCallId,
            state: 'output-error',
            errorText: 'Could not get location',
          })
        }
      }
    },

    // Handle transient data parts
    onData: (dataPart) => {
      if (dataPart.type === 'data-status') {
        setStatusMessage(dataPart.data.message)
      }
    },

    onFinish: ({ message }) => {
      setStatusMessage(null)
      console.log('Message completed:', message.metadata?.totalTokens, 'tokens')
    },

    onError: (error) => {
      setStatusMessage(null)
      console.error('Chat error:', error)
    },
  })

  // Focus input when ready
  useEffect(() => {
    if (status === 'ready') {
      inputRef.current?.focus()
    }
  }, [status])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && status === 'ready') {
      sendMessage({ text: input })
      setInput('')
    }
  }

  const handleDeleteAgent = async () => {
    if (confirm('Delete this conversation?')) {
      await deleteAgent(agentId)
      router.push('/')
    }
  }

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 pb-4 border-b">
        <h1 className="text-xl font-semibold">Agent Chat</h1>
        <button
          onClick={handleDeleteAgent}
          className="text-red-600 hover:text-red-800 text-sm"
        >
          Delete
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[80%] ${
                message.role === 'user'
                  ? 'bg-blue-100 rounded-l-lg rounded-tr-lg'
                  : 'bg-gray-100 rounded-r-lg rounded-tl-lg'
              } p-4`}
            >
              {/* Render message parts */}
              <MessageParts
                parts={message.parts}
                addToolOutput={addToolOutput}
              />

              {/* Message metadata */}
              {message.metadata?.totalTokens && (
                <div className="text-xs text-gray-400 mt-2">
                  {message.metadata.totalTokens} tokens
                </div>
              )}

              {/* Delete button for user messages */}
              {message.role === 'user' && (
                <button
                  onClick={async () => {
                    if (confirm('Delete this message and all following?')) {
                      await deleteMessage(message.id)
                      const idx = messages.findIndex((m) => m.id === message.id)
                      setMessages(messages.slice(0, idx))
                    }
                  }}
                  className="text-xs text-red-500 mt-2 hover:underline"
                  disabled={status !== 'ready'}
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}

        {/* Status indicator */}
        {statusMessage && (
          <div className="text-center text-gray-500 text-sm animate-pulse">
            {statusMessage}
          </div>
        )}

        {/* Loading indicator */}
        {status === 'submitted' && (
          <div className="text-center text-gray-500">
            <span className="animate-pulse">Thinking...</span>
          </div>
        )}
      </div>

      {/* Error display */}
      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
          {error.message}
          <button onClick={() => reload()} className="ml-2 underline">
            Retry
          </button>
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={status !== 'ready'}
          className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {status === 'streaming' || status === 'submitted' ? (
          <button
            type="button"
            onClick={() => stop()}
            className="px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Stop
          </button>
        ) : (
          <button
            type="submit"
            disabled={!input.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
          >
            Send
          </button>
        )}
      </form>
    </div>
  )
}

/**
 * Render message parts with generative UI
 */
function MessageParts({
  parts,
  addToolOutput,
}: {
  parts: MyUIMessage['parts']
  addToolOutput: ReturnType<typeof useChat<MyUIMessage>>['addToolOutput']
}) {
  return (
    <div className="space-y-3">
      {parts.map((part, idx) => {
        switch (part.type) {
          case 'text':
            return (
              <p key={idx} className="whitespace-pre-wrap">
                {part.text}
              </p>
            )

          case 'reasoning':
            return (
              <details key={idx} className="text-gray-500 text-sm">
                <summary className="cursor-pointer hover:text-gray-700">
                  View reasoning
                </summary>
                <pre className="mt-2 p-2 bg-gray-50 rounded text-xs overflow-x-auto">
                  {part.text}
                </pre>
              </details>
            )

          case 'tool-confirmAction':
            return (
              <ConfirmationCard
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

          case 'tool-generateProposal':
            return (
              <div
                key={part.toolCallId}
                className="bg-blue-50 p-3 rounded border"
              >
                {part.state === 'input-available' && (
                  <div className="animate-pulse">
                    Generating proposal for {part.input.coverage}...
                  </div>
                )}
                {part.state === 'output-available' && (
                  <div className="text-green-600">
                    ✓ {part.output.summary}
                  </div>
                )}
                {part.state === 'output-error' && (
                  <div className="text-red-600">Error: {part.errorText}</div>
                )}
              </div>
            )

          case 'tool-getWeatherInfo':
            return <WeatherCard key={part.toolCallId} part={part} />

          case 'tool-getUserLocation':
            return (
              <div key={part.toolCallId} className="text-sm text-gray-600">
                {part.state === 'input-available' && 'Getting location...'}
                {part.state === 'output-available' && (
                  <span>📍 {part.output.city}</span>
                )}
                {part.state === 'output-error' && (
                  <span className="text-red-600">{part.errorText}</span>
                )}
              </div>
            )

          case 'data-proposal':
            return <ProposalCard key={part.id} data={part.data} />

          case 'step-start':
            return idx > 0 ? (
              <hr key={idx} className="my-2 border-gray-200" />
            ) : null

          case 'source-url':
            return (
              <a
                key={idx}
                href={part.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline text-sm block"
              >
                📎 {part.title || part.url}
              </a>
            )

          default:
            return null
        }
      })}
    </div>
  )
}
