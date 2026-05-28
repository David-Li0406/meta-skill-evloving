---
name: flutter-dart-expert
description: Use this skill when you need expert guidance in Flutter and Dart development, including best practices for mobile app architecture, state management, and performance optimization.
---

# Skill body

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
- Follow PascalCase for classes and camelCase for variables, functions, and methods.
- Write short functions with a single purpose (less than 20 instructions).
- Avoid deeply nested widget trees.
- Use const constructors wherever possible.
- Implement clean architecture principles with repository pattern.

## State Management
### Riverpod
- Use @riverpod annotation for generating providers.
- Prefer AsyncNotifierProvider and NotifierProvider over StateProvider.
- Use Freezed for immutable state classes.

### Bloc/Cubit
- Use Cubit for managing simple state.
- Use Bloc for complex event-driven state management.
- Implement error handling properly in state classes.

## Error Handling
- Implement error handling in views using SelectableText.rich instead of SnackBars.
- Use proper error types for different failure scenarios.
- Handle async errors appropriately.

## Performance Optimization
- Use const widgets to prevent unnecessary rebuilds.
- Implement lazy loading for lists.
- Optimize images and assets.
- Profile and optimize widget rebuilds.

## Testing
- Write unit tests for business logic.
- Widget tests for UI components.
- Integration tests for full app flows.
- Follow official Flutter testing documentation.

## Example Code Snippets

### Dart Fundamentals
```dart
// Variables and types
var name = 'John';  // Type inference
String explicitType = 'Explicit';
final constantValue = 42;  // Runtime constant
const compileConstant = 'Compile-time';

// Null safety
String? nullableString;
String nonNullable = 'Never null';

// Functions
int add(int a, int b) => a + b;
```

### Flutter Widget Example
```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text('Hello, Flutter!'),
    );
  }
}
```

### Async Programming
```dart
import 'dart:async';

Future<String> fetchUser(String id) async {
  await Future.delayed(Duration(seconds: 1));
  return 'User $id';
}
```