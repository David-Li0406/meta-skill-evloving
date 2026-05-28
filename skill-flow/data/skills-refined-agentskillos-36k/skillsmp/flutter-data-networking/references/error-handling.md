# Network Error Handling

Complete guide to handling network errors, implementing retry strategies, and building offline-first Flutter applications.

## Overview

Network operations fail frequently in mobile applications due to poor connectivity, server issues, or timeouts. Production applications must handle these failures gracefully, providing clear feedback to users and recovering automatically when possible.

This reference covers comprehensive error handling strategies, automatic retry logic with exponential backoff, and offline-first architecture patterns.

## Error Categories

### Network Errors

Errors related to network connectivity:

- **Connection Timeout**: Server not responding within timeout period
- **Connection Error**: Cannot establish connection (no internet, DNS failure)
- **Send Timeout**: Timeout while sending request data
- **Receive Timeout**: Timeout while receiving response data
- **TLS/SSL Error**: Certificate validation failure

These errors are typically transient and should be retried.

### HTTP Errors

Errors indicated by HTTP status codes:

**Client Errors (4xx):**
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Validation errors
- 429 Too Many Requests: Rate limit exceeded

**Server Errors (5xx):**
- 500 Internal Server Error: Server malfunction
- 502 Bad Gateway: Upstream server error
- 503 Service Unavailable: Temporary outage
- 504 Gateway Timeout: Upstream timeout

Client errors (4xx) should NOT be retried (request is fundamentally wrong). Server errors (5xx) can be retried.

### Serialization Errors

Errors during JSON parsing:

- Invalid JSON format
- Missing required fields
- Type mismatches
- Null values for non-nullable fields

These indicate a mismatch between client expectations and server response.

## Exception Hierarchy

Define a clear exception hierarchy:

```dart
// Base exception
abstract class NetworkException implements Exception {
  final String message;
  final StackTrace? stackTrace;

  NetworkException(this.message, {this.stackTrace});

  @override
  String toString() => message;
}

// Connection-related errors
class ConnectionException extends NetworkException {
  ConnectionException(String message, {StackTrace? stackTrace})
      : super(message, stackTrace: stackTrace);
}

class TimeoutException extends NetworkException {
  TimeoutException(String message, {StackTrace? stackTrace})
      : super(message, stackTrace: stackTrace);
}

class NoInternetException extends NetworkException {
  NoInternetException()
      : super('No internet connection. Please check your network settings.');
}

// HTTP errors
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

class BadRequestException extends HttpException {
  BadRequestException(String message, {dynamic responseData})
      : super(
          message,
          statusCode: 400,
          responseData: responseData,
        );
}

class UnauthorizedException extends HttpException {
  UnauthorizedException([String message = 'Authentication required'])
      : super(message, statusCode: 401);
}

class ForbiddenException extends HttpException {
  ForbiddenException([String message = 'Access denied'])
      : super(message, statusCode: 403);
}

class NotFoundException extends HttpException {
  NotFoundException([String message = 'Resource not found'])
      : super(message, statusCode: 404);
}

class ValidationException extends HttpException {
  final Map<String, List<String>> errors;

  ValidationException(this.errors)
      : super(
          'Validation failed',
          statusCode: 422,
          responseData: errors,
        );

  String getFieldError(String field) {
    return errors[field]?.first ?? '';
  }
}

class RateLimitException extends HttpException {
  final int? retryAfter; // Seconds to wait

  RateLimitException({
    String message = 'Too many requests',
    this.retryAfter,
  }) : super(message, statusCode: 429);
}

class ServerException extends HttpException {
  ServerException(String message, {int statusCode = 500})
      : super(message, statusCode: statusCode);
}

// Serialization errors
class SerializationException extends NetworkException {
  final dynamic data;

  SerializationException(
    String message, {
    this.data,
    StackTrace? stackTrace,
  }) : super(message, stackTrace: stackTrace);
}

// Cancellation
class CancelledException extends NetworkException {
  CancelledException([String message = 'Request was cancelled'])
      : super(message);
}
```

