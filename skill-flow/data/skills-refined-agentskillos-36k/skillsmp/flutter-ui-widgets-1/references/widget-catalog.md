# Flutter Widget Catalog

A comprehensive reference of Flutter's widget library, organized by category and purpose. Flutter provides hundreds of widgets across 11 base categories plus two complete design systems (Material and Cupertino).

## Organization Structure

Flutter's widget catalog is divided into:

1. **Base Widgets** - Platform-agnostic building blocks organized into 11 functional categories
2. **Material Widgets** - Components implementing Material Design 3 specifications
3. **Cupertino Widgets** - Components implementing Apple's iOS/macOS design language

## Layout Widgets

Layout widgets arrange other widgets in rows, columns, grids, and custom configurations. They control positioning, sizing, and spacing.

### Row and Column

The fundamental linear layout widgets. `Row` arranges children horizontally, `Column` arranges them vertically.

```dart
import 'package:flutter/material.dart';

// Row: Horizontal layout
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Icon(Icons.home, size: 32),
    Icon(Icons.search, size: 32),
    Icon(Icons.settings, size: 32),
  ],
)

// Column: Vertical layout
Column(
  mainAxisAlignment: MainAxisAlignment.start,
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [
    Text('Header', style: TextStyle(fontSize: 24)),
    SizedBox(height: 16),
    Text('Content goes here'),
    SizedBox(height: 16),
    ElevatedButton(
      onPressed: () {},
      child: Text('Action'),
    ),
  ],
)
```

**Key Properties:**
- `mainAxisAlignment` - Alignment along the primary axis (horizontal for Row, vertical for Column)
- `crossAxisAlignment` - Alignment along the cross axis
- `mainAxisSize` - How much space to occupy on the main axis (`MainAxisSize.min` or `MainAxisSize.max`)

### Stack

Overlays widgets on top of each other, with the first child as the base layer.

```dart
Stack(
  alignment: Alignment.center,
  children: [
    // Base layer
    Container(
      width: 200,
      height: 200,
      decoration: BoxDecoration(
        color: Colors.blue,
        borderRadius: BorderRadius.circular(8),
      ),
    ),
    // Overlay layers
    Icon(Icons.favorite, size: 48, color: Colors.white),
    Positioned(
      top: 8,
      right: 8,
      child: Icon(Icons.close, color: Colors.white),
    ),
  ],
)
```

Use `Positioned` to control exact placement of children within the Stack.

### Container

A versatile widget that combines painting, positioning, and sizing capabilities. Most commonly used for padding, margins, borders, and backgrounds.

```dart
Container(
  width: 200,
  height: 100,
  padding: const EdgeInsets.all(16),
  margin: const EdgeInsets.symmetric(vertical: 8),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(12),
    boxShadow: [
      BoxShadow(
        color: Colors.black26,
        blurRadius: 4,
        offset: Offset(0, 2),
      ),
    ],
  ),
  child: Text(
    'Styled Container',
    style: TextStyle(color: Colors.white),
  ),
)
```

### Expanded and Flexible

Control how children of Row, Column, or Flex fill available space.

```dart
// Expanded: Fill available space proportionally
Row(
  children: [
    Expanded(
      flex: 1,
      child: Container(color: Colors.red, height: 50),
    ),
    Expanded(
      flex: 2,
      child: Container(color: Colors.blue, height: 50),
    ),
    Expanded(
      flex: 1,
      child: Container(color: Colors.green, height: 50),
    ),
  ],
)

// Flexible: Like Expanded but allows child to be smaller than available space
Row(
  children: [
    Flexible(
      child: Container(
        color: Colors.orange,
        height: 50,
        child: Text('This can wrap and be smaller'),
      ),
    ),
    Container(
      color: Colors.purple,
      width: 100,
      height: 50,
    ),
  ],
)
```

**Key Difference:** `Expanded` forces children to fill available space, while `Flexible` allows them to be smaller.

### Padding

Adds empty space around a widget.

