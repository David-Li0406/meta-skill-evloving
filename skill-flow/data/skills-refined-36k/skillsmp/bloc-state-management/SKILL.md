---
name: bloc-state-management
description: Expert Bloc/Cubit state management implementation for Flutter apps. Use when implementing state management with flutter_bloc, bloc library, Cubit pattern, or BLoC pattern. Covers events, states, business logic separation, reactive programming with streams, testing, and modern Bloc 9.x+ patterns with latest features.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Bloc State Management Skill

Expert assistance for implementing state management using the Bloc/Cubit pattern in Flutter applications.

## When to Use This Skill

- Setting up Bloc/Cubit in a Flutter project
- Creating Blocs and Cubits for state management
- Implementing events and states
- Managing complex business logic with Bloc pattern
- Handling async operations and data fetching
- Implementing form validation with Bloc
- Testing Blocs and Cubits
- Using Bloc observers and transformers
- Optimizing Bloc performance
- Migrating between Bloc versions

## Setup

### Dependencies
```yaml
dependencies:
  flutter_bloc: ^9.0.0
  equatable: ^2.0.5  # For value equality

dev_dependencies:
  bloc_test: ^10.0.0
  mocktail: ^1.0.0
```

### Project Setup
```bash
# Add dependencies
flutter pub add flutter_bloc equatable
flutter pub add --dev bloc_test mocktail
```

### App Configuration
```dart
import 'package:flutter_bloc/flutter_bloc.dart';

void main() {
  // Optional: Global Bloc observer
  Bloc.observer = AppBlocObserver();

  runApp(const MyApp());
}

// Bloc Observer for debugging
class AppBlocObserver extends BlocObserver {
  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    print('${bloc.runtimeType} $change');
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    print('${bloc.runtimeType} $error $stackTrace');
    super.onError(bloc, error, stackTrace);
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    super.onTransition(bloc, transition);
    print('${bloc.runtimeType} $transition');
  }

  @override
  void onEvent(Bloc bloc, Object? event) {
    super.onEvent(bloc, event);
    print('${bloc.runtimeType} $event');
  }
}
```

## Core Concepts

### Cubit vs Bloc

| Feature | Cubit | Bloc |
|---------|-------|------|
| Complexity | Simple | Complex |
| Input | Methods | Events |
| Best for | Simple state | Complex business logic |
| Testability | Easy | Very structured |
| Boilerplate | Less | More |
| Traceability | Good | Excellent |

**Rule of thumb:** Use Cubit for simple state, Bloc for complex logic with clear events.

## Cubit Pattern (Simple State Management)

### Basic Cubit

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// Simple state (can be primitive or class)
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
  void reset() => emit(0);
}

// In widget
BlocProvider(
  create: (context) => CounterCubit(),
  child: CounterView(),
)
```

### Cubit with Complex State

```dart
import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// State class
class TodoState extends Equatable {
  const TodoState({
    this.todos = const [],
    this.isLoading = false,
    this.error,
  });

  final List<Todo> todos;
  final bool isLoading;
  final String? error;

  TodoState copyWith({
    List<Todo>? todos,
    bool? isLoading,
    String? error,
  }) {
    return TodoState(
      todos: todos ?? this.todos,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }

  @override
  List<Object?> get props => [todos, isLoading, error];
}

// Cubit
class TodoCubit extends Cubit<TodoState> {
  TodoCubit(this._repository) : super(const TodoState());

  final TodoRepository _repository;

  Future<void> loadTodos() async {
    emit(state.copyWith(isLoading: true, error: null));

    try {
      final todos = await _repository.fetchTodos();
      emit(state.copyWith(todos: todos, isLoading: false));
    } catch (e) {
      emit(state.copyWith(
        isLoading: false,
        error: e.toString(),
      ));
    }
  }

  Future<void> addTodo(String title) async {
    try {
      final newTodo = await _repository.addTodo(title);
      emit(state.copyWith(
        todos: [...state.todos, newTodo],
      ));
    } catch (e) {
      emit(state.copyWith(error: e.toString()));
    }
  }

  void removeTodo(String id) {
    emit(state.copyWith(
      todos: state.todos.where((todo) => todo.id != id).toList(),
    ));
  }

  @override
  Future<void> close() {
    // Cleanup if needed
    return super.close();
  }
}
```

## Bloc Pattern (Event-Driven State Management)

### Complete Bloc Example

```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

// Events
abstract class TodoEvent extends Equatable {
  const TodoEvent();

