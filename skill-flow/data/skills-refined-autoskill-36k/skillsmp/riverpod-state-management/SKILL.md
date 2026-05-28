---
name: riverpod-state-management
description: Expert Riverpod state management implementation for Flutter apps. Use when implementing state management with Riverpod, flutter_riverpod, hooks_riverpod, or riverpod_annotation. Covers providers, code generation, dependency injection, async data handling, and modern Riverpod 3.x+ patterns with latest features.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Riverpod State Management Skill

Expert assistance for implementing state management using Riverpod in Flutter applications.

## When to Use This Skill

- Setting up Riverpod in a Flutter project
- Creating and using providers (Provider, StateProvider, FutureProvider, StreamProvider, etc.)
- Implementing dependency injection with Riverpod
- Using Riverpod code generation with riverpod_generator
- Managing async state and data fetching
- Testing Riverpod providers
- Migrating from Provider to Riverpod
- Implementing complex state logic with StateNotifier or Notifier
- Using Riverpod with hooks (hooks_riverpod)

## Setup

### Dependencies
```yaml
dependencies:
  flutter_riverpod: ^3.0.0
  # OR for hooks support
  hooks_riverpod: ^3.0.0

dev_dependencies:
  riverpod_annotation: ^3.0.0
  build_runner: ^2.4.0
  riverpod_generator: ^3.0.0
  riverpod_lint: ^3.0.0
```

### Project Setup
```bash
# Add dependencies
flutter pub add flutter_riverpod
flutter pub add --dev riverpod_annotation build_runner riverpod_generator

# For code generation
flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode for development
flutter pub run build_runner watch --delete-conflicting-outputs
```

### App Configuration
```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    const ProviderScope(  // Required root widget
      child: MyApp(),
    ),
  );
}
```

## Core Concepts

### Provider Types Overview

| Provider Type | Use Case | Example |
|--------------|----------|---------|
| `Provider` | Immutable values, DI | Configuration, services |
| `StateProvider` | Simple state (primitive) | Counter, toggle |
| `FutureProvider` | Async data (one-time) | API call, file read |
| `StreamProvider` | Async stream | WebSocket, Firebase |
| `StateNotifierProvider` | Complex state | Form, list management |
| `NotifierProvider` | Modern complex state | Recommended for new code |
| `AsyncNotifierProvider` | Async complex state | Data with loading/error |

## Modern Patterns (Riverpod 3.x+)

### Code Generation Approach (Recommended)

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'counter.g.dart';

// Simple provider
@riverpod
int counter(CounterRef ref) {
  return 0;
}

// Async provider
@riverpod
Future<User> user(UserRef ref, String userId) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.fetchUser(userId);
}

// Family provider (parameterized)
@riverpod
Future<Post> post(PostRef ref, String postId) async {
  final repository = ref.watch(postRepositoryProvider);
  return repository.fetchPost(postId);
}

// Stateful provider (Notifier)
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
  void reset() => state = 0;
}

// Async Notifier
@riverpod
class UserList extends _$UserList {
  @override
  Future<List<User>> build() async {
    return _fetchUsers();
  }

  Future<void> addUser(User user) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final users = await _fetchUsers();
      return [...users, user];
    });
  }

  Future<List<User>> _fetchUsers() async {
    final repository = ref.read(userRepositoryProvider);
    return repository.fetchUsers();
  }
}
```

### Manual Approach (Legacy but still valid)

```dart
// Simple provider
final counterProvider = Provider<int>((ref) => 0);

// State provider
final counterStateProvider = StateProvider<int>((ref) => 0);

// Future provider
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.fetchUser(userId);
});

// StateNotifier
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
}

final counterNotifierProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

// Notifier (Modern)
class Counter extends Notifier<int> {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
}

final counterNotifierProvider = NotifierProvider<Counter, int>(Counter.new);
```

## Consuming Providers

### In Widgets

```dart
// ConsumerWidget (recommended)
class CounterWidget extends ConsumerWidget {
  const CounterWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).increment(),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}

// Consumer (for part of widget tree)
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer(
      builder: (context, ref, child) {
        final count = ref.watch(counterProvider);
        return Text('Count: $count');
      },
    );
  }
}

// ConsumerStatefulWidget
class CounterPage extends ConsumerStatefulWidget {
  const CounterPage({super.key});

