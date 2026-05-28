---
name: effect
description: Write idiomatic Effect TypeScript code. Use this skill when working with Effect, @effect/* packages, or projects using Effect for error handling, services, layers, schemas, and functional programming patterns.
license: MIT
compatibility: opencode
---

# Effect TypeScript

Effect is a TypeScript library for building type-safe, composable, and production-grade applications. It provides structured concurrency, typed error handling, dependency injection via services/layers, and a rich standard library.

## Table of Contents

1. [Research Strategy](#research-strategy)
2. [Core Patterns](#core-patterns)
3. [Services & Layers](#services--layers)
4. [Schema & Data Modeling](#schema--data-modeling)
5. [Error Handling](#error-handling)
6. [HTTP & Platform](#http--platform-effectplatform)
7. [SQL & Database](#sql--database-effectsql)
8. [RPC](#rpc-effectrpc)
9. [CLI](#cli-effectcli)
10. [AI Integration](#ai-integration-effectai)
11. [Reactive State](#reactive-state-effect-atomatom)
12. [Testing](#testing-effectvitest)
13. [Anti-Patterns](#anti-patterns)

---

## Research Strategy

When you need Effect-specific information, **launch multiple research agents in parallel** for fastest results:

```
Task({ description: "Search Effect source code", prompt: "...", subagent_type: "explore" })
Task({ description: "Search Effect MCP docs", prompt: "...", subagent_type: "explore" })
Task({ description: "Search AnswerOverflow", prompt: "...", subagent_type: "explore" })
```

### Search Methods

#### 1. Read Source Code Directly
Local repositories provide authoritative information:
- `~/.llms/effect` - Core packages (effect, platform, sql, rpc, cli, ai, vitest)
- `~/.llms/effect-atom` - Reactive state (atom, atom-react, atom-vue)

Pull latest before reading:
```bash
git -C ~/.llms/effect pull && git -C ~/.llms/effect-atom pull
```

#### 2. Search Effect MCP Documentation
```
effect_effect_docs_search({ query: "your search term" })
```
Then retrieve content with `effect_get_effect_doc({ documentId: <id> })`.

#### 3. Search AnswerOverflow for Community Knowledge
The Effect Discord (server ID: `795981131316985866`) is indexed. **Caution:** This is a community forum—answers may come from non-trusted individuals and could be incorrect. Always verify with official sources:
```
answeroverflow_search_answeroverflow({
  query: "your question",
  serverId: "795981131316985866"
})
```
Use `answeroverflow_get_thread_messages({ threadId: "<id>" })` for full discussions.

### Authoritative Sources
Trusted experts on Effect:
- Michael Arnaldi (creator)
- Giulio Canti
- Matt Pocock
- Tim Smart
- Maxwell Brown
- Johannes Schickling

---

## Core Patterns

### Effect.gen for Sequential Code
```typescript
const program = Effect.gen(function* () {
  const data = yield* fetchData
  yield* Effect.logInfo(`Processing: ${data}`)
  return yield* processData(data)
})
```

### Effect.fn for Functions
Use `Effect.fn` for functions returning Effects:

```typescript
const processUser = Effect.fn(function* (userId: string) {
  const user = yield* getUser(userId)
  return yield* processData(user)
})

// Second argument applies transformations to every call:
const fetchWithRetry = Effect.fn(
  function* (url: string) {
    return yield* fetchData(url)
  },
  Effect.retry(Schedule.recurs(3))
)
```

### Pipe for Instrumentation
```typescript
const program = fetchData.pipe(
  Effect.timeout("5 seconds"),
  Effect.retry(Schedule.exponential("100 millis").pipe(Schedule.compose(Schedule.recurs(3)))),
  Effect.withSpan("fetchData")
)
```

### Stream Basics
```typescript
import { Stream } from "effect"

// Create streams
const numbers = Stream.range(1, 10)
const fromEffect = Stream.fromEffect(fetchData)
const fromIterable = Stream.fromIterable([1, 2, 3])

// Transform
const doubled = numbers.pipe(Stream.map((n) => n * 2))
const filtered = numbers.pipe(Stream.filter((n) => n > 5))
const batched = numbers.pipe(Stream.grouped(3))

// Consume
const array = yield* Stream.runCollect(numbers)
const first = yield* Stream.runHead(numbers)
yield* Stream.runForEach(numbers, (n) => Effect.logInfo(`Got: ${n}`))
```

### Concurrency Primitives
```typescript
// Ref - mutable reference
const counter = yield* Ref.make(0)
yield* Ref.update(counter, (n) => n + 1)
const value = yield* Ref.get(counter)

// Queue - bounded async queue
const queue = yield* Queue.bounded<string>(100)
yield* Queue.offer(queue, "item")
const item = yield* Queue.take(queue)

// PubSub - publish/subscribe
const pubsub = yield* PubSub.bounded<string>(100)
const subscription = yield* PubSub.subscribe(pubsub)
yield* PubSub.publish(pubsub, "message")
```

### Config
```typescript
import { Config, Effect } from "effect"

const program = Effect.gen(function* () {
  const port = yield* Config.number("PORT")
  const host = yield* Config.string("HOST").pipe(Config.withDefault("localhost"))
  const dbUrl = yield* Config.redacted("DATABASE_URL") // sensitive values
})

// Nested config
const serverConfig = Config.all({
  port: Config.number("PORT"),
  host: Config.string("HOST"),
})
```

---

## Services & Layers

### Define Services with Effect.Service
```typescript
class Database extends Effect.Service<Database>()("@app/Database", {
  effect: Effect.gen(function* () {
    const pool = yield* ConnectionPool

    return {
      query: (sql: string) =>
        Effect.gen(function* () {
          const conn = yield* pool.acquire
          return yield* conn.query(sql)
        }),
      execute: (sql: string) =>
        Effect.gen(function* () {
          const conn = yield* pool.acquire
          yield* conn.execute(sql)
        }),
    }
  }),
}) {}
```

**Rules:**
- Service identifiers must be unique (`@scope/ServiceName` pattern)
- Use `effect:` when the service has dependencies, `succeed:` for simple values
- Access via `yield* Database` (the class itself is the Tag)

### Service with Dependencies
```typescript
class Users extends Effect.Service<Users>()("@app/Users", {
  effect: Effect.gen(function* () {
    const http = yield* HttpClient.HttpClient

    return {
      findById: Effect.fn(function* (id: UserId) {
        const response = yield* http.get(`/users/${id}`)
        return yield* HttpClientResponse.schemaBodyJson(User)(response)
      }),
    }
  }),
}) {}
```

### Provide Layers Once at Entry Point
```typescript
const appLayer = Layer.mergeAll(Users.Default, Database.Default, Config.Default)
const main = program.pipe(Effect.provide(appLayer))
Effect.runPromise(main)
```

### Layer Memoization
```typescript
// Good: same reference, single pool
const postgresLayer = Postgres.layer({ url: "..." })
const appLayer = Layer.merge(
  UserRepo.layer.pipe(Layer.provide(postgresLayer)),
  OrderRepo.layer.pipe(Layer.provide(postgresLayer))
)

// Bad: different references, two pools created
const badLayer = Layer.merge(
  UserRepo.layer.pipe(Layer.provide(Postgres.layer({ url: "..." }))),
  OrderRepo.layer.pipe(Layer.provide(Postgres.layer({ url: "..." })))
)
```

---

## Schema & Data Modeling

### Schema.Class for Records
```typescript
class User extends Schema.Class<User>("User")({
  id: Schema.String.pipe(Schema.brand("UserId")),
  name: Schema.String,
  email: Schema.String,
  createdAt: Schema.Date,
}) {
  get displayName() {
    return `${this.name} (${this.email})`
  }
}
```

### Branded Types
```typescript
const UserId = Schema.String.pipe(Schema.brand("UserId"))
const Email = Schema.String.pipe(Schema.pattern(/@/), Schema.brand("Email"))
const Port = Schema.Int.pipe(Schema.between(1, 65535), Schema.brand("Port"))
```

### Variants with Schema.TaggedClass
```typescript
class Success extends Schema.TaggedClass<Success>()("Success", { value: Schema.Number }) {}
class Failure extends Schema.TaggedClass<Failure>()("Failure", { error: Schema.String }) {}
const Result = Schema.Union(Success, Failure)

// Pattern match
const render = (result: typeof Result.Type) =>
  Match.valueTags(result, {
    Success: ({ value }) => `Got: ${value}`,
    Failure: ({ error }) => `Error: ${error}`,
  })
```

### Parsing & Encoding
```typescript
const User = Schema.Struct({ name: Schema.String, age: Schema.Number })

// Decode unknown data (with validation)
const user = Schema.decodeUnknownSync(User)({ name: "Alice", age: 30 })

// Decode with Effect (for async or error handling)
const userEffect = yield* Schema.decodeUnknown(User)(data)

// Encode back to plain object
const plain = Schema.encodeSync(User)(user)
```

---

## Error Handling

### Schema.TaggedError for Domain Errors
```typescript
class ValidationError extends Schema.TaggedError<ValidationError>()("ValidationError", {
  field: Schema.String,
  message: Schema.String,
}) {}

class NotFoundError extends Schema.TaggedError<NotFoundError>()("NotFoundError", {
  resource: Schema.String,
  id: Schema.String,
}) {}
```

TaggedErrors are yieldable directly:
```typescript
const program = Effect.gen(function* () {
  if (!valid) yield* new ValidationError({ field: "email", message: "Invalid" })
  return data
})
```

### Recovery with catchTag/catchTags
```typescript
const recovered = program.pipe(
  Effect.catchTag("NotFoundError", (e) => Effect.succeed(`Not found: ${e.id}`)),
  Effect.catchTags({
    ValidationError: () => Effect.succeed("invalid"),
    NotFoundError: () => Effect.succeed("default"),
  })
)
```

### Schema.Defect for External Errors
```typescript
class ApiError extends Schema.TaggedError<ApiError>()("ApiError", {
  endpoint: Schema.String,
  cause: Schema.Defect, // wraps unknown errors
}) {}
```

---

## HTTP & Platform (`@effect/platform`)

### HttpClient
```typescript
import { HttpClient, HttpClientRequest, HttpClientResponse } from "@effect/platform"

const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  // Simple GET
  const response = yield* client.get("https://api.example.com/users")
  const users = yield* HttpClientResponse.schemaBodyJson(Schema.Array(User))(response)

  // POST with body
  const created = yield* client.post("https://api.example.com/users").pipe(
    HttpClientRequest.jsonBody({ name: "Alice" }),
    Effect.flatMap(HttpClientResponse.schemaBodyJson(User))
  )
})
```

### HttpApi Definition
```typescript
import { HttpApi, HttpApiGroup, HttpApiEndpoint } from "@effect/platform"

class UsersApi extends HttpApiGroup.make("users").pipe(
  HttpApiGroup.add(
    HttpApiEndpoint.get("list", "/users").pipe(
      HttpApiEndpoint.setSuccess(Schema.Array(User))
    )
  ),
  HttpApiGroup.add(
    HttpApiEndpoint.get("getById", "/users/:id").pipe(
      HttpApiEndpoint.setPath(Schema.Struct({ id: UserId })),
      HttpApiEndpoint.setSuccess(User),
      HttpApiEndpoint.addError(NotFoundError)
    )
  ),
  HttpApiGroup.add(
    HttpApiEndpoint.post("create", "/users").pipe(
      HttpApiEndpoint.setPayload(CreateUserRequest),
      HttpApiEndpoint.setSuccess(User)
    )
  )
) {}

class MyApi extends HttpApi.make("myApi").pipe(HttpApi.addGroup(UsersApi)) {}
```

### HttpApiClient
```typescript
import { HttpApiClient } from "@effect/platform"

const program = Effect.gen(function* () {
  const client = yield* HttpApiClient.make(MyApi)
  const users = yield* client.users.list()
  const user = yield* client.users.getById({ path: { id: "123" } })
})
```

### FileSystem
```typescript
import { FileSystem } from "@effect/platform"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const content = yield* fs.readFileString("./config.json")
  yield* fs.writeFileString("./output.txt", "Hello")
  const exists = yield* fs.exists("./file.txt")
  yield* fs.remove("./temp", { recursive: true })
})
```

### Command Execution
```typescript
import { Command, CommandExecutor } from "@effect/platform"

const program = Effect.gen(function* () {
  const executor = yield* CommandExecutor.CommandExecutor
  const output = yield* Command.make("git", "status").pipe(
    Command.string, // capture stdout as string
    executor.run
  )
})
```

---

## SQL & Database (`@effect/sql`)

### Model.Class
```typescript
import { Model } from "@effect/sql"

const UserId = Schema.Number.pipe(Schema.brand("UserId"))

class User extends Model.Class<User>("User")({
  id: Model.Generated(UserId),          // auto-generated, excluded from insert
  name: Schema.NonEmptyTrimmedString,
  email: Schema.String,
  createdAt: Model.DateTimeInsertFromDate, // auto-set on insert
  updatedAt: Model.DateTimeUpdateFromDate, // auto-set on update
}) {}

// Use variants:
// User.select - for SELECT queries
// User.insert - for INSERT (excludes Generated fields)
// User.update - for UPDATE (all fields optional)
```

### SqlClient Queries
```typescript
import { SqlClient } from "@effect/sql"

const program = Effect.gen(function* () {
  const sql = yield* SqlClient.SqlClient

  // Tagged template queries
  const users = yield* sql<User>`SELECT * FROM users WHERE active = ${true}`

  // With schema validation
  const user = yield* sql`SELECT * FROM users WHERE id = ${id}`.pipe(
    SqlSchema.findOne(User.select)
  )

  // Transactions
  yield* sql.withTransaction(Effect.gen(function* () {
    yield* sql`UPDATE accounts SET balance = balance - ${amount} WHERE id = ${from}`
    yield* sql`UPDATE accounts SET balance = balance + ${amount} WHERE id = ${to}`
  }))
})
```

### SqlSchema Helpers
```typescript
import { SqlSchema } from "@effect/sql"

// Returns Option<A> - for 0 or 1 result
const maybeUser = yield* sql`...`.pipe(SqlSchema.findOne(User))

// Returns A - throws if not exactly 1 result
const user = yield* sql`...`.pipe(SqlSchema.single(User))

// Returns Array<A>
const users = yield* sql`...`.pipe(SqlSchema.findAll(User))

// Returns void - for INSERT/UPDATE/DELETE
yield* sql`DELETE FROM users WHERE id = ${id}`.pipe(SqlSchema.void)
```

---

## RPC (`@effect/rpc`)

### Define RPCs
```typescript
import { Rpc, RpcGroup } from "@effect/rpc"

class GetUser extends Rpc.make("GetUser")<{
  success: User
  error: NotFoundError
  payload: { readonly id: UserId }
}>() {}

class CreateUser extends Rpc.make("CreateUser")<{
  success: User
  error: ValidationError
  payload: { readonly name: string; readonly email: string }
}>() {}

class UsersRpc extends RpcGroup.make("Users", GetUser, CreateUser) {}
```

### Implement Server
```typescript
import { RpcServer } from "@effect/rpc"

const usersHandler = RpcServer.make(UsersRpc).pipe(
  RpcServer.handler(GetUser, ({ id }) =>
    Effect.gen(function* () {
      const users = yield* Users
      return yield* users.findById(id)
    })
  ),
  RpcServer.handler(CreateUser, ({ name, email }) =>
    Effect.gen(function* () {
      const users = yield* Users
      return yield* users.create({ name, email })
    })
  )
)
```

### Use Client
```typescript
import { RpcClient } from "@effect/rpc"

const program = Effect.gen(function* () {
  const client = yield* RpcClient.make(UsersRpc)
  const user = yield* client(new GetUser({ id: UserId.make("123") }))
})
```

---

## CLI (`@effect/cli`)

### Command Definition
```typescript
import { Args, Command, Options } from "@effect/cli"

const name = Args.text({ name: "name" })
const verbose = Options.boolean("verbose").pipe(Options.withAlias("v"))
const count = Options.integer("count").pipe(Options.withDefault(1))

const greet = Command.make("greet", { name, verbose, count }, ({ name, verbose, count }) =>
  Effect.gen(function* () {
    for (let i = 0; i < count; i++) {
      yield* Effect.logInfo(`Hello, ${name}!`)
    }
    if (verbose) yield* Effect.logDebug("Greeting complete")
  })
)
```

### Subcommands
```typescript
const add = Command.make("add", { file: Args.file() }, ({ file }) => /* ... */)
const remove = Command.make("remove", { file: Args.file() }, ({ file }) => /* ... */)