  @override
  List<Object?> get props => [];
}

class TodoLoadRequested extends TodoEvent {
  const TodoLoadRequested();
}

class TodoAdded extends TodoEvent {
  const TodoAdded(this.title);

  final String title;

  @override
  List<Object?> get props => [title];
}

class TodoDeleted extends TodoEvent {
  const TodoDeleted(this.id);

  final String id;

  @override
  List<Object?> get props => [id];
}

class TodoToggled extends TodoEvent {
  const TodoToggled(this.id);

  final String id;

  @override
  List<Object?> get props => [id];
}

// States
abstract class TodoState extends Equatable {
  const TodoState();

  @override
  List<Object?> get props => [];
}

class TodoInitial extends TodoState {
  const TodoInitial();
}

class TodoLoadInProgress extends TodoState {
  const TodoLoadInProgress();
}

class TodoLoadSuccess extends TodoState {
  const TodoLoadSuccess(this.todos);

  final List<Todo> todos;

  @override
  List<Object?> get props => [todos];
}

class TodoLoadFailure extends TodoState {
  const TodoLoadFailure(this.error);

  final String error;

  @override
  List<Object?> get props => [error];
}

// Bloc
class TodoBloc extends Bloc<TodoEvent, TodoState> {
  TodoBloc(this._repository) : super(const TodoInitial()) {
    on<TodoLoadRequested>(_onLoadRequested);
    on<TodoAdded>(_onAdded);
    on<TodoDeleted>(_onDeleted);
    on<TodoToggled>(_onToggled);
  }

  final TodoRepository _repository;

  Future<void> _onLoadRequested(
    TodoLoadRequested event,
    Emitter<TodoState> emit,
  ) async {
    emit(const TodoLoadInProgress());

    try {
      final todos = await _repository.fetchTodos();
      emit(TodoLoadSuccess(todos));
    } catch (e) {
      emit(TodoLoadFailure(e.toString()));
    }
  }

  Future<void> _onAdded(
    TodoAdded event,
    Emitter<TodoState> emit,
  ) async {
    if (state is TodoLoadSuccess) {
      try {
        final newTodo = await _repository.addTodo(event.title);
        final currentState = state as TodoLoadSuccess;
        emit(TodoLoadSuccess([...currentState.todos, newTodo]));
      } catch (e) {
        emit(TodoLoadFailure(e.toString()));
      }
    }
  }

  void _onDeleted(
    TodoDeleted event,
    Emitter<TodoState> emit,
  ) {
    if (state is TodoLoadSuccess) {
      final currentState = state as TodoLoadSuccess;
      emit(TodoLoadSuccess(
        currentState.todos.where((todo) => todo.id != event.id).toList(),
      ));
    }
  }

  void _onToggled(
    TodoToggled event,
    Emitter<TodoState> emit,
  ) {
    if (state is TodoLoadSuccess) {
      final currentState = state as TodoLoadSuccess;
      emit(TodoLoadSuccess(
        currentState.todos.map((todo) {
          return todo.id == event.id
              ? todo.copyWith(completed: !todo.completed)
              : todo;
        }).toList(),
      ));
    }
  }

