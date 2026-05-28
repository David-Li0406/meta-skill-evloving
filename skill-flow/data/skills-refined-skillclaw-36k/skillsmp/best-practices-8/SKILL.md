---
name: best-practices
description: Kotlin Coroutines with Spring Boot/WebFlux performance optimization and best practices guidelines
license: MIT
metadata:
  author: devnogari
  project_type: kotlin-spring
  rule_count: 48
  categories: 8
---

# Kotlin Coroutines + Spring Boot Best Practices

Comprehensive performance optimization and best practices for Spring Boot applications with Kotlin Coroutines. **48 rules across 8 categories** based on Spring Framework 7.0, Spring Boot 4.0, Kotlin 2.x coroutines, and R2DBC async patterns.

## Activation Triggers

This skill activates when:
- Writing new controllers, services, or repositories with coroutines
- Implementing Flow patterns and reactive streams
- Optimizing async performance with WebFlux
- Reviewing or refactoring Kotlin coroutine code
- Debugging scope, cancellation, or flow issues
- Implementing authentication/authorization with reactive security
- Writing tests for coroutine-based applications

## Rule Categories

| # | Category | Priority | Prefix | Rule Count | Focus |
|---|----------|----------|--------|------------|-------|
| 1 | Coroutine Basics | CRITICAL | `coroutine-` | 6 | suspend functions, dispatchers |
| 2 | Scope Management | CRITICAL | `scope-` | 6 | GlobalScope avoidance, structured concurrency |
| 3 | Flow Patterns | HIGH | `flow-` | 6 | Flow, StateFlow, SharedFlow |
| 4 | R2DBC Database | HIGH | `db-` | 6 | Reactive repositories, transactions |
| 5 | Error Handling | HIGH | `err-` | 6 | SupervisorJob, exception handling |
| 6 | Spring WebFlux | MEDIUM | `webflux-` | 6 | Reactive endpoints, context propagation |
| 7 | Security | MEDIUM | `sec-` | 6 | Reactive security, JWT, context |
| 8 | Testing | MEDIUM | `test-` | 6 | runTest, MockK, Turbine |

## Quick Reference - All 48 Rules

### Coroutine Basics (CRITICAL) - `coroutine-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `coroutine-suspend` | Use suspend functions correctly | Non-blocking execution |
| `coroutine-dispatcher` | Choose correct dispatcher | CPU/IO optimization |
| `coroutine-blocking` | Never block in coroutines | Prevents thread starvation |
| `coroutine-context` | Understand CoroutineContext | Proper context propagation |
| `coroutine-async` | Use async/await for parallel | Concurrent execution |
| `coroutine-withContext` | Use withContext for dispatcher switch | Clean context switching |

### Scope Management (CRITICAL) - `scope-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `scope-no-global` | Never use GlobalScope | Prevents memory leaks |
| `scope-structured` | Use structured concurrency | Automatic cleanup |
| `scope-coroutineScope` | Use coroutineScope for grouping | Child coroutine management |
| `scope-supervisorScope` | Use supervisorScope for isolation | Fault tolerance |
| `scope-lifecycle` | Tie scope to lifecycle | Resource management |
| `scope-injection` | Inject CoroutineScope | Testability |

### Flow Patterns (HIGH) - `flow-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `flow-cold` | Understand Flow is cold | Proper subscription |
| `flow-operators` | Use flow operators correctly | Efficient transformations |
| `flow-stateflow` | Use StateFlow for state | UI state management |
| `flow-sharedflow` | Use SharedFlow for events | Event broadcasting |
| `flow-flowOn` | Use flowOn for context | Single context switch |
| `flow-collect` | Collect safely in scope | Prevent leaks |

### R2DBC Database (HIGH) - `db-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `db-r2dbc` | Use R2DBC not JDBC | Non-blocking DB |
| `db-repository` | Use CoroutineCrudRepository | Coroutine-native API |
| `db-transaction` | Handle transactions correctly | Data consistency |
| `db-connection-pool` | Configure connection pool | Resource efficiency |
| `db-n-plus-one` | Avoid N+1 queries | Query optimization |
| `db-migration` | Use Flyway/Liquibase async | Schema management |

### Error Handling (HIGH) - `err-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `err-supervisor` | Use SupervisorJob correctly | Fault isolation |
| `err-handler` | Use CoroutineExceptionHandler | Centralized error handling |
| `err-try-catch` | Catch exceptions in coroutines | Proper error recovery |
| `err-cancellation` | Handle CancellationException | Correct cancellation |
| `err-flow-catch` | Use catch operator in Flow | Flow error handling |
| `err-retry` | Implement retry with backoff | Resilience |

### Spring WebFlux (MEDIUM) - `webflux-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `webflux-controller` | Use suspend in controllers | Non-blocking endpoints |
| `webflux-coRouter` | Use coRouter DSL | Coroutine-friendly routing |
| `webflux-webclient` | Use WebClient with awaitBody | Async HTTP calls |
| `webflux-context` | Propagate ReactorContext | Observability, tracing |
| `webflux-response` | Return proper types | Efficient serialization |
| `webflux-filter` | Use CoWebFilter | Coroutine-aware filters |

### Security (MEDIUM) - `sec-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `sec-reactive` | Use ReactiveSecurityContextHolder | Reactive auth context |
| `sec-method` | Use @PreAuthorize with suspend | Method-level security |
| `sec-context-propagation` | Propagate SecurityContext | Cross-thread auth |
| `sec-jwt` | Implement JWT properly | Stateless auth |
| `sec-cors` | Configure CORS correctly | Cross-origin security |
| `sec-csrf` | Handle CSRF in WebFlux | Request forgery protection |

### Testing (MEDIUM) - `test-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `test-runTest` | Use runTest for coroutines | Proper test execution |
| `test-mockk` | Use MockK coEvery/coVerify | Suspend function mocking |
| `test-turbine` | Use Turbine for Flow testing | Flow assertions |
| `test-dispatcher` | Use TestDispatcher | Deterministic tests |
| `test-webclient` | Test with WebTestClient | Integration testing |
| `test-container` | Use Testcontainers | Database testing |

---

## Detailed Rules by Category

### 1. Coroutine Basics (CRITICAL)

#### `coroutine-suspend` - Use Suspend Functions Correctly

**Impact**: Non-blocking execution, proper coroutine integration

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

