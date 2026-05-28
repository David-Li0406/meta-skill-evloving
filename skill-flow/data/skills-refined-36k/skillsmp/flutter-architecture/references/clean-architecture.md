# Clean Architecture in Flutter

Clean Architecture is a software design philosophy that emphasizes separation of concerns through well-defined layers with explicit dependencies. Created by Robert C. Martin (Uncle Bob), Clean Architecture provides a systematic approach to building maintainable, testable, and scalable applications.

## Why Clean Architecture

As Flutter applications grow, they face common challenges:

- **Tight coupling**: Changes in one area break unrelated features
- **Difficult testing**: Business logic mixed with UI and data access requires complex integration tests
- **Unclear boundaries**: Developers don't know where to put new code
- **Framework dependency**: Business logic depends on Flutter, making it hard to migrate or reuse
- **Poor scalability**: Adding features becomes progressively harder

Clean Architecture addresses these challenges by establishing clear layers with well-defined responsibilities and dependencies. Each layer focuses on a specific concern, making the system easier to understand, test, and modify.

## The Three Layers

Clean Architecture in Flutter consists of three primary layers: Presentation, Domain, and Data. Each layer has a specific responsibility and can only depend on layers closer to the center.

### Presentation Layer

The Presentation layer is the outermost layer, responsible for presenting information to users and capturing user interactions. This layer includes all UI components and presentation logic.

**Components**:

- **Views**: Widgets that compose the user interface (StatelessWidget, StatefulWidget)
- **Presentation Logic Holders**: ViewModels, BLoCs, Controllers that manage UI state
- **UI Models**: Data classes specifically formatted for display
- **Widgets**: Reusable UI components

**Responsibilities**:

- Rendering the user interface
- Handling user input and gestures
- Managing UI state (loading, error, success)
- Formatting data for display
- Navigation between screens
- Displaying error messages and loading indicators

**Dependencies**: The Presentation layer depends on the Domain layer to access use cases and entities. It never directly accesses the Data layer.

**Framework-Specific**: This layer contains Flutter-specific code. It's the only layer that should import Flutter UI packages.

### Domain Layer

The Domain layer is the heart of the application, containing core business logic. This layer is completely independent of frameworks, UI, and data sources. It represents the essential functionality that would remain constant even if you changed frameworks or databases.

**Components**:

- **Entities**: Core business objects that represent the essential concepts of your domain
- **Use Cases**: Individual business operations that orchestrate the flow of data
- **Repository Interfaces**: Abstract definitions of data access (implemented in Data layer)
- **Business Logic**: Rules and validations that define how the application works

**Responsibilities**:

- Defining business entities and their behaviors
- Implementing business rules and validations
- Orchestrating data flow between layers
- Defining contracts for data access through repository interfaces
- Containing domain-specific exceptions and errors

**Dependencies**: The Domain layer has no dependencies on other layers. It's pure Dart code without any Flutter or third-party framework dependencies.

**Platform-Independent**: The Domain layer should be executable on any Dart platform (Flutter, server-side Dart, command-line tools). This independence makes business logic highly portable and reusable.

### Data Layer

The Data layer is responsible for retrieving data from various sources and making it available to the Domain layer. This layer implements the repository interfaces defined in the Domain layer.

**Components**:

- **Repository Implementations**: Concrete classes that implement Domain repository interfaces
- **Data Sources**: Classes that interact with specific data sources (API, database, cache)
- **DTOs (Data Transfer Objects)**: Data models for serialization and deserialization
- **Mappers**: Functions that convert between DTOs and Domain entities

**Responsibilities**:

- Fetching data from remote APIs
- Reading and writing to local databases
- Caching data for offline use
- Handling network errors and retries
- Transforming raw data into domain entities
- Managing data synchronization

**Dependencies**: The Data layer depends on the Domain layer for entity definitions and repository interfaces. It never depends on the Presentation layer.

**Implementation Details**: All the "messy" details live here - JSON serialization, SQL queries, HTTP requests, caching strategies. These details are hidden from other layers.

## The Dependency Rule

The fundamental rule of Clean Architecture is the Dependency Rule: source code dependencies must point inward toward higher-level policies.

**Inward Dependencies**:
- Presentation → Domain
- Data → Domain
- Domain → Nothing

