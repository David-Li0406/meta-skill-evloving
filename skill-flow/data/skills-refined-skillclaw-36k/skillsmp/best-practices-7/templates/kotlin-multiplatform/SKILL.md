---
name: best-practices
description: Kotlin Multiplatform performance optimization and clean architecture patterns. This skill should be used when writing, reviewing, or refactoring KMP code to ensure optimal performance patterns. Triggers on tasks involving Compose Multiplatform, Ktor client, Koin DI, coroutines, or platform-specific code.
license: MIT
metadata:
  author: devnogari
  project_type: kotlin-multiplatform
---

# Kotlin Multiplatform Best Practices

Comprehensive performance optimization guide for Kotlin Multiplatform (KMP) applications with Compose Multiplatform, Ktor, and Koin. Contains 44 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing Compose Multiplatform UI components
- Implementing state management with StateFlow/MutableStateFlow
- Setting up Koin dependency injection modules
- Writing Ktor client HTTP requests
- Creating expect/actual platform abstractions
- Managing coroutine scopes and structured concurrency
- Implementing ViewModel patterns
- Writing tests for Compose and coroutines

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Compose State | CRITICAL | `compose-state-` |
| 2 | Coroutines | CRITICAL | `coroutine-` |
| 3 | Koin DI | CRITICAL | `koin-` |
| 4 | Ktor Client | HIGH | `ktor-` |
| 5 | Expect/Actual | HIGH | `expect-` |
| 6 | ViewModel | HIGH | `viewmodel-` |
| 7 | Navigation | MEDIUM | `nav-` |
| 8 | Testing | MEDIUM | `test-` |

## Quick Reference

### 1. Compose State (CRITICAL)

- `compose-state-flow` - Use StateFlow with collectAsState for reactive UI
- `compose-state-remember` - Use remember/rememberSaveable correctly
- `compose-state-effect` - Use LaunchedEffect/DisposableEffect properly
- `compose-state-derived` - Use derivedStateOf for computed values
- `compose-state-stable` - Mark classes with @Stable/@Immutable
- `compose-state-key` - Use key() to preserve state across recompositions

### 2. Coroutines (CRITICAL)

- `coroutine-scope` - Use appropriate coroutine scope hierarchy
- `coroutine-structured` - Follow structured concurrency principles
- `coroutine-cancel` - Handle cancellation properly
- `coroutine-exception` - Use CoroutineExceptionHandler correctly
- `coroutine-dispatcher` - Use correct dispatchers (Main, IO, Default)
- `coroutine-flow` - Use Flow operators correctly (stateIn, shareIn)

### 3. Koin DI (CRITICAL)

- `koin-module` - Organize modules by feature/layer
- `koin-scope` - Use proper scoping (single, factory, viewModel)
- `koin-inject` - Inject dependencies correctly in Compose
- `koin-qualifier` - Use named qualifiers for disambiguation
- `koin-lazy` - Use lazy injection for optional dependencies
- `koin-test` - Mock dependencies properly in tests

### 4. Ktor Client (HIGH)

- `ktor-client` - Configure HttpClient properly
- `ktor-error` - Handle HTTP errors and exceptions
- `ktor-serialization` - Configure JSON serialization correctly
- `ktor-timeout` - Set appropriate timeouts
- `ktor-retry` - Implement retry logic for transient failures
- `ktor-logging` - Configure request/response logging

### 5. Expect/Actual (HIGH)

- `expect-interface` - Prefer interfaces over expect/actual when possible
- `expect-minimal` - Keep expect declarations minimal
- `expect-default` - Provide default implementations where appropriate
- `expect-platform` - Use platform-specific optimizations
- `expect-test` - Test platform implementations independently

### 6. ViewModel (HIGH)

- `viewmodel-state` - Use sealed class/interface for UI state
- `viewmodel-event` - Separate one-time events from state
- `viewmodel-loading` - Handle loading/error/success states
- `viewmodel-scope` - Use viewModelScope for coroutines
- `viewmodel-save` - Save/restore state across process death

### 7. Navigation (MEDIUM)

- `nav-typesafe` - Use type-safe navigation arguments
- `nav-deeplink` - Handle deep links correctly
- `nav-backstack` - Manage back stack properly
- `nav-result` - Pass results between screens safely
- `nav-compose` - Integrate with Compose navigation

### 8. Testing (MEDIUM)

- `test-compose` - Write Compose UI tests correctly
- `test-coroutine` - Test coroutines with TestDispatcher
- `test-flow` - Test Flow emissions with Turbine
- `test-koin` - Setup Koin for testing
- `test-ktor` - Mock Ktor client responses

---

## Detailed Rules

### 1. Compose State (CRITICAL)

#### `compose-state-flow` - Use StateFlow with collectAsState

StateFlow provides lifecycle-aware state collection that survives recomposition. Always use collectAsState() in composables.

**Incorrect (using mutableStateOf in ViewModel):**

```kotlin
class UserViewModel : ViewModel() {
    // Wrong: mutableStateOf is not lifecycle-aware
    var user by mutableStateOf<User?>(null)
        private set

    fun loadUser() {
        viewModelScope.launch {
            user = repository.getUser()
        }
    }
}

@Composable
fun UserScreen(viewModel: UserViewModel) {
    // Direct access to mutableStateOf
    val user = viewModel.user
}
```

**Correct (using StateFlow):**