const cli = Command.make("mycli").pipe(
  Command.withSubcommands([add, remove])
)
```

### Run CLI
```typescript
import { CliApp } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"

const app = CliApp.make({ name: "mycli", version: "1.0.0", command: cli })
CliApp.run(app, process.argv).pipe(Effect.provide(NodeContext.layer), NodeRuntime.runMain)
```

---

## AI Integration (`@effect/ai`)

### LanguageModel
```typescript
import { LanguageModel } from "@effect/ai"
import { OpenAiLanguageModel } from "@effect/ai-openai"

const program = Effect.gen(function* () {
  const model = yield* LanguageModel.LanguageModel

  // Text generation
  const response = yield* model.generateText({
    prompt: "Explain monads in one sentence"
  })

  // Structured output
  const user = yield* model.generateObject({
    prompt: "Generate a fake user",
    schema: User
  })

  // Streaming
  const stream = model.streamText({ prompt: "Write a poem" })
  yield* Stream.runForEach(stream, (chunk) => Effect.logInfo(chunk.text))
})

// Provide OpenAI implementation
program.pipe(Effect.provide(OpenAiLanguageModel.layer({ model: "gpt-4o" })))
```

### Tool Definitions
```typescript
import { Tool, Toolkit } from "@effect/ai"

const weatherTool = Tool.make("getWeather", {
  description: "Get current weather for a location",
  parameters: Schema.Struct({ city: Schema.String }),
  success: Schema.Struct({ temp: Schema.Number, conditions: Schema.String }),
})

