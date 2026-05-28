# MVVM Pattern in Flutter

Model-View-ViewModel (MVVM) is the recommended architectural pattern for Flutter applications. This pattern provides clear separation between UI, presentation logic, and data access, making applications more maintainable, testable, and scalable.

## Understanding MVVM

MVVM separates an application feature into three interconnected but distinct parts, each with a specific responsibility. This separation enables developers to work on different aspects of a feature independently and makes it easier to test each part in isolation.

### The Three Components

**Model** represents the data layer of your application. In Flutter MVVM, services and repositories make up your Model layer. This layer is responsible for:

- Fetching data from remote APIs
- Reading and writing to local databases
- Caching data for offline use
- Transforming raw data into domain models
- Managing data-related business rules

The Model layer doesn't know anything about how data will be presented to users. It simply provides data access APIs that can be consumed by ViewModels.

**View** describes how to present application data to the user. Views are compositions of widgets that make up a feature or screen. A View is typically (but not always) a screen with a Scaffold widget along with all the widgets below it in the widget tree.

Views are responsible for:

- Building the UI widget tree
- Displaying data provided by ViewModels
- Capturing user interactions (taps, swipes, text input)
- Triggering ViewModel methods in response to user actions
- Navigating to other screens when appropriate

Views should be as simple as possible, containing minimal logic. Ideally, Views are pure presentations of state, with all logic delegated to ViewModels.

**ViewModel** contains the logic that converts app data into UI state. Data from repositories is often formatted differently from the data that needs to be displayed, and ViewModels handle this transformation.

ViewModels are responsible for:

- Fetching data from repositories and services
- Transforming domain models into UI state
- Handling user interaction logic
- Managing loading, error, and success states
- Validating user input
- Exposing methods that Views can call
- Notifying Views when state changes

In the simplest terms, a ViewModel manages the UI state, and the View displays that state.

## The MVVM Relationship

The relationship between these three components follows a strict unidirectional knowledge pattern:

**The View knows about the ViewModel**: Views reference ViewModels to access UI state and call methods in response to user interactions. Views observe ViewModels for state changes and rebuild when state updates.

**The ViewModel knows about the Model**: ViewModels reference repositories and services to fetch and manipulate data. ViewModels call Model layer methods and transform the results into UI state.

**The Model is unaware of the ViewModel**: Repositories and services have no knowledge of ViewModels. They expose generic data access methods that can be used by any consumer.

**The ViewModel is unaware of the View**: ViewModels don't reference Views or widgets. They simply expose state and methods. This makes ViewModels reusable and testable without involving the UI.

This unidirectional dependency structure prevents circular dependencies and keeps concerns cleanly separated. Each component can be developed, tested, and modified independently as long as the contract between components remains stable.

## One-to-One Relationship

Views and ViewModels should have a one-to-one relationship. Each screen or major feature component should have its own dedicated ViewModel that manages state specifically for that View.

This doesn't mean you can't reuse ViewModels, but in practice, each View typically needs slightly different state management. Trying to share ViewModels between Views often leads to bloated ViewModels that try to serve multiple masters.

For shared functionality between ViewModels, extract that logic into services or utility classes rather than trying to reuse ViewModels.

## Implementing Views in Flutter

Views in Flutter are typically StatelessWidgets that consume state from a ViewModel. Modern state management solutions make it possible to build most Views as StatelessWidgets, simplifying the widget tree.

### View Structure

A well-structured View follows this pattern:

```dart
class LoginView extends StatelessWidget {
  const LoginView({super.key});

  @override
  Widget build(BuildContext context) {
    // Access the ViewModel (method depends on state management solution)
    final viewModel = context.watch<LoginViewModel>();

    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Display state from ViewModel
            if (viewModel.isLoading)
              const CircularProgressIndicator(),

            // Display error messages
            if (viewModel.errorMessage != null)
              Text(
                viewModel.errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),

            // Input fields
            TextField(
              onChanged: viewModel.updateEmail,
              decoration: const InputDecoration(labelText: 'Email'),
            ),

            TextField(
              onChanged: viewModel.updatePassword,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Password'),
            ),

            // Actions trigger ViewModel methods
            ElevatedButton(
              onPressed: viewModel.isLoading ? null : viewModel.login,
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### View Best Practices

**Keep Views Simple**: Views should contain minimal logic. All business logic, data transformation, and state management should be in the ViewModel.

**Use Const Constructors**: Where possible, use const constructors for widgets. This improves performance by allowing Flutter to reuse widget instances.

**Extract Complex Widgets**: If a View becomes large, extract logical sections into separate widget classes. This improves readability and makes widgets more reusable.

**Handle Loading and Error States**: Every View that displays data should handle loading states (showing progress indicators) and error states (displaying error messages).

**Disable Actions During Loading**: Prevent users from triggering actions while an operation is in progress by disabling buttons or showing overlays.

## Implementing ViewModels

ViewModels are the heart of the MVVM pattern. They contain all the presentation logic and manage the state that Views display.

### ViewModel Structure

A well-structured ViewModel includes state properties, methods for updating state, and methods that Views can call:

```dart
class LoginViewModel extends ChangeNotifier {
  final AuthRepository _authRepository;

