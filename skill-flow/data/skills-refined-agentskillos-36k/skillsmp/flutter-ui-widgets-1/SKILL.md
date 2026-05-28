---
name: flutter-ui-widgets
description: Comprehensive guidance for building Flutter user interfaces with widgets, including Material Design 3 components, Cupertino iOS-style widgets, layout composition patterns, widget lifecycle management, and creating reusable custom UI components. Use when working with Flutter UI, composing widgets, building layouts, implementing Material Design, creating iOS-style interfaces, or developing custom reusable widgets.
version: 1.0.0
---

# Flutter UI Widgets

Master Flutter's powerful widget-based UI system to build beautiful, responsive, and platform-adaptive interfaces. This skill covers everything from basic layout widgets to advanced Material Design 3 components and iOS-style Cupertino widgets.

## Purpose

Flutter's UI is built entirely from widgets—composable building blocks that describe what the view should look like given their current configuration and state. Everything in Flutter is a widget, from structural elements like buttons and menus to layout models like padding and alignment. This fundamental design philosophy enables unprecedented flexibility and reusability.

The widget system operates on a composition model where complex UIs emerge from combining simple, single-purpose widgets. Rather than inheriting behavior through deep class hierarchies, Flutter favors shallow, broad hierarchies that maximize possible combinations. This approach leads to code that is concise, performant, and easier to reason about.

Flutter ships with two comprehensive design systems: Material Design for cross-platform consistency and Cupertino for iOS-native aesthetics. Material Design 3, enabled by default since Flutter 3.16, provides dynamic color support, enhanced accessibility, and an expressive component library. Cupertino widgets implement Apple's Human Interface Guidelines with high-fidelity iOS and macOS styling. You can use either system exclusively or mix them within the same app for truly adaptive experiences.

## Core Concepts

### 1. Widget Composition

Flutter's architecture is built on composition, not inheritance. Complex widgets are created by combining simpler widgets, each doing one thing well. The framework's shallow class hierarchy maximizes flexibility—instead of subclassing to modify behavior, you compose new widgets from existing ones.

**Example:**
```dart
// Composition: Build complex UI from simple widgets
Widget build(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: Colors.blue,
      borderRadius: BorderRadius.circular(8),
    ),
    child: Row(
      children: [
        const Icon(Icons.star),
        const SizedBox(width: 8),
        const Text('Featured'),
      ],
    ),
  );
}
```

### 2. Stateless vs Stateful Widgets

Widgets come in two flavors: `StatelessWidget` for immutable UI and `StatefulWidget` for dynamic, interactive components. Stateless widgets are ideal for static content, while stateful widgets maintain mutable state that can trigger rebuilds when changed via `setState()`.

**Example:**
```dart
// Stateless: UI doesn't change
class WelcomeMessage extends StatelessWidget {
  const WelcomeMessage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text('Welcome to Flutter!');
  }
}

// Stateful: UI responds to interaction
class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### 3. Layout Constraints

Flutter's layout system is constraint-based. Parent widgets pass constraints (minimum and maximum width/height) down to their children. Children then decide their size within those constraints, and the parent positions them accordingly. Understanding this "constraints go down, sizes go up, parent sets position" model is crucial for effective layout design.

### 4. Material Design 3

Material 3 is Flutter's default design language, providing a comprehensive set of components, theming capabilities, and design tokens. It emphasizes dynamic color, personal expression, and accessibility. Key widgets include `Scaffold`, `AppBar`, `Card`, `FloatingActionButton`, and navigation components like `NavigationBar` and `NavigationDrawer`.

### 5. Cupertino Widgets

For iOS-native experiences, Cupertino widgets implement Apple's design language with pixel-perfect fidelity. Use `CupertinoApp`, `CupertinoPageScaffold`, `CupertinoButton`, and other iOS-styled components when targeting Apple platforms or when you need that specific aesthetic.

### 6. Responsive Layouts

Build responsive UIs using `Row`, `Column`, `Expanded`, `Flexible`, and `MediaQuery`. `Expanded` makes children fill available space proportionally, while `Flexible` allows wrapping. Use `MediaQuery` to adapt layouts based on screen size, orientation, and platform.

### 7. Widget Lifecycle

Stateful widgets have a well-defined lifecycle: `initState()` for initialization, `build()` for rendering, `setState()` for triggering rebuilds, and `dispose()` for cleanup. Understanding this lifecycle is essential for managing resources, subscriptions, and animations properly.

### 8. Custom Widgets

Create reusable custom widgets to maintain consistency, reduce duplication, and encapsulate complexity. Extract common UI patterns into dedicated widget classes that can be configured through constructor parameters. This promotes a clean architecture and makes your codebase more maintainable.

## Quick Reference

### Basic Layout
```dart
import 'package:flutter/material.dart';

