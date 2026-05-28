# Compose State Rules

## compose-state-flow - Use StateFlow with collectAsState

StateFlow provides lifecycle-aware state collection that survives recomposition.

### Incorrect

```kotlin
class UserViewModel : ViewModel() {
    // Wrong: mutableStateOf is not lifecycle-aware in ViewModel
    var user by mutableStateOf<User?>(null)
        private set

    fun loadUser() {
        viewModelScope.launch {
            user = repository.getUser()
        }
    }
}
```

### Correct

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

---

## compose-state-remember - Use remember/rememberSaveable correctly

Use remember for expensive calculations, rememberSaveable for configuration change survival.

### Incorrect

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    // Wrong: Recalculated on every recomposition
    val sortedItems = items.sortedBy { it.name }
    val filteredItems = sortedItems.filter { it.isActive }
}
```

### Correct

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    val processedItems = remember(items) {
        items.filter { it.isActive }.sortedBy { it.name }
    }

    var searchQuery by rememberSaveable { mutableStateOf("") }

    val filteredItems = remember(processedItems, searchQuery) {
        if (searchQuery.isEmpty()) processedItems
        else processedItems.filter { it.name.contains(searchQuery, ignoreCase = true) }
    }
}
```

---

## compose-state-derived - Use derivedStateOf for computed values

Use derivedStateOf when you need computed state that only updates when dependencies change.

### Incorrect

```kotlin
@Composable
fun ShoppingCart(items: List<CartItem>) {
    // Recalculates every recomposition
    val totalPrice = items.sumOf { it.price * it.quantity }
}
```

### Correct

```kotlin
@Composable
fun ShoppingCart(items: List<CartItem>) {
    val totalPrice by remember {
        derivedStateOf { items.sumOf { it.price * it.quantity } }
    }
}
```

---

## compose-state-stable - Mark classes with @Stable/@Immutable

Mark data classes to enable Compose compiler optimizations.

### Incorrect

```kotlin
// Without annotations, Compose assumes unstable
data class User(
    val id: String,
    val name: String,
    val avatar: String
)
```

### Correct

```kotlin
@Immutable
data class User(
    val id: String,
    val name: String,
    val avatar: String
)

// For mutable but stable types
@Stable
class UserState(
    val user: User,
    private var _isLoading: Boolean = false
) {
    val isLoading: Boolean get() = _isLoading
}
```

---

## compose-state-key - Use key() to preserve state

Use key() composable to maintain identity across recompositions.

### Incorrect

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

### Correct

```kotlin
@Composable
fun TodoList(items: List<TodoItem>) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            TodoItemRow(item)
        }
    }
}
```
