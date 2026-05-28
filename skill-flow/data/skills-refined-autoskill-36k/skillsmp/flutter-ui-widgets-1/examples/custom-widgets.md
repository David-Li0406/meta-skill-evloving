# Custom Widgets Example

A complete working example demonstrating how to build reusable custom widgets in Flutter using composition, configuration through constructor parameters, and proper encapsulation.

## Overview

This example shows how to create a custom widget library for a social media app, including reusable components for user profiles, posts, and actions. The approach demonstrates Flutter's composition-first philosophy and best practices for building maintainable custom widgets.

## Complete Example

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Custom Widgets Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const FeedScreen(),
    );
  }
}

// ============================================================================
// Custom Widget 1: UserAvatar
// A reusable avatar widget with online status indicator
// ============================================================================

class UserAvatar extends StatelessWidget {
  final String imageUrl;
  final double radius;
  final bool showOnlineStatus;
  final bool isOnline;
  final VoidCallback? onTap;

  const UserAvatar({
    super.key,
    required this.imageUrl,
    this.radius = 20,
    this.showOnlineStatus = false,
    this.isOnline = false,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final avatar = CircleAvatar(
      radius: radius,
      backgroundImage: NetworkImage(imageUrl),
      backgroundColor: Colors.grey.shade300,
    );

    if (!showOnlineStatus) {
      return onTap != null
          ? GestureDetector(onTap: onTap, child: avatar)
          : avatar;
    }

    // Avatar with online status indicator
    final avatarWithStatus = Stack(
      children: [
        avatar,
        Positioned(
          bottom: 0,
          right: 0,
          child: Container(
            width: radius * 0.4,
            height: radius * 0.4,
            decoration: BoxDecoration(
              color: isOnline ? Colors.green : Colors.grey,
              shape: BoxShape.circle,
              border: Border.all(
                color: Colors.white,
                width: 2,
              ),
            ),
          ),
        ),
      ],
    );

    return onTap != null
        ? GestureDetector(onTap: onTap, child: avatarWithStatus)
        : avatarWithStatus;
  }
}

// ============================================================================
// Custom Widget 2: UserProfileHeader
// Displays user information with avatar, name, and subtitle
// ============================================================================

class UserProfileHeader extends StatelessWidget {
  final String name;
  final String subtitle;
  final String avatarUrl;
  final bool showOnlineStatus;
  final bool isOnline;
  final Widget? trailing;
  final VoidCallback? onTap;

  const UserProfileHeader({
    super.key,
    required this.name,
    required this.subtitle,
    required this.avatarUrl,
    this.showOnlineStatus = false,
    this.isOnline = false,
    this.trailing,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            UserAvatar(
              imageUrl: avatarUrl,
              radius: 24,
              showOnlineStatus: showOnlineStatus,
              isOnline: isOnline,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    name,
                    style: textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: textTheme.bodySmall?.copyWith(
                      color: Colors.grey.shade600,
                    ),
                  ),
                ],
              ),
            ),
            if (trailing != null) trailing!,
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Custom Widget 3: ActionButton
// A reusable button with icon and label
// ============================================================================

class ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;
  final Color? color;
  final bool isActive;

  const ActionButton({
    super.key,
    required this.icon,
    required this.label,
    required this.onPressed,
    this.color,
    this.isActive = false,
  });

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final effectiveColor = isActive
        ? (color ?? colorScheme.primary)
        : Colors.grey.shade600;

    return InkWell(
      onTap: onPressed,
      borderRadius: BorderRadius.circular(4),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 20,
              color: effectiveColor,
            ),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                color: effectiveColor,
                fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Custom Widget 4: PostCard
// Complete post card with user info, content, image, and actions
// ============================================================================

class PostCard extends StatefulWidget {
  final String authorName;
  final String authorSubtitle;
  final String authorAvatarUrl;
  final String content;
  final String? imageUrl;
  final int initialLikes;
  final int comments;
  final int shares;
  final VoidCallback? onAuthorTap;

  const PostCard({
    super.key,
    required this.authorName,
    required this.authorSubtitle,
    required this.authorAvatarUrl,
    required this.content,
    this.imageUrl,
    this.initialLikes = 0,
    this.comments = 0,
    this.shares = 0,
    this.onAuthorTap,
  });

  @override
  State<PostCard> createState() => _PostCardState();
}

class _PostCardState extends State<PostCard> {
  late bool _isLiked;
  late int _likeCount;

  @override
  void initState() {
    super.initState();
    _isLiked = false;
    _likeCount = widget.initialLikes;
  }

