# Anti-Patterns (Forbidden)

These patterns break Effect's composition model, lose type safety, or prevent proper testing.

## 1. Effect.runSync/runPromise Inside Services

```typescript
// BAD - breaks composition, loses error handling
class MyService extends Effect.Service<MyService>()("MyService", {
  effect: Effect.gen(function* () {
    return {
      doThing: () => {
        const result = Effect.runSync(someEffect) // WRONG
        return result
      }
    }
  })
}) {}

// GOOD - return Effect, run at edge
class MyService extends Effect.Service<MyService>()("MyService", {
  effect: Effect.gen(function* () {
    return {
      doThing: () => someEffect // Returns Effect
    }
  })
}) {}
```

## 2. throw Inside Effect.gen

```typescript
// BAD - bypasses Effect's error channel
Effect.gen(function* () {
  if (!valid) throw new Error("Invalid") // WRONG
})

// GOOD - use typed errors
Effect.gen(function* () {
  if (!valid) yield* Effect.fail(new ValidationError({ message: "Invalid" }))
})
```

## 3. catchAll Losing Type Information

```typescript
// BAD - destroys error type info
effect.pipe(
  Effect.catchAll(() => Effect.succeed(defaultValue)) // Loses error context
)

// GOOD - handle specific errors
effect.pipe(
  Effect.catchTag("UserNotFoundError", () => Effect.succeed(defaultValue)),
  Effect.catchTag("AuthError", (e) => Effect.fail(new PublicAuthError(e)))
)
```

## 4. any/unknown Casts

```typescript
// BAD - bypasses type safety
const user = data as User // WRONG
const result: any = something // WRONG

// GOOD - use Schema
const user = yield* Schema.decodeUnknown(User)(data)
```

## 5. Promise in Service Signatures

```typescript
// BAD - loses Effect benefits
interface UserService {
  findUser(id: string): Promise<User> // WRONG
}

// GOOD - return Effect
interface UserService {
  findUser(id: UserId): Effect.Effect<User, UserNotFoundError>
}
```

## 6. console.log

```typescript
// BAD - not structured, lost in production
console.log("User created:", user)

// GOOD - structured logging
Effect.log("User created").pipe(
  Effect.annotateLogs({ userId: user.id, email: user.email })
)
```

## 7. process.env Directly

```typescript
// BAD - no validation, fails silently
const apiKey = process.env.API_KEY // WRONG

// GOOD - Config with validation
const ApiKey = Config.string("API_KEY").pipe(Config.withDescription("API key"))
const apiKey = yield* ApiKey
```

## 8. null/undefined in Domain Types

```typescript
// BAD - implicit absence
interface User {
  avatar: string | null // WRONG
}

// GOOD - explicit absence with Option
interface User {
  avatar: Option.Option<string>
}
```

## 9. Option.getOrThrow

```typescript
// BAD - throws exceptions
const value = Option.getOrThrow(maybeValue) // WRONG

// GOOD - explicit handling
const value = Option.match(maybeValue, {
  onNone: () => defaultValue,
  onSome: (v) => v
})
```

## 10. Context.Tag for Business Services

```typescript
// BAD - boilerplate, no built-in accessors
const UserService = Context.Tag<UserService>("UserService")

// GOOD - Effect.Service
class UserService extends Effect.Service<UserService>()("UserService", {
  effect: Effect.gen(function* () { /* ... */ })
}) {}
```

## 11. Ignoring Errors with orDie

```typescript
// BAD - converts recoverable to defects
effect.pipe(Effect.orDie) // WRONG - loses error info

// GOOD - handle errors explicitly
effect.pipe(
  Effect.catchTag("ExpectedError", (e) => /* handle or transform */)
)
```

## 12. Mixing Effect and Promise Chains

```typescript
// BAD - inconsistent error handling
const result = await effect.pipe(Effect.runPromise)
  .then(/* ... */)
  .catch(/* ... */) // WRONG

// GOOD - stay in Effect
effect.pipe(
  Effect.flatMap(/* ... */),
  Effect.catchAll(/* ... */),
  Effect.runPromise // Only at the edge
)
```

## 13. Mutable State Without Ref

```typescript
// BAD - race conditions, breaks referential transparency
let counter = 0
const increment = () => { counter++ } // WRONG

// GOOD - Ref for mutable state
const counter = yield* Ref.make(0)
const increment = Ref.update(counter, (n) => n + 1)
```

## 14. Date.now() / new Date() Directly

```typescript
// BAD - non-deterministic, hard to test
const timestamp = Date.now() // WRONG

// GOOD - Clock service
const timestamp = yield* Clock.currentTimeMillis
```

## 15. catchAll When Error Type is never

```typescript
// BAD - no errors to catch
const effect: Effect.Effect<User, never, Deps> = /* ... */
effect.pipe(Effect.catchAll(/* ... */)) // WRONG - pointless

// GOOD - only catch when there are errors
const effect: Effect.Effect<User, UserNotFoundError, Deps> = /* ... */
effect.pipe(Effect.catchTag("UserNotFoundError", /* ... */))
```
