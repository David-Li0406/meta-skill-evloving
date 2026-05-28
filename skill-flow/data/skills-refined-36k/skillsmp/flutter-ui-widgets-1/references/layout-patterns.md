# Flutter Layout Patterns

A comprehensive guide to building layouts in Flutter, covering fundamental concepts, layout widgets, constraints, sizing strategies, and common patterns for responsive UIs.

## Core Layout Principles

Flutter's layout system is built entirely on widgets. The framework uses a composition model where simple widgets combine to create complex layouts. Understanding how constraints flow through the widget tree is essential for effective layout design.

### The Constraint Model

Flutter's layout follows a three-step process:

1. **Constraints go down** - Parent widgets pass constraints (min/max width and height) to their children
2. **Sizes go up** - Children decide their size within those constraints and report it to the parent
3. **Parent sets position** - Parent positions children based on size and alignment properties

This constraint-based system differs from traditional layout models and is crucial to understand for avoiding common layout issues.

### Key Constraint Rules

- A widget cannot know its position on screen; only its parent knows this
- A widget cannot have any size it wants; it must fit within parent constraints
- Parent widgets set children positions; children cannot position themselves
- The size and position of a widget depends on the entire widget tree

## Row and Column Layouts

`Row` and `Column` are the fundamental building blocks for linear layouts in Flutter.

### Row (Horizontal Layout)

Arranges children horizontally from left to right.

```dart
import 'package:flutter/material.dart';

Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  crossAxisAlignment: CrossAxisAlignment.center,
  mainAxisSize: MainAxisSize.max,
  children: [
    Icon(Icons.home, size: 32),
    Icon(Icons.search, size: 32),
    Icon(Icons.settings, size: 32),
  ],
)
```

**Main axis:** Horizontal (left to right)
**Cross axis:** Vertical (top to bottom)

### Column (Vertical Layout)

Arranges children vertically from top to bottom.

```dart
Column(
  mainAxisAlignment: MainAxisAlignment.start,
  crossAxisAlignment: CrossAxisAlignment.stretch,
  mainAxisSize: MainAxisSize.min,
  children: [
    Text('Header', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
    SizedBox(height: 16),
    Text('Description text that can wrap to multiple lines'),
    SizedBox(height: 24),
    ElevatedButton(
      onPressed: () {},
      child: Text('Action Button'),
    ),
  ],
)
```

**Main axis:** Vertical (top to bottom)
**Cross axis:** Horizontal (left to right)

### Main Axis Alignment

Controls how children are positioned along the primary axis.

```dart
// MainAxisAlignment.start - Children at the start
Row(
  mainAxisAlignment: MainAxisAlignment.start,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [A B C                    ]

// MainAxisAlignment.center - Children in the center
Row(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [          A B C          ]

// MainAxisAlignment.end - Children at the end
Row(
  mainAxisAlignment: MainAxisAlignment.end,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [                    A B C]

// MainAxisAlignment.spaceBetween - Equal space between children
Row(
  mainAxisAlignment: MainAxisAlignment.spaceBetween,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [A          B          C]

// MainAxisAlignment.spaceAround - Equal space around each child
Row(
  mainAxisAlignment: MainAxisAlignment.spaceAround,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [  A    B    C  ]

// MainAxisAlignment.spaceEvenly - Equal space including edges
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [Text('A'), Text('B'), Text('C')],
)
// Result: [   A   B   C   ]
```

### Cross Axis Alignment

Controls how children are positioned along the cross axis.

```dart
// CrossAxisAlignment.start - Align to top (Column) or left (Row)
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Text('Short'),
    Text('Much longer text here'),
  ],
)

// CrossAxisAlignment.center - Center children
Column(
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Text('Short'),
    Text('Much longer text here'),
  ],
)

// CrossAxisAlignment.end - Align to bottom (Column) or right (Row)
Column(
  crossAxisAlignment: CrossAxisAlignment.end,
  children: [
    Text('Short'),
    Text('Much longer text here'),
  ],
)

// CrossAxisAlignment.stretch - Stretch to fill cross axis
Column(
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [
    Container(color: Colors.red, height: 50),
    Container(color: Colors.blue, height: 50),
  ],
)

// CrossAxisAlignment.baseline - Align text baselines
Row(
  crossAxisAlignment: CrossAxisAlignment.baseline,
  textBaseline: TextBaseline.alphabetic,
  children: [
    Text('Small', style: TextStyle(fontSize: 12)),
    Text('Medium', style: TextStyle(fontSize: 24)),
    Text('Large', style: TextStyle(fontSize: 36)),
  ],
)
```