```kotlin
class UserViewModel : ViewModel() {
    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    fun loadUser() {
        viewModelScope.launch {
            _user.value = repository.getUser()
        }
    }
}

@Composable
fun UserScreen(viewModel: UserViewModel) {
    val user by viewModel.user.collectAsState()

    user?.let { UserContent(it) }
}
```

**Impact:** Lifecycle-aware collection, proper state restoration, thread safety.

---

#### `compose-state-remember` - Use remember/rememberSaveable correctly

Use remember for expensive calculations, rememberSaveable for state that survives configuration changes.

**Incorrect (recreating expensive objects):**

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    // Wrong: Recalculated on every recomposition
    val sortedItems = items.sortedBy { it.name }
    val filteredItems = sortedItems.filter { it.isActive }

    LazyColumn {
        items(filteredItems) { item ->
            ItemRow(item)
        }
    }
}
```

**Correct (using remember with keys):**

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    // Recalculated only when items change
    val processedItems = remember(items) {
        items.filter { it.isActive }.sortedBy { it.name }
    }

    // Survives configuration changes
    var searchQuery by rememberSaveable { mutableStateOf("") }

    val filteredItems = remember(processedItems, searchQuery) {
        if (searchQuery.isEmpty()) processedItems
        else processedItems.filter { it.name.contains(searchQuery, ignoreCase = true) }
    }

    LazyColumn {
        items(filteredItems, key = { it.id }) { item ->
            ItemRow(item)
        }
    }
}
```

**Impact:** 2-10x reduction in unnecessary calculations.

---

#### `compose-state-effect` - Use LaunchedEffect/DisposableEffect properly

Use LaunchedEffect for suspending operations, DisposableEffect for cleanup.

**Incorrect (side effects in composition):**

```kotlin
@Composable
fun AnalyticsScreen(screenName: String, viewModel: AnalyticsViewModel) {
    // Wrong: Runs on every recomposition!
    viewModel.trackScreenView(screenName)

    // Wrong: No cleanup for listener
    val listener = object : SomeListener {
        override fun onEvent(event: Event) { /* handle */ }
    }
    someService.addListener(listener)
}
```

**Correct (using effects):**

```kotlin
@Composable
fun AnalyticsScreen(screenName: String, viewModel: AnalyticsViewModel) {
    // Runs once when screenName changes
    LaunchedEffect(screenName) {
        viewModel.trackScreenView(screenName)
    }

    // Cleanup when composable leaves composition
    DisposableEffect(Unit) {
        val listener = object : SomeListener {
            override fun onEvent(event: Event) { /* handle */ }
        }
        someService.addListener(listener)

        onDispose {
            someService.removeListener(listener)
        }
    }
}
```

---

#### `compose-state-derived` - Use derivedStateOf for computed values

Use derivedStateOf when you need computed state that only updates when dependencies change.

**Incorrect (recalculating on every recomposition):**

```kotlin
@Composable
fun ShoppingCart(items: List<CartItem>) {
    // Recalculates every recomposition even if items unchanged
    val totalPrice = items.sumOf { it.price * it.quantity }
    val itemCount = items.sumOf { it.quantity }

    Text("Total: $$totalPrice ($itemCount items)")
}
```

**Correct (using derivedStateOf):**

```kotlin
@Composable
fun ShoppingCart(items: List<CartItem>) {
    val totalPrice by remember {
        derivedStateOf { items.sumOf { it.price * it.quantity } }
    }
    val itemCount by remember {
        derivedStateOf { items.sumOf { it.quantity } }
    }

    Text("Total: $$totalPrice ($itemCount items)")
}
```

---

#### `compose-state-stable` - Mark classes with @Stable/@Immutable

Mark data classes as @Stable or @Immutable to enable Compose compiler optimizations.

**Incorrect (unstable parameters cause recomposition):**

```kotlin
// Without annotations, Compose assumes this is unstable
data class User(
    val id: String,
    val name: String,
    val avatar: String
)

@Composable
fun UserCard(user: User) {
    // Recomposes even when user hasn't changed
    Card {
        Text(user.name)
        AsyncImage(user.avatar)
    }
}
```

**Correct (marking as Immutable):**

```kotlin
@Immutable
data class User(
    val id: String,
    val name: String,
    val avatar: String
)

// Or for mutable but stable types
@Stable
class UserState(
    val user: User,
    private var _isLoading: Boolean = false
) {
    val isLoading: Boolean get() = _isLoading
}

@Composable
fun UserCard(user: User) {
    // Skips recomposition when user is the same instance
    Card {
        Text(user.name)
        AsyncImage(user.avatar)
    }
}
```

**Impact:** 50-90% reduction in unnecessary recompositions.

---

#### `compose-state-key` - Use key() to preserve state across recompositions

Use key() composable to maintain identity and state when items change position.

**Incorrect (state lost when items reorder):**

```kotlin
@Composable
fun TodoList(items: List<TodoItem>) {
    Column {
        items.forEach { item ->
            // State lost when items reorder
            TodoItemRow(item)
        }
    }
}
```

**Correct (using key for identity):**

```kotlin
@Composable
fun TodoList(items: List<TodoItem>) {
    Column {
        items.forEach { item ->
            key(item.id) {
                TodoItemRow(item)
            }
        }
    }
}

// Or with LazyColumn (preferred for long lists)
@Composable
fun TodoList(items: List<TodoItem>) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            TodoItemRow(item)
        }
    }
}
```

---

### 2. Coroutines (CRITICAL)

#### `coroutine-scope` - Use appropriate coroutine scope hierarchy

Use proper scope hierarchy: viewModelScope for ViewModels, rememberCoroutineScope for Compose.

