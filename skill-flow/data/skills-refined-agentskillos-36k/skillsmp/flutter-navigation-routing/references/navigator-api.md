# Navigator 2.0 API Reference

Navigator 2.0 represents Flutter's declarative routing architecture, providing fine-grained control over navigation state and deep linking. While most applications should use GoRouter, understanding Navigator 2.0's underlying architecture is valuable for custom navigation requirements.

## Architecture Overview

Navigator 2.0 introduces a declarative paradigm where the navigation stack is a function of application state. The architecture consists of four primary components:

**Router:** The top-level widget that configures the Navigator based on application state and platform information.

**RouteInformationProvider:** Provides route information from the platform (URLs from the browser or deep links from the OS).

**RouteInformationParser:** Converts route information into a user-defined configuration type.

**RouterDelegate:** Builds the Navigator with the current page stack based on the configuration.

**BackButtonDispatcher:** Handles platform back button events and dispatches them to the Router.

### Data Flow

1. Platform provides route information (URL or deep link)
2. RouteInformationProvider receives the information
3. RouteInformationParser converts it to app-specific configuration
4. RouterDelegate receives configuration and builds page stack
5. Navigator displays the pages
6. User interactions update app state
7. RouterDelegate rebuilds with new page stack

## Router Widget

The Router widget coordinates the routing system and is typically used through MaterialApp.router:

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routeInformationProvider: routeInformationProvider,
      routeInformationParser: routeInformationParser,
      routerDelegate: routerDelegate,
      backButtonDispatcher: backButtonDispatcher,
    );
  }
}
```

### Router Configuration

**routeInformationProvider:** Provides RouteInformation from the platform. Typically use the default `PlatformRouteInformationProvider`.

**routeInformationParser:** Converts RouteInformation to your configuration type. Must implement `RouteInformationParser<T>`.

**routerDelegate:** Builds the Navigator based on configuration. Must implement `RouterDelegate<T>`.

**backButtonDispatcher:** Handles back button events. Use `RootBackButtonDispatcher` for the root router.

## RouteInformation

RouteInformation represents a route location from the platform:

```dart
class RouteInformation {
  const RouteInformation({
    this.uri,
    this.state,
  });

  final Uri? uri;
  final Object? state;
}
```

**uri:** The location of the route, including path and query parameters.

**state:** Optional state information associated with the route (platform-specific).

### Creating RouteInformation

```dart
final routeInfo = RouteInformation(
  uri: Uri.parse('/products/123?view=details'),
);
```

## RouteInformationParser

RouteInformationParser converts RouteInformation to application-specific configuration:

```dart
class MyRouteInformationParser extends RouteInformationParser<AppRoutePath> {
  @override
  Future<AppRoutePath> parseRouteInformation(
    RouteInformation routeInformation,
  ) async {
    final uri = routeInformation.uri;

    // Handle '/'
    if (uri.pathSegments.isEmpty) {
      return AppRoutePath.home();
    }

    // Handle '/products/:id'
    if (uri.pathSegments.length == 2 && uri.pathSegments[0] == 'products') {
      final id = uri.pathSegments[1];
      return AppRoutePath.product(id);
    }

    // Handle unknown routes
    return AppRoutePath.unknown();
  }

  @override
  RouteInformation? restoreRouteInformation(AppRoutePath configuration) {
    if (configuration.isHomePage) {
      return RouteInformation(uri: Uri.parse('/'));
    }
    if (configuration.isProductPage) {
      return RouteInformation(
        uri: Uri.parse('/products/${configuration.productId}'),
      );
    }
    return null;
  }
}
```

### RouteInformationParser Methods

**parseRouteInformation:** Converts RouteInformation from the platform into your configuration type. This is called when the app starts or when a deep link is opened.

**restoreRouteInformation:** Converts your configuration type back into RouteInformation. This is called when the app state changes to update the browser URL.

### Configuration Class Example

Define a configuration class representing your app's routing state:

```dart
class AppRoutePath {
  final String? productId;
  final bool isUnknown;

  AppRoutePath.home()
      : productId = null,
        isUnknown = false;

  AppRoutePath.product(this.productId) : isUnknown = false;

  AppRoutePath.unknown()
      : productId = null,
        isUnknown = true;

