# Layer Patterns

## Flat Composition with Layer.mergeAll

```typescript
// GOOD - flat composition at app root
const MainLayer = Layer.mergeAll(
  UserServiceLive,
  AuthServiceLive,
  PaymentServiceLive,
  DatabaseLive,
  CacheLive,
)

// BAD - deeply nested
const MainLayer = UserServiceLive.pipe(
  Layer.provide(AuthServiceLive.pipe(
    Layer.provide(PaymentServiceLive.pipe(
      Layer.provide(DatabaseLive)
    ))
  ))
)
```

## Dependencies Declared in Services

```typescript
// Dependencies declared in service, auto-provided
class UserService extends Effect.Service<UserService>()("UserService", {
  dependencies: [DatabaseService.Default],
  effect: /* ... */
}) {}

// At app root, just merge
const MainLayer = Layer.mergeAll(
  UserService.Default,
  DatabaseLive,
)
```

## Infrastructure Exception

Database, Redis, HTTP clients can remain undeclared when provided once at root:

```typescript
// OK - infrastructure provided at root
class UserService extends Effect.Service<UserService>()("UserService", {
  // DatabaseClient not in dependencies - it's infrastructure
  effect: Effect.gen(function* () {
    const db = yield* DatabaseClient
    // ...
  }),
}) {}

// App root provides infrastructure
const MainLayer = Layer.mergeAll(
  UserService.Default,
  DatabaseLive, // Provided once here
)
```

## Naming Conventions

| Suffix | Usage |
|--------|-------|
| `ServiceLive` | Production implementation |
| `ServiceTest` | Test mock |
| `ServiceLayer` | Generic/configurable implementation |

```typescript
const UserServiceLive = UserService.Default
const UserServiceTest = Layer.succeed(UserService, mockUserService)
```

## Layer.effect vs Layer.succeed

```typescript
// Layer.succeed - static, no effects needed
const ConfigLayer = Layer.succeed(Config, { port: 3000, debug: false })

// Layer.effect - requires Effect for construction
const DatabaseLayer = Layer.effect(
  DatabaseClient,
  Effect.gen(function* () {
    const config = yield* DatabaseConfig
    return yield* createConnection(config)
  })
)
```

## Layer.scoped for Resources

```typescript
// Acquire/release semantics
const DatabaseLayer = Layer.scoped(
  DatabaseClient,
  Effect.acquireRelease(
    createConnection(config),
    (conn) => conn.close().pipe(Effect.orDie)
  )
)
```

## Layer.unwrapEffect for Config-Dependent Layers

```typescript
// Layer that depends on async configuration
const FeatureFlagsLayer = Layer.unwrapEffect(
  Effect.gen(function* () {
    const config = yield* FeatureFlagsConfig
    if (config.provider === "launchdarkly") {
      return LaunchDarklyLayer
    } else {
      return LocalFeatureFlagsLayer
    }
  })
)
```

## Layer.lazy for Deferred Initialization

```typescript
// Expensive initialization deferred until first use
const HeavyServiceLayer = Layer.lazy(() =>
  Layer.effect(HeavyService, createHeavyService())
)
```

## Layer Memoization

Layers are memoized by object identity (reference equality):

```typescript
const DbLayer = Layer.effect(DatabaseClient, createConnection())

// Same reference - memoized, one connection
const App = Layer.mergeAll(
  UserService.pipe(Layer.provide(DbLayer)),
  OrderService.pipe(Layer.provide(DbLayer)),
)

// Different references - NOT memoized, two connections!
const App = Layer.mergeAll(
  UserService.pipe(Layer.provide(Layer.effect(DatabaseClient, createConnection()))),
  OrderService.pipe(Layer.provide(Layer.effect(DatabaseClient, createConnection()))),
)
```

## Layer.fresh to Escape Memoization

```typescript
// Force new instance
const FreshDbLayer = Layer.fresh(DbLayer)

// Useful for:
// - Per-request database connections
// - Test isolation
// - Avoiding shared state
```

## Test Layer Composition

```typescript
// Centralized test layers
const TestLayers = Layer.mergeAll(
  UserServiceTest,
  AuthServiceTest,
  Layer.succeed(Config, testConfig),
)

// In tests
describe("OrderService", () => {
  it.effect("creates order", () =>
    Effect.gen(function* () {
      const order = yield* OrderService.create(input)
      expect(order.status).toBe("pending")
    }).pipe(Effect.provide(TestLayers))
  )
})
```

## Layer Composition Patterns

```typescript
// Provide specific dependency
const UserWithDb = UserService.Default.pipe(
  Layer.provide(DatabaseLive)
)

// Merge independent layers
const Services = Layer.mergeAll(
  UserService.Default,
  AuthService.Default,
)

// Sequential composition (second depends on first)
const FullStack = Services.pipe(
  Layer.provideMerge(DatabaseLive)
)
```
