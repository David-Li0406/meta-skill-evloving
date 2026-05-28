---
name: best-practices
description: Flutter performance optimization and clean architecture patterns. This skill should be used when writing, reviewing, or refactoring Flutter/Dart code to ensure optimal performance patterns. Triggers on tasks involving Flutter widgets, state management, async patterns, memory management, or architecture design.
license: MIT
metadata:
  author: devnogari
  project_type: flutter
---

# Flutter Best Practices

Comprehensive performance optimization guide for Flutter applications. Contains 42 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new widgets or screens
- Implementing state management (BLoC, Riverpod, Provider)
- Reviewing code for performance issues
- Refactoring existing Flutter code
- Optimizing build/render performance
- Debugging memory leaks or jank

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Widget Optimization | CRITICAL | `widget-` |
| 2 | State Management | CRITICAL | `state-` |
| 3 | Async Patterns | HIGH | `async-` |
| 4 | Memory Management | HIGH | `mem-` |
| 5 | Rendering Performance | MEDIUM | `render-` |
| 6 | Architecture | MEDIUM | `arch-` |
| 7 | Testing | MEDIUM | `test-` |
| 8 | Platform Integration | LOW | `platform-` |

## Quick Reference

### 1. Widget Optimization (CRITICAL)

- `widget-const` - Use const constructors to prevent unnecessary rebuilds
- `widget-split` - Split widgets to minimize rebuild scope
- `widget-key` - Use keys correctly for widget identity and state preservation
- `widget-builder` - Use Builder widgets to limit rebuild context
- `widget-repaint` - Use RepaintBoundary to isolate expensive paints
- `widget-sliver` - Use Slivers for efficient scrolling lists

### 2. State Management (CRITICAL)

- `state-bloc` - Use BLoC pattern for complex business logic
- `state-riverpod` - Use Riverpod for reactive state with compile-time safety
- `state-provider` - Scope Provider to minimize rebuild area
- `state-consumer` - Use Consumer/BlocBuilder with buildWhen/select
- `state-selector` - Use Selector to watch specific state properties
- `state-rebuild` - Avoid unnecessary setState calls

### 3. Async Patterns (HIGH)

- `async-future-builder` - Handle all FutureBuilder states correctly
- `async-stream` - Use StreamBuilder with proper stream lifecycle
- `async-cancel` - Cancel async operations on widget disposal
- `async-error` - Handle errors with try-catch and error states
- `async-cache` - Cache futures to prevent refetch on rebuild
- `async-isolate` - Use Isolates for heavy computation

### 4. Memory Management (HIGH)

- `mem-dispose` - Always dispose controllers and subscriptions
- `mem-controller` - Dispose TextEditingController, ScrollController, AnimationController
- `mem-subscription` - Cancel StreamSubscriptions in dispose
- `mem-image` - Use cached_network_image and precacheImage
- `mem-cache` - Implement LRU cache for expensive objects
- `mem-leak` - Avoid closures capturing BuildContext across async gaps

### 5. Rendering Performance (MEDIUM)

- `render-boundary` - Use RepaintBoundary for animation isolation
- `render-clip` - Avoid ClipRRect when possible, use decoration instead
- `render-opacity` - Use Opacity sparingly, prefer AnimatedOpacity
- `render-transform` - Use Transform with alignment for GPU acceleration
- `render-list` - Use ListView.builder for long lists
- `render-animation` - Use AnimatedBuilder to limit animation rebuilds

### 6. Architecture (MEDIUM)

- `arch-layer` - Separate presentation, domain, and data layers
- `arch-repository` - Use Repository pattern for data abstraction
- `arch-usecase` - Encapsulate business logic in UseCases
- `arch-entity` - Use immutable Entities with Equatable
- `arch-di` - Use dependency injection (get_it, injectable)
- `arch-router` - Use declarative routing (go_router, auto_route)

### 7. Testing (MEDIUM)

- `test-widget` - Write widget tests with WidgetTester
- `test-golden` - Use golden tests for visual regression
- `test-integration` - Write integration tests for user flows
- `test-mock` - Use Mockito for dependency mocking
- `test-pump` - Use pumpAndSettle for async widget testing
- `test-finder` - Use semantic finders over positional