**Incorrect (creating unmanaged scopes):**

```kotlin
class DataRepository {
    // Wrong: Unmanaged scope, will leak
    private val scope = CoroutineScope(Dispatchers.IO)

    fun fetchData() {
        scope.launch {
            // Work that won't be cancelled properly
        }
    }
}
```

**Correct (managed scope hierarchy):**

```kotlin
class DataRepository(
    private val scope: CoroutineScope // Injected, managed externally
) {
    fun fetchData() = scope.launch {
        // Properly managed
    }
}

// In ViewModel
class MyViewModel(
    private val repository: DataRepository
) : ViewModel() {

    fun loadData() {
        viewModelScope.launch {
            repository.fetchData().join()
        }
    }
}

// In Compose
@Composable
fun MyScreen() {
    val scope = rememberCoroutineScope()

    Button(onClick = {
        scope.launch {
            // Cancelled when composable leaves composition
        }
    }) {
        Text("Load")
    }
}
```

---

#### `coroutine-structured` - Follow structured concurrency principles

Use structured concurrency: parent-child relationships, proper cancellation propagation.

**Incorrect (breaking structured concurrency):**

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

**Correct (structured concurrency):**

```kotlin
class OrderService {
    suspend fun processOrder(order: Order) = coroutineScope {
        // Children are properly structured
        val emailJob = launch {
            sendConfirmationEmail(order)
        }

        val inventoryJob = launch {
            updateInventory(order)
        }

        // Wait for both, cancellation propagates
        emailJob.join()
        inventoryJob.join()
    }

    // Or use async for parallel with results
    suspend fun processOrderParallel(order: Order) = coroutineScope {
        val emailDeferred = async { sendConfirmationEmail(order) }
        val inventoryDeferred = async { updateInventory(order) }

        // Both run in parallel, exceptions propagate
        emailDeferred.await()
        inventoryDeferred.await()
    }
}
```

---

#### `coroutine-cancel` - Handle cancellation properly

Check for cancellation and clean up resources when coroutines are cancelled.

**Incorrect (ignoring cancellation):**

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

**Correct (cancellation-aware):**

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
        // Runs even if cancelled
        withContext(NonCancellable) {
            if (!isActive) {
                tempFile.delete() // Cleanup on cancellation
            }
        }
    }
}
```

---

#### `coroutine-exception` - Use CoroutineExceptionHandler correctly

Handle exceptions at appropriate scope levels with CoroutineExceptionHandler.

**Incorrect (exceptions silently swallowed or crash):**

```kotlin
class MyViewModel : ViewModel() {
    fun loadData() {
        viewModelScope.launch {
            // Exception crashes the app
            val data = repository.fetchData()
            _state.value = data
        }
    }
}
```

**Correct (proper exception handling):**

```kotlin
class MyViewModel : ViewModel() {
    private val exceptionHandler = CoroutineExceptionHandler { _, throwable ->
        _state.value = UiState.Error(throwable.message ?: "Unknown error")
        // Log to analytics
        logger.error("ViewModel error", throwable)
    }

    fun loadData() {
        viewModelScope.launch(exceptionHandler) {
            _state.value = UiState.Loading
            try {
                val data = repository.fetchData()
                _state.value = UiState.Success(data)
            } catch (e: CancellationException) {
                throw e // Don't catch cancellation
            } catch (e: Exception) {
                _state.value = UiState.Error(e.message ?: "Failed to load")
            }
        }
    }
}
```

---

#### `coroutine-dispatcher` - Use correct dispatchers

Use Dispatchers.Main for UI, Dispatchers.IO for blocking I/O, Dispatchers.Default for CPU-intensive work.

**Incorrect (blocking Main thread):**

```kotlin
class FileRepository {
    suspend fun readFile(path: String): String {
        // Wrong: Blocks Main thread
        return File(path).readText()
    }
}
```

**Correct (proper dispatcher usage):**

```kotlin
class FileRepository(
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend fun readFile(path: String): String = withContext(ioDispatcher) {
        File(path).readText()
    }

    suspend fun processData(data: List<Int>): List<Int> = withContext(Dispatchers.Default) {
        // CPU-intensive work
        data.map { heavyComputation(it) }
    }
}

// In ViewModel - update UI on Main
class MyViewModel(private val repo: FileRepository) : ViewModel() {
    fun loadFile(path: String) {
        viewModelScope.launch {
            val content = repo.readFile(path) // Runs on IO
            _content.value = content // Updates on Main
        }
    }
}
```

---

#### `coroutine-flow` - Use Flow operators correctly

Use stateIn/shareIn for sharing flows, proper terminal operators.

**Incorrect (creating new flow on each collection):**

```kotlin
class UserRepository(private val api: UserApi) {
    // Wrong: Creates new network request each time collected
    fun getUsers(): Flow<List<User>> = flow {
        val users = api.fetchUsers()
        emit(users)
    }
}

// In ViewModel
class UsersViewModel(private val repo: UserRepository) : ViewModel() {
    // Wrong: Each collector triggers new request
    val users = repo.getUsers()
}
```

**Correct (sharing with stateIn):**

```kotlin
class UserRepository(private val api: UserApi) {
    fun getUsers(): Flow<List<User>> = flow {
        val users = api.fetchUsers()
        emit(users)
    }
}

