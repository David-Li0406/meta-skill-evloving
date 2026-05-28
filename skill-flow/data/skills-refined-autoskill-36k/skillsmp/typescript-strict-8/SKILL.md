---
name: typescript-strict
description: TypeScript strict mode patterns and advanced type techniques
license: MIT
---

# TypeScript Strict Mode Skill

Advanced TypeScript patterns for strict mode, type safety, and sophisticated type techniques.

## When to Use

- Enforcing strict TypeScript configuration
- Implementing advanced type patterns
- Building type-safe APIs and libraries
- Improving type inference and narrowing

## Strict Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Strict mode (enables all strict flags)
    "strict": true,

    // Individual strict flags (all enabled by "strict": true)
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,

    // Additional strictness
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,

    // Module resolution
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],

    // Output
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Interop
    "esModuleInterop": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

## Type Narrowing

### Type Guards

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase() // value is string
  }
  return value.toFixed(2) // value is number
}

// instanceof guard
function handleError(error: Error | string) {
  if (error instanceof Error) {
    return error.message // error is Error
  }
  return error // error is string
}

// in operator
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark() // animal is Dog
  } else {
    animal.meow() // animal is Cat
  }
}

// Custom type guard
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj &&
    typeof (obj as User).id === 'string' &&
    typeof (obj as User).email === 'string'
  )
}

// Assertion function
function assertDefined<T>(value: T | null | undefined, message?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Value is not defined')
  }
}

// Usage
function getUser(id: string): User | null {
  // ...
}

const user = getUser('123')
assertDefined(user, 'User not found')
console.log(user.email) // user is User, not User | null
```

### Discriminated Unions

```typescript
// Status pattern
type LoadingState = { status: 'loading' }
type SuccessState<T> = { status: 'success'; data: T }
type ErrorState = { status: 'error'; error: Error }
type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState

function handleState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'loading':
      return 'Loading...'
    case 'success':
      return `Data: ${state.data}` // state.data is available
    case 'error':
      return `Error: ${state.error.message}` // state.error is available
  }
}

// Event pattern
type UserCreatedEvent = {
  type: 'USER_CREATED'
  payload: { userId: string; email: string }
}

type UserUpdatedEvent = {
  type: 'USER_UPDATED'
  payload: { userId: string; changes: Partial<User> }
}

type UserDeletedEvent = {
  type: 'USER_DELETED'
  payload: { userId: string }
}

type UserEvent = UserCreatedEvent | UserUpdatedEvent | UserDeletedEvent

function handleEvent(event: UserEvent) {
  switch (event.type) {
    case 'USER_CREATED':
      console.log(`Created user ${event.payload.email}`)
      break
    case 'USER_UPDATED':
      console.log(`Updated user ${event.payload.userId}`)
      break
    case 'USER_DELETED':
      console.log(`Deleted user ${event.payload.userId}`)
      break
  }
}
```

## Utility Types

### Built-in Utilities

```typescript
interface User {
  id: string
  email: string
  name: string
  age: number
  role: 'admin' | 'user'
}

// Partial - all properties optional
type PartialUser = Partial<User>
// { id?: string; email?: string; ... }

// Required - all properties required
type RequiredUser = Required<PartialUser>

// Readonly - all properties readonly
type ReadonlyUser = Readonly<User>

// Pick - select specific properties
type UserCredentials = Pick<User, 'email' | 'id'>
// { email: string; id: string }

// Omit - exclude specific properties
type PublicUser = Omit<User, 'role'>
// { id: string; email: string; name: string; age: number }

// Record - object with specific key/value types
type UserRoles = Record<string, 'admin' | 'user'>
// { [key: string]: 'admin' | 'user' }

// Extract - extract types from union
type StringOrNumber = string | number | boolean
type JustStrings = Extract<StringOrNumber, string>
// string

// Exclude - exclude types from union
type NotStrings = Exclude<StringOrNumber, string>
// number | boolean

// NonNullable - remove null and undefined
type MaybeString = string | null | undefined
type DefinitelyString = NonNullable<MaybeString>
// string

// ReturnType - get function return type
function createUser() {
  return { id: '1', name: 'John' }
}
type NewUser = ReturnType<typeof createUser>
// { id: string; name: string }

// Parameters - get function parameter types
function updateUser(id: string, data: Partial<User>) {}
type UpdateParams = Parameters<typeof updateUser>
// [string, Partial<User>]

