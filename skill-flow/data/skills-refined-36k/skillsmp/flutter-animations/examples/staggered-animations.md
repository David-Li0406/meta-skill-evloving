# Staggered Animations

Staggered animations create choreographed sequences where multiple properties animate in a coordinated way. Instead of all changes happening simultaneously, staggered animations orchestrate when each animation starts and ends, creating sophisticated visual effects with a single `AnimationController`.

## Core Concept

Staggered animations use **intervals** to control the timing of each individual animation within a single controller's 0.0 to 1.0 timeline. Each property gets its own `Tween` and `Interval`, allowing precise control over when and how it animates.

### Key Principle

**One controller, multiple animations, coordinated timing.**

```dart
// Controller goes from 0.0 to 1.0
AnimationController(duration: Duration(seconds: 2));

// Opacity animates from 0.0 to 0.1 (0% to 10% of timeline)
Animation<double> opacity = Tween<double>(begin: 0.0, end: 1.0).animate(
  CurvedAnimation(
    parent: controller,
    curve: Interval(0.0, 0.1, curve: Curves.ease),
  ),
);

// Width animates from 0.125 to 0.25 (12.5% to 25% of timeline)
Animation<double> width = Tween<double>(begin: 50, end: 150).animate(
  CurvedAnimation(
    parent: controller,
    curve: Interval(0.125, 0.25, curve: Curves.ease),
  ),
);
```

## Basic Staggered Animation

### Example: Expanding and Transforming Card

```dart
import 'package:flutter/material.dart';

class StaggeredAnimation extends StatelessWidget {
  StaggeredAnimation({super.key, required this.controller})
      : opacity = Tween<double>(
          begin: 0.0,
          end: 1.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.0, 0.1, curve: Curves.ease),
          ),
        ),
        width = Tween<double>(
          begin: 50.0,
          end: 150.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.125, 0.25, curve: Curves.ease),
          ),
        ),
        height = Tween<double>(
          begin: 50.0,
          end: 150.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.25, 0.375, curve: Curves.ease),
          ),
        ),
        padding = EdgeInsetsTween(
          begin: EdgeInsets.only(bottom: 16),
          end: EdgeInsets.only(bottom: 75),
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.25, 0.375, curve: Curves.ease),
          ),
        ),
        borderRadius = BorderRadiusTween(
          begin: BorderRadius.circular(4),
          end: BorderRadius.circular(75),
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.375, 0.5, curve: Curves.ease),
          ),
        ),
        color = ColorTween(
          begin: Colors.indigo[100],
          end: Colors.orange[400],
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.5, 0.75, curve: Curves.ease),
          ),
        );

  final AnimationController controller;
  final Animation<double> opacity;
  final Animation<double> width;
  final Animation<double> height;
  final Animation<EdgeInsets> padding;
  final Animation<BorderRadius?> borderRadius;
  final Animation<Color?> color;

  Widget _buildAnimation(BuildContext context, Widget? child) {
    return Container(
      padding: padding.value,
      alignment: Alignment.bottomCenter,
      child: Opacity(
        opacity: opacity.value,
        child: Container(
          width: width.value,
          height: height.value,
          decoration: BoxDecoration(
            color: color.value,
            border: Border.all(
              color: Colors.indigo[300]!,
              width: 3,
            ),
            borderRadius: borderRadius.value,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      builder: _buildAnimation,
      animation: controller,
    );
  }
}

// Usage in a StatefulWidget:
class StaggerDemo extends StatefulWidget {
  @override
  State<StaggerDemo> createState() => _StaggerDemoState();
}

class _StaggerDemoState extends State<StaggerDemo>
    with TickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _playAnimation() async {
    try {
      await _controller.forward().orCancel;
      await _controller.reverse().orCancel;
    } on TickerCanceled {
      // Animation was canceled
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: _playAnimation,
        child: Center(
          child: Container(
            width: 300,
            height: 300,
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.1),
              border: Border.all(
                color: Colors.black.withOpacity(0.5),
              ),
            ),
            child: StaggeredAnimation(controller: _controller),
          ),
        ),
      ),
    );
  }
}
```

### Animation Timeline

