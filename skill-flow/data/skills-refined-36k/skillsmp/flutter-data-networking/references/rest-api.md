# REST API Integration

Complete guide to integrating REST APIs in Flutter applications with best practices for CRUD operations, authentication, and error handling.

## Overview

REST (Representational State Transfer) is the most common API architecture for Flutter applications. RESTful APIs expose resources through HTTP endpoints and use standard HTTP methods (GET, POST, PUT, PATCH, DELETE) to perform operations on those resources.

This reference covers everything needed to build production-ready REST API integrations, including proper resource modeling, authentication patterns, error handling, and testing strategies.

## REST Principles

### Resource-Based URLs

REST APIs organize around resources, represented by nouns in URLs:

```
Good:
  GET    /users           # List users
  GET    /users/123       # Get specific user
  POST   /users           # Create user
  PUT    /users/123       # Update user
  DELETE /users/123       # Delete user

Bad:
  GET  /getUsers
  POST /createUser
  POST /deleteUser/123
```

### HTTP Methods

Use standard HTTP methods for their intended purposes:

- **GET**: Retrieve resources (safe and idempotent)
- **POST**: Create new resources (not idempotent)
- **PUT**: Replace entire resource (idempotent)
- **PATCH**: Partially update resource (idempotent)
- **DELETE**: Remove resource (idempotent)

Idempotent operations produce the same result when called multiple times, making them safe to retry.

### Status Codes

REST APIs use HTTP status codes to indicate request outcomes:

**Success:**
- 200 OK: Request succeeded
- 201 Created: Resource created successfully
- 204 No Content: Success with no response body

**Client Errors:**
- 400 Bad Request: Invalid request data
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Validation errors

**Server Errors:**
- 500 Internal Server Error: Server malfunction
- 502 Bad Gateway: Upstream server error
- 503 Service Unavailable: Temporary outage

## Repository Pattern

Isolate API logic in repository classes that abstract data sources from application code:

```dart
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<List<User>> getUsers({int page, int perPage});
  Future<User> createUser(CreateUserDto dto);
  Future<User> updateUser(String id, UpdateUserDto dto);
  Future<void> deleteUser(String id);
}

class ApiUserRepository implements UserRepository {
  final Dio _dio;

  ApiUserRepository(this._dio);

  @override
  Future<User> getUser(String id) async {
    try {
      final response = await _dio.get('/users/$id');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  @override
  Future<List<User>> getUsers({
    int page = 1,
    int perPage = 20,
  }) async {
    try {
      final response = await _dio.get(
        '/users',
        queryParameters: {
          'page': page,
          'per_page': perPage,
        },
      );

      return (response.data['data'] as List)
          .map((json) => User.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  @override
  Future<User> createUser(CreateUserDto dto) async {
    try {
      final response = await _dio.post(
        '/users',
        data: dto.toJson(),
      );
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  @override
  Future<User> updateUser(String id, UpdateUserDto dto) async {
    try {
      final response = await _dio.patch(
        '/users/$id',
        data: dto.toJson(),
      );
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      await _dio.delete('/users/$id');
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Exception _mapException(DioException e) {
    // Map DioException to domain exceptions
    // Implementation in Error Handling section
  }
}
```

Benefits of the repository pattern:

- **Testability**: Mock repositories in tests instead of mocking HTTP calls
- **Flexibility**: Swap implementations (API, local database, mock) without changing application code
- **Separation of Concerns**: Business logic doesn't know about HTTP details
- **Single Source of Truth**: One place for all data access logic

## CRUD Operations

### Create (POST)

Create new resources with POST requests:

```dart
// DTO (Data Transfer Object) for creating users
class CreateUserDto {
  final String name;
  final String email;
  final String password;

  CreateUserDto({
    required this.name,
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() => {
    'name': name,
    'email': email,
    'password': password,
  };
}

// Repository method
Future<User> createUser(CreateUserDto dto) async {
  try {
    final response = await _dio.post(
      '/users',
      data: dto.toJson(),
    );

    // Most APIs return the created resource
    return User.fromJson(response.data);
  } on DioException catch (e) {
    if (e.response?.statusCode == 422) {
      // Validation errors
      throw ValidationException(
        e.response?.data['errors'] ?? {},
      );
    }
    throw _mapException(e);
  }
}

// Usage
try {
  final user = await userRepository.createUser(
    CreateUserDto(
      name: 'John Doe',
      email: 'john@example.com',
      password: 'secret123',
    ),
  );
  print('User created: ${user.id}');
} on ValidationException catch (e) {
  print('Validation errors: ${e.errors}');
} catch (e) {
  print('Failed to create user: $e');
}
```

### Read (GET)

Retrieve resources with GET requests:

