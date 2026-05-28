# Interactive Animations

Interactive animations respond to user gestures in real-time, creating direct manipulation experiences where the UI feels tangible and responsive. Unlike time-based animations that play from start to finish, interactive animations follow the user's touch, incorporating velocity and momentum to feel natural and fluid.

## Core Principles

**Direct Manipulation**: The animated widget should follow the user's finger position directly during the gesture.

**Velocity Preservation**: When the user releases a drag or fling gesture, the animation should continue with the gesture's velocity, not jump to a predetermined speed.

**Interruptibility**: Users should be able to interrupt ongoing animations by touching the widget again, without jarring transitions.

**Physics-Based Settling**: After release, the animation should use physics (typically spring simulation) to settle into the final position naturally.

## Draggable Widget with Spring Return

The foundational pattern for interactive animations:

```dart
import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';

class DraggableBox extends StatefulWidget {
  const DraggableBox({super.key});

  @override
  State<DraggableBox> createState() => _DraggableBoxState();
}

class _DraggableBoxState extends State<DraggableBox>
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

    // Convert pixel velocity to unit velocity
    final unitsPerSecondX = pixelsPerSecond.dx / size.width;
    final unitsPerSecondY = pixelsPerSecond.dy / size.height;
    final unitsPerSecond = Offset(unitsPerSecondX, unitsPerSecondY);
    final unitVelocity = unitsPerSecond.distance;

    const spring = SpringDescription(
      mass: 30,
      stiffness: 1,
      damping: 1,
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
        child: Container(
          width: 100,
          height: 100,
          decoration: BoxDecoration(
            color: Colors.blue,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.2),
                blurRadius: 10,
                offset: Offset(0, 5),
              ),
            ],
          ),
          child: Center(
            child: Icon(Icons.drag_indicator, color: Colors.white),
          ),
        ),
      ),
    );
  }
}
```

### Key Techniques

**Stop on Touch**: `_controller.stop()` in `onPanDown` halts any ongoing spring animation when the user touches the widget.

**Direct Update**: `onPanUpdate` directly modifies `_dragAlignment` based on the delta, making the widget follow the finger.

**Velocity Conversion**: Convert pixels-per-second to normalized units for the spring simulation.

**Spring Settling**: Use `SpringSimulation` to create natural momentum and settling behavior.

## Swipe to Dismiss

Implement dismissible cards that can be swiped away:

```dart
class SwipeToDismiss extends StatefulWidget {
  final Widget child;
  final VoidCallback onDismissed;

  const SwipeToDismiss({
    super.key,
    required this.child,
    required this.onDismissed,
  });

  @override
  State<SwipeToDismiss> createState() => _SwipeToDismissState();
}

class _SwipeToDismissState extends State<SwipeToDismiss>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _animation;
  Offset _dragOffset = Offset.zero;
  final double _dismissThreshold = 0.4;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);

    _controller.addListener(() {
      setState(() {
        _dragOffset = _animation.value;
      });
    });

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        widget.onDismissed();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleDragUpdate(DragUpdateDetails details, Size size) {
    setState(() {
      _dragOffset += Offset(
        details.delta.dx / size.width,
        0,
      );
    });
  }

  void _handleDragEnd(DragEndDetails details, Size size) {
    final velocity = details.velocity.pixelsPerSecond.dx / size.width;

    if (_dragOffset.dx.abs() > _dismissThreshold || velocity.abs() > 1.0) {
      // Dismiss
      _animateDismiss(velocity);
    } else {
      // Return to center
      _animateReturn(velocity);
    }
  }

  void _animateDismiss(double velocity) {
    final target = _dragOffset.dx > 0 ? Offset(2.0, 0.0) : Offset(-2.0, 0.0);

    _animation = _controller.drive(
      Tween<Offset>(
        begin: _dragOffset,
        end: target,
      ),
    );

    final simulation = SpringSimulation(
      SpringDescription(
        mass: 1,
        stiffness: 500,
        damping: 30,
      ),
      0,
      1,
      velocity,
    );

    _controller.animateWith(simulation);
  }

  void _animateReturn(double velocity) {
    _animation = _controller.drive(
      Tween<Offset>(
        begin: _dragOffset,
        end: Offset.zero,
      ),
    );

    final simulation = SpringSimulation(
      SpringDescription(
        mass: 1,
        stiffness: 500,
        damping: 25,
      ),
      0,
      1,
      -velocity,
    );

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return GestureDetector(
      onHorizontalDragUpdate: (details) => _handleDragUpdate(details, size),
      onHorizontalDragEnd: (details) => _handleDragEnd(details, size),
      child: Transform.translate(
        offset: Offset(_dragOffset.dx * size.width, 0),
        child: Opacity(
          opacity: 1.0 - _dragOffset.dx.abs().clamp(0.0, 1.0),
          child: widget.child,
        ),
      ),
    );
  }
}

// Usage:
SwipeToDismiss(
  onDismissed: () {
    print('Card dismissed');
  },
  child: Card(
    child: ListTile(
      title: Text('Swipe me'),
      subtitle: Text('Swipe left or right to dismiss'),
    ),
  ),
)
```

