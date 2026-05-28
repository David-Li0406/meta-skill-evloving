# TypeScript Patterns Reference

## Contents
- Idiomatic Type Patterns
- Type Inference Best Practices
- Error Handling Conventions
- React-Specific Patterns
- Anti-Patterns to Avoid

## Idiomatic Type Patterns

### Use `as const` for Literal Arrays

When defining static configuration data, use `as const` to preserve literal types:

```typescript
// GOOD - preserves literal types
const solutions = [
  { name: 'Engineer Efficiency', href: '/solutions/engineer-efficiency', icon: '⚡' },
  { name: 'Service Desk Management', href: '/solutions/service-desk-management', icon: '📊' },
] as const

// TypeScript knows exact string values, enables autocomplete
type SolutionName = typeof solutions[number]['name']
// = 'Engineer Efficiency' | 'Service Desk Management'
```

```typescript
// BAD - types widen to string
const solutions = [
  { name: 'Engineer Efficiency', href: '/solutions/engineer-efficiency' },
]
// TypeScript only knows: { name: string; href: string }[]
```

### Use `satisfies` for Type-Safe Configuration

```typescript
// GOOD - validates type AND preserves inference
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
} satisfies Record<string, string | [number, number, number]>

palette.green.toUpperCase() // Works - TypeScript knows it's string
```

```typescript
// BAD - loses specific type info
const palette: Record<string, string | [number, number, number]> = {
  red: [255, 0, 0],
  green: "#00ff00",
}

palette.green.toUpperCase() // Error - might be array
```

## Type Inference Best Practices

### Let TypeScript Infer When Obvious

```typescript
// GOOD - inference is clear
const [isSubmitting, setIsSubmitting] = useState(false)
const [error, setError] = useState('')

// GOOD - explicit when inference fails
const [formData, setFormData] = useState<FormData>({
  firstName: '',
  lastName: '',
  email: ''
})
```

```typescript
// BAD - redundant type annotation
const [isSubmitting, setIsSubmitting] = useState<boolean>(false)
const count: number = 5
```

### Discriminated Unions for State

```typescript
// GOOD - exhaustive state handling
type RequestState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: string }
  | { status: 'error'; error: Error }

function handleState(state: RequestState) {
  switch (state.status) {
    case 'idle': return null
    case 'loading': return <Spinner />
    case 'success': return <div>{state.data}</div>
    case 'error': return <div>{state.error.message}</div>
  }
}
```

## Error Handling Conventions

### Type-Safe Error Handling

```typescript
// Pattern from app/contact/page.tsx
try {
  const response = await fetch('/api/contact', {
    method: 'POST',
    body: JSON.stringify(formData),
  })
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.error || 'Something went wrong')
  }
} catch (err) {
  // GOOD - narrow unknown to Error
  setError(err instanceof Error ? err.message : 'Something went wrong')
}
```

### WARNING: Never Use `any` for Caught Errors

```typescript
// BAD - any type disables all checking
} catch (err: any) {
  setError(err.message) // Runtime error if err isn't an Error
}

// GOOD - handle unknown properly
} catch (err: unknown) {
  setError(err instanceof Error ? err.message : String(err))
}
```

## React-Specific Patterns

### Event Handler Types

```typescript
// Pattern from this codebase
const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value
  })
}

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  // ...
}

// onClick with event target comparison
onClick={(e) => {
  if (e.target === e.currentTarget) {
    setModalOpen(false)
  }
}}
```

### Children Prop Typing

```typescript
// Pattern from app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## Anti-Patterns to Avoid

### WARNING: Avoid Type Assertions When Narrowing Works

**The Problem:**

```typescript
// BAD - type assertion bypasses safety
const data = response.json() as UserData
```

**Why This Breaks:**
1. No runtime validation - API could return anything
2. Silent failures when data shape changes
3. Type assertion tells TS "trust me" - it won't catch mismatches

**The Fix:**

```typescript
// GOOD - validate at runtime
const data = await response.json()
if (!isValidUserData(data)) {
  throw new Error('Invalid response shape')
}
// data is now narrowed to UserData
```

### WARNING: Don't Use Index Signatures When Keys Are Known

**The Problem:**

```typescript
// BAD - loses type safety
interface Config {
  [key: string]: string
}
```

**The Fix:**

```typescript
// GOOD - explicit keys
interface Config {
  apiUrl: string
  apiKey: string
}

// Or use Record with union
type Config = Record<'apiUrl' | 'apiKey', string>