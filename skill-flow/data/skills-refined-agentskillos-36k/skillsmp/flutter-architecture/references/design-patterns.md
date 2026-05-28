# Design Patterns in Flutter

Design patterns are reusable solutions to common programming problems. In Flutter applications, certain patterns appear repeatedly and provide proven approaches to organizing code, managing dependencies, and structuring features.

## Why Design Patterns Matter

Design patterns provide several benefits in Flutter development:

**Common Vocabulary**: Patterns give teams a shared language. Saying "use the repository pattern" immediately communicates structure and intent.

**Proven Solutions**: Patterns represent solutions that have been refined over time and proven effective across many projects.

**Best Practices**: Following established patterns naturally leads to better code organization and architecture.

**Easier Onboarding**: Developers familiar with common patterns can quickly understand codebases that use them.

**Reduced Bugs**: Patterns help avoid common pitfalls and edge cases that have already been solved.

## Repository Pattern

The repository pattern provides an abstraction layer between the domain layer and data sources. Repositories hide the implementation details of data access and provide a clean API for business logic.

### Purpose

Repositories serve as the source of truth for domain entities. They:

- Abstract data access implementation details
- Provide a type-safe API for data operations
- Handle data source selection (network, cache, database)
- Manage caching strategies
- Transform raw data into domain entities

### Implementation

Define repository interface in domain layer:

```dart
abstract class ProductRepository {
  Future<List<Product>> getProducts();
  Future<Product> getProduct(String id);
  Future<Product> createProduct(CreateProductParams params);
  Future<Product> updateProduct(String id, UpdateProductParams params);
  Future<void> deleteProduct(String id);
  Stream<List<Product>> watchProducts();
}
```

Implement in data layer:

```dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductApiService _apiService;
  final ProductDatabaseService _databaseService;
  final NetworkInfo _networkInfo;

  ProductRepositoryImpl(
    this._apiService,
    this._databaseService,
    this._networkInfo,
  );

  @override
  Future<List<Product>> getProducts() async {
    try {
      if (await _networkInfo.isConnected) {
        // Fetch from network
        final dtos = await _apiService.getProducts();
        final products = dtos.map((dto) => dto.toEntity()).toList();

        // Update cache
        await _databaseService.cacheProducts(products);

        return products;
      } else {
        // Return cached data
        return await _databaseService.getProducts();
      }
    } on ServerException catch (e) {
      // Fallback to cache on server error
      final cached = await _databaseService.getProducts();
      if (cached.isEmpty) {
        throw DataException('No cached data available');
      }
      return cached;
    }
  }

  @override
  Stream<List<Product>> watchProducts() {
    return _databaseService.watchProducts();
  }

  // ... other methods
}
```

### Benefits

**Abstraction**: Business logic doesn't know if data comes from network, database, or memory.

**Testability**: Easy to mock repositories for testing use cases and ViewModels.

**Flexibility**: Change data sources without modifying business logic.

**Caching Control**: Centralize caching logic in one place.

**Error Handling**: Convert low-level exceptions to domain-appropriate errors.

### When to Use

Use repositories for:
- Accessing domain entities (users, products, orders)
- Operations that may involve multiple data sources
- Data that needs caching
- Any data access that business logic depends on

Don't use repositories for:
- Simple configuration values
- Temporary UI state
- Single-use API calls that don't map to domain entities

## Service Pattern

Services encapsulate business logic that doesn't fit naturally into entities or repositories. While repositories focus on data access for specific entities, services orchestrate complex operations involving multiple repositories.

### Purpose

Services handle:
- Complex business operations involving multiple entities
- Operations that span multiple repositories
- Business logic that doesn't belong to a single entity
- Coordination between different parts of the domain

### Implementation