  @override
  ConsumerState<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends ConsumerState<CounterPage> {
  @override
  void initState() {
    super.initState();
    // Can use ref here
    ref.read(counterProvider);
  }

  @override
  Widget build(BuildContext context) {
    final count = ref.watch(counterProvider);
    return Text('Count: $count');
  }
}
```

### Ref Methods

```dart
// Watch: Rebuilds when value changes
final value = ref.watch(provider);

// Read: One-time read, no rebuild
final value = ref.read(provider);

// Listen: Execute side effects on change
ref.listen(provider, (previous, next) {
  if (next.hasError) {
    showErrorSnackBar(context, next.error);
  }
});

// Invalidate: Force provider refresh
ref.invalidate(provider);

// Refresh: Get new value immediately
final newValue = ref.refresh(provider);
```

## Async Data Handling

### AsyncValue Pattern

```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    return _fetchTodos();
  }

  Future<List<Todo>> _fetchTodos() async {
    final repository = ref.read(todoRepositoryProvider);
    return repository.fetchTodos();
  }
}

// In widget
class TodoListWidget extends ConsumerWidget {
  const TodoListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final asyncTodos = ref.watch(todoListProvider);

    return asyncTodos.when(
      data: (todos) => ListView.builder(
        itemCount: todos.length,
        itemBuilder: (context, index) => TodoItem(todo: todos[index]),
      ),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}

// Alternative pattern matching
asyncTodos.when(
  data: (todos) => /* success */,
  loading: () => /* loading */,
  error: (error, stack) => /* error */,
);

// Map for custom handling
asyncTodos.maybeWhen(
  data: (todos) => /* success */,
  orElse: () => const SizedBox(),
);
```

### Manual State Updates

```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    return _fetchTodos();
  }

  Future<void> addTodo(Todo todo) async {
    // Set loading
    state = const AsyncValue.loading();

    // Use AsyncValue.guard to handle errors
    state = await AsyncValue.guard(() async {
      final repository = ref.read(todoRepositoryProvider);
      await repository.addTodo(todo);
      return _fetchTodos();
    });
  }

  // Or handle manually
  Future<void> removeTodo(String id) async {
    final previousState = state;

    state = const AsyncValue.loading();

    try {
      final repository = ref.read(todoRepositoryProvider);
      await repository.removeTodo(id);
      state = AsyncValue.data(await _fetchTodos());
    } catch (error, stackTrace) {
      state = AsyncValue.error(error, stackTrace);
      // Optionally restore previous state
      // state = previousState;
    }
  }

  Future<List<Todo>> _fetchTodos() async {
    final repository = ref.read(todoRepositoryProvider);
    return repository.fetchTodos();
  }
}
```

## Dependency Injection

```dart
// Repository provider
@riverpod
TodoRepository todoRepository(TodoRepositoryRef ref) {
  final client = ref.watch(httpClientProvider);
  return TodoRepository(client);
}

// Service provider depending on repository
@riverpod
class TodoService extends _$TodoService {
  @override
  void build() {}

  Future<void> syncTodos() async {
    final repository = ref.read(todoRepositoryProvider);
    await repository.sync();
    ref.invalidate(todoListProvider);
  }
}

