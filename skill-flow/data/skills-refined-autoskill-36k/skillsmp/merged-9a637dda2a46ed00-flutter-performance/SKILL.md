---
name: flutter-performance
description: Use this skill when optimizing Flutter applications for rebuilds and memory efficiency.
---

# Performance Optimization

## **Priority: P1 (OPERATIONAL)**

Techniques for achieving smooth 60fps Flutter applications.

- **Rebuilds**: Use `const` widgets and `buildWhen` / `select` for granular updates.
- **Lists**: Always use `ListView.builder` for item recycling.
- **Heavy Tasks**: Use `compute()` or `Isolates` for parsing/logic.
- **Repaints**: Use `RepaintBoundary` for complex animations. Utilize `debugRepaintRainbowEnabled` for debugging.
- **Images**: Use `CachedNetworkImage` with `memCacheWidth` and `precachePicture` for SVGs.

## 🚫 Anti-Patterns

- **Large Rebuilds**: Avoid `SetState` at the root; use granular builders (e.g., BlocBuilder, Consumer).
- **Logic in Build**: Do not perform heavy work in the build method; handle parsing/sorting in the business layer.
- **Missing Const**: Avoid dynamic leaf widgets; use `const` where possible.

```dart
BlocBuilder<UserBloc, UserState>(
  buildWhen: (p, c) => p.id != c.id,
  builder: (context, state) => Text(state.name),
)
```