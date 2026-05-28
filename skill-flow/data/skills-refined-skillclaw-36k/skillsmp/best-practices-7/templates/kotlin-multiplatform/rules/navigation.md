# Navigation Rules

## nav-typesafe - Use type-safe navigation arguments

Use type-safe route definitions with proper argument handling.

### Incorrect

```kotlin
// String-based navigation - error prone
fun navigateToUser(userId: String) {
    navController.navigate("user/$userId")
}

// Wrong parsing
val userId = navBackStackEntry.arguments?.getString("userId")
```

### Correct

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
}

// Usage in Composable
@Composable
fun RootContent(navigator: RootNavigator = koinInject()) {
    val screens by navigator.screenStack.collectAsState()

    screens.lastOrNull()?.let { screen ->
        when (screen) {
            is Screen.Home -> HomeScreen(
                onUserClick = { userId -> navigator.push(Screen.UserDetail(userId)) }
            )
            is Screen.UserDetail -> UserDetailScreen(
                userId = screen.userId,
                onBack = { navigator.pop() }
            )
            is Screen.ProductDetail -> ProductDetailScreen(
                productId = screen.productId,
                source = screen.source
            )
        }
    }
}
```

---

## nav-backstack - Manage back stack properly

Handle back navigation and back stack manipulation correctly.

### Correct

```kotlin
class Navigator {
    private val _backStack = MutableStateFlow<List<Screen>>(listOf(Screen.Home))
    val currentScreen: StateFlow<Screen> = _backStack.map { it.last() }.stateIn(/*...*/)

    val canGoBack: Boolean get() = _backStack.value.size > 1

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
        if (!canGoBack) return false
        _backStack.update { it.dropLast(1) }
        return true
    }

    fun popUpTo(screen: Screen, inclusive: Boolean = false) {
        _backStack.update { stack ->
            val index = stack.indexOfLast { it == screen }
            if (index >= 0) {
                stack.take(if (inclusive) index else index + 1)
            } else stack
        }
    }

    fun replaceAll(screen: Screen) {
        _backStack.value = listOf(screen)
    }
}

// Handle back press
@Composable
fun AppContent(navigator: Navigator) {
    BackHandler(enabled = navigator.canGoBack) {
        navigator.popBackStack()
    }

    // ... content
}
```

---

## nav-result - Pass results between screens safely

Handle navigation results without memory leaks.

### Correct

```kotlin
// Result callback pattern
class Navigator {
    private val resultCallbacks = mutableMapOf<String, (Any?) -> Unit>()

    fun <T> navigateForResult(
        screen: Screen,
        resultKey: String,
        onResult: (T?) -> Unit
    ) {
        @Suppress("UNCHECKED_CAST")
        resultCallbacks[resultKey] = { onResult(it as T?) }
        push(screen)
    }

    fun setResult(resultKey: String, result: Any?) {
        resultCallbacks.remove(resultKey)?.invoke(result)
    }

    fun popWithResult(resultKey: String, result: Any?) {
        setResult(resultKey, result)
        pop()
    }
}

// Usage
@Composable
fun UserListScreen(navigator: Navigator) {
    Button(onClick = {
        navigator.navigateForResult<User>(
            screen = Screen.UserPicker,
            resultKey = "selected_user"
        ) { selectedUser ->
            selectedUser?.let { handleUserSelected(it) }
        }
    }) {
        Text("Select User")
    }
}

@Composable
fun UserPickerScreen(navigator: Navigator) {
    LazyColumn {
        items(users) { user ->
            UserItem(
                user = user,
                onClick = {
                    navigator.popWithResult("selected_user", user)
                }
            )
        }
    }
}
```

---

## nav-deeplink - Handle deep links correctly

Process deep links and restore navigation state.

### Correct

```kotlin
sealed class DeepLink {
    data class User(val userId: String) : DeepLink()
    data class Product(val productId: String) : DeepLink()
    data class Order(val orderId: String) : DeepLink()
}

class DeepLinkHandler(private val navigator: Navigator) {
    fun handleDeepLink(uri: String): Boolean {
        val deepLink = parseDeepLink(uri) ?: return false

        when (deepLink) {
            is DeepLink.User -> {
                navigator.replaceAll(Screen.Home)
                navigator.push(Screen.UserDetail(deepLink.userId))
            }
            is DeepLink.Product -> {
                navigator.replaceAll(Screen.Home)
                navigator.push(Screen.ProductDetail(deepLink.productId))
            }
            is DeepLink.Order -> {
                navigator.replaceAll(Screen.Home)
                navigator.push(Screen.Orders)
                navigator.push(Screen.OrderDetail(deepLink.orderId))
            }
        }
        return true
    }

    private fun parseDeepLink(uri: String): DeepLink? {
        val parsedUri = Uri.parse(uri)
        val pathSegments = parsedUri.pathSegments

        return when {
            pathSegments.getOrNull(0) == "user" && pathSegments.size >= 2 ->
                DeepLink.User(pathSegments[1])
            pathSegments.getOrNull(0) == "product" && pathSegments.size >= 2 ->
                DeepLink.Product(pathSegments[1])
            pathSegments.getOrNull(0) == "order" && pathSegments.size >= 2 ->
                DeepLink.Order(pathSegments[1])
            else -> null
        }
    }
}
```

---

## nav-transition - Implement smooth transitions

Add animations for navigation transitions.

### Correct

```kotlin
@Composable
fun AnimatedNavigation(navigator: Navigator) {
    val screenStack by navigator.screenStack.collectAsState()
    val currentScreen = screenStack.lastOrNull() ?: return

    AnimatedContent(
        targetState = currentScreen,
        transitionSpec = {
            if (targetState.index > initialState.index) {
                // Forward navigation
                slideInHorizontally { width -> width } + fadeIn() togetherWith
                    slideOutHorizontally { width -> -width } + fadeOut()
            } else {
                // Back navigation
                slideInHorizontally { width -> -width } + fadeIn() togetherWith
                    slideOutHorizontally { width -> width } + fadeOut()
            }.using(SizeTransform(clip = false))
        },
        label = "navigation"
    ) { screen ->
        when (screen) {
            is Screen.Home -> HomeScreen()
            is Screen.UserDetail -> UserDetailScreen(screen.userId)
            is Screen.ProductDetail -> ProductDetailScreen(screen.productId)
        }
    }
}

// Screen index for transition direction
val Screen.index: Int get() = when (this) {
    is Screen.Home -> 0
    is Screen.UserDetail -> 1
    is Screen.ProductDetail -> 2
}
```
