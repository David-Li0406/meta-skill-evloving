# Implicit Animations in Flutter

Implicit animations are the easiest and most efficient way to add animation to Flutter applications. They automatically handle animation controllers, tweens, and state management, allowing you to create smooth transitions by simply changing widget properties.

## What Are Implicit Animations?

Implicit animations are widgets that automatically animate property changes over a specified duration. When you rebuild the widget with new parameter values, the implicit animated widget smoothly transitions from the old values to the new ones.

All implicit animations derive from the `ImplicitlyAnimatedWidget` class and share common characteristics:
- Automatic animation controller management
- Built-in disposal to prevent memory leaks
- Configurable duration and curve
- No need for explicit `setState()` calls in listeners

## Core Concept

The fundamental pattern for using implicit animations:

```dart
class _MyWidgetState extends State<MyWidget> {
  double _size = 100.0;
  Color _color = Colors.blue;

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      width: _size,
      height: _size,
      color: _color,
      curve: Curves.easeInOut,
    );
  }

  void _changeProperties() {
    setState(() {
      _size = 200.0;
      _color = Colors.red;
    });
  }
}
```

When you call `setState()` with new values, `AnimatedContainer` automatically animates from the old values to the new ones over the specified duration.

## AnimatedContainer

`AnimatedContainer` is the most versatile implicit animation widget, capable of animating almost any container property.

### Animatable Properties

- **Size**: `width`, `height`, `constraints`
- **Spacing**: `margin`, `padding`
- **Decoration**: `color`, `borderRadius`, `border`, `boxShadow`, `gradient`
- **Layout**: `alignment`, `transform`
- **Other**: `foregroundDecoration`, `clipBehavior`

### Basic Example

```dart
class ColorSizeAnimation extends StatefulWidget {
  @override
  State<ColorSizeAnimation> createState() => _ColorSizeAnimationState();
}

class _ColorSizeAnimationState extends State<ColorSizeAnimation> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _expanded = !_expanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.fastOutSlowIn,
        width: _expanded ? 200.0 : 100.0,
        height: _expanded ? 200.0 : 100.0,
        decoration: BoxDecoration(
          color: _expanded ? Colors.blue : Colors.red,
          borderRadius: BorderRadius.circular(_expanded ? 50.0 : 8.0),
        ),
        child: Center(
          child: Text(
            'Tap me',
            style: TextStyle(
              color: Colors.white,
              fontSize: _expanded ? 20.0 : 14.0,
            ),
          ),
        ),
      ),
    );
  }
}
```

### Advanced Example: Random Properties

```dart
import 'dart:math';

class RandomBoxAnimation extends StatefulWidget {
  @override
  State<RandomBoxAnimation> createState() => _RandomBoxAnimationState();
}

class _RandomBoxAnimationState extends State<RandomBoxAnimation> {
  double _width = 50;
  double _height = 50;
  Color _color = Colors.green;
  BorderRadiusGeometry _borderRadius = BorderRadius.circular(8);

  void _randomize() {
    setState(() {
      final random = Random();
      _width = random.nextInt(300).toDouble();
      _height = random.nextInt(300).toDouble();
      _color = Color.fromRGBO(
        random.nextInt(256),
        random.nextInt(256),
        random.nextInt(256),
        1,
      );
      _borderRadius = BorderRadius.circular(
        random.nextInt(100).toDouble(),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        AnimatedContainer(
          width: _width,
          height: _height,
          decoration: BoxDecoration(
            color: _color,
            borderRadius: _borderRadius,
          ),
          duration: const Duration(seconds: 1),
          curve: Curves.fastOutSlowIn,
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: _randomize,
          child: Text('Randomize'),
        ),
      ],
    );
  }
}
```