  @override
  Future<void> close() {
    // Cleanup
    return super.close();
  }
}
```

## Widget Integration

### BlocProvider (Single Bloc)

```dart
BlocProvider(
  create: (context) => TodoCubit(
    context.read<TodoRepository>(),
  )..loadTodos(),  // Can call methods immediately
  child: const TodoView(),
)
```

### MultiBlocProvider (Multiple Blocs)

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(create: (context) => AuthBloc()),
    BlocProvider(create: (context) => TodoBloc()),
    BlocProvider(create: (context) => SettingsBloc()),
  ],
  child: const MyApp(),
)
```

### BlocBuilder (Rebuild on State Change)

```dart
BlocBuilder<TodoCubit, TodoState>(
  builder: (context, state) {
    if (state.isLoading) {
      return const CircularProgressIndicator();
    }

    if (state.error != null) {
      return Text('Error: ${state.error}');
    }

    return ListView.builder(
      itemCount: state.todos.length,
      itemBuilder: (context, index) {
        return TodoItem(todo: state.todos[index]);
      },
    );
  },
)

// With buildWhen for optimization
BlocBuilder<CounterCubit, int>(
  buildWhen: (previous, current) => previous != current,
  builder: (context, state) => Text('$state'),
)
```

### BlocSelector (Rebuild on Specific Property)

```dart
// Only rebuilds when name changes, not entire user state
BlocSelector<UserCubit, UserState, String>(
  selector: (state) => state.name,
  builder: (context, name) => Text(name),
)
```

### BlocListener (Side Effects)

```dart
BlocListener<TodoBloc, TodoState>(
  listener: (context, state) {
    if (state is TodoLoadFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.error)),
      );
    }
  },
  child: const TodoView(),
)

// Listen to specific events
BlocListener<TodoBloc, TodoState>(
  listenWhen: (previous, current) {
    return previous is TodoLoadInProgress &&
           current is TodoLoadSuccess;
  },
  listener: (context, state) {
    // Show success message
  },
  child: const TodoView(),
)
```

### BlocConsumer (Builder + Listener)

```dart
BlocConsumer<TodoBloc, TodoState>(
  listener: (context, state) {
    if (state is TodoLoadFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.error)),
      );
    }
  },
  builder: (context, state) {
    if (state is TodoLoadInProgress) {
      return const CircularProgressIndicator();
    }

    if (state is TodoLoadSuccess) {
      return TodoList(todos: state.todos);
    }

    return const SizedBox();
  },
)
```

### Reading/Dispatching Events

```dart
// Read Cubit/Bloc instance (doesn't rebuild)
context.read<TodoCubit>().addTodo('New Todo');

// Watch state (rebuilds on change)
final state = context.watch<TodoCubit>().state;

// Select specific property
final count = context.select(
  (TodoCubit cubit) => cubit.state.todos.length,
);

// For Bloc: dispatch events
context.read<TodoBloc>().add(const TodoAdded('New Todo'));
```

## Advanced Patterns

### Bloc Transformers (Event Processing)

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';
import 'package:stream_transform/stream_transform.dart';

class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc() : super(const SearchState()) {
    // Debounce search events
    on<SearchQueryChanged>(
      _onQueryChanged,
      transformer: debounce(const Duration(milliseconds: 300)),
    );

    // Sequential processing
    on<DataLoadRequested>(
      _onDataLoadRequested,
      transformer: sequential(),
    );

    // Concurrent processing
    on<DataRefreshRequested>(
      _onDataRefreshRequested,
      transformer: concurrent(),
    );

    // Drop previous events
    on<ButtonPressed>(
      _onButtonPressed,
      transformer: droppable(),
    );

    // Restart on new event
    on<InputChanged>(
      _onInputChanged,
      transformer: restartable(),
    );
  }
}

// Custom debounce transformer
EventTransformer<E> debounce<E>(Duration duration) {
  return (events, mapper) => events.debounce(duration).switchMap(mapper);
}
```

### Bloc Communication

```dart
// Bloc listening to another Bloc
class DependentBloc extends Bloc<DependentEvent, DependentState> {
  DependentBloc(this._authBloc) : super(DependentInitial()) {
    _authSubscription = _authBloc.stream.listen((authState) {
      if (authState is Authenticated) {
        add(const DataLoadRequested());
      } else if (authState is Unauthenticated) {
        add(const DataCleared());
      }
    });

    on<DataLoadRequested>(_onDataLoadRequested);
    on<DataCleared>(_onDataCleared);
  }

  final AuthBloc _authBloc;
  late StreamSubscription _authSubscription;

  @override
  Future<void> close() {
    _authSubscription.cancel();
    return super.close();
  }
}
```

### Hydrated Bloc (Persistence)

```dart
// Add dependency: hydrated_bloc: ^9.1.2

import 'package:hydrated_bloc/hydrated_bloc.dart';
import 'package:path_provider/path_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  HydratedBloc.storage = await HydratedStorage.build(
    storageDirectory: await getApplicationDocumentsDirectory(),
  );

  runApp(const MyApp());
}