```dart
Padding(
  padding: const EdgeInsets.all(16.0),
  child: Text('Padded text'),
)

// Different padding for each side
Padding(
  padding: const EdgeInsets.only(
    left: 8,
    top: 16,
    right: 8,
    bottom: 24,
  ),
  child: Text('Custom padding'),
)

// Symmetric padding
Padding(
  padding: const EdgeInsets.symmetric(
    horizontal: 16,
    vertical: 8,
  ),
  child: Text('Symmetric padding'),
)
```

### Center and Align

Position a child widget within their parent.

```dart
// Center: Centers the child
Center(
  child: Text('I am centered'),
)

// Align: Position child with precise control
Align(
  alignment: Alignment.topRight,
  child: Icon(Icons.close),
)

// Custom alignment using coordinates
Align(
  alignment: Alignment(0.5, -0.5), // x: 0.5 right, y: 0.5 up
  child: Text('Custom position'),
)
```

### SizedBox

Creates a fixed-size box, commonly used for spacing.

```dart
// Fixed size container
SizedBox(
  width: 200,
  height: 100,
  child: Card(child: Text('Fixed size')),
)

// Spacing between widgets
Column(
  children: [
    Text('First'),
    SizedBox(height: 16), // 16 pixels of vertical space
    Text('Second'),
  ],
)

// Infinite constraints
SizedBox.expand(
  child: Container(color: Colors.blue),
)
```

### Wrap

Like Row or Column but wraps children to new lines when they don't fit.

```dart
Wrap(
  spacing: 8.0, // Horizontal spacing between children
  runSpacing: 4.0, // Vertical spacing between lines
  children: [
    Chip(label: Text('Tag 1')),
    Chip(label: Text('Tag 2')),
    Chip(label: Text('Tag 3')),
    Chip(label: Text('Tag 4')),
    Chip(label: Text('Tag 5')),
    Chip(label: Text('Tag 6')),
  ],
)
```

## Scrolling Widgets

Widgets that enable scrolling when content exceeds available space.

### ListView

A scrollable list of widgets arranged linearly.

```dart
// Basic ListView
ListView(
  children: [
    ListTile(
      leading: Icon(Icons.map),
      title: Text('Map'),
    ),
    ListTile(
      leading: Icon(Icons.photo),
      title: Text('Album'),
    ),
    ListTile(
      leading: Icon(Icons.phone),
      title: Text('Phone'),
    ),
  ],
)

// ListView.builder: Efficient for long lists
ListView.builder(
  itemCount: 100,
  itemBuilder: (context, index) {
    return ListTile(
      leading: CircleAvatar(child: Text('$index')),
      title: Text('Item $index'),
      subtitle: Text('Description for item $index'),
    );
  },
)

// ListView.separated: With dividers
ListView.separated(
  itemCount: 50,
  separatorBuilder: (context, index) => Divider(),
  itemBuilder: (context, index) {
    return ListTile(title: Text('Item $index'));
  },
)
```

### GridView

A scrollable 2D array of widgets.

```dart
// GridView.count: Fixed number of tiles in cross axis
GridView.count(
  crossAxisCount: 3,
  crossAxisSpacing: 8,
  mainAxisSpacing: 8,
  padding: const EdgeInsets.all(8),
  children: List.generate(20, (index) {
    return Container(
      color: Colors.blue[100 * ((index % 9) + 1)],
      child: Center(child: Text('Item $index')),
    );
  }),
)

// GridView.extent: Maximum tile width
GridView.extent(
  maxCrossAxisExtent: 150,
  padding: const EdgeInsets.all(8),
  crossAxisSpacing: 8,
  mainAxisSpacing: 8,
  children: [
    Card(child: Center(child: Text('Tile 1'))),
    Card(child: Center(child: Text('Tile 2'))),
    Card(child: Center(child: Text('Tile 3'))),
  ],
)

// GridView.builder: Efficient for large grids
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,
    crossAxisSpacing: 8,
    mainAxisSpacing: 8,
  ),
  itemCount: 100,
  itemBuilder: (context, index) {
    return Card(
      child: Center(child: Text('Item $index')),
    );
  },
)
```

### SingleChildScrollView

Makes a single widget scrollable.

