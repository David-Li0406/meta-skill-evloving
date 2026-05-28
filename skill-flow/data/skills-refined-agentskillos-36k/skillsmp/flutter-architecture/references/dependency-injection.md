# Dependency Injection in Flutter

Dependency Injection (DI) is a design pattern that implements Inversion of Control (IoC) for resolving dependencies. Instead of classes creating their own dependencies, dependencies are provided from outside, making code more modular, testable, and maintainable.

## Why Dependency Injection

Without dependency injection, classes create and manage their own dependencies, leading to tight coupling and testing difficulties.

### The Problem: Hard-Coded Dependencies

```dart
class UserProfileViewModel {
  // Hard-coded dependencies
  final UserRepository _repository = UserRepositoryImpl();
  final ImageService _imageService = ImageService();
  final AnalyticsService _analytics = AnalyticsService();

  Future<void> loadProfile() async {
    // Use dependencies...
  }
}
```

**Problems with this approach**:

- **Tight Coupling**: ViewModel is tightly coupled to specific implementations
- **Difficult Testing**: Can't substitute mock implementations for testing
- **Inflexible Configuration**: Can't easily switch implementations for different environments
- **Hidden Dependencies**: Dependencies aren't visible in the class interface
- **Lifecycle Management**: No control over when dependencies are created or disposed

### The Solution: Dependency Injection

```dart
class UserProfileViewModel {
  final UserRepository _repository;
  final ImageService _imageService;
  final AnalyticsService _analytics;

  UserProfileViewModel(
    this._repository,
    this._imageService,
    this._analytics,
  );

  Future<void> loadProfile() async {
    // Use dependencies...
  }
}
```

**Benefits**:

- **Loose Coupling**: ViewModel depends on abstractions, not concrete implementations
- **Easy Testing**: Can pass mock implementations in tests
- **Flexible Configuration**: Can provide different implementations for dev/prod
- **Explicit Dependencies**: Dependencies are visible in the constructor
- **Lifecycle Control**: External control over dependency creation and disposal

## Dependency Injection Fundamentals

Dependency Injection follows the Dependency Inversion Principle (the "D" in SOLID): high-level modules should depend on abstractions, not concrete implementations.

### Constructor Injection

Constructor injection is the recommended form of dependency injection in Flutter. Dependencies are provided through the class constructor:

```dart
abstract class AuthRepository {
  Future<User> login(String email, String password);
}

class AuthRepositoryImpl implements AuthRepository {
  final ApiService _apiService;
  final StorageService _storageService;

  AuthRepositoryImpl(this._apiService, this._storageService);

  @override
  Future<User> login(String email, String password) async {
    // Implementation...
  }
}
```

**Advantages**:
- Dependencies are explicit and visible
- Compiler enforces that all dependencies are provided
- Immutability: dependencies can be `final`
- Easy to unit test

**Best Practice**: If you can't tell what a class depends on by reading its constructor, your dependency injection has failed.

### Property Injection

Property injection sets dependencies through setter methods or public properties. Avoid this pattern in Flutter:

```dart
// Don't do this
class UserService {
  late UserRepository repository;

  void loadUser() {
    repository.getUser(); // Might throw if not set!
  }
}
```

Property injection makes dependencies optional and hidden, leading to runtime errors if dependencies aren't set before use.

### Method Injection

Method injection provides dependencies through method parameters. Use this for dependencies that vary per method call:

```dart
class ReportGenerator {
  void generateReport(ReportData data, OutputFormatter formatter) {
    final formatted = formatter.format(data);
    // Save or display report...
  }
}
```

Method injection is appropriate when different method calls need different implementations, but constructor injection is preferred for dependencies used throughout the class.

## get_it: Service Locator for Flutter

get_it is Flutter's most popular dependency injection solution. It implements the Service Locator pattern, providing a global registry where you register dependencies and retrieve them when needed.

### Why get_it

**Simple API**: Easy to learn and use, with minimal boilerplate
**No Code Generation Required**: Works without build_runner (though it pairs well with injectable)
**Framework Agnostic**: Works with any Dart project, not just Flutter
**Flexible Lifecycles**: Supports singletons, factories, and lazy singletons
**Named Instances**: Can register multiple instances of the same type with different names
**Async Registration**: Supports asynchronous initialization
**Large Ecosystem**: Well-maintained with extensive community support

