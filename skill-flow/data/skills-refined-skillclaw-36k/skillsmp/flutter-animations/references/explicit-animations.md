# Explicit Animations in Flutter

Explicit animations provide full control over the animation lifecycle through `AnimationController`. Unlike implicit animations that manage controllers automatically, explicit animations require you to create, configure, and dispose of controllers manually. This complexity comes with powerful capabilities: coordinating multiple animations, responding to user gestures, creating loops, and building custom animation choreography.

## Core Components

### AnimationController

The `AnimationController` is the heart of explicit animations. It's a special `Animation<double>` that generates sequential values, typically from 0.0 to 1.0, synchronized with the display's refresh rate (usually 60 frames per second).

#### Basic Setup

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Use controller to build animations
  }
}
```

#### Key Parameters

- **duration**: How long the animation takes to complete (0.0 to 1.0)
- **vsync**: Ticker provider that prevents offscreen animations from consuming resources
- **lowerBound**: Minimum value (default: 0.0)
- **upperBound**: Maximum value (default: 1.0)
- **value**: Initial value
- **animationBehavior**: Defines behavior during app lifecycle changes

#### The vsync Parameter

The `vsync` parameter is crucial for performance. It requires a `TickerProvider`, which you get by adding a mixin:

- **SingleTickerProviderStateMixin**: For a single AnimationController
- **TickerProviderStateMixin**: For multiple AnimationControllers

```dart
// Single controller
class _MyState extends State<MyWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
}

// Multiple controllers
class _MyState extends State<MyWidget> with TickerProviderStateMixin {
  late AnimationController _controller1;
  late AnimationController _controller2;
}
```

This ensures animations pause when the app is in the background, saving battery and resources.

### Animation Control Methods

#### forward()

Starts the animation from its current value to `upperBound`:

```dart
_controller.forward();

// With completion callback
_controller.forward().then((_) {
  print('Animation completed');
});

// Start from specific value
_controller.forward(from: 0.5);
```

#### reverse()

Runs the animation backward from current value to `lowerBound`:

```dart
_controller.reverse();

// With callback
_controller.reverse().then((_) {
  print('Animation reversed to start');
});

// Reverse from specific value
_controller.reverse(from: 1.0);
```

#### repeat()

Loops the animation continuously:

```dart
// Repeat forward only
_controller.repeat();

// Repeat with reverse (yo-yo effect)
_controller.repeat(reverse: true);

// Limit repetitions
_controller.repeat(
  reverse: true,
  period: Duration(seconds: 1),
);
```

#### animateTo()

Animates to a specific value:

```dart
_controller.animateTo(
  0.75,
  duration: Duration(milliseconds: 500),
  curve: Curves.easeOut,
);
```

#### stop()

Stops the animation at its current value:

```dart
_controller.stop();

// Check if stopped
if (!_controller.isAnimating) {
  print('Animation is stopped');
}
```

#### reset()

Resets the animation to its initial value (lowerBound):

```dart
_controller.reset();
```

### Animation Status

Track animation state with `AnimationStatus`:

```dart
_controller.addStatusListener((status) {
  switch (status) {
    case AnimationStatus.dismissed:
      print('Animation at start (lowerBound)');
      break;
    case AnimationStatus.forward:
      print('Animation playing forward');
      break;
    case AnimationStatus.reverse:
      print('Animation playing backward');
      break;
    case AnimationStatus.completed:
      print('Animation at end (upperBound)');
      break;
  }
});
```

Common pattern - create a loop:

```dart
_controller.addStatusListener((status) {
  if (status == AnimationStatus.completed) {
    _controller.reverse();
  } else if (status == AnimationStatus.dismissed) {
    _controller.forward();
  }
});
_controller.forward();
```

## Tween (In-Betweening)

`Tween` maps the controller's 0.0-1.0 range to custom values of any type.

### Basic Tweens

```dart
// Double values
final sizeTween = Tween<double>(begin: 0, end: 300);

// Integer values
final alphaTween = IntTween(begin: 0, end: 255);

