---
name: flutter-data-networking
description: Master HTTP clients, REST APIs, GraphQL integration, WebSockets, and JSON serialization in Flutter applications. Use when implementing API calls, handling network requests, parsing JSON, or working with real-time data.
version: 1.0.0
---

# Flutter Data Networking

Master HTTP clients, REST APIs, GraphQL, WebSockets, and JSON serialization in Flutter applications.

## When to Use This Skill

Use this skill when working with Flutter applications that need to:

- Make HTTP requests to REST APIs or web services
- Implement GraphQL queries, mutations, or subscriptions
- Establish real-time bidirectional communication with WebSockets
- Serialize and deserialize JSON data with type safety
- Handle network errors, timeouts, and offline scenarios
- Implement authentication and authorization headers
- Build offline-first applications with data synchronization
- Upload or download files over the network
- Create robust API clients with interceptors and middleware

## Overview

Networking is fundamental to modern Flutter applications. Whether you're fetching data from a REST API, subscribing to real-time updates via WebSockets, or querying a GraphQL backend, Flutter provides powerful tools and packages to handle all networking scenarios efficiently and reliably.

This skill covers the complete spectrum of networking in Flutter, from basic HTTP requests to advanced patterns like offline-first architecture, request interceptors, and automatic retry strategies. You'll learn to choose the right networking solution for your needs and implement it following industry best practices.

## HTTP Client Packages

Flutter offers multiple HTTP client options, each suited to different use cases:

### http Package

The official `http` package is Flutter's simplest HTTP client, ideal for straightforward API calls. It provides basic GET, POST, PUT, DELETE methods with minimal configuration. Use it for simple applications or when you need a lightweight solution without advanced features.

The package is cross-platform, supporting Android, iOS, macOS, Windows, Linux, and web. However, it requires platform-specific permissions configuration, such as internet permission in AndroidManifest.xml for Android and network client entitlements for macOS.

### Dio Package

Dio is a powerful, feature-rich HTTP client that has become the industry standard for Flutter networking. It excels with:

- **Global Configuration**: Set base URLs, headers, timeouts, and other options globally for all requests
- **Interceptors**: Intercept requests, responses, and errors for logging, authentication, or transformation
- **Request Cancellation**: Cancel in-flight requests when they're no longer needed
- **FormData Support**: Upload files with multipart form data
- **Download Progress**: Track download progress for large files
- **Automatic Retries**: Configure retry logic for failed requests
- **Custom Adapters**: Replace the default HTTP adapter with custom implementations

Dio's interceptor system is particularly powerful, allowing you to implement cross-cutting concerns like JWT authentication, request logging, error handling, and response caching without duplicating code across your application.

### Choosing the Right Client

For production applications, Dio is typically the better choice due to its robust feature set and excellent error handling. Use the basic `http` package only for simple apps or quick prototypes. For enterprise applications requiring advanced features like certificate pinning, custom adapters, or sophisticated retry logic, Dio provides the necessary flexibility.

## REST API Integration

REST (Representational State Transfer) APIs are the most common backend architecture for Flutter applications. Implementing REST APIs effectively requires understanding HTTP methods, status codes, headers, and error handling.

### CRUD Operations

REST APIs typically expose four core operations (CRUD):

- **CREATE**: POST requests to create new resources
- **READ**: GET requests to retrieve existing resources
- **UPDATE**: PUT or PATCH requests to modify resources
- **DELETE**: DELETE requests to remove resources

Each operation should be wrapped in a service or repository class that handles serialization, error handling, and business logic. This separation of concerns makes your code more testable and maintainable.

### Authentication Patterns

Most production APIs require authentication, typically implemented using:

- **Bearer Tokens**: JWT tokens sent in the Authorization header
- **API Keys**: Static keys passed in headers or query parameters
- **OAuth 2.0**: Token-based authentication with refresh tokens

Dio interceptors are ideal for implementing authentication, automatically adding authentication headers to every request and handling token refresh when tokens expire.

### Error Handling

Robust error handling distinguishes production-quality apps from prototypes. Your networking layer should handle:

- **Network Errors**: Connection timeouts, DNS failures, no internet
- **HTTP Errors**: 4xx client errors, 5xx server errors
- **Serialization Errors**: Invalid JSON or schema mismatches
- **Business Logic Errors**: Application-specific error codes

Implement a consistent error handling strategy using custom exception types and a centralized error handler that can display appropriate messages to users.

## GraphQL Integration

GraphQL is an alternative to REST that allows clients to request exactly the data they need, reducing over-fetching and under-fetching. The `graphql_flutter` package provides comprehensive GraphQL support for Flutter.

### Core Concepts

GraphQL operates through three operation types:

- **Queries**: Read operations that fetch data
- **Mutations**: Write operations that create, update, or delete data
- **Subscriptions**: Real-time operations that push updates to clients

Unlike REST, GraphQL uses a single endpoint and a typed schema that defines available operations and data structures. This schema provides excellent type safety and enables powerful tooling.

### graphql_flutter Widgets

The package provides three primary widgets:

- **Query**: Executes GraphQL queries and rebuilds when data changes
- **Mutation**: Provides a callback to execute mutations
- **Subscription**: Opens a WebSocket connection for real-time updates

All widgets must be wrapped in a GraphQLProvider that configures the GraphQL client, including the endpoint URL, authentication, and caching policies.

### Caching and Optimistic Updates

graphql_flutter includes a sophisticated caching system that normalizes data by type and ID. This enables:

- **Cache-first queries**: Return cached data immediately, then update if needed
- **Optimistic updates**: Update the UI immediately, before server confirmation
- **Cache persistence**: Save cache to disk for offline access

Proper cache configuration significantly improves perceived performance and enables offline functionality.

## WebSocket Communication

WebSockets provide full-duplex communication channels over a single TCP connection, enabling real-time bidirectional data flow. They're essential for features like chat, live notifications, collaborative editing, and real-time dashboards.

### web_socket_channel Package

Flutter's `web_socket_channel` package provides a Stream-based API for WebSocket communication. The package abstracts platform differences and provides a consistent interface across all Flutter platforms.

WebSocket connections follow a lifecycle:

1. **Connection**: Establish a WebSocket connection to a URL (ws:// or wss://)
2. **Communication**: Send messages via the sink, receive via the stream
3. **Closure**: Close the connection gracefully when done

### Stream-Based Architecture

WebSockets integrate naturally with Flutter's reactive architecture through Streams. Use StreamBuilder widgets to display real-time data, and StreamControllers to manage WebSocket state in your business logic layer.

### Error Handling and Reconnection

Production WebSocket implementations must handle:

- **Connection Failures**: Network issues, server unavailability
- **Disconnections**: Unexpected connection drops
- **Reconnection Logic**: Exponential backoff for automatic reconnection
- **Message Queuing**: Queue messages sent while disconnected

Implement a WebSocket manager class that handles these concerns automatically, exposing a simple Stream interface to your application code.

## JSON Serialization

JSON is the standard data format for web APIs. Flutter provides multiple approaches to JSON serialization, from manual parsing to automatic code generation.

### Manual Serialization

For simple data structures, manual serialization using `dart:convert` is straightforward. You write fromJson and toJson methods manually. This approach works for small projects but becomes error-prone and tedious as your data models grow.

### Code Generation with json_serializable

The `json_serializable` package automatically generates serialization code from annotated classes. This approach:

- **Eliminates Boilerplate**: No manual fromJson/toJson implementation
- **Prevents Runtime Errors**: Catches serialization issues at compile time
- **Improves Maintainability**: Generated code stays in sync with your models

To use json_serializable, annotate your model classes with @JsonSerializable() and run build_runner to generate the serialization code.

### Freezed Package

Freezed combines code generation with immutable data classes, providing:

- **Immutability**: All fields are final by default
- **copyWith Method**: Create modified copies of objects
- **Union Types**: Model multiple states or variants
- **Deep Equality**: Automatic == and hashCode implementation
- **JSON Serialization**: Integrated with json_serializable

Freezed is the recommended approach for production applications, especially when combined with state management solutions like Riverpod or Bloc. The immutability guarantees eliminate entire classes of bugs related to unexpected state mutations.

### Custom Converters

For complex data types (DateTime, enums, nested objects), implement custom JsonConverter classes. These converters handle special serialization logic and can be reused across your application.

## Error Handling Strategies

Robust error handling is critical for production applications. Network operations can fail in numerous ways, and your application must handle failures gracefully.

### Exception Types

Categorize network errors into distinct types:

- **Network Exceptions**: Timeouts, connection failures, DNS errors
- **HTTP Exceptions**: 4xx and 5xx status codes
- **Serialization Exceptions**: JSON parsing failures
- **Business Logic Exceptions**: Application-specific errors

Create custom exception classes for each category, including relevant context like status codes, error messages, and original exceptions.

### Retry Strategies

Many network failures are transient and succeed when retried. Implement retry logic with:

- **Exponential Backoff**: Increase delay between retries (100ms, 200ms, 400ms, etc.)
- **Maximum Attempts**: Limit retries to prevent infinite loops (typically 3-5 attempts)
- **Jitter**: Add random delay to prevent thundering herd problems
- **Selective Retries**: Only retry idempotent operations and transient errors

Dio's interceptor system makes implementing retry logic straightforward. For selective retries, only retry on network errors and 5xx server errors, never on 4xx client errors which indicate problems with the request itself.

### Offline Handling

Modern applications should function partially or fully while offline. Implement offline support through:

- **Connectivity Monitoring**: Detect online/offline state changes
- **Request Queuing**: Queue requests made while offline, send when online
- **Local Caching**: Cache API responses for offline access
- **Conflict Resolution**: Handle conflicts when local and server data diverge

The repository pattern provides an excellent abstraction for offline handling, presenting a unified data interface regardless of connectivity state.

## Offline-First Architecture

Offline-first applications prioritize local data and synchronize with servers opportunistically. This architecture improves perceived performance and enables true offline functionality.

### Repository Pattern

The repository pattern is central to offline-first architecture. Repositories:

- **Abstract Data Sources**: Hide whether data comes from network or local storage
- **Coordinate Synchronization**: Manage syncing between local and remote data
- **Provide Single Source of Truth**: Application code interacts only with repositories

A typical repository combines a local database (SQLite, Hive, Isar) with a remote API client, returning local data immediately and updating from the server in the background.

### Synchronization Strategies

Implement synchronization using:

- **Background Sync**: Periodic background tasks that sync data (using WorkManager)
- **Pull-to-Refresh**: User-initiated sync via pull-to-refresh gesture
- **Push Notifications**: Server-initiated sync via push notifications
- **Hybrid Approach**: Combine periodic sync with push notifications

### Conflict Resolution

Conflicts occur when data is modified both locally and remotely before synchronization. Common resolution strategies include:

- **Last Write Wins**: Newest change takes precedence (based on timestamps)
- **Server Wins**: Server data always takes precedence
- **Client Wins**: Local data always takes precedence
- **Custom Merge Logic**: Application-specific merge rules
- **User Resolution**: Prompt user to resolve conflicts manually

Choose a strategy based on your application's requirements. Last write wins works for most applications, while user resolution is necessary for collaborative editing.

## Best Practices

Follow these best practices for production-quality networking code:

### Separation of Concerns

- **Isolate Network Logic**: Keep network code in dedicated service or repository classes
- **Model Layer**: Define clean data models separate from API response structures
- **Error Boundaries**: Handle errors at appropriate levels (network, business, UI)

### Performance Optimization

- **Connection Pooling**: Reuse HTTP connections for better performance
- **Request Deduplication**: Avoid duplicate concurrent requests
- **Response Caching**: Cache responses with appropriate TTL
- **Lazy Loading**: Load data progressively, not all at once
- **Pagination**: Use pagination for large datasets

### Security

- **HTTPS Only**: Never use HTTP in production
- **Certificate Pinning**: Pin SSL certificates for critical APIs
- **Secure Token Storage**: Use flutter_secure_storage for tokens
- **Token Expiration**: Implement automatic token refresh
- **Input Validation**: Validate all data before sending to server

### Testing

- **Mock Network Calls**: Use packages like mockito or mocktail
- **Test Error Scenarios**: Test timeout, network failure, invalid responses
- **Integration Tests**: Test against real APIs in staging environment
- **Network Simulation**: Use tools to simulate slow/flaky networks

### Monitoring and Logging

- **Request Logging**: Log all requests in development, selectively in production
- **Error Tracking**: Integrate with services like Sentry or Firebase Crashlytics
- **Performance Metrics**: Track request duration, success rates, error rates
- **Network Analytics**: Monitor bandwidth usage and API costs

## References

For detailed implementation guidance, see:

- [HTTP Client](references/http-client.md) - Comprehensive guide to Dio setup, interceptors, and advanced features
- [REST API Integration](references/rest-api.md) - CRUD operations, authentication, and error handling
- [GraphQL Integration](references/graphql-integration.md) - Queries, mutations, subscriptions, and caching
- [WebSocket Communication](references/websockets.md) - Real-time bidirectional communication patterns
- [JSON Serialization](references/json-serialization.md) - Code generation with json_serializable and freezed
- [Error Handling](references/error-handling.md) - Exception types, retry strategies, and offline handling

## Examples

Complete, production-ready examples:

- [API Client Implementation](examples/api-client.md) - Full-featured API client with authentication, error handling, and interceptors
- [Offline-First Data Sync](examples/offline-sync.md) - Complete offline-first implementation with conflict resolution

## Quick Reference

### Adding Dependencies

```yaml
dependencies:
  dio: ^5.4.0
  graphql_flutter: ^5.1.0
  web_socket_channel: ^2.4.0
  json_annotation: ^4.8.1
  freezed_annotation: ^2.4.1

dev_dependencies:
  build_runner: ^2.4.7
  json_serializable: ^6.7.1
  freezed: ^2.4.6
```

### Basic GET Request

```dart
final dio = Dio();
final response = await dio.get('https://api.example.com/users');
final users = (response.data as List)
    .map((json) => User.fromJson(json))
    .toList();
```

### GraphQL Query

```dart
Query(
  options: QueryOptions(
    document: gql('''
      query GetUser(\$id: ID!) {
        user(id: \$id) { id name email }
      }
    '''),
    variables: {'id': userId},
  ),
  builder: (result, {fetchMore, refetch}) {
    if (result.isLoading) return CircularProgressIndicator();
    if (result.hasException) return Text('Error: ${result.exception}');
    return UserWidget(user: result.data['user']);
  },
)
```

### WebSocket Connection

```dart
final channel = WebSocketChannel.connect(
  Uri.parse('wss://api.example.com/ws'),
);

// Listen to messages
channel.stream.listen((message) {
  print('Received: $message');
});

// Send messages
channel.sink.add('Hello, server!');
```

### JSON Serializable Model

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) =>
      _$UserFromJson(json);
}
```

## Common Pitfalls

- **Forgetting Platform Permissions**: Android requires INTERNET permission, macOS requires network client entitlement
- **Not Handling Errors**: Always wrap network calls in try-catch blocks
- **Blocking UI Thread**: Never parse large JSON on the main thread, use compute() for heavy parsing
- **Memory Leaks**: Always dispose WebSocket channels and cancel Dio requests when widgets are disposed
- **Missing Timeouts**: Set reasonable timeout values to prevent hanging requests
- **Over-Fetching**: Use pagination and lazy loading for large datasets
- **Insecure Storage**: Never store tokens in SharedPreferences, use flutter_secure_storage
- **Missing Content-Type**: Always set Content-Type header for POST/PUT requests
- **Not Testing Offline**: Test your app's behavior with airplane mode enabled

## Conclusion

Mastering networking in Flutter requires understanding multiple technologies: HTTP clients, REST APIs, GraphQL, WebSockets, and JSON serialization. Each serves specific use cases, and production applications typically combine several approaches.

Start with Dio for HTTP requests, implement proper error handling and retry logic, and add offline support through the repository pattern. Use code generation for JSON serialization to eliminate boilerplate and prevent runtime errors. For real-time features, integrate WebSockets or GraphQL subscriptions.

Following the patterns and practices outlined in this skill will help you build robust, performant, and user-friendly Flutter applications that handle networking gracefully under all conditions.
