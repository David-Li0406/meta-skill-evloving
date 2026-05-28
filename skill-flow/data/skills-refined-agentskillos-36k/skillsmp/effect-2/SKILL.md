---
name: effect
description: Effect-TS best practices for services, errors, layers, schemas, and testing. Use when writing/reviewing Effect code, implementing services, handling errors, or composing layers.
---

# Effect-TS Best Practices

Opinionated patterns for Effect-TS codebases. Effect provides typed functional programming with composable errors, dependency injection, and observability.

## Critical Rules

1. **NEVER use `any` or type casts (`as Type`)** - Use `Schema.make()` for branded types, `Schema.decodeUnknown()` for parsing
2. **Don't use `catchAll` when error type is `never`** - No errors to catch
3. **Never use global `Error` in Effect channels** - Use `Schema.TaggedError` for domain errors
4. **Ban `{ disableValidation: true }`** - Lint against this
5. **Don't wrap safe operations in Effect** - Only use `Effect.try()` for throwing operations
6. **Use `mapError` not `catchAllCause`** - Distinguish expected errors from bugs
7. **Never silently swallow errors** - Failures MUST be visible in the Effect's error channel E

## Quick Reference

| Pattern | DON'T | DO |
|---------|-------|-----|
| Service definition | `Context.Tag` | `Effect.Service` with `dependencies` array |
| Error types | Generic `Error` | `Schema.TaggedError` with context fields |
| Branded IDs | Raw `string` | `Schema.String.pipe(Schema.brand("@Ns/Entity"))` |
| Running effects | `runSync`/`runPromise` in services | Return `Effect`, run at edge |
| Logging | `console.log` | `Effect.log` with structured data |
| Configuration | `process.env` | `Config` with validation |
| Method tracing | Manual spans | `Effect.fn("Service.method")` |
| Nullable results | `null`/`undefined` | `Option` types |
| State | Mutable variables | `Ref` |
| Time | `Date.now()`, `new Date()` | `Clock` service |

## Service Pattern

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  dependencies: [DatabaseService.Default],
  effect: Effect.gen(function* () {
    const db = yield* DatabaseService

    return {
      findById: Effect.fn("UserService.findById")(
        (id: UserId) => db.query(/* ... */)
      ),
    }
  }),
}) {}

// Usage - dependencies auto-provided
UserService.findById(userId)
```

## Error Handling

```typescript
// Define domain-specific errors
class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()(
  "UserNotFoundError",
  { userId: UserId, message: Schema.String }
) {}

// Handle with catchTag (preserves type info)
effect.pipe(
  Effect.catchTag("UserNotFoundError", (e) => /* handle */),
  Effect.catchTag("AuthExpiredError", (e) => /* handle */)
)
```

## Schema Pattern

```typescript
// Branded ID
const UserId = Schema.String.pipe(Schema.brand("@App/UserId"))

// Domain entity with Schema.Class
class User extends Schema.Class<User>("User")({
  id: UserId,
  email: Schema.String,
  createdAt: Schema.DateFromSelf,
}) {
  get displayName() { return this.email.split("@")[0] }
}
```

## Layer Composition

```typescript
// Declare dependencies in service, not at usage
const MainLayer = Layer.mergeAll(
  UserServiceLive,
  AuthServiceLive,
  DatabaseLive
)

// Run program
Effect.runPromise(program.pipe(Effect.provide(MainLayer)))
```

## Detailed Guides

- [Anti-Patterns](./references/anti-patterns.md) - Forbidden patterns with fixes
- [Error Patterns](./references/error-patterns.md) - Domain errors, rich context, HTTP mapping
- [Schema Patterns](./references/schema-patterns.md) - Branded types, transforms, validation
- [Service Patterns](./references/service-patterns.md) - Effect.Service, dependency injection
- [Layer Patterns](./references/layer-patterns.md) - Composition, memoization, testing
- [Observability Patterns](./references/observability-patterns.md) - Logging, tracing, metrics
- [SQL Patterns](./references/sql-patterns.md) - Database integration, transactions
- [Testing Patterns](./references/testing-patterns.md) - effect-vitest, property testing, Testcontainers
- [Atom Patterns](./references/atom-patterns.md) - React state management with Effect
- [RPC & Cluster Patterns](./references/rpc-cluster-patterns.md) - Distributed systems
