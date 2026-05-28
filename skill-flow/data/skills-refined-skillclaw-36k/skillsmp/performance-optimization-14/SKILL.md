---
name: Performance Optimization
description: Performance optimization patterns for Flutter applications including widget optimization, memory management, profiling, and 60 FPS best practices
version: 1.0.0
---

# Performance Optimization for Flutter

Complete guide to building high-performance Flutter applications that maintain 60 FPS (or 120 FPS on capable devices).

## Performance Goals

- **60 FPS**: Each frame must render in < 16ms
- **120 FPS**: Each frame must render in < 8ms (for high refresh rate displays)
- **Jank-free**: No dropped frames during scrolling or animations
- **Fast startup**: App ready in < 2 seconds
- **Low memory**: < 100MB for typical screens

## Widget Optimization

### Use const Constructors

Const widgets are built once and reused:

```dart
// ❌ BAD - Widget rebuilt every time
Widget build(BuildContext context) {
  return Container(
    padding: EdgeInsets.all(16.0),
    child: Text('Static Text'),
  );
}

// ✅ GOOD - Widget built once, reused
Widget build(BuildContext context) {
  return const Padding(
    padding: EdgeInsets.all(16.0),
    child: Text('Static Text'),
  );
}

// ✅ GOOD - Individual widgets const
Widget build(BuildContext context) {
  return Column(
    children: const [
      Icon(Icons.home),
      SizedBox(height: 8),
      Text('Home'),
    ],
  );
}
```

**Rule**: If a widget's properties don't change, make it const.

### Minimize Widget Rebuilds

Use `Obx` strategically to limit rebuild scope:

```dart
// ❌ BAD - Entire Column rebuilds
Obx(() => Column(
  children: [
    Text(controller.title.value),
    ExpensiveWidget(),
    AnotherExpensiveWidget(),
  ],
))

// ✅ GOOD - Only Text rebuilds
Column(
  children: [
    Obx(() => Text(controller.title.value)),
    const ExpensiveWidget(),
    const AnotherExpensiveWidget(),
  ],
)
```

### Proper Key Usage

Keys help Flutter identify which widgets to reuse:

```dart
// ❌ BAD - No keys, Flutter may rebuild unnecessarily
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(title: Text(items[index].name));
  },
)

// ✅ GOOD - ValueKey helps Flutter track items
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(
      key: ValueKey(items[index].id),
      title: Text(items[index].name),
    );
  },
)

// When to use keys:
// - ObjectKey: Compare entire object
// - ValueKey: Compare single value (id, index)
// - UniqueKey: Force rebuild
// - GlobalKey: Access widget state from anywhere (expensive, use sparingly)
```

### Extract Widgets

Extract complex widgets to reduce rebuild scope:

```dart
// ❌ BAD - All items rebuild when list changes
class MyList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Obx(() => ListView.builder(
      itemCount: controller.items.length,
      itemBuilder: (context, index) {
        final item = controller.items[index];
        return Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text(item.title),
              Text(item.subtitle),
              Row(
                children: [
                  Icon(Icons.star),
                  Text('${item.rating}'),
                ],
              ),
            ],
          ),
        );
      },
    ));
  }
}

// ✅ GOOD - Extract item widget
class MyList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Obx(() => ListView.builder(
      itemCount: controller.items.length,
      itemBuilder: (context, index) {
        return ItemWidget(item: controller.items[index]);
      },
    ));
  }
}

class ItemWidget extends StatelessWidget {
  final Item item;
  const ItemWidget({Key? key, required this.item}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Text(item.title),
          Text(item.subtitle),
          Row(
            children: [
              const Icon(Icons.star),
              Text('${item.rating}'),
            ],
          ),
        ],
      ),
    );
  }
}
```

## List Performance

### Use ListView.builder

Never use `ListView(children: [...])` for large lists:

```dart
// ❌ BAD - All items created upfront
ListView(
  children: items.map((item) => ItemWidget(item: item)).toList(),
)

// ✅ GOOD - Items created on demand
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
)

// ✅ GOOD - Separated items (for sticky headers)
ListView.separated(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
  separatorBuilder: (context, index) => const Divider(),
)
```

### Optimize List Scroll Performance

```dart
// Add cacheExtent for smoother scrolling
ListView.builder(
  cacheExtent: 500, // Render items 500px off-screen
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
)

// Use addAutomaticKeepAlives: false if items don't need to preserve state
ListView.builder(
  addAutomaticKeepAlives: false,
  addRepaintBoundaries: true,
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
)
```

### Infinite Scroll / Pagination