```dart
SingleChildScrollView(
  padding: const EdgeInsets.all(16),
  child: Column(
    children: [
      Container(height: 300, color: Colors.red),
      SizedBox(height: 16),
      Container(height: 300, color: Colors.blue),
      SizedBox(height: 16),
      Container(height: 300, color: Colors.green),
    ],
  ),
)
```

## Input Widgets

Widgets that accept user input.

### TextField

A text input field.

```dart
TextField(
  decoration: InputDecoration(
    labelText: 'Email',
    hintText: 'Enter your email',
    prefixIcon: Icon(Icons.email),
    border: OutlineInputBorder(),
  ),
  keyboardType: TextInputType.emailAddress,
  onChanged: (value) {
    print('Email: $value');
  },
)

// With controller for programmatic access
class MyForm extends StatefulWidget {
  @override
  State<MyForm> createState() => _MyFormState();
}

class _MyFormState extends State<MyForm> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(
          controller: _controller,
          decoration: InputDecoration(labelText: 'Name'),
        ),
        ElevatedButton(
          onPressed: () {
            print('Value: ${_controller.text}');
          },
          child: Text('Submit'),
        ),
      ],
    );
  }
}
```

### Checkbox

A Material Design checkbox.

```dart
class CheckboxExample extends StatefulWidget {
  @override
  State<CheckboxExample> createState() => _CheckboxExampleState();
}

class _CheckboxExampleState extends State<CheckboxExample> {
  bool _isChecked = false;

  @override
  Widget build(BuildContext context) {
    return CheckboxListTile(
      title: Text('Accept terms and conditions'),
      value: _isChecked,
      onChanged: (bool? value) {
        setState(() {
          _isChecked = value ?? false;
        });
      },
    );
  }
}
```

### Radio

Select one option from a set.

```dart
class RadioExample extends StatefulWidget {
  @override
  State<RadioExample> createState() => _RadioExampleState();
}

class _RadioExampleState extends State<RadioExample> {
  String _selectedValue = 'option1';

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        RadioListTile<String>(
          title: Text('Option 1'),
          value: 'option1',
          groupValue: _selectedValue,
          onChanged: (value) {
            setState(() {
              _selectedValue = value!;
            });
          },
        ),
        RadioListTile<String>(
          title: Text('Option 2'),
          value: 'option2',
          groupValue: _selectedValue,
          onChanged: (value) {
            setState(() {
              _selectedValue = value!;
            });
          },
        ),
      ],
    );
  }
}
```

### Switch

A toggle switch.

```dart
class SwitchExample extends StatefulWidget {
  @override
  State<SwitchExample> createState() => _SwitchExampleState();
}

class _SwitchExampleState extends State<SwitchExample> {
  bool _isSwitched = false;

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      title: Text('Enable notifications'),
      value: _isSwitched,
      onChanged: (bool value) {
        setState(() {
          _isSwitched = value;
        });
      },
    );
  }
}
```

### Slider

Select a value from a range.

```dart
class SliderExample extends StatefulWidget {
  @override
  State<SliderExample> createState() => _SliderExampleState();
}

class _SliderExampleState extends State<SliderExample> {
  double _currentValue = 50;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Value: ${_currentValue.round()}'),
        Slider(
          value: _currentValue,
          min: 0,
          max: 100,
          divisions: 100,
          label: _currentValue.round().toString(),
          onChanged: (double value) {
            setState(() {
              _currentValue = value;
            });
          },
        ),
      ],
    );
  }
}
```

## Display Widgets

Widgets for displaying content.

### Text

Display and style text.

```dart
// Basic text
Text('Hello, World!')

// Styled text
Text(
  'Styled Text',
  style: TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
    letterSpacing: 1.2,
  ),
)

// Rich text with multiple styles
Text.rich(
  TextSpan(
    text: 'Hello ',
    style: TextStyle(fontSize: 18),
    children: [
      TextSpan(
        text: 'bold',
        style: TextStyle(fontWeight: FontWeight.bold),
      ),
      TextSpan(text: ' and '),
      TextSpan(
        text: 'colored',
        style: TextStyle(color: Colors.red),
      ),
      TextSpan(text: ' text'),
    ],
  ),
)
```

### Image

Display images from various sources.

