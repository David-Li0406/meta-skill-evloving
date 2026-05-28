---
title: Scope Management
impact: CRITICAL
impactDescription: Memory leak prevention, structured concurrency
tags: scope, GlobalScope, coroutineScope, supervisorScope, structured-concurrency
---

# Scope Management

Proper scope management ensures coroutines are cancelled when no longer needed and exceptions propagate correctly.

## Rule 1: Never Use GlobalScope

```kotlin
// ❌ INCORRECT - GlobalScope leaks and can't be cancelled
@Service
class NotificationService {
    fun sendAsync(notification: Notification) {
        GlobalScope.launch {  // NEVER CANCELLED!
            sendNotification(notification)
        }
    }
}

// ✅ CORRECT - inject scope tied to service lifecycle
@Service
class NotificationService(
    private val scope: CoroutineScope  // injected
) {
    fun sendAsync(notification: Notification) {
        scope.launch {  // cancelled when service destroyed
            sendNotification(notification)
        }
    }
}

// ✅ CORRECT - define scope as Spring bean
@Configuration
class CoroutineConfig {
    @Bean
    fun applicationScope(): CoroutineScope {
        return CoroutineScope(
            SupervisorJob() +
            Dispatchers.Default +
            CoroutineName("app-scope")
        )
    }

    @Bean
    fun cleanupScope(scope: CoroutineScope): DisposableBean {
        return DisposableBean { scope.cancel() }
    }
}
```

## Rule 2: Use Structured Concurrency

```kotlin
// ❌ INCORRECT - fire-and-forget without structure
suspend fun processOrders(orders: List<Order>) {
    orders.forEach { order ->
        CoroutineScope(Dispatchers.Default).launch {
            processOrder(order)  // orphaned coroutines!
        }
    }
    // returns immediately, children still running
}

// ✅ CORRECT - structured concurrency waits for children
suspend fun processOrders(orders: List<Order>) = coroutineScope {
    orders.forEach { order ->
        launch {
            processOrder(order)
        }
    }
    // waits for all children to complete
}
```

## Rule 3: Use coroutineScope for Grouping

```kotlin
// ✅ CORRECT - group related operations
suspend fun updateUserProfile(userId: Long, profile: Profile): User = coroutineScope {
    // Validate in parallel
    val validationDeferred = async { validateProfile(profile) }
    val existingUser = async { userRepository.findById(userId) }

    validationDeferred.await()  // throws if invalid
    val user = existingUser.await() ?: throw UserNotFoundException(userId)

    // Update with validated data
    val updatedUser = user.copy(name = profile.name, email = profile.email)

    // Parallel side effects
    launch { auditService.logUpdate(userId) }
    launch { cacheService.invalidate(userId) }

    userRepository.save(updatedUser)
}
```

## Rule 4: Use supervisorScope for Fault Isolation

```kotlin
// ❌ INCORRECT - one failure cancels all
suspend fun sendNotifications(users: List<User>) = coroutineScope {
    users.forEach { user ->
        launch {
            sendNotification(user)  // one failure cancels ALL
        }
    }
}

// ✅ CORRECT - isolated failures with supervisorScope
suspend fun sendNotifications(users: List<User>) = supervisorScope {
    users.forEach { user ->
        launch {
            try {
                sendNotification(user)
            } catch (e: Exception) {
                logger.error("Failed to notify ${user.id}", e)
                // continues with other users
            }
        }
    }
}
```

## Rule 5: Tie Scope to Lifecycle

```kotlin
// ✅ CORRECT - scope tied to component lifecycle
@Component
class BackgroundProcessor : DisposableBean {
    private val scope = CoroutineScope(
        SupervisorJob() + Dispatchers.Default
    )

    fun startProcessing() {
        scope.launch {
            while (isActive) {
                processNextItem()
                delay(1000)
            }
        }
    }

    override fun destroy() {
        scope.cancel()  // cleanup on shutdown
    }
}
```

## Rule 6: Inject CoroutineScope for Testability

```kotlin
// ✅ CORRECT - inject scope for testability
@Service
class OrderProcessor(
    private val orderRepository: OrderRepository,
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.Default)
) {
    fun processAsync(orderId: Long): Job {
        return scope.launch {
            val order = orderRepository.findById(orderId)
            processOrder(order)
        }
    }
}

// In tests
@Test
fun `test order processing`() = runTest {
    val testScope = this  // TestScope from runTest
    val processor = OrderProcessor(mockRepository, testScope)

    processor.processAsync(1L)
    advanceUntilIdle()

    coVerify { mockRepository.findById(1L) }
}
```

## Detection Checklist

Look for these scope anti-patterns:

- [ ] `GlobalScope.launch` or `GlobalScope.async`
- [ ] `CoroutineScope(Dispatchers.X).launch` (ad-hoc scope creation)
- [ ] Missing `scope.cancel()` in `DisposableBean.destroy()`
- [ ] Fire-and-forget coroutines without structured concurrency
- [ ] Using `coroutineScope` where `supervisorScope` is needed for fault tolerance