```dart
// Get single resource
Future<User> getUser(String id) async {
  try {
    final response = await _dio.get('/users/$id');
    return User.fromJson(response.data);
  } on DioException catch (e) {
    if (e.response?.statusCode == 404) {
      throw NotFoundException('User not found');
    }
    throw _mapException(e);
  }
}

// Get collection with pagination
class PaginatedResponse<T> {
  final List<T> data;
  final int page;
  final int perPage;
  final int total;
  final int totalPages;

  PaginatedResponse({
    required this.data,
    required this.page,
    required this.perPage,
    required this.total,
    required this.totalPages,
  });
}

Future<PaginatedResponse<User>> getUsers({
  int page = 1,
  int perPage = 20,
  String? search,
  String? sortBy,
  String? sortOrder,
}) async {
  try {
    final response = await _dio.get(
      '/users',
      queryParameters: {
        'page': page,
        'per_page': perPage,
        if (search != null) 'search': search,
        if (sortBy != null) 'sort_by': sortBy,
        if (sortOrder != null) 'sort_order': sortOrder,
      },
    );

    final data = response.data;
    return PaginatedResponse(
      data: (data['data'] as List)
          .map((json) => User.fromJson(json))
          .toList(),
      page: data['page'],
      perPage: data['per_page'],
      total: data['total'],
      totalPages: data['total_pages'],
    );
  } on DioException catch (e) {
    throw _mapException(e);
  }
}

// Usage with infinite scroll
class UserListController {
  final UserRepository _repository;
  final List<User> _users = [];
  int _currentPage = 1;
  bool _hasMore = true;

  Future<void> loadMore() async {
    if (!_hasMore) return;

    final response = await _repository.getUsers(
      page: _currentPage,
      perPage: 20,
    );

    _users.addAll(response.data);
    _currentPage++;
    _hasMore = _currentPage <= response.totalPages;
  }
}
```

### Update (PUT/PATCH)

Modify resources with PUT or PATCH:

```dart
// PUT - Replace entire resource
class UpdateUserDto {
  final String name;
  final String email;
  final String? bio;
  final String? avatarUrl;

  UpdateUserDto({
    required this.name,
    required this.email,
    this.bio,
    this.avatarUrl,
  });

  Map<String, dynamic> toJson() => {
    'name': name,
    'email': email,
    'bio': bio,
    'avatar_url': avatarUrl,
  };
}

Future<User> updateUser(String id, UpdateUserDto dto) async {
  try {
    final response = await _dio.put(
      '/users/$id',
      data: dto.toJson(),
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    if (e.response?.statusCode == 404) {
      throw NotFoundException('User not found');
    }
    if (e.response?.statusCode == 422) {
      throw ValidationException(e.response?.data['errors']);
    }
    throw _mapException(e);
  }
}

// PATCH - Partial update (only changed fields)
Future<User> patchUser(
  String id,
  Map<String, dynamic> updates,
) async {
  try {
    final response = await _dio.patch(
      '/users/$id',
      data: updates,
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    if (e.response?.statusCode == 404) {
      throw NotFoundException('User not found');
    }
    if (e.response?.statusCode == 422) {
      throw ValidationException(e.response?.data['errors']);
    }
    throw _mapException(e);
  }
}

// Usage
// Full update
final user = await repository.updateUser(
  userId,
  UpdateUserDto(
    name: 'Jane Doe',
    email: 'jane@example.com',
    bio: 'Flutter developer',
  ),
);

// Partial update
final user = await repository.patchUser(
  userId,
  {'bio': 'Updated bio'},
);
```

### Delete (DELETE)

Remove resources with DELETE:

```dart
Future<void> deleteUser(String id) async {
  try {
    await _dio.delete('/users/$id');
  } on DioException catch (e) {
    if (e.response?.statusCode == 404) {
      throw NotFoundException('User not found');
    }
    if (e.response?.statusCode == 409) {
      throw ConflictException(
        'Cannot delete user: resource in use',
      );
    }
    throw _mapException(e);
  }
}

// Soft delete (if API supports it)
Future<User> softDeleteUser(String id) async {
  try {
    final response = await _dio.patch(
      '/users/$id',
      data: {'deleted_at': DateTime.now().toIso8601String()},
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _mapException(e);
  }
}

// Usage with confirmation
Future<void> deleteUserWithConfirmation(String id) async {
  final confirmed = await showConfirmationDialog(
    'Delete User',
    'Are you sure you want to delete this user?',
  );

  if (!confirmed) return;

  try {
    await repository.deleteUser(id);
    showSuccessMessage('User deleted successfully');
  } on ConflictException catch (e) {
    showErrorMessage(e.message);
  } catch (e) {
    showErrorMessage('Failed to delete user');
  }
}
```

## Authentication

### Bearer Token Authentication

Most modern APIs use JWT (JSON Web Token) authentication:

```dart
class AuthService {
  final Dio _dio;
  final SecureStorage _storage;

  AuthService(this._dio, this._storage);

  Future<AuthTokens> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      final tokens = AuthTokens.fromJson(response.data);
      await _storage.saveTokens(tokens);
      return tokens;
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw AuthException('Invalid credentials');
      }
      throw _mapException(e);
    }
  }

  Future<void> logout() async {
    try {
      await _dio.post('/auth/logout');
    } finally {
      await _storage.clearTokens();
    }
  }

  Future<AuthTokens> refreshToken() async {
    final refreshToken = await _storage.getRefreshToken();
    if (refreshToken == null) {
      throw AuthException('No refresh token available');
    }

    try {
      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final tokens = AuthTokens.fromJson(response.data);
      await _storage.saveTokens(tokens);
      return tokens;
    } on DioException catch (e) {
      await _storage.clearTokens();
      throw AuthException('Session expired');
    }
  }
}

// Secure token storage
class SecureStorage {
  final FlutterSecureStorage _storage;

  SecureStorage(this._storage);

  Future<void> saveTokens(AuthTokens tokens) async {
    await Future.wait([
      _storage.write(
        key: 'access_token',
        value: tokens.accessToken,
      ),
      _storage.write(
        key: 'refresh_token',
        value: tokens.refreshToken,
      ),
    ]);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'refresh_token');
  }

  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: 'access_token'),
      _storage.delete(key: 'refresh_token'),
    ]);
  }
}

// Auth interceptor (from http-client.md)
class AuthInterceptor extends QueuedInterceptor {
  final SecureStorage _storage;
  final AuthService _authService;

  AuthInterceptor(this._storage, this._authService);

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await _storage.getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      try {
        // Try to refresh token
        await _authService.refreshToken();

        // Retry original request with new token
        final token = await _storage.getAccessToken();
        err.requestOptions.headers['Authorization'] = 'Bearer $token';

        final response = await Dio().fetch(err.requestOptions);
        return handler.resolve(response);
      } catch (e) {
        // Refresh failed, redirect to login
        return handler.reject(err);
      }
    }

    handler.next(err);
  }
}
```

### API Key Authentication

Some APIs use static API keys:

```dart
class ApiKeyInterceptor extends Interceptor {
  final String apiKey;

  ApiKeyInterceptor(this.apiKey);

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) {
    // Add API key to header
    options.headers['X-API-Key'] = apiKey;

    // Or add to query parameters
    // options.queryParameters['api_key'] = apiKey;

    handler.next(options);
  }
}

// Setup
final dio = Dio();
dio.interceptors.add(ApiKeyInterceptor('your_api_key_here'));
```

### OAuth 2.0

For OAuth 2.0, use the `oauth2` package:

```dart
import 'package:oauth2/oauth2.dart' as oauth2;

class OAuthService {
  static const authorizationEndpoint =
      Uri.parse('https://example.com/oauth/authorize');
  static const tokenEndpoint =
      Uri.parse('https://example.com/oauth/token');
  static const clientId = 'your_client_id';
  static const clientSecret = 'your_client_secret';
  static const redirectUrl = 'myapp://oauth/callback';

  Future<oauth2.Client> authenticate() async {
    // Create authorization code grant
    final grant = oauth2.AuthorizationCodeGrant(
      clientId,
      authorizationEndpoint,
      tokenEndpoint,
      secret: clientSecret,
    );

    // Get authorization URL
    final authorizationUrl = grant.getAuthorizationUrl(
      Uri.parse(redirectUrl),
      scopes: ['read', 'write'],
    );

    // Open authorization URL in browser
    await launchUrl(authorizationUrl);

    // Listen for redirect
    final responseUrl = await listenForRedirect();

    // Handle authorization response
    final client = await grant.handleAuthorizationResponse(
      responseUrl.queryParameters,
    );

    return client;
  }
}
```

## Request/Response Models

Separate API models from domain models:

```dart
// API Response Model (matches API structure)
class UserApiModel {
  final String id;
  final String name;
  final String email;
  final String? avatarUrl;
  final String createdAt;
  final String updatedAt;

  UserApiModel({
    required this.id,
    required this.name,
    required this.email,
    this.avatarUrl,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UserApiModel.fromJson(Map<String, dynamic> json) {
    return UserApiModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      avatarUrl: json['avatar_url'],
      createdAt: json['created_at'],
      updatedAt: json['updated_at'],
    );
  }

  // Convert to domain model
  User toDomain() {
    return User(
      id: id,
      name: name,
      email: email,
      avatarUrl: avatarUrl,
      createdAt: DateTime.parse(createdAt),
      updatedAt: DateTime.parse(updatedAt),
    );
  }
}

// Domain Model (used in application)
class User {
  final String id;
  final String name;
  final String email;
  final String? avatarUrl;
  final DateTime createdAt;
  final DateTime updatedAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    this.avatarUrl,
    required this.createdAt,
    required this.updatedAt,
  });
}

// Repository converts between models
Future<User> getUser(String id) async {
  final response = await _dio.get('/users/$id');
  final apiModel = UserApiModel.fromJson(response.data);
  return apiModel.toDomain();
}
```

