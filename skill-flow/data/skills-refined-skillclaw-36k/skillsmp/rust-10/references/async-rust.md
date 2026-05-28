# Async Rust Patterns

Effective async/await patterns with Tokio.

## Basic Async Pattern

```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data("https://api.example.com").await;
    println!("{:?}", result);
}

async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    response.text().await
}
```

## Concurrent Execution

### join! - Run concurrently, wait for all

```rust
use tokio::join;

async fn main() {
    let (users, posts) = join!(
        fetch_users(),
        fetch_posts()
    );
}
```

### select! - Race multiple futures

```rust
use tokio::select;
use tokio::time::{sleep, Duration};

async fn with_timeout() -> Result<Data, Error> {
    select! {
        result = fetch_data() => result,
        _ = sleep(Duration::from_secs(5)) => Err(Error::Timeout),
    }
}
```

### Spawning Tasks

```rust
use tokio::task;

async fn process_many(items: Vec<Item>) -> Vec<Result<Output, Error>> {
    let handles: Vec<_> = items
        .into_iter()
        .map(|item| {
            task::spawn(async move {
                process_item(item).await
            })
        })
        .collect();

    let mut results = Vec::new();
    for handle in handles {
        results.push(handle.await.unwrap());
    }
    results
}
```

## Streams

```rust
use futures::stream::{self, StreamExt};

async fn process_stream() {
    let items = vec![1, 2, 3, 4, 5];

    stream::iter(items)
        .map(|n| async move { fetch_item(n).await })
        .buffer_unordered(3)  // Max 3 concurrent
        .for_each(|result| async {
            println!("{:?}", result);
        })
        .await;
}
```

## Cancellation with Timeouts

```rust
use tokio::time::{timeout, Duration};

async fn with_timeout<T, F: Future<Output = T>>(
    duration: Duration,
    future: F,
) -> Result<T, tokio::time::error::Elapsed> {
    timeout(duration, future).await
}

// Usage
match with_timeout(Duration::from_secs(5), slow_operation()).await {
    Ok(result) => println!("Got result: {:?}", result),
    Err(_) => println!("Operation timed out"),
}
```

## Channels

### mpsc - Multiple producers, single consumer

```rust
use tokio::sync::mpsc;

async fn channel_example() {
    let (tx, mut rx) = mpsc::channel(100);

    // Spawn producers
    for i in 0..3 {
        let tx = tx.clone();
        tokio::spawn(async move {
            tx.send(format!("Message from {}", i)).await.unwrap();
        });
    }
    drop(tx);  // Close when done

    // Receive
    while let Some(message) = rx.recv().await {
        println!("{}", message);
    }
}
```

### broadcast - Multiple consumers

```rust
use tokio::sync::broadcast;

async fn broadcast_example() {
    let (tx, _) = broadcast::channel(100);

    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();

    tokio::spawn(async move {
        while let Ok(msg) = rx1.recv().await {
            println!("rx1: {}", msg);
        }
    });

    tx.send("hello").unwrap();
}
```

## Shared State

```rust
use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Clone)]
struct AppState {
    counter: Arc<Mutex<u64>>,
}

async fn increment(state: AppState) {
    let mut counter = state.counter.lock().await;
    *counter += 1;
}
```

## Common Anti-Patterns

```rust
// ❌ Holding lock across await
async fn bad(state: Arc<Mutex<Data>>) {
    let data = state.lock().await;
    slow_operation().await;  // Lock held during await!
    println!("{:?}", data);
}

// ✅ Release lock before await
async fn good(state: Arc<Mutex<Data>>) {
    let value = {
        let data = state.lock().await;
        data.clone()
    };  // Lock released
    slow_operation().await;
    println!("{:?}", value);
}

// ❌ Blocking in async context
async fn bad() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks runtime!
}

// ✅ Use async sleep
async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// ❌ spawn_blocking for async work
let result = tokio::task::spawn_blocking(|| {
    some_async_function()  // Wrong!
}).await;

// ✅ spawn_blocking for CPU-bound work
let result = tokio::task::spawn_blocking(|| {
    expensive_computation()
}).await;
```

## Error Handling in Async

```rust
use anyhow::{Context, Result};

async fn fetch_user(id: u64) -> Result<User> {
    let response = reqwest::get(format!("/users/{}", id))
        .await
        .context("Failed to fetch user")?;

    if !response.status().is_success() {
        anyhow::bail!("User not found: {}", id);
    }

    response
        .json()
        .await
        .context("Failed to parse user JSON")
}
```