// Hydrated Cubit
class CounterCubit extends HydratedCubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);

  @override
  int? fromJson(Map<String, dynamic> json) => json['value'] as int?;

  @override
  Map<String, dynamic>? toJson(int state) => {'value': state};
}
```

## Testing

### Cubit Testing

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockTodoRepository extends Mock implements TodoRepository {}

void main() {
  group('TodoCubit', () {
    late TodoRepository repository;

    setUp(() {
      repository = MockTodoRepository();
    });

    test('initial state is TodoState()', () {
      expect(
        TodoCubit(repository).state,
        equals(const TodoState()),
      );
    });

    blocTest<TodoCubit, TodoState>(
      'emits loading and success when loadTodos succeeds',
      build: () {
        when(() => repository.fetchTodos())
            .thenAnswer((_) async => [Todo(id: '1', title: 'Test')]);
        return TodoCubit(repository);
      },
      act: (cubit) => cubit.loadTodos(),
      expect: () => [
        const TodoState(isLoading: true),
        TodoState(
          isLoading: false,
          todos: [Todo(id: '1', title: 'Test')],
        ),
      ],
    );

    blocTest<TodoCubit, TodoState>(
      'emits loading and failure when loadTodos fails',
      build: () {
        when(() => repository.fetchTodos())
            .thenThrow(Exception('Failed'));
        return TodoCubit(repository);
      },
      act: (cubit) => cubit.loadTodos(),
      expect: () => [
        const TodoState(isLoading: true),
        const TodoState(
          isLoading: false,
          error: 'Exception: Failed',
        ),
      ],
    );
  });
}
```

### Bloc Testing

```dart
void main() {
  group('TodoBloc', () {
    late TodoRepository repository;

    setUp(() {
      repository = MockTodoRepository();
    });

    test('initial state is TodoInitial', () {
      expect(TodoBloc(repository).state, equals(const TodoInitial()));
    });

    blocTest<TodoBloc, TodoState>(
      'emits [TodoLoadInProgress, TodoLoadSuccess] when load succeeds',
      build: () {
        when(() => repository.fetchTodos())
            .thenAnswer((_) async => [Todo(id: '1', title: 'Test')]);
        return TodoBloc(repository);
      },
      act: (bloc) => bloc.add(const TodoLoadRequested()),
      expect: () => [
        const TodoLoadInProgress(),
        TodoLoadSuccess([Todo(id: '1', title: 'Test')]),
      ],
    );

    blocTest<TodoBloc, TodoState>(
      'emits [TodoLoadInProgress, TodoLoadFailure] when load fails',
      build: () {
        when(() => repository.fetchTodos())
            .thenThrow(Exception('Failed'));
        return TodoBloc(repository);
      },
      act: (bloc) => bloc.add(const TodoLoadRequested()),
      expect: () => [
        const TodoLoadInProgress(),
        const TodoLoadFailure('Exception: Failed'),
      ],
    );

    blocTest<TodoBloc, TodoState>(
      'emits updated list when todo added',
      build: () {
        when(() => repository.fetchTodos())
            .thenAnswer((_) async => []);
        when(() => repository.addTodo(any()))
            .thenAnswer((_) async => Todo(id: '1', title: 'New'));
        return TodoBloc(repository)..add(const TodoLoadRequested());
      },
      seed: () => const TodoLoadSuccess([]),
      act: (bloc) => bloc.add(const TodoAdded('New')),
      expect: () => [
        TodoLoadSuccess([Todo(id: '1', title: 'New')]),
      ],
    );
  });
}
```

### Widget Testing with Bloc

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';

class MockTodoBloc extends MockBloc<TodoEvent, TodoState>
    implements TodoBloc {}

void main() {
  late TodoBloc todoBloc;

  setUp(() {
    todoBloc = MockTodoBloc();
  });

  testWidgets('renders loading indicator when loading', (tester) async {
    when(() => todoBloc.state).thenReturn(const TodoLoadInProgress());

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider.value(
          value: todoBloc,
          child: const TodoView(),
        ),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('renders todos when loaded', (tester) async {
    when(() => todoBloc.state).thenReturn(
      TodoLoadSuccess([
        Todo(id: '1', title: 'Test Todo'),
      ]),
    );

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider.value(
          value: todoBloc,
          child: const TodoView(),
        ),
      ),
    );

    expect(find.text('Test Todo'), findsOneWidget);
  });
}
```

## Project Structure

```
lib/
├── core/
│   ├── blocs/           # Shared blocs (auth, theme, etc.)
│   └── utils/
├── features/
│   └── todos/
│       ├── data/
│       │   ├── models/
│       │   └── repositories/
│       ├── domain/
│       │   └── entities/
│       └── presentation/
│           ├── blocs/    # Feature-specific blocs/cubits
│           │   └── todo/
│           │       ├── todo_bloc.dart
│           │       ├── todo_event.dart
│           │       └── todo_state.dart
│           ├── pages/
│           └── widgets/
└── main.dart
```

## Common Patterns

### Form Validation Bloc

```dart
class LoginFormCubit extends Cubit<LoginFormState> {
  LoginFormCubit() : super(const LoginFormState());

