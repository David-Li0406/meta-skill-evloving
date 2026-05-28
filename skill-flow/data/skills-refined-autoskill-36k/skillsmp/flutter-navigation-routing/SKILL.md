---
name: flutter-navigation-routing
description: Expert guidance on implementing navigation and routing in Flutter applications with declarative routing patterns, GoRouter integration, deep linking, route guards, and complex navigation flows. Use when implementing navigation, setting up routing, or handling deep links.
version: 1.0.0
---

# Flutter Navigation and Routing

Expert guidance on implementing navigation and routing in Flutter applications, covering declarative routing patterns, GoRouter integration, deep linking, and complex navigation flows.

## When to Use This Skill

Use this skill when working with:

- Setting up navigation architecture in new Flutter applications
- Migrating from Navigator 1.0 to declarative routing approaches
- Implementing GoRouter for type-safe, declarative navigation
- Configuring deep linking for Android App Links and iOS Universal Links
- Building authenticated routing flows with route guards
- Creating nested navigation with bottom navigation bars or drawer menus
- Handling route state management and navigation preservation
- Implementing web-compatible navigation with URL-based routing

## Navigation Approaches in Flutter

Flutter provides multiple navigation paradigms, each suited to different application requirements and complexity levels.

### Navigator 1.0 (Imperative Navigation)

The traditional Navigator API uses an imperative approach where screens are managed as a stack with platform-appropriate transitions. This approach is straightforward for simple applications:

```dart
// Push a new route
Navigator.of(context).push(
  MaterialPageRoute<void>(
    builder: (context) => const DetailScreen(),
  ),
);

// Return to previous route
Navigator.of(context).pop();
```

Navigator 1.0 is suitable for applications with simple linear navigation flows without deep linking requirements. It offers low complexity, direct control over the navigation stack, and simple data passing between screens.

**When to use Navigator 1.0:**
- Prototypes and simple applications
- Linear navigation flows
- No web deployment or deep linking requirements
- Quick implementation needs

**Limitations:**
- Limited deep linking support
- No declarative route configuration
- Difficult to synchronize with browser history on web
- Cannot easily prevent back navigation based on app state

### Named Routes (Legacy Pattern)

Named routes provide a map-based routing system where routes are registered in MaterialApp and navigated to by string identifiers:

```dart
MaterialApp(
  routes: {
    '/': (context) => const HomeScreen(),
    '/details': (context) => const DetailScreen(),
  },
  onGenerateRoute: (settings) {
    // Handle dynamic route arguments
  },
)

// Navigate using route name
Navigator.pushNamed(context, '/details');
```

**Important:** Named routes are no longer recommended by the Flutter team for most applications. They cannot customize deep link behavior, lack browser forward button support, and always push new routes regardless of the user's current location.

### Navigator 2.0 and Router API (Declarative Navigation)

Navigator 2.0 introduces a declarative routing paradigm where the displayed screens are a function of application state. This approach integrates seamlessly with deep linking and web navigation:

```dart
MaterialApp.router(
  routerConfig: router,
)
```

The Router API requires implementing several components:

**Router:** Configures the list of pages to be displayed by the Navigator based on application state and platform information.

**RouteInformationParser:** Converts route information from the platform (like URLs) into a user-defined configuration object.

**RouterDelegate:** Responds to changes in app state and route information, building the Navigator with the appropriate page stack.

**BackButtonDispatcher:** Reports back button presses to the Router.

Navigator 2.0 provides full control over navigation state, deep linking support, browser integration for web apps, and declarative route configuration. However, it requires significant boilerplate code and has a steeper learning curve.

**When to use Navigator 2.0:**
- Applications requiring custom navigation logic
- Full control over the navigation stack needed
- Learning the underlying Flutter navigation architecture

### GoRouter (Recommended Declarative Solution)

GoRouter is the official recommendation from the Flutter team for most applications requiring declarative routing. It provides a high-level API built on Navigator 2.0 that eliminates boilerplate while offering powerful features:

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailScreen(id: id);
          },
        ),
      ],
    ),
  ],
);