### Complex Decoration Animation

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 400),
  decoration: BoxDecoration(
    gradient: LinearGradient(
      colors: _isActive
          ? [Colors.purple, Colors.blue]
          : [Colors.orange, Colors.red],
    ),
    boxShadow: [
      BoxShadow(
        color: _isActive ? Colors.blue.withOpacity(0.5) : Colors.grey,
        blurRadius: _isActive ? 20.0 : 5.0,
        offset: Offset(0, _isActive ? 10 : 2),
      ),
    ],
    border: Border.all(
      color: _isActive ? Colors.white : Colors.black,
      width: _isActive ? 4.0 : 2.0,
    ),
  ),
)
```

## AnimatedOpacity

Animates the opacity of a widget, providing smooth fade in/out effects.

### Basic Usage

```dart
class FadeAnimation extends StatefulWidget {
  @override
  State<FadeAnimation> createState() => _FadeAnimationState();
}

class _FadeAnimationState extends State<FadeAnimation> {
  bool _visible = true;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        AnimatedOpacity(
          opacity: _visible ? 1.0 : 0.0,
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOut,
          child: Container(
            width: 200,
            height: 200,
            color: Colors.blue,
            child: Center(child: Text('Fade Me')),
          ),
        ),
        ElevatedButton(
          onPressed: () => setState(() => _visible = !_visible),
          child: Text(_visible ? 'Fade Out' : 'Fade In'),
        ),
      ],
    );
  }
}
```

### Performance Note

`AnimatedOpacity` is optimized for performance compared to wrapping widgets in the `Opacity` widget. It uses the same internal mechanisms but avoids unnecessary rebuilds.

### Conditional Rendering Pattern

```dart
AnimatedOpacity(
  opacity: _isLoading ? 0.0 : 1.0,
  duration: const Duration(milliseconds: 300),
  child: _isLoading
      ? SizedBox.shrink()
      : ContentWidget(),
)
```

However, for showing/hiding widgets, consider `AnimatedSwitcher` which can cross-fade between completely different widgets.

## AnimatedAlign

Animates the alignment of a child within its parent.

### Usage

```dart
class AlignAnimation extends StatefulWidget {
  @override
  State<AlignAnimation> createState() => _AlignAnimationState();
}

class _AlignAnimationState extends State<AlignAnimation> {
  Alignment _alignment = Alignment.topLeft;

  void _changeAlignment() {
    setState(() {
      _alignment = _alignment == Alignment.topLeft
          ? Alignment.bottomRight
          : Alignment.topLeft;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _changeAlignment,
      child: Container(
        color: Colors.grey[200],
        width: 300,
        height: 300,
        child: AnimatedAlign(
          alignment: _alignment,
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOut,
          child: Container(
            width: 50,
            height: 50,
            color: Colors.blue,
          ),
        ),
      ),
    );
  }
}
```

### Cycle Through Alignments

```dart
final alignments = [
  Alignment.topLeft,
  Alignment.topCenter,
  Alignment.topRight,
  Alignment.centerRight,
  Alignment.bottomRight,
  Alignment.bottomCenter,
  Alignment.bottomLeft,
  Alignment.centerLeft,
];

int _currentIndex = 0;

void _nextAlignment() {
  setState(() {
    _currentIndex = (_currentIndex + 1) % alignments.length;
  });
}

// In build:
AnimatedAlign(
  alignment: alignments[_currentIndex],
  duration: const Duration(milliseconds: 400),
  child: Icon(Icons.star, size: 50, color: Colors.amber),
)
```

## AnimatedPadding

Animates changes to padding values.

### Usage

```dart
class PaddingAnimation extends StatefulWidget {
  @override
  State<PaddingAnimation> createState() => _PaddingAnimationState();
}

class _PaddingAnimationState extends State<PaddingAnimation> {
  double _padding = 8.0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          color: Colors.grey[300],
          child: AnimatedPadding(
            padding: EdgeInsets.all(_padding),
            duration: const Duration(milliseconds: 400),
            curve: Curves.easeInOut,
            child: Container(
              color: Colors.blue,
              child: Center(child: Text('Content')),
            ),
          ),
        ),
        Slider(
          value: _padding,
          min: 0,
          max: 100,
          onChanged: (value) => setState(() => _padding = value),
        ),
      ],
    );
  }
}
```

### Directional Padding

```dart
AnimatedPadding(
  padding: EdgeInsets.only(
    left: _expanded ? 50.0 : 10.0,
    top: _expanded ? 30.0 : 10.0,
    right: _expanded ? 50.0 : 10.0,
    bottom: _expanded ? 30.0 : 10.0,
  ),
  duration: const Duration(milliseconds: 300),
  child: YourWidget(),
)
```

## AnimatedPositioned

Animates position changes within a `Stack`. Only works as a direct child of `Stack`.

### Usage

```dart
class PositionedAnimation extends StatefulWidget {
  @override
  State<PositionedAnimation> createState() => _PositionedAnimationState();
}

