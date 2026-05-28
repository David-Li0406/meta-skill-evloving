# Custom Page Transitions in Flutter

Custom page transitions allow you to control exactly how one screen transitions to another, replacing the default platform-specific animations with custom effects like slides, fades, scales, or combinations thereof. Flutter provides `PageRouteBuilder` as the foundation for creating these custom transitions.

## Understanding PageRouteBuilder

`PageRouteBuilder` is a generic class that lets you define custom transitions by providing two key builders:

- **pageBuilder**: Returns the content of the new route (required)
- **transitionsBuilder**: Defines how the transition animation looks (required)

### Basic Structure

```dart
Navigator.push(
  context,
  PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) {
      return DestinationPage();
    },
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      return child; // No animation yet
    },
  ),
);
```

### Key Parameters

- **context**: BuildContext for the route
- **animation**: Primary animation from 0.0 to 1.0 during the forward transition
- **secondaryAnimation**: Animation for the page being pushed on top of this one
- **child**: The widget returned by `pageBuilder` (reused for performance)

## Animation and Tween Basics

The `animation` parameter is an `Animation<double>` that goes from 0.0 to 1.0. To create meaningful transitions, you need to transform this using `Tween` and apply it with transition widgets.

### Creating a Tween

```dart
final tween = Tween<Offset>(
  begin: Offset(1.0, 0.0), // Start position (off-screen right)
  end: Offset.zero,         // End position (on-screen)
);
```

### Driving the Animation

```dart
final offsetAnimation = animation.drive(tween);
```

### Applying with Transition Widget

```dart
SlideTransition(
  position: offsetAnimation,
  child: child,
)
```

## Common Transition Patterns

### Slide Transition

Slides the new page in from a direction.

#### Slide from Right

```dart
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    const begin = Offset(1.0, 0.0); // Start off-screen to the right
    const end = Offset.zero;        // End at normal position
    const curve = Curves.easeInOut;

    final tween = Tween(begin: begin, end: end);
    final curvedAnimation = CurvedAnimation(
      parent: animation,
      curve: curve,
    );

    return SlideTransition(
      position: tween.animate(curvedAnimation),
      child: child,
    );
  },
)
```

#### Slide from Bottom

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  const begin = Offset(0.0, 1.0); // Start below screen
  const end = Offset.zero;
  const curve = Curves.easeOut;

  final tween = Tween(begin: begin, end: end)
    .chain(CurveTween(curve: curve));

  return SlideTransition(
    position: animation.drive(tween),
    child: child,
  );
}
```

#### Slide from Left

```dart
const begin = Offset(-1.0, 0.0); // Start off-screen to the left
```

#### Slide from Top

```dart
const begin = Offset(0.0, -1.0); // Start above screen
```

### Fade Transition

Fades the new page in.

```dart
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(
      opacity: animation,
      child: child,
    );
  },
)
```

#### Fade with Custom Curve

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  final curvedAnimation = CurvedAnimation(
    parent: animation,
    curve: Curves.easeIn,
  );

  return FadeTransition(
    opacity: curvedAnimation,
    child: child,
  );
}
```

### Scale Transition

Scales the new page from small to full size.

```dart
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    const curve = Curves.easeInOut;

    final curvedAnimation = CurvedAnimation(
      parent: animation,
      curve: curve,
    );

    return ScaleTransition(
      scale: curvedAnimation,
      child: child,
    );
  },
)
```

#### Scale from Center with Fade

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return ScaleTransition(
    scale: Tween<double>(begin: 0.0, end: 1.0)
      .animate(CurvedAnimation(
        parent: animation,
        curve: Curves.fastOutSlowIn,
      )),
    child: FadeTransition(
      opacity: animation,
      child: child,
    ),
  );
}
```

### Rotation Transition

Rotates the new page as it appears.

```dart
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return RotationTransition(
      turns: Tween<double>(begin: 0.0, end: 1.0)
        .animate(CurvedAnimation(
          parent: animation,
          curve: Curves.easeInOut,
        )),
      child: child,
    );
  },
)
```

## Combined Transitions

Combine multiple transition effects for rich animations.

### Slide and Fade

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  const begin = Offset(0.0, 1.0);
  const end = Offset.zero;
  const curve = Curves.easeInOut;

  final tween = Tween(begin: begin, end: end)
    .chain(CurveTween(curve: curve));
  final offsetAnimation = animation.drive(tween);

  return SlideTransition(
    position: offsetAnimation,
    child: FadeTransition(
      opacity: animation,
      child: child,
    ),
  );
}
```

### Scale and Rotate

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return ScaleTransition(
    scale: Tween<double>(begin: 0.0, end: 1.0)
      .animate(CurvedAnimation(
        parent: animation,
        curve: Curves.fastOutSlowIn,
      )),
    child: RotationTransition(
      turns: Tween<double>(begin: 0.0, end: 0.25)
        .animate(CurvedAnimation(
          parent: animation,
          curve: Curves.easeInOut,
        )),
      child: child,
    ),
  );
}
```

### Slide with Scale

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  const begin = Offset(1.0, 0.0);
  const end = Offset.zero;
  final slideTween = Tween(begin: begin, end: end)
    .chain(CurveTween(curve: Curves.easeOut));

  final scaleTween = Tween<double>(begin: 0.8, end: 1.0)
    .chain(CurveTween(curve: Curves.easeOut));

  return SlideTransition(
    position: animation.drive(slideTween),
    child: ScaleTransition(
      scale: animation.drive(scaleTween),
      child: child,
    ),
  );
}
```