  bool get isHomePage => productId == null && !isUnknown;
  bool get isProductPage => productId != null;
}
```

## RouterDelegate

RouterDelegate builds the Navigator widget based on the current configuration:

```dart
class MyRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey;

  String? _selectedProductId;
  bool _show404 = false;

  MyRouterDelegate() : navigatorKey = GlobalKey<NavigatorState>();

  // Current configuration
  @override
  AppRoutePath get currentConfiguration {
    if (_show404) {
      return AppRoutePath.unknown();
    }
    if (_selectedProductId != null) {
      return AppRoutePath.product(_selectedProductId!);
    }
    return AppRoutePath.home();
  }

  // Build the Navigator
  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      pages: [
        MaterialPage(
          key: const ValueKey('HomePage'),
          child: HomeScreen(
            onProductTapped: _handleProductTapped,
          ),
        ),
        if (_selectedProductId != null)
          MaterialPage(
            key: ValueKey(_selectedProductId),
            child: ProductScreen(
              productId: _selectedProductId!,
            ),
          ),
        if (_show404)
          const MaterialPage(
            key: ValueKey('UnknownPage'),
            child: UnknownScreen(),
          ),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }

        // Update state when page is popped
        _selectedProductId = null;
        _show404 = false;
        notifyListeners();

        return true;
      },
    );
  }

  // Handle new route information
  @override
  Future<void> setNewRoutePath(AppRoutePath configuration) async {
    if (configuration.isUnknown) {
      _selectedProductId = null;
      _show404 = true;
      return;
    }

    if (configuration.isProductPage) {
      _selectedProductId = configuration.productId;
      _show404 = false;
      return;
    }

    _selectedProductId = null;
    _show404 = false;
  }

  // Handle imperative navigation
  void _handleProductTapped(String productId) {
    _selectedProductId = productId;
    notifyListeners();
  }
}
```

### RouterDelegate Methods

**currentConfiguration:** Returns the current routing configuration. Called when the system needs to update the URL.

**build:** Builds the Navigator widget with the current page stack.

**setNewRoutePath:** Called when a new route is pushed from the outside (deep links, URL changes). Update app state to reflect the new route.

**onPopPage:** Called when a page is popped. Return true if the pop was successful, false otherwise. Update app state when pages are removed.

### Mixins

**ChangeNotifier:** Enables notifying listeners when navigation state changes, triggering rebuilds.

**PopNavigatorRouterDelegateMixin:** Provides default implementation for handling system back button. Requires `navigatorKey`.

## Page Class

The Page class represents a route in the Navigator's history:

```dart
class MaterialPage<T> extends Page<T> {
  const MaterialPage({
    required this.child,
    this.maintainState = true,
    this.fullscreenDialog = false,
    LocalKey? key,
    String? name,
    Object? arguments,
    String? restorationId,
  }) : super(
          key: key,
          name: name,
          arguments: arguments,
          restorationId: restorationId,
        );

  final Widget child;
  final bool maintainState;
  final bool fullscreenDialog;

  @override
  Route<T> createRoute(BuildContext context) {
    return MaterialPageRoute<T>(
      settings: this,
      builder: (BuildContext context) => child,
      maintainState: maintainState,
      fullscreenDialog: fullscreenDialog,
    );
  }
}
```

### Page Properties

**key:** Unique identifier for the page. Changes to the key indicate a different page.

**child:** The widget to display for this page.

**name:** Optional name for the route.

**arguments:** Optional data associated with the route.

**restorationId:** Identifier for state restoration.

**maintainState:** Whether the route should remain in memory when not visible.

**fullscreenDialog:** Whether the route is a fullscreen dialog.

### Custom Page Types

Create custom page types for different transition animations:

```dart
class FadeTransitionPage extends Page {
  const FadeTransitionPage({
    required this.child,
    LocalKey? key,
  }) : super(key: key);

  final Widget child;

  @override
  Route createRoute(BuildContext context) {
    return PageRouteBuilder(
      settings: this,
      pageBuilder: (context, animation, secondaryAnimation) => child,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: animation,
          child: child,
        );
      },
    );
  }
}
```

## Complete Implementation Example

### App Structure

```dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final MyRouterDelegate _routerDelegate = MyRouterDelegate();
  final MyRouteInformationParser _routeInformationParser =
      MyRouteInformationParser();

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Navigator 2.0 Example',
      routerDelegate: _routerDelegate,
      routeInformationParser: _routeInformationParser,
    );
  }

  @override
  void dispose() {
    _routerDelegate.dispose();
    super.dispose();
  }
}
```

### Book Store Example

Complete example with book listing and details:

```dart
// Configuration
class BookRoutePath {
  final int? bookId;
  final bool isUnknown;

  BookRoutePath.home()
      : bookId = null,
        isUnknown = false;

  BookRoutePath.details(this.bookId) : isUnknown = false;

  BookRoutePath.unknown()
      : bookId = null,
        isUnknown = true;

  bool get isHomePage => bookId == null && !isUnknown;
  bool get isDetailsPage => bookId != null;
}

