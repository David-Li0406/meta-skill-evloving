# TypeScript Types Reference

## Contents
- Utility Types
- Generic Patterns
- Conditional Types
- Type Guards and Narrowing
- This Codebase's Type Conventions

## Utility Types

### Partial<T> - Make All Properties Optional

```typescript
interface Todo {
  title: string
  description: string
  completed: boolean
}

// All properties optional - useful for update functions
function updateTodo(todo: Todo, fieldsToUpdate: Partial<Todo>) {
  return { ...todo, ...fieldsToUpdate }
}

updateTodo(existingTodo, { description: 'New description' })
```

### Pick<T, K> - Select Specific Properties

```typescript
interface Todo {
  title: string
  description: string
  completed: boolean
  createdAt: number
}

// Only title and completed
type TodoPreview = Pick<Todo, 'title' | 'completed'>

const preview: TodoPreview = {
  title: 'Clean room',
  completed: false,
}
```

### Omit<T, K> - Remove Specific Properties

```typescript
interface Todo {
  title: string
  description: string
  completed: boolean
  createdAt: number
}

// Everything except description
type TodoPreview = Omit<Todo, 'description'>

const todo: TodoPreview = {
  title: 'Clean room',
  completed: false,
  createdAt: 1615544252770,
}
```

### Record<K, V> - Object with Typed Keys

```typescript
type Colors = 'red' | 'green' | 'blue'
type RGB = [number, number, number]

const palette: Record<Colors, string | RGB> = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
}
```

### Readonly<T> - Immutable Properties

```typescript
interface Config {
  apiUrl: string
  timeout: number
}

const config: Readonly<Config> = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
}

config.timeout = 10000 // Error: Cannot assign to 'timeout'
```

## Type Guards and Narrowing

### Discriminated Unions

```typescript
interface Square {
  kind: 'square'
  size: number
}

interface Circle {
  kind: 'circle'
  radius: number
}

type Shape = Square | Circle

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'square':
      return shape.size * shape.size // TypeScript knows it's Square
    case 'circle':
      return Math.PI * shape.radius ** 2 // TypeScript knows it's Circle
  }
}
```

### Exhaustiveness Checking with `never`

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`)
}

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'square':
      return shape.size ** 2
    case 'circle':
      return Math.PI * shape.radius ** 2
    default:
      return assertNever(shape) // Error if new shape added
  }
}
```

### `typeof` Guards

```typescript
function processValue(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase() // TypeScript knows it's string
  }
  return value.toFixed(2) // TypeScript knows it's number
}
```

### `instanceof` Guards

```typescript
function handleError(error: unknown) {
  if (error instanceof Error) {
    console.error(error.message) // TypeScript knows it's Error
  } else {
    console.error(String(error))
  }
}
```

## This Codebase's Type Conventions

### Form State Types

```typescript
// Pattern from app/contact/page.tsx
interface ContactFormData {
  firstName: string
  lastName: string
  companyName: string
  email: string
  message: string
}

const [formData, setFormData] = useState<ContactFormData>({
  firstName: '',
  lastName: '',
  companyName: '',
  email: '',
  message: ''
})
```

### Global Type Augmentation

```typescript
// Pattern from app/page.tsx - extend Window for third-party scripts
declare global {
  interface Window {
    Calendly: {
      initPopupWidget: (options: { url: string }) => void
      initInlineWidget: (options: { url: string; parentElement: Element | null }) => void
    }
  }
}
```

### Navigation Data Types (Inferred)

```typescript
// TypeScript infers the array type from the data
const solutions = [
  { name: 'Engineer Efficiency', href: '/solutions/engineer-efficiency', icon: '⚡' },
  { name: 'Service Desk Management', href: '/solutions/service-desk-management', icon: '📊' },
]
// Inferred: { name: string; href: string; icon: string }[]
```

### Next.js Metadata Type

```typescript
// Pattern from app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'XOP.ai - AI Solutions Designed by MSPs, For MSPs',
  description: '28 years of MSP experience + cutting-edge Rezolve.ai technology',
}