---
name: react
description: |
  Manages React hooks, components, state management, and interactive features.
  Use when: Building client components, handling forms, managing UI state, creating interactive elements
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# React Skill

This codebase uses React 19 with Next.js 15 App Router. All interactive pages use the `'use client'` directive. State is managed locally with `useState` - no global state library. Forms submit to API routes via fetch.

## Quick Start

### Client Component Pattern

```tsx
'use client'

import { useState, useEffect } from 'react'
import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'

export default function PageName() {
  const [mounted, setMounted] = useState(false)
  
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      {/* Page content */}
      <Footer />
    </div>
  )
}
```

### Form State Pattern

```tsx
const [formData, setFormData] = useState({
  firstName: '',
  lastName: '',
  email: ''
})

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData(prev => ({
    ...prev,
    [e.target.name]: e.target.value
  }))
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Client directive | All interactive pages | `'use client'` at top |
| Mounted check | Prevent hydration errors | `if (!mounted) return null` |
| Object state | Group related form fields | `useState({ field1: '', field2: '' })` |
| Functional updates | Immutable state changes | `setState(prev => ({ ...prev, key: val }))` |
| Array toggle | Multi-select accordion | `prev.includes(i) ? prev.filter(...) : [...prev, i]` |

## Common Patterns

### Accordion Toggle

```tsx
const [expandedItems, setExpandedItems] = useState<number[]>([])

const toggleItem = (index: number) => {
  setExpandedItems(prev => 
    prev.includes(index) 
      ? prev.filter(i => i !== index)
      : [...prev, index]
  )
}
```

### Tab Selection

```tsx
const [activeTab, setActiveTab] = useState('overview')

<button onClick={() => setActiveTab('overview')} 
  className={activeTab === 'overview' ? 'bg-purple-600' : 'bg-gray-800'}>
  Overview
</button>

{activeTab === 'overview' && <OverviewContent />}
```

## See Also

- [hooks](references/hooks.md)
- [components](references/components.md)
- [data-fetching](references/data-fetching.md)
- [state](references/state.md)
- [forms](references/forms.md)
- [performance](references/performance.md)

## Related Skills

- See the **nextjs** skill for App Router patterns and API routes
- See the **typescript** skill for type annotations and interfaces
- See the **tailwind** skill for styling conventions

## Documentation Resources

> Fetch latest React documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "react"
2. Prefer website documentation (IDs starting with `/websites/`) over source code
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/react_dev` (High reputation, 2238 snippets, score 89.9)

**Recommended Queries:**
- "React hooks useState useEffect useCallback useMemo"
- "React event handling onChange onSubmit"
- "React conditional rendering patterns"