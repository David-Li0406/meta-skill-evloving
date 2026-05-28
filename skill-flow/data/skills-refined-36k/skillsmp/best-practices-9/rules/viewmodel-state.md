# ViewModel State Rules

## viewmodel-state-sealed - Use sealed class/interface for UI state

Model UI state as a sealed hierarchy for exhaustive handling.

### Incorrect

```kotlin
class UserViewModel : ViewModel() {
    var isLoading by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    var user by mutableStateOf<User?>(null)
    var isEmpty by mutableStateOf(false)
}
```

### Correct

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

## viewmodel-state-event - Separate one-time events from state

Use SharedFlow for one-time events (navigation, snackbars).

### Incorrect

```kotlin
data class LoginState(
    val isLoading: Boolean = false,
    val navigateToHome: Boolean = false, // Wrong: triggers on recomposition
    val showSnackbar: String? = null      // Wrong: shows multiple times
)
```

### Correct

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

## viewmodel-state-update - Use atomic state updates

Use update{} for thread-safe state modifications.

### Incorrect

```kotlin
class FormViewModel : ViewModel() {
    private val _state = MutableStateFlow(FormState())
    val state: StateFlow<FormState> = _state.asStateFlow()

    fun updateEmail(email: String) {
        // Wrong: Race condition possible
        _state.value = _state.value.copy(email = email)
    }

    fun updatePassword(password: String) {
        // Wrong: Race condition with updateEmail
        _state.value = _state.value.copy(password = password)
    }
}
```

### Correct

```kotlin
class FormViewModel : ViewModel() {
    private val _state = MutableStateFlow(FormState())
    val state: StateFlow<FormState> = _state.asStateFlow()

    fun updateEmail(email: String) {
        _state.update { it.copy(email = email) }
    }

    fun updatePassword(password: String) {
        _state.update { it.copy(password = password) }
    }

    fun updateForm(email: String, password: String) {
        _state.update { it.copy(email = email, password = password) }
    }
}
```

---

## viewmodel-state-combine - Combine multiple state sources

Use combine() to merge multiple state sources into single UI state.

### Correct

```kotlin
class DashboardViewModel(
    private val userRepository: UserRepository,
    private val statsRepository: StatsRepository,
    private val notificationsRepository: NotificationsRepository
) : ViewModel() {
    private val _isLoading = MutableStateFlow(false)
    private val _error = MutableStateFlow<String?>(null)

    val state: StateFlow<DashboardUiState> = combine(
        userRepository.observeUser(),
        statsRepository.observeStats(),
        notificationsRepository.observeUnreadCount(),
        _isLoading,
        _error
    ) { user, stats, unreadCount, isLoading, error ->
        when {
            isLoading -> DashboardUiState.Loading
            error != null -> DashboardUiState.Error(error)
            user == null -> DashboardUiState.NotLoggedIn
            else -> DashboardUiState.Success(
                user = user,
                stats = stats,
                unreadNotifications = unreadCount
            )
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = DashboardUiState.Loading
    )
}
```

---

## viewmodel-state-mvi - Implement MVI pattern for complex screens

Use Model-View-Intent for complex state management.

### Correct

```kotlin
// State
data class ShoppingCartState(
    val items: List<CartItem> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
) {
    val total: Double get() = items.sumOf { it.price * it.quantity }
    val itemCount: Int get() = items.sumOf { it.quantity }
}

// Intent (user actions)
sealed interface CartIntent {
    data class AddItem(val product: Product, val quantity: Int = 1) : CartIntent
    data class RemoveItem(val itemId: String) : CartIntent
    data class UpdateQuantity(val itemId: String, val quantity: Int) : CartIntent
    data object Checkout : CartIntent
    data object Refresh : CartIntent
}

// ViewModel with MVI
class CartViewModel(private val repository: CartRepository) : ViewModel() {
    private val _state = MutableStateFlow(ShoppingCartState())
    val state: StateFlow<ShoppingCartState> = _state.asStateFlow()

    private val _events = MutableSharedFlow<CartEvent>()
    val events: SharedFlow<CartEvent> = _events.asSharedFlow()

    fun processIntent(intent: CartIntent) {
        viewModelScope.launch {
            when (intent) {
                is CartIntent.AddItem -> addItem(intent.product, intent.quantity)
                is CartIntent.RemoveItem -> removeItem(intent.itemId)
                is CartIntent.UpdateQuantity -> updateQuantity(intent.itemId, intent.quantity)
                is CartIntent.Checkout -> checkout()
                is CartIntent.Refresh -> refresh()
            }
        }
    }

    private suspend fun addItem(product: Product, quantity: Int) {
        _state.update { it.copy(isLoading = true, error = null) }

        repository.addToCart(product, quantity)
            .onSuccess { items ->
                _state.update { it.copy(items = items, isLoading = false) }
                _events.emit(CartEvent.ItemAdded(product.name))
            }
            .onFailure { error ->
                _state.update { it.copy(isLoading = false, error = error.message) }
            }
    }

    // ... other intent handlers
}

// Usage
@Composable
fun CartScreen(viewModel: CartViewModel) {
    val state by viewModel.state.collectAsState()

    CartContent(
        state = state,
        onAddItem = { product -> viewModel.processIntent(CartIntent.AddItem(product)) },
        onRemoveItem = { id -> viewModel.processIntent(CartIntent.RemoveItem(id)) },
        onCheckout = { viewModel.processIntent(CartIntent.Checkout) }
    )
}
```
