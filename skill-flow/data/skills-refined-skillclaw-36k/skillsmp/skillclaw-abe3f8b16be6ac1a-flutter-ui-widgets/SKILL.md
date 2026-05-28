---
name: flutter-ui-widgets
description: Use this skill when you need to build maintainable and performant UI components in Flutter.
---

# UI & Widgets

## **Priority: P1 (OPERATIONAL)**

Standards for building reusable, performant Flutter widgets and UI components.

- **State**: Use `StatelessWidget` by default. `StatefulWidget` only for local state/controllers.
- **Composition**: Extract UI into small, atomic `const` widgets.
- **Theming**: Use `Theme.of(context)`. No hardcoded colors.
- **Layout**: Use `Flex` + `Gap/SizedBox`.
- **Specialized**:
  - `SelectionArea`: For multi-widget text selection.
  - `InteractiveViewer`: For zoom/pan.
  - `ListWheelScrollView`: For pickers.
  - `IntrinsicWidth/Height`: Avoid unless strictly required.
- **Large Lists**: Always use `ListView.builder`.

```dart
class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  const AppButton({super.key, required this.label, required this.onPressed});

  @override
  Widget build(BuildContext context) => ElevatedButton(onPressed: onPressed, child: Text(label));
}
```

## Related Topics

performance | testing