# Structured Concurrency Rules

## coroutine-structured-parent-child - Maintain parent-child relationships

Child coroutines should be properly linked to parents for cancellation propagation.

### Incorrect

```kotlin
class OrderService {
    suspend fun processOrder(order: Order) {
        // Wrong: GlobalScope breaks structured concurrency
        GlobalScope.launch {
            sendConfirmationEmail(order)
        }

        // Wrong: Fire-and-forget coroutine
        CoroutineScope(Dispatchers.IO).launch {
            updateInventory(order)
        }
    }
}
```

### Correct

```kotlin
class OrderService {
    suspend fun processOrder(order: Order) = coroutineScope {
        // Children properly structured - cancellation propagates
        launch { sendConfirmationEmail(order) }
        launch { updateInventory(order) }
    }

    // Parallel execution with results
    suspend fun processOrderParallel(order: Order) = coroutineScope {
        val emailDeferred = async { sendConfirmationEmail(order) }
        val inventoryDeferred = async { updateInventory(order) }

        emailDeferred.await()
        inventoryDeferred.await()
    }
}
```

---

## coroutine-structured-exception - Handle exceptions in structured manner

Exceptions should propagate through the hierarchy appropriately.

### Incorrect

```kotlin
suspend fun loadData() = coroutineScope {
    launch {
        try {
            fetchUsers()
        } catch (e: Exception) {
            // Swallowed exception - other coroutines unaware
            log.error("Failed to fetch users", e)
        }
    }

    launch {
        fetchProducts() // May succeed while users failed
    }
}
```

### Correct

```kotlin
// Option 1: Let exception propagate, fail fast
suspend fun loadDataFailFast() = coroutineScope {
    launch { fetchUsers() }   // Failure cancels sibling
    launch { fetchProducts() }
}

// Option 2: Independent results with supervisorScope
suspend fun loadDataIndependent(): Pair<Result<List<User>>, Result<List<Product>>> = supervisorScope {
    val users = async { runCatching { fetchUsers() } }
    val products = async { runCatching { fetchProducts() } }

    users.await() to products.await()
}

// Option 3: Handle and report errors explicitly
sealed class LoadResult {
    data class Success(val users: List<User>, val products: List<Product>) : LoadResult()
    data class Partial(val users: List<User>?, val products: List<Product>?, val errors: List<Throwable>) : LoadResult()
}

suspend fun loadDataWithErrorHandling(): LoadResult = supervisorScope {
    val usersDeferred = async { runCatching { fetchUsers() } }
    val productsDeferred = async { runCatching { fetchProducts() } }

    val usersResult = usersDeferred.await()
    val productsResult = productsDeferred.await()

    val errors = listOfNotNull(
        usersResult.exceptionOrNull(),
        productsResult.exceptionOrNull()
    )

    if (errors.isEmpty()) {
        LoadResult.Success(usersResult.getOrThrow(), productsResult.getOrThrow())
    } else {
        LoadResult.Partial(usersResult.getOrNull(), productsResult.getOrNull(), errors)
    }
}
```

---

## coroutine-structured-cancel - Handle cancellation properly

Check for cancellation and clean up resources when cancelled.

### Incorrect

```kotlin
suspend fun processLargeFile(file: File): Result {
    val lines = file.readLines()
    var processed = 0

    for (line in lines) {
        // Wrong: No cancellation check
        processLine(line)
        processed++
    }

    return Result(processed)
}
```

### Correct

```kotlin
suspend fun processLargeFile(file: File): Result {
    val lines = file.readLines()
    var processed = 0

    for (line in lines) {
        // Check for cancellation periodically
        ensureActive()

        processLine(line)
        processed++

        // Or yield for cooperative cancellation
        if (processed % 100 == 0) {
            yield()
        }
    }

    return Result(processed)
}

// With cleanup on cancellation
suspend fun downloadWithCleanup(url: String, tempFile: File) {
    try {
        downloadTo(url, tempFile)
    } finally {
        withContext(NonCancellable) {
            if (!isActive) {
                tempFile.delete() // Cleanup on cancellation
            }
        }
    }
}
```

---

## coroutine-structured-timeout - Use withTimeout for bounded execution

Use withTimeout/withTimeoutOrNull for time-bounded operations.

### Incorrect

```kotlin
suspend fun fetchWithTimeout(url: String): Data? {
    return try {
        // No timeout - can hang forever
        httpClient.get(url).body()
    } catch (e: Exception) {
        null
    }
}
```

### Correct

```kotlin
suspend fun fetchWithTimeout(url: String): Data? {
    return withTimeoutOrNull(5000) {
        httpClient.get(url).body()
    }
}

// With explicit exception handling
suspend fun fetchWithTimeoutHandled(url: String): Result<Data> {
    return try {
        val data = withTimeout(5000) {
            httpClient.get(url).body<Data>()
        }
        Result.success(data)
    } catch (e: TimeoutCancellationException) {
        Result.failure(NetworkException.Timeout())
    } catch (e: CancellationException) {
        throw e // Don't catch regular cancellation
    } catch (e: Exception) {
        Result.failure(e)
    }
}

// Nested timeouts
suspend fun complexOperation() = withTimeout(30_000) {
    val data = withTimeout(5_000) { fetchData() }
    val processed = withTimeout(10_000) { processData(data) }
    withTimeout(10_000) { saveData(processed) }
}
```

---

## coroutine-structured-scope-function - Use scoping functions correctly

Use coroutineScope, supervisorScope, and withContext appropriately.

### Correct

```kotlin
// coroutineScope - structured, fails on any child failure
suspend fun loadAllData() = coroutineScope {
    val users = async { fetchUsers() }
    val products = async { fetchProducts() }
    DataBundle(users.await(), products.await())
}

// supervisorScope - independent children
suspend fun loadWithPartialResults() = supervisorScope {
    val users = async { runCatching { fetchUsers() } }
    val products = async { runCatching { fetchProducts() } }
    PartialDataBundle(users.await(), products.await())
}

// withContext - switch dispatcher, same scope
suspend fun processOnBackground(data: Data): Result {
    return withContext(Dispatchers.Default) {
        // CPU-intensive work
        heavyComputation(data)
    }
}

// Combining patterns
suspend fun loadAndProcess() = coroutineScope {
    val rawData = async { fetchData() }

    val processedData = withContext(Dispatchers.Default) {
        process(rawData.await())
    }

    withContext(Dispatchers.IO) {
        saveToDatabase(processedData)
    }
}
```
