# Widget Lifecycle

A comprehensive guide to understanding and managing the lifecycle of Flutter widgets, with a focus on StatefulWidget lifecycle methods, state management, and best practices for resource handling.

## Overview

Understanding widget lifecycle is crucial for building performant, bug-free Flutter applications. The lifecycle defines when widgets are created, updated, and destroyed, and provides hooks for initialization, updates, and cleanup.

## StatelessWidget vs StatefulWidget

### StatelessWidget

Immutable widgets that don't maintain internal state. They have a simple lifecycle: they're built once and rebuild when parent widgets change.

```dart
class MyStatelessWidget extends StatelessWidget {
  final String title;

  const MyStatelessWidget({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    // Called every time the widget needs to be rendered
    return Text(title);
  }
}
```

**Lifecycle:** Constructor → build() → dispose (when removed from tree)

### StatefulWidget

Widgets that maintain mutable state that can change over time. They have a complex lifecycle with multiple phases.

```dart
class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({super.key});

  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_counter'),
        ElevatedButton(
          onPressed: () => setState(() => _counter++),
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

## StatefulWidget Lifecycle

The lifecycle of a StatefulWidget's State object follows a well-defined sequence of method calls.

### 1. createState()

Called when the Flutter framework creates the StatefulWidget. Returns the State object that will be associated with this widget.

```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}
```

**When called:** Once, when the widget is first inserted into the tree
**Purpose:** Create the State object
**Best practice:** Keep this method simple; it should only return the State instance

### 2. initState()

Called once when the State object is created and inserted into the tree. This is your opportunity to initialize state variables, subscribe to streams, or set up controllers.

```dart
class _MyWidgetState extends State<MyWidget> {
  late ScrollController _scrollController;
  late StreamSubscription _subscription;
  Timer? _timer;

  @override
  void initState() {
    super.initState(); // MUST call super.initState() first

    // Initialize controllers
    _scrollController = ScrollController();

    // Subscribe to streams
    _subscription = someStream.listen((data) {
      setState(() {
        // Update state based on stream data
      });
    });

    // Start timers or animations
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        // Update state periodically
      });
    });

    // Fetch initial data
    _loadData();
  }

  Future<void> _loadData() async {
    // Async operations
    final data = await fetchData();
    setState(() {
      // Update state with fetched data
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _subscription.cancel();
    _timer?.cancel();
    super.dispose();
  }
}
```

**When called:** Once, immediately after createState()
**Context available:** Yes, but `BuildContext` shouldn't be used for inherited widgets yet
**Can call setState:** No (widget hasn't been built yet)
**Best practices:**
- Always call `super.initState()` first
- Initialize controllers and state variables
- Subscribe to streams or listeners
- Don't perform expensive synchronous operations
- Async operations are allowed but handle carefully

### 3. didChangeDependencies()

Called immediately after `initState()` and whenever the widget's dependencies change (e.g., InheritedWidget it depends on changes).

```dart
class _MyWidgetState extends State<MyWidget> {
  late String _locale;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies(); // MUST call super first

    // Access InheritedWidgets
    _locale = Localizations.localeOf(context).toString();

    // React to theme changes
    final theme = Theme.of(context);
    print('Theme changed: ${theme.brightness}');
  }

  @override
  Widget build(BuildContext context) {
    return Text('Locale: $_locale');
  }
}
```

**When called:**
- Once, immediately after `initState()`
- Whenever dependencies change (InheritedWidget updates)
**Context available:** Yes, safe to use for InheritedWidgets
**Can call setState:** Yes, but be careful to avoid loops
**Best practices:**
- Call `super.didChangeDependencies()` first
- Use for accessing InheritedWidgets (Theme, MediaQuery, etc.)
- Avoid expensive operations; called frequently
- Be cautious with setState to prevent infinite loops

### 4. build()

Called to render the widget. This is where you return the widget tree that describes what the UI should look like.

```dart
class _MyWidgetState extends State<MyWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    // Access theme, media query, etc.
    final theme = Theme.of(context);
    final screenSize = MediaQuery.of(context).size;

    // Build widget tree
    return Scaffold(
      appBar: AppBar(title: Text('Counter: $_counter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'You have pushed the button this many times:',
              style: theme.textTheme.bodyMedium,
            ),
            Text(
              '$_counter',
              style: theme.textTheme.displayLarge,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => setState(() => _counter++),
        child: Icon(Icons.add),
      ),
    );
  }
}
```

**When called:**
- After `didChangeDependencies()`
- After `setState()` is called
- When parent widget rebuilds
- When InheritedWidget dependencies change
**Context available:** Yes
**Can call setState:** No (will cause an error)
**Best practices:**
- Keep build method pure (no side effects)
- Don't perform expensive computations; cache results if needed
- Don't create controllers or subscriptions here
- Don't call setState inside build
- Extract complex subtrees into separate widgets

### 5. didUpdateWidget()

Called when the widget configuration changes (parent rebuilds with different parameters).

```dart
class MyWidget extends StatefulWidget {
  final String title;
  final Color color;

