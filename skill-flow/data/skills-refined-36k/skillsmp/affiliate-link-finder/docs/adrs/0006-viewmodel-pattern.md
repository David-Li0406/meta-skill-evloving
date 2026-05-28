# ADR 0006: ViewModel Pattern for State Management

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The application has 32 screens with varying data requirements. Initial wireframes used hardcoded mock data (`bool isMagnesiumTaken = true`). We needed a scalable state management pattern that:
- Separates UI from business logic
- Supports real-time data updates from Firestore
- Allows dependency injection for testing
- Handles loading/error states consistently

## Decision

Adopt the **ViewModel pattern** with `ChangeNotifier` from Flutter's Provider package.

### Architecture

```
UI (Screens) → ViewModels (ChangeNotifier) → Repositories (interfaces) → Firebase
```

### Implementation

```dart
class DailyStackViewModel extends ChangeNotifier {
  final StackRepository _stackRepository;
  final LogRepository _logRepository;
  
  List<SupplementStack> _stacks = [];
  bool _isLoading = false;
  String? _error;
  
  Future<void> initialize() async {
    _isLoading = true;
    notifyListeners();
    // Load data...
  }
}
```

### DI Registration (get_it)

```dart
locator.registerFactoryParam<DailyStackViewModel, String, void>(
  (userId, _) => DailyStackViewModel(
    stackRepository: locator<StackRepository>(),
    logRepository: locator<LogRepository>(),
    userId: userId,
  ),
);
```

## Consequences

**Positive:**
- Clear separation of concerns
- Easy to unit test ViewModels
- Consistent loading/error handling
- User-scoped state with `registerFactoryParam`

**Negative:**
- Slightly more boilerplate than direct setState
- Must manually dispose ViewModels

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Riverpod | Additional dependency complexity |
| BLoC | Overkill for current app scale |
| GetX | Less explicit dependency injection |