```dart
// Network image
Image.network(
  'https://picsum.photos/250?image=9',
  width: 200,
  height: 200,
  fit: BoxFit.cover,
)

// Asset image
Image.asset(
  'assets/images/logo.png',
  width: 100,
  height: 100,
)

// With loading placeholder
Image.network(
  'https://example.com/image.jpg',
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;
    return Center(
      child: CircularProgressIndicator(
        value: loadingProgress.expectedTotalBytes != null
            ? loadingProgress.cumulativeBytesLoaded /
                loadingProgress.expectedTotalBytes!
            : null,
      ),
    );
  },
)
```

### Icon

Display Material Design icons.

```dart
// Basic icon
Icon(Icons.home)

// Styled icon
Icon(
  Icons.favorite,
  color: Colors.red,
  size: 48,
)

// Icon with semantic label for accessibility
Icon(
  Icons.volume_up,
  semanticLabel: 'Increase volume',
)
```

### Card

A Material Design card with elevation.

```dart
Card(
  elevation: 4,
  margin: const EdgeInsets.all(8),
  child: Padding(
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
        Text('Card content goes here'),
        SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            TextButton(
              onPressed: () {},
              child: Text('ACTION 1'),
            ),
            TextButton(
              onPressed: () {},
              child: Text('ACTION 2'),
            ),
          ],
        ),
      ],
    ),
  ),
)
```

### CircularProgressIndicator and LinearProgressIndicator

Display loading states.

```dart
// Indeterminate progress
CircularProgressIndicator()

// Determinate progress
CircularProgressIndicator(
  value: 0.7, // 70% complete
  backgroundColor: Colors.grey[300],
  valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
)

// Linear progress
LinearProgressIndicator(
  value: 0.5,
  backgroundColor: Colors.grey[300],
  valueColor: AlwaysStoppedAnimation<Color>(Colors.green),
)
```

## Material Widgets

Comprehensive Material Design 3 components.

### Scaffold

The basic Material app structure with app bar, body, drawer, and floating action button.

```dart
Scaffold(
  appBar: AppBar(
    title: Text('App Title'),
    actions: [
      IconButton(
        icon: Icon(Icons.search),
        onPressed: () {},
      ),
      IconButton(
        icon: Icon(Icons.more_vert),
        onPressed: () {},
      ),
    ],
  ),
  body: Center(child: Text('Body content')),
  floatingActionButton: FloatingActionButton(
    onPressed: () {},
    child: Icon(Icons.add),
  ),
  drawer: Drawer(
    child: ListView(
      children: [
        DrawerHeader(
          decoration: BoxDecoration(color: Colors.blue),
          child: Text('Header', style: TextStyle(color: Colors.white)),
        ),
        ListTile(
          leading: Icon(Icons.home),
          title: Text('Home'),
          onTap: () {},
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text('Settings'),
          onTap: () {},
        ),
      ],
    ),
  ),
  bottomNavigationBar: BottomNavigationBar(
    items: const [
      BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
      BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
      BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
    ],
  ),
)
```

### Buttons

Material 3 provides several button variants.

```dart
// Elevated button
ElevatedButton(
  onPressed: () {},
  child: Text('Elevated Button'),
)

// Filled button (M3)
FilledButton(
  onPressed: () {},
  child: Text('Filled Button'),
)

// Filled tonal button (M3)
FilledButton.tonal(
  onPressed: () {},
  child: Text('Filled Tonal'),
)

// Outlined button
OutlinedButton(
  onPressed: () {},
  child: Text('Outlined Button'),
)

// Text button
TextButton(
  onPressed: () {},
  child: Text('Text Button'),
)

// Icon button
IconButton(
  icon: Icon(Icons.favorite),
  onPressed: () {},
)

// Button with icon
ElevatedButton.icon(
  onPressed: () {},
  icon: Icon(Icons.add),
  label: Text('Add Item'),
)
```

### Dialogs

Show dialogs and bottom sheets.

