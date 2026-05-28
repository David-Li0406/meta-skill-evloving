# Reqon Examples

## Simple API Sync

```
mission SyncUsers {
  source API {
    auth: bearer,
    base: "https://api.example.com"
  }

  store users: memory("users")

  action FetchUsers {
    get "/users" {
      paginate: page(page, 50),
      until: length(response) == 0
    }
    store response -> users { key: .id }
  }

  run FetchUsers
}
```

## Multi-File Mission Structure

```
project/
├── mission.vague        # Main: sources, stores, schemas, pipeline
├── fetch-data.vague     # Action: FetchData
├── transform.vague      # Action: Transform
└── validate.vague       # Action: Validate
```

Actions in separate files are automatically merged into the mission.

## Error Handling with Match

```
action FetchWithErrorHandling {
  get "/data"

  match response {
    [DataSchema] -> {
      store response -> data { key: .id }
    },

    RateLimitError -> retry {
      maxAttempts: 5,
      backoff: exponential,
      initialDelay: 60000
    },

    AuthError -> jump RefreshToken then retry,

    NotFoundError -> abort "Resource not found",

    _ -> {
      store {
        error: "Unexpected response",
        response: response,
        timestamp: now()
      } -> errors { key: now() }
    }
  }
}
```

## Data Transformation Pipeline

```
action TransformData {
  for item in raw_items {
    map item -> NormalizedItem {
      id: "item_" + .id,
      title: .name,
      description: .body,
      status: match .state {
        "open" => "active",
        "closed" => "completed",
        _ => "unknown"
      },
      author: .user.login,
      created_at: .created_at,
      synced_at: now()
    }

    validate response {
      assume length(.title) > 0
      assume .id != null
    }

    store response -> normalized_items {
      key: .id,
      upsert: true
    }
  }
}
```

## Parallel Execution

```
mission ParallelSync {
  source GitHubAPI { auth: bearer, base: "https://api.github.com" }

  store issues: memory("issues")
  store prs: memory("prs")
  store work_items: memory("work_items")

  action FetchIssues {
    get "/repos/{owner}/{repo}/issues"
    store response -> issues { key: .id }
  }

  action FetchPRs {
    get "/repos/{owner}/{repo}/pulls"
    store response -> prs { key: .id }
  }

  action Normalize {
    // Process both issues and PRs after parallel fetch
    for issue in issues { ... }
    for pr in prs { ... }
  }

  // FetchIssues and FetchPRs run in parallel, then Normalize
  run [FetchIssues, FetchPRs] then Normalize
}
```

## Incremental Sync

```
action IncrementalFetch {
  get "/items" {
    body: { "updated_after": lastSync },
    since: lastSync
  }
  store response -> items { key: .id, upsert: true }
}
```

## Dead Letter Queue Pattern

```
action ProcessWithDLQ {
  for item in pending {
    post "/process/{item.id}"

    match response {
      SuccessSchema -> {
        store response -> completed { key: .id }
      },

      TransientError -> retry {
        maxAttempts: 3,
        backoff: exponential,
        initialDelay: 1000
      },

      // After retries exhausted or permanent error, queue for later
      _ -> queue dead_letter_queue
    }
  }
}
```

## Conditional Processing

```
action ProcessConditionally {
  for payment in pending_payments
    where not exists(fraud_queue[payment.id]) {

    post "/payments/{payment.id}/capture"

    match response {
      PaymentSuccess -> {
        store response -> completed { key: .id }
      },
      _ -> skip
    }
  }
}
```

## OpenAPI Integration

```
mission OpenAPIExample {
  source API from "./openapi.yaml" {
    auth: bearer,
    base: "https://api.example.com"
  }

  action FetchUsers {
    // Use operation ID from OpenAPI spec
    call API.listUsers { query: { limit: 100 } }
    store response -> users { key: .id }
  }

  run FetchUsers
}
```

## Webhook/Callback Workflow

```
mission PaymentWorkflow {
  source API { auth: bearer, base: "https://api.example.com" }
  store orders: memory("orders")
  store payments: memory("payments")

  action ProcessOrder {
    post "/orders" {
      body: { item: "test" }
    }

    // Wait for payment webhook callback
    wait {
      timeout: 300000,
      path: "/webhooks/payment",
      eventFilter: .status == "completed",
      storage: {
        target: payments,
        key: .order_id
      }
    }

    store response -> orders { key: .id }
  }

  run ProcessOrder
}
```

## Scheduled Mission

```
mission DailySyncWithSchedule {
  schedule: cron "0 9 * * 1-5" {
    timezone: "Europe/London",
    skipIfRunning: true,
    retry: { maxRetries: 3, delaySeconds: 60 }
  }

  source API { auth: bearer, base: "https://api.example.com" }
  store data: memory("data")

  action Sync {
    get "/data" { since: lastSync }
    store response -> data { key: .id, upsert: true }
  }

  run Sync
}
```
