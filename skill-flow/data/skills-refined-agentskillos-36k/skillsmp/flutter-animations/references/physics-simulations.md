# Physics-Based Animations in Flutter

Physics-based animations model real-world physical behavior like springs, gravity, and friction to create natural, realistic motion. Unlike tween-based animations that follow predetermined paths and durations, physics simulations calculate motion based on forces, velocity, and mass, resulting in animations that feel organic and responsive.

## Why Physics-Based Animations?

**Natural Motion**: Physics simulations create movement that matches user expectations based on real-world experience. A spring bounce feels right because we understand how springs behave.

**Velocity Preservation**: When responding to gestures, physics simulations can incorporate the user's flick or drag velocity, making interactions feel direct and responsive.

**Self-Adjusting Duration**: Physics simulations don't have fixed durations. The animation completes when the simulation reaches equilibrium, which depends on the initial conditions and physics parameters.

**Continuity**: If a user interrupts an animation with a new gesture, the physics simulation can seamlessly transition from the current state without jarring jumps.

## Core Concepts

### Simulation

A `Simulation` is an abstract class that maps elapsed time to a double value. Flutter provides several built-in simulations in the `flutter/physics.dart` package:

- `SpringSimulation` - Models spring physics (most common)
- `GravitySimulation` - Models gravity and free fall
- `FrictionSimulation` - Models friction-based deceleration
- `ClampedSimulation` - Clamps another simulation's output

### AnimationController with Simulations

Instead of using `forward()` or `animateTo()`, you use `animateWith()` to drive an animation controller with a physics simulation:

```dart
controller.animateWith(simulation);
```

## SpringSimulation

`SpringSimulation` is the most versatile and commonly used physics simulation. It models a spring system with mass, stiffness, and damping.

### Spring Parameters

```dart
class SpringDescription {
  final double mass;       // Mass of the object (higher = slower response)
  final double stiffness;  // Spring constant (higher = stiffer, snappier)
  final double damping;    // Damping coefficient (higher = less bouncy)
}
```

**Mass**: Represents the inertia of the animated object. Higher mass means the object resists changes in motion more, leading to slower acceleration and deceleration.

**Stiffness**: The spring constant. Higher stiffness creates a tighter spring that responds quickly and snaps into place. Lower stiffness creates a looser, more gradual spring.

**Damping**: Controls how quickly oscillations decay. Higher damping reduces or eliminates bouncing. Lower damping creates more pronounced oscillations.

### Critical Damping

The relationship between mass, stiffness, and damping determines the spring's behavior:

```dart
// Critical damping ratio
final criticalDamping = 2.0 * math.sqrt(mass * stiffness);

// Underdamped (bouncy): damping < criticalDamping
// Critically damped (no overshoot): damping = criticalDamping
// Overdamped (sluggish): damping > criticalDamping
```

Flutter provides a helper for critically damped springs:

```dart
final spring = SpringDescription.withDampingRatio(
  mass: 1.0,
  stiffness: 100.0,
  ratio: 1.0, // Critical damping
);
```

### Basic SpringSimulation Example

```dart
import 'package:flutter/physics.dart';

class SpringAnimationWidget extends StatefulWidget {
  @override
  State<SpringAnimationWidget> createState() => _SpringAnimationWidgetState();
}

class _SpringAnimationWidgetState extends State<SpringAnimationWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      lowerBound: 0.0,
      upperBound: 1.0,
    );

    _animation = _controller;

    _controller.addListener(() {
      setState(() {});
    });
  }

  void _runSpringAnimation() {
    final spring = SpringDescription(
      mass: 1.0,
      stiffness: 100.0,
      damping: 10.0,
    );

    final simulation = SpringSimulation(
      spring,
      0.0,  // Starting position
      1.0,  // Ending position
      0.0,  // Initial velocity
    );

    _controller.animateWith(simulation);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Transform.scale(
          scale: _animation.value,
          child: Container(
            width: 100,
            height: 100,
            color: Colors.blue,
          ),
        ),
        SizedBox(height: 40),
        ElevatedButton(
          onPressed: _runSpringAnimation,
          child: Text('Animate'),
        ),
      ],
    );
  }
}
```

### Interactive Draggable with Spring

The canonical example: a draggable widget that springs back when released.