The Domain layer sits at the center and has no dependencies. Both the Presentation and Data layers depend on Domain, but they don't depend on each other.

### Dependency Inversion

The Data layer depends on Domain even though Domain sits at a "higher" level. This is achieved through dependency inversion - the Domain layer defines abstract repository interfaces, and the Data layer provides concrete implementations.

```dart
// Domain layer defines the interface
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> saveUser(User user);
}

// Data layer implements the interface
class UserRepositoryImpl implements UserRepository {
  final UserApiService _apiService;
  final UserDatabaseService _databaseService;

  UserRepositoryImpl(this._apiService, this._databaseService);

  @override
  Future<User> getUser(String id) async {
    // Implementation details...
  }

  @override
  Future<void> saveUser(User user) async {
    // Implementation details...
  }
}
```

The Domain layer declares what it needs (the interface), and the Data layer provides it (the implementation). The Presentation layer doesn't care about these details - it just uses the interface through dependency injection.

## Communication Flow

Data and events flow through Clean Architecture in predictable patterns.

### Data Flow (Outward)

Data flows from the Data layer through the Domain layer to the Presentation layer:

1. **Data Layer** fetches raw data from sources (API response, database query)
2. **Data Layer** transforms raw data into Domain entities
3. **Domain Layer** receives entities, applies business logic if needed
4. **Presentation Layer** receives entities through use cases
5. **Presentation Layer** formats entities into UI-specific models
6. **View** displays the formatted data

### Event Flow (Inward)

User interactions flow from the Presentation layer through Domain to the Data layer:

1. **View** captures user interaction (button tap, text input)
2. **Presentation Logic Holder** receives the event
3. **Use Case** is called with appropriate parameters
4. **Use Case** applies business logic, validates input
5. **Repository** is called to persist or fetch data
6. **Data Source** performs the actual operation

This bidirectional flow keeps concerns separated - the Presentation layer handles user interaction, the Domain layer applies business rules, and the Data layer manages data persistence.

## Entities

Entities are core business objects that represent the essential concepts in your application's domain. They contain business logic that's relevant across the entire application.

### Entity Design