  LoginViewModel(this._authRepository);

  // State properties
  String _email = '';
  String _password = '';
  bool _isLoading = false;
  String? _errorMessage;

  // Getters expose state to Views
  String get email => _email;
  String get password => _password;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  // Computed properties derive from state
  bool get canSubmit =>
      _email.isNotEmpty &&
      _password.isNotEmpty &&
      !_isLoading;

  // Update methods for form fields
  void updateEmail(String value) {
    _email = value;
    _errorMessage = null; // Clear errors when user types
    notifyListeners();
  }

  void updatePassword(String value) {
    _password = value;
    _errorMessage = null;
    notifyListeners();
  }

  // Action methods triggered by user interaction
  Future<void> login() async {
    if (!canSubmit) return;

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _authRepository.login(
        email: _email,
        password: _password,
      );
      // Navigation or success handling would happen here
      // Often through a callback or navigation service
    } catch (e) {
      _errorMessage = 'Login failed: ${e.toString()}';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    // Clean up any resources
    super.dispose();
  }
}
```

### ViewModel Best Practices

**Private State, Public Getters**: Keep state properties private and expose them through getters. This prevents Views from accidentally mutating state directly.

**Notify After State Changes**: Always call `notifyListeners()` after updating state so Views can rebuild with the new state.

**Handle Errors Gracefully**: Catch exceptions from repository calls and convert them into user-friendly error messages.

**Use Computed Properties**: Derive additional state from existing state using getters rather than storing redundant state.

**Dispose Resources**: Override dispose() to clean up any resources like stream subscriptions or timers.

**Avoid Flutter Dependencies**: ViewModels should not import Flutter UI packages (except foundation packages like ChangeNotifier). This keeps ViewModels testable without widget testing.

## State Management Integration

MVVM works with all major Flutter state management solutions. The ViewModel concept is consistent across solutions, but the mechanism for notifying Views and accessing ViewModels differs.

### With Provider

Provider is a battle-tested state management solution that works naturally with ChangeNotifier-based ViewModels:

```dart
// Setup in main.dart or app widget
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => LoginViewModel(getIt<AuthRepository>()),
        ),
      ],
      child: const MyApp(),
    ),
  );
}

// Access in Views
class LoginView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<LoginViewModel>();
    // Use viewModel...
  }
}
```

### With Riverpod

Riverpod is the modern, recommended solution for new Flutter projects. It provides compile-time safety and better testing support:

```dart
// Define ViewModel as a provider
final loginViewModelProvider = ChangeNotifierProvider.autoDispose(
  (ref) => LoginViewModel(ref.watch(authRepositoryProvider)),
);

// Access in Views
class LoginView extends ConsumerWidget {
  const LoginView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final viewModel = ref.watch(loginViewModelProvider);
    // Use viewModel...
  }
}
```

### With BLoC

BLoC enforces a stricter pattern using streams and events, but the ViewModel concept translates to the BLoC class:

```dart
// LoginBloc acts as the ViewModel
class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final AuthRepository _authRepository;

  LoginBloc(this._authRepository) : super(LoginInitial()) {
    on<LoginSubmitted>(_onLoginSubmitted);
  }

  Future<void> _onLoginSubmitted(
    LoginSubmitted event,
    Emitter<LoginState> emit,
  ) async {
    emit(LoginLoading());
    try {
      await _authRepository.login(
        email: event.email,
        password: event.password,
      );
      emit(LoginSuccess());
    } catch (e) {
      emit(LoginFailure(e.toString()));
    }
  }
}