// ✅ CORRECT - marking function as suspend when it calls other suspend functions
suspend fun getUserWithOrders(userId: Long): UserWithOrders {
    val user = userRepository.findById(userId)  // suspend call
    val orders = orderRepository.findByUserId(userId)  // suspend call
    return UserWithOrders(user, orders)
}
```

#### `coroutine-dispatcher` - Choose Correct Dispatcher

**Impact**: Optimized thread utilization for CPU vs IO operations

```kotlin
// ❌ INCORRECT - CPU-intensive work on Default/IO dispatcher
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

// ✅ CORRECT - no dispatcher needed for suspend-native operations
suspend fun fetchFromApi(url: String): Response {
    // WebClient is already non-blocking, no withContext needed
    return webClient.get()
        .uri(url)
        .awaitExchange { it.awaitBody() }
}
```

#### `coroutine-blocking` - Never Block in Coroutines

**Impact**: Prevents thread starvation, maintains concurrency

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

// ✅ CORRECT - if blocking is unavoidable, use withContext(Dispatchers.IO)
suspend fun legacyOperation(): Result {
    return withContext(Dispatchers.IO) {
        legacyBlockingClient.execute()  // isolated on IO dispatcher
    }
}
```

#### `coroutine-context` - Understand CoroutineContext

**Impact**: Proper context propagation for logging, tracing, auth

```kotlin
// ❌ INCORRECT - losing context elements
suspend fun processWithLogging() {
    // MDC context lost when switching dispatchers
    withContext(Dispatchers.Default) {
        logger.info("Processing")  // MDC context may be empty!
    }
}

// ✅ CORRECT - propagate context elements
suspend fun processWithLogging() {
    val mdcContext = MDCContext()
    withContext(Dispatchers.Default + mdcContext) {
        logger.info("Processing")  // MDC context preserved
    }
}

// ✅ CORRECT - Spring Boot 4.0 automatic context propagation
// application.properties: spring.reactor.context-propagation=auto
@GetMapping("/trace")
suspend fun tracedEndpoint(): Response {
    // Tracing context automatically propagated
    return service.process()
}
```

#### `coroutine-async` - Use async/await for Parallel Execution

**Impact**: Concurrent execution, reduced latency

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

// ✅ CORRECT - with structured error handling
suspend fun getDashboardSafe(userId: Long): Dashboard = supervisorScope {
    val user = async { userService.getUser(userId) }
    val orders = async {
        runCatching { orderService.getOrders(userId) }
            .getOrDefault(emptyList())
    }
    val notifications = async {
        runCatching { notificationService.get() }
            .getOrDefault(emptyList())
    }

    Dashboard(user.await(), orders.await(), notifications.await())
}
```

#### `coroutine-withContext` - Use withContext for Dispatcher Switch

**Impact**: Clean context switching without nested scopes

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

// ✅ CORRECT - combine context elements
suspend fun processWithTimeout(data: Data): Result {
    return withContext(Dispatchers.Default + CoroutineName("processor")) {
        withTimeout(5000) {
            heavyProcessing(data)
        }
    }
}
```

---

### 2. Scope Management (CRITICAL)

#### `scope-no-global` - Never Use GlobalScope

**Impact**: Prevents memory leaks, enables proper cancellation

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

#### `scope-structured` - Use Structured Concurrency

**Impact**: Automatic cleanup, proper parent-child relationships

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

// ✅ CORRECT - parallel with result collection
suspend fun processOrders(orders: List<Order>): List<Result> = coroutineScope {
    orders.map { order ->
        async {
            processOrder(order)
        }
    }.awaitAll()
}
```

#### `scope-coroutineScope` - Use coroutineScope for Grouping

**Impact**: Child coroutine management, exception propagation

```kotlin
// ✅ CORRECT - group related operations
suspend fun updateUserProfile(userId: Long, profile: Profile): User = coroutineScope {
    // Validate in parallel
    val validationDeferred = async { validateProfile(profile) }
    val existingUser = async { userRepository.findById(userId) }

    validationDeferred.await()  // throws if invalid
    val user = existingUser.await() ?: throw UserNotFoundException(userId)

    // Update with validated data
    val updatedUser = user.copy(
        name = profile.name,
        email = profile.email
    )

    // Parallel side effects
    launch { auditService.logUpdate(userId) }
    launch { cacheService.invalidate(userId) }

    userRepository.save(updatedUser)
}
```

#### `scope-supervisorScope` - Use supervisorScope for Isolation

**Impact**: Fault tolerance, independent child failures

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

// ✅ CORRECT - collect results with partial failure handling
suspend fun fetchAllData(): AggregatedData = supervisorScope {
    val users = async {
        runCatching { userService.getAll() }.getOrDefault(emptyList())
    }
    val products = async {
        runCatching { productService.getAll() }.getOrDefault(emptyList())
    }
    val orders = async {
        runCatching { orderService.getAll() }.getOrDefault(emptyList())
    }

    AggregatedData(users.await(), products.await(), orders.await())
}
```

#### `scope-lifecycle` - Tie Scope to Lifecycle

**Impact**: Proper resource management, no orphaned coroutines

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

// ✅ CORRECT - request-scoped with Spring
@RestController
class UserController {
    @GetMapping("/users/{id}")
    suspend fun getUser(@PathVariable id: Long): User {
        // Spring creates request-scoped coroutine context
        return userService.getUser(id)
    }
}
```

#### `scope-injection` - Inject CoroutineScope for Testability

**Impact**: Easy testing, flexible dispatcher configuration

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

---

### 3. Flow Patterns (HIGH)

#### `flow-cold` - Understand Flow is Cold

**Impact**: Proper subscription behavior, no unexpected side effects

```kotlin
// ❌ INCORRECT - expecting Flow to run immediately
fun getUpdates(): Flow<Update> = flow {
    println("Starting flow")  // Not printed until collected!
    emit(fetchUpdate())
}

// This doesn't start the flow:
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

    suspend fun emit(event: Event) {
        _events.emit(event)
    }
}
```

#### `flow-operators` - Use Flow Operators Correctly

**Impact**: Efficient transformations, proper backpressure handling

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
        .buffer(capacity = 64)  // buffer if collector is slow
        .map { enrichNotification(it) }
}

// ✅ CORRECT - use conflate for latest-only semantics
fun getPriceUpdates(): Flow<Price> {
    return priceSource.asFlow()
        .conflate()  // keep only latest if collector is slow
}

// ✅ CORRECT - debounce for rate limiting
fun getSearchResults(queries: Flow<String>): Flow<List<Result>> {
    return queries
        .debounce(300)  // wait 300ms of inactivity
        .distinctUntilChanged()
        .flatMapLatest { query ->
            searchService.search(query)
        }
}
```

