---
name: effect-ts-best-practices
description: Use this skill when implementing or reviewing Effect-TS code, focusing on best practices for services, error handling, layers, schemas, and testing.
---

# Effect-TS Best Practices

This skill provides guidelines and best practices for using Effect-TS effectively in your applications.

## Overview

Use this skill to teach Effect-TS fundamentals and best practices, then apply them to user code and architecture questions.

## Teaching Workflow

1. Clarify context: runtime (node/bun/browser), goal (new app, refactor, review), and constraints.
2. Separate core vs shell: identify pure domain logic vs effects and boundaries.
3. Model errors and dependencies: define tagged error types and Context.Tag service interfaces.
4. Compose with Effect: use pipe/Effect.gen, typed errors, and Layer provisioning.
5. Validate inputs at boundaries with @effect/schema before entering core.
6. Explain resource safety: acquireRelease, scoped lifetimes, and clean finalizers.
7. Provide minimal, runnable examples tailored to the user context.
8. If the user asks for version-specific or "latest" details, verify with official docs before answering.

## Core Practices

- Use Effect for all side effects; keep core functions pure and total.
- Avoid async/await, raw Promise chains, and try/catch in application logic.
- Use Context.Tag + Layer for dependency injection and testability.
- Use tagged error unions and Match.exhaustive for total handling.
- Decode unknown at the boundary with @effect/schema; never leak unknown into core.
- Use Effect.acquireRelease/Effect.scoped for resource safety.
- Use @effect/platform services instead of host APIs (fetch, fs, child_process, etc.).

## Critical Rules

1. **NEVER use `any` or type casts (`as Type`)** - Use `Schema.make()` for branded types, `Schema.decodeUnknown()` for parsing.
2. **Don't use `catchAll` when error type is `never`** - No errors to catch.
3. **Never use global `Error` in Effect channels** - Use `Schema.TaggedError` for domain errors.
4. **Ban `{ disableValidation: true }`** - Lint against this.
5. **Don't wrap safe operations in Effect** - Only use `Effect.try()` for throwing operations.
6. **Use `mapError` not `catchAllCause`** - Distinguish expected errors from bugs.
7. **Never silently swallow errors** - Failures MUST be visible in the Effect's error channel E.

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

## Service Pattern Example

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  dependencies: [DatabaseService.Default],
  effect: Effect.gen(function* () {
    const db = yield* DatabaseService;

    return {
      findById: Effect.fn("UserService.findById")(
        (id: UserId) => db.query(/* ... */)
      ),
    };
  }),
}) {}

// Usage - dependencies auto-provided
UserService.findById(userId);
```

## Error Handling Example

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
);
```

## Schema Pattern Example

```typescript
// Branded ID
const UserId = Schema.String.pipe(Schema.brand("@App/UserId"));

// Domain entity with Schema.Class
class User extends Schema.Class<User>("User")({
  id: UserId,
  email: Schema.String,
  createdAt: Schema.DateFromSelf,
}) {
  get displayName() { return this.email.split("@")[0]; }
}
```

## Layer Composition Example

```typescript
// Declare dependencies in service, not at usage
const MainLayer = Layer.mergeAll(
  UserServiceLive,
  AuthServiceLive,
  DatabaseLive
);

// Run program
Effect.runPromise(program.pipe(Effect.provide(MainLayer)));
```

## Additional Resources

- Read `references/best-practices.md` for the extended checklist and examples.
- Read `references/platform-map.md` when comparing @effect/platform to Node/Bun/Browser APIs.
- Detailed guides on various patterns are available for further reading.