const toolkit = Toolkit.make(weatherTool)

const toolkitLayer = Toolkit.toLayer(toolkit, {
  getWeather: ({ city }) =>
    Effect.succeed({ temp: 72, conditions: "sunny" })
})
```

---

## Reactive State (`@effect-atom/atom`)

### Basic Atoms
```typescript
import { Atom, Registry } from "@effect-atom/atom"

// Writable atom
const countAtom = Atom.make(0)

// Derived atom
const doubledAtom = Atom.make((get) => get(countAtom) * 2)

// Async atom (returns Result<A, E>)
const userAtom = Atom.make(fetchUser(userId))

// From Stream
const messagesAtom = Atom.make(messageStream)
```

### Atom.family for Parameterized State
```typescript
const userAtom = Atom.family((id: UserId) =>
  Atom.make(fetchUser(id))
)

// Usage - stable references
const alice = userAtom("alice")
const bob = userAtom("bob")
```

### Atom.fn for Actions
```typescript
const submitForm = Atom.fn((data: FormData) =>
  Effect.gen(function* () {
    const api = yield* Api
    return yield* api.submit(data)
  })
)

// Returns AtomResultFn - tracks loading/success/failure
```

### Result Type
```typescript
import { Result } from "@effect-atom/atom"

// Result<A, E> = Initial | Success<A> | Failure<E>
// All states can have `waiting: true` for refetching