#### `flow-stateflow` - Use StateFlow for State

**Impact**: Proper state management, UI updates

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

// ✅ CORRECT - expose immutable StateFlow
class ViewModel {
    private val _uiState = MutableStateFlow(UiState.Initial)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    // Never expose MutableStateFlow directly
}
```

#### `flow-sharedflow` - Use SharedFlow for Events

**Impact**: Event broadcasting, multiple subscribers

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

    // For fire-and-forget without suspend
    fun tryPublish(event: AppEvent): Boolean {
        return _events.tryEmit(event)
    }
}

// ✅ CORRECT - replay for late subscribers
@Service
class ConfigService {
    private val _config = MutableSharedFlow<Config>(
        replay = 1  // late subscribers get last value
    )
    val config: SharedFlow<Config> = _config.asSharedFlow()
}
```

#### `flow-flowOn` - Use flowOn for Context Switching

**Impact**: Single context switch point, efficient execution

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
}.flowOn(Dispatchers.Default)  // all upstream on Default

// ✅ CORRECT - multiple flowOn for different stages
fun loadAndProcessData(): Flow<Result> {
    return loadFromDb()
        .flowOn(Dispatchers.IO)  // DB operations on IO
        .map { process(it) }
        .flowOn(Dispatchers.Default)  // processing on Default
}
```

#### `flow-collect` - Collect Safely in Scope

**Impact**: Prevent leaks, proper cancellation

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

    private var job: Job? = null

    fun startListening() {
        job = scope.launch {
            events.collect { handleEvent(it) }
        }
    }

    override fun destroy() {
        job?.cancel()
    }
}

// ✅ CORRECT - use launchIn for cleaner syntax
@Service
class EventListener(
    private val scope: CoroutineScope
) {
    init {
        events
            .onEach { handleEvent(it) }
            .launchIn(scope)
    }
}
```

---

### 4. R2DBC Database (HIGH)

#### `db-r2dbc` - Use R2DBC Not JDBC

**Impact**: Non-blocking database operations

```kotlin
// ❌ INCORRECT - blocking JDBC
@Repository
class UserRepository(
    private val jdbcTemplate: JdbcTemplate
) {
    fun findById(id: Long): User? {
        return jdbcTemplate.queryForObject(...)  // BLOCKS!
    }
}

// ✅ CORRECT - R2DBC with coroutines
@Repository
interface UserRepository : CoroutineCrudRepository<User, Long> {
    suspend fun findByEmail(email: String): User?

    @Query("SELECT * FROM users WHERE status = :status")
    fun findByStatus(status: String): Flow<User>
}

// ✅ CORRECT - configuration
@Configuration
@EnableR2dbcRepositories
class DatabaseConfig : AbstractR2dbcConfiguration() {

    @Bean
    override fun connectionFactory(): ConnectionFactory {
        return ConnectionFactories.get(
            ConnectionFactoryOptions.builder()
                .option(DRIVER, "postgresql")
                .option(HOST, "localhost")
                .option(DATABASE, "mydb")
                .option(USER, "user")
                .option(PASSWORD, "pass")
                .build()
        )
    }
}
```

#### `db-repository` - Use CoroutineCrudRepository

**Impact**: Native coroutine API, clean suspend functions

```kotlin
// ✅ CORRECT - CoroutineCrudRepository for suspend functions
@Repository
interface OrderRepository : CoroutineCrudRepository<Order, Long> {

    // Suspend function for single result
    suspend fun findByOrderNumber(orderNumber: String): Order?

    // Flow for multiple results
    fun findByUserId(userId: Long): Flow<Order>

    // Custom query with suspend
    @Query("SELECT * FROM orders WHERE status = :status LIMIT :limit")
    suspend fun findTopByStatus(status: String, limit: Int): List<Order>
}

// ✅ CORRECT - use in service
@Service
class OrderService(
    private val orderRepository: OrderRepository
) {
    suspend fun getOrder(id: Long): Order {
        return orderRepository.findById(id)
            ?: throw OrderNotFoundException(id)
    }

    fun getUserOrders(userId: Long): Flow<Order> {
        return orderRepository.findByUserId(userId)
    }
}
```

#### `db-transaction` - Handle Transactions Correctly

**Impact**: Data consistency, ACID compliance

```kotlin
// ❌ INCORRECT - no transaction for multiple operations
suspend fun transferMoney(from: Long, to: Long, amount: BigDecimal) {
    val fromAccount = accountRepository.findById(from)!!
    fromAccount.balance -= amount
    accountRepository.save(fromAccount)  // committed

    val toAccount = accountRepository.findById(to)!!  // if this fails, money lost!
    toAccount.balance += amount
    accountRepository.save(toAccount)
}

// ✅ CORRECT - programmatic transaction with coroutines
@Service
class TransferService(
    private val transactionalOperator: TransactionalOperator,
    private val accountRepository: AccountRepository
) {
    suspend fun transferMoney(from: Long, to: Long, amount: BigDecimal) {
        transactionalOperator.executeAndAwait {
            val fromAccount = accountRepository.findById(from)
                ?: throw AccountNotFoundException(from)
            val toAccount = accountRepository.findById(to)
                ?: throw AccountNotFoundException(to)

            if (fromAccount.balance < amount) {
                throw InsufficientFundsException()
            }

            accountRepository.save(fromAccount.copy(balance = fromAccount.balance - amount))
            accountRepository.save(toAccount.copy(balance = toAccount.balance + amount))
        }
    }
}

// ✅ CORRECT - @Transactional with suspend
@Service
class OrderService(
    private val orderRepository: OrderRepository,
    private val inventoryRepository: InventoryRepository
) {
    @Transactional
    suspend fun createOrder(order: Order): Order {
        val savedOrder = orderRepository.save(order)
        inventoryRepository.decrementStock(order.productId, order.quantity)
        return savedOrder
    }
}
```

#### `db-connection-pool` - Configure Connection Pool

**Impact**: Resource efficiency, connection reuse