### 8. Platform Integration (LOW)

- `platform-channel` - Use MethodChannel for native communication
- `platform-plugin` - Create platform-specific plugins correctly
- `platform-native` - Handle platform differences with defaultTargetPlatform
- `platform-web` - Optimize for web with conditional imports
- `platform-desktop` - Handle desktop-specific input and window management

---

## Detailed Rules

### 1. Widget Optimization (CRITICAL)

#### `widget-const` - Use const constructors

Const widgets are cached and reused, preventing unnecessary rebuilds. Always mark widgets as const when possible.

**Incorrect (rebuilds on parent rebuild):**

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Text('Hello World'),
    );
  }
}

// Usage - creates new instance every build
Scaffold(body: MyWidget())
```

**Correct (const prevents rebuild):**

```dart
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Text('Hello World'),
    );
  }
}

// Usage - reuses cached instance
Scaffold(body: const MyWidget())
```

**Impact:** 10-50% reduction in widget rebuilds, significant memory savings.

---

#### `widget-split` - Split widgets to minimize rebuild scope

Extract parts of the widget tree into separate widgets to isolate rebuilds. When state changes, only the widget containing the state rebuilds.

**Incorrect (entire page rebuilds on counter change):**

```dart
class CounterPage extends StatefulWidget {
  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int counter = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Counter')),
      body: Column(
        children: [
          ExpensiveWidget(),  // rebuilds unnecessarily!
          HeavyImageWidget(), // rebuilds unnecessarily!
          Text('Count: $counter'),
          ElevatedButton(
            onPressed: () => setState(() => counter++),
            child: Text('Increment'),
          ),
        ],
      ),
    );
  }
}
```

**Correct (split into separate widgets):**

```dart
class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: const Column(
        children: [
          ExpensiveWidget(),  // doesn't rebuild
          HeavyImageWidget(), // doesn't rebuild
          CounterDisplay(),   // only this rebuilds
        ],
      ),
    );
  }
}

class CounterDisplay extends StatefulWidget {
  const CounterDisplay({super.key});

  @override
  State<CounterDisplay> createState() => _CounterDisplayState();
}

class _CounterDisplayState extends State<CounterDisplay> {
  int counter = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $counter'),
        ElevatedButton(
          onPressed: () => setState(() => counter++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

**Impact:** 2-10x reduction in rebuild scope, smoother animations.

---

#### `widget-key` - Use keys correctly

Keys preserve widget state and identity across rebuilds. Use ValueKey for data-driven widgets, GlobalKey sparingly for accessing state.

**Incorrect (state lost on reorder):**

```dart
ListView(
  children: items.map((item) =>
    ItemTile(item: item)  // state lost when items reorder
  ).toList(),
)
```

**Correct (state preserved with keys):**

```dart
ListView(
  children: items.map((item) =>
    ItemTile(key: ValueKey(item.id), item: item)
  ).toList(),
)

// For form fields that need external access
final _formKey = GlobalKey<FormState>();
Form(
  key: _formKey,
  child: ...,
)
// Access: _formKey.currentState?.validate()
```

**Impact:** Prevents state bugs, correct animations in lists.

---

#### `widget-builder` - Use Builder widgets

Builder widgets create a new BuildContext, limiting the scope of InheritedWidget lookups and rebuilds.

**Incorrect (entire widget rebuilds on theme change):**

```dart
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);  // subscribes entire widget
    return Scaffold(
      body: Column(
        children: [
          ExpensiveWidget(),
          Text('Themed', style: theme.textTheme.bodyLarge),
        ],
      ),
    );
  }
}
```

**Correct (only Builder child rebuilds):**

```dart
class MyPage extends StatelessWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          const ExpensiveWidget(),
          Builder(
            builder: (context) {
              final theme = Theme.of(context);
              return Text('Themed', style: theme.textTheme.bodyLarge);
            },
          ),
        ],
      ),
    );
  }
}
```

---

#### `widget-repaint` - Use RepaintBoundary

RepaintBoundary isolates paint operations, preventing expensive widgets from causing full repaints.

**Incorrect (animation causes full repaint):**

```dart
Stack(
  children: [
    ComplexBackground(),
    AnimatedWidget(),  // causes ComplexBackground to repaint
  ],
)
```

**Correct (animation isolated):**

```dart
Stack(
  children: [
    const RepaintBoundary(
      child: ComplexBackground(),
    ),
    AnimatedWidget(),  // only repaints its own layer
  ],
)
```

**Impact:** 60fps animations, reduced GPU usage.

---

#### `widget-sliver` - Use Slivers for lists

Slivers lazily build only visible items, essential for long scrolling lists.

**Incorrect (all items built at once):**

```dart
SingleChildScrollView(
  child: Column(
    children: items.map((item) => ItemWidget(item)).toList(),
  ),
)
```

**Correct (only visible items built):**

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(title: Text('Items')),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ItemWidget(items[index]),
        childCount: items.length,
      ),
    ),
  ],
)

