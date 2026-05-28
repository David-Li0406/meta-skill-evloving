import React, { useState } from 'react'
import { useChat } from '@hashbrown/react'

export const StreamingChatUI: React.FC = () => {
  const { messages, input, handleInputChange, handleSubmit } = useChat()

  return (
    <div>
      <div>
        {messages.map((m, index) => (
          <div key={index}>
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} placeholder="Say something..." />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
