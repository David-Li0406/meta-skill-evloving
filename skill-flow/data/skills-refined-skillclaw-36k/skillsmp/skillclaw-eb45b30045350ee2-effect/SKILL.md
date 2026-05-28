---
name: effect
description: Use this skill when implementing Effect-TS features such as services, error handling, layers, and testing to ensure best practices are followed.
---

# Effect-TS Best Practices

This skill provides opinionated patterns and best practices for Effect-TS codebases, focusing on typed functional programming with composable errors, dependency injection, and observability.

## Before Implementation

Before implementing Effect features, run `effect-solutions list` to read the relevant guides.

### Available Topics
- Services and layers
- Data modeling with Schema
- Error handling patterns
- Configuration management
- Testing with Effect
- HTTP clients
- CLI applications
- Observability and tracing
- Project structure

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
effect.pipe(/* ... */);
```

## Effect Source Reference

The Effect repository is cloned at `~/.local/share/effect-solutions/effect`. Search here for real implementations when documentation isn't enough.

## Quick Commands

- `effect-solutions list` - List all available guides
- `effect-solutions show <topic>` - Read a specific guide