# Forms Reference

## Contents
- Form Component Structure
- Input Handling
- Submission Pattern
- UI Feedback
- Validation
- WARNING: Code Duplication

## Form Component Structure

```tsx
'use client'

import { useState } from 'react'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // ... submission logic
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  )
}
```

## Input Handling

### Text Input

```tsx
<input
  type="text"
  name="firstName"
  value={formData.firstName}
  onChange={handleChange}
  required
  className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
/>
```

### Textarea

```tsx
<textarea
  name="message"
  value={formData.message}
  onChange={handleChange}
  rows={5}
  required
  className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500 resize-none"
/>
```

### Select Dropdown

```tsx
<select
  name="role"
  value={formData.role}
  onChange={handleChange}
  required
  className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg"
>
  <option value="">Select your role</option>
  <option value="owner">Owner/Principal</option>
  <option value="technical">Technical Manager</option>
  <option value="service">Service Manager</option>
</select>
```

## Submission Pattern

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsSubmitting(true)
  setError('')

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong')
    }

    setIsSubmitted(true)
    setFormData({ firstName: '', lastName: '', email: '', message: '' })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong.')
  } finally {
    setIsSubmitting(false)
  }
}
```

## UI Feedback

### Submit Button with Loading

```tsx
<button
  type="submit"
  disabled={isSubmitting}
  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-full font-semibold flex items-center justify-center gap-2"
>
  {isSubmitting ? (
    <>
      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
      Sending...
    </>
  ) : (
    'Send Message'
  )}
</button>
```

### Error Message

```tsx
{error && (
  <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-300">
    {error}
  </div>
)}
```

### Success Message

```tsx
{isSubmitted && (
  <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4 text-green-300">
    Thank you! We'll get back to you within 24 hours.
  </div>
)}
```

## Validation

### Client-Side (Basic)

HTML5 validation via `required` attribute.

### Server-Side (API Route)

```tsx
// Validate required fields
if (!firstName || !lastName || !email || !message) {
  return NextResponse.json(
    { error: 'All fields are required' },
    { status: 400 }
  )
}

// Validate email format
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(email)) {
  return NextResponse.json(
    { error: 'Invalid email format' },
    { status: 400 }
  )
}
```

## WARNING: Form Code Duplication

**The Problem:**

Contact, e-book, and webinar forms all have identical:
- handleChange function
- handleSubmit structure
- State management trio

**Why This Breaks:**
1. Bug fixes must be applied 3 times
2. Inconsistent behavior (e-book doesn't reset form)
3. Violates DRY principle

**The Fix (Custom Hook):**

```tsx
// hooks/useFormSubmit.ts
import { useState } from 'react'

export function useFormSubmit<T>(endpoint: string, initialData: T) {
  const [formData, setFormData] = useState<T>(initialData)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Something went wrong')

      setIsSubmitted(true)
      setFormData(initialData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return { formData, handleChange, handleSubmit, isSubmitting, isSubmitted, error }
}

// Usage
const { formData, handleChange, handleSubmit, isSubmitting, isSubmitted, error } = 
  useFormSubmit('/api/contact', { firstName: '', lastName: '', email: '', message: '' })