class UsersViewModel(private val repo: UserRepository) : ViewModel() {
    val users: StateFlow<List<User>> = repo.getUsers()
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    // For one-time events, use SharedFlow
    private val _events = MutableSharedFlow<UiEvent>()
    val events: SharedFlow<UiEvent> = _events.asSharedFlow()
}
```

---

### 3. Koin DI (CRITICAL)

#### `koin-module` - Organize modules by feature/layer

Structure Koin modules by feature or architectural layer for maintainability.

**Incorrect (everything in one module):**

```kotlin
val appModule = module {
    single { UserRepository() }
    single { ProductRepository() }
    single { OrderRepository() }
    viewModel { UserViewModel(get()) }
    viewModel { ProductViewModel(get()) }
    viewModel { OrderViewModel(get(), get()) }
    single { HttpClient() }
    single { Database() }
    // 50 more definitions...
}
```

**Correct (organized by feature/layer):**

```kotlin
// Core module - infrastructure
val coreModule = module {
    single { createHttpClient() }
    single { createDatabase() }
}

// Data layer modules
val userDataModule = module {
    single<UserRepository> { UserRepositoryImpl(get()) }
    single { UserApi(get()) }
}

val productDataModule = module {
    single<ProductRepository> { ProductRepositoryImpl(get()) }
    single { ProductApi(get()) }
}

// Presentation layer modules
val userPresentationModule = module {
    viewModel { UserViewModel(get()) }
    viewModel { UserListViewModel(get()) }
}

val productPresentationModule = module {
    viewModel { ProductViewModel(get()) }
    viewModel { ProductListViewModel(get(), get()) }
}

// Combine for different contexts
val allModules = listOf(
    coreModule,
    userDataModule, productDataModule,
    userPresentationModule, productPresentationModule
)
```

---

#### `koin-scope` - Use proper scoping

Use single for singletons, factory for new instances, viewModel for ViewModels.

**Incorrect (wrong scoping):**

```kotlin
val module = module {
    // Wrong: Creates new HttpClient for each injection
    factory { HttpClient() }

    // Wrong: Single instance prevents proper cleanup
    single { UserViewModel(get()) }

    // Wrong: Factory for stateful repository
    factory { UserRepository(get()) }
}
```

**Correct (proper scoping):**

```kotlin
val module = module {
    // Singleton for expensive/shared resources
    single { createHttpClient() }
    single { Database() }

    // Factory for stateless utilities
    factory { DateFormatter() }
    factory<Logger> { ConsoleLogger() }

    // ViewModels with proper scope
    viewModel { UserViewModel(get()) }
    viewModel { params -> DetailViewModel(params.get(), get()) }

    // Repository as singleton (holds state/cache)
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
}
```

---

#### `koin-inject` - Inject dependencies correctly in Compose

Use koinViewModel() and koinInject() in Compose, avoid injecting at composition time.

**Incorrect (injecting during composition):**

```kotlin
@Composable
fun UserScreen() {
    // Wrong: Called on every recomposition
    val viewModel = get<UserViewModel>()

    // Wrong: Direct Koin access in composition
    val repository = KoinPlatformTools.defaultContext().get<UserRepository>()
}
```

**Correct (proper Compose injection):**

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsState()

    UserContent(state)
}

@Composable
fun UserScreen(
    userId: String,
    viewModel: UserDetailViewModel = koinViewModel { parametersOf(userId) }
) {
    val state by viewModel.state.collectAsState()

    UserContent(state)
}

// For non-ViewModel dependencies
@Composable
fun FormattedDate(timestamp: Long) {
    val formatter: DateFormatter = koinInject()

    Text(formatter.format(timestamp))
}
```

---

#### `koin-qualifier` - Use named qualifiers for disambiguation

Use named/qualifier annotations to differentiate same-type dependencies.

**Incorrect (ambiguous dependencies):**

```kotlin
val module = module {
    single { OkHttpClient() } // For general use
    single { OkHttpClient().newBuilder().addInterceptor(authInterceptor).build() } // Conflict!
}
```

**Correct (using qualifiers):**

```kotlin
val module = module {
    single(named("default")) {
        OkHttpClient.Builder().build()
    }

    single(named("authenticated")) {
        OkHttpClient.Builder()
            .addInterceptor(get<AuthInterceptor>())
            .build()
    }
}

// Usage
class ApiClient(
    private val client: OkHttpClient
) { /* ... */ }

val apiModule = module {
    single { ApiClient(get(named("authenticated"))) }
}
```

---

#### `koin-lazy` - Use lazy injection for optional dependencies

Use inject() with lazy for optional or conditionally-used dependencies.

**Incorrect (eager injection of optional dependencies):**

```kotlin
class AnalyticsService(
    private val firebaseAnalytics: FirebaseAnalytics, // Crashes if not available
    private val mixpanel: Mixpanel
) {
    fun track(event: Event) {
        firebaseAnalytics.log(event)
        mixpanel.track(event)
    }
}
```

**Correct (lazy/optional injection):**

```kotlin
class AnalyticsService : KoinComponent {
    // Lazy injection - only resolved when accessed
    private val firebaseAnalytics: FirebaseAnalytics? by injectOrNull()
    private val mixpanel: Mixpanel? by injectOrNull()

    fun track(event: Event) {
        firebaseAnalytics?.log(event)
        mixpanel?.track(event)
    }
}

// Or with constructor injection and defaults
class AnalyticsService(
    private val providers: List<AnalyticsProvider> = emptyList()
) {
    fun track(event: Event) {
        providers.forEach { it.track(event) }
    }
}

val module = module {
    single {
        AnalyticsService(getAll()) // Gets all AnalyticsProvider implementations
    }
}
```

---

