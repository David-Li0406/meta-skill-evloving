---
name: ios26-liquid-glass
description: Use this skill when building or reviewing SwiftUI and UIKit features that utilize the iOS 26+ Liquid Glass API, focusing on glass effects and Apple design guidelines.
---

# Skill body

Liquid Glass is Apple's design language introduced at WWDC 2025. Glass elements float above content with translucent, depth-aware surfaces that reflect and refract surrounding content.

## SwiftUI - glassEffect Modifier

```swift
func glassEffect<S: Shape>(
    _ glass: Glass = .regular,
    in shape: S = DefaultGlassEffectShape,
    isEnabled: Bool = true
) -> some View
```

Apply `.glassEffect()` **last** in your modifier chain for correct rendering.

### Glass Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| `.regular` | Default, balanced transparency | Most UI elements (buttons, controls, overlays) |
| `.clear` | High transparency, limited adaptivity | Media-rich backgrounds (needs dimming layer) |
| `.identity` | No effect applied | Conditional glass application |

### Glass Modifiers

```swift
// semantic color tinting - use only for meaning (success, warning, destructive)
.glassEffect(.regular.tint(.blue))

// iOS-only: enables scaling, bounce, shimmer on interaction
.glassEffect(.regular.interactive())

// combined
.glassEffect(.regular.tint(.blue).interactive())
```

### Shapes

```swift
// default shape (capsule)
.glassEffect()
.glassEffect(.regular, in: DefaultGlassEffectShape())

// built-in shapes
.glassEffect(.regular, in: .capsule)
.glassEffect(.regular, in: .circle)
.glassEffect(.regular, in: .ellipse)
.glassEffect(.regular, in: .rect(cornerRadius: 12))
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))

// adapts corner radius to parent container (for buttons in cards/sheets)
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))
```

## GlassEffectContainer

Groups multiple glass elements for seamless blending and morphing. **Glass cannot sample other glass**, so use this when elements are positioned closely.

```swift
GlassEffectContainer(spacing: 8) {  // spacing = merge threshold in points
    Button("One") { }
        .glassEffect()

    Button("Two") { }
        .glassEffect()
}
```

### Rules
- Don't nest `GlassEffectContainer` inside another.
- Don't place `Menu` inside `GlassEffectContainer`.

### Notes
- Prioritize native APIs (glassEffect, GlassEffectContainer, glass button styles) and Apple design guidance.
- Keep usage consistent, interactive where needed, and performance-aware.
- Provide AppKit Liquid Glass notes for macOS when requested.