// Or simpler with ListView.builder
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

**Impact:** O(visible) vs O(n) build time, constant memory usage.

---

### 2. State Management (CRITICAL)

#### `state-bloc` - Use BLoC for complex state

BLoC (Business Logic Component) separates business logic from UI with events and states.

**Correct BLoC implementation:**

```dart
// Events
sealed class UserEvent {}
class LoadUser extends UserEvent {
  final String userId;
  LoadUser(this.userId);
}
class UpdateUser extends UserEvent {
  final User user;
  UpdateUser(this.user);
}

// States
sealed class UserState {}
class UserInitial extends UserState {}
class UserLoading extends UserState {}
class UserLoaded extends UserState {
  final User user;
  UserLoaded(this.user);
}
class UserError extends UserState {
  final String message;
  UserError(this.message);
}

// BLoC
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository _repository;

  UserBloc(this._repository) : super(UserInitial()) {
    on<LoadUser>(_onLoadUser);
    on<UpdateUser>(_onUpdateUser);
  }

  Future<void> _onLoadUser(LoadUser event, Emitter<UserState> emit) async {
    emit(UserLoading());
    try {
      final user = await _repository.getUser(event.userId);
      emit(UserLoaded(user));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }

  Future<void> _onUpdateUser(UpdateUser event, Emitter<UserState> emit) async {
    emit(UserLoading());
    try {
      await _repository.updateUser(event.user);
      emit(UserLoaded(event.user));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }
}
```

---

#### `state-consumer` - Use buildWhen/select

Only rebuild when relevant state changes using buildWhen or select.

**Incorrect (rebuilds on any state change):**

```dart
BlocBuilder<UserBloc, UserState>(
  builder: (context, state) {
    // Rebuilds for UserLoading, UserLoaded, UserError...
    if (state is UserLoaded) {
      return UserProfile(user: state.user);
    }
    return const SizedBox.shrink();
  },
)
```

**Correct (rebuild only when needed):**

```dart
BlocBuilder<UserBloc, UserState>(
  buildWhen: (previous, current) =>
    current is UserLoaded && previous is! UserLoaded,
  builder: (context, state) {
    if (state is UserLoaded) {
      return UserProfile(user: state.user);
    }
    return const SizedBox.shrink();
  },
)

// Or use BlocSelector for specific property
BlocSelector<UserBloc, UserState, String?>(
  selector: (state) => state is UserLoaded ? state.user.name : null,
  builder: (context, name) {
    return Text(name ?? 'Loading...');
  },
)
```

**Impact:** 50-90% reduction in unnecessary rebuilds.

---

#### `state-riverpod` - Use Riverpod for compile-time safety

Riverpod provides compile-time safety, automatic disposal, and no BuildContext requirement.

**Correct Riverpod implementation:**

```dart
// Define providers
final userRepositoryProvider = Provider((ref) => UserRepository());

final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.getUser(userId);
});

final userNotifierProvider = NotifierProvider<UserNotifier, UserState>(() {
  return UserNotifier();
});

class UserNotifier extends Notifier<UserState> {
  @override
  UserState build() => UserInitial();

  Future<void> loadUser(String userId) async {
    state = UserLoading();
    try {
      final user = await ref.read(userRepositoryProvider).getUser(userId);
      state = UserLoaded(user);
    } catch (e) {
      state = UserError(e.toString());
    }
  }
}

// Usage in widget
class UserPage extends ConsumerWidget {
  const UserPage({super.key, required this.userId});
  final String userId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider(userId));

    return userAsync.when(
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
      data: (user) => UserProfile(user: user),
    );
  }
}
```

