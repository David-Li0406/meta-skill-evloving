---
title: Coroutine Basics
impact: CRITICAL
impactDescription: Non-blocking execution, proper thread utilization
tags: coroutine, suspend, dispatcher, async, withContext
---

# Coroutine Basics

Kotlin coroutines enable non-blocking execution. Blocking operations freeze the entire event loop.

## Rule 1: Use Suspend Functions Correctly

```kotlin
// ❌ INCORRECT - blocking call in suspend function
suspend fun getUser(id: Long): User {
    Thread.sleep(1000)  // BLOCKS the thread!
    return repository.findById(id)  // blocking JDBC
}

// ✅ CORRECT - proper suspend function
suspend fun getUser(id: Long): User {
    delay(1000)  // non-blocking delay
    return repository.findByIdOrNull(id)  // R2DBC suspend
        ?: throw UserNotFoundException(id)
}
```

## Rule 2: Choose Correct Dispatcher

```kotlin
// ❌ INCORRECT - CPU-intensive work on IO dispatcher
suspend fun processImage(data: ByteArray): ByteArray {
    return withContext(Dispatchers.IO) {  // Wrong! IO is for blocking I/O
        heavyImageProcessing(data)  // CPU-bound work
    }
}

// ✅ CORRECT - use appropriate dispatchers
suspend fun processImage(data: ByteArray): ByteArray {
    return withContext(Dispatchers.Default) {  // CPU-bound work
        heavyImageProcessing(data)
    }
}

suspend fun readFile(path: String): String {
    return withContext(Dispatchers.IO) {  // Blocking I/O
        File(path).readText()
    }
}
```

## Rule 3: Never Block in Coroutines

```kotlin
// ❌ INCORRECT - blocking operations in coroutine
@GetMapping("/data")
suspend fun getData(): Data {
    val result = blockingHttpClient.get(url)  // BLOCKS!
    Thread.sleep(100)  // BLOCKS!
    return result
}

// ✅ CORRECT - use non-blocking alternatives
@GetMapping("/data")
suspend fun getData(): Data {
    val result = webClient.get()
        .uri(url)
        .awaitBody<Data>()  // non-blocking
    delay(100)  // non-blocking
    return result
}
```

## Rule 4: Use async/await for Parallel Execution

```kotlin
// ❌ INCORRECT - sequential execution (3x latency)
suspend fun getDashboard(userId: Long): Dashboard {
    val user = userService.getUser(userId)        // 100ms
    val orders = orderService.getOrders(userId)   // 100ms
    val notifications = notificationService.get() // 100ms
    return Dashboard(user, orders, notifications) // Total: 300ms
}

// ✅ CORRECT - parallel execution with coroutineScope
suspend fun getDashboard(userId: Long): Dashboard = coroutineScope {
    val user = async { userService.getUser(userId) }
    val orders = async { orderService.getOrders(userId) }
    val notifications = async { notificationService.get() }

    Dashboard(
        user = user.await(),
        orders = orders.await(),
        notifications = notifications.await()
    )  // Total: ~100ms (max of all)
}
```

## Rule 5: Use withContext for Dispatcher Switch

```kotlin
// ❌ INCORRECT - unnecessary scope creation
suspend fun processData(data: Data): Result {
    return CoroutineScope(Dispatchers.Default).async {
        heavyProcessing(data)
    }.await()  // Creates new scope, loses parent context!
}

// ✅ CORRECT - use withContext
suspend fun processData(data: Data): Result {
    return withContext(Dispatchers.Default) {
        heavyProcessing(data)
    }  // Maintains parent scope, proper cancellation
}
```

## Detection Checklist

Look for these blocking patterns in Kotlin Spring code:

- [ ] `Thread.sleep()` in suspend functions
- [ ] Blocking HTTP clients (`OkHttp`, `RestTemplate`) instead of `WebClient.awaitBody()`
- [ ] Blocking JDBC drivers instead of R2DBC
- [ ] `File.readText()` without `withContext(Dispatchers.IO)`
- [ ] Sequential `await` when parallel is possible
- [ ] `CoroutineScope().async` instead of `withContext`
