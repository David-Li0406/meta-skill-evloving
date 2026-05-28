# CompletableFuture Patterns

## Basic Composition

```java
// Async execution with custom executor
CompletableFuture<User> userFuture = CompletableFuture
    .supplyAsync(() -> userRepository.findById(id), ioExecutor);

// Transform result
CompletableFuture<String> emailFuture = userFuture
    .thenApply(User::getEmail);

// Async transformation
CompletableFuture<Profile> profileFuture = userFuture
    .thenApplyAsync(user -> profileService.load(user), ioExecutor);

// Consume result
userFuture.thenAccept(user -> log.info("Loaded user: {}", user.getName()));

// Run after completion (no access to result)
userFuture.thenRun(() -> metrics.increment("user.loaded"));
```

## Combining Futures

```java
// Combine two futures
CompletableFuture<UserWithOrders> combined = userFuture
    .thenCombine(ordersFuture, (user, orders) -> new UserWithOrders(user, orders));

// Chain dependent futures
CompletableFuture<List<OrderDetails>> details = userFuture
    .thenCompose(user -> orderService.findByUser(user.getId()));

// Wait for all
CompletableFuture<Void> all = CompletableFuture.allOf(
    future1, future2, future3
);

// Get results after allOf
CompletableFuture<List<Result>> results = all.thenApply(v -> List.of(
    future1.join(),
    future2.join(),
    future3.join()
));

// First to complete (race)
CompletableFuture<String> fastest = CompletableFuture.anyOf(
    primaryService.call(),
    backupService.call()
).thenApply(result -> (String) result);
```

## Error Handling

```java
// Recover from exception
CompletableFuture<User> withFallback = userFuture
    .exceptionally(ex -> {
        log.warn("Failed to load user: {}", ex.getMessage());
        return User.guest();
    });

// Handle both success and failure
CompletableFuture<Result> handled = userFuture
    .handle((user, ex) -> {
        if (ex != null) {
            return Result.failure(ex);
        }
        return Result.success(user);
    });

// Async exception handling
CompletableFuture<User> recovered = userFuture
    .exceptionallyAsync(ex -> loadFromCache(id), cacheExecutor);

// whenComplete - observe without changing result
userFuture.whenComplete((user, ex) -> {
    if (ex != null) {
        metrics.increment("user.load.failed");
    } else {
        metrics.increment("user.load.success");
    }
});
```

## Timeouts (Java 9+)

```java
// Timeout with exception
CompletableFuture<User> withTimeout = userFuture
    .orTimeout(5, TimeUnit.SECONDS);

// Timeout with fallback value
CompletableFuture<User> withFallback = userFuture
    .completeOnTimeout(User.guest(), 5, TimeUnit.SECONDS);

// Manual timeout (pre-Java 9)
CompletableFuture<User> manual = new CompletableFuture<>();
scheduler.schedule(
    () -> manual.completeExceptionally(new TimeoutException()),
    5, TimeUnit.SECONDS
);
userFuture.thenAccept(manual::complete);
```

## Parallel Execution

```java
// Execute multiple independent tasks in parallel
public CompletableFuture<Dashboard> loadDashboard(String userId) {
    CompletableFuture<User> userF = loadUser(userId);
    CompletableFuture<List<Order>> ordersF = loadOrders(userId);
    CompletableFuture<Preferences> prefsF = loadPreferences(userId);
    CompletableFuture<Recommendations> recsF = loadRecommendations(userId);

    return CompletableFuture.allOf(userF, ordersF, prefsF, recsF)
        .thenApply(v -> new Dashboard(
            userF.join(),
            ordersF.join(),
            prefsF.join(),
            recsF.join()
        ));
}

// Collect results from list of futures
public <T> CompletableFuture<List<T>> allOf(List<CompletableFuture<T>> futures) {
    return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
        .thenApply(v -> futures.stream()
            .map(CompletableFuture::join)
            .toList());
}
```

## Best Practices

```java
// 1. Always specify executor for async operations
CompletableFuture.supplyAsync(task, executor);  // Good
CompletableFuture.supplyAsync(task);  // Uses ForkJoinPool.commonPool() - careful

// 2. Use join() in composition, get() when you need checked exceptions
results.stream()
    .map(CompletableFuture::join)  // In stream context
    .toList();

try {
    result.get(5, TimeUnit.SECONDS);  // When timeout/exception handling needed
} catch (TimeoutException | ExecutionException e) {
    // handle
}

// 3. Don't block in async chains
userFuture
    .thenApply(user -> {
        // DON'T: orderService.findByUser(user.getId()).get(); // Blocks!
        // DO: return orderService.findByUser(user.getId());
        return user.getName();
    });

// 4. Use thenCompose for dependent async operations
userFuture.thenCompose(user -> loadOrders(user.getId()));  // Good
// Not: userFuture.thenApply(user -> loadOrders(user.getId()).join());  // Blocks
```