### 4. Ktor Client (HIGH)

#### `ktor-client` - Configure HttpClient properly

Create a properly configured HttpClient with all necessary plugins.

**Incorrect (minimal configuration):**

```kotlin
val client = HttpClient()
```

**Correct (full configuration):**

```kotlin
val client = HttpClient(CIO) {
    // JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
            coerceInputValues = true
        })
    }

    // Timeouts
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 10_000
        socketTimeoutMillis = 30_000
    }

    // Logging (debug builds only)
    install(Logging) {
        logger = Logger.DEFAULT
        level = LogLevel.HEADERS
        filter { request ->
            request.url.host.contains("api.example.com")
        }
    }

    // Default headers
    defaultRequest {
        header(HttpHeaders.ContentType, ContentType.Application.Json)
        header("X-App-Version", BuildConfig.VERSION_NAME)
    }

    // Response validation
    expectSuccess = true
    HttpResponseValidator {
        handleResponseExceptionWithRequest { exception, _ ->
            when (exception) {
                is ClientRequestException -> throw ApiException.Client(exception)
                is ServerResponseException -> throw ApiException.Server(exception)
                else -> throw exception
            }
        }
    }
}
```

---

#### `ktor-error` - Handle HTTP errors and exceptions

Implement comprehensive error handling for network requests.

**Incorrect (no error handling):**

```kotlin
class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): User {
        return client.get("$BASE_URL/users/$id").body()
    }
}
```

**Correct (comprehensive error handling):**

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val exception: ApiException) : ApiResult<Nothing>()
}

sealed class ApiException(message: String, cause: Throwable? = null) : Exception(message, cause) {
    class Network(cause: Throwable) : ApiException("Network error", cause)
    class Timeout(cause: Throwable) : ApiException("Request timed out", cause)
    class Client(val code: Int, message: String) : ApiException("Client error: $code - $message")
    class Server(val code: Int, message: String) : ApiException("Server error: $code - $message")
    class Parse(cause: Throwable) : ApiException("Failed to parse response", cause)
    class Unknown(cause: Throwable) : ApiException("Unknown error", cause)
}

class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): ApiResult<User> = safeApiCall {
        client.get("$BASE_URL/users/$id").body()
    }

    private suspend fun <T> safeApiCall(block: suspend () -> T): ApiResult<T> {
        return try {
            ApiResult.Success(block())
        } catch (e: CancellationException) {
            throw e // Don't catch cancellation
        } catch (e: HttpRequestTimeoutException) {
            ApiResult.Error(ApiException.Timeout(e))
        } catch (e: ClientRequestException) {
            val body = e.response.bodyAsText()
            ApiResult.Error(ApiException.Client(e.response.status.value, body))
        } catch (e: ServerResponseException) {
            val body = e.response.bodyAsText()
            ApiResult.Error(ApiException.Server(e.response.status.value, body))
        } catch (e: SerializationException) {
            ApiResult.Error(ApiException.Parse(e))
        } catch (e: IOException) {
            ApiResult.Error(ApiException.Network(e))
        } catch (e: Exception) {
            ApiResult.Error(ApiException.Unknown(e))
        }
    }
}
```

---

#### `ktor-serialization` - Configure JSON serialization correctly

Use kotlinx.serialization with proper configuration.

**Incorrect (default serialization with crashes):**

```kotlin
// Crashes on unknown fields, null values, etc.
val json = Json.Default

@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String // Crashes if null in response
)
```

**Correct (resilient serialization):**

```kotlin
val json = Json {
    ignoreUnknownKeys = true      // Don't crash on extra fields
    isLenient = true              // Allow unquoted strings
    coerceInputValues = true      // Use defaults for null/missing
    encodeDefaults = false        // Don't send default values
    explicitNulls = false         // Omit null values
}

@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String? = null,    // Nullable with default
    val role: UserRole = UserRole.USER  // Default value
)

@Serializable
enum class UserRole {
    @SerialName("admin") ADMIN,
    @SerialName("user") USER,
    @SerialName("guest") GUEST
}
```

---

#### `ktor-retry` - Implement retry logic for transient failures

Add retry logic for network requests that may fail temporarily.

**Correct implementation:**

```kotlin
suspend fun <T> retryWithBackoff(
    times: Int = 3,
    initialDelayMs: Long = 100,
    maxDelayMs: Long = 10000,
    factor: Double = 2.0,
    shouldRetry: (Exception) -> Boolean = { it.isRetryable() },
    block: suspend () -> T
): T {
    var currentDelay = initialDelayMs
    repeat(times - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            if (!shouldRetry(e)) throw e

            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelayMs)
        }
    }
    return block() // Last attempt
}

private fun Exception.isRetryable(): Boolean = when (this) {
    is CancellationException -> false
    is HttpRequestTimeoutException -> true
    is ConnectException -> true
    is ServerResponseException -> response.status.value in 500..599
    else -> false
}

// Usage
class UserApi(private val client: HttpClient) {
    suspend fun getUser(id: String): User = retryWithBackoff {
        client.get("$BASE_URL/users/$id").body()
    }
}
```

---

### 5. Expect/Actual (HIGH)

#### `expect-interface` - Prefer interfaces over expect/actual

Use interfaces with platform-specific implementations when possible.

**Incorrect (overusing expect/actual):**

```kotlin
// commonMain
expect class PlatformLogger() {
    fun log(message: String)
    fun error(message: String, throwable: Throwable?)
}