// Color
final colorTween = ColorTween(
  begin: Colors.blue,
  end: Colors.red,
);

// Offset
final offsetTween = Tween<Offset>(
  begin: Offset.zero,
  end: Offset(1.0, 0.0),
);

// Border radius
final borderTween = BorderRadiusTween(
  begin: BorderRadius.circular(4),
  end: BorderRadius.circular(50),
);

// Rect
final rectTween = RectTween(
  begin: Rect.fromLTWH(0, 0, 50, 50),
  end: Rect.fromLTWH(100, 100, 200, 200),
);
```

### Using Tweens

Two primary methods:

#### 1. animate() - Creates New Animation

```dart
late AnimationController _controller;
late Animation<double> _animation;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    duration: const Duration(seconds: 2),
    vsync: this,
  );

  _animation = Tween<double>(begin: 0, end: 300).animate(_controller);
}

// Use _animation.value in build
Container(
  width: _animation.value,
  height: _animation.value,
)
```

#### 2. evaluate() - Gets Current Value

```dart
final tween = Tween<double>(begin: 0, end: 300);

// Get value at current animation position
final currentValue = tween.evaluate(_controller);
```

### Chaining Tweens

Combine tweens with curves:

```dart
final animation = Tween<double>(begin: 0, end: 300)
  .chain(CurveTween(curve: Curves.easeOut))
  .animate(_controller);
```

## CurvedAnimation

Applies non-linear easing curves to animations.

### Basic Usage

```dart
late AnimationController _controller;
late Animation<double> _curvedAnimation;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    duration: const Duration(seconds: 2),
    vsync: this,
  );

  _curvedAnimation = CurvedAnimation(
    parent: _controller,
    curve: Curves.easeInOut,
  );
}
```

### Common Curves

```dart
// Material Design standard
Curves.fastOutSlowIn

// Gentle easing
Curves.easeIn
Curves.easeOut
Curves.easeInOut

// Bouncy effects
Curves.bounceIn
Curves.bounceOut
Curves.bounceInOut

// Elastic effects
Curves.elasticIn
Curves.elasticOut
Curves.elasticInOut

// Cubic curves
Curves.decelerate
Curves.ease
Curves.linear
```

### Different Curves for Forward/Reverse

```dart
final animation = CurvedAnimation(
  parent: _controller,
  curve: Curves.easeIn,
  reverseCurve: Curves.easeOut,
);
```

### Custom Curves

```dart
class CustomCurve extends Curve {
  @override
  double transform(double t) {
    // Custom easing function
    return t * t; // Example: quadratic ease in
  }
}

// Usage
CurvedAnimation(
  parent: _controller,
  curve: CustomCurve(),
)
```

### Cubic Bézier Curves

```dart
final customCurve = Cubic(0.25, 0.1, 0.25, 1.0);

CurvedAnimation(
  parent: _controller,
  curve: customCurve,
)
```

## AnimatedBuilder

`AnimatedBuilder` is the most important widget for building efficient explicit animations. It rebuilds only the parts of your UI that depend on the animation.

### Basic Pattern

```dart
class LogoAnimation extends StatefulWidget {
  @override
  State<LogoAnimation> createState() => _LogoAnimationState();
}

class _LogoAnimationState extends State<LogoAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 300).animate(_controller);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: _animation.value,
          height: _animation.value,
          child: child,
        );
      },
      child: FlutterLogo(),
    );
  }
}
```

### Performance Optimization: child Parameter

The `child` parameter is critical for performance. Widgets passed as `child` are built once and reused:

```dart
// INEFFICIENT - FlutterLogo rebuilt every frame
AnimatedBuilder(
  animation: _animation,
  builder: (context, child) {
    return Container(
      width: _animation.value,
      height: _animation.value,
      child: FlutterLogo(), // Built 60 times per second!
    );
  },
)