### Main Axis Size

Controls how much space the Row or Column occupies on the main axis.

```dart
// MainAxisSize.max - Take all available space (default)
Row(
  mainAxisSize: MainAxisSize.max,
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    Container(width: 50, height: 50, color: Colors.red),
    Container(width: 50, height: 50, color: Colors.blue),
  ],
)

// MainAxisSize.min - Only take space needed by children
Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    Container(width: 50, height: 50, color: Colors.red),
    Container(width: 50, height: 50, color: Colors.blue),
  ],
)
```

`MainAxisSize.min` is useful when you want to pack children tightly, such as in a `Card` or `Dialog`.

## Expanded and Flexible

Control how children of Row, Column, or Flex fill available space.

### Expanded

Forces children to fill available space proportionally using the `flex` property.

```dart
Row(
  children: [
    Expanded(
      flex: 1,
      child: Container(
        color: Colors.red,
        height: 100,
        child: Center(child: Text('1x')),
      ),
    ),
    Expanded(
      flex: 2,
      child: Container(
        color: Colors.blue,
        height: 100,
        child: Center(child: Text('2x')),
      ),
    ),
    Expanded(
      flex: 1,
      child: Container(
        color: Colors.green,
        height: 100,
        child: Center(child: Text('1x')),
      ),
    ),
  ],
)
```

In this example, the blue container takes twice the space of the red and green containers.

### Flexible

Like `Expanded` but allows children to be smaller than the available space.

```dart
Row(
  children: [
    Flexible(
      flex: 1,
      fit: FlexFit.tight, // Same as Expanded
      child: Container(color: Colors.red, height: 50),
    ),
    Flexible(
      flex: 1,
      fit: FlexFit.loose, // Can be smaller than allocated space
      child: Container(
        color: Colors.blue,
        height: 50,
        width: 50, // Will only take 50 pixels even if more is available
      ),
    ),
  ],
)
```

**Key differences:**
- `Expanded` = `Flexible` with `fit: FlexFit.tight`
- `Flexible` with `fit: FlexFit.loose` allows child to be smaller than allocated space

### Mixing Fixed and Flexible Sizing

```dart
Row(
  children: [
    // Fixed width
    Container(
      width: 80,
      height: 100,
      color: Colors.red,
      child: Center(child: Text('Fixed')),
    ),
    // Takes remaining space
    Expanded(
      child: Container(
        color: Colors.blue,
        height: 100,
        child: Center(child: Text('Expanded')),
      ),
    ),
    // Another fixed width
    Container(
      width: 80,
      height: 100,
      color: Colors.green,
      child: Center(child: Text('Fixed')),
    ),
  ],
)
```

## Stack Layouts

`Stack` overlays widgets on top of each other, with the first child as the base layer.

### Basic Stack

```dart
Stack(
  alignment: Alignment.center,
  children: [
    // Base layer
    Container(
      width: 300,
      height: 200,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.blue, Colors.purple],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
    ),
    // Overlay
    Icon(Icons.favorite, size: 64, color: Colors.white),
  ],
)
```

### Positioned

Control exact placement of children within the Stack.

```dart
Stack(
  children: [
    // Base layer - takes full size
    Container(
      width: 300,
      height: 200,
      color: Colors.blue,
    ),
    // Top-left corner
    Positioned(
      top: 10,
      left: 10,
      child: Icon(Icons.menu, color: Colors.white),
    ),
    // Top-right corner
    Positioned(
      top: 10,
      right: 10,
      child: Icon(Icons.close, color: Colors.white),
    ),
    // Bottom-center
    Positioned(
      bottom: 10,
      left: 0,
      right: 0,
      child: Center(
        child: Text(
          'Centered at bottom',
          style: TextStyle(color: Colors.white),
        ),
      ),
    ),
    // Stretched to fill
    Positioned.fill(
      child: Center(child: Text('Fills entire stack')),
    ),
  ],
)
```

### Stack Alignment

