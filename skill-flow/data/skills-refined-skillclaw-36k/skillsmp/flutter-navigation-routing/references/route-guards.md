# Route Guards and Authentication Flows

Route guards protect application routes from unauthorized access by validating user permissions before navigation. This guide covers implementing authentication flows, route protection, and redirect strategies in Flutter applications.

## Route Guards Overview

Route guards are functions or mechanisms that intercept navigation events to determine whether a user should access a particular route. Common use cases include:

**Authentication checks** to ensure users are logged in before accessing protected content.

**Authorization validation** to verify users have appropriate permissions for specific features.

**Onboarding flows** to redirect new users through setup screens.

**Feature flags** to conditionally enable or disable routes based on configuration.

**Session validation** to check if authentication tokens are still valid.

**Role-based access** to restrict routes to specific user roles (admin, user, guest).

## Route Guards with GoRouter

GoRouter provides two approaches for implementing route guards: global redirects and route-level redirects.

### Global Redirect Function

The global redirect function executes before every navigation event:

```dart
final router = GoRouter(
  redirect: (BuildContext context, GoRouterState state) {
    final authService = context.read<AuthService>();
    final isAuthenticated = authService.isAuthenticated;
    final isAuthRoute = state.matchedLocation == '/login' ||
        state.matchedLocation == '/register';

    // Redirect to login if not authenticated
    if (!isAuthenticated && !isAuthRoute) {
      return '/login';
    }

    // Redirect away from login if already authenticated
    if (isAuthenticated && isAuthRoute) {
      return '/';
    }

    // Allow navigation
    return null;
  },
  routes: routes,
);
```

Return `null` to allow navigation to the requested route, or return a path string to redirect to a different route.

### Route-Level Redirects

Define redirects on specific routes for granular control:

```dart
GoRoute(
  path: '/admin',
  redirect: (BuildContext context, GoRouterState state) {
    final authService = context.read<AuthService>();

    if (!authService.isAuthenticated) {
      return '/login';
    }

    if (!authService.hasRole('admin')) {
      return '/unauthorized';
    }

    return null;
  },
  builder: (context, state) => const AdminScreen(),
)
```

### Redirect Execution Order

When both global and route-level redirects are defined, they execute in this order:

1. Global redirect (on GoRouter)
2. Parent route redirect
3. Child route redirect

Each redirect can override the previous one or allow navigation by returning null.

### Combining Global and Route-Level Redirects

```dart
final router = GoRouter(
  // Global authentication check
  redirect: (context, state) {
    final authService = context.read<AuthService>();

    if (!authService.isAuthenticated &&
        !state.matchedLocation.startsWith('/auth')) {
      return '/auth/login';
    }

    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/admin',
      // Additional authorization check
      redirect: (context, state) {
        final authService = context.read<AuthService>();

        if (!authService.hasRole('admin')) {
          return '/forbidden';
        }

        return null;
      },
      builder: (context, state) => const AdminScreen(),
    ),
  ],
);
```

## State-Based Route Guards

Route guards should react to authentication state changes using `refreshListenable`:

```dart
class AuthService extends ChangeNotifier {
  bool _isAuthenticated = false;
  String? _userRole;

  bool get isAuthenticated => _isAuthenticated;
  String? get userRole => _userRole;

  Future<void> login(String email, String password) async {
    // Perform authentication
    _isAuthenticated = true;
    _userRole = 'user';
    notifyListeners(); // Triggers router refresh
  }

  Future<void> logout() async {
    _isAuthenticated = false;
    _userRole = null;
    notifyListeners(); // Triggers router refresh
  }

  bool hasRole(String role) {
    return _userRole == role;
  }
}

final authService = AuthService();

final router = GoRouter(
  refreshListenable: authService,
  redirect: (context, state) {
    // Redirect logic that uses authService
  },
  routes: routes,
);
```

When `authService.notifyListeners()` is called, the router automatically re-evaluates all redirects.

## Authentication Flow Patterns

### Login Flow with Redirect

Store the intended destination and redirect after successful login:

```dart
class AuthService extends ChangeNotifier {
  String? _redirectPath;

  void setRedirectPath(String path) {
    _redirectPath = path;
  }

  String? getAndClearRedirectPath() {
    final path = _redirectPath;
    _redirectPath = null;
    return path;
  }
}

final router = GoRouter(
  redirect: (context, state) {
    final authService = context.read<AuthService>();
    final isAuthenticated = authService.isAuthenticated;
    final isLoginRoute = state.matchedLocation == '/login';

    if (!isAuthenticated && !isLoginRoute) {
      // Store intended destination
      authService.setRedirectPath(state.uri.toString());
      return '/login';
    }

    return null;
  },
  routes: routes,
);

// In LoginScreen after successful login:
void _handleSuccessfulLogin() {
  final redirectPath = authService.getAndClearRedirectPath();
  context.go(redirectPath ?? '/');
}
```

