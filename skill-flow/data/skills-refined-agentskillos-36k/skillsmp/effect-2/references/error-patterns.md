# Error Patterns

## Core Principles

Use **explicit, domain-specific error types** rather than generic HTTP errors. Generic errors obscure context needed for UI recovery and debugging.

## Why Explicit Errors Matter

- Enables specific UI messages ("Your session expired" vs generic "Unauthorized")
- Allows targeted recovery strategies
- Improves observability and debugging
- Provides type-safe handling with `catchTag`

## Error Naming Conventions

| Category | Pattern | Example |
|----------|---------|---------|
| Entity lookups | `{Entity}NotFoundError` | `UserNotFoundError` |
| Action failures | `{Entity}{Action}Error` | `OrderCancelError` |
| Feature-specific | `{Feature}Error` | `CheckoutError` |
| External services | `{Integration}Error` | `StripePaymentError` |
| Validation | `Invalid{Field}Error` | `InvalidEmailError` |

## Defining Errors with Schema.TaggedError

```typescript
class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()(
  "UserNotFoundError",
  {
    userId: UserId,
    message: Schema.String,
  }
) {}

class OrderCancelError extends Schema.TaggedError<OrderCancelError>()(
  "OrderCancelError",
  {
    orderId: OrderId,
    reason: Schema.Literal("already_shipped", "already_cancelled", "not_found"),
    message: Schema.String,
  }
) {}
```

## Rich Context Pattern

Include contextual fields that support debugging and UI handling:

```typescript
// Entity errors - include resource IDs
class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()(
  "UserNotFoundError",
  {
    userId: UserId,
    message: Schema.String,
  }
) {}

// Action errors - include failed input
class OrderCreateError extends Schema.TaggedError<OrderCreateError>()(
  "OrderCreateError",
  {
    input: OrderInput,
    reason: Schema.String,
    message: Schema.String,
  }
) {}

// Integration errors - include service info and retryability
class StripePaymentError extends Schema.TaggedError<StripePaymentError>()(
  "StripePaymentError",
  {
    stripeErrorCode: Schema.String,
    retryable: Schema.Boolean,
    message: Schema.String,
  }
) {}

// Auth errors - include session/permission details
class AuthExpiredError extends Schema.TaggedError<AuthExpiredError>()(
  "AuthExpiredError",
  {
    sessionId: SessionId,
    expiredAt: Schema.DateFromSelf,
    message: Schema.String,
  }
) {}
```

## Three-Layer Error Architecture

Errors flow from Persistence -> Domain -> API layers:

```typescript
// Persistence layer
class SqlError extends Schema.TaggedError<SqlError>()(
  "SqlError",
  { query: Schema.String, cause: Schema.Unknown }
) {}

// Domain layer - catches and transforms
const findUser = (id: UserId) =>
  db.query(/* ... */).pipe(
    Effect.catchTag("SqlError", (e) =>
      Effect.fail(new UserNotFoundError({ userId: id, message: "User not found" }))
    )
  )

// API layer - maps to HTTP
const handler = (id: UserId) =>
  findUser(id).pipe(
    Effect.catchTag("UserNotFoundError", (e) =>
      Effect.fail(HttpError.notFound(e.message))
    )
  )
```

## HTTP Status Annotations

```typescript
import { HttpApiSchema } from "@effect/platform"

class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()(
  "UserNotFoundError",
  {
    userId: UserId,
    message: Schema.String,
  },
  HttpApiSchema.annotations({ status: 404 })
) {}

class AuthExpiredError extends Schema.TaggedError<AuthExpiredError>()(
  "AuthExpiredError",
  {
    message: Schema.String,
  },
  HttpApiSchema.annotations({ status: 401 })
) {}
```

## Handling Errors with catchTag

```typescript
// Preserves type information for each error
effect.pipe(
  Effect.catchTag("UserNotFoundError", (e) => {
    // e is typed as UserNotFoundError
    return Effect.succeed(createDefaultUser(e.userId))
  }),
  Effect.catchTag("AuthExpiredError", (e) => {
    // e is typed as AuthExpiredError
    return Effect.fail(new RedirectToLoginError({ returnUrl: currentUrl }))
  })
)

// Handle multiple errors
effect.pipe(
  Effect.catchTags({
    UserNotFoundError: (e) => /* ... */,
    AuthExpiredError: (e) => /* ... */,
    OrderCancelError: (e) => /* ... */,
  })
)
```

## Exhaustive Error Handling with Match

```typescript
import { Match } from "effect"

const handleError = Match.type<AppError>().pipe(
  Match.tag("UserNotFoundError", (e) => `User ${e.userId} not found`),
  Match.tag("AuthExpiredError", (e) => `Session expired at ${e.expiredAt}`),
  Match.tag("OrderCancelError", (e) => `Cannot cancel: ${e.reason}`),
  Match.exhaustive // Compile error if any error type not handled
)
```

## Error Chaining with cause

```typescript
class ServiceError extends Schema.TaggedError<ServiceError>()(
  "ServiceError",
  {
    message: Schema.String,
    cause: Schema.optional(Schema.Unknown),
  }
) {}

// Preserve original error
effect.pipe(
  Effect.mapError((originalError) =>
    new ServiceError({
      message: "Service operation failed",
      cause: originalError,
    })
  )
)
```
