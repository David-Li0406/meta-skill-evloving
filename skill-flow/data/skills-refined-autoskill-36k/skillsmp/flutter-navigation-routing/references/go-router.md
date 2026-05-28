# GoRouter: Complete Implementation Guide

GoRouter is Flutter's recommended declarative routing package, built on Navigator 2.0. It provides a high-level API for implementing navigation with deep linking support, type-safe route definitions, and seamless web integration.

## Installation and Setup

### Adding GoRouter Dependency

Add GoRouter to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  go_router: ^14.0.0
```

Run `flutter pub get` to install the package.

### Basic Router Configuration

Create a router instance and provide it to MaterialApp.router:

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final GoRouter _router = GoRouter(
  routes: <RouteBase>[
    GoRoute(
      path: '/',
      builder: (BuildContext context, GoRouterState state) {
        return const HomeScreen();
      },
    ),
    GoRoute(
      path: '/details',
      builder: (BuildContext context, GoRouterState state) {
        return const DetailsScreen();
      },
    ),
  ],
);

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
    );
  }
}
```

### Router Options

GoRouter provides several configuration options:

```dart
final router = GoRouter(
  routes: routes,
  initialLocation: '/',
  errorBuilder: (context, state) => ErrorScreen(error: state.error),
  redirect: globalRedirectFunction,
  refreshListenable: authChangeNotifier,
  debugLogDiagnostics: true,
  navigatorKey: GlobalKey<NavigatorState>(),
  observers: [MyNavigatorObserver()],
);
```

**initialLocation:** The initial location to navigate to when the app starts. Defaults to '/'.

**errorBuilder:** Builder for the error screen shown when navigation fails or an invalid route is requested.

**redirect:** Global redirect function called before every navigation to potentially redirect to a different route.

**refreshListenable:** Listenable that triggers router refresh when notified, useful for authentication state changes.

**debugLogDiagnostics:** Enable debug logging for navigation events and routing decisions.

**navigatorKey:** Global key for the root Navigator, useful for showing dialogs or snackbars without context.

**observers:** List of NavigatorObserver instances for monitoring navigation events.

## Route Definition

### Simple Routes

Define routes with paths and builders:

```dart
GoRoute(
  path: '/settings',
  builder: (context, state) => const SettingsScreen(),
)
```

### Named Routes

Assign names to routes for type-safe navigation:

```dart
GoRoute(
  name: 'settings',
  path: '/settings',
  builder: (context, state) => const SettingsScreen(),
)

// Navigate using name
context.goNamed('settings');
```

### Path Parameters

Extract dynamic segments from the URL path:

```dart
GoRoute(
  path: '/user/:userId',
  builder: (context, state) {
    final userId = state.pathParameters['userId']!;
    return UserScreen(userId: userId);
  },
)

// Navigate with parameter
context.go('/user/123');
```

### Query Parameters

Access query string parameters from the URL:

```dart
GoRoute(
  path: '/search',
  builder: (context, state) {
    final query = state.uri.queryParameters['q'] ?? '';
    final filter = state.uri.queryParameters['filter'];
    return SearchScreen(query: query, filter: filter);
  },
)

// Navigate with query parameters
context.go('/search?q=flutter&filter=recent');

// Using named routes
context.goNamed(
  'search',
  queryParameters: {'q': 'flutter', 'filter': 'recent'},
);
```

### Multiple Path Parameters

Combine multiple path parameters:

```dart
GoRoute(
  path: '/organization/:orgId/project/:projectId',
  builder: (context, state) {
    final orgId = state.pathParameters['orgId']!;
    final projectId = state.pathParameters['projectId']!;
    return ProjectScreen(
      organizationId: orgId,
      projectId: projectId,
    );
  },
)

// Navigate
context.go('/organization/acme/project/flutter-app');
```

## Navigation Methods

### Declarative Navigation (go)

Replace the current route with a new one:

```dart
// Navigate to a path
context.go('/details');

// With path parameters
context.go('/user/123');

// With query parameters
context.go('/search?q=flutter');

// Using named routes
context.goNamed(
  'userDetails',
  pathParameters: {'userId': '123'},
  queryParameters: {'tab': 'profile'},
);
```

The `go` method provides declarative navigation where the navigation stack is determined by the URL. Navigating to the same URL has no effect.

### Imperative Navigation (push)

Push a new route onto the stack:

```dart
// Push a route
context.push('/details');

// Push with return value
final result = await context.push<String>('/editor');

// Using named routes
context.pushNamed('details');

// Push replacement
context.pushReplacement('/home');
```

The `push` method provides imperative navigation where routes are stacked on top of each other. This allows building up a navigation stack programmatically.

### Going Back

