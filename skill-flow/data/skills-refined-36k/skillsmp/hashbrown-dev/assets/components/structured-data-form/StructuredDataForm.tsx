import { useStructuredCompletion } from '@hashbrownai/react'
import React, { useCallback, useState } from 'react'
import { userProfileSchema } from './schema'

export const StructuredDataForm: React.FC = () => {
  const [inputValue, setInputValue] = useState(
    'My name is Jane Doe and my email is jane@example.com.'
  )
  const [submittedValue, setSubmittedValue] = useState<string | null>(null)

  const { output, isLoading, error } = useStructuredCompletion({
    model: 'gpt-4o-mini',
    system:
      'You are an assistant that extracts user profile information from a single string of text and returns it as a structured JSON object.',
    input: submittedValue,
    schema: userProfileSchema,
  })

  const handleSubmit = useCallback(() => {
    setSubmittedValue(inputValue)
  }, [inputValue])

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
      <h2 style={{ marginTop: 0 }}>User Profile Form</h2>
      <p>
        Describe your profile in a single sentence. The AI will parse it into a structured format.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <textarea
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder="e.g., My name is John Doe, I am 30 years old, and my email is john.doe@example.com"
          rows={3}
          style={{
            width: '100%',
            padding: '8px',
            borderRadius: '8px',
            border: '1px solid #ccc',
            resize: 'vertical',
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
          {isLoading ? 'Parsing...' : 'Parse Data'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginTop: '16px' }}>
          <strong>Error:</strong> {error.message}
        </div>
      )}

      {output && (
        <div style={{ marginTop: '16px' }}>
          <h3>Parsed Profile Data:</h3>
          <pre
            style={{
              backgroundColor: '#f1f1f1',
              padding: '16px',
              borderRadius: '8px',
              whiteSpace: 'pre-wrap',
            }}
          >
            {JSON.stringify(output, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
