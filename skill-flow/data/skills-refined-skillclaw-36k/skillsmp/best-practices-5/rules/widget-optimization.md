---
title: Widget Optimization
impact: CRITICAL
impactDescription: Prevents unnecessary rebuilds, 2-10x performance
tags: widgets, const, rebuild, performance
---

# Widget Optimization

Minimize widget rebuilds for optimal performance.

## Rule 1: Use const Constructors Everywhere

```dart
// ❌ INCORRECT - recreated on every build
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Text('Hello'),
    );
  }
}

// ✅ CORRECT - const prevents recreation
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Text('Hello'),
    );
  }
}
```

## Rule 2: Split Widgets by Rebuild Scope

```dart
// ❌ INCORRECT - everything rebuilds when timer updates
class TimerPage extends StatefulWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Header(),           // rebuilds
        const ExpensiveChart(),   // rebuilds
        Text('Time: $seconds'),   // needs to rebuild
        const Footer(),           // rebuilds
      ],
    );
  }
}

// ✅ CORRECT - only timer widget rebuilds
class TimerPage extends StatelessWidget {
  const TimerPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        Header(),
        ExpensiveChart(),
        TimerDisplay(),  // only this is StatefulWidget
        Footer(),
      ],
    );
  }
}
```

## Rule 3: Use Keys for Dynamic Lists

```dart
// ❌ INCORRECT - items may not update correctly
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(item: items[index]);
  },
)

// ✅ CORRECT - keyed for proper identity
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(
      key: ValueKey(items[index].id),
      item: items[index],
    );
  },
)
```

## Rule 4: Prefer StatelessWidget Over StatefulWidget

```dart
// ❌ INCORRECT - unnecessary state
class GreetingWidget extends StatefulWidget {
  final String name;
  const GreetingWidget({super.key, required this.name});

  @override
  State<GreetingWidget> createState() => _GreetingWidgetState();
}

class _GreetingWidgetState extends State<GreetingWidget> {
  @override
  Widget build(BuildContext context) {
    return Text('Hello, ${widget.name}');
  }
}

// ✅ CORRECT - stateless is simpler and faster
class GreetingWidget extends StatelessWidget {
  final String name;
  const GreetingWidget({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name');
  }
}
```

## Rule 5: Use Builder for Localized Rebuilds

```dart
// ❌ INCORRECT - entire widget rebuilds on theme change
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);  // subscribes entire widget
    return Column(
      children: [
        const ExpensiveWidget(),
        Text('Themed', style: theme.textTheme.bodyLarge),
      ],
    );
  }
}

// ✅ CORRECT - only themed text rebuilds
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        ExpensiveWidget(),
        ThemedText(),
      ],
    );
  }
}

class ThemedText extends StatelessWidget {
  const ThemedText({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Text('Themed', style: theme.textTheme.bodyLarge);
  }
}
```

## Rule 6: Use RepaintBoundary for Animations

```dart
// ❌ INCORRECT - animation causes parent repaint
Column(
  children: [
    StaticContent(),
    SpinningLoader(),  // causes entire column to repaint
  ],
)

// ✅ CORRECT - isolated repaint
Column(
  children: [
    const StaticContent(),
    const RepaintBoundary(
      child: SpinningLoader(),  // only this area repaints
    ),
  ],
)
```