Navigate back in the navigation stack:

```dart
// Pop the current route
context.pop();

// Pop with a result value
context.pop('saved');

// Check if can pop
if (context.canPop()) {
  context.pop();
}
```

### Navigation Extras

Pass extra data alongside navigation:

```dart
context.go(
  '/details',
  extra: ComplexObject(/* ... */),
);

// Access in builder
GoRoute(
  path: '/details',
  builder: (context, state) {
    final data = state.extra as ComplexObject;
    return DetailsScreen(data: data);
  },
)
```

Note: Extra data is not part of the URL and will be lost on page refresh in web applications. Use path or query parameters for persistent data.

## Nested Routes

### Sub-routes

Define hierarchical route structures:

```dart
GoRoute(
  path: '/family',
  builder: (context, state) => const FamilyScreen(),
  routes: <RouteBase>[
    GoRoute(
      path: 'person/:personId',
      builder: (context, state) {
        final personId = state.pathParameters['personId']!;
        return PersonScreen(personId: personId);
      },
      routes: <RouteBase>[
        GoRoute(
          path: 'details',
          builder: (context, state) {
            final personId = state.pathParameters['personId']!;
            return PersonDetailsScreen(personId: personId);
          },
        ),
      ],
    ),
  ],
)
```

This creates the following route structure:
- `/family` - FamilyScreen
- `/family/person/123` - PersonScreen
- `/family/person/123/details` - PersonDetailsScreen

### Route Inheritance

Child routes inherit path parameters from parent routes:

```dart
GoRoute(
  path: '/project/:projectId',
  builder: (context, state) {
    final projectId = state.pathParameters['projectId']!;
    return ProjectScreen(projectId: projectId);
  },
  routes: [
    GoRoute(
      path: 'tasks/:taskId',
      builder: (context, state) {
        final projectId = state.pathParameters['projectId']!; // Inherited
        final taskId = state.pathParameters['taskId']!;
        return TaskScreen(projectId: projectId, taskId: taskId);
      },
    ),
  ],
)
```

## ShellRoute for Persistent UI

ShellRoute wraps child routes with persistent UI elements like navigation bars or drawers:

```dart
ShellRoute(
  builder: (context, state, child) {
    return ScaffoldWithNavBar(body: child);
  },
  routes: [
    GoRoute(
      path: '/home',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
)
```

The `child` parameter in the builder contains the current route's widget, wrapped by the persistent UI.

### Complete ShellRoute Example

```dart
class ScaffoldWithNavBar extends StatelessWidget {
  const ScaffoldWithNavBar({required this.child, super.key});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _calculateSelectedIndex(context),
        onTap: (index) => _onItemTapped(index, context),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
        ],
      ),
    );
  }

  int _calculateSelectedIndex(BuildContext context) {
    final location = GoRouterState.of(context).uri.toString();
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/settings')) return 1;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.go('/home');
        break;
      case 1:
        context.go('/settings');
        break;
    }
  }
}
```

## StatefulShellRoute for Bottom Navigation

StatefulShellRoute maintains separate navigation stacks for each branch, perfect for bottom navigation with preserved state:

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) {
    return ScaffoldWithNavBar(navigationShell: navigationShell);
  },
  branches: [
    StatefulShellBranch(
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
          routes: [
            GoRoute(
              path: 'details',
              builder: (context, state) => const HomeDetailsScreen(),
            ),
          ],
        ),
      ],
    ),
    StatefulShellBranch(
      routes: [
        GoRoute(
          path: '/explore',
          builder: (context, state) => const ExploreScreen(),
        ),
      ],
    ),
    StatefulShellBranch(
      routes: [
        GoRoute(
          path: '/profile',
          builder: (context, state) => const ProfileScreen(),
        ),
      ],
    ),
  ],
)
```

### StatefulShellRoute Builder Widget

```dart
class ScaffoldWithNavBar extends StatelessWidget {
  const ScaffoldWithNavBar({
    required this.navigationShell,
    super.key,
  });

  final StatefulNavigationShell navigationShell;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: navigationShell.currentIndex,
        onTap: (index) => navigationShell.goBranch(
          index,
          initialLocation: index == navigationShell.currentIndex,
        ),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.explore), label: 'Explore'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
