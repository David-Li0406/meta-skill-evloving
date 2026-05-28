# Hero Transitions in Flutter

Hero animations, also known as shared element transitions, create visual continuity when navigating between screens by animating a widget from its position on one route to its position on another. This pattern is ubiquitous in modern mobile apps and provides an intuitive sense of flow and navigation.

## What is a Hero Animation?

A hero animation occurs when:
1. A widget on the source screen (Route A) is marked as a hero
2. A corresponding widget on the destination screen (Route B) is marked with the same hero tag
3. When navigating between routes, the widget appears to "fly" from its position on Route A to its position on Route B

The widget can change size, position, and shape during the flight, creating smooth, visually appealing transitions.

## How Hero Animations Work

### Behind the Scenes

When a route transition occurs, Flutter's Navigator performs these steps:

**1. Detection Phase (t = 0.0)**
- Navigator identifies matching Hero widgets on both routes by comparing tags
- Calculates the source hero's screen position and size
- Calculates the destination hero's screen position and size

**2. Preparation**
- Creates a copy of the hero widget in an overlay above both routes
- Positions the overlay hero at the source position
- Hides the source hero (makes it invisible)
- Keeps the destination hero hidden

**3. Animation Phase (t = 0.0 to 1.0)**
- Animates the overlay hero's bounds from source to destination using `RectTween`
- By default, uses `MaterialRectArcTween` for curved motion paths
- The route transition animation happens simultaneously

**4. Completion Phase (t = 1.0)**
- Removes the overlay hero
- Shows the destination hero in its final position
- The source hero becomes visible again when you pop back

### RectTween Animation

Flutter uses `RectTween` to interpolate between the rectangular bounds:

```dart
RectTween(
  begin: Rect.fromLTWH(sourceX, sourceY, sourceWidth, sourceHeight),
  end: Rect.fromLTWH(destX, destY, destWidth, destHeight),
)
```

For Material apps, this uses `MaterialRectArcTween` which creates a curved path rather than a straight line, giving a more natural feel.

## Basic Hero Implementation

### PhotoHero Widget Pattern

A common reusable pattern for hero-wrapped images:

```dart
class PhotoHero extends StatelessWidget {
  const PhotoHero({
    super.key,
    required this.photo,
    this.onTap,
    required this.width,
  });

  final String photo;
  final VoidCallback? onTap;
  final double width;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: Hero(
        tag: photo,
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onTap,
            child: Image.asset(
              photo,
              fit: BoxFit.contain,
            ),
          ),
        ),
      ),
    );
  }
}
```

### Source Screen

```dart
class ThumbnailScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Photo Gallery')),
      body: Center(
        child: PhotoHero(
          photo: 'images/landscape.jpg',
          width: 100.0,
          onTap: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (context) => DetailScreen(),
              ),
            );
          },
        ),
      ),
    );
  }
}
```

### Destination Screen

```dart
class DetailScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Photo Detail')),
      body: GestureDetector(
        onTap: () => Navigator.of(context).pop(),
        child: Center(
          child: PhotoHero(
            photo: 'images/landscape.jpg',
            width: 300.0,
            onTap: () => Navigator.of(context).pop(),
          ),
        ),
      ),
    );
  }
}
```

### Key Points

**Matching Tags**: Both Hero widgets must have identical `tag` values. The tag can be any object (String, int, custom object) as long as it's equal on both routes.

**Material Wrapper**: Wrapping the image in `Material(color: Colors.transparent)` ensures proper rendering during the animation and provides a consistent background.

**Size Changes**: The hero automatically animates size changes. The thumbnail is 100px wide, and the detail view is 300px wide - Flutter interpolates smoothly between them.

## Standard Hero Animation Pattern

### Gallery Grid to Detail View

