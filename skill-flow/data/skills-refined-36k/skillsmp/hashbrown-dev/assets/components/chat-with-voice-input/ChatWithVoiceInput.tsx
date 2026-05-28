import React from 'react'
import { useChat } from '@hashbrown/react'

export const ChatWithVoiceInput: React.FC = () => {
  const { messages, input, setInput, handleInputChange, handleSubmit } = useChat()

  const handleVoiceInput = () => {
    const recognition = new (window as any).webkitSpeechRecognition()
    recognition.onresult = (event: any) => {
      setInput(event.results[0][0].transcript)
    }
    recognition.start()
  }

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
        <button type="button" onClick={handleVoiceInput}>
          🎤
        </button>
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
