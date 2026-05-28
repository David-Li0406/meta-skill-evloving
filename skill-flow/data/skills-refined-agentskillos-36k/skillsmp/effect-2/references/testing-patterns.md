# Testing Patterns

## effect-vitest Integration

```typescript
import { it, describe } from "@effect/vitest"
import { Effect, Layer } from "effect"

describe("UserService", () => {
  // Basic effect test
  it.effect("finds user by id", () =>
    Effect.gen(function* () {
      const user = yield* UserService.findById(testUserId)
      expect(user.email).toBe("test@example.com")
    })
  )

  // With layer provision
  it.effect("creates user", () =>
    Effect.gen(function* () {
      const user = yield* UserService.create({ email: "new@example.com", name: "New" })
      expect(user.id).toBeDefined()
    }).pipe(Effect.provide(TestLayers))
  )
})
```

## Test Variants

```typescript
// it.effect - basic Effect test
it.effect("basic test", () => Effect.succeed(true))

// it.live - with live Clock, Random
it.live("time-dependent test", () =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    expect(now).toBeGreaterThan(0)
  })
)

// it.scoped - with resource cleanup
it.scoped("scoped test", () =>
  Effect.gen(function* () {
    const resource = yield* Effect.acquireRelease(
      openConnection(),
      (conn) => conn.close()
    )
    // resource cleaned up after test
  })
)

// it.scopedLive - scoped with live services
it.scopedLive("scoped live test", () =>
  Effect.gen(function* () {
    const conn = yield* acquireDbConnection()
    yield* conn.query("SELECT 1")
  })
)
```

## Layer Sharing Between Tests

```typescript
const TestLayers = Layer.mergeAll(
  UserServiceTest,
  AuthServiceTest,
  Layer.succeed(Config, testConfig),
)

describe("OrderService", () => {
  // Shared layers for all tests
  const provide = <A, E>(effect: Effect.Effect<A, E, OrderService | UserService>) =>
    effect.pipe(Effect.provide(TestLayers))

  it.effect("creates order", () =>
    provide(
      Effect.gen(function* () {
        const order = yield* OrderService.create(testInput)
        expect(order.status).toBe("pending")
      })
    )
  )

  it.effect("cancels order", () =>
    provide(
      Effect.gen(function* () {
        const result = yield* OrderService.cancel(testOrderId)
        expect(result.status).toBe("cancelled")
      })
    )
  )
})
```

## Mock Services

### Simple Mock with Layer.succeed

```typescript
const mockUser: User = {
  id: UserId.make("test-id"),
  email: "test@example.com",
  name: "Test User",
}

const UserServiceTest = Layer.succeed(UserService, {
  findById: () => Effect.succeed(mockUser),
  create: (input) => Effect.succeed({ ...mockUser, ...input }),
  delete: () => Effect.void,
})
```

### Stateful Mock

```typescript
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
          const user: User = {
            id: UserId.make(crypto.randomUUID()),
            ...input,
            createdAt: new Date(),
          }
          yield* Ref.update(users, (map) => new Map(map).set(user.id, user))
          return user
        }),

      // Helper for test setup
      _seed: (seedUsers: User[]) =>
        Ref.set(users, new Map(seedUsers.map((u) => [u.id, u]))),
    }
  }),
}) {}
```

## Property-Based Testing with FastCheck

```typescript
import * as fc from "fast-check"
import { it } from "@effect/vitest"

it.effect("email validation is consistent", () =>
  Effect.gen(function* () {
    fc.assert(
      fc.property(fc.emailAddress(), (email) => {
        const result = Schema.decodeUnknownEither(Email)(email)
        return Either.isRight(result)
      })
    )
  })
)

it.effect("user creation roundtrips", () =>
  Effect.gen(function* () {
    const userArb = fc.record({
      email: fc.emailAddress(),
      name: fc.string({ minLength: 1, maxLength: 100 }),
    })

    yield* fc.assert(
      fc.asyncProperty(userArb, async (input) => {
        const effect = Effect.gen(function* () {
          const created = yield* UserService.create(input)
          const found = yield* UserService.findById(created.id)
          return created.email === found.email && created.name === found.name
        })

        return Effect.runPromise(effect.pipe(Effect.provide(TestLayers)))
      })
    )
  })
)
```

## Database Testing with Testcontainers

### Per-Test Container

```typescript
import { PostgreSqlContainer } from "@testcontainers/postgresql"

describe("UserRepo", () => {
  let container: StartedPostgreSqlContainer

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start()
  })

  afterAll(async () => {
    await container.stop()
  })

  const makeDbLayer = () =>
    PgClient.layer({
      host: Config.succeed(container.getHost()),
      port: Config.succeed(container.getPort()),
      database: Config.succeed(container.getDatabase()),
      username: Config.succeed(container.getUsername()),
      password: Config.succeed(container.getPassword()),
    })

  it.effect("creates and finds user", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepo
      const created = yield* repo.create({ email: "test@example.com", name: "Test" })
      const found = yield* repo.findById(created.id)
      expect(Option.isSome(found)).toBe(true)
    }).pipe(Effect.provide(Layer.provide(UserRepo.Default, makeDbLayer())))
  )
})
```

### Shared Container Across Tests

```typescript
import { PostgreSqlContainer, StartedPostgreSqlContainer } from "@testcontainers/postgresql"

let sharedContainer: StartedPostgreSqlContainer

beforeAll(async () => {
  sharedContainer = await new PostgreSqlContainer()
    .withReuse()
    .start()
})

const SharedDbLayer = Layer.unwrapEffect(
  Effect.sync(() =>
    PgClient.layer({
      host: Config.succeed(sharedContainer.getHost()),
      port: Config.succeed(sharedContainer.getPort()),
      database: Config.succeed(sharedContainer.getDatabase()),
      username: Config.succeed(sharedContainer.getUsername()),
      password: Config.succeed(sharedContainer.getPassword()),
    })
  )
)
```

## Testing Error Cases

```typescript
it.effect("fails with UserNotFoundError for missing user", () =>
  Effect.gen(function* () {
    const result = yield* UserService.findById(nonExistentId).pipe(
      Effect.either
    )

    expect(Either.isLeft(result)).toBe(true)
    if (Either.isLeft(result)) {
      expect(result.left._tag).toBe("UserNotFoundError")
    }
  })
)

// Or with catchTag
it.effect("handles missing user gracefully", () =>
  Effect.gen(function* () {
    const result = yield* UserService.findById(nonExistentId).pipe(
      Effect.catchTag("UserNotFoundError", () => Effect.succeed(null))
    )
    expect(result).toBeNull()
  })
)
```

## Testing Effects with Timing

```typescript
it.live("debounces requests", () =>
  Effect.gen(function* () {
    const results: number[] = []

    yield* Effect.all([
      Service.request(1).pipe(Effect.tap((r) => results.push(r))),
      Service.request(2).pipe(Effect.tap((r) => results.push(r))),
      Service.request(3).pipe(Effect.tap((r) => results.push(r))),
    ], { concurrency: "unbounded" })

    // Only last request should complete due to debouncing
    expect(results).toEqual([3])
  })
)
```
