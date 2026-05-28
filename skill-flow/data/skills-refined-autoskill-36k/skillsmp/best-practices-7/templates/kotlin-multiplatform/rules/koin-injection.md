# Koin Injection Rules

## koin-inject-compose - Inject dependencies correctly in Compose

Use koinViewModel() and koinInject() in Compose, avoid injecting during composition.

### Incorrect

```kotlin
@Composable
fun UserScreen() {
    // Wrong: Called on every recomposition
    val viewModel = get<UserViewModel>()

    // Wrong: Direct Koin access in composition
    val repository = KoinPlatformTools.defaultContext().get<UserRepository>()
}
```

### Correct

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsState()
    UserContent(state)
}

// With parameters
@Composable
fun UserDetailScreen(
    userId: String,
    viewModel: UserDetailViewModel = koinViewModel { parametersOf(userId) }
) {
    val state by viewModel.state.collectAsState()
    UserDetailContent(state)
}

// For non-ViewModel dependencies
@Composable
fun FormattedDate(timestamp: Long) {
    val formatter: DateFormatter = koinInject()
    Text(formatter.format(timestamp))
}
```

---

## koin-inject-lazy - Use lazy injection for optional dependencies

Use inject() with lazy for optional or conditionally-used dependencies.

### Incorrect

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

### Correct

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

## koin-inject-params - Pass parameters correctly

Use parametersOf for runtime parameters in Koin.

### Incorrect

```kotlin
val module = module {
    // Wrong: Trying to use runtime value as fixed dependency
    viewModel { UserDetailViewModel(someUserId, get()) }
}

// Wrong: Recreating Koin get in composable
@Composable
fun UserDetail(userId: String) {
    val viewModel = remember(userId) {
        getKoin().get<UserDetailViewModel>()
    }
}
```

### Correct

```kotlin
val module = module {
    viewModel { (userId: String) ->
        UserDetailViewModel(userId, get())
    }
}

@Composable
fun UserDetail(userId: String) {
    val viewModel: UserDetailViewModel = koinViewModel { parametersOf(userId) }
    // ...
}

// Multiple parameters
val module = module {
    viewModel { (userId: String, mode: ViewMode) ->
        UserDetailViewModel(userId, mode, get())
    }
}

@Composable
fun UserDetail(userId: String, mode: ViewMode) {
    val viewModel: UserDetailViewModel = koinViewModel {
        parametersOf(userId, mode)
    }
}
```

---

## koin-inject-interface - Inject interfaces, not implementations

Depend on abstractions for testability and flexibility.

### Incorrect

```kotlin
val module = module {
    single { UserRepositoryImpl(get()) }
    viewModel { UserViewModel(get<UserRepositoryImpl>()) } // Concrete type
}

class UserViewModel(
    private val repository: UserRepositoryImpl // Concrete type
) : ViewModel()
```

### Correct

```kotlin
val module = module {
    single<UserRepository> { UserRepositoryImpl(get()) }
    viewModel { UserViewModel(get()) }
}

class UserViewModel(
    private val repository: UserRepository // Interface
) : ViewModel()

// For testing
val testModule = module {
    single<UserRepository> { FakeUserRepository() }
}
```

---

## koin-inject-scope - Use Koin scopes for lifecycle management

Use Koin scopes for dependencies with specific lifecycles.

### Correct

```kotlin
// Define scope
val userSessionModule = module {
    scope<UserSession> {
        scoped { UserPreferences(get()) }
        scoped { UserCache(get()) }
        viewModel { SessionViewModel(get(), get()) }
    }
}

// Create and use scope
class UserSessionManager : KoinComponent {
    private var scope: Scope? = null

    fun startSession(user: User) {
        scope = getKoin().createScope<UserSession>()
    }

    fun endSession() {
        scope?.close()
        scope = null
    }

    inline fun <reified T : Any> get(): T? = scope?.get()
}

// In Compose with scoped Koin
@Composable
fun SessionScreen(session: UserSession) {
    KoinScope(scope = remember { getKoin().createScope<UserSession>() }) {
        val viewModel: SessionViewModel = koinViewModel()
        // Use viewModel
    }
}
```
