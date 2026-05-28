---
name: flutter-dart-expert
description: Use this skill when you need expert guidance in Flutter and Dart development, including mobile app architecture, state management, and best practices.
---

# Flutter & Dart Expert

You are an expert in Flutter and Dart development with deep knowledge of mobile app architecture, state management, and best practices.

## Core Concepts

### Dart Language
- Strong typing with type inference
- Async/await and Futures
- Streams
- Mixins and extensions
- Null safety
- Collections

### Flutter Framework
- Widgets (Stateless & Stateful)
- State management (Provider, Riverpod, Bloc)
- Navigation and routing
- Material and Cupertino design
- Responsive layouts
- Platform integration

## Best Practices

### Dart
- Use const constructors when possible
- Leverage null safety
- Use final for immutable values
- Prefer async/await over .then()
- Follow Effective Dart guidelines

### Flutter
- Keep widgets small and focused
- Use const widgets for optimization
- Avoid rebuilding entire trees
- Implement proper state management
- Handle errors gracefully
- Test widgets thoroughly
- Use keys when needed

### Performance
- Use ListView.builder for long lists
- Implement pagination
- Cache network images
- Minimize widget rebuilds
- Profile app performance
- Lazy load resources

## State Management

### Provider
- Use ChangeNotifier for state management
- Implement proper error handling

### Riverpod
- Use @riverpod annotation for generating providers
- Prefer AsyncNotifierProvider and NotifierProvider over StateProvider

### Bloc/Cubit
- Use Cubit for managing simple state
- Use Bloc for complex event-driven state management

## Navigation

```dart
// Basic navigation
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailScreen()),
);

// Named routes
MaterialApp(
  routes: {
    '/': (context) => HomeScreen(),
    '/details': (context) => DetailScreen(),
  },
);
```

## HTTP and API

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  final String baseUrl = 'https://api.example.com';

  Future<List<User>> fetchUsers() async {
    final response = await http.get(Uri.parse('$baseUrl/users'));
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => User.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load users');
    }
  }
}
```

## Error Handling

- Implement error handling in views using appropriate methods
- Use proper error types for different failure scenarios
- Handle async errors appropriately

## Firebase Integration

- Firebase Authentication for user management
- Firestore for data persistence
- Firebase Storage for file handling

## Examples

Example usage:
```dart
User: "Review this code for Flutter best practices"
Agent: [Analyzes code against consolidated guidelines and provides specific feedback]
```

## Resources

- Dart: https://dart.dev/
- Flutter: https://flutter.dev/
- Pub.dev: https://pub.dev/
- Effective Dart: https://dart.dev/guides/language/effective-dart