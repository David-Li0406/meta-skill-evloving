import React from 'react'
import { useChat } from '@hashbrown/react'
import { useThreads } from './hooks/useThreads'

export const MultiThreadedChatUI: React.FC = () => {
  const { threads, activeThread, createThread, switchThread } = useThreads()
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: `/api/threads/${activeThread?.id}/chat`,
    initialMessages: activeThread?.messages,
  })

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ borderRight: '1px solid #ccc', padding: '10px' }}>
        <h2>Threads</h2>
        <button onClick={createThread}>New Thread</button>
        <ul>
          {threads.map(thread => (
            <li key={thread.id} onClick={() => switchThread(thread.id)}>
              {thread.title}
            </li>
          ))}
        </ul>
      </div>
      <div style={{ flex: 1, padding: '10px' }}>
        {activeThread && (
          <>
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
          </>
        )}
      </div>
    </div>
  )
}