// Navigate declaratively
context.go('/details/123');
context.push('/settings');
```

GoRouter offers URL-based navigation with path and query parameters, nested and stacked routes, route-level and global redirects for authentication, deep linking support for web and mobile, type-safe route definitions, ShellRoute for persistent UI elements, and StatefulShellRoute for bottom navigation with preserved state.

**When to use GoRouter:**
- Most new Flutter applications
- Web applications requiring URL-based routing
- Apps with deep linking requirements
- Applications needing authentication flows
- Complex navigation with nested routes
- Bottom navigation with preserved tab state

## Key Navigation Concepts

### Route Stack Management

Flutter's navigation system manages screens in a stack structure. Each navigation operation modifies this stack:

**Push:** Adds a new route on top of the stack, displaying the new screen while keeping the previous one in memory.

**Pop:** Removes the top route from the stack, returning to the previous screen.

**Replace:** Replaces the current route with a new one without increasing stack depth.

**PopUntil:** Removes routes until a specified condition is met, useful for returning to a specific screen in the stack.

### Data Passing Between Routes

Different navigation approaches handle data passing differently:

**Constructor parameters** work with direct Navigator.push calls, providing type safety and compile-time checking.

**Route arguments** work with named routes and GoRouter, allowing dynamic data passing with runtime type checking.

**State management** provides app-wide state access, useful for complex data sharing across multiple screens.

**Return values** enable data flow back from popped routes using Navigator.pop with a result value.

### Deep Linking

Deep linking allows external sources to open specific screens within your application using URLs. This is essential for:

- Web applications where each screen should have a unique URL
- Marketing campaigns linking to specific app content
- Push notifications directing users to relevant screens
- Platform integration features like Spotlight search on iOS

**Android App Links:** Verified HTTPS URLs that open directly in your app without disambiguation dialogs, requiring domain verification through assetlinks.json.

**iOS Universal Links:** Verified HTTPS URLs associated with your domain, requiring apple-app-site-association file hosted on your website.

**Custom URL schemes:** App-specific URLs (myapp://) that work without domain verification but may show disambiguation if multiple apps register the same scheme.

### Route Guards and Authentication

Route guards protect routes from unauthorized access by checking authentication state before navigation:

```dart
GoRouter(
  redirect: (context, state) {
    final isAuthenticated = /* check auth state */;
    final isAuthRoute = state.matchedLocation == '/login';

    if (!isAuthenticated && !isAuthRoute) {
      return '/login';
    }
    if (isAuthenticated && isAuthRoute) {
      return '/';
    }
    return null; // No redirect needed
  },
  refreshListenable: authChangeNotifier,
)
```

Route guards enable preventing unauthorized access, redirecting to login screens, protecting sensitive routes, and handling authentication state changes during navigation.

## Choosing the Right Navigation Approach

For new applications, use GoRouter unless you have specific requirements for custom navigation logic. GoRouter provides the best balance of features, maintainability, and developer experience.

For existing applications with Navigator 1.0, migrate incrementally by introducing GoRouter in new features while maintaining existing imperative navigation for legacy screens.

For simple prototypes, Navigator 1.0 with MaterialPageRoute is acceptable for quick development without long-term maintenance concerns.

Avoid named routes in new code as they are legacy features with limited capabilities compared to modern alternatives.

For web applications, GoRouter or Navigator 2.0 is required for proper URL synchronization and browser integration.

## Integration Patterns

### State Management Integration

GoRouter integrates seamlessly with state management solutions:

**With Riverpod:**
```dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    redirect: (context, state) {
      // Access Riverpod state for routing decisions
    },
    refreshListenable: authState,
  );
});
```

**With Bloc:**
```dart
GoRouter(
  refreshListenable: GoRouterRefreshStream(authBloc.stream),
  redirect: (context, state) {
    final authState = context.read<AuthBloc>().state;
    // Routing logic based on Bloc state
  },
)
```

**With Provider:**
```dart
GoRouter(
  refreshListenable: authService,
  redirect: (context, state) {
    // Access Provider state for routing decisions
  },
)
```

### Nested Navigation Patterns

StatefulShellRoute enables persistent navigation state across bottom navigation tabs:

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

This pattern preserves scroll position, form state, and navigation history within each tab, providing a native app experience.

## Best Practices

**Start with GoRouter** for new applications to establish proper routing architecture from the beginning.

**Plan deep linking early** as retrofitting deep linking into applications designed without it requires significant refactoring.

**Use type-safe parameters** with GoRouter's path parameters rather than passing complex objects through route state.

**Implement route guards** at the GoRouter level rather than checking authentication in individual screens.

**Separate navigation logic** from UI code by defining routes in a dedicated routing configuration file.

**Test navigation flows** including deep linking, back button behavior, and authentication redirects across platforms.

**Consider web requirements** even for mobile-first apps, as GoRouter's URL-based routing enables easy web deployment.

**Preserve navigation state** in bottom navigation apps using StatefulShellRoute to maintain user context when switching tabs.

**Handle navigation errors** gracefully with custom error pages for invalid routes or failed redirects.

**Document route structure** especially in applications with complex nested navigation hierarchies.

## Related Skills and References

See `references/go-router.md` for comprehensive GoRouter implementation guide covering route configuration, nested routes, redirects, and state management integration.

See `references/navigator-api.md` for detailed Navigator 2.0 architecture including Router, RouterDelegate, and RouteInformationParser.

See `references/deep-linking.md` for platform-specific deep linking configuration for Android App Links and iOS Universal Links.

See `references/route-guards.md` for authentication flow patterns including login redirects and protected routes.

See `examples/authenticated-routing.md` for complete authentication flow implementation with GoRouter.

See `examples/nested-navigation.md` for tab-based navigation with StatefulShellRoute and preserved navigation state.

## Common Pitfalls

**Mixing navigation paradigms:** Avoid combining named routes with GoRouter or mixing imperative and declarative approaches inconsistently.

**Forgetting browser integration:** Web apps require declarative routing for proper back/forward button and URL synchronization.

**Complex route arguments:** Prefer path parameters and query parameters over passing complex objects through route state.

**Not handling authentication redirects:** Route guards should be comprehensive, covering all navigation scenarios including initial app launch.

**Ignoring platform differences:** Deep linking configuration differs significantly between Android and iOS, requiring platform-specific setup.

**Overusing nested routes:** Deep nesting can complicate route structure; consider flatter hierarchies where possible.

**Not preserving navigation state:** Bottom navigation apps should use StatefulShellRoute to maintain tab-specific navigation stacks.

This skill provides comprehensive guidance for implementing robust navigation and routing in Flutter applications, from simple stack-based navigation to complex authenticated flows with deep linking support. The declarative routing approach with GoRouter represents current best practices and offers the most maintainable solution for modern Flutter applications.