## Error Mapping

Map DioException to domain exceptions:

```dart
class ErrorMapper {
  static NetworkException mapDioException(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
        return TimeoutException(
          'Connection timeout. Please check your internet connection.',
          stackTrace: error.stackTrace,
        );

      case DioExceptionType.sendTimeout:
        return TimeoutException(
          'Send timeout. Please try again.',
          stackTrace: error.stackTrace,
        );

      case DioExceptionType.receiveTimeout:
        return TimeoutException(
          'Receive timeout. The server is taking too long to respond.',
          stackTrace: error.stackTrace,
        );

      case DioExceptionType.badResponse:
        return _mapHttpError(error.response!);

      case DioExceptionType.cancel:
        return CancelledException();

      case DioExceptionType.connectionError:
        return NoInternetException();

      case DioExceptionType.badCertificate:
        return ConnectionException(
          'Security certificate verification failed.',
          stackTrace: error.stackTrace,
        );

      case DioExceptionType.unknown:
      default:
        return NetworkException(
          'An unexpected error occurred: ${error.message}',
          stackTrace: error.stackTrace,
        );
    }
  }

  static HttpException _mapHttpError(Response response) {
    final statusCode = response.statusCode ?? 0;
    final data = response.data;

    // Extract error message
    String message = 'HTTP $statusCode';
    if (data is Map && data['message'] != null) {
      message = data['message'].toString();
    } else if (data is Map && data['error'] != null) {
      message = data['error'].toString();
    }

    switch (statusCode) {
      case 400:
        return BadRequestException(message, responseData: data);

      case 401:
        return UnauthorizedException(message);

      case 403:
        return ForbiddenException(message);

      case 404:
        return NotFoundException(message);

      case 422:
        final errors = data is Map && data['errors'] != null
            ? Map<String, List<String>>.from(
                (data['errors'] as Map).map(
                  (key, value) => MapEntry(
                    key.toString(),
                    (value as List).map((e) => e.toString()).toList(),
                  ),
                ),
              )
            : <String, List<String>>{};
        return ValidationException(errors);

      case 429:
        final retryAfter = response.headers['retry-after']?[0];
        return RateLimitException(
          message: message,
          retryAfter: retryAfter != null ? int.tryParse(retryAfter) : null,
        );

      case 500:
      case 502:
      case 503:
      case 504:
        return ServerException(message, statusCode: statusCode);

      default:
        return HttpException(
          message,
          statusCode: statusCode,
          responseData: data,
        );
    }
  }
}

// Usage in repository
class UserRepository {
  final Dio _dio;

  Future<User> getUser(String id) async {
    try {
      final response = await _dio.get('/users/$id');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw ErrorMapper.mapDioException(e);
    } on SerializationException {
      rethrow;
    } catch (e, stackTrace) {
      throw NetworkException(
        'Unexpected error: $e',
        stackTrace: stackTrace,
      );
    }
  }
}
```

## Retry Strategies

### Exponential Backoff

Automatically retry failed requests with increasing delays:

```dart
class RetryConfig {
  final int maxAttempts;
  final Duration initialDelay;
  final double multiplier;
  final Duration maxDelay;
  final bool addJitter;

  const RetryConfig({
    this.maxAttempts = 3,
    this.initialDelay = const Duration(milliseconds: 100),
    this.multiplier = 2.0,
    this.maxDelay = const Duration(seconds: 10),
    this.addJitter = true,
  });
}

class RetryInterceptor extends QueuedInterceptor {
  final Dio _dio;
  final RetryConfig config;

  RetryInterceptor(this._dio, {this.config = const RetryConfig()});

  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (!_shouldRetry(err)) {
      return handler.next(err);
    }

    final attempt = err.requestOptions.extra['retry_attempt'] ?? 0;

    if (attempt >= config.maxAttempts) {
      print('Max retry attempts reached (${config.maxAttempts})');
      return handler.next(err);
    }

    // Calculate delay
    final delay = _calculateDelay(attempt);

    print('Retrying request (attempt ${attempt + 1}/${config.maxAttempts}) '
        'after ${delay.inMilliseconds}ms');

    await Future.delayed(delay);

    // Update retry count
    err.requestOptions.extra['retry_attempt'] = attempt + 1;

    try {
      final response = await _dio.fetch(err.requestOptions);
      return handler.resolve(response);
    } on DioException catch (e) {
      return handler.next(e);
    }
  }

  bool _shouldRetry(DioException err) {
    // Only retry on network errors and 5xx server errors
    if (err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        err.type == DioExceptionType.connectionError) {
      return true;
    }

    // Retry 5xx server errors
    final statusCode = err.response?.statusCode;
    if (statusCode != null && statusCode >= 500) {
      return true;
    }

    // Don't retry 4xx client errors
    return false;
  }

  Duration _calculateDelay(int attempt) {
    // Exponential backoff: initialDelay * (multiplier ^ attempt)
    var delay = config.initialDelay.inMilliseconds *
        pow(config.multiplier, attempt);

    // Apply max delay cap
    delay = min(delay, config.maxDelay.inMilliseconds.toDouble());

    // Add jitter (randomness) to prevent thundering herd
    if (config.addJitter) {
      final jitter = Random().nextInt(100);
      delay += jitter;
    }

    return Duration(milliseconds: delay.toInt());
  }
}

// Usage
final dio = Dio();
dio.interceptors.add(RetryInterceptor(
  dio,
  config: RetryConfig(
    maxAttempts: 5,
    initialDelay: Duration(milliseconds: 200),
    multiplier: 2.0,
    addJitter: true,
  ),
));
```

### Manual Retry with Backoff

Implement retry logic manually for more control:

```dart
Future<T> retryWithBackoff<T>(
  Future<T> Function() operation, {
  int maxAttempts = 3,
  Duration initialDelay = const Duration(milliseconds: 100),
  double multiplier = 2.0,
  bool Function(Object error)? shouldRetry,
}) async {
  int attempt = 0;
  Duration delay = initialDelay;

  while (true) {
    try {
      return await operation();
    } catch (e) {
      attempt++;

      // Check if we should retry
      if (attempt >= maxAttempts) {
        rethrow;
      }

      if (shouldRetry != null && !shouldRetry(e)) {
        rethrow;
      }

      print('Attempt $attempt failed, retrying in ${delay.inMilliseconds}ms...');

      await Future.delayed(delay);

      // Exponential backoff
      delay *= multiplier;
    }
  }
}

// Usage
final user = await retryWithBackoff(
  () => repository.getUser(userId),
  maxAttempts: 5,
  shouldRetry: (error) {
    // Only retry network errors, not validation errors
    return error is TimeoutException ||
        error is ConnectionException ||
        error is ServerException;
  },
);
```

### Rate Limit Handling

Respect API rate limits:

```dart
class RateLimitInterceptor extends QueuedInterceptor {
  @override
  void onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 429) {
      final retryAfterHeader = err.response?.headers['retry-after']?[0];

      if (retryAfterHeader != null) {
        final retryAfter = int.tryParse(retryAfterHeader);

        if (retryAfter != null) {
          print('Rate limited. Waiting $retryAfter seconds...');
          await Future.delayed(Duration(seconds: retryAfter));

          try {
            final response = await Dio().fetch(err.requestOptions);
            return handler.resolve(response);
          } catch (e) {
            return handler.next(err);
          }
        }
      }
    }

    handler.next(err);
  }
}
```

## Offline Handling

### Connectivity Monitoring

Monitor network connectivity:

