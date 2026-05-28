---
title: Use useTransition Over Manual Loading States
impact: LOW
impactDescription: reduces re-renders and improves code clarity
tags: rendering, usetransition, loading-states, react19
---

## Use useTransition Over Manual Loading States

Use `useTransition` instead of manual `useState` for loading states. This provides built-in `isPending` state and automatically manages transitions.

**Incorrect (manual loading state):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  
  const handleSearch = async (q: string) => {
    setIsLoading(true)
    setQuery(q)
    const data = await fetchResults(q)
    setResults(data)
    setIsLoading(false)
  }
  
  return (
    <div>
      <SearchInput onSearch={handleSearch} />
      {isLoading ? <Spinner /> : <ResultsList results={results} />}
    </div>
  )
}
```

**Correct (useTransition with built-in pending state):**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()
  
  const handleSearch = async (q: string) => {
    setQuery(q)
    startTransition(async () => {
      const data = await fetchResults(q)
      setResults(data)
    })
  }
  
  return (
    <div>
      <SearchInput onSearch={handleSearch} />
      {isPending ? <Spinner /> : <ResultsList results={results} />}
    </div>
  )
}
```

**Benefits:**

- **Automatic pending state**: No need to manually manage `setIsLoading(true/false)`
- **Error resilience**: Pending state correctly resets even if the transition throws
- **Better responsiveness**: Keeps the UI responsive during updates
- **Interrupt handling**: New transitions automatically cancel pending ones

Reference: [React useTransition](https://react.dev/reference/react/useTransition)
