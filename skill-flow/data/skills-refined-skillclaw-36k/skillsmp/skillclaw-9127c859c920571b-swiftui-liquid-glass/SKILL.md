---
name: swiftui-liquid-glass
description: Use this skill when implementing, reviewing, or improving SwiftUI features with the iOS 26+ Liquid Glass API, ensuring design alignment and performance.
---

# SwiftUI Liquid Glass

## Overview
Use this skill to build or review SwiftUI features that fully align with the iOS 26+ Liquid Glass API. Prioritize native APIs (`glassEffect`, `GlassEffectContainer`, glass button styles) and Apple design guidance. Keep usage consistent, interactive where needed, and performance aware.

## Workflow Decision Tree
Choose the path that matches the request:

### 1) Review an existing feature
- Inspect where Liquid Glass should be used and where it should not.
- Verify correct modifier order, shape usage, and container placement.
- Check for iOS 26+ availability handling and sensible fallbacks.

### 2) Improve a feature using Liquid Glass
- Identify target components for glass treatment (surfaces, chips, buttons, cards).
- Refactor to use `GlassEffectContainer` where multiple glass elements appear.
- Introduce interactive glass only for tappable or focusable elements.

### 3) Implement a new feature using Liquid Glass
- Design the glass surfaces and interactions first (shape, prominence, grouping).
- Add glass modifiers after layout/appearance modifiers.
- Add morphing transitions only when the view hierarchy changes with animation.

## Core Guidelines
- Prefer native Liquid Glass APIs over custom blurs.
- Use `GlassEffectContainer` when multiple glass elements coexist.
- Apply `.glassEffect(...)` after layout and visual modifiers.
- Use `.interactive()` for elements that respond to touch/pointer.
- Keep shapes consistent across related elements for a cohesive look.
- Gate with `#available(iOS 26, *)` and provide a non-glass fallback.

## Review Checklist
- **Availability**: Ensure `#available(iOS 26, *)` is present with fallback UI.
- **Composition**: Verify multiple glass views are wrapped in `GlassEffectContainer`.
- **Modifier order**: Confirm `glassEffect` is applied after layout/appearance modifiers.
- **Interactivity**: Check that `interactive()` is used only where user interaction exists.
- **Transitions**: Use `glassEffectID` with `@Namespace` for morphing.
- **Consistency**: Ensure shapes, tinting, and spacing align across the feature.

## Implementation Checklist
- Define target elements and desired glass prominence.
- Wrap grouped glass elements in `GlassEffectContainer`.