This example creates the following sequence:

1. **0.0 - 0.1** (0% - 10%): Fade in (opacity 0 → 1)
2. **0.125 - 0.25** (12.5% - 25%): Expand width (50 → 150)
3. **0.25 - 0.375** (25% - 37.5%): Expand height (50 → 150) and adjust padding
4. **0.375 - 0.5** (37.5% - 50%): Round corners (radius 4 → 75)
5. **0.5 - 0.75** (50% - 75%): Change color (indigo → orange)

## List Item Staggered Entrance

Animate list items appearing one after another:

```dart
class StaggeredListAnimation extends StatefulWidget {
  @override
  State<StaggeredListAnimation> createState() => _StaggeredListAnimationState();
}

class _StaggeredListAnimationState extends State<StaggeredListAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<String> _items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    );
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: _items.length,
      itemBuilder: (context, index) {
        final interval = index / _items.length;
        final nextInterval = (index + 1) / _items.length;

        return StaggeredListItem(
          controller: _controller,
          interval: Interval(interval, nextInterval, curve: Curves.easeOut),
          child: ListTile(
            leading: Icon(Icons.star),
            title: Text(_items[index]),
          ),
        );
      },
    );
  }
}

class StaggeredListItem extends StatelessWidget {
  const StaggeredListItem({
    super.key,
    required this.controller,
    required this.interval,
    required this.child,
  });

  final AnimationController controller;
  final Interval interval;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    final slideAnimation = Tween<Offset>(
      begin: Offset(1.0, 0.0),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(
        parent: controller,
        curve: interval,
      ),
    );

    final fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(
      CurvedAnimation(
        parent: controller,
        curve: interval,
      ),
    );

    return SlideTransition(
      position: slideAnimation,
      child: FadeTransition(
        opacity: fadeAnimation,
        child: child,
      ),
    );
  }
}
```

## Complex Choreography: Card Flip

Combine rotation, scale, and opacity for a card flip effect:

```dart
class FlipCardAnimation extends StatelessWidget {
  FlipCardAnimation({super.key, required this.controller})
      : scaleDown = Tween<double>(
          begin: 1.0,
          end: 0.9,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.0, 0.25, curve: Curves.easeOut),
          ),
        ),
        rotateOut = Tween<double>(
          begin: 0.0,
          end: 1.57, // 90 degrees in radians
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.25, 0.5, curve: Curves.easeInOut),
          ),
        ),
        rotateIn = Tween<double>(
          begin: -1.57,
          end: 0.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.5, 0.75, curve: Curves.easeInOut),
          ),
        ),
        scaleUp = Tween<double>(
          begin: 0.9,
          end: 1.0,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.75, 1.0, curve: Curves.easeIn),
          ),
        );

  final AnimationController controller;
  final Animation<double> scaleDown;
  final Animation<double> rotateOut;
  final Animation<double> rotateIn;
  final Animation<double> scaleUp;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        final showFront = controller.value < 0.5;
        final scale = controller.value < 0.25
            ? scaleDown.value
            : (controller.value > 0.75 ? scaleUp.value : 0.9);
        final rotation = showFront ? rotateOut.value : rotateIn.value;

        return Transform.scale(
          scale: scale,
          child: Transform(
            alignment: Alignment.center,
            transform: Matrix4.rotationY(rotation),
            child: Container(
              width: 200,
              height: 300,
              decoration: BoxDecoration(
                color: showFront ? Colors.blue : Colors.red,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Center(
                child: Text(
                  showFront ? 'FRONT' : 'BACK',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
```

## Overlapping Animations

Create smooth flow by overlapping intervals:

```dart
class OverlappingStagger extends StatelessWidget {
  OverlappingStagger({super.key, required this.controller})
      : slide1 = Tween<Offset>(
          begin: Offset(-1.0, 0.0),
          end: Offset.zero,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.0, 0.5, curve: Curves.easeOut),
          ),
        ),
        slide2 = Tween<Offset>(
          begin: Offset(-1.0, 0.0),
          end: Offset.zero,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.25, 0.75, curve: Curves.easeOut),
          ),
        ),
        slide3 = Tween<Offset>(
          begin: Offset(-1.0, 0.0),
          end: Offset.zero,
        ).animate(
          CurvedAnimation(
            parent: controller,
            curve: Interval(0.5, 1.0, curve: Curves.easeOut),
          ),
        );

  final AnimationController controller;
  final Animation<Offset> slide1;
  final Animation<Offset> slide2;
  final Animation<Offset> slide3;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        return Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SlideTransition(
              position: slide1,
              child: Container(
                width: 200,
                height: 50,
                color: Colors.red,
                child: Center(child: Text('First')),
              ),
            ),
            SizedBox(height: 10),
            SlideTransition(
              position: slide2,
              child: Container(
                width: 200,
                height: 50,
                color: Colors.green,
                child: Center(child: Text('Second')),
              ),
            ),
            SizedBox(height: 10),
            SlideTransition(
              position: slide3,
              child: Container(
                width: 200,
                height: 50,
                color: Colors.blue,
                child: Center(child: Text('Third')),
              ),
            ),
          ],
        );
      },
    );
  }
}
```

## Timing Patterns

### Sequential (No Overlap)

```dart
// Animation 1: 0.0 - 0.33
// Animation 2: 0.33 - 0.66
// Animation 3: 0.66 - 1.0
```

### Cascading (Overlapping Start)

```dart
// Animation 1: 0.0 - 0.5
// Animation 2: 0.25 - 0.75  // Starts before 1 finishes
// Animation 3: 0.5 - 1.0    // Starts before 2 finishes
```

### Synchronized (Same Timing, Different Properties)

```dart
// All animations: 0.0 - 1.0
// Different tweens applied to different properties
```

### Wave Effect

```dart
// Progressive delay with same duration
// Animation 1: 0.0 - 0.4
// Animation 2: 0.2 - 0.6
// Animation 3: 0.4 - 0.8
// Animation 4: 0.6 - 1.0
```

## Best Practices

### 1. Use Static Tweens

Define tweens as final properties, not in build methods:

```dart
// GOOD
class MyAnimation extends StatelessWidget {
  MyAnimation({required this.controller})
      : opacity = Tween<double>(begin: 0.0, end: 1.0)
          .animate(CurvedAnimation(parent: controller, curve: Interval(0.0, 0.5)));

  final AnimationController controller;
  final Animation<double> opacity;
}

// BAD
@override
Widget build(BuildContext context) {
  final opacity = Tween<double>(begin: 0.0, end: 1.0)
    .animate(controller); // Created every build!
}
```

### 2. Plan Your Timeline

Sketch out the timing before coding:

```
0.0   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
[Fade In ]
      [Width    ]
            [Height   ]
                  [Border       ]
                        [Color          ]
```

### 3. Keep Intervals Within 0.0-1.0

All interval values must be between 0.0 and 1.0:

```dart
// CORRECT
Interval(0.25, 0.75)

// WRONG
Interval(0.25, 1.5) // End > 1.0!
```

### 4. Use Meaningful Curves

Choose curves that match the animation's purpose:

```dart
// Sharp entrance
Interval(0.0, 0.3, curve: Curves.easeOut)

// Gentle fade
Interval(0.7, 1.0, curve: Curves.easeIn)

// Bouncy effect
Interval(0.5, 0.8, curve: Curves.elasticOut)
```

### 5. Consider Reverse Animations

Test that your staggered animation looks good in both directions:

```dart
await controller.forward().orCancel;
await controller.reverse().orCancel;
```

## Common Pitfalls

### 1. Overlapping Intervals for Same Property

Don't animate the same property with overlapping intervals - the results are unpredictable.

### 2. Forgetting to Dispose

Always dispose the controller:

```dart
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

### 3. Creating Animations in Build

Create animations in the constructor or initState, not in build.

### 4. Too Many Staggered Effects

Don't overdo it - too many staggered animations can feel slow and annoying.

## Conclusion

Staggered animations create sophisticated, choreographed effects with a single animation controller. By carefully timing intervals and choosing appropriate curves, you can build everything from simple list entrance animations to complex multi-property transformations. The key is planning your timeline, using static animation objects, and testing the animation in both forward and reverse to ensure smooth, polished results.