### Multi-Step Authentication

Handle complex authentication flows with multiple steps:

```dart
class AuthService extends ChangeNotifier {
  AuthState _state = AuthState.unauthenticated;

  AuthState get state => _state;

  bool get isAuthenticated => _state == AuthState.authenticated;
  bool get needsTwoFactor => _state == AuthState.needsTwoFactor;
  bool get needsOnboarding => _state == AuthState.needsOnboarding;
}

enum AuthState {
  unauthenticated,
  needsTwoFactor,
  needsOnboarding,
  authenticated,
}

final router = GoRouter(
  refreshListenable: authService,
  redirect: (context, state) {
    final authState = authService.state;
    final location = state.matchedLocation;

    // Define auth routes
    final isLoginRoute = location == '/login';
    final isTwoFactorRoute = location == '/two-factor';
    final isOnboardingRoute = location == '/onboarding';
    final isAuthRoute = isLoginRoute || isTwoFactorRoute || isOnboardingRoute;

    // Unauthenticated: redirect to login
    if (authState == AuthState.unauthenticated && !isLoginRoute) {
      return '/login';
    }

    // Needs two-factor: redirect to two-factor
    if (authState == AuthState.needsTwoFactor && !isTwoFactorRoute) {
      return '/two-factor';
    }

    // Needs onboarding: redirect to onboarding
    if (authState == AuthState.needsOnboarding && !isOnboardingRoute) {
      return '/onboarding';
    }

    // Authenticated: redirect away from auth routes
    if (authState == AuthState.authenticated && isAuthRoute) {
      return '/';
    }

    return null;
  },
  routes: routes,
);
```

### Token Validation

Validate authentication tokens before allowing navigation:

```dart
class AuthService extends ChangeNotifier {
  String? _token;
  DateTime? _tokenExpiry;

  bool get isAuthenticated {
    if (_token == null || _tokenExpiry == null) {
      return false;
    }

    if (DateTime.now().isAfter(_tokenExpiry!)) {
      // Token expired
      _token = null;
      _tokenExpiry = null;
      return false;
    }

    return true;
  }

  Future<void> refreshToken() async {
    // Refresh the authentication token
    // Update _token and _tokenExpiry
    notifyListeners();
  }
}

final router = GoRouter(
  refreshListenable: authService,
  redirect: (context, state) async {
    final authService = context.read<AuthService>();

    // Attempt token refresh if needed
    if (!authService.isAuthenticated && authService.hasRefreshToken) {
      await authService.refreshToken();
    }

    // Standard authentication check
    if (!authService.isAuthenticated &&
        state.matchedLocation != '/login') {
      return '/login';
    }

    return null;
  },
  routes: routes,
);
```

Note: Redirect functions in GoRouter are synchronous. For async validation, perform the check before navigation or use a loading state.

## Role-Based Access Control

Implement role-based access control (RBAC) for fine-grained permissions:

```dart
enum UserRole {
  guest,
  user,
  moderator,
  admin,
}

class AuthService extends ChangeNotifier {
  UserRole _currentRole = UserRole.guest;

  UserRole get currentRole => _currentRole;

  bool hasPermission(UserRole requiredRole) {
    final roleHierarchy = {
      UserRole.guest: 0,
      UserRole.user: 1,
      UserRole.moderator: 2,
      UserRole.admin: 3,
    };

    return roleHierarchy[_currentRole]! >= roleHierarchy[requiredRole]!;
  }
}

// Define routes with role requirements
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/dashboard',
      redirect: (context, state) {
        final authService = context.read<AuthService>();

        if (!authService.hasPermission(UserRole.user)) {
          return '/login';
        }

        return null;
      },
      builder: (context, state) => const DashboardScreen(),
    ),
    GoRoute(
      path: '/moderate',
      redirect: (context, state) {
        final authService = context.read<AuthService>();

        if (!authService.hasPermission(UserRole.moderator)) {
          return '/forbidden';
        }

        return null;
      },
      builder: (context, state) => const ModeratorScreen(),
    ),
    GoRoute(
      path: '/admin',
      redirect: (context, state) {
        final authService = context.read<AuthService>();

        if (!authService.hasPermission(UserRole.admin)) {
          return '/forbidden';
        }

        return null;
      },
      builder: (context, state) => const AdminScreen(),
    ),
  ],
);
```

