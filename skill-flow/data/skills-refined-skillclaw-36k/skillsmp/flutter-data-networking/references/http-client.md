# HTTP Client Reference

Comprehensive guide to implementing HTTP clients in Flutter using the Dio package.

## Overview

HTTP clients are the foundation of network communication in Flutter applications. While Flutter's basic `http` package works for simple use cases, production applications benefit significantly from Dio's advanced features including interceptors, global configuration, request cancellation, and sophisticated error handling.

This reference covers everything you need to build robust, production-ready HTTP clients using Dio, from basic setup through advanced patterns like retry logic, authentication interceptors, and file uploads.

## Package Comparison

### http Package

The official `http` package is Flutter's minimal HTTP client:

**Advantages:**
- Lightweight and simple API
- Official Flutter package with guaranteed maintenance
- Sufficient for basic GET/POST requests
- No learning curve

**Disadvantages:**
- No interceptor support
- Manual configuration for each request
- Limited error information
- No built-in retry logic
- No request cancellation
- No upload/download progress tracking

**When to Use:** Simple apps, quick prototypes, learning projects, or when bundle size is critical.

### Dio Package

Dio is a powerful HTTP client built on top of Dart's http library:

**Advantages:**
- Interceptors for cross-cutting concerns
- Global configuration (base URL, headers, timeouts)
- Request cancellation with CancelToken
- FormData and multipart file uploads
- Download progress callbacks
- Sophisticated error information
- Built-in transformers
- Support for HTTP/2

**Disadvantages:**
- Slightly larger bundle size
- More complex API
- Additional dependency to maintain

**When to Use:** Production applications, apps requiring authentication, file uploads/downloads, or advanced error handling.

## Dio Setup

### Installation

Add Dio to your `pubspec.yaml`:

```yaml
dependencies:
  dio: ^5.4.0
```

Run `flutter pub get` to install the package.

### Basic Configuration

Create a configured Dio instance:

```dart
import 'package:dio/dio.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient({String? baseUrl}) {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl ?? 'https://api.example.com',
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        sendTimeout: const Duration(seconds: 10),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        validateStatus: (status) {
          // Consider any status code < 500 as successful
          // We'll handle 4xx errors manually
          return status != null && status < 500;
        },
      ),
    );
  }

  Dio get dio => _dio;
}
```

### BaseOptions Explained

**baseUrl:** The base URL prepended to all requests. Individual requests append their paths to this base.

**connectTimeout:** Maximum time to establish a connection to the server. If exceeded, a DioException with type `connectionTimeout` is thrown.

**receiveTimeout:** Maximum time to receive data after connection is established. Useful for large responses or slow servers.

**sendTimeout:** Maximum time to send data to the server. Important for upload operations.

**headers:** Default headers sent with every request. Can be overridden per-request.

**validateStatus:** Function that determines if a response is successful. By default, only 2xx codes are successful. The example above treats 4xx as "successful" so they can be handled explicitly rather than throwing exceptions.

### Environment-Based Configuration

Support multiple environments (development, staging, production):

```dart
enum Environment {
  development,
  staging,
  production,
}

class ApiConfig {
  static String getBaseUrl(Environment env) {
    switch (env) {
      case Environment.development:
        return 'http://localhost:3000';
      case Environment.staging:
        return 'https://staging-api.example.com';
      case Environment.production:
        return 'https://api.example.com';
    }
  }
}

class ApiClient {
  late final Dio _dio;

  ApiClient({required Environment environment}) {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.getBaseUrl(environment),
        // ... other options
      ),
    );
  }
}
```

Use const environment variables or build flavors to select the environment at compile time.

## Making Requests

### GET Requests

Fetch data from the server:

```dart
// Simple GET
Future<User> getUser(String userId) async {
  try {
    final response = await _dio.get('/users/$userId');
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _handleError(e);
  }
}

// GET with query parameters
Future<List<User>> searchUsers({
  required String query,
  int page = 1,
  int perPage = 20,
}) async {
  try {
    final response = await _dio.get(
      '/users/search',
      queryParameters: {
        'q': query,
        'page': page,
        'per_page': perPage,
      },
    );
    return (response.data['results'] as List)
        .map((json) => User.fromJson(json))
        .toList();
  } on DioException catch (e) {
    throw _handleError(e);
  }
}

// GET with custom headers
Future<User> getUser(String userId, {required String token}) async {
  try {
    final response = await _dio.get(
      '/users/$userId',
      options: Options(
        headers: {'Authorization': 'Bearer $token'},
      ),
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

### POST Requests

Send data to create new resources:

```dart
// POST with JSON body
Future<User> createUser(User user) async {
  try {
    final response = await _dio.post(
      '/users',
      data: user.toJson(),
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _handleError(e);
  }
}

// POST with form data
Future<void> submitForm(Map<String, dynamic> formData) async {
  try {
    await _dio.post(
      '/forms/submit',
      data: FormData.fromMap(formData),
      options: Options(
        contentType: 'application/x-www-form-urlencoded',
      ),
    );
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

### PUT and PATCH Requests

Update existing resources:

```dart
// PUT - Replace entire resource
Future<User> updateUser(String userId, User user) async {
  try {
    final response = await _dio.put(
      '/users/$userId',
      data: user.toJson(),
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _handleError(e);
  }
}

// PATCH - Partial update
Future<User> patchUser(String userId, Map<String, dynamic> updates) async {
  try {
    final response = await _dio.patch(
      '/users/$userId',
      data: updates,
    );
    return User.fromJson(response.data);
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

### DELETE Requests

Remove resources:

```dart
Future<void> deleteUser(String userId) async {
  try {
    await _dio.delete('/users/$userId');
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

## Interceptors

Interceptors are Dio's most powerful feature, allowing you to intercept requests, responses, and errors globally. They're perfect for cross-cutting concerns like authentication, logging, and error handling.

### Interceptor Types

Dio supports three interceptor types:

**Interceptor:** Base class that executes requests concurrently. Use for stateless operations.

**QueuedInterceptor:** Processes requests sequentially in a queue. Use when order matters or for stateful operations like token refresh.

**InterceptorsWrapper:** Simplified wrapper that doesn't require implementing all methods. Most commonly used.

### Authentication Interceptor

Automatically add authentication tokens to requests:

```dart
class AuthInterceptor extends Interceptor {
  final TokenStorage _tokenStorage;

  AuthInterceptor(this._tokenStorage);

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Get token from secure storage
    final token = await _tokenStorage.getToken();

    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    // Continue with the request
    handler.next(options);
  }

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      // Token expired, try to refresh
      if (await _refreshToken(err.requestOptions)) {
        // Retry the request with new token
        try {
          final response = await _dio.fetch(err.requestOptions);
          return handler.resolve(response);
        } catch (e) {
          return handler.reject(err);
        }
      }
    }

    // Continue with the error
    handler.next(err);
  }

  Future<bool> _refreshToken(RequestOptions options) async {
    try {
      final refreshToken = await _tokenStorage.getRefreshToken();
      if (refreshToken == null) return false;

      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final newToken = response.data['access_token'];
      await _tokenStorage.saveToken(newToken);

      // Update the failed request with new token
      options.headers['Authorization'] = 'Bearer $newToken';
      return true;
    } catch (e) {
      return false;
    }
  }
}

// Add to Dio instance
_dio.interceptors.add(AuthInterceptor(tokenStorage));
```

### Logging Interceptor

Log all requests and responses for debugging:

```dart
class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) {
    print('REQUEST[${options.method}] => PATH: ${options.path}');
    print('Headers: ${options.headers}');
    print('Data: ${options.data}');
    handler.next(options);
  }

  @override
  void onResponse(
    Response response,
    ResponseInterceptorHandler handler,
  ) {
    print('RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
    print('Data: ${response.data}');
    handler.next(response);
  }

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) {
    print('ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
    print('Message: ${err.message}');
    handler.next(err);
  }
}

// Add only in debug mode
if (kDebugMode) {
  _dio.interceptors.add(LoggingInterceptor());
}
```

For production, use the official `dio_logging_interceptor` package which provides better formatting and filtering.

### Retry Interceptor

Automatically retry failed requests with exponential backoff:

```dart
class RetryInterceptor extends QueuedInterceptor {
  final Dio _dio;
  final int maxRetries;
  final Duration initialDelay;

  RetryInterceptor({
    required Dio dio,
    this.maxRetries = 3,
    this.initialDelay = const Duration(milliseconds: 100),
  }) : _dio = dio;

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (!_shouldRetry(err)) {
      return handler.next(err);
    }

    final retryCount = err.requestOptions.extra['retry_count'] ?? 0;

    if (retryCount >= maxRetries) {
      return handler.next(err);
    }

    // Calculate delay with exponential backoff and jitter
    final delay = initialDelay * (1 << retryCount);
    final jitter = Duration(
      milliseconds: Random().nextInt(100),
    );

    await Future.delayed(delay + jitter);

    // Increment retry count
    err.requestOptions.extra['retry_count'] = retryCount + 1;

    try {
      final response = await _dio.fetch(err.requestOptions);
      return handler.resolve(response);
    } on DioException catch (e) {
      return handler.next(e);
    }
  }

  bool _shouldRetry(DioException err) {
    // Only retry on network errors and 5xx server errors
    return err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        err.type == DioExceptionType.connectionError ||
        (err.response?.statusCode ?? 0) >= 500;
  }
}

_dio.interceptors.add(RetryInterceptor(dio: _dio));
```

### Cache Interceptor

Cache GET responses to reduce network usage:

```dart
class CacheInterceptor extends Interceptor {
  final Map<String, Response> _cache = {};
  final Duration cacheDuration;

  CacheInterceptor({
    this.cacheDuration = const Duration(minutes: 5),
  });

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) {
    // Only cache GET requests
    if (options.method != 'GET') {
      return handler.next(options);
    }

    final cacheKey = _getCacheKey(options);
    final cachedResponse = _cache[cacheKey];

    if (cachedResponse != null) {
      print('Cache hit: $cacheKey');
      return handler.resolve(cachedResponse);
    }

    handler.next(options);
  }

  @override
  void onResponse(
    Response response,
    ResponseInterceptorHandler handler,
  ) {
    if (response.requestOptions.method == 'GET') {
      final cacheKey = _getCacheKey(response.requestOptions);
      _cache[cacheKey] = response;

      // Clear cache after duration
      Future.delayed(cacheDuration, () {
        _cache.remove(cacheKey);
      });
    }

    handler.next(response);
  }

  String _getCacheKey(RequestOptions options) {
    return '${options.path}?${options.queryParameters}';
  }

  void clearCache() {
    _cache.clear();
  }
}
```

For production, consider using persistent cache storage with packages like `dio_cache_interceptor`.

## Request Cancellation

Cancel in-flight requests when they're no longer needed:

```dart
class UserRepository {
  final Dio _dio;
  CancelToken? _cancelToken;

  Future<List<User>> searchUsers(String query) async {
    // Cancel previous request if still running
    _cancelToken?.cancel('New search started');

    // Create new cancel token
    _cancelToken = CancelToken();

    try {
      final response = await _dio.get(
        '/users/search',
        queryParameters: {'q': query},
        cancelToken: _cancelToken,
      );

      return (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
    } on DioException catch (e) {
      if (e.type == DioExceptionType.cancel) {
        // Request was cancelled, return empty list
        return [];
      }
      rethrow;
    }
  }

  void dispose() {
    _cancelToken?.cancel();
  }
}
```

This pattern is especially useful for search-as-you-type features where each keystroke triggers a new request.

## File Uploads

### Single File Upload

Upload files using FormData:

```dart
Future<void> uploadProfilePicture(String userId, File image) async {
  final formData = FormData.fromMap({
    'user_id': userId,
    'image': await MultipartFile.fromFile(
      image.path,
      filename: 'profile.jpg',
      contentType: MediaType('image', 'jpeg'),
    ),
  });

  try {
    await _dio.post(
      '/users/$userId/profile-picture',
      data: formData,
      onSendProgress: (sent, total) {
        final progress = (sent / total * 100).toStringAsFixed(0);
        print('Upload progress: $progress%');
      },
    );
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

### Multiple File Upload

Upload multiple files in a single request:

```dart
Future<void> uploadDocuments(String userId, List<File> files) async {
  final formData = FormData.fromMap({
    'user_id': userId,
    'documents': [
      for (final file in files)
        await MultipartFile.fromFile(
          file.path,
          filename: path.basename(file.path),
        ),
    ],
  });

  try {
    await _dio.post(
      '/users/$userId/documents',
      data: formData,
      onSendProgress: (sent, total) {
        final progress = (sent / total * 100).toStringAsFixed(0);
        print('Upload progress: $progress%');
      },
    );
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

## File Downloads

### Download to Memory

Download files directly into memory:

```dart
Future<Uint8List> downloadFile(String url) async {
  try {
    final response = await _dio.get<Uint8List>(
      url,
      options: Options(
        responseType: ResponseType.bytes,
      ),
      onReceiveProgress: (received, total) {
        if (total != -1) {
          final progress = (received / total * 100).toStringAsFixed(0);
          print('Download progress: $progress%');
        }
      },
    );

    return response.data!;
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

### Download to File

Download large files directly to disk:

```dart
Future<void> downloadFile(String url, String savePath) async {
  try {
    await _dio.download(
      url,
      savePath,
      onReceiveProgress: (received, total) {
        if (total != -1) {
          final progress = (received / total * 100).toStringAsFixed(0);
          print('Download progress: $progress%');
        }
      },
    );
  } on DioException catch (e) {
    throw _handleError(e);
  }
}
```

## Timeout Configuration

Configure different timeouts for different scenarios:

```dart
// Short timeout for health checks
Future<bool> healthCheck() async {
  try {
    await _dio.get(
      '/health',
      options: Options(
        receiveTimeout: const Duration(seconds: 3),
        sendTimeout: const Duration(seconds: 3),
      ),
    );
    return true;
  } catch (e) {
    return false;
  }
}

// Long timeout for file uploads
Future<void> uploadLargeFile(File file) async {
  await _dio.post(
    '/upload',
    data: FormData.fromMap({
      'file': await MultipartFile.fromFile(file.path),
    }),
    options: Options(
      sendTimeout: const Duration(minutes: 5),
    ),
  );
}

// No timeout for streaming
Future<void> streamData() async {
  await _dio.get(
    '/stream',
    options: Options(
      receiveTimeout: null, // Disable timeout
    ),
  );
}
```

## Error Handling

Handle different error types appropriately:

```dart
Exception _handleError(DioException error) {
  switch (error.type) {
    case DioExceptionType.connectionTimeout:
    case DioExceptionType.sendTimeout:
    case DioExceptionType.receiveTimeout:
      return NetworkException('Connection timeout. Please check your internet connection.');

    case DioExceptionType.badResponse:
      return _handleHttpError(error.response!);

    case DioExceptionType.cancel:
      return CancelledException('Request was cancelled');

    case DioExceptionType.connectionError:
      return NetworkException('No internet connection');

    case DioExceptionType.badCertificate:
      return NetworkException('Security certificate verification failed');

    case DioExceptionType.unknown:
    default:
      return NetworkException('An unexpected error occurred');
  }
}

Exception _handleHttpError(Response response) {
  switch (response.statusCode) {
    case 400:
      return BadRequestException(response.data['message']);
    case 401:
      return UnauthorizedException('Authentication required');
    case 403:
      return ForbiddenException('Access denied');
    case 404:
      return NotFoundException('Resource not found');
    case 422:
      return ValidationException(response.data['errors']);
    case 429:
      return RateLimitException('Too many requests');
    case 500:
      return ServerException('Server error occurred');
    case 503:
      return ServerException('Service temporarily unavailable');
    default:
      return ServerException('HTTP ${response.statusCode}: ${response.statusMessage}');
  }
}
```

## Testing

Test your HTTP client with mock responses:

```dart
import 'package:dio/dio.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';
import 'package:test/test.dart';

void main() {
  late Dio dio;
  late DioAdapter dioAdapter;
  late ApiClient apiClient;

  setUp(() {
    dio = Dio();
    dioAdapter = DioAdapter(dio: dio);
    apiClient = ApiClient(dio: dio);
  });

  test('getUser returns user on success', () async {
    const userId = '123';
    final mockUser = {'id': userId, 'name': 'John Doe'};

    dioAdapter.onGet(
      '/users/$userId',
      (server) => server.reply(200, mockUser),
    );

    final user = await apiClient.getUser(userId);

    expect(user.id, userId);
    expect(user.name, 'John Doe');
  });

  test('getUser throws on 404', () async {
    const userId = '999';

    dioAdapter.onGet(
      '/users/$userId',
      (server) => server.reply(404, {'message': 'User not found'}),
    );

    expect(
      () => apiClient.getUser(userId),
      throwsA(isA<NotFoundException>()),
    );
  });
}
```

## Best Practices

1. **Single Dio Instance**: Create one configured Dio instance per API and reuse it throughout your app
2. **Dependency Injection**: Inject Dio instances rather than creating them directly in classes
3. **Type Safety**: Always parse responses into strongly-typed models
4. **Error Handling**: Handle all DioException types and provide user-friendly messages
5. **Interceptors**: Use interceptors for cross-cutting concerns, not per-request logic
6. **Cancel Tokens**: Always cancel requests when the widget that initiated them is disposed
7. **Timeouts**: Set reasonable timeout values based on expected response times
8. **Progress Callbacks**: Show progress for uploads and downloads over 1MB
9. **Logging**: Enable detailed logging in development, minimal logging in production
10. **Testing**: Mock all network calls in tests, never hit real APIs

## Conclusion

Dio provides everything needed for production-quality HTTP networking in Flutter. Its interceptor system, error handling, and advanced features like request cancellation and progress tracking make it the clear choice for any application beyond basic prototypes.

Start with basic configuration and requests, add interceptors as needed for authentication and logging, and implement retry logic and caching for robust production behavior. Always handle errors explicitly and test both success and failure scenarios.
