---
name: swiftui-liquid-glass
description: Use this skill when implementing, reviewing, or improving SwiftUI features with the iOS 26+ Liquid Glass API.
---

# SwiftUI Liquid Glass

## Overview
Utilize this skill to build or review SwiftUI features that align with the iOS 26+ Liquid Glass API. Focus on native APIs (`glassEffect`, `GlassEffectContainer`, glass button styles) and adhere to Apple design guidelines. Ensure consistent usage, interactivity where necessary, and performance optimization.

## Workflow Decision Tree
Choose the path that matches the request:

### 1) Review an existing feature
- Inspect where Liquid Glass should be applied and where it should not.
- Verify correct modifier order, shape usage, and container placement.
- Check for iOS 26+ availability handling and sensible fallbacks.

### 2) Improve a feature using Liquid Glass
- Identify target components for glass treatment (surfaces, chips, buttons, cards).
- Refactor to use `GlassEffectContainer` for multiple glass elements.
- Introduce interactive glass only for tappable or focusable elements.

### 3) Implement a new feature using Liquid Glass
- Design glass surfaces and interactions first (shape, prominence, grouping).
- Add glass modifiers after layout/appearance modifiers.
- Introduce morphing transitions only when the view hierarchy changes with animation.

## Core Guidelines
- Prefer native Liquid Glass APIs over custom blurs.
- Use `GlassEffectContainer` when multiple glass elements coexist.
- Apply `.glassEffect(...)` after layout and visual modifiers.
- Use `.interactive()` for elements that respond to touch/pointer.
- Maintain consistent shapes across related elements for a cohesive look.
- Gate with `#available(iOS 26, *)` and provide a non-glass fallback.

## Review Checklist
- **Availability**: Ensure `#available(iOS 26, *)` is present with fallback UI.
- **Composition**: Verify multiple glass views are wrapped in `GlassEffectContainer`.
- **Modifier order**: Confirm `glassEffect` is applied after layout/appearance modifiers.
- **Interactivity**: Check `interactive()` is used only where user interaction exists.
- **Transitions**: Ensure `glassEffectID` is used with `@Namespace` for morphing.
- **Consistency**: Align shapes, tinting, and spacing across the feature.

## Implementation Checklist
- Define target elements and desired glass prominence.
- Wrap grouped glass elements in `GlassEffectContainer` and adjust spacing.
- Use `.glassEffect(.regular.tint(...).interactive(), in: .rect(cornerRadius: ...))` as needed.
- Apply `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` for actions.
- Add morphing transitions with `glassEffectID` when hierarchy changes.
- Provide fallback materials and visuals for earlier iOS versions.

## Quick Snippets
Use these patterns directly and customize shapes/tints/spacing.

```swift
if #available(iOS 26, *) {
    Text("Hello")
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    Text("Hello")
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}
```

```swift
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        Image(systemName: "scribble.variable")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
        Image(systemName: "eraser.fill")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
    }
}
```

```swift
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

## Resources
- Reference guide: `references/liquid-glass.md`
- Prefer Apple documentation for the most up-to-date API details and design guidance.