// Awaited - unwrap Promise type
type AsyncUser = Promise<User>
type ResolvedUser = Awaited<AsyncUser>
// User
```

### Custom Utility Types

```typescript
// DeepPartial - recursive partial
type DeepPartial<T> = T extends object
  ? { [P in keyof T]?: DeepPartial<T[P]> }
  : T

// DeepReadonly - recursive readonly
type DeepReadonly<T> = T extends object
  ? { readonly [P in keyof T]: DeepReadonly<T[P]> }
  : T

// Nullable - add null to type
type Nullable<T> = T | null

// NonEmptyArray - array with at least one element
type NonEmptyArray<T> = [T, ...T[]]

function firstElement<T>(arr: NonEmptyArray<T>): T {
  return arr[0] // No undefined risk
}

// RequireAtLeastOne - at least one property required
type RequireAtLeastOne<T, Keys extends keyof T = keyof T> =
  Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
  }[Keys]

type SearchParams = RequireAtLeastOne<{
  id?: string
  email?: string
  name?: string
}, 'id' | 'email' | 'name'>

// Must provide at least one of id, email, or name
const validSearch: SearchParams = { email: 'test@test.com' }

// Prettify - expand type for better IDE display
type Prettify<T> = {
  [K in keyof T]: T[K]
} & {}

// MergeTypes - merge two types with second overriding first
type MergeTypes<T, U> = Prettify<Omit<T, keyof U> & U>
```

## Template Literal Types

```typescript
// Event names
type EventName = `on${Capitalize<string>}`

// HTTP methods
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
type ApiEndpoint = `/${string}`
type ApiRoute = `${HttpMethod} ${ApiEndpoint}`

const route: ApiRoute = 'GET /users'

// Property paths
type PropPath<T, Prefix extends string = ''> = T extends object
  ? {
      [K in keyof T & string]: K | `${K}.${PropPath<T[K], ''>}`
    }[keyof T & string]
  : never

interface Config {
  database: {
    host: string
    port: number
  }
  cache: {
    enabled: boolean
  }
}

type ConfigPath = PropPath<Config>
// 'database' | 'database.host' | 'database.port' | 'cache' | 'cache.enabled'

// CSS units
type CSSUnit = 'px' | 'em' | 'rem' | '%' | 'vh' | 'vw'
type CSSValue = `${number}${CSSUnit}`

const width: CSSValue = '100px'
const height: CSSValue = '50vh'
```

## Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false
type A = IsString<string> // true
type B = IsString<number> // false

// Infer keyword
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T
type UnwrapArray<T> = T extends (infer U)[] ? U : T

type X = UnwrapPromise<Promise<string>> // string
type Y = UnwrapArray<number[]> // number

// Function return type extraction
type GetReturnType<T> = T extends (...args: any[]) => infer R ? R : never

// Extract function argument types
type GetFirstArg<T> = T extends (first: infer F, ...args: any[]) => any ? F : never

// Distributive conditional types
type ToArray<T> = T extends any ? T[] : never
type StrOrNumArray = ToArray<string | number>
// string[] | number[]

// Prevent distribution with tuple
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never
type StrOrNumArraySingle = ToArrayNonDist<string | number>
// (string | number)[]
```

## Mapped Types

```typescript
// Basic mapped type
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}

interface Person {
  name: string
  age: number
}

type PersonGetters = Getters<Person>
// { getName: () => string; getAge: () => number }

// Filter properties
type FilterByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K]
}

type StringProps = FilterByType<Person, string>
// { name: string }

// Make specific properties required
type RequireProps<T, K extends keyof T> = T & Required<Pick<T, K>>

interface Config {
  host?: string
  port?: number
  debug?: boolean
}

type RequiredHostConfig = RequireProps<Config, 'host'>
// { host: string; port?: number; debug?: boolean }

// Mutable - remove readonly
type Mutable<T> = {
  -readonly [K in keyof T]: T[K]
}
```

## Generic Constraints

```typescript
// Basic constraint
function getLength<T extends { length: number }>(item: T): number {
  return item.length
}

// Key constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

// Constructor constraint
type Constructor<T = {}> = new (...args: any[]) => T

function createInstance<T>(ctor: Constructor<T>): T {
  return new ctor()
}

// Multiple constraints
interface Identifiable { id: string }
interface Timestamped { createdAt: Date }

function processEntity<T extends Identifiable & Timestamped>(entity: T) {
  console.log(entity.id, entity.createdAt)
}

// Default type parameter
function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value)
}

const strings = createArray(3, 'hello') // string[]
const numbers = createArray<number>(3, 42) // number[]
```

