# Effect Atom Patterns

Effect Atom is a reactive state management library integrating with Effect-TS, providing atoms (reactive containers) with automatic dependency tracking and React integration.

## Core Concepts

### Basic Atoms

```typescript
import { Atom } from "@effect-rx/rx"

// Simple atom
const countAtom = Atom.make(0)

// With keepAlive for persistent global state
const userAtom = Atom.make<User | null>(null).pipe(Atom.keepAlive)
```

### Derived Atoms

```typescript
// Computed from other atoms
const doubleCountAtom = Atom.make((get) => get(countAtom) * 2)

// From multiple atoms
const fullNameAtom = Atom.make((get) =>
  `${get(firstNameAtom)} ${get(lastNameAtom)}`
)
```

### Effectful Atoms

```typescript
const userAtom = Atom.make((get) =>
  Effect.gen(function* () {
    const userId = get(userIdAtom)
    return yield* UserService.findById(userId)
  })
)
```

## React Hooks

```typescript
import { useAtomValue, useAtomSet, useAtom } from "@effect-rx/rx-react"

function Counter() {
  // Read only
  const count = useAtomValue(countAtom)

  // Write only
  const setCount = useAtomSet(countAtom)

  // Read and write
  const [count, setCount] = useAtom(countAtom)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  )
}
```

## Result Handling for Effectful Atoms

```typescript
import { Result } from "@effect-rx/rx"

const userAtom = Atom.make((get) =>
  Effect.gen(function* () {
    const userId = get(userIdAtom)
    return yield* UserService.findById(userId)
  })
)

function UserProfile() {
  const userResult = useAtomValue(userAtom)

  return Result.match(userResult, {
    onInitial: () => <p>Loading...</p>,
    onSuccess: (user) => <p>{user.name}</p>,
    onFailure: (error) => <p>Error: {error.message}</p>,
  })
}
```

### Result.builder for Tagged Errors

```typescript
function UserProfile() {
  const userResult = useAtomValue(userAtom)

  return Result.builder(userResult)
    .onInitial(() => <Spinner />)
    .onErrorTag("UserNotFoundError", (e) => <p>User {e.userId} not found</p>)
    .onErrorTag("AuthExpiredError", () => <LoginPrompt />)
    .onError((e) => <p>Unexpected error: {e.message}</p>)
    .onSuccess((user) => <UserCard user={user} />)
    .build()
}
```

## Atom Families

```typescript
// Parameterized atoms
const userByIdAtom = Atom.family((userId: UserId) =>
  Atom.make((get) =>
    Effect.gen(function* () {
      return yield* UserService.findById(userId)
    })
  )
)

// Usage
function UserCard({ userId }: { userId: UserId }) {
  const userResult = useAtomValue(userByIdAtom(userId))
  // ...
}
```

## Side Effects with Finalizers

```typescript
const websocketAtom = Atom.make((get) => {
  const url = get(wsUrlAtom)
  const socket = new WebSocket(url)

  // Register cleanup
  get.addFinalizer(() => {
    socket.close()
  })

  return socket
})
```

## Anti-Patterns

### Never Create Atoms Inside Components

```typescript
// BAD - new atom on every render
function Counter() {
  const countAtom = Atom.make(0) // WRONG!
  const count = useAtomValue(countAtom)
}

// GOOD - atom defined outside component
const countAtom = Atom.make(0)

function Counter() {
  const count = useAtomValue(countAtom)
}
```

### Avoid Imperative Updates from React

```typescript
// BAD - bypasses React's render cycle
function Counter() {
  const handleClick = () => {
    countAtom.set(countAtom.get() + 1) // WRONG!
  }
}

// GOOD - use hooks
function Counter() {
  const setCount = useAtomSet(countAtom)
  const handleClick = () => setCount((c) => c + 1)
}
```

### Always Register Finalizers for Resources

```typescript
// BAD - memory leak
const eventAtom = Atom.make((get) => {
  const handler = () => console.log("event")
  window.addEventListener("resize", handler) // Never cleaned up!
  return handler
})

// GOOD - with finalizer
const eventAtom = Atom.make((get) => {
  const handler = () => console.log("event")
  window.addEventListener("resize", handler)
  get.addFinalizer(() => window.removeEventListener("resize", handler))
  return handler
})
```

### Never Update State During Render

```typescript
// BAD - side effect during render
function Counter() {
  const count = useAtomValue(countAtom)
  if (count > 10) {
    setCount(0) // WRONG! Side effect during render
  }
}

// GOOD - in event handler or useEffect
function Counter() {
  const [count, setCount] = useAtom(countAtom)

  useEffect(() => {
    if (count > 10) setCount(0)
  }, [count])
}
```

## Performance Optimization

### Use Derived Atoms for Selective Re-rendering

```typescript
// BAD - re-renders on any user change
const userAtom = Atom.make({ name: "John", email: "john@example.com", age: 30 })

function UserName() {
  const user = useAtomValue(userAtom) // Re-renders when age changes too
  return <p>{user.name}</p>
}

// GOOD - only re-renders when name changes
const userNameAtom = Atom.make((get) => get(userAtom).name)

function UserName() {
  const name = useAtomValue(userNameAtom)
  return <p>{name}</p>
}
```

### Use keepAlive Judiciously

```typescript
// Use keepAlive for frequently accessed global state
const authAtom = Atom.make<AuthState>(initialAuth).pipe(Atom.keepAlive)

// Don't use keepAlive for component-local or temporary state
const formAtom = Atom.make(initialFormState) // No keepAlive - cleaned up when unmounted
```
