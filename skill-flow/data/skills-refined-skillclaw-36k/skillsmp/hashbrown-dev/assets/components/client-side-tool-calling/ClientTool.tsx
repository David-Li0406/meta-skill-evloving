import { useChat, useTool } from '@hashbrownai/react'
import React, { useCallback, useState } from 'react'
import { s } from '@hashbrownai/core'

// A simple in-component state to demonstrate the tool's effect
const todoItems = [
  { id: 1, text: 'Buy milk', done: false },
  { id: 2, text: 'Walk the dog', done: true },
]

export const ClientTool: React.FC = () => {
  const [inputValue, setInputValue] = useState('Mark "Buy milk" as done')
  const [, setForceUpdate] = useState({}) // To re-render on state change

  // Define a client-side tool to interact with the todoItems array
  const todoTool = useTool({
    name: 'updateTodoStatus',
    description: 'Updates the status of a todo item.',
    schema: s.object('Todo Update', {
      id: s.number('The ID of the todo item'),
      done: s.boolean('The new completion status'),
    }),
    handler: async args => {
      const item = todoItems.find(item => item.id === args.id)
      if (item) {
        item.done = args.done
        setForceUpdate({}) // Force a re-render to show the change
        return { success: true }
      }
      return { success: false, error: 'Item not found' }
    },
    deps: [],
  })

  const { messages, sendMessage, isLoading } = useChat({
    model: 'gpt-4o-mini',
    system:
      'You are a helpful assistant that manages a todo list. Use the `updateTodoStatus` tool to change the status of items. Inform the user when the action is complete.',
    tools: [todoTool],
  })

  const handleSubmit = useCallback(() => {
    if (inputValue.trim()) {
      sendMessage({ role: 'user', content: inputValue })
      setInputValue('')
    }
  }, [inputValue, sendMessage])

  return (
    <div
      style={{
        maxWidth: '600px',
        margin: 'auto',
        padding: '16px',
        border: '1px solid #ccc',
        borderRadius: '8px',
      }}
    >
      <h2>Todo List</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todoItems.map(item => (
          <li key={item.id} style={{ textDecoration: item.done ? 'line-through' : 'none' }}>
            {item.text} (ID: {item.id})
          </li>
        ))}
      </ul>

      <h3 style={{ marginTop: '24px' }}>Chat with AI to manage todos</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '8px' }}>
        <textarea
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder="e.g., Mark item 1 as complete"
          rows={2}
          style={{ width: '100%', padding: '8px', borderRadius: '8px', border: '1px solid #ccc' }}
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
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </div>

      <div style={{ marginTop: '16px' }}>
        {messages
          .filter(m => m.role === 'assistant' && m.content)
          .map((msg, index) => (
            <div
              key={index}
              style={{
                marginBottom: '8px',
                backgroundColor: '#f1f1f1',
                padding: '8px 12px',
                borderRadius: '12px',
              }}
            >
              {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
            </div>
          ))}
      </div>
    </div>
  )
}
