# Complete API Client Implementation

Production-ready API client with authentication, error handling, retry logic, and comprehensive features.

## Overview

This example demonstrates a complete, production-ready API client implementation that includes:

- Dio HTTP client with global configuration
- JWT authentication with automatic token refresh
- Comprehensive error handling and mapping
- Automatic retry with exponential backoff
- Request/response logging
- Caching for GET requests
- Request cancellation
- Type-safe repository pattern

## Project Structure

```
lib/
├── api/
│   ├── api_client.dart           # Dio configuration
│   ├── interceptors/
│   │   ├── auth_interceptor.dart
│   │   ├── logging_interceptor.dart
│   │   ├── retry_interceptor.dart
│   │   └── cache_interceptor.dart
│   └── exceptions/
│       └── network_exceptions.dart
├── models/
│   └── user.dart                  # Data models
├── repositories/
│   └── user_repository.dart       # Repository pattern
└── services/
    ├── auth_service.dart          # Authentication
    └── token_storage.dart         # Secure token storage
```

## Models

Define data models with freezed:

```dart
// lib/models/user.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatarUrl,
    String? bio,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    @JsonKey(name: 'updated_at') required DateTime updatedAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

@freezed
class AuthTokens with _$AuthTokens {
  const factory AuthTokens({
    @JsonKey(name: 'access_token') required String accessToken,
    @JsonKey(name: 'refresh_token') required String refreshToken,
    @JsonKey(name: 'expires_in') required int expiresIn,
  }) = _AuthTokens;

  factory AuthTokens.fromJson(Map<String, dynamic> json) =>
      _$AuthTokensFromJson(json);
}

@freezed
class PaginatedResponse<T> with _$PaginatedResponse<T> {
  const factory PaginatedResponse({
    required List<T> data,
    required int page,
    @JsonKey(name: 'per_page') required int perPage,
    required int total,
    @JsonKey(name: 'total_pages') required int totalPages,
  }) = _PaginatedResponse<T>;

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) =>
      _$PaginatedResponseFromJson(json, fromJsonT);
}
```

## Exception Classes

Define exception hierarchy:

```dart
// lib/api/exceptions/network_exceptions.dart
abstract class NetworkException implements Exception {
  final String message;
  final StackTrace? stackTrace;

  NetworkException(this.message, {this.stackTrace});

  @override
  String toString() => message;
}

class NoInternetException extends NetworkException {
  NoInternetException()
      : super('No internet connection. Please check your network settings.');
}

class TimeoutException extends NetworkException {
  TimeoutException(String message, {StackTrace? stackTrace})
      : super(message, stackTrace: stackTrace);
}

class HttpException extends NetworkException {
  final int statusCode;
  final dynamic responseData;

  HttpException(
    String message, {
    required this.statusCode,
    this.responseData,
    StackTrace? stackTrace,
  }) : super(message, stackTrace: stackTrace);
}

class UnauthorizedException extends HttpException {
  UnauthorizedException([String message = 'Authentication required'])
      : super(message, statusCode: 401);
}

class ValidationException extends HttpException {
  final Map<String, List<String>> errors;

  ValidationException(this.errors)
      : super('Validation failed', statusCode: 422, responseData: errors);
}

class ServerException extends HttpException {
  ServerException(String message, {int statusCode = 500})
      : super(message, statusCode: statusCode);
}
```

## Token Storage

Secure token storage:

```dart
// lib/services/token_storage.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenStorage {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  static const _tokenExpiryKey = 'token_expiry';

  Future<void> saveTokens(AuthTokens tokens) async {
    final expiryTime = DateTime.now()
        .add(Duration(seconds: tokens.expiresIn))
        .toIso8601String();

    await Future.wait([
      _storage.write(key: _accessTokenKey, value: tokens.accessToken),
      _storage.write(key: _refreshTokenKey, value: tokens.refreshToken),
      _storage.write(key: _tokenExpiryKey, value: expiryTime),
    ]);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }

  Future<bool> isTokenExpired() async {
    final expiryStr = await _storage.read(key: _tokenExpiryKey);
    if (expiryStr == null) return true;

    final expiry = DateTime.parse(expiryStr);
    // Consider expired 1 minute before actual expiry
    return DateTime.now().isAfter(expiry.subtract(Duration(minutes: 1)));
  }

  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _refreshTokenKey),
      _storage.delete(key: _tokenExpiryKey),
    ]);
  }
}
```

## Authentication Service

Handle authentication:

```dart
// lib/services/auth_service.dart
import 'package:dio/dio.dart';

class AuthService {
  final Dio _dio;
  final TokenStorage _tokenStorage;

  AuthService(this._dio, this._tokenStorage);

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
      await _tokenStorage.saveTokens(tokens);
      return tokens;
    } on DioException catch (e) {
      throw _mapError(e);
    }
  }

  Future<AuthTokens> refreshToken() async {
    final refreshToken = await _tokenStorage.getRefreshToken();

    if (refreshToken == null) {
      throw UnauthorizedException('No refresh token available');
    }

    try {
      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final tokens = AuthTokens.fromJson(response.data);
      await _tokenStorage.saveTokens(tokens);
      return tokens;
    } on DioException catch (e) {
      await _tokenStorage.clearTokens();
      throw UnauthorizedException('Session expired');
    }
  }

  Future<void> logout() async {
    try {
      await _dio.post('/auth/logout');
    } finally {
      await _tokenStorage.clearTokens();
    }
  }

  NetworkException _mapError(DioException e) {
    if (e.response?.statusCode == 401) {
      return UnauthorizedException('Invalid credentials');
    }
    return ServerException('Login failed');
  }
}
```

## Interceptors

### Auth Interceptor

```dart
// lib/api/interceptors/auth_interceptor.dart
import 'package:dio/dio.dart';

class AuthInterceptor extends QueuedInterceptor {
  final TokenStorage _tokenStorage;
  final AuthService _authService;

  AuthInterceptor(this._tokenStorage, this._authService);

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Skip auth for login/register endpoints
    if (options.path.contains('/auth/login') ||
        options.path.contains('/auth/register')) {
      return handler.next(options);
    }

    final token = await _tokenStorage.getAccessToken();

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
      // Check if token is expired
      final isExpired = await _tokenStorage.isTokenExpired();

      if (isExpired) {
        try {
          // Attempt token refresh
          await _authService.refreshToken();

          // Retry original request
          final token = await _tokenStorage.getAccessToken();
          err.requestOptions.headers['Authorization'] = 'Bearer $token';

          final response = await Dio().fetch(err.requestOptions);
          return handler.resolve(response);
        } catch (e) {
          // Refresh failed, user needs to login again
          await _tokenStorage.clearTokens();
          return handler.reject(err);
        }
      }
    }

    handler.next(err);
  }
}
```

### Logging Interceptor

```dart
// lib/api/interceptors/logging_interceptor.dart
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (kDebugMode) {
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('REQUEST[${options.method}] => ${options.uri}');
      print('Headers: ${options.headers}');
      if (options.data != null) {
        print('Data: ${options.data}');
      }
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (kDebugMode) {
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('RESPONSE[${response.statusCode}] => ${response.requestOptions.uri}');
      print('Data: ${response.data}');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (kDebugMode) {
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('ERROR[${err.response?.statusCode}] => ${err.requestOptions.uri}');
      print('Message: ${err.message}');
      if (err.response?.data != null) {
        print('Data: ${err.response?.data}');
      }
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    }
    handler.next(err);
  }
}
```

### Retry Interceptor

```dart
// lib/api/interceptors/retry_interceptor.dart
import 'dart:math';
import 'package:dio/dio.dart';

class RetryInterceptor extends QueuedInterceptor {
  final Dio _dio;
  final int maxRetries;
  final Duration initialDelay;

  RetryInterceptor(
    this._dio, {
    this.maxRetries = 3,
    this.initialDelay = const Duration(milliseconds: 100),
  });

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (!_shouldRetry(err)) {
      return handler.next(err);
    }

    final attempt = err.requestOptions.extra['retry_attempt'] ?? 0;

    if (attempt >= maxRetries) {
      return handler.next(err);
    }

    final delay = _calculateDelay(attempt);
    await Future.delayed(delay);

    err.requestOptions.extra['retry_attempt'] = attempt + 1;

    try {
      final response = await _dio.fetch(err.requestOptions);
      return handler.resolve(response);
    } on DioException catch (e) {
      return handler.next(e);
    }
  }

  bool _shouldRetry(DioException err) {
    return err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        err.type == DioExceptionType.connectionError ||
        (err.response?.statusCode ?? 0) >= 500;
  }

  Duration _calculateDelay(int attempt) {
    final delay = initialDelay.inMilliseconds * pow(2, attempt);
    final jitter = Random().nextInt(100);
    return Duration(milliseconds: delay.toInt() + jitter);
  }
}
```

## API Client

Main API client configuration:

```dart
// lib/api/api_client.dart
import 'package:dio/dio.dart';

class ApiClient {
  late final Dio dio;
  final String baseUrl;
  final TokenStorage _tokenStorage;
  late final AuthService _authService;

  ApiClient({
    required this.baseUrl,
    required TokenStorage tokenStorage,
  }) : _tokenStorage = tokenStorage {
    dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        sendTimeout: const Duration(seconds: 10),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        validateStatus: (status) => status != null && status < 500,
      ),
    );

    _authService = AuthService(dio, _tokenStorage);

    // Add interceptors
    dio.interceptors.addAll([
      if (kDebugMode) LoggingInterceptor(),
      AuthInterceptor(_tokenStorage, _authService),
      RetryInterceptor(dio, maxRetries: 3),
    ]);
  }

  AuthService get authService => _authService;
}
```

## Repository

Implement repository pattern:

```dart
// lib/repositories/user_repository.dart
import 'package:dio/dio.dart';

class UserRepository {
  final Dio _dio;

  UserRepository(this._dio);

  Future<User> getUser(String id) async {
    try {
      final response = await _dio.get('/users/$id');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<PaginatedResponse<User>> getUsers({
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

      return PaginatedResponse<User>.fromJson(
        response.data,
        (json) => User.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<User> createUser({
    required String name,
    required String email,
  }) async {
    try {
      final response = await _dio.post(
        '/users',
        data: {
          'name': name,
          'email': email,
        },
      );

      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<User> updateUser(String id, {String? name, String? bio}) async {
    try {
      final response = await _dio.patch(
        '/users/$id',
        data: {
          if (name != null) 'name': name,
          if (bio != null) 'bio': bio,
        },
      );

      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<void> deleteUser(String id) async {
    try {
      await _dio.delete('/users/$id');
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  NetworkException _mapException(DioException e) {
    // Use error mapper from error-handling.md
    return ErrorMapper.mapDioException(e);
  }
}
```

## Dependency Injection

Set up dependency injection:

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider(
          create: (_) => TokenStorage(),
        ),
        Provider(
          create: (context) => ApiClient(
            baseUrl: 'https://api.example.com',
            tokenStorage: context.read<TokenStorage>(),
          ),
        ),
        Provider(
          create: (context) => UserRepository(
            context.read<ApiClient>().dio,
          ),
        ),
      ],
      child: MaterialApp(
        title: 'API Client Demo',
        home: HomeScreen(),
      ),
    );
  }
}
```

## Usage in UI

Use the repository in widgets:

```dart
class UserListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final repository = context.read<UserRepository>();

    return Scaffold(
      appBar: AppBar(title: Text('Users')),
      body: FutureBuilder<PaginatedResponse<User>>(
        future: repository.getUsers(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            final error = snapshot.error;
            if (error is NetworkException) {
              return ErrorWidget(
                error: error,
                onRetry: () => setState(() {}),
              );
            }
            return Center(child: Text('An error occurred'));
          }

          final users = snapshot.data!.data;

          return ListView.builder(
            itemCount: users.length,
            itemBuilder: (context, index) {
              final user = users[index];
              return ListTile(
                leading: CircleAvatar(
                  backgroundImage: user.avatarUrl != null
                      ? NetworkImage(user.avatarUrl!)
                      : null,
                  child: user.avatarUrl == null
                      ? Text(user.name[0])
                      : null,
                ),
                title: Text(user.name),
                subtitle: Text(user.email),
              );
            },
          );
        },
      ),
    );
  }
}
```

## Testing

Test the repository:

```dart
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';

void main() {
  late UserRepository repository;
  late MockDio mockDio;

  setUp(() {
    mockDio = MockDio();
    repository = UserRepository(mockDio);
  });

  group('UserRepository', () {
    test('getUser returns user on success', () async {
      when(mockDio.get('/users/123')).thenAnswer(
        (_) async => Response(
          data: {
            'id': '123',
            'name': 'John Doe',
            'email': 'john@example.com',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: '/users/123'),
        ),
      );

      final user = await repository.getUser('123');

      expect(user.id, '123');
      expect(user.name, 'John Doe');
    });

    test('createUser throws ValidationException on 422', () async {
      when(mockDio.post('/users', data: anyNamed('data'))).thenThrow(
        DioException(
          requestOptions: RequestOptions(path: '/users'),
          response: Response(
            statusCode: 422,
            data: {
              'errors': {
                'email': ['Email is required']
              }
            },
            requestOptions: RequestOptions(path: '/users'),
          ),
        ),
      );

      expect(
        () => repository.createUser(name: 'John', email: ''),
        throwsA(isA<ValidationException>()),
      );
    });
  });
}
```

## Conclusion

This complete API client implementation demonstrates production-ready patterns for Flutter networking including authentication, error handling, retry logic, and testing. Adapt this structure to your specific API requirements while maintaining the separation of concerns and robust error handling.