### Basic Setup

Add get_it to your `pubspec.yaml`:

```yaml
dependencies:
  get_it: ^7.6.0
```

Create a service locator file:

```dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

void setupDependencies() {
  // Register dependencies here
}
```

Initialize in your main function:

```dart
void main() {
  setupDependencies();
  runApp(const MyApp());
}
```

### Registering Dependencies

get_it provides several registration methods with different lifecycle behaviors.

#### Factory Registration

Creates a new instance every time it's requested:

```dart
getIt.registerFactory<UserRepository>(
  () => UserRepositoryImpl(
    getIt<ApiService>(),
    getIt<StorageService>(),
  ),
);
```

**Use for**: Short-lived objects, ViewModels, objects that hold state

#### Singleton Registration

Creates one instance that's reused for all requests:

```dart
getIt.registerSingleton<ApiService>(
  ApiService(baseUrl: 'https://api.example.com'),
);
```

**Use for**: App-wide services, configuration, objects without mutable state

#### Lazy Singleton Registration

Creates one instance on first request, then reuses it:

```dart
getIt.registerLazySingleton<DatabaseService>(
  () => DatabaseService(),
);
```

**Use for**: Expensive-to-create singletons that might not be needed immediately

**Important**: Most memory leaks in Flutter apps come from incorrect lifecycle management. Use factory registration for ViewModels and other stateful objects that should be recreated. Use singleton registration only for truly global, stateless services.

### Resolving Dependencies

Retrieve dependencies using the call operator or get method:

```dart
// Using call operator (recommended)
final repository = getIt<UserRepository>();

// Using get method (explicit)
final repository = getIt.get<UserRepository>();

// Check if registered
if (getIt.isRegistered<UserRepository>()) {
  final repository = getIt<UserRepository>();
}
```

### Async Dependencies

Some dependencies require asynchronous initialization (databases, shared preferences, etc.):

```dart
void setupDependencies() async {
  // Register async singleton
  getIt.registerSingletonAsync<DatabaseService>(
    () async {
      final db = DatabaseService();
      await db.initialize();
      return db;
    },
  );

  // Wait for async dependencies
  await getIt.allReady();
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupDependencies();
  runApp(const MyApp());
}
```

### Named Instances

Register multiple instances of the same type with different names:

```dart
getIt.registerSingleton<ApiService>(
  ApiService(baseUrl: 'https://api.example.com'),
  instanceName: 'production',
);

getIt.registerSingleton<ApiService>(
  ApiService(baseUrl: 'https://dev-api.example.com'),
  instanceName: 'development',
);

// Retrieve named instance
final api = getIt<ApiService>(instanceName: 'production');
```

## injectable: Code Generation for get_it

injectable is a code generation package that reduces boilerplate when setting up get_it. It uses annotations to automatically generate registration code.

### Setup

Add dependencies to `pubspec.yaml`:

```yaml
dependencies:
  get_it: ^7.6.0
  injectable: ^2.3.0

dev_dependencies:
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
```

### Configuration

Create an injection configuration file:

```dart
// lib/core/di/injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

import 'injection.config.dart';

final getIt = GetIt.instance;

@InjectableInit()
void configureDependencies() => getIt.init();
```

### Annotations

injectable provides several annotations for different registration types.

#### @injectable

Registers as a factory (new instance each time):

```dart
@injectable
class UserRepository {
  final ApiService _apiService;

  UserRepository(this._apiService);
}
```

#### @singleton

Registers as a singleton (one instance, created immediately):

```dart
@singleton
class ApiService {
  final String baseUrl;

  ApiService(@Named('apiUrl') this.baseUrl);
}
```

#### @lazySingleton

Registers as a lazy singleton (one instance, created on first use):

```dart
@lazySingleton
class DatabaseService {
  Future<void> initialize() async {
    // Initialize database...
  }
}
```

#### @Named

Provides named instances:

```dart
@module
abstract class ConfigModule {
  @Named('apiUrl')
  String get apiUrl => 'https://api.example.com';

  @Named('apiKey')
  String get apiKey => const String.fromEnvironment('API_KEY');
}
```

### Registering Interfaces