// EFFICIENT - FlutterLogo built once
AnimatedBuilder(
  animation: _animation,
  builder: (context, child) {
    return Container(
      width: _animation.value,
      height: _animation.value,
      child: child, // Reused, not rebuilt
    );
  },
  child: FlutterLogo(), // Built once
)
```

### Multiple Properties

Animate multiple properties in a single builder:

```dart
class MultiPropertyAnimation extends StatefulWidget {
  @override
  State<MultiPropertyAnimation> createState() => _MultiPropertyAnimationState();
}

class _MultiPropertyAnimationState extends State<MultiPropertyAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _sizeAnimation;
  late Animation<double> _opacityAnimation;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    _sizeAnimation = Tween<double>(begin: 50, end: 200)
      .animate(CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ));

    _opacityAnimation = Tween<double>(begin: 0.2, end: 1.0)
      .animate(CurvedAnimation(
        parent: _controller,
        curve: Curves.easeIn,
      ));

    _colorAnimation = ColorTween(begin: Colors.blue, end: Colors.red)
      .animate(CurvedAnimation(
        parent: _controller,
        curve: Curves.linear,
      ));

    _controller.repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Opacity(
          opacity: _opacityAnimation.value,
          child: Container(
            width: _sizeAnimation.value,
            height: _sizeAnimation.value,
            decoration: BoxDecoration(
              color: _colorAnimation.value,
              borderRadius: BorderRadius.circular(20),
            ),
            child: child,
          ),
        );
      },
      child: Center(
        child: Icon(Icons.star, color: Colors.white, size: 50),
      ),
    );
  }
}
```

### Listening to Multiple Animations

Use `Listenable.merge()` to rebuild when any animation changes:

```dart
AnimatedBuilder(
  animation: Listenable.merge([_controller1, _controller2]),
  builder: (context, child) {
    return Transform.translate(
      offset: Offset(_controller1.value * 100, _controller2.value * 100),
      child: child,
    );
  },
  child: YourWidget(),
)
```

## AnimatedWidget

`AnimatedWidget` is a base class for creating reusable animated widgets. It's an alternative to `AnimatedBuilder` that's better suited for extracting animation logic into separate widgets.

### Basic Pattern

```dart
class SpinningLogo extends AnimatedWidget {
  const SpinningLogo({
    super.key,
    required Animation<double> animation,
  }) : super(listenable: animation);

  @override
  Widget build(BuildContext context) {
    final animation = listenable as Animation<double>;
    return Transform.rotate(
      angle: animation.value,
      child: FlutterLogo(size: 100),
    );
  }
}

// Usage:
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 6.28).animate(_controller);
    _controller.repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SpinningLogo(animation: _animation);
  }
}
```

### With Multiple Animations

```dart
class GrowingFadingBox extends AnimatedWidget {
  const GrowingFadingBox({
    super.key,
    required this.sizeAnimation,
    required this.opacityAnimation,
  }) : super(listenable: Listenable.merge([sizeAnimation, opacityAnimation]));

  final Animation<double> sizeAnimation;
  final Animation<double> opacityAnimation;

  @override
  Widget build(BuildContext context) {
    return Opacity(
      opacity: opacityAnimation.value,
      child: Container(
        width: sizeAnimation.value,
        height: sizeAnimation.value,
        color: Colors.blue,
      ),
    );
  }
}
```

### When to Use AnimatedWidget vs AnimatedBuilder

**Use AnimatedWidget when:**
- Creating a reusable animated widget
- The animation logic is self-contained
- You want a clean separation of concerns
- The widget will be used in multiple places

**Use AnimatedBuilder when:**
- The animation is specific to one location
- You need inline animation logic
- The animation depends on local state
- You want more flexibility in the builder

## Built-in AnimatedWidgets

Flutter provides several pre-built `AnimatedWidget` subclasses for common transitions:

### FadeTransition

```dart
late AnimationController _controller;
late Animation<double> _animation;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    duration: const Duration(seconds: 2),
    vsync: this,
  );
  _animation = CurvedAnimation(parent: _controller, curve: Curves.easeIn);
  _controller.forward();
}

