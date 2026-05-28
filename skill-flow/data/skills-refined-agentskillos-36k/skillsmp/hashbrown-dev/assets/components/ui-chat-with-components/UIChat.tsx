import { useUiChat, exposeComponent, RenderMessage } from '@hashbrownai/react'
import React, { useCallback, useState } from 'react'
import { s } from '@hashbrownai/core'
import { CustomCard } from './components/CustomCard'

// Expose your custom component to the AI
const ExposedCard = exposeComponent(CustomCard, {
  name: 'CustomCard',
  description: 'A card component to display information with a title and optional children.',
  props: {
    title: s.string('The title of the card'),
  },
  children: 'any',
})

export const UIChat: React.FC = () => {
  const [inputValue, setInputValue] = useState('')
  const { messages, sendMessage, isLoading, lastAssistantMessage } = useUiChat({
    model: 'gpt-4o-mini',
    system: `You are a helpful assistant that can use UI components to display information. When asked to show something in a card, use the CustomCard component.`,
    components: [ExposedCard],
  })

  const handleSubmit = useCallback(() => {
    if (inputValue.trim()) {
      sendMessage({ role: 'user', content: inputValue })
      setInputValue('')
    }
  }, [inputValue, sendMessage])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '500px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '16px',
      }}
    >
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '16px' }}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{ marginBottom: '8px', textAlign: msg.role === 'user' ? 'right' : 'left' }}
          >
            {msg.role === 'user' && (
              <div
                style={{
                  display: 'inline-block',
                  padding: '8px 12px',
                  borderRadius: '12px',
                  backgroundColor: '#007bff',
                  color: 'white',
                }}
              >
                {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
              </div>
            )}
          </div>
        ))}
        {lastAssistantMessage && <RenderMessage message={lastAssistantMessage} />}
      </div>
      <div style={{ display: 'flex', gap: '8px' }}>
        <textarea
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '8px',
            borderRadius: '8px',
            border: '1px solid #ccc',
            resize: 'none',
          }}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: '#007bff',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          {isLoading ? 'Generating...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
