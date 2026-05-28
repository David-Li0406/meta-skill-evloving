import { useCompletion } from '@hashbrownai/react'
import React, { useCallback, useState } from 'react'

export const PredictiveTextInput: React.FC = () => {
  const [inputValue, setInputValue] = useState('')

  const { output, isLoading, exhaustedRetries } = useCompletion({
    model: 'gpt-4o-mini',
    input: inputValue,
    system:
      "You are an autocomplete assistant. Given the user's input, predict the next few words they are likely to type. Return only the suggested text to append. Do not include the original input. Keep suggestions short.",
    debounce: 300, // Debounce requests to avoid excessive API calls
    retries: 2,
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab' && output) {
      e.preventDefault()
      setInputValue(inputValue + output)
    }
  }

  return (
    <div
      style={{
        maxWidth: '500px',
        margin: 'auto',
        padding: '16px',
        border: '1px solid #ccc',
        borderRadius: '8px',
      }}
    >
      <h2 style={{ marginTop: 0 }}>Predictive Text Input</h2>
      <p>Start typing, and the AI will suggest the next few words. Press Tab to accept.</p>
      <div style={{ position: 'relative' }}>
        <textarea
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Start writing..."
          rows={5}
          style={{
            width: '100%',
            padding: '8px',
            borderRadius: '8px',
            border: '1px solid #ccc',
            resize: 'vertical',
            position: 'relative',
            backgroundColor: 'transparent',
            zIndex: 2,
          }}
        />
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            padding: '8px',
            color: 'gray',
            whiteSpace: 'pre-wrap',
            zIndex: 1,
            pointerEvents: 'none',
          }}
        >
          <span style={{ visibility: 'hidden' }}>{inputValue}</span>
          <span>{isLoading ? '...' : output}</span>
        </div>
      </div>
      {exhaustedRetries && (
        <p style={{ color: 'red', fontSize: '12px', marginTop: '8px' }}>
          Autocomplete service is currently unavailable.
        </p>
      )}
    </div>
  )
}