```dart
// Different alignment options
Stack(
  alignment: Alignment.topLeft,
  children: [
    Container(width: 200, height: 200, color: Colors.blue),
    Container(width: 100, height: 100, color: Colors.red),
  ],
)

// Custom alignment using x, y coordinates
// x: -1.0 (left) to 1.0 (right)
// y: -1.0 (top) to 1.0 (bottom)
Stack(
  alignment: Alignment(0.5, -0.5), // Right and up
  children: [
    Container(width: 200, height: 200, color: Colors.blue),
    Container(width: 50, height: 50, color: Colors.red),
  ],
)
```

### IndexedStack

Like `Stack` but only shows one child at a time.

```dart
class TabSwitcher extends StatefulWidget {
  @override
  State<TabSwitcher> createState() => _TabSwitcherState();
}

class _TabSwitcherState extends State<TabSwitcher> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            ElevatedButton(
              onPressed: () => setState(() => _currentIndex = 0),
              child: Text('Tab 1'),
            ),
            ElevatedButton(
              onPressed: () => setState(() => _currentIndex = 1),
              child: Text('Tab 2'),
            ),
            ElevatedButton(
              onPressed: () => setState(() => _currentIndex = 2),
              child: Text('Tab 3'),
            ),
          ],
        ),
        Expanded(
          child: IndexedStack(
            index: _currentIndex,
            children: [
              Container(color: Colors.red, child: Center(child: Text('Content 1'))),
              Container(color: Colors.blue, child: Center(child: Text('Content 2'))),
              Container(color: Colors.green, child: Center(child: Text('Content 3'))),
            ],
          ),
        ),
      ],
    );
  }
}
```

## Container and Decoration

`Container` combines several layout capabilities: padding, margins, borders, background colors, and sizing.

### Comprehensive Container Example

```dart
Container(
  // Sizing
  width: 200,
  height: 150,

  // External spacing
  margin: const EdgeInsets.all(16),

  // Internal spacing
  padding: const EdgeInsets.symmetric(
    horizontal: 20,
    vertical: 12,
  ),

  // Alignment of child within container
  alignment: Alignment.center,

  // Decoration (background, border, etc.)
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(
      color: Colors.blue.shade900,
      width: 2,
    ),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.2),
        blurRadius: 8,
        offset: Offset(0, 4),
      ),
    ],
    gradient: LinearGradient(
      colors: [Colors.blue.shade300, Colors.blue.shade700],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    ),
  ),

  child: Text(
    'Container',
    style: TextStyle(color: Colors.white, fontSize: 18),
  ),
)
```

### BoxDecoration Options

```dart
// Solid color
BoxDecoration(color: Colors.blue)

// Gradient
BoxDecoration(
  gradient: LinearGradient(
    colors: [Colors.blue, Colors.purple],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  ),
)

// Radial gradient
BoxDecoration(
  gradient: RadialGradient(
    colors: [Colors.yellow, Colors.orange],
    radius: 0.5,
  ),
)

// Border
BoxDecoration(
  border: Border.all(color: Colors.blue, width: 2),
  borderRadius: BorderRadius.circular(8),
)

// Asymmetric border radius
BoxDecoration(
  borderRadius: BorderRadius.only(
    topLeft: Radius.circular(20),
    topRight: Radius.circular(20),
  ),
)

// Circular shape
BoxDecoration(
  shape: BoxShape.circle,
  color: Colors.blue,
)

// Image background
BoxDecoration(
  image: DecorationImage(
    image: NetworkImage('https://example.com/image.jpg'),
    fit: BoxFit.cover,
  ),
)

// Shadow
BoxDecoration(
  color: Colors.white,
  boxShadow: [
    BoxShadow(
      color: Colors.black26,
      blurRadius: 10,
      spreadRadius: 2,
      offset: Offset(0, 4),
    ),
  ],
)
```

## Constraints and Sizing

Understanding how constraints work is critical for avoiding layout errors.

### Tight vs Loose Constraints

**Tight constraints:** Min and max are the same (widget must be exact size)
```dart
// Container forces tight constraints
Container(
  width: 100,
  height: 100,
  child: SizedBox.expand(), // Will be exactly 100x100
)
```

**Loose constraints:** Min is smaller than max (widget can choose size within range)
```dart
// Column provides loose constraints
Column(
  children: [
    Container(height: 50), // Can be any width, must be 50 high
  ],
)
```

### ConstrainedBox

Impose additional constraints on a widget.