```

### StatefulShellRoute Features

**Preserved Navigation State:** Each branch maintains its own navigation stack and scroll position.

**Initial Location:** Use `initialLocation: true` in `goBranch` to always navigate to the branch's root route.

**Branch Switching:** Switch between branches with `navigationShell.goBranch(index)`.

**Current Index:** Access the active branch with `navigationShell.currentIndex`.

**Multiple Navigators:** Each branch has its own Navigator for independent navigation stacks.

## Redirects and Route Guards

### Global Redirects

Define a global redirect function that runs before every navigation:

```dart
GoRouter(
  redirect: (context, state) {
    final isAuthenticated = AuthService.instance.isAuthenticated;
    final isAuthRoute = state.matchedLocation == '/login';

    // Redirect to login if not authenticated
    if (!isAuthenticated && !isAuthRoute) {
      return '/login';
    }

    // Redirect away from login if already authenticated
    if (isAuthenticated && isAuthRoute) {
      return '/';
    }

    // No redirect needed
    return null;
  },
  routes: routes,
)
```

Return `null` to allow navigation to the requested route, or return a path string to redirect to a different route.

### Route-Level Redirects

Define redirects on specific routes:

```dart
GoRoute(
  path: '/admin',
  redirect: (context, state) {
    final isAdmin = AuthService.instance.isAdmin;
    if (!isAdmin) {
      return '/unauthorized';
    }
    return null;
  },
  builder: (context, state) => const AdminScreen(),
)
```

### Redirect Execution Order

Redirects execute in this order:
1. Global redirect (defined on GoRouter)
2. Route-level redirect (defined on GoRoute)
3. Parent route redirects before child route redirects

### Refresh on State Changes

Update routing when application state changes:

```dart
class AuthNotifier extends ChangeNotifier {
  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;

  void login() {
    _isAuthenticated = true;
    notifyListeners(); // Triggers router refresh
  }

  void logout() {
    _isAuthenticated = false;
    notifyListeners(); // Triggers router refresh
  }
}

final authNotifier = AuthNotifier();

final router = GoRouter(
  refreshListenable: authNotifier,
  redirect: (context, state) {
    final isAuthenticated = authNotifier.isAuthenticated;
    // Redirect logic
  },
  routes: routes,
);
```

### Redirect Limits

GoRouter limits redirects to prevent infinite loops:

```dart
GoRouter(
  redirectLimit: 10, // Default is 5
  redirect: redirectFunction,
  routes: routes,
)
```

If the limit is exceeded, GoRouter shows an error screen.

## State Management Integration

### Integration with Riverpod

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Auth state provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});

// Router provider with auth integration
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    refreshListenable: GoRouterRefreshStream(
      ref.watch(authProvider.notifier).stream,
    ),
    redirect: (context, state) {
      final isAuthenticated = authState.isAuthenticated;
      final isAuthRoute = state.matchedLocation.startsWith('/auth');

      if (!isAuthenticated && !isAuthRoute) {
        return '/auth/login';
      }
      if (isAuthenticated && isAuthRoute) {
        return '/';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/auth/login',
        builder: (context, state) => const LoginScreen(),
      ),
    ],
  );
});

// App with Riverpod
class MyApp extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      routerConfig: router,
    );
  }
}
```

### Helper Class for Stream Conversion

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';

class GoRouterRefreshStream extends ChangeNotifier {
  GoRouterRefreshStream(Stream<dynamic> stream) {
    notifyListeners();
    _subscription = stream.asBroadcastStream().listen(
      (dynamic _) => notifyListeners(),
    );
  }

  late final StreamSubscription<dynamic> _subscription;

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
}
```

### Integration with Bloc

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class MyApp extends StatelessWidget {
  final AuthBloc authBloc;

  MyApp({required this.authBloc});

  @override
  Widget build(BuildContext context) {
    return BlocProvider.value(
      value: authBloc,
      child: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          final router = GoRouter(
            refreshListenable: GoRouterRefreshStream(authBloc.stream),
            redirect: (context, state) {
              final authState = context.read<AuthBloc>().state;

              if (authState is Unauthenticated &&
                  !state.matchedLocation.startsWith('/login')) {
                return '/login';
              }
              return null;
            },
            routes: routes,
          );

          return MaterialApp.router(
            routerConfig: router,
          );
        },
      ),
    );
  }
}
```

### Integration with Provider

```dart
import 'package:provider/provider.dart';

class AuthService extends ChangeNotifier {
  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;

  Future<void> login() async {
    // Login logic
    _isAuthenticated = true;
    notifyListeners();
  }

  Future<void> logout() async {
    // Logout logic
    _isAuthenticated = false;
    notifyListeners();
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthService(),
      child: Consumer<AuthService>(
        builder: (context, authService, _) {
          final router = GoRouter(
            refreshListenable: authService,
            redirect: (context, state) {
              final isAuthenticated = authService.isAuthenticated;
              final isAuthRoute = state.matchedLocation == '/login';

              if (!isAuthenticated && !isAuthRoute) {
                return '/login';
              }
              if (isAuthenticated && isAuthRoute) {
                return '/';
              }
              return null;
            },
            routes: routes,
          );

          return MaterialApp.router(
            routerConfig: router,
          );
        },
      ),
    );
  }
}
```

