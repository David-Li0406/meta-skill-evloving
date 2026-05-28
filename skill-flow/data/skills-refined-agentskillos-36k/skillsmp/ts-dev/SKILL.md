---
name: ts-dev
description: |
  TypeScript patterns: type definitions, interfaces, generics, type guards, and utility types.
  WHEN: Writing .ts/.tsx files, defining interfaces/types, using generics, implementing type guards, configuring tsconfig.json, Vue script lang="ts".
  WHEN NOT: Plain JavaScript (use js-dev), runtime code without types, Python/PHP backend code.
---

# TypeScript Development

TypeScript patterns, types, and best practices.

## Basic Types

```typescript
// Primitives
const name: string = 'John'
const age: number = 30
const active: boolean = true

// Arrays
const items: string[] = ['a', 'b']
const numbers: Array<number> = [1, 2, 3]

// Tuple
const pair: [string, number] = ['age', 30]

// Any & Unknown
let data: any        // Avoid: bypasses type checking
let input: unknown   // Prefer: requires type check before use

// Void & Never
function log(msg: string): void { console.log(msg) }
function fail(msg: string): never { throw new Error(msg) }
```

## Interfaces vs Types

```typescript
// Interface: extendable, for object shapes
interface User {
  id: number
  name: string
  email?: string           // optional
  readonly createdAt: Date // immutable
}

interface Admin extends User {
  permissions: string[]
}

// Type: unions, intersections, primitives
type ID = string | number
type Status = 'pending' | 'active' | 'inactive'
type UserWithMeta = User & { meta: Record<string, unknown> }

// Prefer interface for objects, type for unions/complex types
```

## Functions

```typescript
// Function types
function greet(name: string): string {
  return `Hello, ${name}`
}

// Arrow function
const add = (a: number, b: number): number => a + b

// Optional & default parameters
function fetch(url: string, options?: RequestInit): Promise<Response>
function log(message: string, level = 'info'): void

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0)
}

// Function type alias
type Handler = (event: Event) => void
type AsyncFn<T> = () => Promise<T>
```

## Generics

```typescript
// Generic function
function first<T>(items: T[]): T | undefined {
  return items[0]
}

// Generic interface
interface Response<T> {
  data: T
  status: number
  message: string
}

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

// Default generic type
interface Container<T = string> {
  value: T
}
```

## Utility Types

```typescript
interface User {
  id: number
  name: string
  email: string
  password: string
}

// Partial: all properties optional
type UpdateUser = Partial<User>

// Required: all properties required
type CompleteUser = Required<User>

// Pick: select specific properties
type UserPreview = Pick<User, 'id' | 'name'>

// Omit: exclude properties
type PublicUser = Omit<User, 'password'>

// Record: key-value map
type UserMap = Record<string, User>

// Readonly: all properties immutable
type ImmutableUser = Readonly<User>

// ReturnType & Parameters
type FnReturn = ReturnType<typeof myFunction>
type FnParams = Parameters<typeof myFunction>

// Exclude & Extract (for unions)
type NonNull = Exclude<string | null | undefined, null | undefined>
type Strings = Extract<string | number | boolean, string>
```

## Type Guards

```typescript
// typeof
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase()  // value is string
  }
  return value * 2  // value is number
}

// instanceof
function handle(error: Error | string) {
  if (error instanceof Error) {
    return error.message
  }
  return error
}

// in operator
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark()
  } else {
    animal.meow()
  }
}

// Custom type guard
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  )
}
```

## Type Assertions

```typescript
// as syntax (preferred)
const input = document.getElementById('input') as HTMLInputElement

// Non-null assertion (use sparingly)
const element = document.getElementById('root')!

// const assertion
const config = {
  endpoint: '/api',
  timeout: 5000
} as const  // readonly, literal types
```

## Mapped Types

```typescript
// Make all properties nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null
}

// Add prefix to keys
type Prefixed<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}
```

## Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur'
type Handler = `on${Capitalize<EventName>}`
// 'onClick' | 'onFocus' | 'onBlur'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'
type Endpoint = `/${string}`
type Route = `${HttpMethod} ${Endpoint}`
```

## Module Declarations

```typescript
// Extend existing module
declare module 'vue' {
  interface ComponentCustomProperties {
    $api: ApiClient
  }
}

// Declare module without types
declare module 'untyped-lib'

// Ambient declarations
declare const __VERSION__: string
declare function gtag(...args: unknown[]): void
```

## Common Patterns

### Discriminated Unions

```typescript
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: Error }

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data)   // data is available
  } else {
    console.error(result.error) // error is available
  }
}
```

### Builder Pattern

```typescript
class QueryBuilder<T> {
  private filters: Array<(item: T) => boolean> = []

  where(predicate: (item: T) => boolean): this {
    this.filters.push(predicate)
    return this
  }

  build(): (items: T[]) => T[] {
    return items => items.filter(item => 
      this.filters.every(f => f(item))
    )
  }
}
```

## Anti-Patterns to Avoid

1. **Overusing `any`** → Use `unknown` with type guards
2. **Type assertions without validation** → Add runtime checks
3. **Ignoring strict mode** → Enable strict in tsconfig
4. **Massive union types** → Use discriminated unions
5. **Duplicate type definitions** → Use generics and utility types