Entities should:
- Be immutable (use `final` fields)
- Contain business logic relevant to the entity
- Have no dependencies on frameworks or UI
- Use value equality (consider using Equatable package)

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final UserRole role;
  final DateTime createdAt;

  const User({
    required this.id,
    required this.email,
    required this.name,
    required this.role,
    required this.createdAt,
  });

  // Business logic methods
  bool get isAdmin => role == UserRole.admin;

  bool canAccessFeature(String featureId) {
    return role.permissions.contains(featureId);
  }

  // Validation logic
  bool get isValidEmail {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }

  // Create modified copies (immutability)
  User copyWith({
    String? id,
    String? email,
    String? name,
    UserRole? role,
    DateTime? createdAt,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      role: role ?? this.role,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  List<Object?> get props => [id, email, name, role, createdAt];
}

enum UserRole {
  user,
  moderator,
  admin;

  Set<String> get permissions {
    switch (this) {
      case UserRole.admin:
        return {'*'}; // All permissions
      case UserRole.moderator:
        return {'moderate_content', 'view_reports'};
      case UserRole.user:
        return {'view_content', 'create_posts'};
    }
  }
}
```

### Entities vs DTOs

Entities are different from DTOs (Data Transfer Objects):

- **Entities** contain business logic and represent domain concepts
- **DTOs** are simple data containers for serialization/deserialization

DTOs live in the Data layer and are converted to entities before leaving that layer.

## Use Cases

Use Cases represent individual business operations. Each use case performs a specific action in your application, like "Login User", "Create Order", or "Update Profile".

### Use Case Design

Use cases should:
- Have a single, well-defined purpose (Single Responsibility Principle)
- Be reusable across different parts of the application
- Coordinate between repositories to fulfill business requirements
- Contain business logic that's specific to the operation
- Return entities, not DTOs or UI models

```dart
class GetUserProfileUseCase {
  final UserRepository _userRepository;
  final ImageRepository _imageRepository;
  final AnalyticsRepository _analyticsRepository;

  GetUserProfileUseCase(
    this._userRepository,
    this._imageRepository,
    this._analyticsRepository,
  );

  Future<UserProfile> execute(String userId) async {
    // Fetch user data
    final user = await _userRepository.getUser(userId);

    // Fetch profile image if user has one
    Image? profileImage;
    if (user.profileImageId != null) {
      profileImage = await _imageRepository.getImage(user.profileImageId!);
    }

    // Track analytics
    await _analyticsRepository.trackProfileView(userId);

    // Combine data into domain model
    return UserProfile(
      user: user,
      profileImage: profileImage,
    );
  }
}
```

### Use Case Naming

Use clear, action-oriented names that describe what the use case does:
- `LoginUserUseCase`
- `CreateOrderUseCase`
- `UpdateUserProfileUseCase`
- `DeleteCommentUseCase`
- `SearchProductsUseCase`

### Use Case Parameters

For use cases that require multiple parameters, create a parameter object:

```dart
class UpdateUserProfileParams {
  final String userId;
  final String? name;
  final String? bio;
  final File? profileImage;

  UpdateUserProfileParams({
    required this.userId,
    this.name,
    this.bio,
    this.profileImage,
  });
}

class UpdateUserProfileUseCase {
  final UserRepository _userRepository;
  final ImageRepository _imageRepository;

  UpdateUserProfileUseCase(this._userRepository, this._imageRepository);

  Future<User> execute(UpdateUserProfileParams params) async {
    // Upload new profile image if provided
    String? imageId;
    if (params.profileImage != null) {
      imageId = await _imageRepository.uploadImage(params.profileImage!);
    }

    // Update user profile
    return await _userRepository.updateUser(
      userId: params.userId,
      name: params.name,
      bio: params.bio,
      profileImageId: imageId,
    );
  }
}
```

## Repository Pattern

Repositories provide an abstraction over data sources, allowing the Domain layer to access data without knowing about implementation details.

### Repository Interface (Domain Layer)

Define repository interfaces in the Domain layer:

```dart
abstract class ProductRepository {
  Future<List<Product>> getProducts();
  Future<Product> getProduct(String id);
  Future<Product> createProduct(Product product);
  Future<Product> updateProduct(Product product);
  Future<void> deleteProduct(String id);
  Stream<List<Product>> watchProducts();
}
```

### Repository Implementation (Data Layer)

Implement repositories in the Data layer:

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
        // Fetch from API
        final productDtos = await _apiService.getProducts();
        final products = productDtos.map((dto) => dto.toEntity()).toList();

        // Cache in database
        await _databaseService.saveProducts(products);

        return products;
      } else {
        // Fetch from cache
        return await _databaseService.getProducts();
      }
    } catch (e) {
      // Fallback to cache on error
      return await _databaseService.getProducts();
    }
  }

  @override
  Future<Product> getProduct(String id) async {
    try {
      if (await _networkInfo.isConnected) {
        final productDto = await _apiService.getProduct(id);
        final product = productDto.toEntity();
        await _databaseService.saveProduct(product);
        return product;
      } else {
        return await _databaseService.getProduct(id);
      }
    } catch (e) {
      return await _databaseService.getProduct(id);
    }
  }

  @override
  Stream<List<Product>> watchProducts() {
    return _databaseService.watchProducts();
  }

  // ... other methods
}
```

### Repository Benefits

**Abstraction**: The Presentation and Domain layers don't know if data comes from an API, database, or in-memory cache.

**Testability**: Easy to mock repositories for testing use cases and ViewModels.

**Flexibility**: Change data sources without affecting business logic. Switch from REST to GraphQL, or from SQLite to Hive, by just changing the repository implementation.

**Caching Strategy**: Repositories can implement sophisticated caching without the rest of the app needing to know.

## Data Sources

Data sources handle the actual interaction with specific technologies (HTTP clients, databases, file systems). Each data source focuses on a single technology or data provider.

### API Data Source

```dart
class UserApiService {
  final Dio _dio;

  UserApiService(this._dio);

  Future<UserDto> getUser(String id) async {
    try {
      final response = await _dio.get('/users/$id');
      return UserDto.fromJson(response.data);
    } on DioError catch (e) {
      throw _handleError(e);
    }
  }

  Future<UserDto> createUser(CreateUserDto dto) async {
    try {
      final response = await _dio.post(
        '/users',
        data: dto.toJson(),
      );
      return UserDto.fromJson(response.data);
    } on DioError catch (e) {
      throw _handleError(e);
    }
  }

  Exception _handleError(DioError error) {
    if (error.type == DioErrorType.connectionTimeout) {
      return NetworkException('Connection timeout');
    } else if (error.response?.statusCode == 404) {
      return NotFoundException('User not found');
    } else {
      return ServerException('Server error: ${error.message}');
    }
  }
}
```

### Database Data Source

```dart
class UserDatabaseService {
  final Database _database;

  UserDatabaseService(this._database);

  Future<User> getUser(String id) async {
    final maps = await _database.query(
      'users',
      where: 'id = ?',
      whereArgs: [id],
    );

    if (maps.isEmpty) {
      throw CacheException('User not found in cache');
    }

    return User.fromMap(maps.first);
  }

  Future<void> saveUser(User user) async {
    await _database.insert(
      'users',
      user.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<User>> getUsers() async {
    final maps = await _database.query('users');
    return maps.map((map) => User.fromMap(map)).toList();
  }

  Stream<List<User>> watchUsers() {
    // Implementation depends on database package
    // Some packages provide stream support directly
  }
}
```

## DTOs and Mappers

DTOs (Data Transfer Objects) are simple data classes used for serialization and deserialization. They live in the Data layer and are converted to domain entities before leaving that layer.

### DTO Design

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user_dto.g.dart';

@JsonSerializable()
class UserDto {
  final String id;
  final String email;
  @JsonKey(name: 'full_name')
  final String fullName;
  @JsonKey(name: 'role_id')
  final int roleId;
  @JsonKey(name: 'created_at')
  final String createdAt;

  UserDto({
    required this.id,
    required this.email,
    required this.fullName,
    required this.roleId,
    required this.createdAt,
  });

  factory UserDto.fromJson(Map<String, dynamic> json) =>
      _$UserDtoFromJson(json);

  Map<String, dynamic> toJson() => _$UserDtoToJson(this);

  // Convert DTO to Domain Entity
  User toEntity() {
    return User(
      id: id,
      email: email,
      name: fullName,
      role: _roleFromId(roleId),
      createdAt: DateTime.parse(createdAt),
    );
  }

  UserRole _roleFromId(int id) {
    switch (id) {
      case 1:
        return UserRole.user;
      case 2:
        return UserRole.moderator;
      case 3:
        return UserRole.admin;
      default:
        return UserRole.user;
    }
  }
}
```

### Mapper Functions

For complex transformations, create dedicated mapper functions:

```dart
class ProductMapper {
  static Product toEntity(ProductDto dto) {
    return Product(
      id: dto.id,
      name: dto.name,
      description: dto.description,
      price: dto.priceInCents / 100, // Convert cents to dollars
      imageUrl: dto.imageUrl,
      category: CategoryMapper.toEntity(dto.category),
      inStock: dto.stockQuantity > 0,
      rating: dto.averageRating.toDouble(),
    );
  }

  static ProductDto fromEntity(Product entity) {
    return ProductDto(
      id: entity.id,
      name: entity.name,
      description: entity.description,
      priceInCents: (entity.price * 100).round(),
      imageUrl: entity.imageUrl,
      category: CategoryMapper.fromEntity(entity.category),
      stockQuantity: entity.inStock ? 1 : 0,
      averageRating: entity.rating,
    );
  }
}
```

## Error Handling

Clean Architecture requires thoughtful error handling across layers. Each layer should handle errors appropriately and convert them to forms suitable for the next layer.

### Domain Layer Exceptions

Define domain-specific exceptions in the Domain layer:

```dart
abstract class DomainException implements Exception {
  final String message;
  DomainException(this.message);

  @override
  String toString() => message;
}

class ValidationException extends DomainException {
  ValidationException(super.message);
}

class UnauthorizedException extends DomainException {
  UnauthorizedException([String message = 'Unauthorized'])
      : super(message);
}

class NotFoundException extends DomainException {
  NotFoundException(super.message);
}
```

### Data Layer Exceptions

Define data-specific exceptions in the Data layer:

```dart
abstract class DataException implements Exception {
  final String message;
  DataException(this.message);
}

class NetworkException extends DataException {
  NetworkException(super.message);
}

class ServerException extends DataException {
  ServerException(super.message);
}

class CacheException extends DataException {
  CacheException(super.message);
}
```

### Error Conversion

Repositories convert Data layer exceptions to Domain layer exceptions:

```dart
class UserRepositoryImpl implements UserRepository {
  @override
  Future<User> getUser(String id) async {
    try {
      final userDto = await _apiService.getUser(id);
      return userDto.toEntity();
    } on NetworkException {
      throw DomainException('Network error. Please check your connection.');
    } on ServerException {
      throw DomainException('Server error. Please try again later.');
    } on NotFoundException {
      throw NotFoundException('User not found');
    } catch (e) {
      throw DomainException('An unexpected error occurred');
    }
  }
}
```

### Presentation Layer Error Handling

ViewModels catch domain exceptions and convert them to user-friendly messages:

```dart
class UserProfileViewModel extends ChangeNotifier {
  String? _errorMessage;
  String? get errorMessage => _errorMessage;

  Future<void> loadUserProfile(String userId) async {
    try {
      final profile = await _getUserProfileUseCase.execute(userId);
      _userProfile = profile;
      _errorMessage = null;
    } on UnauthorizedException {
      _errorMessage = 'You are not authorized to view this profile';
    } on NotFoundException {
      _errorMessage = 'User profile not found';
    } on DomainException catch (e) {
      _errorMessage = e.message;
    } catch (e) {
      _errorMessage = 'An unexpected error occurred';
    }
    notifyListeners();
  }
}
```

## Layer Organization

Clean Architecture layers can be organized in your project structure in different ways.

### Package-Based Organization

Organize by layer with packages inside each layer:

```
lib/
├── core/
│   ├── errors/
│   ├── network/
│   └── utils/
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── blocs/
│   │       ├── pages/
│   │       └── widgets/
│   └── products/
│       ├── data/
│       ├── domain/
│       └── presentation/
```

### Feature-First Organization

Organize by feature with layers inside each feature:

```
lib/
├── features/
│   ├── authentication/
│   │   ├── domain/
│   │   ├── data/
│   │   └── presentation/
│   ├── products/
│   │   ├── domain/
│   │   ├── data/
│   │   └── presentation/
│   └── orders/
│       ├── domain/
│       ├── data/
│       └── presentation/
└── core/
    ├── network/
    ├── database/
    └── errors/
```

Both approaches work well. Feature-first scales better for large applications with many features, while package-based provides a clearer view of architectural layers.

## Testing in Clean Architecture

Clean Architecture makes testing straightforward because each layer can be tested independently with appropriate mocking.

### Domain Layer Testing

Test use cases with mocked repositories:

```dart
class MockUserRepository extends Mock implements UserRepository {}
class MockImageRepository extends Mock implements ImageRepository {}

void main() {
  late GetUserProfileUseCase useCase;
  late MockUserRepository mockUserRepository;
  late MockImageRepository mockImageRepository;

  setUp(() {
    mockUserRepository = MockUserRepository();
    mockImageRepository = MockImageRepository();
    useCase = GetUserProfileUseCase(
      mockUserRepository,
      mockImageRepository,
    );
  });

  test('should get user profile with image', () async {
    // Arrange
    final user = User(id: '1', email: 'test@example.com', ...);
    final image = Image(id: 'img1', url: 'https://...');

    when(() => mockUserRepository.getUser('1'))
        .thenAnswer((_) async => user);
    when(() => mockImageRepository.getImage(any()))
        .thenAnswer((_) async => image);

    // Act
    final result = await useCase.execute('1');

    // Assert
    expect(result.user, user);
    expect(result.profileImage, image);
    verify(() => mockUserRepository.getUser('1')).called(1);
    verify(() => mockImageRepository.getImage(any())).called(1);
  });
}
```

### Data Layer Testing

Test repositories with mocked data sources:

```dart
class MockProductApiService extends Mock implements ProductApiService {}
class MockProductDatabaseService extends Mock implements ProductDatabaseService {}
class MockNetworkInfo extends Mock implements NetworkInfo {}

void main() {
  late ProductRepositoryImpl repository;
  late MockProductApiService mockApiService;
  late MockProductDatabaseService mockDatabaseService;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockApiService = MockProductApiService();
    mockDatabaseService = MockProductDatabaseService();
    mockNetworkInfo = MockNetworkInfo();
    repository = ProductRepositoryImpl(
      mockApiService,
      mockDatabaseService,
      mockNetworkInfo,
    );
  });

  group('getProducts', () {
    test('should return products from API when online', () async {
      // Arrange
      when(() => mockNetworkInfo.isConnected)
          .thenAnswer((_) async => true);
      final dtos = [ProductDto(...)];
      when(() => mockApiService.getProducts())
          .thenAnswer((_) async => dtos);
      when(() => mockDatabaseService.saveProducts(any()))
          .thenAnswer((_) async => {});

      // Act
      final result = await repository.getProducts();

      // Assert
      verify(() => mockApiService.getProducts()).called(1);
      verify(() => mockDatabaseService.saveProducts(any())).called(1);
    });

    test('should return cached products when offline', () async {
      // Arrange
      when(() => mockNetworkInfo.isConnected)
          .thenAnswer((_) async => false);
      final products = [Product(...)];
      when(() => mockDatabaseService.getProducts())
          .thenAnswer((_) async => products);

      // Act
      final result = await repository.getProducts();

      // Assert
      expect(result, products);
      verifyNever(() => mockApiService.getProducts());
      verify(() => mockDatabaseService.getProducts()).called(1);
    });
  });
}
```

### Presentation Layer Testing

Test ViewModels with mocked use cases:

```dart
class MockGetUserProfileUseCase extends Mock implements GetUserProfileUseCase {}