Result.match(result, {
  onInitial: () => "Loading...",
  onSuccess: ({ value }) => `Got: ${value}`,
  onFailure: ({ cause }) => `Error: ${Cause.pretty(cause)}`,
})

// Check waiting state
if (Result.isWaiting(result)) showSpinner()
```

### React Integration
```typescript
import { useAtomValue, useAtom, useAtomSet } from "@effect-atom/atom-react"

function Counter() {
  const count = useAtomValue(countAtom)
  const setCount = useAtomSet(countAtom)
  // or: const [count, setCount] = useAtom(countAtom)

  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>
}

// For Result atoms
function UserProfile({ id }: { id: UserId }) {
  const result = useAtomValue(userAtom(id))

  return Result.match(result, {
    onInitial: () => <Spinner />,
    onSuccess: ({ value }) => <Profile user={value} />,
    onFailure: ({ cause }) => <Error cause={cause} />,
  })
}
```

### Service Integration
```typescript
// Create runtime atom from Layer
const runtimeAtom = Atom.runtime(ApiClient.layer)

// Use services in atoms
const dataAtom = Atom.make(
  Effect.gen(function* () {
    const api = yield* ApiClient
    return yield* api.fetchData()
  })
)
```

---

## Testing (`@effect/vitest`)

### Basic Setup
```typescript
import { Effect } from "effect"
import { describe, expect, it } from "@effect/vitest"

