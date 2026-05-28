---
name: idiomatic-flutter
description: Use this skill when you want to apply modern layout and widget composition standards in Flutter development.
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

- **Missing Mounted Check**: Always check `if (context.mounted)` before using context after an await.
- **Helper Methods for UI**: Avoid using widget functions; prefer specialized widget classes for better performance and profiling.
- **Direct Controller Access**: Decouple UI from state by using BLoC/Signals instead of direct controller access.