```kotlin
// ✅ CORRECT - R2DBC pool configuration
@Configuration
class R2dbcConfig {

    @Bean
    fun connectionFactory(): ConnectionFactory {
        val connectionFactory = ConnectionFactories.get(
            ConnectionFactoryOptions.builder()
                .option(DRIVER, "pool")
                .option(PROTOCOL, "postgresql")
                .option(HOST, "localhost")
                .option(DATABASE, "mydb")
                .option(USER, System.getenv("DB_USER"))
                .option(PASSWORD, System.getenv("DB_PASSWORD"))
                .build()
        )

        val poolConfig = ConnectionPoolConfiguration.builder(connectionFactory)
            .maxIdleTime(Duration.ofMinutes(10))
            .maxSize(20)
            .initialSize(5)
            .maxCreateConnectionTime(Duration.ofSeconds(5))
            .validationQuery("SELECT 1")
            .build()

        return ConnectionPool(poolConfig)
    }
}

// application.yml alternative
# spring:
#   r2dbc:
#     url: r2dbc:pool:postgresql://localhost/mydb
#     pool:
#       initial-size: 5
#       max-size: 20
#       max-idle-time: 10m
```

#### `db-n-plus-one` - Avoid N+1 Queries

**Impact**: Query optimization, reduced database load

```kotlin
// ❌ INCORRECT - N+1 queries
suspend fun getUsersWithOrders(): List<UserWithOrders> {
    val users = userRepository.findAll().toList()
    return users.map { user ->
        val orders = orderRepository.findByUserId(user.id).toList()  // N queries!
        UserWithOrders(user, orders)
    }
}

// ✅ CORRECT - batch fetch with join or single query
@Repository
interface UserRepository : CoroutineCrudRepository<User, Long> {

    @Query("""
        SELECT u.*, o.* FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.status = 'ACTIVE'
    """)
    fun findActiveUsersWithOrders(): Flow<UserWithOrders>
}

// ✅ CORRECT - manual batching
suspend fun getUsersWithOrders(): List<UserWithOrders> {
    val users = userRepository.findAll().toList()
    val userIds = users.map { it.id }

    // Single batch query for all orders
    val ordersByUser = orderRepository.findByUserIdIn(userIds)
        .toList()
        .groupBy { it.userId }

    return users.map { user ->
        UserWithOrders(user, ordersByUser[user.id] ?: emptyList())
    }
}
```

#### `db-migration` - Use Flyway/Liquibase

**Impact**: Schema version control, safe migrations

```kotlin
// ✅ CORRECT - Flyway configuration for R2DBC
// build.gradle.kts
dependencies {
    implementation("org.flywaydb:flyway-core")
    runtimeOnly("org.postgresql:postgresql")  // for migrations
}

// application.yml
# spring:
#   flyway:
#     enabled: true
#     locations: classpath:db/migration
#     url: jdbc:postgresql://localhost/mydb  # JDBC for Flyway
#     user: ${DB_USER}
#     password: ${DB_PASSWORD}
#   r2dbc:
#     url: r2dbc:postgresql://localhost/mydb  # R2DBC for app

// ✅ CORRECT - migration script V1__create_users.sql
/*
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
*/
```

---

### 5. Error Handling (HIGH)

#### `err-supervisor` - Use SupervisorJob Correctly

**Impact**: Fault isolation, independent failure handling

```kotlin
// ❌ INCORRECT - SupervisorJob without exception handler
val scope = CoroutineScope(SupervisorJob())

scope.launch {
    throw Exception("Unhandled!")  // crashes the app on Android, logged on server
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

// ✅ CORRECT - handle exceptions in each child
scope.launch {
    try {
        riskyOperation()
    } catch (e: Exception) {
        logger.error("Operation failed", e)
        // handle gracefully
    }
}
```

#### `err-handler` - Use CoroutineExceptionHandler

**Impact**: Centralized error handling for uncaught exceptions

```kotlin
// ✅ CORRECT - global exception handler
@Configuration
class CoroutineExceptionConfig {

    @Bean
    fun coroutineExceptionHandler(): CoroutineExceptionHandler {
        return CoroutineExceptionHandler { context, exception ->
            val name = context[CoroutineName]?.name ?: "unknown"
            logger.error("Coroutine '$name' failed", exception)

            when (exception) {
                is CancellationException -> {
                    // Normal cancellation, don't report
                }
                is NetworkException -> {
                    // Retry logic or user notification
                    retryQueue.add(context)
                }
                else -> {
                    errorReporter.report(exception)
                }
            }
        }
    }

    @Bean
    fun applicationScope(handler: CoroutineExceptionHandler): CoroutineScope {
        return CoroutineScope(SupervisorJob() + Dispatchers.Default + handler)
    }
}
```

#### `err-try-catch` - Catch Exceptions in Coroutines

**Impact**: Proper error recovery, graceful degradation

```kotlin
// ❌ INCORRECT - unhandled exception in async
suspend fun fetchData(): Data = coroutineScope {
    val result = async {
        riskyNetworkCall()  // exception not caught by try-catch below
    }

    try {
        result.await()
    } catch (e: Exception) {
        // This catches, but coroutineScope already cancelled!
        defaultData()
    }
}

// ✅ CORRECT - catch at the source
suspend fun fetchData(): Data = coroutineScope {
    val result = async {
        try {
            riskyNetworkCall()
        } catch (e: Exception) {
            logger.warn("Network call failed, using default", e)
            defaultData()
        }
    }
    result.await()
}

// ✅ CORRECT - use supervisorScope for independent failures
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

// ✅ CORRECT - use runCatching
suspend fun fetchDataSafe(): Result<Data> {
    return runCatching {
        riskyNetworkCall()
    }
}
```

#### `err-cancellation` - Handle CancellationException Properly

**Impact**: Correct cancellation propagation, resource cleanup

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

// ✅ CORRECT - use runCatching which handles this
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

// ✅ CORRECT - cleanup with try-finally
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

#### `err-flow-catch` - Use catch Operator in Flow

**Impact**: Flow error handling without breaking collection

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
    emit(Update.error(e.message))  // emit error state
}

// ✅ CORRECT - retry on error
fun getUpdates(): Flow<Update> = flow {
    val update = fetchUpdate()
    emit(update)
}.retry(3) { e ->
    e is NetworkException  // retry only network errors
}.catch { e ->
    emit(Update.error("Failed after retries"))
}

// ✅ CORRECT - onEach for side effects, catch for errors
fun processNotifications(): Flow<Notification> {
    return notificationSource
        .onEach { notification ->
            analyticsService.track(notification)
        }
        .catch { e ->
            logger.error("Notification processing failed", e)
            // don't emit, just log
        }
}
```

#### `err-retry` - Implement Retry with Backoff

**Impact**: Resilience for transient failures

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
            logger.warn("Attempt ${attempt + 1} failed, retrying in ${currentDelay}ms", e)
        }
        delay(currentDelay)
        currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
    }
    return block()  // last attempt, let it throw
}

// Usage
suspend fun fetchDataWithRetry(): Data {
    return retryWithBackoff(maxRetries = 3) {
        apiClient.fetchData()
    }
}

// ✅ CORRECT - retry in Flow
fun getDataStream(): Flow<Data> = flow {
    while (currentCoroutineContext().isActive) {
        emit(fetchData())
        delay(5000)
    }
}.retryWhen { cause, attempt ->
    if (cause is NetworkException && attempt < 3) {
        delay(1000L * (attempt + 1))
        true  // retry
    } else {
        false  // give up
    }
}
```

