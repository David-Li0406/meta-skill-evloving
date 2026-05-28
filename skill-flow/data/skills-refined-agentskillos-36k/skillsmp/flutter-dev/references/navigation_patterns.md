# Navigation Patterns

Advanced navigation patterns and examples using GoRouter.

## Authentication Redirects

Configure GoRouter's redirect to handle authentication flows:

```dart
final GoRouter _router = GoRouter(
  redirect: (context, state) {
    final bool isLoggedIn = authService.isLoggedIn;
    final bool isGoingToLogin = state.matchedLocation == '/login';
    
    if (!isLoggedIn && !isGoingToLogin) {
      return '/login';
    }
    
    if (isLoggedIn && isGoingToLogin) {
      return '/';
    }
    
    return null; // No redirect needed
  },
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
  ],
);
```

## Nested Navigation

Handle tab bars and nested navigators:

```dart
final GoRouter _router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return ScaffoldWithNavBar(child: child);
      },
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeTab(),
          routes: [
            GoRoute(
              path: 'details/:id',
              builder: (context, state) {
                final id = state.pathParameters['id']!;
                return DetailsScreen(id: id);
              },
            ),
          ],
        ),
        GoRoute(
          path: '/profile',
          builder: (context, state) => const ProfileTab(),
        ),
      ],
    ),
  ],
);
```

## Deep Linking

Handle deep links with query parameters:

```dart
GoRoute(
  path: '/product/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    final source = state.uri.queryParameters['source'];
    return ProductScreen(id: id, source: source);
  },
)
```

## Navigation Methods

```dart
// Navigate to a route
context.go('/details/123');

// Navigate with query parameters
context.go('/search?q=flutter');

// Push a route onto the stack
context.push('/details/123');

// Pop the current route
context.pop();

// Replace current route
context.replace('/login');

// Go back to a specific route
context.go('/');
```

## Error Handling

```dart
final GoRouter _router = GoRouter(
  errorBuilder: (context, state) => ErrorScreen(error: state.error),
  routes: [
    // routes
  ],
);
```

## Typed Routes (Type-Safe Navigation)

For type-safe navigation with code generation:

```dart
// Define typed routes
class HomeRoute extends GoRouteData {
  const HomeRoute();
  
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const HomeScreen();
  }
}

class DetailsRoute extends GoRouteData {
  const DetailsRoute(this.id);
  final String id;
  
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return DetailsScreen(id: id);
  }
}

// Navigate type-safely
const HomeRoute().go(context);
DetailsRoute('123').push(context);
```
