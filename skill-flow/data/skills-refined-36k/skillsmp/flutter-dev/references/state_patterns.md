# State Management Patterns

Comprehensive examples of state management approaches in Flutter.

## Pattern 1: ValueNotifier (Simplest)

Best for: Simple local state with a single value

```dart
class CounterScreen extends StatefulWidget {
  const CounterScreen({super.key});

  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  final ValueNotifier<int> _counter = ValueNotifier<int>(0);

  @override
  void dispose() {
    _counter.dispose();
    super.dispose();
  }

  void _increment() {
    _counter.value++;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ValueListenableBuilder<int>(
          valueListenable: _counter,
          builder: (context, value, child) {
            return Text('Count: $value');
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Pattern 2: ChangeNotifier (Intermediate)

Best for: Complex state or shared state across widgets

```dart
// Model
class CounterModel extends ChangeNotifier {
  int _count = 0;
  
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners();
  }
  
  void decrement() {
    _count--;
    notifyListeners();
  }
  
  void reset() {
    _count = 0;
    notifyListeners();
  }
}

// Usage
class CounterScreen extends StatefulWidget {
  const CounterScreen({super.key});

  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  final CounterModel _model = CounterModel();

  @override
  void dispose() {
    _model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ListenableBuilder(
          listenable: _model,
          builder: (context, child) {
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Count: ${_model.count}'),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton(
                      onPressed: _model.decrement,
                      child: const Icon(Icons.remove),
                    ),
                    const SizedBox(width: 16),
                    ElevatedButton(
                      onPressed: _model.increment,
                      child: const Icon(Icons.add),
                    ),
                  ],
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
```

## Pattern 3: Streams + StreamBuilder

Best for: Sequences of asynchronous events

```dart
class TimerModel {
  final _controller = StreamController<int>();
  Stream<int> get stream => _controller.stream;
  
  int _count = 0;
  Timer? _timer;
  
  void start() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      _count++;
      _controller.add(_count);
    });
  }
  
  void stop() {
    _timer?.cancel();
  }
  
  void dispose() {
    _timer?.cancel();
    _controller.close();
  }
}

class TimerScreen extends StatefulWidget {
  const TimerScreen({super.key});

  @override
  State<TimerScreen> createState() => _TimerScreenState();
}

class _TimerScreenState extends State<TimerScreen> {
  final TimerModel _model = TimerModel();

  @override
  void dispose() {
    _model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: StreamBuilder<int>(
          stream: _model.stream,
          initialData: 0,
          builder: (context, snapshot) {
            return Text('Time: ${snapshot.data}s');
          },
        ),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: _model.start,
            child: const Icon(Icons.play_arrow),
          ),
          const SizedBox(height: 8),
          FloatingActionButton(
            onPressed: _model.stop,
            child: const Icon(Icons.stop),
          ),
        ],
      ),
    );
  }
}
```

## Pattern 4: MVVM (Advanced)

Best for: Complex applications with business logic separation

```dart
// Model
class User {
  final String id;
  final String name;
  final String email;
  
  const User({
    required this.id,
    required this.name,
    required this.email,
  });
}

// ViewModel
class UserViewModel extends ChangeNotifier {
  final UserRepository _repository;
  
  UserViewModel(this._repository);
  
  User? _user;
  bool _isLoading = false;
  String? _error;
  
  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  Future<void> loadUser(String userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      _user = await _repository.getUser(userId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  Future<void> updateUser(User user) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _repository.updateUser(user);
      _user = user;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}

// View
class UserScreen extends StatefulWidget {
  final String userId;
  
  const UserScreen({super.key, required this.userId});

  @override
  State<UserScreen> createState() => _UserScreenState();
}

class _UserScreenState extends State<UserScreen> {
  late final UserViewModel _viewModel;

  @override
  void initState() {
    super.initState();
    _viewModel = UserViewModel(UserRepository());
    _viewModel.loadUser(widget.userId);
  }

  @override
  void dispose() {
    _viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('User Profile')),
      body: ListenableBuilder(
        listenable: _viewModel,
        builder: (context, child) {
          if (_viewModel.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (_viewModel.error != null) {
            return Center(child: Text('Error: ${_viewModel.error}'));
          }
          
          final user = _viewModel.user;
          if (user == null) {
            return const Center(child: Text('No user found'));
          }
          
          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Name: ${user.name}'),
                const SizedBox(height: 8),
                Text('Email: ${user.email}'),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

## Pattern 5: Manual Dependency Injection

Best for: Making dependencies explicit and testable

```dart
// Service
class AuthService {
  Future<bool> login(String email, String password) async {
    // Implementation
    return true;
  }
  
  bool isLoggedIn() {
    // Implementation
    return false;
  }
}

// Screen with dependency injection
class LoginScreen extends StatefulWidget {
  final AuthService authService;
  
  const LoginScreen({
    super.key,
    required this.authService,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    setState(() => _isLoading = true);
    
    try {
      final success = await widget.authService.login(
        _emailController.text,
        _passwordController.text,
      );
      
      if (success && mounted) {
        // Navigate to home
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // Build UI
    return Scaffold(
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator()
            : ElevatedButton(
                onPressed: _handleLogin,
                child: const Text('Login'),
              ),
      ),
    );
  }
}

// Usage
class MyApp extends StatelessWidget {
  final AuthService authService = AuthService();
  
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: LoginScreen(authService: authService),
    );
  }
}
```

## State Management Decision Tree

1. **Single value, local to widget?** → Use `ValueNotifier`
2. **Multiple values or shared across widgets?** → Use `ChangeNotifier`
3. **Handling async event sequences?** → Use `Stream` + `StreamBuilder`
4. **Single async operation?** → Use `Future` + `FutureBuilder`
5. **Complex app with business logic separation?** → Use MVVM pattern
6. **Need explicit dependencies for testing?** → Use manual DI with constructor injection
7. **User explicitly requests Provider/Riverpod/Bloc?** → Use requested solution