```dart
// Set minimum size
ConstrainedBox(
  constraints: BoxConstraints(
    minWidth: 100,
    minHeight: 50,
  ),
  child: Container(color: Colors.blue),
)

// Set maximum size
ConstrainedBox(
  constraints: BoxConstraints(
    maxWidth: 200,
    maxHeight: 100,
  ),
  child: Image.network('https://example.com/large-image.jpg'),
)

// Set exact size (tight constraints)
ConstrainedBox(
  constraints: BoxConstraints.tight(Size(150, 100)),
  child: Container(color: Colors.red),
)

// Expand to fill parent
ConstrainedBox(
  constraints: BoxConstraints.expand(),
  child: Container(color: Colors.green),
)
```

### UnconstrainedBox

Remove parent constraints (use sparingly).

```dart
UnconstrainedBox(
  child: Container(
    width: 500, // Can exceed parent width
    height: 300,
    color: Colors.blue,
  ),
)
```

### SizedBox

Create a fixed-size box or spacing.

```dart
// Fixed size
SizedBox(
  width: 100,
  height: 100,
  child: Container(color: Colors.red),
)

// Spacing
Column(
  children: [
    Text('First'),
    SizedBox(height: 20), // 20 pixels vertical space
    Text('Second'),
  ],
)

// Expand to fill parent
SizedBox.expand(
  child: Container(color: Colors.blue),
)

// Shrink to zero size
SizedBox.shrink()
```

### AspectRatio

Maintain a specific aspect ratio.

```dart
AspectRatio(
  aspectRatio: 16 / 9, // 16:9 ratio
  child: Container(
    color: Colors.blue,
    child: Center(child: Text('16:9 container')),
  ),
)

// 1:1 square
AspectRatio(
  aspectRatio: 1,
  child: Image.network('https://example.com/image.jpg', fit: BoxFit.cover),
)
```

### FractionallySizedBox

Size widget as a fraction of parent size.

```dart
FractionallySizedBox(
  widthFactor: 0.8, // 80% of parent width
  heightFactor: 0.5, // 50% of parent height
  alignment: Alignment.center,
  child: Container(color: Colors.blue),
)
```

### LimitedBox

Provide constraints only when parent provides unbounded constraints.

```dart
ListView(
  children: [
    LimitedBox(
      maxHeight: 200, // Prevents unbounded height error
      child: Container(color: Colors.blue),
    ),
  ],
)
```

## Common Layout Patterns

### Card with Image and Text

```dart
Card(
  clipBehavior: Clip.antiAlias,
  elevation: 4,
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      AspectRatio(
        aspectRatio: 16 / 9,
        child: Image.network(
          'https://picsum.photos/400/225',
          fit: BoxFit.cover,
        ),
      ),
      Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Card Title',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Card description goes here with additional details about the content.',
              style: TextStyle(color: Colors.grey.shade700),
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: () {},
                  child: Text('SHARE'),
                ),
                SizedBox(width: 8),
                FilledButton(
                  onPressed: () {},
                  child: Text('VIEW'),
                ),
              ],
            ),
          ],
        ),
      ),
    ],
  ),
)
```

### Header with Avatar and Actions

```dart
Container(
  padding: const EdgeInsets.all(16),
  child: Row(
    children: [
      CircleAvatar(
        radius: 24,
        backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=1'),
      ),
      SizedBox(width: 12),
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'John Doe',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              'Software Engineer',
              style: TextStyle(
                color: Colors.grey.shade600,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
      IconButton(
        icon: Icon(Icons.message),
        onPressed: () {},
      ),
      IconButton(
        icon: Icon(Icons.phone),
        onPressed: () {},
      ),
    ],
  ),
)
```

### Responsive Two-Column Layout

```dart
class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 600) {
          // Two-column layout for wide screens
          return Row(
            children: [
              Expanded(child: _buildColumn1()),
              SizedBox(width: 16),
              Expanded(child: _buildColumn2()),
            ],
          );
        } else {
          // Single-column layout for narrow screens
          return Column(
            children: [
              _buildColumn1(),
              SizedBox(height: 16),
              _buildColumn2(),
            ],
          );
        }
      },
    );
  }

  Widget _buildColumn1() {
    return Container(
      padding: EdgeInsets.all(16),
      color: Colors.blue.shade100,
      child: Text('Column 1'),
    );
  }

  Widget _buildColumn2() {
    return Container(
      padding: EdgeInsets.all(16),
      color: Colors.green.shade100,
      child: Text('Column 2'),
    );
  }
}
```

