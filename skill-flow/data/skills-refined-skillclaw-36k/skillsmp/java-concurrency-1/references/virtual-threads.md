# Virtual Threads (Java 21+)

## Overview

Virtual threads are lightweight threads managed by the JVM, not the OS. They enable the "thread-per-request" model without the overhead of platform threads.

## Basic Usage

```java
// Start a virtual thread
Thread.startVirtualThread(() -> {
    // blocking I/O is fine - JVM will unmount from carrier thread
    String response = httpClient.send(request, BodyHandlers.ofString()).body();
    processResponse(response);
});

// Create named virtual thread
Thread vt = Thread.ofVirtual()
    .name("my-virtual-thread")
    .start(() -> doWork());

// Check if current thread is virtual
if (Thread.currentThread().isVirtual()) {
    // running on virtual thread
}
```

## ExecutorService Pattern

```java
// Preferred: ExecutorService with virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = tasks.stream()
        .map(task -> executor.submit(() -> processTask(task)))
        .toList();

    List<Result> results = new ArrayList<>();
    for (Future<Result> future : futures) {
        results.add(future.get());  // blocking is fine
    }
    return results;
}

// For HTTP handlers (e.g., Tomcat, Jetty)
// Configure server to use virtual threads - each request gets its own
```

## Structured Concurrency (Preview)

```java
// Run subtasks with structured lifetime
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> userTask = scope.fork(() -> userService.find(userId));
    Subtask<List<Order>> ordersTask = scope.fork(() -> orderService.findByUser(userId));
    Subtask<Preferences> prefsTask = scope.fork(() -> prefsService.find(userId));

    scope.join();           // Wait for all tasks
    scope.throwIfFailed();  // Propagate exceptions

    return new UserProfile(
        userTask.get(),
        ordersTask.get(),
        prefsTask.get()
    );
}

// ShutdownOnSuccess - cancel remaining tasks when one succeeds
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> fetchFromPrimary());
    scope.fork(() -> fetchFromBackup());

    scope.join();
    return scope.result();  // First successful result
}
```

## When to Use Virtual Threads

### Good Use Cases

```java
// ✅ I/O-bound operations
void processRequests(List<Request> requests) {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        requests.forEach(req ->
            executor.submit(() -> {
                String data = httpClient.get(req.url());     // Network I/O
                String result = database.query(req.query()); // Database I/O
                fileSystem.write(result);                    // File I/O
            })
        );
    }
}

// ✅ HTTP servers handling many concurrent connections
// ✅ Database-heavy applications
// ✅ Microservices making downstream calls
```

### When NOT to Use

```java
// ❌ CPU-bound computation - use platform threads
// Virtual threads don't help with CPU-bound work
void cpuIntensive(List<Data> data) {
    // Use fixed thread pool sized to CPU cores
    ExecutorService cpuPool = Executors.newFixedThreadPool(
        Runtime.getRuntime().availableProcessors()
    );
}

// ❌ Long synchronized blocks - use ReentrantLock instead
// synchronized pins the carrier thread
synchronized (lock) {
    // Long blocking operation - BAD
    Thread.sleep(1000);
}

// GOOD: Use ReentrantLock
lock.lock();
try {
    Thread.sleep(1000);  // Virtual thread unmounts during sleep
} finally {
    lock.unlock();
}
```

## Migration Tips

```java
// 1. Replace thread pools with virtual thread executor
// Before
ExecutorService executor = Executors.newFixedThreadPool(200);

// After (for I/O-bound work)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// 2. Replace synchronized with ReentrantLock for blocking operations
// Before
synchronized (lock) {
    blockingCall();
}

// After
private final ReentrantLock lock = new ReentrantLock();

lock.lock();
try {
    blockingCall();
} finally {
    lock.unlock();
}

// 3. Don't pool virtual threads - create new ones freely
// Virtual threads are cheap (~1KB vs ~1MB for platform threads)
```

## Debugging

```java
// Thread dumps show virtual threads
// jcmd <pid> Thread.dump_to_file -format=json threads.json

// Configure carrier thread count
// -Djdk.virtualThreadScheduler.parallelism=<n>
// -Djdk.virtualThreadScheduler.maxPoolSize=<n>

// Detect pinned virtual threads
// -Djdk.tracePinnedThreads=full
```

## Pitfalls

```java
// 1. ThreadLocal can consume memory with many virtual threads
// Use ScopedValue (preview) instead
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    processRequest();
});

// 2. Don't use thread-per-task executor with CompletableFuture
// Each stage gets a new virtual thread - may be wasteful
CompletableFuture.supplyAsync(task, virtualExecutor)
    .thenApplyAsync(transform, virtualExecutor);  // Unnecessary

// 3. Monitor carrier thread pinning
// Long synchronized blocks or native calls pin carrier threads
```
