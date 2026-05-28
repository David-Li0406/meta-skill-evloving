# Nested Navigation with Bottom Navigation Bar

This example demonstrates implementing tab-based navigation with independent navigation stacks for each tab using GoRouter's StatefulShellRoute. Each tab maintains its own navigation history and scroll position.

## Overview

The example includes:

- Bottom navigation bar with three tabs
- Independent navigation stacks for each tab
- Preserved state when switching between tabs
- Nested routes within each tab
- Deep linking support for all routes

## Project Structure

```
lib/
├── main.dart
├── router/
│   └── app_router.dart
├── widgets/
│   └── scaffold_with_nav_bar.dart
├── screens/
│   ├── home/
│   │   ├── home_screen.dart
│   │   └── home_details_screen.dart
│   ├── explore/
│   │   ├── explore_screen.dart
│   │   └── category_screen.dart
│   └── profile/
│       ├── profile_screen.dart
│       └── edit_profile_screen.dart
```

## Implementation

### Router Configuration with StatefulShellRoute

Define routes with independent navigation stacks:

```dart
// lib/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../widgets/scaffold_with_nav_bar.dart';
import '../screens/home/home_screen.dart';
import '../screens/home/home_details_screen.dart';
import '../screens/explore/explore_screen.dart';
import '../screens/explore/category_screen.dart';
import '../screens/profile/profile_screen.dart';
import '../screens/profile/edit_profile_screen.dart';

final router = GoRouter(
  initialLocation: '/home',
  debugLogDiagnostics: true,
  routes: [
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) {
        return ScaffoldWithNavBar(navigationShell: navigationShell);
      },
      branches: [
        // Home branch
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/home',
              name: 'home',
              builder: (context, state) => const HomeScreen(),
              routes: [
                GoRoute(
                  path: 'details/:id',
                  name: 'home-details',
                  builder: (context, state) {
                    final id = state.pathParameters['id']!;
                    return HomeDetailsScreen(itemId: id);
                  },
                ),
              ],
            ),
          ],
        ),
        // Explore branch
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/explore',
              name: 'explore',
              builder: (context, state) => const ExploreScreen(),
              routes: [
                GoRoute(
                  path: 'category/:category',
                  name: 'category',
                  builder: (context, state) {
                    final category = state.pathParameters['category']!;
                    return CategoryScreen(category: category);
                  },
                ),
              ],
            ),
          ],
        ),
        // Profile branch
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/profile',
              name: 'profile',
              builder: (context, state) => const ProfileScreen(),
              routes: [
                GoRoute(
                  path: 'edit',
                  name: 'edit-profile',
                  builder: (context, state) => const EditProfileScreen(),
                ),
              ],
            ),
          ],
        ),
      ],
    ),
  ],
);
```

### Scaffold with Navigation Bar

Create a scaffold that manages the bottom navigation:

```dart
// lib/widgets/scaffold_with_nav_bar.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

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
        onTap: (index) => _onTap(context, index),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.explore),
            label: 'Explore',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  void _onTap(BuildContext context, int index) {
    navigationShell.goBranch(
      index,
      // Navigate to the initial location of the branch when tapping
      // the tab that is already active
      initialLocation: index == navigationShell.currentIndex,
    );
  }
}
```

### Home Screen

Create the home screen with a list of items:

```dart
// lib/screens/home/home_screen.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: ListView.builder(
        itemCount: 20,
        itemBuilder: (context, index) {
          return ListTile(
            leading: CircleAvatar(
              child: Text('${index + 1}'),
            ),
            title: Text('Item ${index + 1}'),
            subtitle: Text('Description for item ${index + 1}'),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              context.goNamed(
                'home-details',
                pathParameters: {'id': '${index + 1}'},
              );
            },
          );
        },
      ),
    );
  }
}
```

### Home Details Screen

Create a details screen for home items:

```dart
// lib/screens/home/home_details_screen.dart
import 'package:flutter/material.dart';

class HomeDetailsScreen extends StatelessWidget {
  const HomeDetailsScreen({
    required this.itemId,
    super.key,
  });

  final String itemId;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Item $itemId Details'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircleAvatar(
                radius: 64,
                child: Text(
                  itemId,
                  style: const TextStyle(fontSize: 32),
                ),
              ),
              const SizedBox(height: 24),
              Text(
                'Item $itemId',
                style: const TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'This is the detailed view for this item. '
                'Navigate back to see the list preserved.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 32),
              ElevatedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back),
                label: const Text('Go Back'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Explore Screen

Create the explore screen with categories:

```dart
// lib/screens/explore/explore_screen.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class ExploreScreen extends StatelessWidget {
  const ExploreScreen({super.key});

  static const categories = [
    {'name': 'Technology', 'icon': Icons.computer},
    {'name': 'Science', 'icon': Icons.science},
    {'name': 'Art', 'icon': Icons.palette},
    {'name': 'Music', 'icon': Icons.music_note},
    {'name': 'Sports', 'icon': Icons.sports_soccer},
    {'name': 'Food', 'icon': Icons.restaurant},
    {'name': 'Travel', 'icon': Icons.flight},
    {'name': 'Books', 'icon': Icons.book},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Explore'),
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(16.0),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 1.2,
        ),
        itemCount: categories.length,
        itemBuilder: (context, index) {
          final category = categories[index];
          return Card(
            clipBehavior: Clip.antiAlias,
            child: InkWell(
              onTap: () {
                context.goNamed(
                  'category',
                  pathParameters: {
                    'category': category['name'].toString().toLowerCase(),
                  },
                );
              },
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    category['icon'] as IconData,
                    size: 48,
                    color: Theme.of(context).primaryColor,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    category['name'].toString(),
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
```

### Category Screen

Create a screen for individual categories:

```dart
// lib/screens/explore/category_screen.dart
import 'package:flutter/material.dart';

class CategoryScreen extends StatelessWidget {
  const CategoryScreen({
    required this.category,
    super.key,
  });

  final String category;

  @override
  Widget build(BuildContext context) {
    final capitalizedCategory =
        category[0].toUpperCase() + category.substring(1);

    return Scaffold(
      appBar: AppBar(
        title: Text(capitalizedCategory),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: 15,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.only(bottom: 16.0),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16.0),
              leading: Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Icon(Icons.article),
              ),
              title: Text('$capitalizedCategory Article ${index + 1}'),
              subtitle: Text(
                'Interesting content about $category topic ${index + 1}',
              ),
              trailing: const Icon(Icons.arrow_forward_ios),
              onTap: () {
                // Navigate to article details
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      'Opening $capitalizedCategory Article ${index + 1}',
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
```

### Profile Screen

Create the profile screen:

```dart
// lib/screens/profile/profile_screen.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: ListView(
        children: [
          const SizedBox(height: 24),
          const CircleAvatar(
            radius: 64,
            child: Icon(Icons.person, size: 64),
          ),
          const SizedBox(height: 16),
          const Text(
            'John Doe',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          const Text(
            'john.doe@example.com',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: ElevatedButton.icon(
              onPressed: () => context.goNamed('edit-profile'),
              icon: const Icon(Icons.edit),
              label: const Text('Edit Profile'),
            ),
          ),
          const SizedBox(height: 24),
          const Divider(),
          const ListTile(
            leading: Icon(Icons.email),
            title: Text('Email'),
            subtitle: Text('john.doe@example.com'),
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
          const ListTile(
            leading: Icon(Icons.cake),
            title: Text('Birthday'),
            subtitle: Text('January 1, 1990'),
          ),
          const Divider(),
          const SizedBox(height: 8),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16.0),
            child: Text(
              'Statistics',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildStatColumn('Posts', '127'),
              _buildStatColumn('Followers', '1.2K'),
              _buildStatColumn('Following', '345'),
            ],
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildStatColumn(String label, String value) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
}
```

### Edit Profile Screen

Create the edit profile screen:

```dart
// lib/screens/profile/edit_profile_screen.dart
import 'package:flutter/material.dart';

class EditProfileScreen extends StatefulWidget {
  const EditProfileScreen({super.key});

  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController(text: 'John Doe');
  final _emailController = TextEditingController(text: 'john.doe@example.com');
  final _phoneController = TextEditingController(text: '+1 234 567 8900');
  final _locationController = TextEditingController(text: 'San Francisco, CA');

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    _locationController.dispose();
    super.dispose();
  }

  void _saveProfile() {
    if (_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Profile updated successfully')),
      );
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Profile'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(24.0),
          children: [
            Center(
              child: Stack(
                children: [
                  const CircleAvatar(
                    radius: 64,
                    child: Icon(Icons.person, size: 64),
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: CircleAvatar(
                      backgroundColor: Theme.of(context).primaryColor,
                      child: IconButton(
                        icon: const Icon(Icons.camera_alt, color: Colors.white),
                        onPressed: () {
                          // Change profile picture
                        },
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Name',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.person),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter your name';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
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
                if (!value.contains('@')) {
                  return 'Please enter a valid email';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _phoneController,
              decoration: const InputDecoration(
                labelText: 'Phone',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.phone),
              ),
              keyboardType: TextInputType.phone,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _locationController,
              decoration: const InputDecoration(
                labelText: 'Location',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.location_on),
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _saveProfile,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Save Changes'),
            ),
          ],
        ),
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
import 'router/app_router.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Nested Navigation Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      routerConfig: router,
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
```

## Testing the Example

1. Run the app - it opens on the Home tab
2. Scroll through the list and tap an item to see details
3. Switch to the Explore tab - Home tab state is preserved
4. Navigate to a category in Explore
5. Switch to Profile tab
6. Navigate to Edit Profile
7. Switch back to Home tab - you'll see the details screen still there
8. Tap the active tab to return to the root of that branch

## Key Features Demonstrated

**Independent navigation stacks:** Each tab maintains its own navigation history and doesn't affect other tabs.

**State preservation:** Scroll position, form state, and navigation history are preserved when switching tabs.

**Deep linking support:** All routes have proper paths that work with deep links (e.g., `/explore/category/technology`).

**Tab reset behavior:** Tapping the active tab navigates back to the root of that branch.

**Nested routes:** Each tab can have multiple levels of nested routes.

**Material design:** Bottom navigation bar follows Material Design guidelines.

This example demonstrates the power of StatefulShellRoute for implementing complex navigation patterns while maintaining clean, maintainable code and excellent user experience with preserved state across tab switches.
