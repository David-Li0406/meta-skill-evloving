---
name: rust-async-patterns
description: Use this skill when building async Rust applications, implementing concurrent systems, or debugging async code with Tokio and async traits.
---

# Skill body

## When to Use This Skill

- Building async Rust applications
- Implementing concurrent network services
- Using Tokio for async I/O
- Handling async errors properly
- Debugging async code issues
- Optimizing async performance

## Core Concepts

### 1. Async Execution Model

```
Future (lazy) → poll() → Ready(value) | Pending
                ↑           ↓
              Waker ← Runtime schedules
```

### 2. Key Abstractions

| Concept    | Purpose                                  |
|------------|------------------------------------------|
| `Future`   | Lazy computation that may complete later |
| `async fn` | Function returning impl Future           |
| `await`    | Suspend until future completes           |
| `Task`     | Spawned future running concurrently      |
| `Runtime`  | Executor that polls futures              |

## Quick Start

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
futures = "0.3"
async-trait = "0.1"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = "0.3"
```

```rust
use tokio::time::{sleep, Duration};
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    // Async operations
    let result = fetch_data("https://api.example.com").await?;
    println!("Got: {}", result);

    Ok(())
}

async fn fetch_data(url: &str) -> Result<String> {
    // Simulated async operation
    sleep(Duration::from_millis(100)).await;
    Ok(format!("Data from {}", url))
}
```

## Patterns

### Pattern 1: Concurrent Task Execution

```rust
use tokio::task::JoinSet;
use anyhow::Result;

// Spawn multiple concurrent tasks
async fn fetch_all_concurrent(urls: Vec<String>) -> Result<Vec<String>> {
    let mut set = JoinSet::new();

    for url in urls {
        set.spawn(async move {
            fetch_data(&url).await
        });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        match res {
            Ok(Ok(data)) => results.push(data),
            Ok(Err(e)) => tracing::error!("Task failed: {}", e),
        }
    }
    Ok(results)
}
```