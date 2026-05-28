# Authenticated Routing Example

This example demonstrates a complete authentication flow with protected routes, login/logout functionality, and automatic redirects using GoRouter.

## Overview

The example includes:

- Login screen with authentication
- Protected routes requiring authentication
- Automatic redirect to login for unauthenticated users
- Redirect to home after successful login
- Logout functionality
- State preservation across navigation

## Project Structure

```
lib/
├── main.dart
├── router/
│   └── app_router.dart
├── services/
│   └── auth_service.dart
├── screens/
│   ├── login_screen.dart
│   ├── home_screen.dart
│   ├── profile_screen.dart
│   └── settings_screen.dart
```

## Implementation

### Auth Service

Create a service to manage authentication state:

```dart
// lib/services/auth_service.dart
import 'package:flutter/foundation.dart';

class AuthService extends ChangeNotifier {
  bool _isAuthenticated = false;
  String? _username;
  String? _redirectPath;

  bool get isAuthenticated => _isAuthenticated;
  String? get username => _username;

  void setRedirectPath(String path) {
    _redirectPath = path;
  }

  String? getAndClearRedirectPath() {
    final path = _redirectPath;
    _redirectPath = null;
    return path;
  }

  Future<bool> login(String email, String password) async {
    // Simulate API call
    await Future.delayed(const Duration(seconds: 1));

    // Simple validation for demo
    if (email.isNotEmpty && password.isNotEmpty) {
      _isAuthenticated = true;
      _username = email.split('@')[0];
      notifyListeners();
      return true;
    }

    return false;
  }

  void logout() {
    _isAuthenticated = false;
    _username = null;
    _redirectPath = null;
    notifyListeners();
  }
}
```

### Router Configuration

Define routes with authentication guards:

```dart
// lib/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../services/auth_service.dart';
import '../screens/login_screen.dart';
import '../screens/home_screen.dart';
import '../screens/profile_screen.dart';
import '../screens/settings_screen.dart';

class AppRouter {
  final AuthService authService;

  AppRouter(this.authService);

  late final router = GoRouter(
    refreshListenable: authService,
    debugLogDiagnostics: true,
    redirect: (BuildContext context, GoRouterState state) {
      final isAuthenticated = authService.isAuthenticated;
      final isLoginRoute = state.matchedLocation == '/login';

      // Redirect to login if not authenticated
      if (!isAuthenticated && !isLoginRoute) {
        // Store the intended destination
        authService.setRedirectPath(state.uri.toString());
        return '/login';
      }

      // Redirect away from login if already authenticated
      if (isAuthenticated && isLoginRoute) {
        return '/';
      }

      // No redirect needed
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfileScreen(),
      ),
      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => const SettingsScreen(),
      ),
    ],
  );
}
```

### Login Screen

Create a login screen with form validation:

```dart
// lib/screens/login_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final authService = context.read<AuthService>();
    final success = await authService.login(
      _emailController.text,
      _passwordController.text,
    );

    if (!mounted) return;

    setState(() {
      _isLoading = false;
    });

    if (success) {
      // Navigate to intended destination or home
      final redirectPath = authService.getAndClearRedirectPath();
      context.go(redirectPath ?? '/');
    } else {
      setState(() {
        _errorMessage = 'Invalid email or password';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Icon(
                  Icons.lock_outline,
                  size: 64,
                  color: Colors.blue,
                ),
                const SizedBox(height: 32),
                const Text(
                  'Welcome Back',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                const Text(
                  'Please sign in to continue',
                  style: TextStyle(color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),
                TextFormField(
                  controller: _emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.email),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your email';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.lock),
                  ),
                  obscureText: true,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    return null;
                  },
                ),
                if (_errorMessage != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    _errorMessage!,
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                ],
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Login'),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Demo: Use any email and password',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

### Home Screen

Create a home screen with navigation to protected routes:

```dart
// lib/screens/home_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../services/auth_service.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              authService.logout();
            },
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.home,
                size: 64,
                color: Colors.blue,
              ),
              const SizedBox(height: 16),
              Text(
                'Welcome, ${authService.username}!',
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'You are successfully authenticated',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 32),
              ElevatedButton.icon(
                onPressed: () => context.push('/profile'),
                icon: const Icon(Icons.person),
                label: const Text('View Profile'),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: () => context.push('/settings'),
                icon: const Icon(Icons.settings),
                label: const Text('Settings'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Profile Screen

Create a profile screen:

```dart
// lib/screens/profile_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const CircleAvatar(
            radius: 64,
            child: Icon(Icons.person, size: 64),
          ),
          const SizedBox(height: 16),
          Text(
            authService.username ?? 'User',
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 32),
          const ListTile(
            leading: Icon(Icons.email),
            title: Text('Email'),
            subtitle: Text('user@example.com'),
          ),
          const ListTile(
            leading: Icon(Icons.phone),
            title: Text('Phone'),
            subtitle: Text('+1 234 567 8900'),
          ),
          const ListTile(
            leading: Icon(Icons.location_on),
            title: Text('Location'),
            subtitle: Text('San Francisco, CA'),
          ),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: ElevatedButton(
              onPressed: () {
                // Edit profile logic
              },
              child: const Text('Edit Profile'),
            ),
          ),
        ],
      ),
    );
  }
}
```

### Settings Screen

Create a settings screen:

```dart
// lib/screens/settings_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _notificationsEnabled = true;
  bool _darkModeEnabled = false;

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text(
              'Preferences',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          SwitchListTile(
            title: const Text('Enable Notifications'),
            subtitle: const Text('Receive push notifications'),
            value: _notificationsEnabled,
            onChanged: (value) {
              setState(() {
                _notificationsEnabled = value;
              });
            },
          ),
          SwitchListTile(
            title: const Text('Dark Mode'),
            subtitle: const Text('Use dark theme'),
            value: _darkModeEnabled,
            onChanged: (value) {
              setState(() {
                _darkModeEnabled = value;
              });
            },
          ),
          const Divider(),
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text(
              'Account',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.password),
            title: const Text('Change Password'),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              // Change password logic
            },
          ),
          ListTile(
            leading: const Icon(Icons.delete),
            title: const Text('Delete Account'),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              // Delete account logic
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text(
              'Logout',
              style: TextStyle(color: Colors.red),
            ),
            onTap: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Logout'),
                  content: const Text('Are you sure you want to logout?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Cancel'),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.pop(context);
                        authService.logout();
                      },
                      child: const Text('Logout'),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
```

### Main Application

Wire everything together:

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'router/app_router.dart';
import 'services/auth_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late final AuthService _authService;
  late final AppRouter _appRouter;

  @override
  void initState() {
    super.initState();
    _authService = AuthService();
    _appRouter = AppRouter(_authService);
  }

  @override
  void dispose() {
    _authService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: _authService),
      ],
      child: MaterialApp.router(
        title: 'Authenticated Routing Demo',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        routerConfig: _appRouter.router,
      ),
    );
  }
}
```

## Dependencies

Add required dependencies to `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  go_router: ^14.0.0
  provider: ^6.1.1
```

## Testing the Example

1. Run the app - you'll be redirected to the login screen
2. Enter any email and password to log in
3. After login, you'll be redirected to the home screen
4. Navigate to Profile or Settings - these are protected routes
5. Logout from the settings screen or home screen app bar
6. You'll be redirected back to the login screen

## Key Features Demonstrated

**Automatic redirects:** Unauthenticated users are automatically redirected to login when attempting to access protected routes.

**State preservation:** The intended destination is stored and used after successful login.

**Global authentication:** All routes except login require authentication through the global redirect.

**Logout functionality:** Users can logout, which triggers automatic redirect to login.

**State management:** Provider manages authentication state and notifies the router of changes.

**Form validation:** Login screen includes proper form validation.

**Loading states:** Login button shows loading indicator during authentication.

This example provides a foundation for implementing authentication flows in Flutter applications with GoRouter, demonstrating best practices for route protection and user experience.
