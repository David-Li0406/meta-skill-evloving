import { useChat } from '@hashbrownai/react'
import React, { useCallback, useState } from 'react'

export const SimpleChat: React.FC = () => {
  const [inputValue, setInputValue] = useState('')
  const { messages, sendMessage, isLoading } = useChat({
    model: 'gpt-4o-mini',
    system: 'You are a helpful assistant.',
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
        height: '400px',
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
            <div
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '12px',
                backgroundColor: msg.role === 'user' ? '#007bff' : '#f1f1f1',
                color: msg.role === 'user' ? 'white' : 'black',
              }}
            >
              {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
            </div>
          </div>
        ))}
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
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