  void _toggleLike() {
    setState(() {
      if (_isLiked) {
        _isLiked = false;
        _likeCount--;
      } else {
        _isLiked = true;
        _likeCount++;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header with user info
          UserProfileHeader(
            name: widget.authorName,
            subtitle: widget.authorSubtitle,
            avatarUrl: widget.authorAvatarUrl,
            onTap: widget.onAuthorTap,
            trailing: IconButton(
              icon: const Icon(Icons.more_vert),
              onPressed: () {
                // Show options menu
              },
            ),
          ),

          // Post content
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              widget.content,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          const SizedBox(height: 12),

          // Post image (if provided)
          if (widget.imageUrl != null)
            Image.network(
              widget.imageUrl!,
              width: double.infinity,
              height: 200,
              fit: BoxFit.cover,
            ),

          const SizedBox(height: 12),

          // Action buttons
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                ActionButton(
                  icon: _isLiked ? Icons.favorite : Icons.favorite_border,
                  label: _likeCount.toString(),
                  isActive: _isLiked,
                  color: Colors.red,
                  onPressed: _toggleLike,
                ),
                ActionButton(
                  icon: Icons.comment_outlined,
                  label: widget.comments.toString(),
                  onPressed: () {
                    // Show comments
                  },
                ),
                ActionButton(
                  icon: Icons.share_outlined,
                  label: widget.shares.toString(),
                  onPressed: () {
                    // Share post
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================================
// Custom Widget 5: EmptyState
// Reusable empty state widget
// ============================================================================

class EmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String message;
  final String? actionLabel;
  final VoidCallback? onActionPressed;

  const EmptyState({
    super.key,
    required this.icon,
    required this.title,
    required this.message,
    this.actionLabel,
    this.onActionPressed,
  });

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 80,
              color: colorScheme.primary.withOpacity(0.3),
            ),
            const SizedBox(height: 24),
            Text(
              title,
              style: textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              message,
              style: textTheme.bodyMedium?.copyWith(
                color: Colors.grey.shade600,
              ),
              textAlign: TextAlign.center,
            ),
            if (actionLabel != null && onActionPressed != null) ...[
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: onActionPressed,
                icon: const Icon(Icons.add),
                label: Text(actionLabel!),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Demo Screen: Using all custom widgets
// ============================================================================

class FeedScreen extends StatelessWidget {
  const FeedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Social Feed'),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {},
          ),
        ],
      ),
      body: ListView(
        children: [
          PostCard(
            authorName: 'Alice Johnson',
            authorSubtitle: '2 hours ago',
            authorAvatarUrl: 'https://i.pravatar.cc/150?img=1',
            content: 'Just finished building an amazing Flutter app! '
                'The widget system is so powerful and composable. '
                'Love how easy it is to create reusable components.',
            imageUrl: 'https://picsum.photos/600/400?random=1',
            initialLikes: 42,
            comments: 8,
            shares: 3,
            onAuthorTap: () {
              print('Tapped on Alice');
            },
          ),
          PostCard(
            authorName: 'Bob Smith',
            authorSubtitle: '5 hours ago',
            authorAvatarUrl: 'https://i.pravatar.cc/150?img=2',
            content: 'Custom widgets make development so much faster! '
                'Build once, use everywhere. This is the way.',
            initialLikes: 28,
            comments: 5,
            shares: 2,
            onAuthorTap: () {
              print('Tapped on Bob');
            },
          ),
          PostCard(
            authorName: 'Carol Williams',
            authorSubtitle: '1 day ago',
            authorAvatarUrl: 'https://i.pravatar.cc/150?img=3',
            content: 'Composition over inheritance! Flutter gets it right.',
            imageUrl: 'https://picsum.photos/600/400?random=2',
            initialLikes: 156,
            comments: 23,
            shares: 12,
            onAuthorTap: () {
              print('Tapped on Carol');
            },
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Key Concepts Demonstrated

### 1. Single Responsibility

Each custom widget has one clear purpose:
- `UserAvatar` - Display user avatar with optional status
- `UserProfileHeader` - Display user info with avatar and text
- `ActionButton` - Interactive button with icon and label
- `PostCard` - Complete social media post
- `EmptyState` - Empty state placeholder

### 2. Configuration Through Constructor

Widgets are configured through constructor parameters, not inheritance:

```dart
UserAvatar(
  imageUrl: 'url',
  radius: 24,
  showOnlineStatus: true,
  isOnline: true,
  onTap: () {},
)
```

### 3. Composition

Complex widgets are built by composing simpler widgets:

```dart
// PostCard composes multiple custom widgets
PostCard(
  // Uses UserProfileHeader internally
  // Uses ActionButton for actions
  // Combines with standard widgets
)
```

### 4. Optional Features

Optional features use nullable parameters:

```dart
final String? imageUrl;  // Optional image
final VoidCallback? onTap;  // Optional tap handler
final Widget? trailing;  // Optional trailing widget
```

### 5. State Management

State is managed only where needed (PostCard manages like state):

```dart
class _PostCardState extends State<PostCard> {
  late bool _isLiked;
  late int _likeCount;

  void _toggleLike() {
    setState(() {
      _isLiked = !_isLiked;
      _likeCount += _isLiked ? 1 : -1;
    });
  }
}
```

## Benefits

1. **Reusability** - Use the same components across different screens
2. **Consistency** - Uniform appearance and behavior
3. **Maintainability** - Changes in one place affect all instances
4. **Testability** - Small, focused widgets are easier to test
5. **Readability** - Code is self-documenting with descriptive widget names
6. **Flexibility** - Easy to extend and customize through parameters

## Usage Pattern

```dart
// Create custom widget instance
PostCard(
  authorName: 'John Doe',
  authorSubtitle: '2 hours ago',
  authorAvatarUrl: 'https://example.com/avatar.jpg',
  content: 'Post content here',
  imageUrl: 'https://example.com/image.jpg',
  initialLikes: 42,
  comments: 8,
  shares: 3,
  onAuthorTap: () {
    // Navigate to profile
  },
)
```

## Extension Ideas

To extend this example, you could add:

1. **Theming** - Add custom theme support
2. **Animations** - Animate like button, expand/collapse content
3. **Accessibility** - Add semantic labels and screen reader support
4. **Responsive** - Adapt layout for different screen sizes
5. **Error handling** - Handle image loading errors
6. **Loading states** - Show loading indicators while fetching data
7. **Interactions** - Add long-press menus, swipe actions
8. **Customization** - More configuration options (colors, sizes, styles)

## Further Reading

- [Widget Catalog](../references/widget-catalog.md)
- [Composition Patterns Example](composition-patterns.md)
- [Widget Lifecycle](../references/widget-lifecycle.md)