// Parser
class BookRouteInformationParser extends RouteInformationParser<BookRoutePath> {
  @override
  Future<BookRoutePath> parseRouteInformation(
    RouteInformation routeInformation,
  ) async {
    final uri = routeInformation.uri;

    if (uri.pathSegments.isEmpty) {
      return BookRoutePath.home();
    }

    if (uri.pathSegments.length == 2) {
      if (uri.pathSegments[0] == 'book') {
        final id = int.tryParse(uri.pathSegments[1]);
        if (id != null) {
          return BookRoutePath.details(id);
        }
      }
    }

    return BookRoutePath.unknown();
  }

  @override
  RouteInformation? restoreRouteInformation(BookRoutePath configuration) {
    if (configuration.isUnknown) {
      return RouteInformation(uri: Uri.parse('/404'));
    }
    if (configuration.isHomePage) {
      return RouteInformation(uri: Uri.parse('/'));
    }
    if (configuration.isDetailsPage) {
      return RouteInformation(uri: Uri.parse('/book/${configuration.bookId}'));
    }
    return null;
  }
}

// Delegate
class BookRouterDelegate extends RouterDelegate<BookRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<BookRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey;

  final List<Book> books = [
    Book(1, 'Flutter in Action'),
    Book(2, 'Dart Programming'),
    Book(3, 'Mobile Development'),
  ];

  int? _selectedBookId;
  bool _show404 = false;

  BookRouterDelegate() : navigatorKey = GlobalKey<NavigatorState>();

  Book? get selectedBook {
    if (_selectedBookId == null) return null;
    return books.firstWhere((book) => book.id == _selectedBookId);
  }

  @override
  BookRoutePath get currentConfiguration {
    if (_show404) {
      return BookRoutePath.unknown();
    }
    if (_selectedBookId != null) {
      return BookRoutePath.details(_selectedBookId!);
    }
    return BookRoutePath.home();
  }

  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      pages: [
        MaterialPage(
          key: const ValueKey('BooksListPage'),
          child: BooksListScreen(
            books: books,
            onTapped: _handleBookTapped,
          ),
        ),
        if (_show404)
          const MaterialPage(
            key: ValueKey('UnknownPage'),
            child: UnknownScreen(),
          )
        else if (_selectedBookId != null)
          MaterialPage(
            key: ValueKey(_selectedBookId),
            child: BookDetailsScreen(book: selectedBook!),
          ),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }

        _selectedBookId = null;
        _show404 = false;
        notifyListeners();

        return true;
      },
    );
  }

  @override
  Future<void> setNewRoutePath(BookRoutePath configuration) async {
    if (configuration.isUnknown) {
      _selectedBookId = null;
      _show404 = true;
      return;
    }

    if (configuration.isDetailsPage) {
      final bookExists = books.any((book) => book.id == configuration.bookId);
      if (bookExists) {
        _selectedBookId = configuration.bookId;
        _show404 = false;
      } else {
        _show404 = true;
      }
      return;
    }

    _selectedBookId = null;
    _show404 = false;
  }

  void _handleBookTapped(Book book) {
    _selectedBookId = book.id;
    notifyListeners();
  }
}

// Models
class Book {
  final int id;
  final String title;

  Book(this.id, this.title);
}

// Screens
class BooksListScreen extends StatelessWidget {
  final List<Book> books;
  final ValueChanged<Book> onTapped;

  const BooksListScreen({
    required this.books,
    required this.onTapped,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Books')),
      body: ListView.builder(
        itemCount: books.length,
        itemBuilder: (context, index) {
          final book = books[index];
          return ListTile(
            title: Text(book.title),
            onTap: () => onTapped(book),
          );
        },
      ),
    );
  }
}

class BookDetailsScreen extends StatelessWidget {
  final Book book;

  const BookDetailsScreen({required this.book, super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(book.title)),
      body: Center(
        child: Text('Details for ${book.title}'),
      ),
    );
  }
}