### Badge on Avatar

```dart
Stack(
  children: [
    CircleAvatar(
      radius: 40,
      backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=5'),
    ),
    Positioned(
      bottom: 0,
      right: 0,
      child: Container(
        width: 24,
        height: 24,
        decoration: BoxDecoration(
          color: Colors.green,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white, width: 2),
        ),
        child: Icon(Icons.check, size: 14, color: Colors.white),
      ),
    ),
  ],
)
```

### Bottom Sheet Layout

```dart
Container(
  padding: EdgeInsets.only(
    top: 16,
    left: 16,
    right: 16,
    bottom: MediaQuery.of(context).viewInsets.bottom + 16,
  ),
  child: Column(
    mainAxisSize: MainAxisSize.min,
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Text(
        'Bottom Sheet Title',
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      ),
      SizedBox(height: 16),
      TextField(
        decoration: InputDecoration(
          labelText: 'Input field',
          border: OutlineInputBorder(),
        ),
      ),
      SizedBox(height: 16),
      FilledButton(
        onPressed: () {},
        child: Text('Submit'),
      ),
    ],
  ),
)
```

## Debugging Layouts

### Visual Debugging

Enable visual debugging to see widget boundaries:

```dart
import 'package:flutter/rendering.dart';

void main() {
  debugPaintSizeEnabled = true; // Show widget boundaries
  debugPaintBaselinesEnabled = true; // Show text baselines
  debugPaintPointersEnabled = true; // Show tap areas
  runApp(MyApp());
}
```

### LayoutBuilder

Respond to parent constraints:

```dart
LayoutBuilder(
  builder: (context, constraints) {
    print('Available width: ${constraints.maxWidth}');
    print('Available height: ${constraints.maxHeight}');

    return Container(
      color: constraints.maxWidth > 600 ? Colors.blue : Colors.red,
      child: Text('Width: ${constraints.maxWidth}'),
    );
  },
)
```

### Common Layout Errors

**RenderFlex overflow:** Child is too large for parent
```dart
// Problem: Text overflows Row
Row(
  children: [
    Text('Very long text that will overflow the row'),
  ],
)

// Solution: Use Expanded or Flexible
Row(
  children: [
    Expanded(
      child: Text('Very long text that will now wrap properly'),
    ),
  ],
)
```

**Unbounded constraints:** Parent doesn't provide constraints
```dart
// Problem: Column in Column without constraints
Column(
  children: [
    Column(children: [...]), // Error: unbounded height
  ],
)

// Solution: Use Expanded or constrain height
Column(
  children: [
    Expanded(
      child: Column(children: [...]),
    ),
  ],
)
```

## Best Practices

1. **Use const constructors** for widgets that don't change
2. **Extract complex layouts** into separate widget classes
3. **Prefer Column/Row over Container nesting** for layout
4. **Use Expanded/Flexible** instead of fixed sizes when possible
5. **Consider screen sizes** with MediaQuery and LayoutBuilder
6. **Test overflow cases** with long text and different screen sizes
7. **Use Spacer()** for flexible spacing in Row/Column
8. **Avoid deep nesting** - extract subtrees into methods or widgets
9. **Use appropriate MainAxisSize** (min for packed layouts, max for spread layouts)
10. **Profile layouts** with Flutter DevTools to identify performance issues

## Responsive Design

Use `MediaQuery` to adapt to screen size:

```dart
class ResponsiveWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isSmallScreen = size.width < 600;
    final isMediumScreen = size.width >= 600 && size.width < 1200;
    final isLargeScreen = size.width >= 1200;

    return Padding(
      padding: EdgeInsets.all(isSmallScreen ? 8 : 16),
      child: Column(
        children: [
          Text(
            'Responsive Text',
            style: TextStyle(
              fontSize: isSmallScreen ? 14 : (isMediumScreen ? 16 : 18),
            ),
          ),
          if (isLargeScreen)
            Row(children: [...]) // Only show on large screens
          else
            Column(children: [...]) // Show on small/medium screens
        ],
      ),
    );
  }
}
```

## Further Reading

- [Widget Catalog](widget-catalog.md)
- [Material Design 3](material-design-3.md)
- [Custom Widgets Example](../examples/custom-widgets.md)
- [Composition Patterns Example](../examples/composition-patterns.md)
