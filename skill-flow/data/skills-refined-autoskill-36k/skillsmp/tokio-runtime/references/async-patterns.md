# Tokio Async Patterns

## Task Spawning

```rust
use tokio::task;

// Spawn background task
let handle = tokio::spawn(async {
    expensive_computation().await
});

// Wait for result
let result = handle.await?;

// Spawn blocking (for CPU-bound or sync code)
let result = task::spawn_blocking(|| {
    std::thread::sleep(Duration::from_secs(1));
    "done"
}).await?;
```

## Concurrent Execution

```rust
use tokio::join;
use futures::future::join_all;

// Run multiple futures concurrently
let (user, orders, prefs) = tokio::join!(
    fetch_user(id),
    fetch_orders(id),
    fetch_preferences(id),
);

// Run collection of futures
let futures = ids.iter().map(|id| fetch_user(*id));
let users: Vec<User> = join_all(futures).await;

// Try join - fail fast on first error
let (user, orders) = tokio::try_join!(
    fetch_user(id),
    fetch_orders(id),
)?;
```

## Select and Racing

```rust
use tokio::{select, time::timeout};

// Race multiple futures
select! {
    result = fetch_from_primary() => {
        println!("Primary: {:?}", result);
    }
    result = fetch_from_backup() => {
        println!("Backup: {:?}", result);
    }
}

// Timeout
match timeout(Duration::from_secs(5), long_operation()).await {
    Ok(result) => println!("Completed: {:?}", result),
    Err(_) => println!("Timed out"),
}

// Select with cancellation
let mut interval = tokio::time::interval(Duration::from_secs(1));
loop {
    select! {
        _ = interval.tick() => {
            println!("tick");
        }
        _ = shutdown_signal() => {
            println!("shutting down");
            break;
        }
    }
}
```

## Channels

```rust
use tokio::sync::{mpsc, oneshot, broadcast};

// MPSC - multiple producers, single consumer
let (tx, mut rx) = mpsc::channel(100);

tokio::spawn(async move {
    tx.send("hello").await.unwrap();
});

while let Some(msg) = rx.recv().await {
    println!("Got: {}", msg);
}

// Oneshot - single value
let (tx, rx) = oneshot::channel();
tx.send("value").unwrap();
let value = rx.await?;

// Broadcast - multiple consumers
let (tx, _) = broadcast::channel(16);
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();
tx.send("broadcast")?;
```

## Graceful Shutdown

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("failed to listen for ctrl+c");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to listen for terminate")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}
```
