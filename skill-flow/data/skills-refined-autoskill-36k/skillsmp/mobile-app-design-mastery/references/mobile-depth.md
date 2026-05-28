# Mobile Depth & Elevation

Depth principles for mobile apps with platform-specific guidance.

---

## Platform Approaches

| Platform | Depth Style |
|----------|-------------|
| iOS | Subtle shadows, blur/frosted glass, minimal elevation |
| Android | Material elevation, layered surfaces, distinct shadows |
| Cross-platform | Pick one system and be consistent |

---

## Android Elevation Scale

Material Design defines elevation in dp:

| Component | Elevation | Shadow |
|-----------|-----------|--------|
| Flat surfaces | 0dp | None |
| Cards, tiles | 1-2dp | Subtle |
| Raised buttons | 2-4dp | Small |
| App bar | 4dp | Medium |
| FAB (resting) | 6dp | Medium-large |
| Bottom sheet | 8dp | Large |
| Nav drawer | 16dp | Very large |
| Modal dialog | 24dp | Maximum |

**Interaction:** FAB pressed = 12dp (lifts on press, unlike web).

---

## iOS Depth Approach

iOS uses less elevation, more material treatment:

- **Blur effects:** frostedGlass, regular, thin materials
- **Shadows:** Subtle, softer than Material
- **Layering:** Sheet presentations, not explicit elevation

**Shadows when used:**

```dart
BoxShadow(
  color: Colors.black.withOpacity(0.1),
  blurRadius: 10,
  offset: Offset(0, 2),
)
```

---

## Creating Depth Without Shadows

Useful for flat design or performance:

- **Background color difference:** Card lighter/darker than background
- **Border:** Subtle 1px border in gray-200/gray-700
- **Spacing:** More padding around elevated content

---

## Overlapping Elements

Creates visual layers:

- Cards extending below app bar
- Carousel controls overlapping edges
- Floating action button overlapping content/app bar junction

**Technique:** Use negative margins or absolute positioning.

---

## Bottom Sheets & Modals

Highest elevation elements:

- **Bottom sheet:** Rounded top corners, shadow upward
- **Modal dialog:** Centered, background scrim (50% opacity)
- **Drawer:** Full-height, shadow toward content

**Scrim:** Semi-transparent overlay (black at 50%) behind elevated content.