## Error Handling

### Custom Error Screen

Define a custom error builder for invalid routes:

```dart
GoRouter(
  errorBuilder: (context, state) {
    return ErrorScreen(
      error: state.error,
      path: state.uri.toString(),
    );
  },
  routes: routes,
)
```

### Error Screen Implementation

```dart
class ErrorScreen extends StatelessWidget {
  const ErrorScreen({
    required this.error,
    required this.path,
    super.key,
  });

  final Exception? error;
  final String path;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Error')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              'Page not found',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text('Could not navigate to: $path'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => context.go('/'),
              child: const Text('Go Home'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Transition Animations

### Custom Page Transitions

Customize route transition animations:

```dart
GoRoute(
  path: '/details',
  pageBuilder: (context, state) {
    return CustomTransitionPage(
      key: state.pageKey,
      child: const DetailsScreen(),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: animation,
          child: child,
        );
      },
    );
  },
)
```

### Material Page Transitions

Use platform-appropriate Material transitions:

```dart
GoRoute(
  path: '/details',
  pageBuilder: (context, state) {
    return MaterialPage(
      key: state.pageKey,
      child: const DetailsScreen(),
    );
  },
)
```

### Cupertino Page Transitions

Use iOS-style transitions:

```dart
GoRoute(
  path: '/details',
  pageBuilder: (context, state) {
    return CupertinoPage(
      key: state.pageKey,
      child: const DetailsScreen(),
    );
  },
)
```

## Deep Linking

GoRouter automatically handles deep linking when properly configured. The route structure defines the URL structure:

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'products/:productId',
          builder: (context, state) {
            final productId = state.pathParameters['productId']!;
            return ProductScreen(productId: productId);
          },
        ),
      ],
    ),
  ],
);
```

This configuration automatically handles:
- `myapp://` - Opens HomeScreen
- `myapp://products/123` - Opens ProductScreen with productId='123'
- `https://myapp.com/products/123` - Opens ProductScreen (with proper platform configuration)

Platform-specific configuration is required to enable deep linking. See the deep-linking reference for Android App Links and iOS Universal Links setup.

## Testing

### Testing Routes

Test route navigation in widget tests:

```dart
testWidgets('Navigate to details screen', (tester) async {
  final router = GoRouter(
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/details',
        builder: (context, state) => const DetailsScreen(),
      ),
    ],
  );

  await tester.pumpWidget(
    MaterialApp.router(
      routerConfig: router,
    ),
  );

  // Verify initial route
  expect(find.byType(HomeScreen), findsOneWidget);

  // Navigate to details
  router.go('/details');
  await tester.pumpAndSettle();

  // Verify navigation
  expect(find.byType(DetailsScreen), findsOneWidget);
});
```

### Testing Redirects

Test redirect logic:

```dart
testWidgets('Redirects to login when not authenticated', (tester) async {
  final authNotifier = AuthNotifier();

  final router = GoRouter(
    refreshListenable: authNotifier,
    redirect: (context, state) {
      if (!authNotifier.isAuthenticated &&
          state.matchedLocation != '/login') {
        return '/login';
      }
      return null;
    },
    routes: routes,
  );

  await tester.pumpWidget(
    MaterialApp.router(
      routerConfig: router,
    ),
  );

  // Attempt to navigate to protected route
  router.go('/profile');
  await tester.pumpAndSettle();

  // Should be redirected to login
  expect(find.byType(LoginScreen), findsOneWidget);
});
```

## Best Practices

**Use named routes** for type-safe navigation and easier refactoring across large applications.

**Prefer path parameters** for essential route data and query parameters for optional filters or settings.

**Keep route hierarchy shallow** to avoid overly complex URL structures and navigation logic.

**Implement global redirects** for authentication rather than checking auth state in individual screens.

**Use StatefulShellRoute** for bottom navigation to preserve navigation state in each tab.

**Define routes in a separate file** to keep routing configuration organized and maintainable.

**Test navigation flows** including edge cases like authentication redirects and deep links.

**Use extra carefully** as it's not persistent across page refreshes on web platforms.

**Leverage refreshListenable** to automatically update routes when application state changes.

**Set appropriate redirectLimit** based on your redirect complexity to catch infinite loops early.

GoRouter provides a powerful, declarative approach to navigation in Flutter applications. Its integration with Navigator 2.0 enables sophisticated routing scenarios while maintaining a clean, maintainable API. The combination of nested routes, state management integration, and built-in deep linking support makes GoRouter the recommended solution for most Flutter applications.