---

### 6. Spring WebFlux (MEDIUM)

#### `webflux-controller` - Use Suspend in Controllers

**Impact**: Non-blocking endpoints, efficient resource use

```kotlin
// ✅ CORRECT - suspend function in controller
@RestController
@RequestMapping("/api/users")
class UserController(
    private val userService: UserService
) {
    @GetMapping("/{id}")
    suspend fun getUser(@PathVariable id: Long): User {
        return userService.findById(id)
            ?: throw ResponseStatusException(HttpStatus.NOT_FOUND)
    }

    @GetMapping
    fun getAllUsers(): Flow<User> {  // Flow for streaming
        return userService.findAll()
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun createUser(@RequestBody user: User): User {
        return userService.save(user)
    }
}
```

#### `webflux-coRouter` - Use coRouter DSL

**Impact**: Coroutine-friendly functional routing

```kotlin
// ✅ CORRECT - coRouter for functional endpoints
@Configuration
class RouterConfig(
    private val userHandler: UserHandler
) {
    @Bean
    fun userRoutes() = coRouter {
        "/api/users".nest {
            GET("", userHandler::getAllUsers)
            GET("/{id}", userHandler::getUser)
            POST("", userHandler::createUser)
            PUT("/{id}", userHandler::updateUser)
            DELETE("/{id}", userHandler::deleteUser)
        }

        filter { request, next ->
            // logging filter
            val start = System.currentTimeMillis()
            val response = next(request)
            val duration = System.currentTimeMillis() - start
            logger.info("${request.method()} ${request.path()} - ${duration}ms")
            response
        }
    }
}

@Component
class UserHandler(
    private val userService: UserService
) {
    suspend fun getUser(request: ServerRequest): ServerResponse {
        val id = request.pathVariable("id").toLong()
        val user = userService.findById(id)
        return if (user != null) {
            ServerResponse.ok().bodyValueAndAwait(user)
        } else {
            ServerResponse.notFound().buildAndAwait()
        }
    }

    suspend fun getAllUsers(request: ServerRequest): ServerResponse {
        val users = userService.findAll()
        return ServerResponse.ok().bodyAndAwait(users)
    }
}
```

#### `webflux-webclient` - Use WebClient with awaitBody

**Impact**: Non-blocking HTTP client calls

```kotlin
// ✅ CORRECT - WebClient with coroutine extensions
@Service
class ExternalApiService(
    private val webClient: WebClient
) {
    suspend fun fetchUser(userId: String): ExternalUser {
        return webClient.get()
            .uri("/users/{id}", userId)
            .retrieve()
            .awaitBody()
    }

    suspend fun fetchUserOrNull(userId: String): ExternalUser? {
        return webClient.get()
            .uri("/users/{id}", userId)
            .retrieve()
            .awaitBodyOrNull()
    }

    suspend fun createUser(user: ExternalUser): ExternalUser {
        return webClient.post()
            .uri("/users")
            .bodyValue(user)
            .retrieve()
            .awaitBody()
    }

    // Stream response
    fun fetchUsers(): Flow<ExternalUser> {
        return webClient.get()
            .uri("/users")
            .retrieve()
            .bodyToFlow()
    }
}

// ✅ CORRECT - WebClient configuration
@Configuration
class WebClientConfig {
    @Bean
    fun webClient(): WebClient {
        return WebClient.builder()
            .baseUrl("https://api.example.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .filter(ExchangeFilterFunction.ofRequestProcessor { request ->
                logger.debug("Request: ${request.method()} ${request.url()}")
                Mono.just(request)
            })
            .build()
    }
}
```

#### `webflux-context` - Propagate ReactorContext

**Impact**: Observability, tracing, MDC propagation

```kotlin
// ✅ CORRECT - context propagation in Spring Boot 4
// application.properties: spring.reactor.context-propagation=auto

// For earlier versions or custom context
@Configuration
class ContextPropagationConfig {
    @Bean
    fun contextPropagationHook(): Hooks.OnEachOperator {
        return { publisher ->
            if (publisher is Mono<*>) {
                publisher.contextWrite { ctx ->
                    // Copy MDC to reactor context
                    val mdc = MDC.getCopyOfContextMap() ?: emptyMap()
                    ctx.putAll(mdc.mapKeys { (k, _) -> k })
                }
            } else {
                publisher
            }
        }
    }
}

// ✅ CORRECT - propagate context in coroutines
suspend fun <T> withMdcContext(block: suspend () -> T): T {
    return withContext(MDCContext()) {
        block()
    }
}

@GetMapping("/traced")
suspend fun tracedEndpoint(): Response {
    return withMdcContext {
        MDC.put("requestId", UUID.randomUUID().toString())
        logger.info("Processing request")  // MDC available
        service.process()
    }
}
```

#### `webflux-response` - Return Proper Types

**Impact**: Efficient serialization, proper HTTP semantics

```kotlin
// ✅ CORRECT - return appropriate types
@RestController
class ApiController(
    private val itemService: ItemService
) {
    // Single item - suspend function
    @GetMapping("/items/{id}")
    suspend fun getItem(@PathVariable id: Long): ResponseEntity<Item> {
        val item = itemService.findById(id)
        return if (item != null) {
            ResponseEntity.ok(item)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    // Multiple items - Flow for streaming
    @GetMapping("/items", produces = [MediaType.APPLICATION_NDJSON_VALUE])
    fun getItems(): Flow<Item> {
        return itemService.findAll()
    }

    // Server-Sent Events
    @GetMapping("/items/stream", produces = [MediaType.TEXT_EVENT_STREAM_VALUE])
    fun streamItems(): Flow<ServerSentEvent<Item>> {
        return itemService.findAll().map { item ->
            ServerSentEvent.builder(item)
                .id(item.id.toString())
                .event("item")
                .build()
        }
    }

    // No content response
    @DeleteMapping("/items/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    suspend fun deleteItem(@PathVariable id: Long) {
        itemService.delete(id)
    }
}
```

