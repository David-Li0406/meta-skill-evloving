# Reqon DSL Syntax Reference

## Mission Structure

```
mission MissionName {
  // Sources (API connections)
  source SourceName { ... }

  // Stores (data persistence)
  store storeName: type("identifier")

  // Schemas (type definitions)
  schema SchemaName { ... }

  // Actions (pipeline steps)
  action ActionName { ... }

  // Pipeline execution
  run ActionA then ActionB
}
```

## Sources

### Authentication Types

```
// Bearer token (from env var)
source API {
  auth: bearer,
  base: "https://api.example.com",
  headers: { "Accept": "application/json" }
}

// API key
source API {
  auth: api_key,
  base: "https://api.example.com"
}

// Basic auth
source API {
  auth: basic,
  base: "https://api.example.com"
}

// OAuth2
source API {
  auth: oauth2,
  base: "https://api.example.com",
  oauth: {
    tokenUrl: "https://auth.example.com/token",
    clientId: env("CLIENT_ID"),
    clientSecret: env("CLIENT_SECRET"),
    scopes: ["read", "write"]
  }
}
```

### Rate Limiting

```
source API {
  auth: bearer,
  base: "https://api.example.com",
  rateLimit: {
    strategy: "pause",    // or "queue"
    maxWait: 60,          // seconds
    fallbackRpm: 60       // requests per minute fallback
  }
}
```

## Stores

```
store items: memory("items")           // In-memory
store items: file("./data/items.json") // File-based
store items: sql("items_table")        // SQL database (stubs to file in dev)
store items: postgrest("items_table")  // PostgREST/Supabase
```

## Schemas

```
schema User {
  id: int,
  name: string,
  email: string?,       // Optional field
  created_at: date,
  tags: array,
  metadata: object
}
```

Supported types: `int`, `string`, `boolean`, `decimal`, `date`, `array`, `object`

## HTTP Operations

### Basic Fetch

```
get "/users"
post "/users" { body: { "name": "John" } }
put "/users/{id}" { body: { "name": "Jane" } }
delete "/users/{id}"
```

### Full Options

```
get "/users" {
  source: APISource,
  body: { "status": "active" },
  headers: { "X-Custom": "value" },

  // Pagination
  paginate: page(page, 100),           // Page-based
  paginate: cursor(.next_cursor),      // Cursor-based
  paginate: offset(offset, 50),        // Offset-based

  until: length(response) == 0,        // Stop condition

  // Retry configuration
  retry: {
    maxAttempts: 3,
    backoff: "exponential",  // or "constant", "linear"
    initialDelay: 1000,      // ms
    maxDelay: 60000          // ms
  },

  // Incremental sync
  since: lastSync
}
```

## Pattern Matching

```
match response {
  // Match array of schema type
  [UserSchema] -> { store response -> users { key: .id } },

  // Match single schema type
  ErrorSchema -> abort "API error",

  // Match with condition
  _ where .status == "rate_limited" -> retry { maxAttempts: 3 },

  // Wildcard
  _ -> skip
}
```

## Loops and Iteration

```
// Basic loop
for user in users {
  // process each user
}

// Loop with filter
for user in users where .active == true {
  // process only active users
}

// Loop with complex filter
for item in items where .status == "pending" and .priority > 5 {
  // process filtered items
}
```

## Mapping

```
map input -> OutputSchema {
  id: .id,
  fullName: .firstName + " " + .lastName,
  status: match .state {
    "active" => "enabled",
    "inactive" => "disabled",
    _ => "unknown"
  },
  createdAt: .created_at,
  tags: .labels
}
```

## Validation

```
validate response {
  assume length(.name) > 0
  assume .age >= 0
  assume .email contains "@"
}
```

## Store Operations

```
// Basic store
store response -> items { key: .id }

// Upsert mode
store response -> items { key: .id, upsert: true }

// Partial update
store response -> items { key: .id, partial: true }
```

## Pipeline Execution

```
// Sequential
run ActionA then ActionB then ActionC

// Parallel then sequential
run [ActionA, ActionB] then ActionC

// Multiple parallel groups
run [ActionA, ActionB] then [ActionC, ActionD] then ActionE
```

## Flow Control Directives

| Directive | Description |
|-----------|-------------|
| `continue` | Proceed to next step |
| `skip` | Skip current loop item |
| `abort "msg"` | Stop mission with error |
| `retry {...}` | Retry current operation |
| `queue storeName` | Send to dead letter queue |
| `jump ActionName then retry` | Execute action then retry |

## Built-in Functions

- `length(array)` - Array length
- `now()` - Current timestamp
- `env("VAR_NAME")` - Environment variable
- `exists(store[key])` - Check if key exists in store

## Expressions

```
// Arithmetic
.price * .quantity
.total + .tax

// String concatenation
.firstName + " " + .lastName
"prefix_" + .id

// Comparisons
.age >= 18
.status == "active"
.count > 0 and .count < 100

// Property access
.user.name
.items[0].id
```

## Webhook/Callback Waiting

```
wait {
  timeout: 60000,                           // Required: ms to wait
  path: "/webhooks/callback",               // Optional: specific path
  expectedEvents: 3,                        // Optional: wait for N events
  eventFilter: .type == "payment.completed", // Optional: filter events
  storage: {
    target: events_store,
    key: .id
  },
  retry: {
    maxAttempts: 3,
    backoff: exponential,
    initialDelay: 1000
  }
}
```

## Scheduling

```
// Interval-based
schedule: every 6 hours
schedule: every 30 minutes
schedule: every 1 days

// Cron-based
schedule: cron "0 */6 * * *"
schedule: cron "30 9 * * 1-5"

// One-time
schedule: at "2025-01-25T15:00:00Z"

// With options
schedule: every 6 hours {
  timezone: "America/New_York",
  maxConcurrency: 1,
  skipIfRunning: true,
  retry: {
    maxRetries: 3,
    delaySeconds: 60
  }
}
```