// Access in Views
class LoginView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<LoginBloc, LoginState>(
      builder: (context, state) {
        // Build UI based on state...
      },
    );
  }
}
```

## Model Layer Implementation

The Model layer consists of repositories and services that provide data access to ViewModels. This layer abstracts away implementation details like network calls, database queries, and caching.

### Repository Pattern

Repositories provide type-safe access to domain entities:

```dart
abstract class AuthRepository {
  Future<User> login({required String email, required String password});
  Future<void> logout();
  Future<User?> getCurrentUser();
}

class AuthRepositoryImpl implements AuthRepository {
  final AuthApiService _apiService;
  final LocalStorageService _localStorage;

  AuthRepositoryImpl(this._apiService, this._localStorage);

  @override
  Future<User> login({
    required String email,
    required String password,
  }) async {
    final response = await _apiService.login(email, password);
    final user = User.fromJson(response.data);
    await _localStorage.saveUser(user);
    return user;
  }

  @override
  Future<void> logout() async {
    await _apiService.logout();
    await _localStorage.clearUser();
  }

  @override
  Future<User?> getCurrentUser() async {
    return await _localStorage.getUser();
  }
}
```

### Service Pattern

Services combine multiple repositories for complex operations:

```dart
class UserProfileService {
  final UserRepository _userRepository;
  final ImageRepository _imageRepository;
  final AnalyticsService _analytics;

  UserProfileService(
    this._userRepository,
    this._imageRepository,
    this._analytics,
  );

  Future<UserProfile> loadUserProfile(String userId) async {
    final user = await _userRepository.getUser(userId);
    final profileImage = await _imageRepository.getImage(user.imageId);

    _analytics.trackProfileView(userId);

    return UserProfile(
      user: user,
      profileImage: profileImage,
    );
  }
}
```

## Data Transformation

One of the ViewModel's key responsibilities is transforming data from the Model layer into a format suitable for display. This often involves:

### Formatting Data

Converting raw data into user-friendly formats:

```dart
class ProductListViewModel extends ChangeNotifier {
  final ProductRepository _productRepository;

  List<ProductListItem> _items = [];
  List<ProductListItem> get items => _items;

  Future<void> loadProducts() async {
    final products = await _productRepository.getProducts();

    _items = products.map((product) => ProductListItem(
      id: product.id,
      name: product.name,
      // Transform price to formatted string
      price: '\$${product.price.toStringAsFixed(2)}',
      // Transform boolean to user-friendly text
      availability: product.inStock ? 'In Stock' : 'Out of Stock',
      // Transform rating to star display
      rating: '⭐' * product.rating.round(),
    )).toList();

    notifyListeners();
  }
}

class ProductListItem {
  final String id;
  final String name;
  final String price;
  final String availability;
  final String rating;

  ProductListItem({
    required this.id,
    required this.name,
    required this.price,
    required this.availability,
    required this.rating,
  });
}
```

### Aggregating Data

Combining data from multiple sources:

```dart
class DashboardViewModel extends ChangeNotifier {
  final OrderRepository _orderRepository;
  final ProductRepository _productRepository;
  final UserRepository _userRepository;

  DashboardData? _dashboardData;
  DashboardData? get dashboardData => _dashboardData;

  Future<void> loadDashboard() async {
    final results = await Future.wait([
      _orderRepository.getRecentOrders(),
      _productRepository.getFeaturedProducts(),
      _userRepository.getCurrentUser(),
    ]);

    _dashboardData = DashboardData(
      recentOrders: results[0] as List<Order>,
      featuredProducts: results[1] as List<Product>,
      userName: (results[2] as User).name,
      // Computed from multiple sources
      totalSpent: (results[0] as List<Order>)
          .fold(0.0, (sum, order) => sum + order.total),
    );

    notifyListeners();
  }
}
```

### Filtering and Sorting

Processing data for display:

```dart
class ProductSearchViewModel extends ChangeNotifier {
  final ProductRepository _productRepository;

  List<Product> _allProducts = [];
  String _searchQuery = '';
  SortOption _sortOption = SortOption.name;

