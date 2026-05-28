# Async Patterns in Rust

Comprehensive guide to asynchronous programming in Rust using Tokio and async/await.

## Async Basics

### Async Functions

```rust
async fn fetch_data(url: &str) -> Result<String, Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// Calling async function
#[tokio::main]
async fn main() {
    let data = fetch_data("https://example.com").await.unwrap();
    println!("{}", data);
}
```

### Async Blocks

```rust
let future = async {
    let data = fetch_data("https://example.com").await?;
    process_data(&data).await
};

let result = future.await?;
```

### Async Closures

```rust
let fetch = |url: &str| async move {
    reqwest::get(url).await?.text().await
};

let data = fetch("https://example.com").await?;
```

## Tokio Runtime

### Runtime Flavors

```rust
// Multi-threaded runtime (default)
#[tokio::main]
async fn main() {
    // Your async code
}

// Equivalent to:
fn main() {
    tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(async {
            // Your async code
        })
}

// Single-threaded runtime
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Your async code
}

// Custom runtime
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .thread_name("my-worker")
        .enable_all()
        .build()
        .unwrap();

    runtime.block_on(async {
        // Your async code
    });
}
```

### Spawning Tasks

```rust
use tokio::task;

// Spawn a task
let handle = task::spawn(async {
    // Async work
    fetch_data("https://example.com").await
});

// Wait for result
let result = handle.await??;

// Spawn multiple tasks
let handles: Vec<_> = urls
    .iter()
    .map(|url| {
        let url = url.clone();
        task::spawn(async move {
            fetch_data(&url).await
        })
    })
    .collect();

// Wait for all
for handle in handles {
    let data = handle.await??;
    process(data);
}
```

### Blocking Code in Async

```rust
use tokio::task;

// Bad: Blocks the async runtime
async fn bad_example() {
    std::thread::sleep(Duration::from_secs(1));  // Don't do this!
}

// Good: Use spawn_blocking
async fn good_example() {
    task::spawn_blocking(|| {
        // Blocking operation
        std::thread::sleep(Duration::from_secs(1));
        expensive_computation()
    })
    .await
    .unwrap()
}

// CPU-intensive work
async fn process_data() {
    let result = task::spawn_blocking(|| {
        // Runs on blocking thread pool
        heavy_computation()
    })
    .await
    .unwrap();
}
```

## Concurrent Operations

### Join Multiple Futures

```rust
use tokio::join;

// Wait for all futures
let (result1, result2, result3) = join!(
    fetch_data("url1"),
    fetch_data("url2"),
    fetch_data("url3"),
);

// With error handling
async fn fetch_all() -> Result<(), Error> {
    let (r1, r2, r3) = join!(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    );

    let data1 = r1?;
    let data2 = r2?;
    let data3 = r3?;

    Ok(())
}
```

### Select First Completed

```rust
use tokio::select;

async fn race() {
    select! {
        result = fetch_from_cache() => {
            println!("Got from cache: {:?}", result);
        }
        result = fetch_from_db() => {
            println!("Got from DB: {:?}", result);
        }
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            println!("Timeout!");
        }
    }
}

// Biased selection (checks in order)
select! {
    biased;
    result = high_priority() => { /* ... */ }
    result = low_priority() => { /* ... */ }
}
```

### Try Join (Fail Fast)

```rust
use tokio::try_join;

async fn fetch_all() -> Result<(), Error> {
    let (data1, data2, data3) = try_join!(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )?;

    // All succeeded
    Ok(())
}
```

## Async Traits

### Using async-trait

```rust
use async_trait::async_trait;

#[async_trait]
pub trait DataSource {
    async fn fetch(&self, id: u64) -> Result<Data, Error>;
    async fn save(&self, data: Data) -> Result<(), Error>;
}

#[async_trait]
impl DataSource for Database {
    async fn fetch(&self, id: u64) -> Result<Data, Error> {
        let data = sqlx::query_as("SELECT * FROM data WHERE id = $1")
            .bind(id)
            .fetch_one(&self.pool)
            .await?;
        Ok(data)
    }

    async fn save(&self, data: Data) -> Result<(), Error> {
        sqlx::query("INSERT INTO data VALUES ($1, $2)")
            .bind(data.id)
            .bind(data.value)
            .execute(&self.pool)
            .await?;
        Ok(())
    }
}
```

### Native Async Traits (Rust 1.75+)

```rust
// Return Position Impl Trait in Trait (RPITIT)
trait DataSource {
    async fn fetch(&self, id: u64) -> Result<Data, Error>;
}

// Equivalent to:
trait DataSource {
    fn fetch(&self, id: u64) -> impl Future<Output = Result<Data, Error>> + '_;
}
```

## Streams

### Creating Streams