### Route Metadata for Permissions

Define route metadata to centralize permission requirements:

```dart
class RouteMetadata {
  final UserRole? requiredRole;
  final bool requiresAuth;

  const RouteMetadata({
    this.requiredRole,
    this.requiresAuth = false,
  });
}

GoRoute createProtectedRoute({
  required String path,
  required Widget Function(BuildContext, GoRouterState) builder,
  RouteMetadata? metadata,
  List<RouteBase> routes = const [],
}) {
  return GoRoute(
    path: path,
    redirect: (context, state) {
      final authService = context.read<AuthService>();

      if (metadata?.requiresAuth == true) {
        if (!authService.isAuthenticated) {
          return '/login';
        }
      }

      if (metadata?.requiredRole != null) {
        if (!authService.hasPermission(metadata!.requiredRole!)) {
          return '/forbidden';
        }
      }

      return null;
    },
    builder: builder,
    routes: routes,
  );
}

// Usage
final routes = [
  createProtectedRoute(
    path: '/',
    builder: (context, state) => const HomeScreen(),
  ),
  createProtectedRoute(
    path: '/profile',
    metadata: const RouteMetadata(requiresAuth: true),
    builder: (context, state) => const ProfileScreen(),
  ),
  createProtectedRoute(
    path: '/admin',
    metadata: const RouteMetadata(
      requiresAuth: true,
      requiredRole: UserRole.admin,
    ),
    builder: (context, state) => const AdminScreen(),
  ),
];
```

## Integration with State Management

### Riverpod Integration

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Auth state provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(const AuthState.unauthenticated());

  Future<void> login(String email, String password) async {
    // Login logic
    state = const AuthState.authenticated(user: user);
  }

  void logout() {
    state = const AuthState.unauthenticated();
  }
}

// Router provider with auth integration
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    refreshListenable: GoRouterRefreshStream(
      ref.watch(authProvider.notifier).stream,
    ),
    redirect: (context, state) {
      final isAuthenticated = authState.maybeWhen(
        authenticated: (_) => true,
        orElse: () => false,
      );

      final isAuthRoute = state.matchedLocation.startsWith('/auth');

      if (!isAuthenticated && !isAuthRoute) {
        return '/auth/login';
      }

      if (isAuthenticated && isAuthRoute) {
        return '/';
      }

      return null;
    },
    routes: routes,
  );
});

// Stream wrapper for Riverpod
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

### Bloc Integration

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(const AuthState.unauthenticated()) {
    on<LoginEvent>(_onLogin);
    on<LogoutEvent>(_onLogout);
  }

  Future<void> _onLogin(LoginEvent event, Emitter<AuthState> emit) async {
    // Login logic
    emit(AuthState.authenticated(user: user));
  }

  void _onLogout(LogoutEvent event, Emitter<AuthState> emit) {
    emit(const AuthState.unauthenticated());
  }
}

class MyApp extends StatelessWidget {
  final AuthBloc authBloc;