---

#### `state-selector` - Watch specific properties

Use Selector or select extension to watch only the state properties you need.

**Incorrect (rebuilds on any cart change):**

```dart
Consumer<CartProvider>(
  builder: (context, cart, child) {
    return Text('Items: ${cart.items.length}');
    // Rebuilds when total changes too!
  },
)
```

**Correct (rebuilds only when count changes):**

```dart
Selector<CartProvider, int>(
  selector: (context, cart) => cart.items.length,
  builder: (context, itemCount, child) {
    return Text('Items: $itemCount');
  },
)

// With Riverpod
ref.watch(cartProvider.select((cart) => cart.items.length))
```

---

#### `state-rebuild` - Avoid unnecessary setState

Only call setState when state actually changes, and batch multiple changes.

**Incorrect (multiple rebuilds):**

```dart
void updateUser() {
  setState(() => _name = newName);
  setState(() => _email = newEmail);  // second rebuild!
  setState(() => _phone = newPhone);  // third rebuild!
}
```

**Correct (single rebuild):**

```dart
void updateUser() {
  setState(() {
    _name = newName;
    _email = newEmail;
    _phone = newPhone;
  });
}

// Or check if value changed
void setName(String name) {
  if (_name != name) {
    setState(() => _name = name);
  }
}
```

---

### 3. Async Patterns (HIGH)

#### `async-future-builder` - Handle all states

Always handle waiting, error, and data states in FutureBuilder.

**Correct implementation:**

```dart
FutureBuilder<User>(
  future: _userFuture,
  builder: (context, snapshot) {
    // Handle connection state
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Center(child: CircularProgressIndicator());
    }

    // Handle error
    if (snapshot.hasError) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Error: ${snapshot.error}'),
            ElevatedButton(
              onPressed: _retryLoad,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    // Handle no data
    if (!snapshot.hasData) {
      return const Center(child: Text('No user found'));
    }

    // Success
    return UserProfile(user: snapshot.data!);
  },
)
```

---

#### `async-cache` - Cache futures to prevent refetch

Cache futures in state to prevent refetching on every rebuild.

**Incorrect (refetches every rebuild):**

```dart
class _MyWidgetState extends State<MyWidget> {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: fetchUser(),  // Called every build!
      builder: (context, snapshot) => ...,
    );
  }
}
```

**Correct (cached in state):**

```dart
class _MyWidgetState extends State<MyWidget> {
  late final Future<User> _userFuture;

  @override
  void initState() {
    super.initState();
    _userFuture = fetchUser();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _userFuture,  // Cached, not refetched
      builder: (context, snapshot) => ...,
    );
  }
}
```

---

#### `async-cancel` - Cancel async operations

Cancel async operations when widget disposes to prevent setState on disposed widget.

**Correct implementation:**

```dart
class _MyWidgetState extends State<MyWidget> {
  CancelableOperation<User>? _operation;

  @override
  void initState() {
    super.initState();
    _loadUser();
  }

  Future<void> _loadUser() async {
    _operation = CancelableOperation.fromFuture(fetchUser());
    try {
      final user = await _operation!.value;
      if (mounted) {
        setState(() => _user = user);
      }
    } catch (e) {
      if (mounted) {
        setState(() => _error = e.toString());
      }
    }
  }

  @override
  void dispose() {
    _operation?.cancel();
    super.dispose();
  }
}
```

---

#### `async-isolate` - Use Isolates for heavy computation

Move CPU-intensive work to Isolates to keep UI responsive.

**Correct implementation:**