```dart
import 'package:flutter/physics.dart';
import 'package:flutter/material.dart';

class DraggableCard extends StatefulWidget {
  final Widget child;

  const DraggableCard({super.key, required this.child});

  @override
  State<DraggableCard> createState() => _DraggableCardState();
}

class _DraggableCardState extends State<DraggableCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Alignment> _animation;
  Alignment _dragAlignment = Alignment.center;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);

    _controller.addListener(() {
      setState(() {
        _dragAlignment = _animation.value;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _runAnimation(Offset pixelsPerSecond, Size size) {
    _animation = _controller.drive(
      AlignmentTween(
        begin: _dragAlignment,
        end: Alignment.center,
      ),
    );

    // Convert pixel velocity to unit velocity (0.0 to 1.0 per second)
    final unitsPerSecondX = pixelsPerSecond.dx / size.width;
    final unitsPerSecondY = pixelsPerSecond.dy / size.height;
    final unitsPerSecond = Offset(unitsPerSecondX, unitsPerSecondY);
    final unitVelocity = unitsPerSecond.distance;

    const spring = SpringDescription(
      mass: 30,      // Higher mass = more inertia
      stiffness: 1,  // Lower stiffness = slower return
      damping: 1,    // Minimal damping for bounce
    );

    final simulation = SpringSimulation(spring, 0, 1, -unitVelocity);

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return GestureDetector(
      onPanDown: (details) {
        _controller.stop();
      },
      onPanUpdate: (details) {
        setState(() {
          _dragAlignment += Alignment(
            details.delta.dx / (size.width / 2),
            details.delta.dy / (size.height / 2),
          );
        });
      },
      onPanEnd: (details) {
        _runAnimation(details.velocity.pixelsPerSecond, size);
      },
      child: Align(
        alignment: _dragAlignment,
        child: Card(
          child: widget.child,
        ),
      ),
    );
  }
}

// Usage:
DraggableCard(
  child: Container(
    width: 100,
    height: 100,
    color: Colors.blue,
    child: Center(child: Text('Drag me')),
  ),
)
```

### Key Points in Draggable Example

**Velocity Conversion**: The gesture velocity is in pixels per second. To use it with the animation (which works in 0.0-1.0 coordinates), you must convert:

```dart
final unitsPerSecondX = pixelsPerSecond.dx / size.width;
final unitsPerSecondY = pixelsPerSecond.dy / size.height;
```

**Negative Velocity**: The simulation uses `-unitVelocity` because the animation goes from current position (0) to center (1), but the velocity direction is typically away from center.

**Stopping on Touch**: When the user touches the dragging widget, `_controller.stop()` halts the spring animation so the user can take control.

## Spring Tuning

Different spring parameters create different feels:

### Bouncy Spring

```dart
final bouncySpring = SpringDescription(
  mass: 1.0,
  stiffness: 50.0,
  damping: 3.0, // Low damping = bouncy
);
```

### Snappy Spring

```dart
final snappySpring = SpringDescription(
  mass: 1.0,
  stiffness: 500.0, // High stiffness = fast
  damping: 30.0,
);
```

### Gentle Spring

```dart
final gentleSpring = SpringDescription(
  mass: 2.0,      // Higher mass = slower
  stiffness: 20.0, // Lower stiffness = gentle
  damping: 10.0,
);
```

### Critically Damped (No Overshoot)

```dart
final criticalSpring = SpringDescription.withDampingRatio(
  mass: 1.0,
  stiffness: 100.0,
  ratio: 1.0, // No bounce, smooth settling
);
```

### Underdamped (Oscillates)

```dart
final underdampedSpring = SpringDescription.withDampingRatio(
  mass: 1.0,
  stiffness: 100.0,
  ratio: 0.5, // Oscillates before settling
);
```

## GravitySimulation

Models free fall under gravity with optional acceleration limits.

### Basic Gravity

```dart
import 'package:flutter/physics.dart';

class FallingBox extends StatefulWidget {
  @override
  State<FallingBox> createState() => _FallingBoxState();
}

class _FallingBoxState extends State<FallingBox>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      lowerBound: 0.0,
      upperBound: 500.0, // Maximum fall distance
    );

    _animation = _controller;

    _controller.addListener(() {
      setState(() {});
    });
  }

  void _drop() {
    final simulation = GravitySimulation(
      9.8,   // Acceleration (m/s^2)
      0.0,   // Starting position
      500.0, // Ending position
      0.0,   // Initial velocity
    );

    _controller.animateWith(simulation);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Positioned(
          top: _animation.value,
          left: 100,
          child: Container(
            width: 50,
            height: 50,
            color: Colors.red,
          ),
        ),
        Positioned(
          bottom: 20,
          left: 0,
          right: 0,
          child: Center(
            child: ElevatedButton(
              onPressed: () {
                _controller.reset();
                _drop();
              },
              child: Text('Drop'),
            ),
          ),
        ),
      ],
    );
  }
}
```

### Bouncing Ball with Gravity