```rust
use tokio_stream::{StreamExt, Stream};

// From iterator
let stream = tokio_stream::iter(vec![1, 2, 3, 4, 5]);

// Manual stream
use async_stream::stream;

fn fibonacci() -> impl Stream<Item = u64> {
    stream! {
        let (mut a, mut b) = (0u64, 1u64);
        loop {
            yield a;
            (a, b) = (b, a + b);
        }
    }
}
```

### Processing Streams

```rust
use tokio_stream::StreamExt;

async fn process_stream() {
    let mut stream = fetch_stream();

    // Iterate
    while let Some(item) = stream.next().await {
        process(item);
    }

    // Map
    let mapped = stream.map(|x| x * 2);

    // Filter
    let filtered = stream.filter(|x| x % 2 == 0);

    // Collect
    let vec: Vec<_> = stream.collect().await;

    // Fold
    let sum = stream.fold(0, |acc, x| acc + x).await;
}
```

### Chunking and Buffering

```rust
use tokio_stream::StreamExt;

async fn buffered_processing() {
    let stream = fetch_stream();

    // Process in chunks
    let mut chunks = stream.chunks(10);
    while let Some(chunk) = chunks.next().await {
        process_batch(chunk).await;
    }

    // Buffer futures
    let results = stream
        .map(|item| async move { process(item).await })
        .buffered(10)  // Process up to 10 concurrently
        .collect::<Vec<_>>()
        .await;
}
```

## Channels

### MPSC (Multi-Producer, Single-Consumer)

```rust
use tokio::sync::mpsc;

async fn mpsc_example() {
    let (tx, mut rx) = mpsc::channel(32);  // Buffered

    // Producer
    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
        }
    });

    // Consumer
    while let Some(value) = rx.recv().await {
        println!("Got: {}", value);
    }
}

// Unbounded channel
let (tx, mut rx) = mpsc::unbounded_channel();
tx.send(1).unwrap();  // Never blocks
```

### Broadcast

```rust
use tokio::sync::broadcast;

async fn broadcast_example() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();

    // Send to all subscribers
    tx.send("message").unwrap();

    // Both receivers get it
    assert_eq!(rx1.recv().await.unwrap(), "message");
    assert_eq!(rx2.recv().await.unwrap(), "message");
}
```

### Watch (Single-Producer, Multi-Consumer)

```rust
use tokio::sync::watch;

async fn watch_example() {
    let (tx, mut rx) = watch::channel("initial");

    tokio::spawn(async move {
        // Watch for changes
        while rx.changed().await.is_ok() {
            println!("New value: {}", *rx.borrow());
        }
    });

    // Update value
    tx.send("updated").unwrap();
}
```

### Oneshot

```rust
use tokio::sync::oneshot;

async fn oneshot_example() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        let result = expensive_operation().await;
        tx.send(result).unwrap();
    });

    // Wait for result
    let result = rx.await.unwrap();
}
```

## Synchronization Primitives

### Mutex

```rust
use tokio::sync::Mutex;

let data = Arc::new(Mutex::new(0));

// Multiple tasks can access
let data_clone = data.clone();
tokio::spawn(async move {
    let mut guard = data_clone.lock().await;
    *guard += 1;
});

// No deadlocks across await points
let mut guard = data.lock().await;
some_async_function().await;  // Lock is held
*guard += 1;
```

### RwLock

```rust
use tokio::sync::RwLock;

let data = Arc::new(RwLock::new(HashMap::new()));

// Multiple readers
let read_guard = data.read().await;
let value = read_guard.get(&key);

// Exclusive writer
let mut write_guard = data.write().await;
write_guard.insert(key, value);
```

### Semaphore

```rust
use tokio::sync::Semaphore;

let semaphore = Arc::new(Semaphore::new(3));  // Max 3 concurrent

for i in 0..10 {
    let permit = semaphore.clone().acquire_owned().await.unwrap();
    tokio::spawn(async move {
        // Only 3 tasks run concurrently
        expensive_operation(i).await;
        drop(permit);  // Release
    });
}
```

### Barrier

```rust
use tokio::sync::Barrier;

let barrier = Arc::new(Barrier::new(10));

for i in 0..10 {
    let barrier = barrier.clone();
    tokio::spawn(async move {
        // Do work
        println!("Task {} waiting", i);
        barrier.wait().await;
        println!("Task {} proceeding", i);
    });
}
```

## Error Handling Patterns

### Timeout

```rust
use tokio::time::{timeout, Duration};

async fn with_timeout() -> Result<Data, Error> {
    match timeout(Duration::from_secs(5), fetch_data()).await {
        Ok(Ok(data)) => Ok(data),
        Ok(Err(e)) => Err(e),
        Err(_) => Err(Error::Timeout),
    }
}
```

### Retry Logic