  List<Product> get displayedProducts {
    var filtered = _allProducts;

    // Filter by search query
    if (_searchQuery.isNotEmpty) {
      filtered = filtered
          .where((p) => p.name.toLowerCase().contains(_searchQuery.toLowerCase()))
          .toList();
    }

    // Sort based on selected option
    switch (_sortOption) {
      case SortOption.name:
        filtered.sort((a, b) => a.name.compareTo(b.name));
        break;
      case SortOption.price:
        filtered.sort((a, b) => a.price.compareTo(b.price));
        break;
      case SortOption.rating:
        filtered.sort((a, b) => b.rating.compareTo(a.rating));
        break;
    }

    return filtered;
  }

  void updateSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void updateSortOption(SortOption option) {
    _sortOption = option;
    notifyListeners();
  }
}
```

## Form Handling in MVVM

Forms are a common UI pattern that MVVM handles elegantly. ViewModels manage form state, validation, and submission.

### Form State Management

```dart
class RegistrationViewModel extends ChangeNotifier {
  final UserRepository _userRepository;

  // Form fields
  String _email = '';
  String _password = '';
  String _confirmPassword = '';

  // Validation errors
  String? _emailError;
  String? _passwordError;
  String? _confirmPasswordError;

  // Form state
  bool _isSubmitting = false;

  // Getters
  String get email => _email;
  String get password => _password;
  String get confirmPassword => _confirmPassword;
  String? get emailError => _emailError;
  String? get passwordError => _passwordError;
  String? get confirmPasswordError => _confirmPasswordError;
  bool get isSubmitting => _isSubmitting;

  bool get canSubmit =>
      _email.isNotEmpty &&
      _password.isNotEmpty &&
      _confirmPassword.isNotEmpty &&
      _emailError == null &&
      _passwordError == null &&
      _confirmPasswordError == null &&
      !_isSubmitting;

  void updateEmail(String value) {
    _email = value;
    _validateEmail();
    notifyListeners();
  }

  void updatePassword(String value) {
    _password = value;
    _validatePassword();
    _validateConfirmPassword(); // Re-validate confirm password
    notifyListeners();
  }

  void updateConfirmPassword(String value) {
    _confirmPassword = value;
    _validateConfirmPassword();
    notifyListeners();
  }

  void _validateEmail() {
    if (_email.isEmpty) {
      _emailError = null;
      return;
    }

    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(_email)) {
      _emailError = 'Please enter a valid email';
    } else {
      _emailError = null;
    }
  }

  void _validatePassword() {
    if (_password.isEmpty) {
      _passwordError = null;
      return;
    }

    if (_password.length < 8) {
      _passwordError = 'Password must be at least 8 characters';
    } else {
      _passwordError = null;
    }
  }

  void _validateConfirmPassword() {
    if (_confirmPassword.isEmpty) {
      _confirmPasswordError = null;
      return;
    }

    if (_password != _confirmPassword) {
      _confirmPasswordError = 'Passwords do not match';
    } else {
      _confirmPasswordError = null;
    }
  }

  Future<void> submit() async {
    if (!canSubmit) return;

    _isSubmitting = true;
    notifyListeners();

    try {
      await _userRepository.register(
        email: _email,
        password: _password,
      );
      // Handle success (navigation, callback, etc.)
    } catch (e) {
      // Handle error
    } finally {
      _isSubmitting = false;
      notifyListeners();
    }
  }
}
```

## Navigation in MVVM

Navigation presents a challenge in MVVM because ViewModels shouldn't reference Views or UI context. There are several approaches to handling navigation while maintaining separation.

### Navigation Callbacks

Pass navigation callbacks to ViewModels from Views:

```dart
class LoginViewModel extends ChangeNotifier {
  final AuthRepository _authRepository;
  final VoidCallback? onLoginSuccess;

  LoginViewModel(this._authRepository, {this.onLoginSuccess});

  Future<void> login() async {
    // ... login logic ...

    if (success) {
      onLoginSuccess?.call();
    }
  }
}

// In View
LoginViewModel(
  getIt<AuthRepository>(),
  onLoginSuccess: () {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const HomeView()),
    );
  },
)
```

### Navigation Service

Create a navigation service that ViewModels can use:

```dart
class NavigationService {
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  Future<void> navigateTo(String routeName) async {
    await navigatorKey.currentState?.pushNamed(routeName);
  }

  void goBack() {
    navigatorKey.currentState?.pop();
  }
}

// ViewModel uses navigation service
class LoginViewModel extends ChangeNotifier {
  final AuthRepository _authRepository;
  final NavigationService _navigationService;