// Column: Vertical layout
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Item 1'),
    const Text('Item 2'),
    const Text('Item 3'),
  ],
)

// Row: Horizontal layout
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [
    const Icon(Icons.home),
    const Icon(Icons.search),
    const Icon(Icons.settings),
  ],
)

// Stack: Overlapping widgets
Stack(
  alignment: Alignment.center,
  children: [
    Container(width: 200, height: 200, color: Colors.blue),
    const Text('Centered', style: TextStyle(color: Colors.white)),
  ],
)
```

### Responsive Sizing
```dart
// Expanded: Fill available space proportionally
Row(
  children: [
    Expanded(
      flex: 1,
      child: Container(color: Colors.red),
    ),
    Expanded(
      flex: 2,
      child: Container(color: Colors.blue),
    ),
  ],
)

// Flexible: Flexible sizing with wrapping
Row(
  children: [
    Flexible(
      child: Text('This text will wrap if needed'),
    ),
  ],
)
```

### Material Design 3
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(title: const Text('Material 3')),
        body: Center(
          child: FilledButton(
            onPressed: () {},
            child: const Text('Filled Button'),
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {},
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
}
```

### Cupertino (iOS Style)
```dart
import 'package:flutter/cupertino.dart';

class MyIOSApp extends StatelessWidget {
  const MyIOSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoApp(
      theme: const CupertinoThemeData(
        primaryColor: CupertinoColors.systemBlue,
      ),
      home: CupertinoPageScaffold(
        navigationBar: const CupertinoNavigationBar(
          middle: Text('iOS Style'),
        ),
        child: Center(
          child: CupertinoButton.filled(
            onPressed: () {},
            child: const Text('iOS Button'),
          ),
        ),
      ),
    );
  }
}
```

### Stateful Widget Template
```dart
class MyWidget extends StatefulWidget {
  const MyWidget({super.key});

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  // State variables
  int _counter = 0;

  @override
  void initState() {
    super.initState();
    // Initialize state, subscribe to streams
  }

  @override
  void dispose() {
    // Clean up controllers, subscriptions
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: () => setState(() => _counter++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### Custom Reusable Widget
```dart
class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final IconData? icon;

  const PrimaryButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(icon),
            const SizedBox(width: 8),
          ],
          Text(label),
        ],
      ),
    );
  }
}
```

## Progressive Disclosure

For comprehensive information on specific topics, refer to the following detailed guides:

- **[Widget Catalog](references/widget-catalog.md)** - Complete reference of Flutter widgets organized by category, including layout, input, display, Material, and Cupertino widgets with code examples

- **[Layout Patterns](references/layout-patterns.md)** - Deep dive into Row, Column, Stack, Expanded, Flexible, constraints, sizing, and common layout patterns for responsive UIs

- **[Material Design 3](references/material-design-3.md)** - Comprehensive guide to Material 3 components, theming, color schemes, typography, and migration from Material 2

- **[Cupertino Widgets](references/cupertino-widgets.md)** - Complete reference for iOS-style widgets, when to use Cupertino vs Material, and building platform-adaptive UIs

- **[Widget Lifecycle](references/widget-lifecycle.md)** - Detailed explanation of initState, build, setState, dispose, and best practices for managing widget lifecycle

- **[Custom Widgets Example](examples/custom-widgets.md)** - Complete working example of building reusable custom widgets with proper composition

- **[Composition Patterns Example](examples/composition-patterns.md)** - Complete working example demonstrating how to build complex UIs through widget composition

## Related Skills

- **flutter-state-management** - Managing state across your Flutter app with Provider, Riverpod, Bloc, and other state management solutions
- **flutter-navigation** - Implementing navigation and routing patterns in Flutter apps
- **flutter-responsive-design** - Building responsive and adaptive UIs that work across different screen sizes and platforms
- **flutter-animations** - Creating smooth, performant animations in Flutter
- **flutter-theming** - Advanced theming techniques, dark mode, and custom theme creation