void main() {
  late UserProfileViewModel viewModel;
  late MockGetUserProfileUseCase mockGetUserProfile;

  setUp(() {
    mockGetUserProfile = MockGetUserProfileUseCase();
    viewModel = UserProfileViewModel(mockGetUserProfile);
  });

  test('should load user profile successfully', () async {
    // Arrange
    final profile = UserProfile(...);
    when(() => mockGetUserProfile.execute(any()))
        .thenAnswer((_) async => profile);

    // Act
    await viewModel.loadUserProfile('1');

    // Assert
    expect(viewModel.userProfile, profile);
    expect(viewModel.errorMessage, null);
    verify(() => mockGetUserProfile.execute('1')).called(1);
  });
}
```

## Benefits of Clean Architecture

**Testability**: Each layer can be tested independently with appropriate mocks. Business logic can be unit tested without any UI or framework dependencies.

**Maintainability**: Clear separation of concerns makes it easy to find and modify code. Changes in one layer don't ripple through the entire application.

**Scalability**: Multiple developers can work on different layers or features simultaneously with minimal conflicts.

**Flexibility**: Easy to swap implementations (change from REST to GraphQL, SQLite to Hive) without affecting business logic.

**Portability**: Domain layer is pure Dart and can be reused in different contexts (mobile app, web app, command-line tool).

**Framework Independence**: Business logic doesn't depend on Flutter or any framework, making it easier to migrate or share code.

## Common Challenges

**Initial Complexity**: Clean Architecture has more files and layers than simpler approaches. For very small apps, this might be overkill.

**Learning Curve**: Developers new to Clean Architecture need time to understand layer responsibilities and dependencies.

**Over-Engineering**: Not every feature needs the full treatment. Use judgment to determine appropriate complexity for each feature.

**Boilerplate**: More layers mean more interfaces and implementations. Code generation tools can help reduce boilerplate.

## When to Use Clean Architecture

Clean Architecture is valuable for:

- Medium to large applications with multiple features
- Applications expected to grow significantly
- Projects with multiple developers
- Applications requiring high test coverage
- Projects with complex business logic
- Applications with long-term maintenance requirements

For small apps or prototypes, simpler approaches might be more appropriate. The investment in Clean Architecture pays off as the application grows.

## Clean Architecture in Practice

Clean Architecture is not about strict rules but about principles that guide design decisions. Adapt the architecture to your specific needs while maintaining the core principles:

- Separation of concerns through layers
- Dependencies pointing inward
- Business logic independence from frameworks
- Clear interfaces between layers

Start with the Domain layer - define your entities and use cases. Then build the Data layer to provide data access. Finally, create the Presentation layer to display data and handle user interaction.

As you gain experience, you'll develop intuition for how to structure features and where to draw boundaries between layers. The result is a codebase that's easier to understand, test, and evolve over time.
