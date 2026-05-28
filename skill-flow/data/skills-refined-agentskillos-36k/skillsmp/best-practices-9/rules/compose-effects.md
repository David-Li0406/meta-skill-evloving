# Compose Effects Rules

## compose-effect-launched - Use LaunchedEffect for suspending operations

LaunchedEffect runs suspending code in composition scope.

### Incorrect

```kotlin
@Composable
fun AnalyticsScreen(screenName: String, viewModel: AnalyticsViewModel) {
    // Wrong: Runs on every recomposition!
    viewModel.trackScreenView(screenName)
}
```

### Correct

```kotlin
@Composable
fun AnalyticsScreen(screenName: String, viewModel: AnalyticsViewModel) {
    // Runs once when screenName changes
    LaunchedEffect(screenName) {
        viewModel.trackScreenView(screenName)
    }
}

// For initial load only
@Composable
fun InitialLoadScreen(viewModel: DataViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadInitialData()
    }
}
```

---

## compose-effect-disposable - Use DisposableEffect for cleanup

DisposableEffect handles setup and cleanup of resources.

### Incorrect

```kotlin
@Composable
fun EventListenerScreen() {
    // Wrong: No cleanup for listener
    val listener = object : SomeListener {
        override fun onEvent(event: Event) { /* handle */ }
    }
    someService.addListener(listener)
}
```

### Correct

```kotlin
@Composable
fun EventListenerScreen() {
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

// With key for reregistration
@Composable
fun ScopedListenerScreen(scope: String) {
    DisposableEffect(scope) {
        val listener = createListener(scope)
        service.register(listener)

        onDispose {
            service.unregister(listener)
        }
    }
}
```

---

## compose-effect-side - Use SideEffect for non-suspending side effects

SideEffect runs after every successful recomposition.

### Incorrect

```kotlin
@Composable
fun TrackedScreen(analyticsHelper: AnalyticsHelper) {
    // Wrong: May run before composition completes
    analyticsHelper.setCurrentScreen("TrackedScreen")
}
```

### Correct

```kotlin
@Composable
fun TrackedScreen(analyticsHelper: AnalyticsHelper) {
    SideEffect {
        // Runs after every successful recomposition
        analyticsHelper.setCurrentScreen("TrackedScreen")
    }
}
```

---

## compose-effect-produced - Use produceState for async to state conversion

produceState converts async operations to Compose state.

### Incorrect

```kotlin
@Composable
fun UserProfile(userId: String, repository: UserRepository) {
    var user by remember { mutableStateOf<User?>(null) }
    var loading by remember { mutableStateOf(true) }

    LaunchedEffect(userId) {
        loading = true
        user = repository.getUser(userId)
        loading = false
    }
}
```

### Correct

```kotlin
@Composable
fun UserProfile(userId: String, repository: UserRepository) {
    val userState by produceState<Result<User>?>(initialValue = null, userId) {
        value = try {
            Result.success(repository.getUser(userId))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    when (val result = userState) {
        null -> LoadingIndicator()
        else -> result.fold(
            onSuccess = { UserContent(it) },
            onFailure = { ErrorMessage(it.message ?: "Error") }
        )
    }
}
```

---

## compose-effect-derived-state - Use snapshotFlow for state observation

Convert Compose state to Flow for complex observation patterns.

### Correct

```kotlin
@Composable
fun SearchScreen() {
    var searchQuery by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        snapshotFlow { searchQuery }
            .debounce(300)
            .distinctUntilChanged()
            .filter { it.length >= 3 }
            .collectLatest { query ->
                performSearch(query)
            }
    }

    TextField(
        value = searchQuery,
        onValueChange = { searchQuery = it }
    )
}
```
