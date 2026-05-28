---
name: typescript
description: |
  Enforces TypeScript type safety and strict mode configuration
  Use when: Writing type definitions, configuring tsconfig.json, fixing type errors, improving type safety
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# TypeScript Skill

This codebase uses TypeScript 5.x with strict mode enabled. The `tsconfig.json` has `"strict": true` configured, which enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and related checks. All React components use TypeScript with explicit typing for props, state, and event handlers.

## Quick Start

### Client Component with Typed State

```tsx
'use client'

import { useState } from 'react'

// Form state interface
interface FormData {
  firstName: string
  lastName: string
  email: string
}

export default function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    email: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }
}
```

### API Route with Request Validation

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const body = await request.json()
  const { firstName, lastName, email } = body

  if (!firstName || !lastName || !email) {
    return NextResponse.json(
      { error: 'All fields are required' },
      { status: 400 }
    )
  }

  return NextResponse.json({ success: true }, { status: 200 })
}
```

### Global Type Augmentation

```typescript
// Extend Window interface for third-party libraries
declare global {
  interface Window {
    Calendly: {
      initPopupWidget: (options: { url: string }) => void
      initInlineWidget: (options: { url: string; parentElement: Element | null }) => void
    }
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Strict mode | Enabled globally in tsconfig.json | `"strict": true` |
| Path aliases | Import from project root | `@/app/components/...` |
| React types | Event handlers and refs | `React.ChangeEvent<HTMLInputElement>` |
| Union types | Discriminated unions for state | `string \| null` |
| Utility types | Transform existing types | `Partial<T>`, `Pick<T, K>`, `Omit<T, K>` |

## Common Patterns

### Typed Navigation Data

```typescript
const solutions = [
  { name: 'Engineer Efficiency', href: '/solutions/engineer-efficiency', icon: '⚡' },
  { name: 'Service Desk Management', href: '/solutions/service-desk-management', icon: '📊' },
]
// TypeScript infers: { name: string; href: string; icon: string }[]
```

### Optional Chaining for Nullable Data

```typescript
// Safe property access
console.log('Email sent:', data?.id)
```

## See Also

- [patterns](references/patterns.md)
- [types](references/types.md)
- [modules](references/modules.md)
- [errors](references/errors.md)

## Related Skills

For React component patterns and hooks, see the **react** skill.
For Next.js App Router and API routes, see the **nextjs** skill.

## Documentation Resources

> Fetch latest TypeScript documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "typescript"
2. **Prefer website documentation** (`/websites/typescriptlang`) over source code repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/typescriptlang` _(High reputation, benchmark score 91.3)_

**Recommended Queries:**
- "Utility types Partial Pick Omit Record"
- "Strict mode configuration tsconfig"
- "Type narrowing discriminated unions"
- "as const satisfies operator"