// androidMain
actual class PlatformLogger {
    actual fun log(message: String) = Log.d(TAG, message)
    actual fun error(message: String, throwable: Throwable?) = Log.e(TAG, message, throwable)
}

// iosMain
actual class PlatformLogger {
    actual fun log(message: String) = NSLog(message)
    actual fun error(message: String, throwable: Throwable?) = NSLog("$message: $throwable")
}
```

**Correct (interface with expect factory):**

```kotlin
// commonMain
interface Logger {
    fun log(message: String)
    fun error(message: String, throwable: Throwable? = null)
}

expect fun createLogger(): Logger

// androidMain
actual fun createLogger(): Logger = AndroidLogger()

class AndroidLogger : Logger {
    override fun log(message: String) = Log.d(TAG, message)
    override fun error(message: String, throwable: Throwable?) = Log.e(TAG, message, throwable)
}

// iosMain
actual fun createLogger(): Logger = IosLogger()

class IosLogger : Logger {
    override fun log(message: String) = NSLog(message)
    override fun error(message: String, throwable: Throwable?) = NSLog("$message: $throwable")
}
```

**Impact:** Better testability, easier DI integration.

---

#### `expect-minimal` - Keep expect declarations minimal

Only use expect/actual for truly platform-specific code.

**Incorrect (expect for common logic):**

```kotlin
// commonMain
expect fun formatDate(timestamp: Long): String

// androidMain - duplicated logic
actual fun formatDate(timestamp: Long): String {
    val date = Date(timestamp)
    val format = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    return format.format(date)
}

// iosMain - duplicated logic
actual fun formatDate(timestamp: Long): String {
    val date = NSDate.dateWithTimeIntervalSince1970(timestamp.toDouble() / 1000)
    val formatter = NSDateFormatter()
    formatter.dateFormat = "yyyy-MM-dd"
    return formatter.stringFromDate(date)
}
```

**Correct (minimal expect, common logic):**

```kotlin
// commonMain
expect class DateFormatter() {
    fun format(timestamp: Long, pattern: String): String
}

fun formatDate(timestamp: Long): String = DateFormatter().format(timestamp, "yyyy-MM-dd")
fun formatDateTime(timestamp: Long): String = DateFormatter().format(timestamp, "yyyy-MM-dd HH:mm")
fun formatTime(timestamp: Long): String = DateFormatter().format(timestamp, "HH:mm")

// Or use kotlinx-datetime for fully common implementation
import kotlinx.datetime.*

fun formatDate(timestamp: Long): String {
    val instant = Instant.fromEpochMilliseconds(timestamp)
    val dateTime = instant.toLocalDateTime(TimeZone.currentSystemDefault())
    return "${dateTime.year}-${dateTime.monthNumber.toString().padStart(2, '0')}-${dateTime.dayOfMonth.toString().padStart(2, '0')}"
}
```

---

### 6. ViewModel (HIGH)

#### `viewmodel-state` - Use sealed class/interface for UI state

Model UI state as a sealed hierarchy for exhaustive handling.

**Incorrect (multiple boolean flags):**

```kotlin
class UserViewModel : ViewModel() {
    var isLoading by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    var user by mutableStateOf<User?>(null)
    var isEmpty by mutableStateOf(false)
}
```

**Correct (sealed UI state):**

```kotlin
sealed interface UserUiState {
    data object Loading : UserUiState
    data class Success(val user: User) : UserUiState
    data class Error(val message: String, val retry: () -> Unit) : UserUiState
    data object Empty : UserUiState
}

class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    private val _state = MutableStateFlow<UserUiState>(UserUiState.Loading)
    val state: StateFlow<UserUiState> = _state.asStateFlow()

    fun loadUser(userId: String) {
        viewModelScope.launch {
            _state.value = UserUiState.Loading

            repository.getUser(userId)
                .onSuccess { user ->
                    _state.value = if (user != null) {
                        UserUiState.Success(user)
                    } else {
                        UserUiState.Empty
                    }
                }
                .onFailure { error ->
                    _state.value = UserUiState.Error(
                        message = error.message ?: "Unknown error",
                        retry = { loadUser(userId) }
                    )
                }
        }
    }
}

// In Composable
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val state by viewModel.state.collectAsState()

    when (val currentState = state) {
        is UserUiState.Loading -> LoadingIndicator()
        is UserUiState.Success -> UserContent(currentState.user)
        is UserUiState.Error -> ErrorMessage(currentState.message, currentState.retry)
        is UserUiState.Empty -> EmptyMessage()
    }
}
```

---

#### `viewmodel-event` - Separate one-time events from state

Use SharedFlow for one-time events (navigation, snackbars) instead of state.

**Incorrect (events in state):**

```kotlin
data class LoginState(
    val isLoading: Boolean = false,
    val navigateToHome: Boolean = false, // Wrong: causes navigation on recomposition
    val showSnackbar: String? = null      // Wrong: shows multiple times
)
```

**Correct (separate events):**

```kotlin
data class LoginState(
    val isLoading: Boolean = false,
    val email: String = "",
    val password: String = ""
)

sealed interface LoginEvent {
    data object NavigateToHome : LoginEvent
    data class ShowSnackbar(val message: String) : LoginEvent
    data class ShowError(val error: String) : LoginEvent
}

class LoginViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _state = MutableStateFlow(LoginState())
    val state: StateFlow<LoginState> = _state.asStateFlow()

    private val _events = MutableSharedFlow<LoginEvent>()
    val events: SharedFlow<LoginEvent> = _events.asSharedFlow()

    fun login() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }

            authRepository.login(_state.value.email, _state.value.password)
                .onSuccess {
                    _events.emit(LoginEvent.NavigateToHome)
                }
                .onFailure { error ->
                    _state.update { it.copy(isLoading = false) }
                    _events.emit(LoginEvent.ShowError(error.message ?: "Login failed"))
                }
        }
    }
}