#### `webflux-filter` - Use CoWebFilter

**Impact**: Coroutine-aware request filtering

```kotlin
// ✅ CORRECT - CoWebFilter for coroutine-based filtering
@Component
class LoggingFilter : CoWebFilter() {

    override suspend fun filter(exchange: ServerWebExchange, chain: CoWebFilterChain) {
        val request = exchange.request
        val start = System.currentTimeMillis()
        val requestId = UUID.randomUUID().toString()

        // Add request ID to context
        exchange.attributes["requestId"] = requestId

        try {
            chain.filter(exchange)
        } finally {
            val duration = System.currentTimeMillis() - start
            logger.info(
                "[$requestId] ${request.method} ${request.path} - ${duration}ms"
            )
        }
    }
}

// ✅ CORRECT - authentication filter
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
class AuthenticationFilter(
    private val tokenService: TokenService
) : CoWebFilter() {

    override suspend fun filter(exchange: ServerWebExchange, chain: CoWebFilterChain) {
        val token = exchange.request.headers.getFirst(HttpHeaders.AUTHORIZATION)
            ?.removePrefix("Bearer ")

        if (token != null) {
            val user = tokenService.validateAndGetUser(token)
            if (user != null) {
                exchange.attributes["currentUser"] = user
            }
        }

        chain.filter(exchange)
    }
}
```

---

### 7. Security (MEDIUM)

#### `sec-reactive` - Use ReactiveSecurityContextHolder

**Impact**: Reactive-compatible security context access

```kotlin
// ❌ INCORRECT - blocking SecurityContextHolder
suspend fun getCurrentUser(): User {
    val auth = SecurityContextHolder.getContext().authentication  // May be empty!
    return auth.principal as User
}

// ✅ CORRECT - ReactiveSecurityContextHolder with coroutines
suspend fun getCurrentUser(): User {
    return ReactiveSecurityContextHolder.getContext()
        .awaitSingleOrNull()
        ?.authentication
        ?.principal as? User
        ?: throw UnauthorizedException()
}

// ✅ CORRECT - as extension function
suspend fun <T : Principal> ReactiveSecurityContextHolder.currentUserOrNull(): T? {
    return getContext()
        .awaitSingleOrNull()
        ?.authentication
        ?.principal as? T
}

// Usage
@GetMapping("/me")
suspend fun getProfile(): UserProfile {
    val user = ReactiveSecurityContextHolder.currentUserOrNull<User>()
        ?: throw ResponseStatusException(HttpStatus.UNAUTHORIZED)
    return userService.getProfile(user.id)
}
```

#### `sec-method` - Use @PreAuthorize with Suspend

**Impact**: Method-level security on suspend functions

```kotlin
// ✅ CORRECT - enable reactive method security
@Configuration
@EnableReactiveMethodSecurity
class SecurityConfig

// ✅ CORRECT - @PreAuthorize on suspend functions
@Service
class AdminService {

    @PreAuthorize("hasRole('ADMIN')")
    suspend fun deleteUser(userId: Long) {
        userRepository.deleteById(userId)
    }

    @PreAuthorize("hasRole('ADMIN') or #userId == principal.id")
    suspend fun updateUser(userId: Long, update: UserUpdate): User {
        return userRepository.update(userId, update)
    }

    @PreAuthorize("@permissionService.canAccess(principal, #resourceId)")
    suspend fun accessResource(resourceId: Long): Resource {
        return resourceRepository.findById(resourceId)
    }
}
```

#### `sec-context-propagation` - Propagate SecurityContext

**Impact**: Security context available across async boundaries

```kotlin
// ✅ CORRECT - propagate security context to coroutines
@Configuration
class SecurityContextConfig {

    @Bean
    fun securityContextCoroutineContext(): CoroutineContext {
        return ReactorContext(
            Context.of(SecurityContext::class.java,
                ReactiveSecurityContextHolder.getContext())
        )
    }
}

// ✅ CORRECT - custom context element for security
class SecurityContextElement(
    val securityContext: SecurityContext
) : AbstractCoroutineContextElement(Key) {
    companion object Key : CoroutineContext.Key<SecurityContextElement>
}

suspend fun withSecurityContext(block: suspend () -> Unit) {
    val securityContext = ReactiveSecurityContextHolder.getContext()
        .awaitSingleOrNull()

    if (securityContext != null) {
        withContext(SecurityContextElement(securityContext)) {
            block()
        }
    } else {
        block()
    }
}
```

#### `sec-jwt` - Implement JWT Properly

**Impact**: Stateless authentication, token validation

```kotlin
// ✅ CORRECT - JWT configuration for WebFlux
@Configuration
@EnableWebFluxSecurity
class SecurityConfig {

    @Bean
    fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
        return http
            .csrf { it.disable() }
            .httpBasic { it.disable() }
            .formLogin { it.disable() }
            .authorizeExchange { auth ->
                auth.pathMatchers("/api/auth/**").permitAll()
                auth.pathMatchers("/api/admin/**").hasRole("ADMIN")
                auth.anyExchange().authenticated()
            }
            .oauth2ResourceServer { oauth2 ->
                oauth2.jwt { jwt ->
                    jwt.jwtAuthenticationConverter(jwtAuthConverter())
                }
            }
            .build()
    }

    @Bean
    fun jwtAuthConverter(): ReactiveJwtAuthenticationConverter {
        val converter = ReactiveJwtAuthenticationConverter()
        converter.setJwtGrantedAuthoritiesConverter { jwt ->
            val roles = jwt.getClaimAsStringList("roles") ?: emptyList()
            Flux.fromIterable(roles.map { SimpleGrantedAuthority("ROLE_$it") })
        }
        return converter
    }
}

// ✅ CORRECT - JWT token service
@Service
class JwtTokenService(
    @Value("\${jwt.secret}") private val secret: String,
    @Value("\${jwt.expiration}") private val expiration: Long
) {
    private val key = Keys.hmacShaKeyFor(secret.toByteArray())

    fun generateToken(user: User): String {
        val now = Date()
        val expiryDate = Date(now.time + expiration)

        return Jwts.builder()
            .setSubject(user.id.toString())
            .claim("email", user.email)
            .claim("roles", user.roles)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(key, SignatureAlgorithm.HS256)
            .compact()
    }

    suspend fun validateToken(token: String): User? {
        return try {
            val claims = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .body

            val userId = claims.subject.toLong()
            userRepository.findById(userId)
        } catch (e: Exception) {
            null
        }
    }
}
```

#### `sec-cors` - Configure CORS Correctly