```dart
class OrderService {
  final ProductRepository _productRepository;
  final UserRepository _userRepository;
  final PaymentService _paymentService;
  final InventoryService _inventoryService;
  final NotificationService _notificationService;

  OrderService(
    this._productRepository,
    this._userRepository,
    this._paymentService,
    this._inventoryService,
    this._notificationService,
  );

  Future<Order> createOrder(CreateOrderParams params) async {
    // Validate user
    final user = await _userRepository.getCurrentUser();
    if (!user.canPlaceOrders) {
      throw UnauthorizedException('User cannot place orders');
    }

    // Get products and calculate total
    final products = await _productRepository.getProductsByIds(
      params.productIds,
    );
    final total = _calculateTotal(products, params.quantities);

    // Check inventory
    final available = await _inventoryService.checkAvailability(
      products,
      params.quantities,
    );
    if (!available) {
      throw BusinessException('Some products are out of stock');
    }

    // Process payment
    final payment = await _paymentService.processPayment(
      userId: user.id,
      amount: total,
      paymentMethod: params.paymentMethod,
    );

    // Create order
    final order = Order(
      id: generateId(),
      userId: user.id,
      products: products,
      total: total,
      paymentId: payment.id,
      status: OrderStatus.confirmed,
      createdAt: DateTime.now(),
    );

    // Reserve inventory
    await _inventoryService.reserveProducts(products, params.quantities);

    // Send confirmation
    await _notificationService.sendOrderConfirmation(order);

    return order;
  }

  double _calculateTotal(List<Product> products, Map<String, int> quantities) {
    return products.fold(0.0, (sum, product) {
      final quantity = quantities[product.id] ?? 1;
      return sum + (product.price * quantity);
    });
  }
}
```

### Service vs Repository

**Repository**:
- Focuses on data access for one entity type
- Transforms data between sources and domain entities
- Typically one repository per entity
- Lives in data layer (implementation) and domain layer (interface)

**Service**:
- Orchestrates complex business operations
- Coordinates multiple repositories
- Contains business logic
- Lives in domain layer

### When to Use

Use services for:
- Operations involving multiple entities
- Complex business workflows
- Operations that need to coordinate multiple repositories
- Business logic that doesn't belong to a single entity

Example service scenarios:
- Order processing (involves user, products, payment, inventory)
- User registration (involves user creation, email verification, analytics)
- Report generation (aggregates data from multiple sources)

## Factory Pattern

The factory pattern encapsulates object creation logic. Instead of calling constructors directly, you call factory methods that handle creation complexity.

### Purpose

Factories provide:
- Centralized object creation logic
- Complex initialization sequences
- Conditional object creation based on parameters
- Abstraction of creation details from consumers

### Implementation

#### Simple Factory

```dart
class UserFactory {
  static User createUser({
    required String email,
    required String name,
    UserRole role = UserRole.user,
  }) {
    return User(
      id: generateId(),
      email: email.toLowerCase().trim(),
      name: name.trim(),
      role: role,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  static User createAdmin(String email, String name) {
    return User(
      id: generateId(),
      email: email.toLowerCase().trim(),
      name: name.trim(),
      role: UserRole.admin,
      permissions: AdminPermissions.all(),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }
}
```

#### Factory with Dependencies

```dart
class OrderFactory {
  final UserRepository _userRepository;
  final ProductRepository _productRepository;

  OrderFactory(this._userRepository, this._productRepository);

  Future<Order> createOrder(CreateOrderParams params) async {
    final user = await _userRepository.getCurrentUser();
    final products = await _productRepository.getProductsByIds(
      params.productIds,
    );

    return Order(
      id: generateId(),
      userId: user.id,
      userEmail: user.email,
      products: products,
      total: _calculateTotal(products),
      status: OrderStatus.pending,
      createdAt: DateTime.now(),
    );
  }

  double _calculateTotal(List<Product> products) {
    return products.fold(0.0, (sum, p) => sum + p.price);
  }
}
```

#### Abstract Factory

Abstract factories create families of related objects:

```dart
abstract class ThemeFactory {
  AppColors createColors();
  TextTheme createTextTheme();
  ButtonTheme createButtonTheme();
}

class LightThemeFactory implements ThemeFactory {
  @override
  AppColors createColors() => AppColors.light();

  @override
  TextTheme createTextTheme() => TextTheme.light();

  @override
  ButtonTheme createButtonTheme() => ButtonTheme.light();
}

class DarkThemeFactory implements ThemeFactory {
  @override
  AppColors createColors() => AppColors.dark();

  @override
  TextTheme createTextTheme() => TextTheme.dark();

  @override
  ButtonTheme createButtonTheme() => ButtonTheme.dark();
}
```

### When to Use