Use the `as` parameter to register implementations against interfaces:

```dart
@Injectable(as: UserRepository)
class UserRepositoryImpl implements UserRepository {
  final ApiService _apiService;

  UserRepositoryImpl(this._apiService);

  @override
  Future<User> getUser(String id) async {
    // Implementation...
  }
}
```

Now you can inject `UserRepository` and get `UserRepositoryImpl`:

```dart
@injectable
class UserProfileViewModel {
  final UserRepository _repository; // Receives UserRepositoryImpl

  UserProfileViewModel(this._repository);
}
```

### Modules

Modules provide dependencies that require manual registration (third-party packages, platform-specific code):

```dart
@module
abstract class AppModule {
  @lazySingleton
  Dio get dio => Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: const Duration(seconds: 5),
    ),
  );

  @preResolve // For async dependencies
  Future<SharedPreferences> get prefs => SharedPreferences.getInstance();

  @lazySingleton
  Database get database => Database.instance;
}
```

**@preResolve**: Marks async dependencies that should be resolved before the app starts. Call `await getIt.allReady()` after `configureDependencies()`.

### Environment Support

injectable supports different configurations for different environments:

```dart
@Injectable(as: ApiService, env: [Environment.dev])
class DevApiService implements ApiService {
  // Development implementation
}

@Injectable(as: ApiService, env: [Environment.prod])
class ProdApiService implements ApiService {
  // Production implementation
}

// Configure for specific environment
@InjectableInit(
  initializerName: 'init',
  preferRelativeImports: true,
  asExtension: true,
)
void configureDependencies(String environment) {
  getIt.init(environment: environment);
}

// Use in main
void main() {
  const environment = String.fromEnvironment(
    'ENV',
    defaultValue: Environment.dev,
  );
  configureDependencies(environment);
  runApp(const MyApp());
}
```

### Code Generation

Run build_runner to generate registration code:

```bash
# One-time generation
flutter pub run build_runner build

# Watch mode (regenerates on file changes)
flutter pub run build_runner watch

# Clean build (removes old generated files)
flutter pub run build_runner build --delete-conflicting-outputs
```

This generates `injection.config.dart` with all registration code:

```dart
// GENERATED CODE - DO NOT MODIFY BY HAND

extension GetItInjectableX on GetIt {
  void init({String? environment}) {
    final gh = GetItHelper(this, environment);

    gh.factory<UserRepository>(
      () => UserRepositoryImpl(gh<ApiService>()),
    );
    gh.singleton<ApiService>(
      ApiService(gh<String>(instanceName: 'apiUrl')),
    );
    // ... more registrations
  }
}
```

## Dependency Injection Best Practices

### 1. Centralize Registration

Keep all dependency registration in one place (typically `lib/core/di/injection.dart`). This makes it easy to see all dependencies and their lifecycles.

```dart
void configureDependencies() {
  // Core services
  getIt.registerLazySingleton<ApiService>(() => ApiService());
  getIt.registerLazySingleton<DatabaseService>(() => DatabaseService());

  // Repositories
  getIt.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(getIt(), getIt()),
  );

  // ViewModels (factories - new instance each time)
  getIt.registerFactory<LoginViewModel>(
    () => LoginViewModel(getIt()),
  );
}
```

### 2. Use Constructor Injection

Always use constructor injection to make dependencies explicit:

```dart
// Good
class UserService {
  final UserRepository _repository;
  final AnalyticsService _analytics;

  UserService(this._repository, this._analytics);
}

// Bad
class UserService {
  final _repository = getIt<UserRepository>();
  final _analytics = getIt<AnalyticsService>();
}
```

The bad example hides dependencies and makes testing difficult.

### 3. Depend on Abstractions

Inject interfaces, not concrete implementations:

```dart
// Good
class UserViewModel {
  final UserRepository _repository; // Interface

  UserViewModel(this._repository);
}

// Bad
class UserViewModel {
  final UserRepositoryImpl _repository; // Concrete implementation

  UserViewModel(this._repository);
}
```

### 4. Manage Lifecycles Carefully

Choose the appropriate registration method based on lifecycle needs:

```dart
// Singleton: App-wide, stateless services
getIt.registerSingleton<ApiService>(ApiService());

// Lazy Singleton: Expensive but stateless services
getIt.registerLazySingleton<DatabaseService>(() => DatabaseService());

// Factory: Stateful objects, ViewModels
getIt.registerFactory<LoginViewModel>(() => LoginViewModel(getIt()));
```

**Common mistake**: Registering ViewModels as singletons. ViewModels hold state and should be created fresh for each use.

### 5. Use Environment-Specific Dependencies

Provide different implementations for development and production:

```dart
@Injectable(as: ApiService, env: [Environment.dev])
class MockApiService implements ApiService {
  @override
  Future<User> getUser(String id) async {
    // Return mock data
    return User.mock();
  }
}

@Injectable(as: ApiService, env: [Environment.prod])
class HttpApiService implements ApiService {
  final Dio _dio;

  HttpApiService(this._dio);

  @override
  Future<User> getUser(String id) async {
    final response = await _dio.get('/users/$id');
    return User.fromJson(response.data);
  }
}
```

### 6. Test with Dependency Injection

DI makes testing straightforward - just inject mocks instead of real implementations:

```dart
void main() {
  late LoginViewModel viewModel;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    viewModel = LoginViewModel(mockRepository);
  });

  test('login calls repository with correct credentials', () async {
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => User.test());

    await viewModel.login('test@example.com', 'password');

    verify(() => mockRepository.login('test@example.com', 'password'))
        .called(1);
  });
}
```

No need to configure get_it or use the service locator in tests.

### 7. Avoid Service Locator Anti-Pattern

While get_it is a service locator, use it only at the composition root. Don't call `getIt<T>()` throughout your code:

```dart
// Bad: Service locator calls scattered everywhere
class UserService {
  void doSomething() {
    final repo = getIt<UserRepository>();
    final analytics = getIt<AnalyticsService>();
    // ...
  }
}

// Good: Dependencies injected via constructor
class UserService {
  final UserRepository _repository;
  final AnalyticsService _analytics;

  UserService(this._repository, this._analytics);

  void doSomething() {
    // Use injected dependencies
  }
}
```

## Dependency Injection Patterns

### Factory Pattern with DI

Factories can use DI to create complex objects:

```dart
@injectable
class OrderFactory {
  final UserRepository _userRepository;
  final ProductRepository _productRepository;

  OrderFactory(this._userRepository, this._productRepository);

  Future<Order> createOrder(CreateOrderParams params) async {
    final user = await _userRepository.getCurrentUser();
    final products = await _productRepository.getProducts(params.productIds);

    return Order(
      userId: user.id,
      products: products,
      total: products.fold(0.0, (sum, p) => sum + p.price),
      createdAt: DateTime.now(),
    );
  }
}
```

### Repository Pattern with DI

Repositories inject data sources and other dependencies:

```dart
@Injectable(as: UserRepository)
class UserRepositoryImpl implements UserRepository {
  final ApiService _apiService;
  final CacheService _cacheService;
  final NetworkInfo _networkInfo;

  UserRepositoryImpl(
    this._apiService,
    this._cacheService,
    this._networkInfo,
  );

  @override
  Future<User> getUser(String id) async {
    if (await _networkInfo.isConnected) {
      final user = await _apiService.getUser(id);
      await _cacheService.saveUser(user);
      return user;
    } else {
      return await _cacheService.getUser(id);
    }
  }
}
```

### Chain of Responsibility with DI

DI makes it easy to set up chains of handlers:

```dart
@module
abstract class ErrorHandlerModule {
  @singleton
  ErrorHandler get errorHandler {
    return NetworkErrorHandler(
      next: ValidationErrorHandler(
        next: GenericErrorHandler(),
      ),
    );
  }
}

abstract class ErrorHandler {
  final ErrorHandler? next;

  ErrorHandler({this.next});

  String handle(Exception error) {
    if (canHandle(error)) {
      return doHandle(error);
    } else if (next != null) {
      return next!.handle(error);
    } else {
      return 'An unexpected error occurred';
    }
  }

  bool canHandle(Exception error);
  String doHandle(Exception error);
}
```

## Integration with State Management

Dependency injection works seamlessly with all state management solutions.

### With Provider