class _PositionedAnimationState extends State<PositionedAnimation> {
  bool _moved = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _moved = !_moved),
      child: Container(
        color: Colors.grey[200],
        width: 300,
        height: 300,
        child: Stack(
          children: [
            AnimatedPositioned(
              left: _moved ? 200.0 : 50.0,
              top: _moved ? 200.0 : 50.0,
              duration: const Duration(milliseconds: 500),
              curve: Curves.easeInOut,
              child: Container(
                width: 50,
                height: 50,
                color: Colors.blue,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Animating Size and Position

```dart
AnimatedPositioned(
  left: _expanded ? 0 : 100,
  top: _expanded ? 0 : 100,
  right: _expanded ? 0 : 100,
  bottom: _expanded ? 0 : 100,
  duration: const Duration(milliseconds: 400),
  curve: Curves.fastOutSlowIn,
  child: Container(color: Colors.blue),
)
```

## AnimatedSwitcher

Cross-fades between different widgets when the child changes.

### Basic Usage

```dart
class SwitcherAnimation extends StatefulWidget {
  @override
  State<SwitcherAnimation> createState() => _SwitcherAnimationState();
}

class _SwitcherAnimationState extends State<SwitcherAnimation> {
  bool _showFirst = true;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 300),
          child: _showFirst
              ? Container(
                  key: ValueKey('first'),
                  width: 200,
                  height: 200,
                  color: Colors.blue,
                  child: Center(child: Text('First')),
                )
              : Container(
                  key: ValueKey('second'),
                  width: 200,
                  height: 200,
                  color: Colors.red,
                  child: Center(child: Text('Second')),
                ),
        ),
        ElevatedButton(
          onPressed: () => setState(() => _showFirst = !_showFirst),
          child: Text('Switch'),
        ),
      ],
    );
  }
}
```

### Important: Keys Are Required

`AnimatedSwitcher` uses the child's key to determine when to animate. Without different keys, it won't detect the change:

```dart
// WRONG - Won't animate without keys
AnimatedSwitcher(
  duration: Duration(milliseconds: 300),
  child: _showFirst ? WidgetA() : WidgetB(),
)

// CORRECT - Uses keys to detect changes
AnimatedSwitcher(
  duration: Duration(milliseconds: 300),
  child: _showFirst
      ? WidgetA(key: ValueKey('A'))
      : WidgetB(key: ValueKey('B')),
)
```

### Custom Transitions

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 500),
  transitionBuilder: (Widget child, Animation<double> animation) {
    return ScaleTransition(scale: animation, child: child);
  },
  child: _currentWidget,
)
```

### Slide Transition

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 400),
  transitionBuilder: (Widget child, Animation<double> animation) {
    final offsetAnimation = Tween<Offset>(
      begin: Offset(1.0, 0.0),
      end: Offset.zero,
    ).animate(animation);
    return SlideTransition(position: offsetAnimation, child: child);
  },
  child: _currentWidget,
)
```

### Rotation Transition

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 400),
  transitionBuilder: (Widget child, Animation<double> animation) {
    return RotationTransition(
      turns: animation,
      child: child,
    );
  },
  child: _currentWidget,
)
```

## AnimatedCrossFade

Specialized widget for cross-fading between exactly two children.

### Usage

```dart
class CrossFadeAnimation extends StatefulWidget {
  @override
  State<CrossFadeAnimation> createState() => _CrossFadeAnimationState();
}

class _CrossFadeAnimationState extends State<CrossFadeAnimation> {
  bool _showFirst = true;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        AnimatedCrossFade(
          duration: const Duration(milliseconds: 300),
          crossFadeState: _showFirst
              ? CrossFadeState.showFirst
              : CrossFadeState.showSecond,
          firstChild: Container(
            width: 200,
            height: 100,
            color: Colors.blue,
            child: Center(child: Text('First')),
          ),
          secondChild: Container(
            width: 200,
            height: 200,
            color: Colors.red,
            child: Center(child: Text('Second')),
          ),
        ),
        ElevatedButton(
          onPressed: () => setState(() => _showFirst = !_showFirst),
          child: Text('Toggle'),
        ),
      ],
    );
  }
}
```

### Size Transition Curve

`AnimatedCrossFade` automatically animates size changes between children:

```dart
AnimatedCrossFade(
  duration: const Duration(milliseconds: 400),
  sizeCurve: Curves.easeInOut,
  crossFadeState: _state,
  firstChild: SmallWidget(),
  secondChild: LargeWidget(),
)
```

## AnimatedDefaultTextStyle

Animates text style changes.

### Usage

```dart
class TextStyleAnimation extends StatefulWidget {
  @override
  State<TextStyleAnimation> createState() => _TextStyleAnimationState();
}