```dart
import 'package:connectivity_plus/connectivity_plus.dart';

class ConnectivityService {
  final Connectivity _connectivity = Connectivity();

  Stream<bool> get isConnected => _connectivity.onConnectivityChanged.map(
        (result) => result != ConnectivityResult.none,
      );

  Future<bool> checkConnectivity() async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }
}

// Usage in UI
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder<bool>(
      stream: ConnectivityService().isConnected,
      builder: (context, snapshot) {
        final isConnected = snapshot.data ?? true;

        return MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                if (!isConnected)
                  Container(
                    color: Colors.red,
                    padding: EdgeInsets.all(8),
                    child: Text(
                      'No internet connection',
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                Expanded(child: HomeScreen()),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

### Request Queue

Queue requests made while offline:

```dart
class OfflineRequestQueue {
  final List<QueuedRequest> _queue = [];
  final Dio _dio;
  final ConnectivityService _connectivity;

  OfflineRequestQueue(this._dio, this._connectivity) {
    // Process queue when connectivity is restored
    _connectivity.isConnected.listen((isConnected) {
      if (isConnected) {
        _processQueue();
      }
    });
  }

  Future<Response?> enqueue(RequestOptions options) async {
    final isConnected = await _connectivity.checkConnectivity();

    if (isConnected) {
      // Execute immediately
      return await _dio.fetch(options);
    }

    // Queue for later
    final completer = Completer<Response?>();
    _queue.add(QueuedRequest(options, completer));

    print('Request queued. Queue size: ${_queue.length}');

    return completer.future;
  }

  Future<void> _processQueue() async {
    if (_queue.isEmpty) return;

    print('Processing ${_queue.length} queued requests...');

    final requests = List<QueuedRequest>.from(_queue);
    _queue.clear();

    for (final request in requests) {
      try {
        final response = await _dio.fetch(request.options);
        request.completer.complete(response);
      } catch (e) {
        request.completer.completeError(e);
      }
    }
  }

  int get queueSize => _queue.length;

  void clear() {
    for (final request in _queue) {
      request.completer.completeError(
        CancelledException('Queue cleared'),
      );
    }
    _queue.clear();
  }
}

class QueuedRequest {
  final RequestOptions options;
  final Completer<Response?> completer;

  QueuedRequest(this.options, this.completer);
}
```

### Cache-First Strategy

Return cached data when offline:

```dart
class CacheFirstInterceptor extends Interceptor {
  final Map<String, CachedResponse> _cache = {};

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Only cache GET requests
    if (options.method != 'GET') {
      return handler.next(options);
    }

    final key = _getCacheKey(options);
    final cached = _cache[key];

    // Check if we're online
    final isOnline = await ConnectivityService().checkConnectivity();

    if (!isOnline && cached != null) {
      print('Offline: Returning cached response');
      return handler.resolve(cached.response, true);
    }

    if (cached != null && !cached.isExpired) {
      print('Cache hit: $key');
      return handler.resolve(cached.response, true);
    }

    handler.next(options);
  }

  @override
  void onResponse(
    Response response,
    ResponseInterceptorHandler handler,
  ) {
    if (response.requestOptions.method == 'GET') {
      final key = _getCacheKey(response.requestOptions);
      _cache[key] = CachedResponse(
        response: response,
        timestamp: DateTime.now(),
        ttl: Duration(minutes: 5),
      );
    }

    handler.next(response);
  }

  String _getCacheKey(RequestOptions options) {
    return '${options.path}?${options.queryParameters}';
  }
}

class CachedResponse {
  final Response response;
  final DateTime timestamp;
  final Duration ttl;

  CachedResponse({
    required this.response,
    required this.timestamp,
    required this.ttl,
  });

  bool get isExpired =>
      DateTime.now().difference(timestamp) > ttl;
}
```

## Error UI Patterns

### Error Widget

Display errors to users:

```dart
class ErrorWidget extends StatelessWidget {
  final NetworkException error;
  final VoidCallback? onRetry;

