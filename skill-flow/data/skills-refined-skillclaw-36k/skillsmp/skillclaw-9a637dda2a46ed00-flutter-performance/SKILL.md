---
name: flutter-performance
description: Use this skill when you need to optimize Flutter applications for rebuilds and memory management to achieve smooth performance.
---

# Performance Optimization Techniques

## **Priority: P1 (OPERATIONAL)**

To ensure your Flutter applications run smoothly at 60fps, follow these performance optimization techniques:

### Best Practices

- **Rebuilds**: 
  - Use `const` widgets to prevent unnecessary rebuilds.
  - Implement `buildWhen` or `select` for granular updates in state management.

- **Lists**: 
  - Always utilize `ListView.builder` for efficient item recycling.

- **Heavy Tasks**: 
  - Offload heavy computations using `compute()` or `Isolates` to keep the UI responsive.

- **Repaints**: 
  - Use `RepaintBoundary` for complex animations to minimize repaint areas.
  - Enable `debugRepaintRainbowEnabled` to identify repaint issues during development.

- **Images**: 
  - Use `CachedNetworkImage` with `memCacheWidth` for efficient image loading.
  - Use `precachePicture` for SVGs to improve rendering performance.

### Anti-Patterns to Avoid

- **Large Rebuilds**: 
  - Avoid using `setState` at the root level. Instead, use granular builders like `BlocBuilder` or `Consumer`.

- **Logic in Build**: 
  - Do not perform heavy work in the build method. Move parsing and sorting to the business layer.

- **Missing Const**: 
  - Avoid dynamic leaf widgets. Use `const` wherever possible to enhance performance.

### Example Code

```dart
BlocBuilder<UserBloc, UserState>(
  buildWhen: (previous, current) => previous.id != current.id,
  builder: (context, state) => Text(state.name),
)
```