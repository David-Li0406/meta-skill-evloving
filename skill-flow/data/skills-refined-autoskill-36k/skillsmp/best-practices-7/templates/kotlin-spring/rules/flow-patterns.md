---
title: Flow Patterns
impact: HIGH
impactDescription: Reactive streams, state management, event handling
tags: flow, StateFlow, SharedFlow, flowOn, operators
---

# Flow Patterns

Kotlin Flow provides reactive streams with coroutine support. Understanding cold vs hot flows is essential.

## Rule 1: Understand Flow is Cold

```kotlin
// ❌ INCORRECT - expecting Flow to run immediately
fun getUpdates(): Flow<Update> = flow {
    println("Starting flow")  // Not printed until collected!
    emit(fetchUpdate())
}

val updates = getUpdates()  // Nothing happens yet

// ✅ CORRECT - collect to start the flow
suspend fun processUpdates() {
    getUpdates().collect { update ->
        println("Received: $update")
    }
}

// ✅ CORRECT - use SharedFlow for hot streams
@Service
class EventService {
    private val _events = MutableSharedFlow<Event>(
        replay = 1,
        extraBufferCapacity = 64
    )
    val events: SharedFlow<Event> = _events.asSharedFlow()
}
```

## Rule 2: Use Flow Operators Correctly

```kotlin
// ✅ CORRECT - chain operators efficiently
fun getProcessedOrders(): Flow<ProcessedOrder> {
    return orderRepository.findAllAsFlow()
        .filter { it.status == OrderStatus.PENDING }
        .map { order -> processOrder(order) }
        .catch { e ->
            logger.error("Processing failed", e)
            emit(ProcessedOrder.failed())
        }
        .onCompletion { logger.info("Processing complete") }
}

// ✅ CORRECT - use buffer for slow collectors
fun getNotifications(): Flow<Notification> {
    return notificationSource.asFlow()
        .buffer(capacity = 64)
        .map { enrichNotification(it) }
}

// ✅ CORRECT - debounce for rate limiting
fun getSearchResults(queries: Flow<String>): Flow<List<Result>> {
    return queries
        .debounce(300)
        .distinctUntilChanged()
        .flatMapLatest { query -> searchService.search(query) }
}
```

## Rule 3: Use StateFlow for State

```kotlin
// ✅ CORRECT - StateFlow for observable state
@Service
class ConnectionService {
    private val _connectionState = MutableStateFlow(ConnectionState.DISCONNECTED)
    val connectionState: StateFlow<ConnectionState> = _connectionState.asStateFlow()

    suspend fun connect() {
        _connectionState.value = ConnectionState.CONNECTING
        try {
            establishConnection()
            _connectionState.value = ConnectionState.CONNECTED
        } catch (e: Exception) {
            _connectionState.value = ConnectionState.ERROR
        }
    }
}
```

## Rule 4: Use SharedFlow for Events

```kotlin
// ✅ CORRECT - SharedFlow for one-time events
@Service
class EventBus {
    private val _events = MutableSharedFlow<AppEvent>(
        extraBufferCapacity = 64,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val events: SharedFlow<AppEvent> = _events.asSharedFlow()

    suspend fun publish(event: AppEvent) {
        _events.emit(event)
    }

    fun tryPublish(event: AppEvent): Boolean {
        return _events.tryEmit(event)
    }
}
```

## Rule 5: Use flowOn for Context Switching

```kotlin
// ❌ INCORRECT - multiple unnecessary context switches
fun processItems(): Flow<Item> = flow {
    items.forEach { item ->
        val processed = withContext(Dispatchers.Default) {  // switch per item!
            process(item)
        }
        emit(processed)
    }
}

// ✅ CORRECT - single flowOn for upstream
fun processItems(): Flow<Item> = flow {
    items.forEach { item ->
        emit(process(item))
    }
}.flowOn(Dispatchers.Default)
```

## Rule 6: Collect Safely in Scope

```kotlin
// ❌ INCORRECT - collecting in GlobalScope
@Service
class EventListener {
    fun startListening() {
        GlobalScope.launch {  // leaks!
            events.collect { handleEvent(it) }
        }
    }
}

// ✅ CORRECT - collect in lifecycle-bound scope
@Service
class EventListener(
    private val scope: CoroutineScope
) : DisposableBean {

    init {
        events
            .onEach { handleEvent(it) }
            .launchIn(scope)
    }

    override fun destroy() {
        // scope is cancelled by Spring
    }
}
```

## Detection Checklist

Look for these Flow anti-patterns:

- [ ] Expecting Flow to execute without `collect()`
- [ ] `withContext` inside flow builder (use `flowOn` instead)
- [ ] Exposing `MutableStateFlow` directly (expose `asStateFlow()`)
- [ ] Missing `buffer()` for slow collectors
- [ ] `GlobalScope.launch` with `collect`