Use factories when:
- Object creation involves complex logic
- Objects need default values or validation during creation
- Creation logic should be centralized
- You need to create families of related objects
- Creation depends on configuration or environment

## Singleton Pattern

The singleton pattern ensures only one instance of a class exists. In Flutter, use dependency injection instead of implementing singletons manually.

### Purpose

Singletons provide:
- Single instance across the application
- Global access point
- Lazy or eager initialization
- Resource sharing (database connections, API clients)

### Implementation with get_it

Don't implement singletons manually. Use get_it's singleton registration:

```dart
// Manual singleton (don't do this)
class ApiService {
  static final ApiService _instance = ApiService._internal();

  factory ApiService() => _instance;

  ApiService._internal();

  // ...
}

// Better: Use get_it (do this)
@singleton
class ApiService {
  final String baseUrl;

  ApiService(@Named('apiUrl') this.baseUrl);

  // ...
}
```

### Types of Singletons in get_it

**Eager Singleton**: Created immediately at registration

```dart
getIt.registerSingleton<ApiService>(
  ApiService(baseUrl: 'https://api.example.com'),
);
```

**Lazy Singleton**: Created on first access

```dart
getIt.registerLazySingleton<DatabaseService>(
  () => DatabaseService(),
);
```

### When to Use

Use singleton registration for:
- API clients and HTTP clients
- Database connections
- Analytics services
- Configuration objects
- Logging services

Don't use singleton registration for:
- ViewModels (use factory)
- Repositories that hold state
- Objects that should be recreated

## Builder Pattern

The builder pattern constructs complex objects step by step. Flutter's widget system uses this pattern extensively.

### Purpose

Builders provide:
- Step-by-step object construction
- Fluent API for configuration
- Optional parameters with sensible defaults
- Validation before construction

### Implementation

```dart
class QueryBuilder {
  String? _table;
  List<String>? _columns;
  String? _where;
  List<dynamic>? _whereArgs;
  String? _orderBy;
  int? _limit;

  QueryBuilder table(String table) {
    _table = table;
    return this;
  }

  QueryBuilder columns(List<String> columns) {
    _columns = columns;
    return this;
  }

  QueryBuilder where(String where, List<dynamic> whereArgs) {
    _where = where;
    _whereArgs = whereArgs;
    return this;
  }

  QueryBuilder orderBy(String orderBy) {
    _orderBy = orderBy;
    return this;
  }

  QueryBuilder limit(int limit) {
    _limit = limit;
    return this;
  }

  Query build() {
    if (_table == null) {
      throw StateError('Table must be specified');
    }

    return Query(
      table: _table!,
      columns: _columns,
      where: _where,
      whereArgs: _whereArgs,
      orderBy: _orderBy,
      limit: _limit,
    );
  }
}

// Usage
final query = QueryBuilder()
    .table('users')
    .columns(['id', 'name', 'email'])
    .where('age > ?', [18])
    .orderBy('name ASC')
    .limit(10)
    .build();
```

### When to Use

Use builders for:
- Complex objects with many optional parameters
- Objects requiring validation before construction
- When you want fluent API style
- Configuration objects

Flutter examples:
- `ThemeData.builder()`
- `BoxDecoration` with many optional parameters
- Complex widget configurations

## Observer Pattern

The observer pattern defines a one-to-many relationship where observers are notified when the subject's state changes. Flutter's state management is built on this pattern.

### Purpose

Observers provide:
- Automatic notification of state changes
- Decoupling between state and UI
- Multiple observers for single subject
- Reactive programming model

### Implementation with ChangeNotifier

```dart
class CartViewModel extends ChangeNotifier {
  final List<CartItem> _items = [];

  List<CartItem> get items => List.unmodifiable(_items);

  int get itemCount => _items.length;

  double get total => _items.fold(
        0.0,
        (sum, item) => sum + (item.price * item.quantity),
      );

  void addItem(Product product) {
    final existingIndex = _items.indexWhere(
      (item) => item.productId == product.id,
    );

    if (existingIndex != -1) {
      _items[existingIndex] = _items[existingIndex].copyWith(
        quantity: _items[existingIndex].quantity + 1,
      );
    } else {
      _items.add(CartItem(
        productId: product.id,
        name: product.name,
        price: product.price,
        quantity: 1,
      ));
    }

    notifyListeners(); // Notify all observers
  }

  void removeItem(String productId) {
    _items.removeWhere((item) => item.productId == productId);
    notifyListeners();
  }

  void updateQuantity(String productId, int quantity) {
    final index = _items.indexWhere((item) => item.productId == productId);
    if (index != -1) {
      if (quantity <= 0) {
        _items.removeAt(index);
      } else {
        _items[index] = _items[index].copyWith(quantity: quantity);
      }
      notifyListeners();
    }
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
```