  Future<void> login() async {
    // ... login logic ...

    if (success) {
      await _navigationService.navigateTo('/home');
    }
  }
}
```

### Stream-Based Navigation

Expose navigation events as streams that Views can listen to:

```dart
class LoginViewModel extends ChangeNotifier {
  final _navigationController = StreamController<NavigationEvent>();
  Stream<NavigationEvent> get navigationEvents =>
      _navigationController.stream;

  Future<void> login() async {
    // ... login logic ...

    if (success) {
      _navigationController.add(NavigateToHome());
    }
  }

  @override
  void dispose() {
    _navigationController.close();
    super.dispose();
  }
}

// In View
@override
void initState() {
  super.initState();
  widget.viewModel.navigationEvents.listen((event) {
    if (event is NavigateToHome) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const HomeView()),
      );
    }
  });
}
```

## Testing ViewModels

One of the primary benefits of MVVM is testability. ViewModels can be unit tested without any Flutter UI dependencies.

### Unit Testing ViewModels

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late LoginViewModel viewModel;
  late MockAuthRepository mockAuthRepository;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
    viewModel = LoginViewModel(mockAuthRepository);
  });

  tearDown(() {
    viewModel.dispose();
  });

  group('LoginViewModel', () {
    test('initial state is correct', () {
      expect(viewModel.email, '');
      expect(viewModel.password, '');
      expect(viewModel.isLoading, false);
      expect(viewModel.errorMessage, null);
    });

    test('updateEmail updates email and clears error', () {
      viewModel.updateEmail('test@example.com');

      expect(viewModel.email, 'test@example.com');
      expect(viewModel.errorMessage, null);
    });

    test('login sets loading state and calls repository', () async {
      when(mockAuthRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => User(id: '1', email: 'test@example.com'));

      viewModel.updateEmail('test@example.com');
      viewModel.updatePassword('password123');

      final loginFuture = viewModel.login();

      // Should be loading immediately
      expect(viewModel.isLoading, true);

      await loginFuture;

      // Should not be loading after completion
      expect(viewModel.isLoading, false);

      // Should have called repository
      verify(mockAuthRepository.login(
        email: 'test@example.com',
        password: 'password123',
      )).called(1);
    });

    test('login handles errors correctly', () async {
      when(mockAuthRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenThrow(Exception('Invalid credentials'));

      viewModel.updateEmail('test@example.com');
      viewModel.updatePassword('wrongpassword');

      await viewModel.login();

      expect(viewModel.isLoading, false);
      expect(viewModel.errorMessage, contains('Invalid credentials'));
    });
  });
}
```

## Common Pitfalls and How to Avoid Them

### Putting Business Logic in Views

**Problem**: Developers often put business logic directly in Views, defeating the purpose of MVVM.

**Solution**: If you find yourself writing complex logic in a View's build method or event handlers, extract that logic into the ViewModel.

### ViewModels Referencing Views

**Problem**: ViewModels that import Flutter UI packages or reference Views directly can't be unit tested easily.

**Solution**: ViewModels should only expose state and methods. Use callbacks, streams, or navigation services for View-related actions.

### Sharing ViewModels Across Views

**Problem**: Trying to reuse the same ViewModel instance across multiple Views leads to bloated ViewModels with conditional logic.

**Solution**: Create dedicated ViewModels for each View. Extract shared logic into services that ViewModels can use.

### Not Handling Loading and Error States

**Problem**: Views that don't handle loading and error states provide poor user experience.

**Solution**: Every ViewModel that fetches data should expose loading and error state. Every View should display appropriate UI for these states.

### Forgetting to Dispose ViewModels

**Problem**: ViewModels with streams or listeners that aren't disposed cause memory leaks.

**Solution**: Always override dispose() and clean up resources. Use state management solutions that automatically handle disposal when appropriate.

## MVVM in Practice

MVVM is not a rigid framework but a flexible pattern that can be adapted to your needs. The core principles - separation of concerns, unidirectional dependencies, and testability - remain constant regardless of implementation details.

Start with simple ViewModels and Views. As you gain experience with the pattern, you'll develop intuition for where logic belongs and how to structure features for maximum maintainability.

Remember that MVVM works best when combined with other patterns and principles: Clean Architecture for overall system structure, SOLID principles for class design, and appropriate design patterns for specific problems.

The investment in learning and applying MVVM pays dividends as your Flutter application grows. Features that are easy to develop, test, and maintain lead to faster development cycles, fewer bugs, and happier users.