**Impact**: Cross-origin security for SPAs

```kotlin
// ✅ CORRECT - CORS configuration for WebFlux
@Configuration
class CorsConfig {

    @Bean
    fun corsConfigurationSource(): CorsConfigurationSource {
        val configuration = CorsConfiguration().apply {
            allowedOrigins = listOf(
                "https://myapp.com",
                "https://staging.myapp.com"
            )
            allowedMethods = listOf("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
            allowedHeaders = listOf(
                HttpHeaders.AUTHORIZATION,
                HttpHeaders.CONTENT_TYPE,
                "X-Request-ID"
            )
            exposedHeaders = listOf("X-Total-Count", "X-Page-Count")
            allowCredentials = true
            maxAge = 3600
        }

        return UrlBasedCorsConfigurationSource().apply {
            registerCorsConfiguration("/api/**", configuration)
        }
    }
}

// In SecurityConfig
@Bean
fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
    return http
        .cors { it.configurationSource(corsConfigurationSource()) }
        // ... rest of config
        .build()
}
```

#### `sec-csrf` - Handle CSRF in WebFlux

**Impact**: Request forgery protection

```kotlin
// ✅ CORRECT - CSRF for stateless APIs (typically disabled)
@Configuration
@EnableWebFluxSecurity
class SecurityConfig {

    @Bean
    fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
        return http
            // For stateless JWT APIs, CSRF is typically disabled
            .csrf { it.disable() }
            // ... rest of config
            .build()
    }
}

// ✅ CORRECT - CSRF for stateful apps with cookies
@Configuration
@EnableWebFluxSecurity
class StatefulSecurityConfig {

    @Bean
    fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
        return http
            .csrf { csrf ->
                csrf.csrfTokenRepository(
                    CookieServerCsrfTokenRepository.withHttpOnlyFalse()
                )
            }
            // ... rest of config
            .build()
    }
}
```

---

### 8. Testing (MEDIUM)

#### `test-runTest` - Use runTest for Coroutines

**Impact**: Proper test execution, virtual time control

```kotlin
// ✅ CORRECT - use runTest for coroutine tests
class UserServiceTest {

    private val userRepository = mockk<UserRepository>()
    private val userService = UserService(userRepository)

    @Test
    fun `should return user by id`() = runTest {
        // Given
        val user = User(1L, "test@example.com")
        coEvery { userRepository.findById(1L) } returns user

        // When
        val result = userService.getUser(1L)

        // Then
        assertEquals(user, result)
        coVerify { userRepository.findById(1L) }
    }

    @Test
    fun `should handle delay correctly`() = runTest {
        // Given
        coEvery { userRepository.findById(any()) } coAnswers {
            delay(1000)  // Virtual time - completes instantly
            User(1L, "test@example.com")
        }

        // When
        val result = userService.getUser(1L)

        // Then
        assertNotNull(result)
        // Test completes instantly despite 1000ms delay
    }
}
```

#### `test-mockk` - Use MockK coEvery/coVerify

**Impact**: Suspend function mocking, clean test syntax

```kotlin
// ✅ CORRECT - MockK for coroutine mocking
class OrderServiceTest {

    private val orderRepository = mockk<OrderRepository>()
    private val paymentService = mockk<PaymentService>()
    private val orderService = OrderService(orderRepository, paymentService)

    @Test
    fun `should create order with payment`() = runTest {
        // Given
        val order = Order(productId = 1L, quantity = 2)
        val savedOrder = order.copy(id = 1L)

        coEvery { orderRepository.save(any()) } returns savedOrder
        coEvery { paymentService.processPayment(any()) } returns PaymentResult.SUCCESS

        // When
        val result = orderService.createOrder(order)

        // Then
        assertEquals(1L, result.id)

        coVerify(exactly = 1) { orderRepository.save(order) }
        coVerify(exactly = 1) { paymentService.processPayment(savedOrder) }
    }

    @Test
    fun `should handle payment failure`() = runTest {
        // Given
        coEvery { orderRepository.save(any()) } returns Order(id = 1L)
        coEvery { paymentService.processPayment(any()) } throws PaymentException("Failed")

        // When/Then
        assertThrows<PaymentException> {
            orderService.createOrder(Order())
        }
    }
}
```

#### `test-turbine` - Use Turbine for Flow Testing

**Impact**: Clean Flow assertions, timeout handling

```kotlin
// build.gradle.kts
// testImplementation("app.cash.turbine:turbine:1.0.0")

// ✅ CORRECT - Turbine for Flow testing
class EventServiceTest {

    private val eventService = EventService()

    @Test
    fun `should emit events in order`() = runTest {
        eventService.events.test {
            // Trigger events
            eventService.emit(Event("first"))
            eventService.emit(Event("second"))

            // Assert emissions
            assertEquals(Event("first"), awaitItem())
            assertEquals(Event("second"), awaitItem())

            // Cancel and ensure no more events
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `should complete flow`() = runTest {
        val flow = flowOf(1, 2, 3)

        flow.test {
            assertEquals(1, awaitItem())
            assertEquals(2, awaitItem())
            assertEquals(3, awaitItem())
            awaitComplete()
        }
    }

    @Test
    fun `should handle flow errors`() = runTest {
        val errorFlow = flow {
            emit(1)
            throw RuntimeException("Error")
        }

        errorFlow.test {
            assertEquals(1, awaitItem())
            val error = awaitError()
            assertEquals("Error", error.message)
        }
    }
}
```

#### `test-dispatcher` - Use TestDispatcher

**Impact**: Deterministic tests, controlled execution

```kotlin
// ✅ CORRECT - TestDispatcher for controlled execution
class TimerServiceTest {

    @Test
    fun `should emit at intervals`() = runTest {
        val testDispatcher = StandardTestDispatcher(testScheduler)
        val timerService = TimerService(testDispatcher)

        val emissions = mutableListOf<Long>()
        val job = launch {
            timerService.ticker(1000).take(3).collect { emissions.add(it) }
        }

        // Advance time manually
        advanceTimeBy(3000)
        runCurrent()

        assertEquals(3, emissions.size)
        job.cancel()
    }

    @Test
    fun `should use UnconfinedTestDispatcher for immediate execution`() = runTest {
        val testDispatcher = UnconfinedTestDispatcher(testScheduler)

        var executed = false
        launch(testDispatcher) {
            executed = true
        }

        assertTrue(executed)  // Executed immediately
    }
}

// ✅ CORRECT - inject dispatcher for testability
class DataRefresher(
    private val dispatcher: CoroutineDispatcher = Dispatchers.Default
) {
    suspend fun refresh() = withContext(dispatcher) {
        // ...
    }
}

// In test
@Test
fun `should refresh data`() = runTest {
    val refresher = DataRefresher(StandardTestDispatcher(testScheduler))
    refresher.refresh()
    advanceUntilIdle()
    // assertions
}
```

