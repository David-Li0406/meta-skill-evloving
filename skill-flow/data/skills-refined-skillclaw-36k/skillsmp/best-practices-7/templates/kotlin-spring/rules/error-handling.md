---
title: Error Handling
impact: HIGH
impactDescription: Fault tolerance, proper exception propagation
tags: exception, SupervisorJob, CancellationException, catch, retry
---

# Error Handling

Proper error handling in coroutines requires understanding structured concurrency and exception propagation.

## Rule 1: Use SupervisorJob Correctly

```kotlin
// ❌ INCORRECT - SupervisorJob without exception handler
val scope = CoroutineScope(SupervisorJob())

scope.launch {
    throw Exception("Unhandled!")  // crashes the app
}

// ✅ CORRECT - SupervisorJob with CoroutineExceptionHandler
val exceptionHandler = CoroutineExceptionHandler { _, exception ->
    logger.error("Coroutine failed", exception)
    errorReporter.report(exception)
}

val scope = CoroutineScope(
    SupervisorJob() +
    Dispatchers.Default +
    exceptionHandler
)

// Children fail independently
scope.launch {
    riskyOperation()  // failure doesn't cancel siblings
}
```

## Rule 2: Handle CancellationException Properly

```kotlin
// ❌ INCORRECT - swallowing CancellationException
suspend fun processItems(items: List<Item>) {
    items.forEach { item ->
        try {
            processItem(item)
        } catch (e: Exception) {  // catches CancellationException!
            logger.error("Failed", e)
            // Cancellation is swallowed, coroutine continues!
        }
    }
}

// ✅ CORRECT - rethrow CancellationException
suspend fun processItems(items: List<Item>) {
    items.forEach { item ->
        try {
            processItem(item)
        } catch (e: CancellationException) {
            throw e  // always rethrow!
        } catch (e: Exception) {
            logger.error("Failed to process ${item.id}", e)
        }
    }
}

// ✅ CORRECT - use runCatching
suspend fun processItems(items: List<Item>) {
    items.forEach { item ->
        runCatching {
            processItem(item)
        }.onFailure { e ->
            if (e is CancellationException) throw e
            logger.error("Failed to process ${item.id}", e)
        }
    }
}
```

## Rule 3: Catch Exceptions at the Source in async

```kotlin
// ❌ INCORRECT - exception in async not caught by try-catch
suspend fun fetchData(): Data = coroutineScope {
    val result = async {
        riskyNetworkCall()  // exception not caught below
    }

    try {
        result.await()
    } catch (e: Exception) {
        // This catches, but coroutineScope already cancelled!
        defaultData()
    }
}

// ✅ CORRECT - use supervisorScope
suspend fun fetchData(): Data = supervisorScope {
    val result = async {
        riskyNetworkCall()
    }

    try {
        result.await()
    } catch (e: Exception) {
        defaultData()
    }
}

// ✅ CORRECT - catch at the source
suspend fun fetchData(): Data = coroutineScope {
    val result = async {
        try {
            riskyNetworkCall()
        } catch (e: Exception) {
            defaultData()
        }
    }
    result.await()
}
```

## Rule 4: Use catch Operator in Flow

```kotlin
// ❌ INCORRECT - exception breaks entire flow
fun getUpdates(): Flow<Update> = flow {
    while (true) {
        val update = fetchUpdate()  // throws on network error
        emit(update)
        delay(1000)
    }
}

// ✅ CORRECT - catch and recover
fun getUpdates(): Flow<Update> = flow {
    while (true) {
        val update = fetchUpdate()
        emit(update)
        delay(1000)
    }
}.catch { e ->
    logger.error("Update fetch failed", e)
    emit(Update.error(e.message))
}

// ✅ CORRECT - retry on error
fun getUpdates(): Flow<Update> = flow {
    val update = fetchUpdate()
    emit(update)
}.retry(3) { e ->
    e is NetworkException
}.catch { e ->
    emit(Update.error("Failed after retries"))
}
```

## Rule 5: Implement Retry with Backoff

```kotlin
// ✅ CORRECT - retry with exponential backoff
suspend fun <T> retryWithBackoff(
    maxRetries: Int = 3,
    initialDelay: Long = 100,
    maxDelay: Long = 1000,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(maxRetries - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            if (e is CancellationException) throw e
            logger.warn("Attempt ${attempt + 1} failed", e)
        }
        delay(currentDelay)
        currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
    }
    return block()  // last attempt
}

// Usage
suspend fun fetchDataWithRetry(): Data {
    return retryWithBackoff(maxRetries = 3) {
        apiClient.fetchData()
    }
}
```

## Rule 6: Cleanup with NonCancellable

```kotlin
// ✅ CORRECT - cleanup even on cancellation
suspend fun processWithResource() {
    val resource = acquireResource()
    try {
        process(resource)
    } finally {
        withContext(NonCancellable) {
            resource.close()  // cleanup even on cancellation
        }
    }
}
```

## Detection Checklist

Look for these error handling anti-patterns:

- [ ] `catch (e: Exception)` without rethrowing `CancellationException`
- [ ] `SupervisorJob` without `CoroutineExceptionHandler`
- [ ] `coroutineScope` with `async` where `supervisorScope` is needed
- [ ] Flow without `catch` operator for error handling
- [ ] Missing retry logic for network operations
- [ ] Cleanup code without `withContext(NonCancellable)`