```dart
class PhotoGrid extends StatelessWidget {
  final List<String> photos = [
    'photo1.jpg',
    'photo2.jpg',
    'photo3.jpg',
    'photo4.jpg',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Photo Gallery')),
      body: GridView.builder(
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        padding: EdgeInsets.all(8),
        itemCount: photos.length,
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => PhotoDetail(
                    photoPath: photos[index],
                    tag: 'photo_$index',
                  ),
                ),
              );
            },
            child: Hero(
              tag: 'photo_$index',
              child: Material(
                color: Colors.transparent,
                child: Image.asset(
                  photos[index],
                  fit: BoxFit.cover,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class PhotoDetail extends StatelessWidget {
  const PhotoDetail({
    super.key,
    required this.photoPath,
    required this.tag,
  });

  final String photoPath;
  final String tag;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: GestureDetector(
        onTap: () => Navigator.pop(context),
        child: Center(
          child: Hero(
            tag: tag,
            child: Material(
              color: Colors.transparent,
              child: Image.asset(
                photoPath,
                fit: BoxFit.contain,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

## Radial Hero Animations

Radial hero animations transform a circular widget into a rectangular one (or vice versa) while flying between screens. This requires special handling to maintain the circular clipping during the transition.

### RadialExpansion Widget

```dart
import 'dart:math' as math;

class RadialExpansion extends StatelessWidget {
  const RadialExpansion({
    super.key,
    required this.maxRadius,
    this.child,
  }) : clipRectSize = 2.0 * (maxRadius / math.sqrt2);

  final double maxRadius;
  final double clipRectSize;
  final Widget? child;

  @override
  Widget build(BuildContext context) {
    return ClipOval(
      child: Center(
        child: SizedBox(
          width: clipRectSize,
          height: clipRectSize,
          child: ClipRect(
            child: child,
          ),
        ),
      ),
    );
  }
}
```

The `RadialExpansion` widget:
- Uses `ClipOval` to create circular clipping
- Calculates the clip rect size based on the maximum radius
- Centers the rectangular content within the circular clip

### Photo Widget for Radial Heroes

```dart
class Photo extends StatelessWidget {
  const Photo({
    super.key,
    required this.photo,
    this.color,
    required this.onTap,
  });