```rust
async fn retry_with_backoff<F, Fut, T, E>(
    mut f: F,
    max_attempts: u32,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
{
    let mut attempt = 0;
    loop {
        match f().await {
            Ok(result) => return Ok(result),
            Err(e) if attempt >= max_attempts - 1 => return Err(e),
            Err(_) => {
                attempt += 1;
                let delay = Duration::from_millis(2u64.pow(attempt) * 100);
                tokio::time::sleep(delay).await;
            }
        }
    }
}

// Usage
let result = retry_with_backoff(
    || fetch_data("url"),
    5
).await?;
```

### Cancellation

```rust
use tokio::select;
use tokio::sync::oneshot;

async fn cancellable_operation(cancel: oneshot::Receiver<()>) -> Result<Data, Error> {
    select! {
        result = fetch_data() => result,
        _ = cancel => Err(Error::Cancelled),
    }
}

// Usage
let (tx, rx) = oneshot::channel();

let handle = tokio::spawn(cancellable_operation(rx));

// Cancel after 5 seconds
tokio::time::sleep(Duration::from_secs(5)).await;
let _ = tx.send(());
```

## Common Patterns

### Actor Pattern

```rust
use tokio::sync::mpsc;

enum ActorMessage {
    Get { respond_to: oneshot::Sender<Data> },
    Update(Data),
}

struct Actor {
    receiver: mpsc::Receiver<ActorMessage>,
    state: Data,
}

impl Actor {
    async fn run(mut self) {
        while let Some(msg) = self.receiver.recv().await {
            match msg {
                ActorMessage::Get { respond_to } => {
                    let _ = respond_to.send(self.state.clone());
                }
                ActorMessage::Update(data) => {
                    self.state = data;
                }
            }
        }
    }
}

struct ActorHandle {
    sender: mpsc::Sender<ActorMessage>,
}

impl ActorHandle {
    fn new(initial_state: Data) -> Self {
        let (sender, receiver) = mpsc::channel(32);
        let actor = Actor { receiver, state: initial_state };
        tokio::spawn(actor.run());
        ActorHandle { sender }
    }

    async fn get(&self) -> Data {
        let (tx, rx) = oneshot::channel();
        self.sender.send(ActorMessage::Get { respond_to: tx }).await.unwrap();
        rx.await.unwrap()
    }
}
```

### Rate Limiting

```rust
use tokio::time::{interval, Duration};

async fn rate_limited_requests() {
    let mut interval = interval(Duration::from_millis(100));

    for request in requests {
        interval.tick().await;  // Wait for next interval
        process_request(request).await;
    }
}
```

### Connection Pooling

```rust
use deadpool::managed;

#[async_trait]
impl managed::Manager for ConnectionManager {
    type Type = Connection;
    type Error = Error;

    async fn create(&self) -> Result<Connection, Error> {
        Connection::connect(&self.url).await
    }

    async fn recycle(&self, conn: &mut Connection) -> managed::RecycleResult<Error> {
        conn.ping().await.map_err(Into::into)
    }
}

// Usage
let manager = ConnectionManager { url: "..." };
let pool = Pool::builder(manager).max_size(16).build().unwrap();

let conn = pool.get().await?;
conn.query("SELECT ...").await?;
```

## Anti-Patterns

### Blocking in Async

```rust
// Bad: Blocks the runtime
async fn bad() {
    std::thread::sleep(Duration::from_secs(1));
}

// Good: Use tokio::time::sleep
async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}
```

### Holding Locks Across Await

```rust
// Bad: Lock held across await
async fn bad(mutex: &Mutex<Data>) {
    let mut guard = mutex.lock().await;
    some_async_function().await;  // Still holding lock!
    *guard = new_value;
}

// Good: Release lock before await
async fn good(mutex: &Mutex<Data>) {
    let value = {
        let guard = mutex.lock().await;
        guard.clone()
    };  // Lock released

    some_async_function().await;

    let mut guard = mutex.lock().await;
    *guard = new_value;
}
```

### Spawning Too Many Tasks

```rust
// Bad: Unbounded concurrency
for item in large_list {
    tokio::spawn(process(item));
}

// Good: Use buffered stream or semaphore
use futures::stream::{self, StreamExt};

stream::iter(large_list)
    .map(|item| async move { process(item).await })
    .buffered(10)  // Limit to 10 concurrent
    .collect::<Vec<_>>()
    .await;
```

## Best Practices

1. **Use async only when needed**: Don't make everything async
2. **Avoid blocking**: Use `spawn_blocking` for CPU-heavy work
3. **Limit concurrency**: Use buffering or semaphores
4. **Handle cancellation**: Clean up resources properly
5. **Release locks early**: Don't hold locks across await points
6. **Use appropriate channels**: Choose the right channel type
7. **Test with timeouts**: Add timeouts to prevent hangs
8. **Monitor task panics**: Use `JoinHandle` to detect failures
9. **Prefer structured concurrency**: Use join/select over manual spawning
10. **Profile and benchmark**: Async doesn't always mean faster