// In Composable
@Composable
fun LoginScreen(
    viewModel: LoginViewModel,
    onNavigateToHome: () -> Unit
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is LoginEvent.NavigateToHome -> onNavigateToHome()
                is LoginEvent.ShowSnackbar -> snackbarHostState.showSnackbar(event.message)
                is LoginEvent.ShowError -> snackbarHostState.showSnackbar(event.error)
            }
        }
    }

    LoginContent(state, viewModel::login)
}
```

---

### 7. Navigation (MEDIUM)

#### `nav-typesafe` - Use type-safe navigation arguments

Use type-safe route definitions with proper argument handling.

**Correct implementation (Voyager/Decompose style):**

```kotlin
// Define screens with type-safe arguments
sealed class Screen : Parcelable {
    @Parcelize
    data object Home : Screen()

    @Parcelize
    data class UserDetail(val userId: String) : Screen()

    @Parcelize
    data class ProductDetail(val productId: String, val source: String? = null) : Screen()
}

// Navigation component
class RootNavigator {
    private val _screenStack = MutableStateFlow<List<Screen>>(listOf(Screen.Home))
    val screenStack: StateFlow<List<Screen>> = _screenStack.asStateFlow()

    fun push(screen: Screen) {
        _screenStack.update { it + screen }
    }

    fun pop(): Boolean {
        if (_screenStack.value.size <= 1) return false
        _screenStack.update { it.dropLast(1) }
        return true
    }

    fun replaceAll(screen: Screen) {
        _screenStack.value = listOf(screen)
    }
}

// Usage in Composable
@Composable
fun RootContent(navigator: RootNavigator = koinInject()) {
    val screens by navigator.screenStack.collectAsState()

    screens.lastOrNull()?.let { screen ->
        when (screen) {
            is Screen.Home -> HomeScreen(
                onUserClick = { userId -> navigator.push(Screen.UserDetail(userId)) },
                onProductClick = { productId -> navigator.push(Screen.ProductDetail(productId)) }
            )
            is Screen.UserDetail -> UserDetailScreen(
                userId = screen.userId,
                onBack = { navigator.pop() }
            )
            is Screen.ProductDetail -> ProductDetailScreen(
                productId = screen.productId,
                source = screen.source,
                onBack = { navigator.pop() }
            )
        }
    }
}
```

---

#### `nav-backstack` - Manage back stack properly

Handle back navigation and back stack manipulation correctly.

**Correct implementation:**

```kotlin
class Navigator {
    private val _backStack = MutableStateFlow<List<Screen>>(listOf(Screen.Home))
    val currentScreen: StateFlow<Screen> = _backStack.map { it.last() }.stateIn(/*...*/)

    fun navigate(screen: Screen, popUpTo: Screen? = null, inclusive: Boolean = false) {
        _backStack.update { stack ->
            val newStack = if (popUpTo != null) {
                val index = stack.indexOfLast { it == popUpTo }
                if (index >= 0) {
                    stack.take(if (inclusive) index else index + 1)
                } else stack
            } else stack

            newStack + screen
        }
    }

    fun popBackStack(): Boolean {
        if (_backStack.value.size <= 1) return false
        _backStack.update { it.dropLast(1) }
        return true
    }

    // Handle system back press
    fun onBackPressed(): Boolean {
        return popBackStack()
    }
}

// Handle back press in Compose
@Composable
fun AppContent(navigator: Navigator) {
    BackHandler(enabled = navigator.canGoBack) {
        navigator.popBackStack()
    }

    // ... screen content
}
```

---

### 8. Testing (MEDIUM)

#### `test-compose` - Write Compose UI tests correctly

Use ComposeTestRule for testing Compose UI components.

**Correct implementation:**

```kotlin
class UserCardTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun userCard_displaysUserInfo() {
        val user = User(id = "1", name = "John Doe", email = "john@example.com")

        composeTestRule.setContent {
            MaterialTheme {
                UserCard(user = user)
            }
        }

        composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
        composeTestRule.onNodeWithText("john@example.com").assertIsDisplayed()
    }

    @Test
    fun userCard_callsOnClick_whenTapped() {
        var clicked = false
        val user = User(id = "1", name = "John", email = "john@example.com")

        composeTestRule.setContent {
            MaterialTheme {
                UserCard(user = user, onClick = { clicked = true })
            }
        }

        composeTestRule.onNodeWithText("John").performClick()

        assertTrue(clicked)
    }

    @Test
    fun userCard_showsLoadingState() {
        composeTestRule.setContent {
            MaterialTheme {
                UserCard(isLoading = true)
            }
        }

        composeTestRule.onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }
}
```

---

#### `test-coroutine` - Test coroutines with TestDispatcher

Use TestDispatcher for deterministic coroutine testing.

**Correct implementation:**

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: UserViewModel
    private lateinit var repository: FakeUserRepository

    @BeforeTest
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = FakeUserRepository()
        viewModel = UserViewModel(repository)
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun loadUser_emitsLoadingThenSuccess() = runTest {
        val user = User("1", "John")
        repository.setUser(user)

        val states = mutableListOf<UserUiState>()
        val job = launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.state.toList(states)
        }

        viewModel.loadUser("1")
        advanceUntilIdle()

        assertEquals(
            listOf(UserUiState.Loading, UserUiState.Success(user)),
            states.drop(1) // Skip initial state
        )

        job.cancel()
    }

    @Test
    fun loadUser_emitsError_onFailure() = runTest {
        repository.setShouldFail(true)

        viewModel.loadUser("1")
        advanceUntilIdle()

        assertTrue(viewModel.state.value is UserUiState.Error)
    }
}
```