```dart
class BouncingBall extends StatefulWidget {
  @override
  State<BouncingBall> createState() => _BouncingBallState();
}

class _BouncingBallState extends State<BouncingBall>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  double _velocity = 0.0;
  final double _gravity = 500.0;
  final double _bounceFactor = 0.7; // Energy retained on bounce

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      lowerBound: 0.0,
      upperBound: 400.0,
    );

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        // Bounce
        _velocity = -_velocity * _bounceFactor;
        if (_velocity.abs() > 5.0) {
          _drop(_velocity);
        }
      }
    });

    _controller.addListener(() {
      setState(() {});
    });
  }

  void _drop(double initialVelocity) {
    final simulation = GravitySimulation(
      _gravity,
      _controller.value,
      400.0,
      initialVelocity,
    );

    _controller.animateWith(simulation);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        _controller.reset();
        _velocity = 0.0;
        _drop(0.0);
      },
      child: Stack(
        children: [
          Positioned(
            top: _controller.value,
            left: MediaQuery.of(context).size.width / 2 - 25,
            child: Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                color: Colors.blue,
                shape: BoxShape.circle,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

## FrictionSimulation

Models deceleration due to friction, useful for scroll physics and momentum.

### Basic Friction

```dart
class FrictionScrollWidget extends StatefulWidget {
  @override
  State<FrictionScrollWidget> createState() => _FrictionScrollWidgetState();
}

class _FrictionScrollWidgetState extends State<FrictionScrollWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      lowerBound: -500.0,
      upperBound: 500.0,
    );

    _animation = _controller;

    _controller.addListener(() {
      setState(() {});
    });
  }

  void _fling(double velocity) {
    final simulation = FrictionSimulation(
      0.05,             // Drag coefficient
      _controller.value, // Starting position
      velocity,         // Initial velocity
    );

    _controller.animateWith(simulation);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onHorizontalDragEnd: (details) {
        _fling(details.velocity.pixelsPerSecond.dx);
      },
      child: Container(
        color: Colors.grey[200],
        child: Transform.translate(
          offset: Offset(_animation.value, 0),
          child: Container(
            width: 100,
            height: 100,
            color: Colors.blue,
            child: Center(child: Text('Fling me')),
          ),
        ),
      ),
    );
  }
}
```

## ClampedSimulation

Wraps another simulation and clamps its output to a range.

```dart
final spring = SpringSimulation(
  SpringDescription(mass: 1.0, stiffness: 100.0, damping: 10.0),
  0.0,
  1.0,
  0.0,
);

final clampedSimulation = ClampedSimulation(
  spring,
  xMin: 0.0,
  xMax: 1.0,
  dxMin: -1.0,
  dxMax: 1.0,
);

_controller.animateWith(clampedSimulation);
```

## Custom Simulations

Create custom physics by extending `Simulation`:

```dart
class CustomBouncySimulation extends Simulation {
  final double start;
  final double end;
  final double velocity;

  CustomBouncySimulation({
    required this.start,
    required this.end,
    required this.velocity,
  });

  @override
  double x(double time) {
    // Calculate position at given time
    final progress = time / 2.0; // 2 second duration
    final eased = Curves.bounceOut.transform(progress);
    return start + (end - start) * eased;
  }

  @override
  double dx(double time) {
    // Calculate velocity at given time
    // Derivative of x(time)
    return velocity * (1.0 - time / 2.0);
  }

  @override
  bool isDone(double time) {
    return time > 2.0;
  }
}

// Usage:
final simulation = CustomBouncySimulation(
  start: 0.0,
  end: 1.0,
  velocity: 0.0,
);
_controller.animateWith(simulation);
```

## Combining Physics with Gestures

### Pull-to-Refresh Spring

```dart
class PullToRefreshSpring extends StatefulWidget {
  final Widget child;

  const PullToRefreshSpring({super.key, required this.child});

  @override
  State<PullToRefreshSpring> createState() => _PullToRefreshSpringState();
}