## Branded Types

```typescript
// Create distinct types for primitive values
declare const brand: unique symbol

type Brand<T, B> = T & { [brand]: B }

type UserId = Brand<string, 'UserId'>
type PostId = Brand<string, 'PostId'>
type Email = Brand<string, 'Email'>

// Constructor functions
function UserId(id: string): UserId {
  return id as UserId
}

function PostId(id: string): PostId {
  return id as PostId
}

function Email(email: string): Email {
  if (!email.includes('@')) {
    throw new Error('Invalid email')
  }
  return email as Email
}

// Usage - prevents mixing IDs
function getUser(id: UserId): User {
  // ...
}

function getPost(id: PostId): Post {
  // ...
}

const userId = UserId('user-123')
const postId = PostId('post-456')

getUser(userId) // OK
// getUser(postId) // Error: PostId is not assignable to UserId
```

## Type-Safe Event Emitter

```typescript
type EventMap = Record<string, any[]>

class TypedEventEmitter<Events extends EventMap> {
  private listeners = new Map<keyof Events, Set<Function>>()

  on<E extends keyof Events>(
    event: E,
    listener: (...args: Events[E]) => void
  ): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set())
    }
    this.listeners.get(event)!.add(listener)

    return () => this.off(event, listener)
  }

  off<E extends keyof Events>(
    event: E,
    listener: (...args: Events[E]) => void
  ): void {
    this.listeners.get(event)?.delete(listener)
  }

  emit<E extends keyof Events>(event: E, ...args: Events[E]): void {
    this.listeners.get(event)?.forEach(listener => listener(...args))
  }
}

// Usage
interface AppEvents {
  userLoggedIn: [userId: string]
  userLoggedOut: []
  messageReceived: [message: string, from: string]
}

const emitter = new TypedEventEmitter<AppEvents>()

emitter.on('userLoggedIn', (userId) => {
  console.log(`User ${userId} logged in`)
})

emitter.on('messageReceived', (message, from) => {
  console.log(`${from}: ${message}`)
})

emitter.emit('userLoggedIn', 'user-123')
emitter.emit('messageReceived', 'Hello!', 'John')
```

## Type-Safe Builder Pattern

```typescript
type BuilderState = {
  name: boolean
  email: boolean
  age: boolean
}

type RequiredFields = 'name' | 'email'

class UserBuilder<State extends Partial<BuilderState> = {}> {
  private user: Partial<User> = {}

  setName(name: string): UserBuilder<State & { name: true }> {
    this.user.name = name
    return this as any
  }

  setEmail(email: string): UserBuilder<State & { email: true }> {
    this.user.email = email
    return this as any
  }

  setAge(age: number): UserBuilder<State & { age: true }> {
    this.user.age = age
    return this as any
  }

  build(
    this: UserBuilder<{ name: true; email: true }>
  ): User {
    return this.user as User
  }
}

// Usage
const user = new UserBuilder()
  .setName('John')
  .setEmail('john@example.com')
  .setAge(30)
  .build() // Only available after name and email are set

// const invalid = new UserBuilder()
//   .setName('John')
//   .build() // Error: email not set
```

## Best Practices

1. **Enable all strict flags** - don't half-measure
2. **Avoid `any`** - use `unknown` and narrow
3. **Use discriminated unions** - for state machines
4. **Prefer interfaces for objects** - use types for unions/intersections
5. **Use `const` assertions** - for literal types
6. **Leverage type inference** - don't over-annotate
7. **Use branded types** - for domain primitives
8. **Write type guards** - for runtime safety
9. **Use `satisfies`** - for type checking without widening
10. **Keep types close to usage** - colocate when possible

## Common Pitfalls

```typescript
// Bad: any
function process(data: any) {}

// Good: unknown with narrowing
function process(data: unknown) {
  if (typeof data === 'string') {
    // data is string
  }
}

// Bad: type assertion without validation
const user = JSON.parse(data) as User

// Good: runtime validation
const user = parseUser(JSON.parse(data))

// Bad: ignoring null checks
function getName(user: User | null) {
  return user.name // Error in strict mode
}

// Good: proper null handling
function getName(user: User | null) {
  return user?.name ?? 'Unknown'
}

// Bad: object index without undefined check
const value = obj[key] // might be undefined

// Good: with noUncheckedIndexedAccess
const value = obj[key]
if (value !== undefined) {
  // use value
}
```