```dart
// For simple functions
Future<List<Item>> parseJsonInBackground(String json) async {
  return compute(_parseJson, json);
}

List<Item> _parseJson(String json) {
  final data = jsonDecode(json) as List;
  return data.map((e) => Item.fromJson(e)).toList();
}

// For complex operations with multiple calls
class ImageProcessor {
  late final SendPort _sendPort;

  Future<void> init() async {
    final receivePort = ReceivePort();
    await Isolate.spawn(_isolateEntry, receivePort.sendPort);
    _sendPort = await receivePort.first;
  }

  Future<Uint8List> processImage(Uint8List image) async {
    final response = ReceivePort();
    _sendPort.send([image, response.sendPort]);
    return await response.first;
  }

  static void _isolateEntry(SendPort sendPort) {
    final receivePort = ReceivePort();
    sendPort.send(receivePort.sendPort);

    receivePort.listen((message) {
      final image = message[0] as Uint8List;
      final replyPort = message[1] as SendPort;
      final processed = _heavyImageProcessing(image);
      replyPort.send(processed);
    });
  }
}
```

**Impact:** 60fps UI during heavy computation.

---

### 4. Memory Management (HIGH)

#### `mem-dispose` - Always dispose resources

Dispose all controllers, subscriptions, and listeners in dispose().

**Correct implementation:**

```dart
class _MyWidgetState extends State<MyWidget> {
  final _textController = TextEditingController();
  final _scrollController = ScrollController();
  late final AnimationController _animationController;
  StreamSubscription? _subscription;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(vsync: this);
    _subscription = eventStream.listen(_handleEvent);
    _timer = Timer.periodic(Duration(seconds: 1), _tick);
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    _animationController.dispose();
    _subscription?.cancel();
    _timer?.cancel();
    super.dispose();
  }
}
```

---

#### `mem-leak` - Avoid context capture across async gaps

Don't capture BuildContext in closures that outlive the widget.

**Incorrect (context captured across async gap):**

```dart
void _handleTap() async {
  final result = await longRunningOperation();
  // Widget may be disposed by now!
  Navigator.of(context).push(...);  // CRASH!
  ScaffoldMessenger.of(context).showSnackBar(...);  // CRASH!
}
```

**Correct (check mounted, capture early):**

```dart
void _handleTap() async {
  final navigator = Navigator.of(context);
  final messenger = ScaffoldMessenger.of(context);

  final result = await longRunningOperation();

  if (!mounted) return;

  navigator.push(...);
  messenger.showSnackBar(...);
}
```

---

#### `mem-image` - Optimize image memory

Use cached_network_image and control cache size for images.

**Correct implementation:**

```dart
// Use cached_network_image
CachedNetworkImage(
  imageUrl: url,
  memCacheWidth: 200,  // Decode at display size
  memCacheHeight: 200,
  maxWidthDiskCache: 400,
  maxHeightDiskCache: 400,
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
)

// Precache images
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  precacheImage(AssetImage('assets/logo.png'), context);
}

// Clear image cache when memory pressure
@override
void didReceiveMemoryWarning() {
  imageCache.clear();
  imageCache.clearLiveImages();
}
```

---

### 5. Rendering Performance (MEDIUM)

#### `render-list` - Use ListView.builder

Use builder constructors for lists to build only visible items.

**Incorrect (builds all items):**

```dart
ListView(
  children: items.map((item) => ItemTile(item)).toList(),
)
```

**Correct (builds only visible):**

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemTile(items[index]),
  // Optional: provide item extent for better performance
  itemExtent: 80,
)

// For very long lists with variable heights
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemTile(items[index]),
  addAutomaticKeepAlives: false,
  addRepaintBoundaries: true,
)
```

---

#### `render-animation` - Use AnimatedBuilder

Isolate animation rebuilds with AnimatedBuilder.

**Incorrect (entire widget rebuilds):**

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  Widget build(BuildContext context) {
    return Transform.rotate(
      angle: _controller.value * 2 * pi,
      child: Column(
        children: [
          ExpensiveWidget(),  // rebuilds 60 times/second!
          Icon(Icons.star),
        ],
      ),
    );
  }
}
```

**Correct (only transform rebuilds):**

```dart
@override
Widget build(BuildContext context) {
  return AnimatedBuilder(
    animation: _controller,
    child: const Column(
      children: [
        ExpensiveWidget(),  // built once
        Icon(Icons.star),
      ],
    ),
    builder: (context, child) {
      return Transform.rotate(
        angle: _controller.value * 2 * pi,
        child: child,  // reused
      );
    },
  );
}
```

---

#### `render-clip` - Avoid ClipRRect when possible

