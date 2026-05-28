---
name: flutter-bloc-state-management
description: Use this skill for implementing predictable state management in Flutter applications using flutter_bloc, freezed, and equatable.
---

# BLoC State Management

## **Priority: P0 (CRITICAL)**

Implement predictable state management that separates business logic from UI using `flutter_bloc`, `freezed`, or `equatable`.

## Structure

```text
lib/features/auth/
├── bloc/
│   ├── auth_bloc.dart
│   ├── auth_event.dart # (@freezed or Equatable)
│   └── auth_state.dart # (@freezed or Equatable)
```

## Implementation Guidelines

- **States & Events**: Default to using `@freezed` for union states. Use `Equatable` if the library is present in `pubspec.yaml`.
  - **freezed**: Ideal for union states (initial, loading, success) and automatic `copyWith`.
  - **Equatable**: Use if avoiding code generation or if `equatable` is the only comparison library.
  - Choose strategy:
    - **Union State**: For exclusive UI phases (loading vs data).
    - **Property-based State**: For complex forms (Option<$Either>, flags).
- **State Properties**: Utilize enums, sealed classes, or `Status` objects.
- **Error Handling**: Implement `Failure` objects; avoid throwing exceptions.
- **Async Data**: Use `emit.forEach` or `emit.onEach` for streams.
- **Concurrency**: Apply `transformer` for event debouncing (restartable, droppable).
- **Testing**: Utilize `blocTest` for verifying state transitions.
- **Injection**: Register BLoCs as `@injectable` (Factory).

## Anti-Patterns

- **No Manual Emit**: Avoid calling `emit()` inside `Future.then`; always use `await` or `emit.forEach`.
- **No UI Logic**: Do not perform calculations or data formatting inside `BlocBuilder`.
- **No Cross-Bloc Reference**: Do not pass a BLoC instance into another BLoC; use streams or the UI layer for coordination.

## Related Topics

layer-based-clean-architecture | feature-based-clean-architecture | dependency-injection | error-handling