---
name: Tokio Runtime
description: Async runtime for Rust with task scheduling, I/O, and timers.
metadata:
  labels: [rust, tokio, async, runtime]
  triggers:
    files: ['**/main.rs', '**/lib.rs']
    keywords: [tokio, spawn, select, async, await]
---

# Tokio Runtime Standards

## Runtime Setup

```rust
// Full runtime with all features
#[tokio::main]
async fn main() {
    // Your async code
}

// Custom runtime configuration
#[tokio::main(flavor = "multi_thread", worker_threads = 4)]
async fn main() { }

// Current-thread runtime (single-threaded)
#[tokio::main(flavor = "current_thread")]
async fn main() { }
```

## Task Spawning

```rust
use tokio::task;

// Spawn async task
let handle = tokio::spawn(async {
    // Background work
    expensive_computation().await
});

// Wait for result
let result = handle.await?;

// Spawn blocking task (CPU-bound work)
let result = task::spawn_blocking(|| {
    // Blocking/CPU-intensive code
    compute_hash(data)
}).await?;

// Detached task (fire and forget)
tokio::spawn(async {
    log_event(event).await;
});
```

## Concurrency Patterns

```rust
use tokio::{select, join, time};

// Run multiple futures concurrently
let (a, b, c) = join!(task_a(), task_b(), task_c());

// Race futures, cancel losers
select! {
    result = fetch_primary() => handle_primary(result),
    result = fetch_backup() => handle_backup(result),
    _ = time::sleep(Duration::from_secs(5)) => timeout_error(),
}

// Timeout wrapper
let result = time::timeout(
    Duration::from_secs(30),
    long_running_task()
).await?;
```

## Synchronization

```rust
use tokio::sync::{Mutex, RwLock, mpsc, broadcast, oneshot};

// Async mutex (allows holding across await)
let data = Arc::new(Mutex::new(vec![]));
{
    let mut guard = data.lock().await;
    guard.push(item);
}

// RwLock for read-heavy workloads
let cache = Arc::new(RwLock::new(HashMap::new()));
let value = cache.read().await.get(&key);

// Channels
let (tx, mut rx) = mpsc::channel(100);
tx.send(message).await?;
while let Some(msg) = rx.recv().await {
    process(msg);
}

// Oneshot for single response
let (tx, rx) = oneshot::channel();
tokio::spawn(async move { tx.send(result) });
let response = rx.await?;
```

## I/O Operations

```rust
use tokio::{fs, io::{AsyncReadExt, AsyncWriteExt}, net::TcpListener};

// File I/O
let content = fs::read_to_string("file.txt").await?;
fs::write("output.txt", data).await?;

// TCP server
let listener = TcpListener::bind("127.0.0.1:8080").await?;
loop {
    let (socket, _) = listener.accept().await?;
    tokio::spawn(handle_connection(socket));
}

// Buffered I/O
use tokio::io::{BufReader, BufWriter};
let reader = BufReader::new(file);
let mut lines = reader.lines();
while let Some(line) = lines.next_line().await? {
    process(line);
}
```

## Graceful Shutdown

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("Failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("Failed to install SIGTERM handler")
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

## Best Practices

1. **Never block**: Use `spawn_blocking` for CPU-bound or blocking I/O
2. **Channel sizing**: Size mpsc channels appropriately to avoid backpressure
3. **Error propagation**: Use `JoinHandle::await?` to propagate panics
4. **Timeouts**: Always add timeouts to network operations
5. **Tracing**: Use `tokio-console` for debugging async issues