ClipRRect is expensive. Use decoration when you only need rounded corners.

**Incorrect (uses clip):**

```dart
ClipRRect(
  borderRadius: BorderRadius.circular(8),
  child: Container(
    color: Colors.blue,
    child: Text('Hello'),
  ),
)
```

**Correct (uses decoration):**

```dart
Container(
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text('Hello'),
)
```

---

### 6. Architecture (MEDIUM)

#### `arch-layer` - Separate layers

Use clean architecture layers: presentation, domain, data.

**Correct structure:**

```
lib/
  features/
    user/
      presentation/
        pages/
          user_page.dart
        widgets/
          user_card.dart
        bloc/
          user_bloc.dart
          user_event.dart
          user_state.dart
      domain/
        entities/
          user.dart
        repositories/
          user_repository.dart
        usecases/
          get_user.dart
          update_user.dart
      data/
        datasources/
          user_remote_datasource.dart
          user_local_datasource.dart
        models/
          user_model.dart
        repositories/
          user_repository_impl.dart
```

---

#### `arch-repository` - Use Repository pattern

Abstract data sources behind repository interfaces.

**Correct implementation:**

```dart
// Domain layer - abstract repository
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> updateUser(User user);
  Future<List<User>> searchUsers(String query);
}

// Data layer - concrete implementation
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource;
  final UserLocalDataSource _localDataSource;
  final NetworkInfo _networkInfo;

  UserRepositoryImpl({
    required UserRemoteDataSource remoteDataSource,
    required UserLocalDataSource localDataSource,
    required NetworkInfo networkInfo,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource,
        _networkInfo = networkInfo;

  @override
  Future<User> getUser(String id) async {
    if (await _networkInfo.isConnected) {
      final user = await _remoteDataSource.getUser(id);
      await _localDataSource.cacheUser(user);
      return user;
    } else {
      return _localDataSource.getUser(id);
    }
  }
}
```

---

#### `arch-di` - Use dependency injection

Use get_it or injectable for dependency injection.

**Correct implementation:**

```dart
// injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // BLoCs
  sl.registerFactory(() => UserBloc(sl()));

  // Use Cases
  sl.registerLazySingleton(() => GetUser(sl()));
  sl.registerLazySingleton(() => UpdateUser(sl()));

  // Repositories
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data Sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(client: sl()),
  );
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sharedPreferences: sl()),
  );

  // External
  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerLazySingleton(() => sharedPreferences);
  sl.registerLazySingleton(() => http.Client());
}
```

---

### 7. Testing (MEDIUM)

#### `test-widget` - Write widget tests

Use WidgetTester for comprehensive widget testing.

**Correct implementation:**

```dart
void main() {
  group('UserCard', () {
    testWidgets('displays user name', (tester) async {
      final user = User(id: '1', name: 'John Doe', email: 'john@example.com');

      await tester.pumpWidget(
        MaterialApp(
          home: UserCard(user: user),
        ),
      );

      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('john@example.com'), findsOneWidget);
    });

    testWidgets('calls onTap when tapped', (tester) async {
      var tapped = false;
      final user = User(id: '1', name: 'John', email: 'john@example.com');

      await tester.pumpWidget(
        MaterialApp(
          home: UserCard(
            user: user,
            onTap: () => tapped = true,
          ),
        ),
      );

      await tester.tap(find.byType(UserCard));
      expect(tapped, isTrue);
    });
  });
}
```

---

#### `test-pump` - Use pumpAndSettle correctly

Use pump for controlled animation frames, pumpAndSettle for waiting animations.

**Correct implementation:**

```dart
testWidgets('shows loading then data', (tester) async {
  await tester.pumpWidget(MyApp());

  // Initially shows loading
  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  // Pump until animations complete and futures resolve
  await tester.pumpAndSettle();

  // Now shows data
  expect(find.byType(CircularProgressIndicator), findsNothing);
  expect(find.byType(UserList), findsOneWidget);
});

testWidgets('animation test with controlled frames', (tester) async {
  await tester.pumpWidget(AnimatedWidget());

  // Advance 100ms
  await tester.pump(const Duration(milliseconds: 100));
  expect(find.byType(FadeTransition), findsOneWidget);

  // Advance to completion
  await tester.pump(const Duration(milliseconds: 200));
});
```