  const MyWidget({
    super.key,
    required this.title,
    required this.color,
  });

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late String _localTitle;

  @override
  void initState() {
    super.initState();
    _localTitle = widget.title;
  }

  @override
  void didUpdateWidget(MyWidget oldWidget) {
    super.didUpdateWidget(oldWidget); // MUST call super first

    // React to widget property changes
    if (oldWidget.title != widget.title) {
      setState(() {
        _localTitle = widget.title;
      });
    }

    if (oldWidget.color != widget.color) {
      print('Color changed from ${oldWidget.color} to ${widget.color}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: widget.color,
      child: Text(_localTitle),
    );
  }
}
```

**When called:** When parent rebuilds with different widget configuration
**Context available:** Yes
**Can call setState:** Yes
**Best practices:**
- Call `super.didUpdateWidget()` first
- Compare `oldWidget` with `widget` to detect changes
- Update state only when necessary
- Use for reacting to configuration changes

### 6. setState()

Notifies the framework that internal state has changed and the widget should be rebuilt.

```dart
class _MyWidgetState extends State<MyWidget> {
  int _counter = 0;
  bool _isLoading = false;

  void _incrementCounter() {
    setState(() {
      // Update state inside setState callback
      _counter++;
    });
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final data = await fetchData();
      setState(() {
        _isLoading = false;
        // Update state with fetched data
      });
    } catch (error) {
      setState(() {
        _isLoading = false;
        // Handle error
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return CircularProgressIndicator();
    }

    return Column(
      children: [
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: _incrementCounter,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

**When to call:**
- When internal state changes
- After async operations complete
- In response to user input
**Effect:** Schedules a rebuild of the widget
**Best practices:**
- Only update state variables inside setState callback
- Keep setState callback synchronous and fast
- Don't call setState after dispose
- Check `mounted` before calling setState in async callbacks

### 7. deactivate()

Called when the State object is removed from the tree but might be reinserted before the frame ends.

```dart
class _MyWidgetState extends State<MyWidget> {
  @override
  void deactivate() {
    // Pause animations or subscriptions that might continue
    // while the widget is temporarily removed

    super.deactivate(); // Call super last
  }
}
```

**When called:** When widget is removed from tree (might be temporary)
**Best practices:**
- Rarely needed in most apps
- Useful for pausing animations or subscriptions
- Don't dispose resources here; use dispose() instead

### 8. dispose()

Called when the State object is permanently removed from the tree. This is your opportunity to clean up resources.

```dart
class _MyWidgetState extends State<MyWidget> {
  late TextEditingController _controller;
  late AnimationController _animationController;
  late StreamSubscription _subscription;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _animationController = AnimationController(
      vsync: this,
      duration: Duration(seconds: 1),
    );
    _subscription = someStream.listen((data) {});
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {});
  }

  @override
  void dispose() {
    // Clean up controllers
    _controller.dispose();
    _animationController.dispose();

    // Cancel subscriptions
    _subscription.cancel();
    _timer?.cancel();

    // Call super.dispose() last
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextField(controller: _controller);
  }
}
```

**When called:** When widget is permanently removed from tree
**State after dispose:** `mounted` property becomes false
**Can call setState:** No (will throw error)
**Best practices:**
- Dispose all controllers (TextEditingController, AnimationController, etc.)
- Cancel all subscriptions and listeners
- Cancel timers
- Close streams
- Call `super.dispose()` last
- Always dispose to prevent memory leaks

## Lifecycle Diagram

```
1. createState()
   ↓
2. initState()
   ↓
3. didChangeDependencies()
   ↓
4. build()
   ↓
   ┌─────────────────┐
   │ Widget Active   │ ←───────────┐
   │                 │             │
   │ setState() ─────┼─→ build()   │
   │                 │             │
   │ Parent rebuilds ┼─────────────┘
   │ (didUpdateWidget)
   └─────────────────┘
   ↓
5. deactivate()
   ↓
6. dispose()
```

## Common Patterns and Best Practices

### Safe setState in Async Callbacks

Always check if the widget is still mounted before calling setState in async callbacks:

```dart
class _MyWidgetState extends State<MyWidget> {
  bool _isLoading = false;

  Future<void> _loadData() async {
    setState(() => _isLoading = true);

    try {
      final data = await fetchData();

      // Check if widget is still in tree before calling setState
      if (!mounted) return;

      setState(() {
        _isLoading = false;
        // Update state with data
      });
    } catch (error) {
      if (!mounted) return;

      setState(() {
        _isLoading = false;
        // Handle error
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return CircularProgressIndicator();
    }
    return ElevatedButton(
      onPressed: _loadData,
      child: Text('Load Data'),
    );
  }
}
```

### Proper Controller Management

Always create controllers in `initState()` and dispose them in `dispose()`:

```dart
class _FormWidgetState extends State<FormWidget> {
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late FocusNode _emailFocusNode;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _emailController = TextEditingController();
    _emailFocusNode = FocusNode();

    // Add listeners if needed
    _nameController.addListener(() {
      print('Name: ${_nameController.text}');
    });
  }

  @override
  void dispose() {
    // Dispose in reverse order of creation
    _nameController.dispose();
    _emailController.dispose();
    _emailFocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(
          controller: _nameController,
          decoration: InputDecoration(labelText: 'Name'),
        ),
        TextField(
          controller: _emailController,
          focusNode: _emailFocusNode,
          decoration: InputDecoration(labelText: 'Email'),
        ),
      ],
    );
  }
}
```

### Stream Subscriptions

Manage stream subscriptions properly to avoid memory leaks:

```dart
class _StreamWidgetState extends State<StreamWidget> {
  late StreamSubscription<int> _subscription;
  int _value = 0;

  @override
  void initState() {
    super.initState();
    _subscription = someStream.listen(
      (value) {
        if (!mounted) return;
        setState(() {
          _value = value;
        });
      },
      onError: (error) {
        print('Stream error: $error');
      },
    );
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Text('Value: $_value');
  }
}
```

### Animation Controllers

Use `SingleTickerProviderStateMixin` or `TickerProviderStateMixin` for animations:

```dart
class _AnimatedWidgetState extends State<AnimatedWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(seconds: 2),
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
    _controller.repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: Container(
        width: 200,
        height: 200,
        color: Colors.blue,
      ),
    );
  }
}
```

### Timers and Periodic Updates

Manage timers properly:

```dart
class _TimerWidgetState extends State<TimerWidget> {
  Timer? _timer;
  int _seconds = 0;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }
      setState(() {
        _seconds++;
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Text('Elapsed: $_seconds seconds');
  }
}
```

### Using AutomaticKeepAliveClientMixin

Preserve state when widgets scroll out of view:

```dart
class _KeepAliveWidgetState extends State<KeepAliveWidget>
    with AutomaticKeepAliveClientMixin {
  int _counter = 0;

  @override
  bool get wantKeepAlive => true;

  @override
  Widget build(BuildContext context) {
    super.build(context); // MUST call super.build()

    return Column(
      children: [
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: () => setState(() => _counter++),
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

## Debugging Lifecycle

### Print Lifecycle Methods

Add print statements to understand lifecycle flow:

```dart
class _MyWidgetState extends State<MyWidget> {
  @override
  void initState() {
    super.initState();
    print('initState called');
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    print('didChangeDependencies called');
  }

  @override
  void didUpdateWidget(MyWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    print('didUpdateWidget called');
  }

  @override
  Widget build(BuildContext context) {
    print('build called');
    return Container();
  }

  @override
  void deactivate() {
    print('deactivate called');
    super.deactivate();
  }

  @override
  void dispose() {
    print('dispose called');
    super.dispose();
  }
}
```

### Check Mounted Property

Verify widget is still in tree before operations:

```dart
if (mounted) {
  setState(() {
    // Safe to update state
  });
}
```

## Common Mistakes

### 1. Calling setState After Dispose

```dart
// WRONG
Future<void> _loadData() async {
  final data = await fetchData();
  setState(() {}); // May throw if widget was disposed
}

// CORRECT
Future<void> _loadData() async {
  final data = await fetchData();
  if (!mounted) return;
  setState(() {});
}
```

### 2. Not Disposing Controllers

```dart
// WRONG - Memory leak
class _MyWidgetState extends State<MyWidget> {
  final _controller = TextEditingController();
  // No dispose method
}

// CORRECT
class _MyWidgetState extends State<MyWidget> {
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

### 3. Expensive Operations in build()

```dart
// WRONG
@override
Widget build(BuildContext context) {
  final expensiveData = performExpensiveComputation(); // Called every rebuild
  return Text(expensiveData);
}

// CORRECT
class _MyWidgetState extends State<MyWidget> {
  late String _cachedData;

  @override
  void initState() {
    super.initState();
    _cachedData = performExpensiveComputation();
  }

  @override
  Widget build(BuildContext context) {
    return Text(_cachedData);
  }
}
```

### 4. Forgetting super Calls

```dart
// WRONG
@override
void initState() {
  // Forgot super.initState()
  _controller = TextEditingController();
}

// CORRECT
@override
void initState() {
  super.initState(); // MUST call first
  _controller = TextEditingController();
}
```

## Best Practices Summary

1. **Always call super methods** in the correct order
2. **Initialize in initState**, clean up in dispose
3. **Check mounted** before setState in async callbacks
4. **Dispose controllers** to prevent memory leaks
5. **Keep build pure** - no side effects or expensive operations
6. **Cancel subscriptions** in dispose
7. **Use const constructors** where possible
8. **Extract complex widgets** to separate classes
9. **Profile performance** with Flutter DevTools
10. **Test lifecycle** with unit and widget tests

## Further Reading

- [Widget Catalog](widget-catalog.md)
- [Layout Patterns](layout-patterns.md)
- [Custom Widgets Example](../examples/custom-widgets.md)
- [Flutter State Documentation](https://api.flutter.dev/flutter/widgets/State-class.html)