```dart
class ProductListController extends GetxController {
  final _items = <Product>[].obs;
  List<Product> get items => _items;

  final _isLoading = false.obs;
  bool get isLoading => _isLoading.value;

  int _currentPage = 1;
  bool _hasMore = true;

  final ScrollController scrollController = ScrollController();

  @override
  void onInit() {
    super.onInit();
    loadItems();
    scrollController.addListener(_onScroll);
  }

  @override
  void onClose() {
    scrollController.dispose();
    super.onClose();
  }

  void _onScroll() {
    if (scrollController.position.pixels >=
        scrollController.position.maxScrollExtent - 200) {
      if (!_isLoading.value && _hasMore) {
        loadMore();
      }
    }
  }

  Future<void> loadItems() async {
    _isLoading.value = true;
    final result = await repository.getProducts(page: 1);
    result.fold(
      (failure) => {},
      (products) {
        _items.value = products;
        _hasMore = products.length >= 20; // Assuming page size of 20
      },
    );
    _isLoading.value = false;
  }

  Future<void> loadMore() async {
    _isLoading.value = true;
    _currentPage++;
    final result = await repository.getProducts(page: _currentPage);
    result.fold(
      (failure) => _currentPage--,
      (products) {
        _items.addAll(products);
        _hasMore = products.length >= 20;
      },
    );
    _isLoading.value = false;
  }
}
```

## Image Optimization

### Use cached_network_image

```dart
import 'package:cached_network_image/cached_network_image.dart';

// ❌ BAD - No caching, re-downloads every time
Image.network('https://example.com/image.jpg')

// ✅ GOOD - Cached, with placeholders
CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  fadeInDuration: const Duration(milliseconds: 300),
  memCacheWidth: 400, // Resize for memory efficiency
)
```

### Optimize Image Sizes

```dart
// Specify dimensions to avoid unnecessary rendering
CachedNetworkImage(
  imageUrl: product.imageUrl,
  width: 200,
  height: 200,
  fit: BoxFit.cover,
  memCacheWidth: 200 * 2, // 2x for high DPI displays
  memCacheHeight: 200 * 2,
)

// For list thumbnails, use lower resolution
CachedNetworkImage(
  imageUrl: product.thumbnailUrl, // Server-side thumbnail
  width: 50,
  height: 50,
  memCacheWidth: 100,
  memCacheHeight: 100,
)
```

### Precache Images

```dart
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  // Precache images that will be needed soon
  precacheImage(
    CachedNetworkImageProvider(product.imageUrl),
    context,
  );
}
```

## Memory Management

### Dispose Controllers and Listeners

```dart
class MyController extends GetxController {
  late final StreamSubscription _subscription;
  late final ScrollController scrollController;
  late final TextEditingController textController;

  @override
  void onInit() {
    super.onInit();
    scrollController = ScrollController();
    textController = TextEditingController();
    _subscription = someStream.listen((data) {
      // Handle data
    });
  }

  @override
  void onClose() {
    // CRITICAL: Dispose all resources
    scrollController.dispose();
    textController.dispose();
    _subscription.cancel();
    super.onClose();
  }
}
```

### Avoid Memory Leaks with GetX

```dart
// ❌ BAD - Permanent controller never disposed
Get.put(MyController(), permanent: true);

// ✅ GOOD - Controller disposed when not needed
Get.lazyPut(() => MyController());

// ✅ GOOD - Explicitly control lifecycle
Get.put(MyController(), tag: 'unique-tag');
// Later: Get.delete<MyController>(tag: 'unique-tag');
```

### Use WeakReference for Callbacks

```dart
class MyController extends GetxController {
  Timer? _timer;

  @override
  void onInit() {
    super.onInit();
    // Use WeakReference to avoid keeping controller alive
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (!isClosed) {
        updateData();
      }
    });
  }

  @override
  void onClose() {
    _timer?.cancel();
    super.onClose();
  }
}
```

## Lazy Loading and Code Splitting

### Deferred Imports

```dart
// feature_a.dart - Large feature module
import 'package:flutter/material.dart';

class FeatureAPage extends StatelessWidget {
  // Heavy feature implementation
}

// main.dart - Lazy load feature
import 'feature_a.dart' deferred as feature_a;

void navigateToFeatureA() async {
  await feature_a.loadLibrary(); // Load code on demand
  Get.to(() => feature_a.FeatureAPage());
}
```

### Lazy Controller Initialization

```dart
// ❌ BAD - All controllers loaded at startup
void main() {
  Get.put(HomeController());
  Get.put(ProfileController());
  Get.put(SettingsController());
  runApp(MyApp());
}

// ✅ GOOD - Controllers loaded when needed
class HomeBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => HomeController());
  }
}

GetPage(
  name: '/home',
  page: () => HomePage(),
  binding: HomeBinding(), // Loaded only when route accessed
)
```

## Animation Performance

### Use AnimatedWidget

```dart
// ❌ BAD - Rebuilds entire widget tree
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  Widget build(BuildContext context) {
    return Transform.scale(
      scale: _controller.value,
      child: ExpensiveWidget(), // Rebuilt every frame!
    );
  }
}

// ✅ GOOD - Only animated part rebuilds
class ScaleTransition extends AnimatedWidget {
  const ScaleTransition({
    required Animation<double> scale,
    required this.child,
  }) : super(listenable: scale);

  final Widget child;

  @override
  Widget build(BuildContext context) {
    final animation = listenable as Animation<double>;
    return Transform.scale(
      scale: animation.value,
      child: child,
    );
  }
}

// Usage
ScaleTransition(
  scale: _controller,
  child: const ExpensiveWidget(), // Not rebuilt!
)
```