---

#### `test-mock` - Use Mockito for mocking

Mock dependencies with Mockito and mocktail.

**Correct implementation:**

```dart
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late UserBloc bloc;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    bloc = UserBloc(mockRepository);
  });

  tearDown(() {
    bloc.close();
  });

  group('LoadUser', () {
    final testUser = User(id: '1', name: 'John', email: 'john@example.com');

    test('emits [Loading, Loaded] when successful', () async {
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) async => testUser);

      bloc.add(LoadUser('1'));

      await expectLater(
        bloc.stream,
        emitsInOrder([
          isA<UserLoading>(),
          isA<UserLoaded>().having((s) => s.user, 'user', testUser),
        ]),
      );
    });

    test('emits [Loading, Error] when fails', () async {
      when(() => mockRepository.getUser('1'))
          .thenThrow(Exception('Network error'));

      bloc.add(LoadUser('1'));

      await expectLater(
        bloc.stream,
        emitsInOrder([
          isA<UserLoading>(),
          isA<UserError>(),
        ]),
      );
    });
  });
}
```

---

### 8. Platform Integration (LOW)

#### `platform-channel` - Use MethodChannel correctly

Implement platform channels with proper error handling.

**Correct implementation:**

```dart
class BatteryService {
  static const _channel = MethodChannel('com.example.app/battery');

  Future<int> getBatteryLevel() async {
    try {
      final int result = await _channel.invokeMethod('getBatteryLevel');
      return result;
    } on PlatformException catch (e) {
      throw BatteryException('Failed to get battery level: ${e.message}');
    }
  }

  Stream<int> batteryLevelStream() {
    const eventChannel = EventChannel('com.example.app/battery_stream');
    return eventChannel
        .receiveBroadcastStream()
        .map((event) => event as int);
  }
}

// Usage
final batteryService = BatteryService();
final level = await batteryService.getBatteryLevel();
```

---

#### `platform-native` - Handle platform differences

Use defaultTargetPlatform for platform-specific behavior.

**Correct implementation:**

```dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb, defaultTargetPlatform;

Widget buildPlatformWidget() {
  if (kIsWeb) {
    return WebWidget();
  }

  switch (defaultTargetPlatform) {
    case TargetPlatform.iOS:
      return CupertinoWidget();
    case TargetPlatform.android:
      return MaterialWidget();
    case TargetPlatform.macOS:
    case TargetPlatform.windows:
    case TargetPlatform.linux:
      return DesktopWidget();
    default:
      return MaterialWidget();
  }
}

// Platform-specific styling
EdgeInsets get platformPadding {
  if (kIsWeb) return const EdgeInsets.all(24);
  if (Platform.isIOS) return const EdgeInsets.all(16);
  return const EdgeInsets.all(12);
}
```

---

## Integration Workflow

### When Writing New Widgets

1. Start with `const` constructor (`widget-const`)
2. Identify state boundaries and split widgets (`widget-split`)
3. Add RepaintBoundary for animations (`widget-repaint`)
4. Use Builder for InheritedWidget access (`widget-builder`)

### When Implementing State Management

1. Choose BLoC for complex logic (`state-bloc`) or Riverpod for reactive patterns (`state-riverpod`)
2. Use buildWhen/select to limit rebuilds (`state-consumer`, `state-selector`)
3. Scope providers appropriately (`state-provider`)

### When Working with Async Operations

1. Cache futures in initState (`async-cache`)
2. Handle all FutureBuilder states (`async-future-builder`)
3. Cancel operations in dispose (`async-cancel`)
4. Use Isolates for heavy work (`async-isolate`)

### When Optimizing Performance

1. Profile with Flutter DevTools first
2. Add RepaintBoundary to animations (`render-boundary`)
3. Use ListView.builder for lists (`render-list`)
4. Dispose all resources (`mem-dispose`)

---

## References

- [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices)
- [Effective Dart](https://dart.dev/effective-dart)
- [Flutter BLoC Library](https://bloclibrary.dev/)
- [Riverpod Documentation](https://riverpod.dev/)
- [Flutter Testing](https://docs.flutter.dev/testing)