### Implementation with Streams

```dart
class SearchViewModel {
  final _searchQueryController = StreamController<String>();
  final _searchResultsController = StreamController<List<Product>>();

  Stream<List<Product>> get searchResults => _searchResultsController.stream;

  SearchViewModel(this._productRepository) {
    _searchQueryController.stream
        .debounceTime(const Duration(milliseconds: 300))
        .distinct()
        .switchMap((query) => _performSearch(query))
        .listen(
          (results) => _searchResultsController.add(results),
          onError: (error) => _searchResultsController.addError(error),
        );
  }

  void search(String query) {
    _searchQueryController.add(query);
  }

  Stream<List<Product>> _performSearch(String query) async* {
    if (query.isEmpty) {
      yield [];
      return;
    }

    try {
      final results = await _productRepository.searchProducts(query);
      yield results;
    } catch (e) {
      yield [];
    }
  }

  void dispose() {
    _searchQueryController.close();
    _searchResultsController.close();
  }
}
```

### When to Use

Use observer pattern for:
- State management in ViewModels
- Reactive data streams
- Event notification systems
- UI updates based on model changes

## Strategy Pattern

The strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. The strategy can be selected at runtime.

### Purpose

Strategies provide:
- Runtime algorithm selection
- Encapsulation of algorithm variations
- Easy addition of new strategies
- Elimination of conditional statements

### Implementation

```dart
abstract class PaymentStrategy {
  Future<PaymentResult> processPayment(double amount);
  String get name;
  bool get requiresAuth;
}

class CreditCardPaymentStrategy implements PaymentStrategy {
  final String cardNumber;
  final String cvv;
  final String expiryDate;

  CreditCardPaymentStrategy({
    required this.cardNumber,
    required this.cvv,
    required this.expiryDate,
  });

  @override
  String get name => 'Credit Card';

  @override
  bool get requiresAuth => true;

  @override
  Future<PaymentResult> processPayment(double amount) async {
    // Process credit card payment
    // Validate card details
    // Call payment gateway
    return PaymentResult.success();
  }
}

class PayPalPaymentStrategy implements PaymentStrategy {
  final String email;

  PayPalPaymentStrategy({required this.email});

  @override
  String get name => 'PayPal';

  @override
  bool get requiresAuth => true;

  @override
  Future<PaymentResult> processPayment(double amount) async {
    // Process PayPal payment
    return PaymentResult.success();
  }
}

class CashPaymentStrategy implements PaymentStrategy {
  @override
  String get name => 'Cash';

  @override
  bool get requiresAuth => false;

  @override
  Future<PaymentResult> processPayment(double amount) async {
    // Handle cash payment
    return PaymentResult.success();
  }
}

// Context that uses strategies
class CheckoutService {
  Future<Order> processOrder(
    Order order,
    PaymentStrategy paymentStrategy,
  ) async {
    // Validate order
    if (order.total <= 0) {
      throw BusinessException('Invalid order total');
    }

    // Process payment using selected strategy
    final paymentResult = await paymentStrategy.processPayment(order.total);

    if (!paymentResult.isSuccess) {
      throw PaymentException('Payment failed: ${paymentResult.errorMessage}');
    }

    // Update order status
    return order.copyWith(
      status: OrderStatus.paid,
      paymentMethod: paymentStrategy.name,
      paymentId: paymentResult.transactionId,
    );
  }
}

// Usage
final checkoutService = CheckoutService();

final order = await checkoutService.processOrder(
  currentOrder,
  CreditCardPaymentStrategy(
    cardNumber: '1234567890123456',
    cvv: '123',
    expiryDate: '12/25',
  ),
);
```

### When to Use