#### `test-webclient` - Test with WebTestClient

**Impact**: Integration testing for WebFlux endpoints

```kotlin
// ✅ CORRECT - WebTestClient for integration tests
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserControllerIntegrationTest {

    @Autowired
    lateinit var webTestClient: WebTestClient

    @Test
    fun `should get user by id`() {
        webTestClient.get()
            .uri("/api/users/1")
            .exchange()
            .expectStatus().isOk
            .expectBody<User>()
            .consumeWith { result ->
                val user = result.responseBody!!
                assertEquals(1L, user.id)
            }
    }

    @Test
    fun `should create user`() {
        val newUser = UserCreate("test@example.com", "Test User")

        webTestClient.post()
            .uri("/api/users")
            .bodyValue(newUser)
            .exchange()
            .expectStatus().isCreated
            .expectBody<User>()
            .consumeWith { result ->
                val user = result.responseBody!!
                assertNotNull(user.id)
                assertEquals("test@example.com", user.email)
            }
    }

    @Test
    fun `should return 404 for missing user`() {
        webTestClient.get()
            .uri("/api/users/999")
            .exchange()
            .expectStatus().isNotFound
    }

    // ✅ CORRECT - test Flow endpoints
    @Test
    fun `should stream users`() {
        webTestClient.get()
            .uri("/api/users/stream")
            .accept(MediaType.APPLICATION_NDJSON)
            .exchange()
            .expectStatus().isOk
            .returnResult<User>()
            .responseBody
            .test()
            .expectNextCount(10)
            .verifyComplete()
    }
}
```

#### `test-container` - Use Testcontainers

**Impact**: Real database testing, production-like tests

```kotlin
// build.gradle.kts
// testImplementation("org.testcontainers:postgresql:1.19.0")
// testImplementation("org.testcontainers:r2dbc:1.19.0")

// ✅ CORRECT - Testcontainers with R2DBC
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    companion object {
        @Container
        val postgres = PostgreSQLContainer("postgres:15-alpine")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test")

        @JvmStatic
        @DynamicPropertySource
        fun properties(registry: DynamicPropertyRegistry) {
            registry.add("spring.r2dbc.url") {
                "r2dbc:postgresql://${postgres.host}:${postgres.getMappedPort(5432)}/${postgres.databaseName}"
            }
            registry.add("spring.r2dbc.username") { postgres.username }
            registry.add("spring.r2dbc.password") { postgres.password }
            registry.add("spring.flyway.url") { postgres.jdbcUrl }
            registry.add("spring.flyway.user") { postgres.username }
            registry.add("spring.flyway.password") { postgres.password }
        }
    }

    @Autowired
    lateinit var userRepository: UserRepository

    @Test
    fun `should save and retrieve user`() = runTest {
        // Given
        val user = User(email = "test@example.com", name = "Test User")

        // When
        val saved = userRepository.save(user)
        val retrieved = userRepository.findById(saved.id!!)

        // Then
        assertNotNull(retrieved)
        assertEquals("test@example.com", retrieved?.email)
    }

    @Test
    fun `should find users by email`() = runTest {
        // Given
        userRepository.save(User(email = "find@example.com", name = "Find Me"))

        // When
        val found = userRepository.findByEmail("find@example.com")

        // Then
        assertNotNull(found)
        assertEquals("Find Me", found?.name)
    }
}
```

---

## Project Structure

```
src/
├── main/kotlin/com/example/
│   ├── Application.kt              # Main application
│   ├── config/
│   │   ├── CoroutineConfig.kt     # Coroutine scope beans
│   │   ├── R2dbcConfig.kt         # Database configuration
│   │   ├── SecurityConfig.kt      # Security configuration
│   │   └── WebClientConfig.kt     # HTTP client configuration
│   ├── controller/
│   │   └── UserController.kt      # REST controllers
│   ├── domain/
│   │   └── User.kt                # Domain entities
│   ├── repository/
│   │   └── UserRepository.kt      # R2DBC repositories
│   ├── service/
│   │   └── UserService.kt         # Business logic
│   └── exception/
│       └── Exceptions.kt          # Custom exceptions
├── main/resources/
│   ├── application.yml            # Configuration
│   └── db/migration/              # Flyway migrations
└── test/kotlin/com/example/
    ├── controller/
    │   └── UserControllerTest.kt
    ├── service/
    │   └── UserServiceTest.kt
    └── repository/
        └── UserRepositoryTest.kt
```

## Integration Workflow

When implementing Kotlin Coroutine + Spring features:

1. **Before implementation**: Review relevant rule categories
2. **During development**: Apply patterns from quick reference
3. **Code review**: Verify against rule checklist
4. **Performance issues**: Consult detailed rules for solutions

```
coroutine-* rules → Proper suspend functions, no blocking
    ↓
scope-* rules → Structured concurrency, no GlobalScope
    ↓
flow-* rules → Correct Flow patterns and operators
    ↓
db-* rules → R2DBC, transactions, N+1 prevention
    ↓
err-* rules → SupervisorJob, proper exception handling
    ↓
webflux-* rules → Non-blocking endpoints, context propagation
    ↓
sec-* rules → Reactive security, JWT, context
    ↓
test-* rules → runTest, MockK, Turbine
```

## Compliance Checklist

Before submitting Kotlin Coroutine + Spring code:

- [ ] No blocking calls in suspend functions (`coroutine-blocking`)
- [ ] Correct dispatcher for CPU vs IO (`coroutine-dispatcher`)
- [ ] No GlobalScope usage (`scope-no-global`)
- [ ] Structured concurrency with coroutineScope/supervisorScope (`scope-structured`)
- [ ] StateFlow/SharedFlow used appropriately (`flow-stateflow`, `flow-sharedflow`)
- [ ] R2DBC with CoroutineCrudRepository (`db-r2dbc`, `db-repository`)
- [ ] Transactions handled correctly (`db-transaction`)
- [ ] CancellationException rethrown (`err-cancellation`)
- [ ] SupervisorJob with exception handler (`err-supervisor`)
- [ ] Security context propagated (`sec-context-propagation`)
- [ ] Tests use runTest with MockK (`test-runTest`, `test-mockk`)