## Pull to Refresh

Implement a custom pull-to-refresh interaction:

```dart
class PullToRefresh extends StatefulWidget {
  final Widget child;
  final Future<void> Function() onRefresh;

  const PullToRefresh({
    super.key,
    required this.child,
    required this.onRefresh,
  });

  @override
  State<PullToRefresh> createState() => _PullToRefreshState();
}

class _PullToRefreshState extends State<PullToRefresh>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  double _dragExtent = 0.0;
  bool _isRefreshing = false;

  static const double _refreshTriggerDistance = 100.0;
  static const double _maxDragDistance = 150.0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);

    _controller.addListener(() {
      if (!_isRefreshing) {
        setState(() {
          _dragExtent = _controller.value * _maxDragDistance;
        });
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleDragUpdate(DragUpdateDetails details) {
    if (!_isRefreshing) {
      setState(() {
        _dragExtent = (_dragExtent + details.delta.dy)
            .clamp(0.0, _maxDragDistance);
      });
    }
  }

  void _handleDragEnd(DragEndDetails details) {
    if (_isRefreshing) return;

    if (_dragExtent >= _refreshTriggerDistance) {
      _triggerRefresh();
    } else {
      _snapBack(details.velocity.pixelsPerSecond.dy);
    }
  }

  void _triggerRefresh() async {
    setState(() {
      _isRefreshing = true;
      _dragExtent = _refreshTriggerDistance;
    });

    await widget.onRefresh();

    setState(() {
      _isRefreshing = false;
    });

    _snapBack(0);
  }

  void _snapBack(double velocity) {
    final spring = SpringDescription.withDampingRatio(
      mass: 1.0,
      stiffness: 500.0,
      ratio: 1.0,
    );

    final simulation = SpringSimulation(
      spring,
      _dragExtent / _maxDragDistance,
      0.0,
      -velocity / 1000,
    );

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onVerticalDragUpdate: _handleDragUpdate,
      onVerticalDragEnd: _handleDragEnd,
      child: Stack(
        children: [
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: _buildRefreshIndicator(),
          ),
          Transform.translate(
            offset: Offset(0, _dragExtent),
            child: widget.child,
          ),
        ],
      ),
    );
  }

  Widget _buildRefreshIndicator() {
    final progress = (_dragExtent / _refreshTriggerDistance).clamp(0.0, 1.0);

    return Container(
      height: _dragExtent,
      alignment: Alignment.center,
      child: _isRefreshing
          ? SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Transform.rotate(
              angle: progress * 6.28, // Full rotation
              child: Icon(
                Icons.refresh,
                size: 24 * progress,
                color: Colors.blue.withOpacity(progress),
              ),
            ),
    );
  }
}

// Usage:
PullToRefresh(
  onRefresh: () async {
    await Future.delayed(Duration(seconds: 2));
    print('Refreshed!');
  },
  child: ListView.builder(
    itemCount: 20,
    itemBuilder: (context, index) {
      return ListTile(title: Text('Item $index'));
    },
  ),
)
```

## Rotatable Dial

Create a dial that users can rotate with gestures:

```dart
class RotatableDial extends StatefulWidget {
  final Function(double)? onRotationChanged;

  const RotatableDial({super.key, this.onRotationChanged});

  @override
  State<RotatableDial> createState() => _RotatableDialState();
}

class _RotatableDialState extends State<RotatableDial>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  double _rotation = 0.0;
  double _lastRotation = 0.0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 300),
    );

    _controller.addListener(() {
      setState(() {
        _rotation = _controller.value;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handlePanUpdate(DragUpdateDetails details, Offset center) {
    final touchPosition = details.localPosition - center;
    final angle = touchPosition.direction;

    setState(() {
      _rotation = angle;
      widget.onRotationChanged?.call(_rotation);
    });
  }

  void _handlePanEnd(DragEndDetails details, Size size) {
    // Snap to nearest increment (e.g., 30 degrees)
    const snapIncrement = 0.5236; // 30 degrees in radians
    final snappedRotation = (_rotation / snapIncrement).round() * snapIncrement;

    _controller.value = _rotation;

    final spring = SpringDescription.withDampingRatio(
      mass: 1.0,
      stiffness: 300.0,
      ratio: 0.8,
    );

    final simulation = SpringSimulation(
      spring,
      _rotation,
      snappedRotation,
      0,
    );

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final size = Size(
          constraints.maxWidth,
          constraints.maxHeight,
        );
        final center = Offset(size.width / 2, size.height / 2);

        return GestureDetector(
          onPanUpdate: (details) => _handlePanUpdate(details, center),
          onPanEnd: (details) => _handlePanEnd(details, size),
          child: Transform.rotate(
            angle: _rotation,
            child: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: RadialGradient(
                  colors: [Colors.blue[300]!, Colors.blue[700]!],
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 15,
                    offset: Offset(0, 5),
                  ),
                ],
              ),
              child: CustomPaint(
                painter: DialPainter(),
              ),
            ),
          ),
        );
      },
    );
  }
}

class DialPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    // Draw tick marks
    for (int i = 0; i < 12; i++) {
      final angle = (i * 30) * (3.14159 / 180);
      final startX = center.dx + (radius - 20) * cos(angle);
      final startY = center.dy + (radius - 20) * sin(angle);
      final endX = center.dx + (radius - 10) * cos(angle);
      final endY = center.dy + (radius - 10) * sin(angle);

      canvas.drawLine(
        Offset(startX, startY),
        Offset(endX, endY),
        Paint()
          ..color = Colors.white
          ..strokeWidth = 2,
      );
    }

    // Draw pointer
    canvas.drawLine(
      center,
      Offset(center.dx, center.dy - radius + 30),
      Paint()
        ..color = Colors.red
        ..strokeWidth = 4
        ..strokeCap = StrokeCap.round,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

## Slider with Haptic Feedback

Interactive slider with physics and haptic feedback:

```dart
import 'package:flutter/services.dart';

