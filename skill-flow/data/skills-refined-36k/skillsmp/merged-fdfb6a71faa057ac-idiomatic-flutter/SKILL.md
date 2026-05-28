---
name: idiomatic-flutter
description: Use this skill when implementing modern layout and widget composition standards in Flutter applications.
---

# Idiomatic Flutter

## **Priority: P1 (OPERATIONAL)**

Modern Flutter layout patterns and composition techniques.

- **Async Gaps**: Check `if (context.mounted)` before using `BuildContext` after `await`.
- **Composition**: Extract complex UI into small widgets. Avoid deep nesting or large helper methods.
- **Layout**:
  - Spacing: Use `Gap(n)` or `SizedBox` over `Padding` for simple gaps.
  - Empty UI: Use `const SizedBox.shrink()`.
  - Intrinsic: Avoid `IntrinsicWidth/Height`; use `Stack` + `FractionallySizedBox` for overlays.
- **Optimization**: Use `ColoredBox`/`Padding`/`DecoratedBox` instead of `Container` when possible.
- **Themes**: Use extensions for `Theme.of(context)` access.

## 🚫 Anti-Patterns

- **Missing Mounted Check**: Always check `if (context.mounted)` before using context after await.
- **Helper Methods for UI**: Use specialized Widget classes for better performance/profiling instead of widget functions.
- **Direct Controller Access**: Use BLoC/Signals to decouple UI from State and avoid UI-Logic coupling.