```dart
void main() {
  configureDependencies();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => getIt<LoginViewModel>(),
        ),
        Provider(
          create: (_) => getIt<AuthService>(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

### With Riverpod

```dart
final authRepositoryProvider = Provider<AuthRepository>(
  (ref) => getIt<AuthRepository>(),
);

final loginViewModelProvider = ChangeNotifierProvider.autoDispose(
  (ref) => LoginViewModel(ref.watch(authRepositoryProvider)),
);
```

### With BLoC

```dart
void main() {
  configureDependencies();

  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (_) => getIt<LoginBloc>(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

## Common Pitfalls

### Circular Dependencies

When A depends on B and B depends on A:

```dart
// This will fail!
@injectable
class ServiceA {
  final ServiceB _serviceB;
  ServiceA(this._serviceB);
}

@injectable
class ServiceB {
  final ServiceA _serviceA;
  ServiceB(this._serviceA);
}
```

**Solution**: Refactor to extract shared logic into a third service, or use lazy injection.

### Forgetting to Register

Using a dependency without registering it:

```dart
// Registered
@injectable
class UserRepository { }

// Not registered
class ProductRepository { }

// This will throw at runtime!
final repo = getIt<ProductRepository>();
```

**Solution**: Ensure all dependencies are annotated with injectable annotations or manually registered.

### Wrong Lifecycle

Registering ViewModels as singletons:

```dart
// Bad: ViewModel holds state and should be factory
@singleton
class LoginViewModel extends ChangeNotifier { }

// Good: Factory creates new instance
@injectable
class LoginViewModel extends ChangeNotifier { }
```

**Solution**: Use factory registration for stateful objects.

## Testing with Dependency Injection

Dependency injection dramatically simplifies testing.

### Unit Testing

Test classes in isolation with mock dependencies:

```dart
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late UserService service;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    service = UserService(mockRepository);
  });

  test('getUserById returns user from repository', () async {
    final user = User(id: '1', name: 'Test');
    when(() => mockRepository.getUser('1'))
        .thenAnswer((_) async => user);

    final result = await service.getUserById('1');

    expect(result, user);
  });
}
```

### Widget Testing

Override dependencies for widget tests:

```dart
void main() {
  late MockAuthRepository mockAuthRepository;

  setUp(() {
    mockAuthRepository = MockAuthRepository();

    // Reset and configure get_it for testing
    getIt.reset();
    getIt.registerFactory<AuthRepository>(() => mockAuthRepository);
    getIt.registerFactory<LoginViewModel>(
      () => LoginViewModel(getIt<AuthRepository>()),
    );
  });

  testWidgets('login button triggers login', (tester) async {
    when(() => mockAuthRepository.login(any(), any()))
        .thenAnswer((_) async => User.test());

    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => getIt<LoginViewModel>(),
        child: const MaterialApp(home: LoginView()),
      ),
    );

    await tester.enterText(find.byType(TextField).first, 'test@example.com');
    await tester.enterText(find.byType(TextField).last, 'password');
    await tester.tap(find.byType(ElevatedButton));

    await tester.pump();

    verify(() => mockAuthRepository.login('test@example.com', 'password'))
        .called(1);
  });
}
```

### Integration Testing

For integration tests, you can use real implementations or a mix of real and mock:

```dart
void main() {
  setUpAll(() {
    configureDependencies();

    // Override specific dependencies
    getIt.allowReassignment = true;
    getIt.registerSingleton<ApiService>(
      MockApiService(), // Use mock API for integration tests
    );
  });

  testWidgets('complete user flow', (tester) async {
    // Test with mostly real implementations but mock API
  });
}
```

## Dependency Injection in Practice

Dependency injection is essential for building maintainable Flutter applications. By making dependencies explicit and injectable, you create code that's easier to understand, test, and modify.

Start simple: use constructor injection and register dependencies manually with get_it. As your application grows, adopt injectable for code generation to reduce boilerplate.

Remember the core principles:

- Make dependencies explicit through constructor parameters
- Depend on abstractions, not concrete implementations
- Manage lifecycles appropriately (factory vs singleton)
- Design for testability from the beginning
- Use environment-specific dependencies for dev/prod configurations

The investment in proper dependency injection pays dividends throughout the lifetime of your application. Features become easier to test, modify, and extend. New developers can understand dependencies at a glance. And your codebase remains flexible as requirements evolve.