class UnknownScreen extends StatelessWidget {
  const UnknownScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('404')),
      body: const Center(
        child: Text('Page not found'),
      ),
    );
  }
}
```

## Nested Navigation

Navigator 2.0 supports nested navigators for complex navigation hierarchies:

```dart
class NestedRouterDelegate extends RouterDelegate<NestedRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<NestedRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey;

  int _selectedTab = 0;
  final List<GlobalKey<NavigatorState>> _tabNavigatorKeys = [
    GlobalKey<NavigatorState>(),
    GlobalKey<NavigatorState>(),
  ];

  NestedRouterDelegate() : navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedTab,
        children: [
          _buildTabNavigator(0),
          _buildTabNavigator(1),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedTab,
        onTap: (index) {
          _selectedTab = index;
          notifyListeners();
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
        ],
      ),
    );
  }

  Widget _buildTabNavigator(int tabIndex) {
    return Navigator(
      key: _tabNavigatorKeys[tabIndex],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }
        notifyListeners();
        return true;
      },
      pages: _getTabPages(tabIndex),
    );
  }

  List<Page> _getTabPages(int tabIndex) {
    if (tabIndex == 0) {
      return [
        const MaterialPage(
          child: HomeTabScreen(),
        ),
      ];
    } else {
      return [
        const MaterialPage(
          child: SettingsTabScreen(),
        ),
      ];
    }
  }

  @override
  Future<void> setNewRoutePath(NestedRoutePath configuration) async {
    _selectedTab = configuration.tabIndex;
  }

  @override
  NestedRoutePath get currentConfiguration {
    return NestedRoutePath(_selectedTab);
  }
}
```

## Authentication Flow

Implement authentication-aware routing:

```dart
class AuthenticatedRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey;

  final AuthService authService;
  String? _selectedRoute;

  AuthenticatedRouterDelegate({required this.authService})
      : navigatorKey = GlobalKey<NavigatorState>() {
    authService.addListener(notifyListeners);
  }

  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      pages: [
        // Show login if not authenticated
        if (!authService.isAuthenticated)
          const MaterialPage(
            key: ValueKey('LoginPage'),
            child: LoginScreen(),
          )
        // Show app pages if authenticated
        else ...[
          const MaterialPage(
            key: ValueKey('HomePage'),
            child: HomeScreen(),
          ),
          if (_selectedRoute == '/profile')
            const MaterialPage(
              key: ValueKey('ProfilePage'),
              child: ProfileScreen(),
            ),
        ],
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }

        _selectedRoute = null;
        notifyListeners();

        return true;
      },
    );
  }

  @override
  Future<void> setNewRoutePath(AppRoutePath configuration) async {
    _selectedRoute = configuration.path;
  }

  @override
  AppRoutePath get currentConfiguration {
    if (!authService.isAuthenticated) {
      return AppRoutePath('/login');
    }
    return AppRoutePath(_selectedRoute ?? '/');
  }

  @override
  void dispose() {
    authService.removeListener(notifyListeners);
    super.dispose();
  }
}
```

## State Restoration

Implement state restoration for web apps:

```dart
class RestorationRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey;

  String? _selectedRoute;

  RestorationRouterDelegate() : navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      restorationScopeId: 'app',
      pages: [
        const MaterialPage(
          key: ValueKey('HomePage'),
          child: HomeScreen(),
          restorationId: 'home',
        ),
        if (_selectedRoute != null)
          MaterialPage(
            key: ValueKey(_selectedRoute),
            child: DetailScreen(route: _selectedRoute!),
            restorationId: _selectedRoute,
          ),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }
        _selectedRoute = null;
        notifyListeners();
        return true;
      },
    );
  }

  @override
  Future<void> setNewRoutePath(AppRoutePath configuration) async {
    _selectedRoute = configuration.path;
  }

  @override
  AppRoutePath get currentConfiguration {
    return AppRoutePath(_selectedRoute ?? '/');
  }
}
```

## Best Practices

**Use GoRouter instead** for most applications as it provides a higher-level API with less boilerplate.

**Implement Navigator 2.0 directly** only when you need full control over navigation logic not provided by routing packages.

**Keep configuration types simple** with clear serialization/deserialization to RouteInformation.

**Handle unknown routes** gracefully by showing 404 pages rather than crashing.

**Use unique keys** for Page objects to help Flutter identify which pages changed.

**Validate route parameters** in setNewRoutePath before updating state to handle invalid URLs.

**Dispose listeners** properly to avoid memory leaks when RouterDelegate is disposed.

**Separate concerns** by keeping routing configuration distinct from UI code.

**Test thoroughly** including deep links, back button behavior, and state restoration.

**Document the routing architecture** to help team members understand the navigation flow.

## When to Use Navigator 2.0

Use Navigator 2.0 directly when:

- Building a routing package or library
- Requiring navigation logic not supported by existing packages
- Learning Flutter's routing architecture at a deep level
- Needing fine-grained control over page transitions and state

For application development, prefer GoRouter or other high-level routing packages that build on Navigator 2.0's foundation while providing cleaner APIs and reducing boilerplate code.

Navigator 2.0 provides the foundation for Flutter's declarative routing, enabling sophisticated navigation scenarios with deep linking and web support. Understanding its architecture helps developers make informed decisions about routing solutions and debug navigation issues effectively.