  const MyApp({required this.authBloc, super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider.value(
      value: authBloc,
      child: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, authState) {
          final router = GoRouter(
            refreshListenable: GoRouterRefreshStream(authBloc.stream),
            redirect: (context, state) {
              final isAuthenticated = authState.maybeWhen(
                authenticated: (_) => true,
                orElse: () => false,
              );

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

## Preventing Redirect Loops

Redirect loops occur when redirects continuously redirect to each other. Prevent them with careful logic:

```dart
final router = GoRouter(
  redirectLimit: 10, // Default is 5
  redirect: (context, state) {
    final authService = context.read<AuthService>();
    final location = state.matchedLocation;

    // Define route categories
    final publicRoutes = ['/login', '/register', '/forgot-password'];
    final isPublicRoute = publicRoutes.contains(location);

    // Simple authentication check
    if (!authService.isAuthenticated && !isPublicRoute) {
      return '/login';
    }

    if (authService.isAuthenticated && isPublicRoute) {
      return '/';
    }

    // No redirect needed
    return null;
  },
  routes: routes,
);
```

### Debugging Redirects

Enable debug logging to track redirect behavior:

```dart
final router = GoRouter(
  debugLogDiagnostics: true,
  redirect: (context, state) {
    print('Redirect check for: ${state.matchedLocation}');
    final result = _performRedirectLogic(context, state);
    print('Redirect result: $result');
    return result;
  },
  routes: routes,
);
```

## Feature Flags and Conditional Routes

Use feature flags to conditionally enable routes:

```dart
class FeatureFlags {
  final bool adminPanelEnabled;
  final bool betaFeaturesEnabled;

  const FeatureFlags({
    this.adminPanelEnabled = false,
    this.betaFeaturesEnabled = false,
  });
}

final router = GoRouter(
  routes: [
    GoRoute(
      path: '/admin',
      redirect: (context, state) {
        final featureFlags = context.read<FeatureFlags>();

        if (!featureFlags.adminPanelEnabled) {
          return '/not-available';
        }

        final authService = context.read<AuthService>();
        if (!authService.hasPermission(UserRole.admin)) {
          return '/forbidden';
        }

        return null;
      },
      builder: (context, state) => const AdminScreen(),
    ),
    GoRoute(
      path: '/beta',
      redirect: (context, state) {
        final featureFlags = context.read<FeatureFlags>();

        if (!featureFlags.betaFeaturesEnabled) {
          return '/';
        }

        return null;
      },
      builder: (context, state) => const BetaScreen(),
    ),
  ],
);
```

## Onboarding and Setup Flows

Redirect new users through onboarding:

```dart
class UserService extends ChangeNotifier {
  bool _hasCompletedOnboarding = false;

  bool get hasCompletedOnboarding => _hasCompletedOnboarding;

  void completeOnboarding() {
    _hasCompletedOnboarding = true;
    notifyListeners();
  }
}

final router = GoRouter(
  redirect: (context, state) {
    final authService = context.read<AuthService>();
    final userService = context.read<UserService>();
    final location = state.matchedLocation;

    // Not authenticated
    if (!authService.isAuthenticated && location != '/login') {
      return '/login';
    }

    // Authenticated but needs onboarding
    if (authService.isAuthenticated &&
        !userService.hasCompletedOnboarding &&
        location != '/onboarding') {
      return '/onboarding';
    }

    // Skip auth/onboarding routes if already authenticated and onboarded
    if (authService.isAuthenticated &&
        userService.hasCompletedOnboarding &&
        (location == '/login' || location == '/onboarding')) {
      return '/';
    }

    return null;
  },
  routes: routes,
);
```

## Security Best Practices

**Validate on server side** as client-side route guards are not a security measure but a UX enhancement. Always validate permissions on the backend.

**Use HTTPS** for authentication endpoints to prevent token interception.

**Implement token refresh** to maintain sessions without requiring re-login.

**Clear sensitive data** on logout, including tokens, user data, and cached information.

**Handle token expiry** gracefully by refreshing or redirecting to login when tokens expire.

**Avoid storing tokens in local storage** on web platforms; use secure storage mechanisms.

**Log security events** such as failed authentication attempts and unauthorized access attempts.

**Rate limit authentication** endpoints to prevent brute force attacks.

**Use secure password policies** and enforce them during registration.

**Implement multi-factor authentication** for sensitive applications.

## Testing Route Guards

Test route guard behavior in widget tests:

```dart
testWidgets('Redirects to login when not authenticated', (tester) async {
  final authService = AuthService();
  final router = createRouter(authService);

  await tester.pumpWidget(
    MaterialApp.router(
      routerConfig: router,
    ),
  );

  // Attempt to navigate to protected route
  router.go('/profile');
  await tester.pumpAndSettle();

  // Should be redirected to login
  expect(find.text('Login'), findsOneWidget);
});

testWidgets('Allows access when authenticated', (tester) async {
  final authService = AuthService();
  await authService.login('test@example.com', 'password');

  final router = createRouter(authService);

  await tester.pumpWidget(
    MaterialApp.router(
      routerConfig: router,
    ),
  );

  // Navigate to protected route
  router.go('/profile');
  await tester.pumpAndSettle();

  // Should show profile screen
  expect(find.text('Profile'), findsOneWidget);
});
```

## Best Practices

**Centralize auth logic** in a service or state management layer rather than duplicating it across routes.

**Use global redirects** for authentication and route-level redirects for authorization to separate concerns.

**Implement loading states** to handle async authentication checks without flickering screens.

**Preserve navigation intent** by storing the attempted route and redirecting after successful login.

**Test all redirect scenarios** including edge cases like expired tokens and role changes.

**Provide clear error messages** when users lack permissions for specific routes.

**Monitor redirect performance** to ensure authentication checks don't slow down navigation.

**Document route protection** requirements so developers understand which routes require authentication.

**Use type-safe roles** with enums rather than strings to prevent typos and enable refactoring.

**Handle state changes gracefully** by using refreshListenable to automatically update routes when auth state changes.

Route guards are essential for protecting application routes and providing appropriate user experiences based on authentication and authorization state. Combined with proper state management and testing, route guards enable secure, user-friendly navigation flows in Flutter applications.