class _TextStyleAnimationState extends State<TextStyleAnimation> {
  bool _large = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _large = !_large),
      child: AnimatedDefaultTextStyle(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        style: TextStyle(
          fontSize: _large ? 48.0 : 24.0,
          color: _large ? Colors.blue : Colors.black,
          fontWeight: _large ? FontWeight.bold : FontWeight.normal,
        ),
        child: Text('Tap to change'),
      ),
    );
  }
}
```

### Gradual Style Changes

```dart
AnimatedDefaultTextStyle(
  duration: const Duration(milliseconds: 400),
  style: TextStyle(
    fontSize: _sliderValue,
    color: Color.lerp(Colors.black, Colors.red, _sliderValue / 100),
    letterSpacing: _sliderValue / 10,
  ),
  child: Text('Animated Text'),
)
```

## AnimatedPhysicalModel

Animates elevation and color changes with Material shadow effects.

### Usage

```dart
class PhysicalModelAnimation extends StatefulWidget {
  @override
  State<PhysicalModelAnimation> createState() => _PhysicalModelAnimationState();
}

class _PhysicalModelAnimationState extends State<PhysicalModelAnimation> {
  bool _elevated = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _elevated = !_elevated),
      child: AnimatedPhysicalModel(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        elevation: _elevated ? 20.0 : 0.0,
        color: _elevated ? Colors.blue : Colors.white,
        shadowColor: Colors.black,
        shape: BoxShape.rectangle,
        borderRadius: BorderRadius.circular(_elevated ? 20.0 : 8.0),
        child: Container(
          width: 200,
          height: 200,
          child: Center(child: Text('Tap me')),
        ),
      ),
    );
  }
}
```

## TweenAnimationBuilder

The most powerful implicit animation widget - creates custom implicit animations for any property.

### Basic Usage

```dart
class CustomTweenAnimation extends StatefulWidget {
  @override
  State<CustomTweenAnimation> createState() => _CustomTweenAnimationState();
}