This separation allows you to:
- Change API structure without affecting application code
- Add computed properties to domain models
- Handle API quirks (snake_case, weird dates, etc.)
- Keep domain models clean and focused

## API Error Handling

Handle API-specific errors:

```dart
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic data;

  ApiException(this.message, {this.statusCode, this.data});

  @override
  String toString() => message;
}

class ValidationException extends ApiException {
  final Map<String, List<String>> errors;

  ValidationException(this.errors)
      : super('Validation failed', statusCode: 422);
}

Exception _mapException(DioException e) {
  if (e.response == null) {
    // Network error
    return NetworkException('Network error: ${e.message}');
  }

  final statusCode = e.response!.statusCode!;
  final data = e.response!.data;

  switch (statusCode) {
    case 400:
      return BadRequestException(
        data['message'] ?? 'Bad request',
      );

    case 401:
      return AuthException('Authentication required');

    case 403:
      return ForbiddenException('Access denied');

    case 404:
      return NotFoundException(
        data['message'] ?? 'Resource not found',
      );

    case 422:
      return ValidationException(
        Map<String, List<String>>.from(
          data['errors'] ?? {},
        ),
      );

    case 429:
      final retryAfter = e.response!.headers['retry-after']?[0];
      return RateLimitException(
        'Too many requests',
        retryAfter: retryAfter != null
            ? int.tryParse(retryAfter)
            : null,
      );

    case 500:
    case 502:
    case 503:
      return ServerException(
        data['message'] ?? 'Server error',
      );

    default:
      return ApiException(
        'HTTP $statusCode: ${data['message'] ?? e.message}',
        statusCode: statusCode,
        data: data,
      );
  }
}
```

## Testing

Test repositories with mocked Dio:

```dart
import 'package:dio/dio.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';
import 'package:test/test.dart';

void main() {
  late Dio dio;
  late DioAdapter dioAdapter;
  late UserRepository repository;

  setUp(() {
    dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
    dioAdapter = DioAdapter(dio: dio);
    repository = ApiUserRepository(dio);
  });

  group('UserRepository', () {
    test('getUser returns user on success', () async {
      const userId = '123';
      final mockResponse = {
        'id': userId,
        'name': 'John Doe',
        'email': 'john@example.com',
      };

      dioAdapter.onGet(
        '/users/$userId',
        (server) => server.reply(200, mockResponse),
      );

      final user = await repository.getUser(userId);

      expect(user.id, userId);
      expect(user.name, 'John Doe');
      expect(user.email, 'john@example.com');
    });

    test('getUser throws NotFoundException on 404', () async {
      const userId = '999';

      dioAdapter.onGet(
        '/users/$userId',
        (server) => server.reply(
          404,
          {'message': 'User not found'},
        ),
      );

      expect(
        () => repository.getUser(userId),
        throwsA(isA<NotFoundException>()),
      );
    });

    test('createUser handles validation errors', () async {
      final dto = CreateUserDto(
        name: '',
        email: 'invalid',
        password: '123',
      );

      dioAdapter.onPost(
        '/users',
        (server) => server.reply(
          422,
          {
            'errors': {
              'name': ['Name is required'],
              'email': ['Email is invalid'],
              'password': ['Password too short'],
            },
          },
        ),
      );

      try {
        await repository.createUser(dto);
        fail('Should throw ValidationException');
      } on ValidationException catch (e) {
        expect(e.errors['name'], isNotEmpty);
        expect(e.errors['email'], isNotEmpty);
        expect(e.errors['password'], isNotEmpty);
      }
    });
  });
}
```

## Best Practices

1. **Use Repository Pattern**: Isolate API logic from business logic
2. **Separate Models**: Keep API models separate from domain models
3. **Handle All Status Codes**: Explicitly handle each expected status code
4. **Validate Input**: Validate data before sending to API
5. **Secure Authentication**: Store tokens securely with flutter_secure_storage
6. **Implement Pagination**: Use cursor or offset pagination for large datasets
7. **Cache Responses**: Cache GET responses when appropriate
8. **Rate Limiting**: Respect API rate limits, handle 429 responses
9. **Versioning**: Include API version in base URL or headers
10. **Test Thoroughly**: Test success cases, error cases, and edge cases

## Conclusion

REST API integration is fundamental to most Flutter applications. Following the patterns in this guide—repository pattern, proper error handling, secure authentication, and thorough testing—will help you build robust, maintainable API integrations that provide excellent user experiences even when networks are unreliable or APIs return errors.