```dart
// Alert dialog
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: Text('Alert'),
    content: Text('This is an alert dialog'),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: Text('Cancel'),
      ),
      TextButton(
        onPressed: () {
          // Handle action
          Navigator.pop(context);
        },
        child: Text('OK'),
      ),
    ],
  ),
);

// Bottom sheet
showModalBottomSheet(
  context: context,
  builder: (context) => Container(
    padding: const EdgeInsets.all(16),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ListTile(
          leading: Icon(Icons.share),
          title: Text('Share'),
          onTap: () {},
        ),
        ListTile(
          leading: Icon(Icons.link),
          title: Text('Get link'),
          onTap: () {},
        ),
      ],
    ),
  ),
);
```

### SnackBar

Brief messages at the bottom of the screen.

```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Text('Message sent'),
    action: SnackBarAction(
      label: 'Undo',
      onPressed: () {
        // Handle undo
      },
    ),
    duration: Duration(seconds: 3),
  ),
);
```

### NavigationBar and NavigationRail

Material 3 navigation components.

```dart
// NavigationBar (bottom navigation for mobile)
NavigationBar(
  selectedIndex: _selectedIndex,
  onDestinationSelected: (index) {
    setState(() {
      _selectedIndex = index;
    });
  },
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.home_outlined),
      selectedIcon: Icon(Icons.home),
      label: 'Home',
    ),
    NavigationDestination(
      icon: Icon(Icons.search_outlined),
      selectedIcon: Icon(Icons.search),
      label: 'Search',
    ),
    NavigationDestination(
      icon: Icon(Icons.person_outline),
      selectedIcon: Icon(Icons.person),
      label: 'Profile',
    ),
  ],
)

// NavigationRail (side navigation for tablets/desktop)
NavigationRail(
  selectedIndex: _selectedIndex,
  onDestinationSelected: (index) {
    setState(() {
      _selectedIndex = index;
    });
  },
  labelType: NavigationRailLabelType.all,
  destinations: const [
    NavigationRailDestination(
      icon: Icon(Icons.home_outlined),
      selectedIcon: Icon(Icons.home),
      label: Text('Home'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.search_outlined),
      selectedIcon: Icon(Icons.search),
      label: Text('Search'),
    ),
  ],
)
```

## Cupertino Widgets

iOS-style widgets implementing Apple's Human Interface Guidelines. See [Cupertino Widgets](cupertino-widgets.md) for comprehensive coverage.

### Basic Cupertino Widgets

```dart
// Cupertino button
CupertinoButton(
  onPressed: () {},
  child: Text('iOS Button'),
)

// Filled Cupertino button
CupertinoButton.filled(
  onPressed: () {},
  child: Text('Filled iOS Button'),
)

// Cupertino switch
CupertinoSwitch(
  value: _switchValue,
  onChanged: (bool value) {
    setState(() {
      _switchValue = value;
    });
  },
)

// Cupertino slider
CupertinoSlider(
  value: _sliderValue,
  onChanged: (double value) {
    setState(() {
      _sliderValue = value;
    });
  },
)
```

## Best Practices

1. **Use const constructors** wherever possible for better performance
2. **Extract complex widgets** into separate widget classes for reusability
3. **Prefer composition over inheritance** when building custom widgets
4. **Use appropriate layout widgets** - don't nest Rows/Columns unnecessarily
5. **Leverage themed widgets** that adapt to app theme automatically
6. **Consider platform-adaptive widgets** for cross-platform consistency
7. **Use builder methods** for long lists (ListView.builder, GridView.builder)
8. **Dispose controllers** in StatefulWidget.dispose() to prevent memory leaks
9. **Use semantic labels** on icons and images for accessibility
10. **Test on multiple screen sizes** using different device simulators

## Performance Tips

- Use `const` widgets to avoid unnecessary rebuilds
- Use `ListView.builder` instead of `ListView` for long lists
- Use `RepaintBoundary` to isolate expensive paint operations
- Avoid deep widget trees; extract subtrees into separate widgets
- Use `AutomaticKeepAliveClientMixin` to preserve scroll positions
- Profile with Flutter DevTools to identify performance bottlenecks

## Further Reading

- [Flutter Widget Index](https://docs.flutter.dev/reference/widgets)
- [Layout Patterns](layout-patterns.md)
- [Material Design 3](material-design-3.md)
- [Widget Lifecycle](widget-lifecycle.md)