Use strategy pattern for:
- Multiple algorithms for the same task
- Runtime algorithm selection
- Eliminating conditional logic for algorithm selection
- Making new algorithms easy to add

Common Flutter use cases:
- Payment processing methods
- Sorting algorithms
- Data validation strategies
- Export formats (PDF, Excel, CSV)

## Adapter Pattern

The adapter pattern converts an interface into another interface that clients expect. It allows classes with incompatible interfaces to work together.

### Purpose

Adapters provide:
- Interface compatibility
- Integration with third-party code
- Reuse of existing classes with different interfaces
- Platform-specific implementations

### Implementation

```dart
// Target interface your app expects
abstract class CloudStorageService {
  Future<String> uploadFile(File file);
  Future<File> downloadFile(String fileId);
  Future<void> deleteFile(String fileId);
}

// Third-party AWS S3 client (adaptee)
class S3Client {
  Future<S3UploadResult> putObject(String bucket, String key, Uint8List data) async {
    // AWS S3 specific upload
  }

  Future<Uint8List> getObject(String bucket, String key) async {
    // AWS S3 specific download
  }

  Future<void> removeObject(String bucket, String key) async {
    // AWS S3 specific delete
  }
}

// Adapter that makes S3Client compatible with CloudStorageService
class S3StorageAdapter implements CloudStorageService {
  final S3Client _s3Client;
  final String _bucket;

  S3StorageAdapter(this._s3Client, this._bucket);

  @override
  Future<String> uploadFile(File file) async {
    final bytes = await file.readAsBytes();
    final fileName = path.basename(file.path);

    final result = await _s3Client.putObject(_bucket, fileName, bytes);

    return result.key; // Return file ID
  }

  @override
  Future<File> downloadFile(String fileId) async {
    final bytes = await _s3Client.getObject(_bucket, fileId);

    final tempDir = await getTemporaryDirectory();
    final file = File('${tempDir.path}/$fileId');

    await file.writeAsBytes(bytes);
    return file;
  }

  @override
  Future<void> deleteFile(String fileId) async {
    await _s3Client.removeObject(_bucket, fileId);
  }
}

// Another adapter for Firebase Storage
class FirebaseStorageAdapter implements CloudStorageService {
  final FirebaseStorage _storage;

  FirebaseStorageAdapter(this._storage);

  @override
  Future<String> uploadFile(File file) async {
    final fileName = path.basename(file.path);
    final ref = _storage.ref().child(fileName);
    final uploadTask = ref.putFile(file);
    final snapshot = await uploadTask;
    return snapshot.ref.fullPath;
  }

  // ... implement other methods
}
```

### When to Use

Use adapter pattern for:
- Integrating third-party libraries with incompatible interfaces
- Platform-specific implementations (iOS vs Android)
- Legacy code integration
- Making existing classes work with new interfaces

## Decorator Pattern

The decorator pattern attaches additional responsibilities to objects dynamically. Decorators provide a flexible alternative to subclassing.

### Purpose

Decorators provide:
- Dynamic behavior addition
- Flexible alternative to subclassing
- Multiple decorators can be stacked
- Single Responsibility Principle adherence

### Implementation