  const ErrorWidget({
    required this.error,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              _getIcon(),
              size: 64,
              color: Colors.red,
            ),
            SizedBox(height: 16),
            Text(
              _getTitle(),
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 8),
            Text(
              error.message,
              style: TextStyle(color: Colors.grey[600]),
              textAlign: TextAlign.center,
            ),
            if (onRetry != null) ...[
              SizedBox(height: 24),
              ElevatedButton(
                onPressed: onRetry,
                child: Text('Retry'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  IconData _getIcon() {
    if (error is NoInternetException) {
      return Icons.wifi_off;
    } else if (error is TimeoutException) {
      return Icons.timer_off;
    } else if (error is NotFoundException) {
      return Icons.search_off;
    } else if (error is UnauthorizedException) {
      return Icons.lock;
    }
    return Icons.error_outline;
  }

  String _getTitle() {
    if (error is NoInternetException) {
      return 'No Internet Connection';
    } else if (error is TimeoutException) {
      return 'Request Timeout';
    } else if (error is NotFoundException) {
      return 'Not Found';
    } else if (error is UnauthorizedException) {
      return 'Authentication Required';
    } else if (error is ServerException) {
      return 'Server Error';
    }
    return 'Error';
  }
}
```

### Snackbar Errors

Show transient error messages:

```dart
class ErrorHandler {
  static void show(BuildContext context, NetworkException error) {
    String message = error.message;
    Color backgroundColor = Colors.red;
    IconData icon = Icons.error;

    if (error is NoInternetException) {
      icon = Icons.wifi_off;
      message = 'No internet connection';
    } else if (error is TimeoutException) {
      icon = Icons.timer_off;
      message = 'Request timed out';
    } else if (error is ValidationException) {
      icon = Icons.warning;
      backgroundColor = Colors.orange;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(icon, color: Colors.white),
            SizedBox(width: 12),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: backgroundColor,
        action: SnackBarAction(
          label: 'Dismiss',
          textColor: Colors.white,
          onPressed: () {
            ScaffoldMessenger.of(context).hideCurrentSnackBar();
          },
        ),
      ),
    );
  }
}

// Usage
try {
  await repository.getUser(userId);
} on NetworkException catch (e) {
  ErrorHandler.show(context, e);
}
```

## Testing Error Handling

Test error scenarios:

```dart
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';

void main() {
  group('Error Handling', () {
    test('maps timeout to TimeoutException', () {
      final dioError = DioException(
        requestOptions: RequestOptions(path: '/test'),
        type: DioExceptionType.connectionTimeout,
      );

      final mapped = ErrorMapper.mapDioException(dioError);

      expect(mapped, isA<TimeoutException>());
    });

    test('retries on network error', () async {
      int attempts = 0;

      final result = await retryWithBackoff(
        () async {
          attempts++;
          if (attempts < 3) {
            throw TimeoutException('Timeout');
          }
          return 'success';
        },
        maxAttempts: 5,
        initialDelay: Duration(milliseconds: 10),
      );

      expect(result, 'success');
      expect(attempts, 3);
    });

    test('does not retry on validation error', () async {
      int attempts = 0;

      try {
        await retryWithBackoff(
          () async {
            attempts++;
            throw ValidationException({});
          },
          maxAttempts: 5,
          shouldRetry: (e) => e is! ValidationException,
        );
        fail('Should throw');
      } on ValidationException {
        expect(attempts, 1);
      }
    });
  });
}
```

## Best Practices

1. **Clear Error Hierarchy**: Define specific exception types for different error categories
2. **User-Friendly Messages**: Provide actionable error messages, not technical details
3. **Automatic Retries**: Retry transient failures with exponential backoff
4. **Selective Retries**: Only retry idempotent operations and transient errors
5. **Offline Support**: Queue requests and show cached data when offline
6. **Error Logging**: Log errors to analytics for debugging
7. **Rate Limit Respect**: Honor Retry-After headers
8. **Timeout Configuration**: Set appropriate timeouts for different operations
9. **Error UI**: Show clear error states with retry options
10. **Testing**: Test all error scenarios thoroughly

## Conclusion

Robust error handling distinguishes production applications from prototypes. Implement a clear exception hierarchy, automatic retry logic with exponential backoff, and offline support to create resilient Flutter applications that handle network failures gracefully and provide excellent user experiences even under poor network conditions.