### Limit Simultaneous Animations

```dart
// ❌ BAD - Too many simultaneous animations
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(100, (index) =>
        AnimatedContainer(
          duration: Duration(seconds: 1),
          // Each container animates independently
        ),
      ),
    );
  }
}

// ✅ GOOD - Stagger animations, limit concurrent
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return AnimatedList(
      initialItemCount: items.length,
      itemBuilder: (context, index, animation) {
        return FadeTransition(
          opacity: animation,
          child: ItemWidget(item: items[index]),
        );
      },
    );
  }
}
```

## Profiling and Debugging

### Use Flutter DevTools

```bash
# Run app in profile mode (not debug!)
flutter run --profile

# Open DevTools
# Press 'w' in terminal or visit: http://localhost:9100
```

**Key DevTools Features**:
- **Performance**: Identify janky frames, long build times
- **Memory**: Track heap usage, find leaks
- **Network**: Monitor API calls, payload sizes
- **Timeline**: Visualize frame rendering

### Identify Build Performance Issues

```dart
// Add debug print to measure build time
@override
Widget build(BuildContext context) {
  final stopwatch = Stopwatch()..start();

  final widget = ExpensiveWidget();

  if (kDebugMode) {
    print('Build took: ${stopwatch.elapsedMilliseconds}ms');
  }

  return widget;
}
```

### Performance Overlay

```dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      showPerformanceOverlay: true, // Shows FPS graphs
      home: HomePage(),
    );
  }
}
```

## Best Practices Checklist

### Widget Optimization
- [ ] Use `const` constructors wherever possible
- [ ] Minimize `Obx` scope to smallest widget
- [ ] Extract complex widgets into separate classes
- [ ] Use proper keys for list items
- [ ] Avoid unnecessary `setState` or `update()` calls

### List Performance
- [ ] Always use `ListView.builder` for dynamic lists
- [ ] Implement pagination for large datasets
- [ ] Add `cacheExtent` for smoother scrolling
- [ ] Use `addAutomaticKeepAlives: false` when appropriate

### Image Performance
- [ ] Use `cached_network_image` for network images
- [ ] Specify image dimensions
- [ ] Use appropriate image resolutions
- [ ] Precache critical images

### Memory Management
- [ ] Dispose all controllers in `onClose()`
- [ ] Cancel stream subscriptions
- [ ] Dispose animation controllers
- [ ] Use `lazyPut` instead of `put` for GetX controllers

### Code Organization
- [ ] Use deferred imports for large features
- [ ] Lazy-load controllers with bindings
- [ ] Split large files into smaller modules

### Animation
- [ ] Use `AnimatedWidget` for custom animations
- [ ] Limit simultaneous animations to 2-3
- [ ] Use `RepaintBoundary` for expensive widgets
- [ ] Prefer implicit animations (`AnimatedContainer`, `AnimatedOpacity`)

### Profiling
- [ ] Test in profile mode (not debug)
- [ ] Use Flutter DevTools regularly
- [ ] Monitor frame rendering times (< 16ms target)
- [ ] Check memory usage with DevTools
- [ ] Profile on real devices, not just emulators

## Common Performance Anti-Patterns

### Anti-Pattern 1: Unnecessary Rebuilds

```dart
// ❌ Obx wrapping entire screen
Obx(() => Scaffold(
  body: Column(children: [
    Text(controller.title.value),
    LargeWidget(),
  ]),
))

// ✅ Obx only on changing widget
Scaffold(
  body: Column(children: [
    Obx(() => Text(controller.title.value)),
    const LargeWidget(),
  ]),
)
```

### Anti-Pattern 2: Expensive Build Methods

```dart
// ❌ Heavy computation in build
@override
Widget build(BuildContext context) {
  final processedData = heavyComputation(rawData); // Runs every build!
  return Text(processedData);
}

// ✅ Compute once, cache result
class MyController extends GetxController {
  final _processedData = ''.obs;

  @override
  void onInit() {
    super.onInit();
    _processedData.value = heavyComputation(rawData);
  }
}
```

### Anti-Pattern 3: Not Disposing Resources

```dart
// ❌ Memory leak - controller never disposed
class MyController extends GetxController {
  final StreamController<int> _controller = StreamController();
  // Missing onClose() to dispose!
}

// ✅ Proper disposal
class MyController extends GetxController {
  final StreamController<int> _controller = StreamController();

  @override
  void onClose() {
    _controller.close();
    super.onClose();
  }
}
```

## Performance Targets

| Metric | Target | Tool |
|--------|--------|------|
| Frame time | < 16ms (60 FPS) | DevTools Performance |
| Build time | < 5ms for simple widgets | Debug prints |
| Memory usage | < 100MB typical screen | DevTools Memory |
| App startup | < 2 seconds | Stopwatch |
| Image load | < 1 second | Network tab |
| API response | < 500ms | Network tab |