@override
Widget build(BuildContext context) {
  return FadeTransition(
    opacity: _animation,
    child: FlutterLogo(size: 100),
  );
}
```

### ScaleTransition

```dart
ScaleTransition(
  scale: _animation,
  child: FlutterLogo(size: 100),
)
```

### RotationTransition

```dart
RotationTransition(
  turns: _animation, // 0.0 to 1.0 = 0 to 360 degrees
  child: FlutterLogo(size: 100),
)
```

### SlideTransition

```dart
final offsetAnimation = Tween<Offset>(
  begin: Offset.zero,
  end: Offset(1.5, 0.0),
).animate(CurvedAnimation(
  parent: _controller,
  curve: Curves.easeInOut,
));

SlideTransition(
  position: offsetAnimation,
  child: FlutterLogo(size: 100),
)
```

### SizeTransition

```dart
SizeTransition(
  sizeFactor: _animation,
  axis: Axis.horizontal,
  child: FlutterLogo(size: 100),
)
```

### PositionedTransition

Only works inside a Stack:

```dart
final rectAnimation = RelativeRectTween(
  begin: RelativeRect.fromLTRB(0, 0, 0, 0),
  end: RelativeRect.fromLTRB(100, 100, 0, 0),
).animate(_controller);

Stack(
  children: [
    PositionedTransition(
      rect: rectAnimation,
      child: FlutterLogo(size: 100),
    ),
  ],
)
```

### DecoratedBoxTransition

```dart
final decorationAnimation = DecorationTween(
  begin: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  end: BoxDecoration(
    color: Colors.red,
    borderRadius: BorderRadius.circular(50),
  ),
).animate(_controller);

DecoratedBoxTransition(
  decoration: decorationAnimation,
  child: Container(
    width: 100,
    height: 100,
    child: Center(child: Text('Animating')),
  ),
)
```

### AlignTransition

```dart
final alignAnimation = Tween<AlignmentGeometry>(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
).animate(_controller);

Container(
  width: 300,
  height: 300,
  child: AlignTransition(
    alignment: alignAnimation,
    child: FlutterLogo(size: 50),
  ),
)
```

### DefaultTextStyleTransition

```dart
final textStyleAnimation = TextStyleTween(
  begin: TextStyle(fontSize: 20, color: Colors.blue),
  end: TextStyle(fontSize: 50, color: Colors.red),
).animate(_controller);

DefaultTextStyleTransition(
  style: textStyleAnimation,
  child: Text('Animating Text'),
)
```

## Combining Animations

### Sequential Animations

Use status listeners to chain animations:

```dart
class SequentialAnimation extends StatefulWidget {
  @override
  State<SequentialAnimation> createState() => _SequentialAnimationState();
}

class _SequentialAnimationState extends State<SequentialAnimation>
    with TickerProviderStateMixin {
  late AnimationController _controller1;
  late AnimationController _controller2;

  @override
  void initState() {
    super.initState();

    _controller1 = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );

    _controller2 = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );

    _controller1.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        _controller2.forward();
      }
    });

    _controller1.forward();
  }

  @override
  void dispose() {
    _controller1.dispose();
    _controller2.dispose();
    super.dispose();
  }
}
```

### Parallel Animations

Multiple animations driven by the same controller:

```dart
class ParallelAnimations extends StatefulWidget {
  @override
  State<ParallelAnimations> createState() => _ParallelAnimationsState();
}