## Advanced Transition Patterns

### Shared Axis Transition (Material Motion)

Material Design's shared axis transition pattern.

```dart
class SharedAxisPageRoute extends PageRouteBuilder {
  final Widget page;

  SharedAxisPageRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return _buildSharedAxisTransition(
              context,
              animation,
              secondaryAnimation,
              child,
            );
          },
        );

  static Widget _buildSharedAxisTransition(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    return FadeTransition(
      opacity: Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(
          parent: animation,
          curve: Interval(0.3, 1.0, curve: Curves.easeIn),
        ),
      ),
      child: SlideTransition(
        position: Tween<Offset>(
          begin: Offset(0.0, 0.3),
          end: Offset.zero,
        ).animate(
          CurvedAnimation(
            parent: animation,
            curve: Curves.easeOut,
          ),
        ),
        child: FadeTransition(
          opacity: Tween<double>(begin: 1.0, end: 0.0).animate(
            CurvedAnimation(
              parent: secondaryAnimation,
              curve: Interval(0.0, 0.7, curve: Curves.easeOut),
            ),
          ),
          child: child,
        ),
      ),
    );
  }
}
```

### Fade Through Transition

```dart
class FadeThroughPageRoute extends PageRouteBuilder {
  final Widget page;

  FadeThroughPageRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(
              opacity: Tween<double>(begin: 0.0, end: 1.0).animate(
                CurvedAnimation(
                  parent: animation,
                  curve: Interval(0.5, 1.0, curve: Curves.easeIn),
                ),
              ),
              child: ScaleTransition(
                scale: Tween<double>(begin: 0.92, end: 1.0).animate(
                  CurvedAnimation(
                    parent: animation,
                    curve: Interval(0.5, 1.0, curve: Curves.easeOut),
                  ),
                ),
                child: child,
              ),
            );
          },
        );
}
```

### Custom Slide with Secondary Animation

Animate both the incoming and outgoing pages:

```dart
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    // Incoming page slides in from right
    const incomingBegin = Offset(1.0, 0.0);
    const incomingEnd = Offset.zero;
    final incomingTween = Tween(begin: incomingBegin, end: incomingEnd)
      .chain(CurveTween(curve: Curves.easeOut));

    // Outgoing page slides out to left
    const outgoingBegin = Offset.zero;
    const outgoingEnd = Offset(-0.3, 0.0);
    final outgoingTween = Tween(begin: outgoingBegin, end: outgoingEnd)
      .chain(CurveTween(curve: Curves.easeOut));

    return SlideTransition(
      position: animation.drive(incomingTween),
      child: child,
    );
  },
)
```

## Reusable Route Classes

Create reusable custom route classes for consistent transitions throughout your app.

### SlideRightRoute

```dart
class SlideRightRoute extends PageRouteBuilder {
  final Widget page;

  SlideRightRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            const begin = Offset(1.0, 0.0);
            const end = Offset.zero;
            const curve = Curves.easeInOut;

            final tween = Tween(begin: begin, end: end)
              .chain(CurveTween(curve: curve));

            return SlideTransition(
              position: animation.drive(tween),
              child: child,
            );
          },
        );
}

// Usage:
Navigator.push(
  context,
  SlideRightRoute(page: DestinationPage()),
);
```

### FadeRoute

```dart
class FadeRoute extends PageRouteBuilder {
  final Widget page;
  final Duration duration;

  FadeRoute({
    required this.page,
    this.duration = const Duration(milliseconds: 300),
  }) : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionDuration: duration,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(
              opacity: CurvedAnimation(
                parent: animation,
                curve: Curves.easeInOut,
              ),
              child: child,
            );
          },
        );
}
```

### ScaleRoute

```dart
class ScaleRoute extends PageRouteBuilder {
  final Widget page;

  ScaleRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return ScaleTransition(
              scale: Tween<double>(begin: 0.0, end: 1.0).animate(
                CurvedAnimation(
                  parent: animation,
                  curve: Curves.fastOutSlowIn,
                ),
              ),
              child: child,
            );
          },
        );
}
```

### Custom Configurable Route