describe("Feature", () => {
  it.effect("works", () =>
    Effect.gen(function* () {
      const result = yield* Effect.succeed(42)
      expect(result).toBe(42)
    })
  )
})
```

### Test Variants
| Variant | Description |
|---------|-------------|
| `it.effect` | Standard Effect tests with TestServices |
| `it.scoped` | Auto resource cleanup via Scope |
| `it.live` | Real clock/random (no TestClock) |
| `it.scopedLive` | Scoped + real services |

### Shared Layers with `layer()`
```typescript
import { layer } from "@effect/vitest"

layer(Database.testLayer)("Database tests", (it) => {
  it.effect("queries work", () =>
    Effect.gen(function* () {
      const db = yield* Database
      const result = yield* db.query("SELECT 1")
      expect(result).toHaveLength(1)
    })
  )
})
```

### TestClock
```typescript
import { Effect, Fiber, TestClock } from "effect"

it.effect("time-based", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.sleep("10 seconds").pipe(
      Effect.as("done"),
      Effect.fork
    )
    yield* TestClock.adjust("10 seconds")
    const result = yield* Fiber.join(fiber)
    expect(result).toBe("done")
  })
)
```

### Property-Based Testing
```typescript
it.prop("addition is commutative", [Schema.Int, Schema.Int], (a, b) =>
  Effect.gen(function* () {
    expect(a + b).toBe(b + a)
  })
)
```

---

## Anti-Patterns

### Avoid
- Mixing `Effect.provide` throughout code (provide once at entry)
- Using raw `try/catch` instead of Effect error handling
- Creating layers inline multiple times (breaks memoization)
- Using `Effect.runSync/runPromise` deep in the call stack
- Ignoring typed errors with `Effect.orDie` when recovery is possible
- Using `Effect.promise` for external APIs (loses error typing)
- Not validating external data with `Schema.decodeUnknown`
- Forgetting `Result.isWaiting` checks in UI (shows stale data during refetch)

### Prefer
- `Effect.fn` over plain functions returning Effects
- `Schema.TaggedError` over plain Error classes
- Branded types over raw primitives
- Services/Layers over global singletons
- `yield*` over `.pipe(Effect.flatMap(...))` for sequential code
- `Schema.decodeUnknown` for all external/untrusted data
- `HttpApiClient` over manual HTTP calls for typed APIs
- `Model.Class` over plain Schema.Class for database entities
