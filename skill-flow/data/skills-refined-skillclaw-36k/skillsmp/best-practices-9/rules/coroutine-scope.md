# Coroutine Scope Rules

## coroutine-scope-hierarchy - Use appropriate coroutine scope hierarchy

Use proper scope hierarchy: viewModelScope for ViewModels, rememberCoroutineScope for Compose.

### Incorrect

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

### Correct

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

## coroutine-scope-viewmodel - Use viewModelScope correctly

viewModelScope is tied to ViewModel lifecycle, cancelled on onCleared().

### Incorrect

```kotlin
class UserViewModel : ViewModel() {
    // Wrong: Manual scope management
    private val job = Job()
    private val scope = CoroutineScope(Dispatchers.Main + job)

    override fun onCleared() {
        job.cancel() // Manual cleanup required
    }
}
```

### Correct

```kotlin
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    init {
        loadUser()
    }

    fun loadUser() {
        viewModelScope.launch {
            _state.value = UiState.Loading
            try {
                val user = repository.getUser()
                _state.value = UiState.Success(user)
            } catch (e: Exception) {
                _state.value = UiState.Error(e.message)
            }
        }
    }
}
```

---

## coroutine-scope-compose - Use rememberCoroutineScope in Compose

rememberCoroutineScope creates a scope tied to composition lifecycle.

### Incorrect

```kotlin
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    Button(onClick = {
        // Wrong: Can't call suspend function directly
        viewModel.login()

        // Wrong: GlobalScope ignores lifecycle
        GlobalScope.launch {
            viewModel.login()
        }
    }) {
        Text("Login")
    }
}
```

### Correct

```kotlin
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    val scope = rememberCoroutineScope()

    Button(onClick = {
        scope.launch {
            viewModel.login()
        }
    }) {
        Text("Login")
    }
}

// Or use non-suspend wrapper in ViewModel
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    Button(onClick = { viewModel.onLoginClick() }) {
        Text("Login")
    }
}

class LoginViewModel : ViewModel() {
    fun onLoginClick() {
        viewModelScope.launch {
            login()
        }
    }

    private suspend fun login() { /* ... */ }
}
```

---

## coroutine-scope-supervisor - Use SupervisorJob for independent children

SupervisorJob prevents child failure from cancelling siblings.

### Incorrect

```kotlin
class DataSyncService {
    private val scope = CoroutineScope(Dispatchers.IO)

    fun syncAll() {
        scope.launch {
            // If any fails, all are cancelled
            launch { syncUsers() }
            launch { syncProducts() }
            launch { syncOrders() }
        }
    }
}
```

### Correct

```kotlin
class DataSyncService {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    fun syncAll() {
        scope.launch {
            // Each child independent - failure doesn't cancel siblings
            launch { syncUsers() }
            launch { syncProducts() }
            launch { syncOrders() }
        }
    }

    fun cancel() {
        scope.cancel()
    }
}

// Or use supervisorScope for one-time isolation
suspend fun syncAllWithResults(): List<Result<Unit>> = supervisorScope {
    listOf(
        async { runCatching { syncUsers() } },
        async { runCatching { syncProducts() } },
        async { runCatching { syncOrders() } }
    ).awaitAll()
}
```

---

## coroutine-scope-lifecycle - Match scope to lifecycle

Choose scope based on the lifecycle you want.

### Correct

```kotlin
// Application scope - lives as long as app
class AppScope(
    private val scope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
) {
    fun launchInBackground(block: suspend () -> Unit) {
        scope.launch { block() }
    }
}

// Session scope - lives as long as user session
class UserSessionScope {
    private var scope: CoroutineScope? = null

    fun start() {
        scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    }

    fun end() {
        scope?.cancel()
        scope = null
    }

    fun launch(block: suspend () -> Unit) {
        scope?.launch { block() }
    }
}

// Feature scope - lives as long as feature/screen
@Composable
fun FeatureScreen() {
    val scope = rememberCoroutineScope() // Auto-cancelled on leave

    DisposableEffect(Unit) {
        val job = scope.launch { /* long-running feature work */ }
        onDispose { job.cancel() }
    }
}
```