  final String photo;
  final Color? color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Theme.of(context).primaryColor.withOpacity(0.25),
      child: InkWell(
        onTap: onTap,
        child: LayoutBuilder(
          builder: (context, constraints) {
            return Image.asset(
              photo,
              fit: BoxFit.contain,
            );
          },
        ),
      ),
    );
  }
}
```

### Radial Hero Implementation

```dart
class CircularThumbnailScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Radial Hero')),
      body: Center(
        child: Hero(
          tag: 'radial_hero',
          createRectTween: (begin, end) {
            return MaterialRectCenterArcTween(begin: begin, end: end);
          },
          child: RadialExpansion(
            maxRadius: 50.0,
            child: Photo(
              photo: 'images/avatar.jpg',
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (context) => RadialDetailScreen(),
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }
}

class RadialDetailScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Detail')),
      body: Container(
        padding: EdgeInsets.all(16),
        alignment: Alignment.topLeft,
        child: Hero(
          tag: 'radial_hero',
          createRectTween: (begin, end) {
            return MaterialRectCenterArcTween(begin: begin, end: end);
          },
          child: Photo(
            photo: 'images/avatar.jpg',
            onTap: () => Navigator.of(context).pop(),
          ),
        ),
      ),
    );
  }
}
```

### MaterialRectCenterArcTween

The key difference in radial heroes is using `MaterialRectCenterArcTween`:

```dart
Hero(
  tag: 'my_hero',
  createRectTween: (begin, end) {
    return MaterialRectCenterArcTween(begin: begin, end: end);
  },
  child: // ...
)
```

This ensures the animation maintains the center point and aspect ratio during the transition, rather than morphing corners directly.

## Advanced Hero Patterns

### Custom Flight Path

Customize the animation curve and duration:

```dart
Hero(
  tag: 'custom_flight',
  flightShuttleBuilder: (
    BuildContext flightContext,
    Animation<double> animation,
    HeroFlightDirection flightDirection,
    BuildContext fromHeroContext,
    BuildContext toHeroContext,
  ) {
    return RotationTransition(
      turns: animation,
      child: Material(
        color: Colors.transparent,
        child: toHeroContext.widget,
      ),
    );
  },
  child: YourWidget(),
)
```

### Placeholder Builders

Show a different widget in place of the hero during flight:

```dart
Hero(
  tag: 'placeholder_hero',
  placeholderBuilder: (context, heroSize, child) {
    return Container(
      width: heroSize.width,
      height: heroSize.height,
      color: Colors.grey[300],
      child: Icon(Icons.image),
    );
  },
  child: Image.network('https://example.com/image.jpg'),
)
```

### Card Expansion Pattern

```dart
class CardListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Cards')),
      body: ListView.builder(
        itemCount: 10,
        itemBuilder: (context, index) {
          return Padding(
            padding: EdgeInsets.all(8),
            child: Hero(
              tag: 'card_$index',
              child: Card(
                child: ListTile(
                  leading: Icon(Icons.album),
                  title: Text('Item $index'),
                  subtitle: Text('Tap to expand'),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CardDetailScreen(
                          index: index,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class CardDetailScreen extends StatelessWidget {
  const CardDetailScreen({super.key, required this.index});

  final int index;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Detail $index')),
      body: Hero(
        tag: 'card_$index',
        child: Card(
          margin: EdgeInsets.all(16),
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.album, size: 60),
                    SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Item $index',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          Text('Expanded view'),
                        ],
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 20),
                Text('Additional details about item $index...'),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

## Controlling Hero Behavior

### Hero Properties

```dart
Hero(
  tag: 'my_hero',
  transitionOnUserGestures: true, // Animate during back swipe
  createRectTween: (begin, end) => RectTween(begin: begin, end: end),
  flightShuttleBuilder: (
    flightContext,
    animation,
    direction,
    fromContext,
    toContext,
  ) {
    // Custom widget during flight
    return DefaultTextStyle(
      style: DefaultTextStyle.of(toContext).style,
      child: toContext.widget,
    );
  },
  placeholderBuilder: (context, size, child) {
    // Widget shown in place of hero during flight
    return SizedBox(
      width: size.width,
      height: size.height,
      child: Placeholder(),
    );
  },
  child: YourWidget(),
)
```

### transitionOnUserGestures

Enable hero animation during interactive gestures (like iOS back swipe):

```dart
Hero(
  tag: 'interactive_hero',
  transitionOnUserGestures: true,
  child: Image.asset('photo.jpg'),
)
```

## Debugging Hero Animations

### Slow Down Animations

Use `timeDilation` to slow animations for debugging:

```dart
import 'package:flutter/scheduler.dart';

void main() {
  timeDilation = 5.0; // 5x slower
  runApp(MyApp());
}
```

### Visual Debugging

Enable size visualization:

```dart
void main() {
  debugPaintSizeEnabled = true;
  runApp(MyApp());
}
```

### Print Hero Flight Info

```dart
Hero(
  tag: 'debug_hero',
  flightShuttleBuilder: (
    flightContext,
    animation,
    direction,
    fromContext,
    toContext,
  ) {
    print('Hero flight direction: $direction');
    print('Animation value: ${animation.value}');
    return Material(
      color: Colors.transparent,
      child: toContext.widget,
    );
  },
  child: YourWidget(),
)
```

## Common Pitfalls and Solutions

### Problem: Hero Animation Not Working

**Cause**: Tags don't match or are not unique.

**Solution**: Ensure both heroes use identical tags:

```dart
// Source screen
Hero(tag: 'photo_1', child: ...)

// Destination screen
Hero(tag: 'photo_1', child: ...) // Must match exactly
```

### Problem: Multiple Heroes with Same Tag

**Cause**: Multiple visible heroes on the same screen share a tag.

**Solution**: Ensure tags are unique per screen. Use identifiers like IDs or indices:

```dart
Hero(tag: 'photo_${item.id}', child: ...)
```

### Problem: Hero Looks Wrong During Flight

**Cause**: Different widget trees between source and destination.

**Solution**: Keep the widget structure similar:

```dart
// Both heroes should wrap Image in Material
Hero(
  tag: 'photo',
  child: Material(
    color: Colors.transparent,
    child: Image.asset('photo.jpg'),
  ),
)
```

### Problem: Hero Clips Incorrectly

**Cause**: Clipping behavior differs between source and destination.

**Solution**: Apply consistent clipping on both screens or use `RadialExpansion` for circular heroes.

### Problem: Text Jumps During Hero Animation

**Cause**: Text style changes aren't animated smoothly.

**Solution**: Wrap text in `Material` with consistent `TextStyle`:

```dart
Hero(
  tag: 'title',
  child: Material(
    color: Colors.transparent,
    child: Text(
      'Title',
      style: TextStyle(fontSize: 20),
    ),
  ),
)
```

## Best Practices

### 1. Use Meaningful Tags

```dart
// GOOD - Descriptive and unique
Hero(tag: 'product_${product.id}', ...)

// BAD - Generic and collision-prone
Hero(tag: 'item', ...)
```

### 2. Keep Widget Trees Similar

The hero widget should have similar structure on both routes:

```dart
// Both screens
Hero(
  tag: 'profile_photo',
  child: Material(
    color: Colors.transparent,
    child: CircleAvatar(
      backgroundImage: NetworkImage(user.photoUrl),
    ),
  ),
)
```

### 3. Handle Loading States

Show placeholders during image loading:

```dart
Hero(
  tag: 'async_image',
  child: Material(
    color: Colors.transparent,
    child: FadeInImage(
      placeholder: AssetImage('assets/placeholder.png'),
      image: NetworkImage(imageUrl),
    ),
  ),
)
```

### 4. Optimize Image Heroes

Use appropriate image resolutions to avoid performance issues:

```dart
Hero(
  tag: 'optimized_image',
  child: Image.asset(
    'image.jpg',
    cacheWidth: 500, // Limit decoded size
  ),
)
```

### 5. Consider Accessibility

Ensure hero animations don't disorient users with reduced motion preferences:

```dart
final reduceMotion = MediaQuery.of(context).disableAnimations;

Navigator.push(
  context,
  PageRouteBuilder(
    transitionDuration: reduceMotion
        ? Duration.zero
        : Duration(milliseconds: 300),
    pageBuilder: (context, animation, secondaryAnimation) {
      return DetailScreen();
    },
  ),
);
```

## Performance Considerations

### 1. Image Caching

Hero animations with images work best when images are cached:

```dart
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  precacheImage(AssetImage('large_image.jpg'), context);
}
```

### 2. Avoid Expensive Widgets in Heroes

Keep hero widgets lightweight. Avoid embedding complex layouts:

```dart
// GOOD - Simple image hero
Hero(tag: 'photo', child: Image.asset('photo.jpg'))

// BAD - Complex widget tree
Hero(
  tag: 'complex',
  child: Column(
    children: [
      ComplexWidget1(),
      ComplexWidget2(),
      ExpensiveChart(),
    ],
  ),
)
```

### 3. Use RepaintBoundary

For complex heroes, wrap in `RepaintBoundary`:

```dart
Hero(
  tag: 'complex_hero',
  child: RepaintBoundary(
    child: ComplexWidget(),
  ),
)
```

## Conclusion

Hero animations are a powerful way to create fluid, continuous navigation experiences in Flutter apps. By understanding the animation lifecycle, using appropriate tags, and following best practices, you can implement smooth shared element transitions that enhance your app's user experience. Whether using standard hero animations for images or radial heroes for circular transformations, the pattern remains consistent: mark your heroes, match your tags, and let Flutter handle the magic.