class _CustomTweenAnimationState extends State<CustomTweenAnimation> {
  double _targetValue = 0.0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TweenAnimationBuilder<double>(
          tween: Tween<double>(begin: 0, end: _targetValue),
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOut,
          builder: (context, value, child) {
            return Transform.rotate(
              angle: value,
              child: child,
            );
          },
          child: Icon(Icons.star, size: 100, color: Colors.amber),
        ),
        ElevatedButton(
          onPressed: () {
            setState(() {
              _targetValue = _targetValue == 0 ? 3.14159 : 0;
            });
          },
          child: Text('Rotate'),
        ),
      ],
    );
  }
}
```

### Color Animation

```dart
TweenAnimationBuilder<Color?>(
  tween: ColorTween(begin: Colors.red, end: _targetColor),
  duration: const Duration(milliseconds: 400),
  builder: (context, color, child) {
    return Container(
      width: 200,
      height: 200,
      color: color,
    );
  },
)
```

### Multiple Property Animation

```dart
TweenAnimationBuilder<double>(
  tween: Tween<double>(begin: 0, end: _progress),
  duration: const Duration(milliseconds: 600),
  curve: Curves.easeOut,
  builder: (context, value, child) {
    return Column(
      children: [
        LinearProgressIndicator(value: value),
        SizedBox(height: 20),
        Transform.scale(
          scale: value,
          child: child,
        ),
        Text('${(value * 100).toInt()}%'),
      ],
    );
  },
  child: Icon(Icons.download, size: 50),
)
```

### Custom Object Animation

```dart
class Point {
  final double x;
  final double y;
  Point(this.x, this.y);
}

class PointTween extends Tween<Point> {
  PointTween({required Point begin, required Point end})
      : super(begin: begin, end: end);

  @override
  Point lerp(double t) {
    return Point(
      begin!.x + (end!.x - begin!.x) * t,
      begin!.y + (end!.y - begin!.y) * t,
    );
  }
}

// Usage:
TweenAnimationBuilder<Point>(
  tween: PointTween(begin: Point(0, 0), end: _targetPoint),
  duration: const Duration(milliseconds: 500),
  builder: (context, point, child) {
    return Transform.translate(
      offset: Offset(point.x, point.y),
      child: child,
    );
  },
  child: YourWidget(),
)
```

## Performance Optimization

### 1. Use Const Widgets

Pass constant child widgets to avoid rebuilding them:

```dart
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  color: _color,
  child: const Center(
    child: Text('Static Content'),
  ),
)
```

### 2. Minimize Rebuild Scope

Only wrap the animating parts of your UI, not the entire widget tree.

### 3. Prefer Specific Widgets

Use specific implicit animated widgets instead of `TweenAnimationBuilder` when possible - they're optimized for their use case.

### 4. Combine Animations

Use `AnimatedContainer` to animate multiple properties instead of nesting multiple implicit animation widgets.

## Common Patterns

### Loading State Transition

```dart
AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  child: _isLoading
      ? CircularProgressIndicator(key: ValueKey('loading'))
      : ContentWidget(key: ValueKey('content')),
)
```

### Expandable Panel

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  height: _expanded ? 300 : 60,
  child: SingleChildScrollView(
    child: PanelContent(),
  ),
)
```

### Pulsing Button

```dart
class PulsingButton extends StatefulWidget {
  @override
  State<PulsingButton> createState() => _PulsingButtonState();
}

class _PulsingButtonState extends State<PulsingButton> {
  bool _large = false;

  @override
  void initState() {
    super.initState();
    _pulse();
  }

  void _pulse() async {
    while (mounted) {
      await Future.delayed(Duration(milliseconds: 500));
      if (mounted) setState(() => _large = !_large);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 500),
      curve: Curves.easeInOut,
      width: _large ? 200 : 180,
      height: _large ? 60 : 50,
      child: ElevatedButton(
        onPressed: () {},
        child: Text('Click Me'),
      ),
    );
  }
}
```

## When to Use Each Widget

- **AnimatedContainer**: Multiple properties changing (size, color, padding)
- **AnimatedOpacity**: Fading in/out
- **AnimatedAlign**: Moving within parent bounds
- **AnimatedPadding**: Spacing changes only
- **AnimatedPositioned**: Absolute positioning in Stack
- **AnimatedSwitcher**: Completely different widgets
- **AnimatedCrossFade**: Exactly two widgets with size animation
- **TweenAnimationBuilder**: Custom properties not covered by other widgets

## Conclusion

Implicit animations provide a powerful, efficient way to add polish to Flutter applications with minimal code. They handle the complexity of animation controllers, tweens, and state management, allowing you to focus on what should animate rather than how to implement the animation. Start with these widgets before moving to more complex explicit animations.