class PhysicsSlider extends StatefulWidget {
  final double min;
  final double max;
  final Function(double)? onChanged;

  const PhysicsSlider({
    super.key,
    this.min = 0.0,
    this.max = 1.0,
    this.onChanged,
  });

  @override
  State<PhysicsSlider> createState() => _PhysicsSliderState();
}

class _PhysicsSliderState extends State<PhysicsSlider>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  double _value = 0.5;
  double _lastSnapValue = 0.5;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);

    _controller.addListener(() {
      setState(() {
        _value = _controller.value;
        widget.onChanged?.call(_value);
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleDragUpdate(DragUpdateDetails details, double width) {
    final delta = details.delta.dx / width;
    final newValue = (_value + delta).clamp(widget.min, widget.max);

    // Trigger haptic feedback on snap points
    final snapPoint = (newValue * 10).round() / 10;
    if (snapPoint != _lastSnapValue) {
      HapticFeedback.selectionClick();
      _lastSnapValue = snapPoint;
    }

    setState(() {
      _value = newValue;
      widget.onChanged?.call(_value);
    });
  }

  void _handleDragEnd(DragEndDetails details, double width) {
    final velocity = details.velocity.pixelsPerSecond.dx / width;

    // Snap to nearest 0.1
    final snappedValue = (_value * 10).round() / 10;

    _controller.value = _value;

    final spring = SpringDescription.withDampingRatio(
      mass: 1.0,
      stiffness: 400.0,
      ratio: 0.9,
    );

    final simulation = SpringSimulation(
      spring,
      _value,
      snappedValue,
      velocity,
    );

    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;

        return GestureDetector(
          onHorizontalDragUpdate: (details) => _handleDragUpdate(details, width),
          onHorizontalDragEnd: (details) => _handleDragEnd(details, width),
          child: Container(
            height: 60,
            child: Stack(
              children: [
                // Track
                Positioned(
                  left: 0,
                  right: 0,
                  top: 28,
                  child: Container(
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                // Progress
                Positioned(
                  left: 0,
                  top: 28,
                  child: Container(
                    width: _value * width,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                // Thumb
                Positioned(
                  left: (_value * width) - 20,
                  top: 20,
                  child: Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.blue,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.2),
                          blurRadius: 8,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Center(
                      child: Text(
                        _value.toStringAsFixed(1),
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

## Best Practices

### 1. Always Stop Ongoing Animations

When the user touches the widget, stop any running animations:

```dart
onPanDown: (details) {
  _controller.stop();
}
```

### 2. Convert Velocities Correctly

Transform pixel velocities to normalized coordinates:

```dart
final unitVelocity = pixelsPerSecond.dx / size.width;
```

### 3. Use Appropriate Spring Parameters

- **Snappy**: High stiffness (500+), moderate damping
- **Bouncy**: Low damping (<10)
- **Smooth**: Critical damping ratio (1.0)

### 4. Clamp Values

Prevent values from exceeding bounds:

```dart
_value = (_value + delta).clamp(min, max);
```

### 5. Provide Visual Feedback

Show the user how the interaction affects the UI:
- Shadows that respond to drag distance
- Opacity changes
- Scale transformations
- Rotation based on drag direction

### 6. Test on Real Devices

Physics simulations feel different on real devices vs simulators. Always test interactive animations on physical hardware.

## Common Patterns

### Threshold-Based Actions

```dart
if (_dragDistance.abs() > _threshold) {
  _triggerAction();
} else {
  _returnToStart();
}
```

### Momentum Preservation

```dart
final simulation = SpringSimulation(
  spring,
  currentPosition,
  targetPosition,
  gestureVelocity, // Preserve user's velocity
);
```

### Snap Points

```dart
final snappedValue = (currentValue / snapIncrement).round() * snapIncrement;
```

## Conclusion

Interactive animations transform static UIs into responsive, tangible experiences. By combining gesture detection with physics simulations, you create interfaces that feel direct and natural. The key is preserving velocity, stopping animations when users touch the screen, and using appropriate spring parameters to create the right feel for your interaction.
