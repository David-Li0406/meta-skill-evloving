---
name: Java Concurrency
description: Thread management, Executor framework, CompletableFuture, synchronization, and virtual threads.
metadata:
  labels: [java, concurrency, threads, async]
  triggers:
    files: ['**/*.java']
    keywords: [Thread, Runnable, Executor, CompletableFuture, synchronized, Lock, Atomic, Future, Callable, ExecutorService]
---

# Java Concurrency Standards

## Executor Framework

```java
// Fixed thread pool - bounded, predictable
ExecutorService executor = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);

// Cached thread pool - unbounded, use carefully
ExecutorService cached = Executors.newCachedThreadPool();

// Scheduled executor
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.scheduleAtFixedRate(task, 0, 1, TimeUnit.SECONDS);

// Virtual threads (Java 21+)
ExecutorService virtual = Executors.newVirtualThreadPerTaskExecutor();

// Custom thread pool
ThreadPoolExecutor custom = new ThreadPoolExecutor(
    4,                      // core pool size
    8,                      // max pool size
    60, TimeUnit.SECONDS,   // keep alive
    new LinkedBlockingQueue<>(100),  // work queue
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejection handler
);

// Always shutdown executors
try {
    executor.shutdown();
    if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
        executor.shutdownNow();
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();
}
```

## CompletableFuture

```java
// Async execution
CompletableFuture<User> userFuture = CompletableFuture
    .supplyAsync(() -> userService.findById(id), executor);

// Chaining
CompletableFuture<String> result = userFuture
    .thenApply(User::getEmail)
    .thenApply(String::toLowerCase)
    .exceptionally(ex -> "unknown@example.com");

// Combine multiple futures
CompletableFuture<UserProfile> profile = CompletableFuture
    .allOf(userFuture, ordersFuture, preferencesFuture)
    .thenApply(v -> new UserProfile(
        userFuture.join(),
        ordersFuture.join(),
        preferencesFuture.join()
    ));

// Either/race
CompletableFuture<String> fastest = CompletableFuture
    .anyOf(primaryService, fallbackService)
    .thenApply(result -> (String) result);

// Timeout (Java 9+)
CompletableFuture<User> withTimeout = userFuture
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> defaultUser);
```

## Synchronization

```java
// synchronized block - prefer over method
private final Object lock = new Object();

public void update(String value) {
    synchronized (lock) {
        // critical section
    }
}

// ReentrantLock - more flexible
private final ReentrantLock lock = new ReentrantLock();

public void process() {
    lock.lock();
    try {
        // critical section
    } finally {
        lock.unlock();
    }
}

// ReadWriteLock - multiple readers, single writer
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();

public String read() {
    rwLock.readLock().lock();
    try {
        return data;
    } finally {
        rwLock.readLock().unlock();
    }
}

public void write(String value) {
    rwLock.writeLock().lock();
    try {
        data = value;
    } finally {
        rwLock.writeLock().unlock();
    }
}
```

## Atomic Classes

```java
// Atomic primitives
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.compareAndSet(expected, newValue);

// Atomic reference
AtomicReference<Config> configRef = new AtomicReference<>(initialConfig);
configRef.updateAndGet(config -> config.withNewValue(value));

// LongAdder for high contention
LongAdder adder = new LongAdder();
adder.increment();
long sum = adder.sum();
```

## Virtual Threads (Java 21+)

```java
// Simple virtual thread
Thread.startVirtualThread(() -> {
    // blocking I/O is fine
    String data = httpClient.get(url);
    process(data);
});

// With executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = tasks.stream()
        .map(task -> executor.submit(task::execute))
        .toList();

    for (Future<Result> future : futures) {
        results.add(future.get());
    }
}

// Don't use with CPU-bound tasks
// Don't use synchronized for long operations (use ReentrantLock)
```

## Best Practices

1. **Prefer high-level constructs** (Executor, CompletableFuture) over raw threads
2. **Size thread pools** based on task type (CPU-bound: cores, I/O-bound: higher)
3. **Always handle InterruptedException** - restore interrupt status
4. **Use virtual threads** for I/O-bound tasks (Java 21+)
5. **Prefer Atomic classes** over synchronized for simple counters
6. **Immutability** is the best synchronization

## References

- [Executor Patterns](references/executor-patterns.md) - Thread pool configuration, shutdown
- [CompletableFuture](references/completable-future.md) - Async composition patterns
- [Virtual Threads](references/virtual-threads.md) - Java 21+ patterns