```dart
abstract class DataSource {
  Future<String> readData();
  Future<void> writeData(String data);
}

class FileDataSource implements DataSource {
  final String filePath;

  FileDataSource(this.filePath);

  @override
  Future<String> readData() async {
    final file = File(filePath);
    return await file.readAsString();
  }

  @override
  Future<void> writeData(String data) async {
    final file = File(filePath);
    await file.writeAsString(data);
  }
}

// Base decorator
abstract class DataSourceDecorator implements DataSource {
  final DataSource _wrappee;

  DataSourceDecorator(this._wrappee);

  @override
  Future<String> readData() => _wrappee.readData();

  @override
  Future<void> writeData(String data) => _wrappee.writeData(data);
}

// Encryption decorator
class EncryptionDecorator extends DataSourceDecorator {
  EncryptionDecorator(super.wrappee);

  @override
  Future<String> readData() async {
    final data = await super.readData();
    return _decrypt(data);
  }

  @override
  Future<void> writeData(String data) async {
    final encrypted = _encrypt(data);
    await super.writeData(encrypted);
  }

  String _encrypt(String data) {
    // Encryption logic
    return base64Encode(utf8.encode(data));
  }

  String _decrypt(String data) {
    // Decryption logic
    return utf8.decode(base64Decode(data));
  }
}

// Compression decorator
class CompressionDecorator extends DataSourceDecorator {
  CompressionDecorator(super.wrappee);

  @override
  Future<String> readData() async {
    final data = await super.readData();
    return _decompress(data);
  }

  @override
  Future<void> writeData(String data) async {
    final compressed = _compress(data);
    await super.writeData(compressed);
  }

  String _compress(String data) {
    final bytes = utf8.encode(data);
    final compressed = gzip.encode(bytes);
    return base64Encode(compressed);
  }

  String _decompress(String data) {
    final bytes = base64Decode(data);
    final decompressed = gzip.decode(bytes);
    return utf8.decode(decompressed);
  }
}

// Usage: Stack decorators
final dataSource = CompressionDecorator(
  EncryptionDecorator(
    FileDataSource('data.txt'),
  ),
);

// Writes compressed and encrypted data
await dataSource.writeData('Hello World');

// Reads, decrypts, and decompresses
final data = await dataSource.readData();
```

### When to Use

Use decorator pattern for:
- Adding behavior without modifying existing code
- Combining multiple behaviors flexibly
- Adding features that can be applied in any combination
- Avoiding class explosion from subclassing

## Facade Pattern

The facade pattern provides a simplified interface to a complex subsystem. It makes subsystems easier to use by providing a higher-level interface.

### Purpose

Facades provide:
- Simplified interface to complex systems
- Reduced coupling between clients and subsystems
- Layered architecture support
- Easier testing through abstraction

### Implementation

```dart
// Complex subsystems
class AuthenticationService {
  Future<String> authenticate(String email, String password) async { }
}

class UserProfileService {
  Future<UserProfile> fetchProfile(String userId) async { }
}

class PreferencesService {
  Future<UserPreferences> fetchPreferences(String userId) async { }
}

class AnalyticsService {
  void trackLogin(String userId) { }
}

class NotificationService {
  Future<void> registerDevice(String userId, String deviceId) async { }
}

// Facade providing simplified login interface
class LoginFacade {
  final AuthenticationService _authService;
  final UserProfileService _profileService;
  final PreferencesService _preferencesService;
  final AnalyticsService _analyticsService;
  final NotificationService _notificationService;

  LoginFacade(
    this._authService,
    this._profileService,
    this._preferencesService,
    this._analyticsService,
    this._notificationService,
  );

  Future<LoginResult> login(String email, String password) async {
    try {
      // Step 1: Authenticate
      final userId = await _authService.authenticate(email, password);

      // Step 2: Fetch profile
      final profile = await _profileService.fetchProfile(userId);

      // Step 3: Fetch preferences
      final preferences = await _preferencesService.fetchPreferences(userId);

      // Step 4: Track analytics
      _analyticsService.trackLogin(userId);

      // Step 5: Register for notifications
      final deviceId = await _getDeviceId();
      await _notificationService.registerDevice(userId, deviceId);

      return LoginResult.success(
        userId: userId,
        profile: profile,
        preferences: preferences,
      );
    } catch (e) {
      return LoginResult.failure(e.toString());
    }
  }

  Future<String> _getDeviceId() async {
    // Get device ID
    return 'device-id';
  }
}

// Simple client code
final loginFacade = getIt<LoginFacade>();
final result = await loginFacade.login(email, password);
```

### When to Use

Use facade pattern for:
- Simplifying complex subsystems
- Providing clear entry points to features
- Reducing dependencies on subsystem details
- Creating higher-level APIs

## Design Patterns in Practice

Design patterns are tools, not rules. Use them when they solve real problems, not because they're "best practices."

**Signs you need a pattern**:
- Code is difficult to test
- Adding features requires changing many files
- Similar code appears in multiple places
- Dependencies are tightly coupled

**Signs you're overusing patterns**:
- Code is more complex than the problem
- Patterns are nested multiple levels deep
- You're implementing patterns "just in case"
- New developers struggle to understand the code

Start simple. Add patterns when complexity justifies them. The best code is often the simplest code that solves the problem effectively.
