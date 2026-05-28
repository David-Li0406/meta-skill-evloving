# Service Patterns

## Effect.Service (Preferred)

Use `Effect.Service` for business services. It provides:
- Built-in `Default` layer
- Automatic method accessors
- Explicit dependency declaration
- Consistent structure

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  dependencies: [DatabaseService.Default, CacheService.Default],
  effect: Effect.gen(function* () {
    const db = yield* DatabaseService
    const cache = yield* CacheService

    return {
      findById: Effect.fn("UserService.findById")(
        (id: UserId): Effect.Effect<User, UserNotFoundError> =>
          cache.get(id).pipe(
            Effect.flatMap(Option.match({
              onNone: () => db.findUser(id).pipe(
                Effect.tap((user) => cache.set(id, user))
              ),
              onSome: Effect.succeed,
            }))
          )
      ),

      create: Effect.fn("UserService.create")(
        (input: UserInput): Effect.Effect<User, ValidationError> =>
          db.createUser(input)
      ),
    }
  }),
}) {}

// Usage - dependencies auto-provided when using Default
UserService.findById(userId)

// Or with explicit provision
program.pipe(Effect.provide(UserService.Default))
```

## Declaring Dependencies

Always declare dependencies in the `dependencies` array:

```typescript
// GOOD - dependencies declared
class OrderService extends Effect.Service<OrderService>()("OrderService", {
  dependencies: [UserService.Default, PaymentService.Default],
  effect: Effect.gen(function* () {
    const users = yield* UserService
    const payments = yield* PaymentService
    // ...
  }),
}) {}

// BAD - dependencies leaked
class OrderService extends Effect.Service<OrderService>()("OrderService", {
  effect: Effect.gen(function* () {
    const users = yield* UserService // Dependency not declared!
    // ...
  }),
}) {}
```

## Effect.fn for Tracing

Wrap methods with `Effect.fn` for automatic spans:

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  effect: Effect.gen(function* () {
    return {
      // Automatic span: "UserService.findById"
      findById: Effect.fn("UserService.findById")(
        (id: UserId) => /* ... */
      ),

      // With annotations
      create: Effect.fn("UserService.create")(
        (input: UserInput) =>
          Effect.gen(function* () {
            // Add business context to span
            yield* Effect.annotateCurrentSpan({ email: input.email })
            // ...
          })
      ),
    }
  }),
}) {}
```

## Context.Tag for Infrastructure

Use `Context.Tag` only for infrastructure injected at runtime:

```typescript
// OK - runtime-injected infrastructure
class DatabaseClient extends Context.Tag("DatabaseClient")<
  DatabaseClient,
  SqlClient.SqlClient
>() {}

class CloudflareEnv extends Context.Tag("CloudflareEnv")<
  CloudflareEnv,
  Env
>() {}

// NOT OK - business service
const UserService = Context.Tag<UserService>("UserService") // Use Effect.Service instead
```

## Return Types

Services return `Effect`, not `Promise`:

```typescript
interface UserService {
  // GOOD - returns Effect
  findById(id: UserId): Effect.Effect<User, UserNotFoundError>

  // BAD - returns Promise
  findById(id: UserId): Promise<User>
}
```

## Option vs Effect for Nullable Results

Offer both variants when useful:

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  effect: Effect.gen(function* () {
    const db = yield* DatabaseService

    return {
      // Returns Effect that fails if not found
      findById: Effect.fn("UserService.findById")(
        (id: UserId): Effect.Effect<User, UserNotFoundError> =>
          db.findUser(id).pipe(
            Effect.flatMap(Option.match({
              onNone: () => Effect.fail(new UserNotFoundError({ userId: id })),
              onSome: Effect.succeed,
            }))
          )
      ),

      // Returns Option for simpler null-checking
      findByIdOption: Effect.fn("UserService.findByIdOption")(
        (id: UserId): Effect.Effect<Option.Option<User>> =>
          db.findUser(id)
      ),
    }
  }),
}) {}
```

## Single Responsibility

Focus services on specific domains:

```typescript
// GOOD - focused services
class UserService { /* user operations */ }
class AuthService { /* authentication */ }
class NotificationService { /* notifications */ }

// BAD - god service
class AppService {
  createUser() { /* ... */ }
  login() { /* ... */ }
  sendEmail() { /* ... */ }
  processPayment() { /* ... */ }
}
```

## Test Implementations

```typescript
// Simple mock with Layer.succeed
const TestUserService = Layer.succeed(UserService, {
  findById: () => Effect.succeed(mockUser),
  create: () => Effect.succeed(mockUser),
})

// Stateful mock for integration tests
class TestUserService extends Effect.Service<TestUserService>()("UserService", {
  effect: Effect.gen(function* () {
    const users = yield* Ref.make<Map<UserId, User>>(new Map())

    return {
      findById: (id: UserId) =>
        Ref.get(users).pipe(
          Effect.flatMap((map) =>
            Option.fromNullable(map.get(id)).pipe(
              Option.match({
                onNone: () => Effect.fail(new UserNotFoundError({ userId: id })),
                onSome: Effect.succeed,
              })
            )
          )
        ),

      create: (input: UserInput) =>
        Effect.gen(function* () {
          const user = new User({ id: UserId.make(crypto.randomUUID()), ...input })
          yield* Ref.update(users, (map) => new Map(map).set(user.id, user))
          return user
        }),
    }
  }),
}) {}
```