  void emailChanged(String email) {
    final emailError = _validateEmail(email);
    emit(state.copyWith(
      email: email,
      emailError: emailError,
    ));
  }

  void passwordChanged(String password) {
    final passwordError = _validatePassword(password);
    emit(state.copyWith(
      password: password,
      passwordError: passwordError,
    ));
  }

  Future<void> submit() async {
    if (!state.isValid) return;

    emit(state.copyWith(status: FormStatus.submitting));

    try {
      await _authRepository.login(state.email, state.password);
      emit(state.copyWith(status: FormStatus.success));
    } catch (e) {
      emit(state.copyWith(
        status: FormStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  String? _validateEmail(String email) {
    if (email.isEmpty) return 'Email is required';
    if (!email.contains('@')) return 'Invalid email';
    return null;
  }

  String? _validatePassword(String password) {
    if (password.isEmpty) return 'Password is required';
    if (password.length < 6) return 'Password too short';
    return null;
  }
}
```

### Pagination Bloc

```dart
class PostListBloc extends Bloc<PostListEvent, PostListState> {
  PostListBloc(this._repository) : super(const PostListState()) {
    on<PostListLoadRequested>(_onLoadRequested);
    on<PostListLoadMore>(_onLoadMore);
  }

  final PostRepository _repository;
  static const _pageSize = 20;

  Future<void> _onLoadRequested(
    PostListLoadRequested event,
    Emitter<PostListState> emit,
  ) async {
    emit(state.copyWith(status: PostListStatus.loading));

    try {
      final posts = await _repository.fetchPosts(0, _pageSize);
      emit(state.copyWith(
        status: PostListStatus.success,
        posts: posts,
        hasMore: posts.length >= _pageSize,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: PostListStatus.failure,
        error: e.toString(),
      ));
    }
  }

  Future<void> _onLoadMore(
    PostListLoadMore event,
    Emitter<PostListState> emit,
  ) async {
    if (!state.hasMore || state.isLoadingMore) return;

    emit(state.copyWith(isLoadingMore: true));

    try {
      final posts = await _repository.fetchPosts(
        state.posts.length,
        _pageSize,
      );

      emit(state.copyWith(
        posts: [...state.posts, ...posts],
        hasMore: posts.length >= _pageSize,
        isLoadingMore: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        isLoadingMore: false,
        error: e.toString(),
      ));
    }
  }
}
```

## Best Practices

- **Use Cubit for simple state**, Bloc for complex event-driven logic
- **Use Equatable** for automatic value comparison
- **Separate events, states, and bloc** into different files for clarity
- **Use sealed classes or freezed** for exhaustive state matching
- **Name events in past tense** (UserLoggedIn, DataLoadRequested)
- **Name states descriptively** (Loading, Success, Failure)
- **Use BlocObserver** for debugging and logging
- **Test blocs thoroughly** with bloc_test
- **Use event transformers** to control event processing
- **Avoid accessing BuildContext in Blocs** (pass data through events)
- **Close blocs properly** to prevent memory leaks
- **Use BlocProvider.value** only for existing instances
- **Use BlocSelector** to optimize rebuilds
- **Keep business logic in Blocs**, not in widgets
- **Use repositories** for data access, not directly in Blocs

## Common Issues

### Issue: BlocProvider.of() called with no matching provider
**Solution:** Wrap widget with BlocProvider
```dart
BlocProvider(
  create: (context) => TodoBloc(),
  child: const TodoView(),
)
```

### Issue: Bloc is not updating UI
**Solution:** Ensure states are properly compared (use Equatable)
```dart
class TodoState extends Equatable {
  @override
  List<Object?> get props => [todos, isLoading];
}
```

### Issue: Memory leak
**Solution:** Close blocs and cancel subscriptions
```dart
@override
Future<void> close() {
  _subscription.cancel();
  return super.close();
}
```

### Issue: Cannot emit new states after close
**Solution:** Check if closed before emitting
```dart
if (!isClosed) {
  emit(newState);
}
```

## Resources

- **Official Docs:** https://bloclibrary.dev
- **Examples:** https://github.com/felangel/bloc/tree/master/examples
- **Bloc Extension:** VS Code and IntelliJ extensions for code generation
- **Bloc Architecture:** https://bloclibrary.dev/#/architecture

## Notes

This skill focuses on Bloc/Cubit patterns. For Flutter-specific UI patterns, use the flutter-developer skill. For alternative state management, see the riverpod-state-management skill. Consider using code generation tools like freezed for immutable state classes.