class _PullToRefreshSpringState extends State<PullToRefreshSpring>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  double _dragExtent = 0.0;
  final double _maxDragExtent = 100.0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);
    _controller.addListener(() {
      setState(() {
        _dragExtent = _controller.value;
      });
    });
  }

  void _handleDragUpdate(DragUpdateDetails details) {
    setState(() {
      _dragExtent += details.delta.dy;
      _dragExtent = _dragExtent.clamp(0.0, _maxDragExtent);
    });
  }

  void _handleDragEnd(DragEndDetails details) {
    if (_dragExtent >= _maxDragExtent) {
      // Trigger refresh
      _triggerRefresh();
    } else {
      _snapBack(details.velocity.pixelsPerSecond.dy);
    }
  }

  void _snapBack(double velocity) {
    final spring = SpringDescription.withDampingRatio(
      mass: 1.0,
      stiffness: 500.0,
      ratio: 1.0,
    );

    final simulation = SpringSimulation(
      spring,
      _dragExtent,
      0.0,
      velocity / 1000,
    );

    _controller.animateWith(simulation);
  }

  void _triggerRefresh() async {
    // Simulate refresh
    await Future.delayed(Duration(seconds: 2));
    _snapBack(0.0);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onVerticalDragUpdate: _handleDragUpdate,
      onVerticalDragEnd: _handleDragEnd,
      child: Stack(
        children: [
          if (_dragExtent > 0)
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: Container(
                height: _dragExtent,
                color: Colors.blue.withOpacity(0.5),
                child: Center(
                  child: _dragExtent >= _maxDragExtent
                      ? Icon(Icons.refresh)
                      : SizedBox(),
                ),
              ),
            ),
          Transform.translate(
            offset: Offset(0, _dragExtent),
            child: widget.child,
          ),
        ],
      ),
    );
  }
}
```

## Scrollable Physics

Flutter's scrolling uses physics simulations under the hood. You can customize scroll physics:

### Custom Scroll Physics

```dart
class CustomScrollPhysics extends ScrollPhysics {
  const CustomScrollPhysics({ScrollPhysics? parent}) : super(parent: parent);

  @override
  CustomScrollPhysics applyTo(ScrollPhysics? ancestor) {
    return CustomScrollPhysics(parent: buildParent(ancestor));
  }

  @override
  Simulation? createBallisticSimulation(
    ScrollMetrics position,
    double velocity,
  ) {
    if (velocity.abs() < 100.0) {
      return null;
    }

    return ScrollSpringSimulation(
      SpringDescription.withDampingRatio(
        mass: 0.5,
        stiffness: 100.0,
        ratio: 1.1, // Slightly overdamped
      ),
      position.pixels,
      position.pixels + velocity * 0.5, // Shorter fling distance
      velocity,
    );
  }
}

// Usage:
ListView(
  physics: CustomScrollPhysics(),
  children: [
    // List items
  ],
)
```

## Performance Considerations

### Limiting Simulation Complexity

Complex physics calculations can be expensive. Simplify when possible:

```dart
// Expensive: Calculate every frame
@override
double x(double time) {
  return complexCalculation(time);
}

// Better: Cache intermediate values
final _cache = <double, double>{};

@override
double x(double time) {
  return _cache.putIfAbsent(
    time,
    () => complexCalculation(time),
  );
}
```

### Using Tolerance

Simulations have a `tolerance` parameter that determines when they're considered "done":

```dart
final simulation = SpringSimulation(
  spring,
  0.0,
  1.0,
  0.0,
  tolerance: Tolerance(
    distance: 0.01, // Consider done within 0.01 units of target
    velocity: 0.01, // Consider done when velocity below 0.01
  ),
);
```

## Common Patterns

### Snap to Grid with Spring

```dart
void _snapToNearestGridPoint(Offset position, Offset velocity) {
  final gridSize = 100.0;
  final targetX = (position.dx / gridSize).round() * gridSize;
  final targetY = (position.dy / gridSize).round() * gridSize;

  final spring = SpringDescription.withDampingRatio(
    mass: 1.0,
    stiffness: 200.0,
    ratio: 0.8,
  );

  final xSimulation = SpringSimulation(
    spring,
    position.dx,
    targetX,
    velocity.dx,
  );

  final ySimulation = SpringSimulation(
    spring,
    position.dy,
    targetY,
    velocity.dy,
  );

  // Animate both axes simultaneously
}
```

### Elastic Boundary

```dart
void _handleBoundaryCollision(double position, double velocity) {
  if (position < 0 || position > maxBounds) {
    final spring = SpringDescription(
      mass: 1.0,
      stiffness: 300.0,
      damping: 15.0,
    );

    final target = position < 0 ? 0.0 : maxBounds;

    final simulation = SpringSimulation(
      spring,
      position,
      target,
      velocity,
    );

    _controller.animateWith(simulation);
  }
}
```

## Conclusion

Physics-based animations bring a level of realism and responsiveness to Flutter apps that tween-based animations can't match. By modeling real-world physics through springs, gravity, and friction, you create interactions that feel natural and intuitive. Master `SpringSimulation` for most interactive needs, and explore gravity and friction simulations for specialized effects. The key is tuning the parameters to match your desired feel - experiment with mass, stiffness, and damping until the motion feels right.