```dart
enum TransitionType { fade, slide, scale, rotate }

class CustomPageRoute extends PageRouteBuilder {
  final Widget page;
  final TransitionType transitionType;
  final Duration duration;
  final Curve curve;

  CustomPageRoute({
    required this.page,
    this.transitionType = TransitionType.fade,
    this.duration = const Duration(milliseconds: 300),
    this.curve = Curves.easeInOut,
  }) : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionDuration: duration,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return _buildTransition(
              transitionType,
              animation,
              curve,
              child,
            );
          },
        );

  static Widget _buildTransition(
    TransitionType type,
    Animation<double> animation,
    Curve curve,
    Widget child,
  ) {
    final curvedAnimation = CurvedAnimation(
      parent: animation,
      curve: curve,
    );

    switch (type) {
      case TransitionType.fade:
        return FadeTransition(
          opacity: curvedAnimation,
          child: child,
        );

      case TransitionType.slide:
        return SlideTransition(
          position: Tween<Offset>(
            begin: Offset(1.0, 0.0),
            end: Offset.zero,
          ).animate(curvedAnimation),
          child: child,
        );

      case TransitionType.scale:
        return ScaleTransition(
          scale: Tween<double>(begin: 0.0, end: 1.0)
            .animate(curvedAnimation),
          child: child,
        );

      case TransitionType.rotate:
        return RotationTransition(
          turns: Tween<double>(begin: 0.0, end: 1.0)
            .animate(curvedAnimation),
          child: child,
        );
    }
  }
}

// Usage:
Navigator.push(
  context,
  CustomPageRoute(
    page: DestinationPage(),
    transitionType: TransitionType.slide,
    duration: Duration(milliseconds: 400),
    curve: Curves.fastOutSlowIn,
  ),
);
```

## Controlling Transition Duration

Customize how long the transition takes:

```dart
PageRouteBuilder(
  transitionDuration: const Duration(milliseconds: 600),
  reverseTransitionDuration: const Duration(milliseconds: 300),
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(opacity: animation, child: child);
  },
)
```

## Custom Route Settings

Pass arguments and configure route settings:

```dart
PageRouteBuilder(
  settings: RouteSettings(
    name: '/destination',
    arguments: {'id': 123, 'title': 'Example'},
  ),
  pageBuilder: (context, animation, secondaryAnimation) {
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    return DestinationPage(
      id: args['id'],
      title: args['title'],
    );
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(opacity: animation, child: child);
  },
)
```

## Full-Screen Dialog Transitions

Create modal-style transitions:

```dart
PageRouteBuilder(
  fullscreenDialog: true,
  transitionDuration: const Duration(milliseconds: 300),
  pageBuilder: (context, animation, secondaryAnimation) {
    return DialogPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    const begin = Offset(0.0, 1.0);
    const end = Offset.zero;
    const curve = Curves.easeOut;

    final tween = Tween(begin: begin, end: end)
      .chain(CurveTween(curve: curve));

    return SlideTransition(
      position: animation.drive(tween),
      child: child,
    );
  },
)
```

## Opaque vs Transparent Routes

### Opaque Route (Default)

Blocks underlying routes from rendering:

```dart
PageRouteBuilder(
  opaque: true, // Default
  pageBuilder: (context, animation, secondaryAnimation) {
    return DestinationPage();
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(opacity: animation, child: child);
  },
)
```

### Transparent Route

Allows underlying routes to show through:

```dart
PageRouteBuilder(
  opaque: false,
  barrierColor: Colors.black54,
  barrierDismissible: true,
  pageBuilder: (context, animation, secondaryAnimation) {
    return Center(
      child: Container(
        width: 300,
        height: 400,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
        ),
        child: ModalContent(),
      ),
    );
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return ScaleTransition(
      scale: Tween<double>(begin: 0.0, end: 1.0)
        .animate(CurvedAnimation(
          parent: animation,
          curve: Curves.fastOutSlowIn,
        )),
      child: FadeTransition(
        opacity: animation,
        child: child,
      ),
    );
  },
)
```

## Performance Optimization

### Use Child Parameter

Always pass static widgets as `child` to avoid rebuilding:

```dart
// BAD - Logo rebuilt every frame
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return FadeTransition(
    opacity: animation,
    child: FlutterLogo(), // Rebuilt 60 times per second!
  );
}

// GOOD - Logo built once
PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) {
    return Scaffold(
      body: Center(
        child: FlutterLogo(), // Built once by pageBuilder
      ),
    );
  },
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(
      opacity: animation,
      child: child, // Reuses widget from pageBuilder
    );
  },
)
```

### Caching Tweens

Create tweens once, not on every transition:

```dart
class _MyPageState extends State<MyPage> {
  static final _tween = Tween<Offset>(
    begin: Offset(1.0, 0.0),
    end: Offset.zero,
  );

  void _navigate() {
    Navigator.push(
      context,
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) {
          return DestinationPage();
        },
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return SlideTransition(
            position: _tween.animate(animation),
            child: child,
          );
        },
      ),
    );
  }
}
```

## Platform-Specific Transitions

Adapt transitions based on platform:

```dart
Route _createRoute() {
  if (Theme.of(context).platform == TargetPlatform.iOS) {
    return CupertinoPageRoute(
      builder: (context) => DestinationPage(),
    );
  } else {
    return PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) {
        return DestinationPage();
      },
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(opacity: animation, child: child);
      },
    );
  }
}
```

## Conclusion

Custom page transitions give you complete control over navigation animations in Flutter. By mastering `PageRouteBuilder`, tweens, and transition widgets, you can create polished, brand-specific navigation experiences that enhance your app's usability and visual appeal. Start with simple transitions like fades and slides, then combine them to create sophisticated effects that match your design vision.