// Using in widget
class SyncButton extends ConsumerWidget {
  const SyncButton({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ElevatedButton(
      onPressed: () => ref.read(todoServiceProvider).syncTodos(),
      child: const Text('Sync'),
    );
  }
}
```

## Advanced Patterns

### Combining Providers

```dart
@riverpod
Future<UserProfile> userProfile(UserProfileRef ref, String userId) async {
  final user = await ref.watch(userProvider(userId).future);
  final settings = await ref.watch(userSettingsProvider(userId).future);

  return UserProfile(
    user: user,
    settings: settings,
  );
}

// Select specific parts
@riverpod
String userName(UserNameRef ref, String userId) {
  return ref.watch(
    userProvider(userId).select((user) => user.name),
  );
}
```

### Provider Scope Override

```dart
// For testing or feature-specific overrides
void main() {
  runApp(
    ProviderScope(
      overrides: [
        todoRepositoryProvider.overrideWith(
          (ref) => MockTodoRepository(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

### Auto-dispose

```dart
// Automatically disposed when no longer watched
@riverpod
Future<Data> data(DataRef ref) async {
  // Auto-disposed by default with code generation

  final link = ref.keepAlive();  // Keep alive

  // Cancel after 30 seconds
  Timer(const Duration(seconds: 30), link.close);

  return fetchData();
}

// Manual approach
final dataProvider = FutureProvider.autoDispose<Data>((ref) async {
  return fetchData();
});
```

### Family Providers (Parameterized)

```dart
// Code generation (automatic)
@riverpod
Future<User> user(UserRef ref, String userId) async {
  return fetchUser(userId);
}

// Manual
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  return fetchUser(userId);
});

// In widget
final user = ref.watch(userProvider('123'));
```

## Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:riverpod/riverpod.dart';

void main() {
  test('Counter increments', () {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    // Initial value
    expect(container.read(counterProvider), 0);

    // Increment
    container.read(counterProvider.notifier).increment();

    // Check new value
    expect(container.read(counterProvider), 1);
  });

  test('Async provider test', () async {
    final container = ProviderContainer(
      overrides: [
        userRepositoryProvider.overrideWith(
          (ref) => MockUserRepository(),
        ),
      ],
    );
    addTearDown(container.dispose);

    final user = await container.read(userProvider('123').future);

    expect(user.id, '123');
  });

  test('Listen to changes', () async {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    final listener = Listener<int>();

    container.listen(
      counterProvider,
      listener.call,
      fireImmediately: true,
    );

    verify(listener.call(null, 0));

    container.read(counterProvider.notifier).increment();

    verify(listener.call(0, 1));
  });
}

class Listener<T> extends Mock {
  void call(T? previous, T next);
}
```

## Project Structure

```
lib/
├── core/
│   ├── providers/         # Core providers (DI, services)
│   └── utils/
├── features/
│   └── todos/
│       ├── data/
│       │   ├── models/
│       │   ├── repositories/
│       │   └── providers/  # Data providers
│       ├── domain/
│       │   └── entities/
│       └── presentation/
│           ├── providers/  # State providers
│           ├── pages/
│           └── widgets/
└── main.dart
```

## Common Patterns

### Repository Pattern
```dart
@riverpod
TodoRepository todoRepository(TodoRepositoryRef ref) {
  return TodoRepositoryImpl();
}

@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() {
    final repository = ref.watch(todoRepositoryProvider);
    return repository.fetchTodos();
  }

  Future<void> addTodo(String title) async {
    final repository = ref.read(todoRepositoryProvider);
    await repository.addTodo(title);
    ref.invalidateSelf();  // Refresh data
  }
}
```

### Form State
```dart
@riverpod
class LoginForm extends _$LoginForm {
  @override
  LoginFormState build() {
    return const LoginFormState();
  }

  void updateEmail(String email) {
    state = state.copyWith(email: email);
  }

  void updatePassword(String password) {
    state = state.copyWith(password: password);
  }

  Future<void> submit() async {
    if (!state.isValid) return;

    state = state.copyWith(isLoading: true);

    try {
      final auth = ref.read(authServiceProvider);
      await auth.login(state.email, state.password);
      state = state.copyWith(isLoading: false, isSuccess: true);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
}

@freezed
class LoginFormState with _$LoginFormState {
  const factory LoginFormState({
    @Default('') String email,
    @Default('') String password,
    @Default(false) bool isLoading,
    @Default(false) bool isSuccess,
    String? error,
  }) = _LoginFormState;

  const LoginFormState._();

  bool get isValid => email.isNotEmpty && password.length >= 6;
}
```

## Migration from Provider

```dart
// Old (Provider)
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }
}

final counterProvider = ChangeNotifierProvider((ref) => CounterProvider());

// New (Riverpod)
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
}
```

## Best Practices

- **Use code generation** for new projects (cleaner syntax, less boilerplate)
- **Prefer Notifier over StateNotifier** for new code
- **Use ConsumerWidget** instead of StatelessWidget for reactive UI
- **Keep providers small and focused** (single responsibility)
- **Use ref.listen** for side effects (navigation, snackbars)
- **Use AsyncValue.guard** for error handling in async operations
- **Override providers in ProviderScope** for testing
- **Use family providers** for parameterized providers
- **Leverage auto-dispose** to prevent memory leaks
- **Use select** to optimize rebuilds (watch only specific fields)
- **Invalidate providers** to refresh data instead of manual updates
- **Separate business logic** from UI (providers should be UI-agnostic)

## Common Issues

### Issue: Provider not found
**Solution:** Ensure ProviderScope wraps your app
```dart
void main() {
  runApp(const ProviderScope(child: MyApp()));
}
```

### Issue: Cannot read provider during build
**Solution:** Use ref.watch instead of ref.read
```dart
// Wrong
final value = ref.read(provider);

// Correct
final value = ref.watch(provider);
```

### Issue: Provider not updating
**Solution:** Check if you're reading instead of watching
```dart
// Use watch for reactive updates
final value = ref.watch(provider);
```

## Resources

- **Official Docs:** https://riverpod.dev
- **Code Generation:** https://riverpod.dev/docs/concepts/about_code_generation
- **Migration Guide:** https://riverpod.dev/docs/migration/from_provider
- **Examples:** https://github.com/rrousselGit/riverpod/tree/master/examples

## Notes

This skill focuses on Riverpod 3.x+ patterns with emphasis on code generation and latest features. For Flutter-specific UI patterns, use the flutter-developer skill. For alternative state management, see the bloc-state-management skill.
