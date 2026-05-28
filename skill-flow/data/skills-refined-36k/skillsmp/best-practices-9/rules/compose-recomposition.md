# Compose Recomposition Rules

## compose-recomp-stable-lambda - Stabilize lambda parameters

Avoid creating new lambda instances that trigger recomposition.

### Incorrect

```kotlin
@Composable
fun ParentScreen(viewModel: UserViewModel) {
    // Wrong: New lambda created every recomposition
    UserList(
        onUserClick = { userId -> viewModel.selectUser(userId) }
    )
}
```

### Correct

```kotlin
@Composable
fun ParentScreen(viewModel: UserViewModel) {
    // Lambda reference is stable
    val onUserClick = remember { { userId: String -> viewModel.selectUser(userId) } }

    UserList(onUserClick = onUserClick)
}

// Or use method reference when possible
@Composable
fun ParentScreen(viewModel: UserViewModel) {
    UserList(onUserClick = viewModel::selectUser)
}
```

---

## compose-recomp-skip - Design for skippable composables

Ensure composables can be skipped when parameters unchanged.

### Incorrect

```kotlin
// Unstable parameter - never skipped
@Composable
fun UserCard(user: User, actions: List<() -> Unit>) {
    // List<() -> Unit> is unstable
}

// Capturing scope makes lambda unstable
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) { // Captures count
        Text("Count: $count")
    }
}
```

### Correct

```kotlin
@Immutable
data class User(val id: String, val name: String)

@Stable
data class UserActions(
    val onEdit: (String) -> Unit,
    val onDelete: (String) -> Unit
)

@Composable
fun UserCard(user: User, actions: UserActions) {
    // All parameters stable - can be skipped
}

// Extract counter display to allow skipping
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        CounterDisplay(count = count) // Skippable
        CounterButton(onIncrement = { count++ })
    }
}

@Composable
fun CounterDisplay(count: Int) {
    Text("Count: $count")
}

@Composable
fun CounterButton(onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Increment")
    }
}
```

---

## compose-recomp-list - Optimize list recomposition

Use keys and lazy layouts for efficient list rendering.

### Incorrect

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    // All items recompose when list changes
    Column {
        items.forEach { item ->
            ItemRow(item)
        }
    }
}
```

### Correct

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    LazyColumn {
        items(
            items = items,
            key = { it.id }, // Stable identity
            contentType = { it.type } // Optimize item type
        ) { item ->
            ItemRow(item)
        }
    }
}

// For heterogeneous lists
@Composable
fun MixedList(items: List<ListItem>) {
    LazyColumn {
        items(items, key = { it.id }, contentType = { it::class }) { item ->
            when (item) {
                is ListItem.Header -> HeaderRow(item)
                is ListItem.Content -> ContentRow(item)
                is ListItem.Footer -> FooterRow(item)
            }
        }
    }
}
```

---

## compose-recomp-scope - Minimize recomposition scope

Isolate state to smallest possible scope.

### Incorrect

```kotlin
@Composable
fun ProfileScreen(viewModel: ProfileViewModel) {
    val user by viewModel.user.collectAsState()
    val posts by viewModel.posts.collectAsState()
    val stats by viewModel.stats.collectAsState()

    // Entire screen recomposes when any state changes
    Column {
        UserHeader(user)
        UserStats(stats)
        PostList(posts)
    }
}
```

### Correct

```kotlin
@Composable
fun ProfileScreen(viewModel: ProfileViewModel) {
    Column {
        // Each section manages its own state subscription
        UserHeaderSection(viewModel)
        UserStatsSection(viewModel)
        PostListSection(viewModel)
    }
}

@Composable
private fun UserHeaderSection(viewModel: ProfileViewModel) {
    val user by viewModel.user.collectAsState()
    UserHeader(user)
}

@Composable
private fun UserStatsSection(viewModel: ProfileViewModel) {
    val stats by viewModel.stats.collectAsState()
    UserStats(stats)
}

@Composable
private fun PostListSection(viewModel: ProfileViewModel) {
    val posts by viewModel.posts.collectAsState()
    PostList(posts)
}
```

---

## compose-recomp-deferred - Use deferred reads for animations

Defer state reads to avoid recomposing during animations.

### Incorrect

```kotlin
@Composable
fun AnimatedBox(offsetX: Float) {
    // Causes recomposition on every animation frame
    Box(
        modifier = Modifier.offset(x = offsetX.dp)
    )
}
```

### Correct

```kotlin
@Composable
fun AnimatedBox(offsetXProvider: () -> Float) {
    Box(
        modifier = Modifier.offset {
            // Deferred read - only layout phase, no recomposition
            IntOffset(offsetXProvider().roundToInt(), 0)
        }
    )
}

// With Animatable
@Composable
fun SmoothAnimatedBox() {
    val offsetX = remember { Animatable(0f) }

    Box(
        modifier = Modifier.offset {
            IntOffset(offsetX.value.roundToInt(), 0)
        }
    )
}
```