class _ParallelAnimationsState extends State<ParallelAnimations>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _rotationAnimation;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 0.5, end: 2.0)
      .animate(CurvedAnimation(
        parent: _controller,
        curve: Curves.elasticOut,
      ));

    _rotationAnimation = Tween<double>(begin: 0, end: 2 * 3.14159)
      .animate(CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ));

    _colorAnimation = ColorTween(begin: Colors.blue, end: Colors.purple)
      .animate(_controller);

    _controller.forward();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.rotate(
          angle: _rotationAnimation.value,
          child: Transform.scale(
            scale: _scaleAnimation.value,
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color: _colorAnimation.value,
                borderRadius: BorderRadius.circular(20),
              ),
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

## Advanced Patterns

### Value Listeners

React to specific animation values:

```dart
_animation.addListener(() {
  if (_animation.value > 0.5 && !_midpointReached) {
    _midpointReached = true;
    print('Animation passed midpoint');
  }

  if (_animation.value > 0.9) {
    // Trigger something near completion
  }
});
```

### Custom Animation Values

Access controller value directly for custom calculations:

```dart
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    final value = _controller.value;
    final customValue = math.sin(value * math.pi * 2);

    return Transform.translate(
      offset: Offset(0, customValue * 50),
      child: child,
    );
  },
  child: YourWidget(),
)
```

### Drive Multiple Animations from One Controller

```dart
final controller = AnimationController(
  duration: Duration(seconds: 3),
  vsync: this,
);

final animation1 = Tween<double>(begin: 0, end: 100)
  .animate(CurvedAnimation(
    parent: controller,
    curve: Interval(0.0, 0.5, curve: Curves.easeOut),
  ));

final animation2 = Tween<double>(begin: 0, end: 100)
  .animate(CurvedAnimation(
    parent: controller,
    curve: Interval(0.5, 1.0, curve: Curves.easeIn),
  ));
```

## Performance Best Practices

### 1. Dispose Controllers

Always dispose controllers to prevent memory leaks:

```dart
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

### 2. Use RepaintBoundary

Isolate expensive widgets from animation rebuilds:

```dart
AnimatedBuilder(
  animation: _animation,
  builder: (context, child) {
    return Column(
      children: [
        Transform.scale(
          scale: _animation.value,
          child: AnimatedWidget(),
        ),
        RepaintBoundary(
          child: ExpensiveStaticWidget(),
        ),
      ],
    );
  },
)
```

### 3. Minimize Builder Scope

Only rebuild what needs to change:

```dart
// BAD - Rebuilds entire Column
AnimatedBuilder(
  animation: _animation,
  builder: (context, child) {
    return Column(
      children: [
        AnimatedWidget(_animation.value),
        StaticWidget1(),
        StaticWidget2(),
      ],
    );
  },
)

// GOOD - Only rebuilds animated part
Column(
  children: [
    AnimatedBuilder(
      animation: _animation,
      builder: (context, child) => AnimatedWidget(_animation.value),
    ),
    StaticWidget1(),
    StaticWidget2(),
  ],
)
```

### 4. Reuse Animation Objects

Don't create new Tween/CurvedAnimation objects in build:

```dart
// BAD
@override
Widget build(BuildContext context) {
  final animation = Tween<double>(begin: 0, end: 100)
    .animate(_controller); // Created every build!
  // ...
}

// GOOD
late Animation<double> _animation;

@override
void initState() {
  super.initState();
  _animation = Tween<double>(begin: 0, end: 100)
    .animate(_controller); // Created once
}
```

## Common Pitfalls

### 1. Forgetting vsync

```dart
// WRONG - No vsync
AnimationController(duration: Duration(seconds: 1))

// CORRECT
AnimationController(
  duration: Duration(seconds: 1),
  vsync: this,
)
```

### 2. Not Disposing Controllers

Memory leaks occur if controllers aren't disposed.

### 3. Using setState in addListener

```dart
// INEFFICIENT
_animation.addListener(() {
  setState(() {}); // Rebuilds entire widget
});

// BETTER - Use AnimatedBuilder
AnimatedBuilder(
  animation: _animation,
  builder: (context, child) => ...,
)
```

### 4. Animating Opacity Incorrectly

```dart
// INEFFICIENT
Opacity(
  opacity: _animation.value,
  child: ExpensiveWidget(),
)

// BETTER
FadeTransition(
  opacity: _animation,
  child: ExpensiveWidget(),
)
```

## Conclusion

Explicit animations provide the foundation for sophisticated animation experiences in Flutter. While they require more setup than implicit animations, they offer precise control over timing, coordination, and interaction. Master the core components - `AnimationController`, `Tween`, `CurvedAnimation`, and `AnimatedBuilder` - and you'll be able to create any animation effect your app requires.