---

#### `test-flow` - Test Flow emissions with Turbine

Use Turbine library for testing Flow emissions.

**Correct implementation:**

```kotlin
class UserRepositoryTest {
    @Test
    fun observeUsers_emitsUpdates() = runTest {
        val repository = UserRepositoryImpl(fakeDatabase)

        repository.observeUsers().test {
            // Initial empty state
            assertEquals(emptyList<User>(), awaitItem())

            // Add user
            repository.addUser(User("1", "John"))
            assertEquals(listOf(User("1", "John")), awaitItem())

            // Add another user
            repository.addUser(User("2", "Jane"))
            assertEquals(
                listOf(User("1", "John"), User("2", "Jane")),
                awaitItem()
            )

            cancelAndConsumeRemainingEvents()
        }
    }

    @Test
    fun observeUser_completesOnDeletion() = runTest {
        val repository = UserRepositoryImpl(fakeDatabase)
        repository.addUser(User("1", "John"))

        repository.observeUser("1").test {
            assertEquals(User("1", "John"), awaitItem())

            repository.deleteUser("1")

            awaitComplete()
        }
    }
}
```

---

#### `test-koin` - Setup Koin for testing

Configure Koin properly for unit and integration tests.

**Correct implementation:**

```kotlin
class UserViewModelKoinTest : KoinTest {
    private val mockRepository: UserRepository = mockk()

    @get:Rule
    val koinTestRule = KoinTestRule.create {
        modules(
            module {
                single<UserRepository> { mockRepository }
                viewModel { UserViewModel(get()) }
            }
        )
    }

    private val viewModel: UserViewModel by inject()

    @Test
    fun loadUser_callsRepository() = runTest {
        val user = User("1", "John")
        coEvery { mockRepository.getUser("1") } returns Result.success(user)

        viewModel.loadUser("1")

        coVerify { mockRepository.getUser("1") }
    }
}

// Or without Rule, manual start/stop
class ManualKoinTest : KoinTest {
    @BeforeTest
    fun setup() {
        startKoin {
            modules(testModule)
        }
    }

    @AfterTest
    fun tearDown() {
        stopKoin()
    }
}
```

---

#### `test-ktor` - Mock Ktor client responses

Use MockEngine for testing Ktor client code.

**Correct implementation:**

```kotlin
class UserApiTest {
    @Test
    fun getUser_parsesResponse() = runTest {
        val mockEngine = MockEngine { request ->
            when {
                request.url.encodedPath == "/users/1" -> respond(
                    content = ByteReadChannel("""{"id":"1","name":"John","email":"john@example.com"}"""),
                    status = HttpStatusCode.OK,
                    headers = headersOf(HttpHeaders.ContentType, "application/json")
                )
                else -> respond(
                    content = ByteReadChannel(""),
                    status = HttpStatusCode.NotFound
                )
            }
        }

        val client = HttpClient(mockEngine) {
            install(ContentNegotiation) { json() }
        }

        val api = UserApi(client)
        val result = api.getUser("1")

        assertEquals(User("1", "John", "john@example.com"), result)
    }

    @Test
    fun getUser_handlesError() = runTest {
        val mockEngine = MockEngine {
            respond(
                content = ByteReadChannel("""{"error":"User not found"}"""),
                status = HttpStatusCode.NotFound
            )
        }

        val client = HttpClient(mockEngine) {
            install(ContentNegotiation) { json() }
        }

        val api = UserApi(client)

        assertFailsWith<ClientRequestException> {
            api.getUser("999")
        }
    }
}
```

---

## Integration Workflow

### When Writing Compose UI

1. Use StateFlow with collectAsState (`compose-state-flow`)
2. Mark data classes as @Immutable (`compose-state-stable`)
3. Use remember with keys for expensive calculations (`compose-state-remember`)
4. Use LaunchedEffect for side effects (`compose-state-effect`)

### When Setting Up DI

1. Organize modules by feature (`koin-module`)
2. Use proper scoping (single, factory, viewModel) (`koin-scope`)
3. Use koinViewModel() in Compose (`koin-inject`)
4. Add qualifiers for same-type dependencies (`koin-qualifier`)

### When Making Network Requests

1. Configure HttpClient properly (`ktor-client`)
2. Implement comprehensive error handling (`ktor-error`)
3. Add retry logic for transient failures (`ktor-retry`)
4. Use resilient serialization configuration (`ktor-serialization`)

### When Writing ViewModels

1. Use sealed class for UI state (`viewmodel-state`)
2. Separate one-time events from state (`viewmodel-event`)
3. Use viewModelScope for coroutines (`viewmodel-scope`)
4. Handle all loading/error/success states (`viewmodel-loading`)

---

## References

- [Kotlin Multiplatform Documentation](https://kotlinlang.org/docs/multiplatform.html)
- [Compose Multiplatform](https://www.jetbrains.com/lp/compose-multiplatform/)
- [Koin Documentation](https://insert-koin.io/docs/reference/koin-mp/kmp/)
- [Ktor Client](https://ktor.io/docs/getting-started-ktor-client.html)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization)
