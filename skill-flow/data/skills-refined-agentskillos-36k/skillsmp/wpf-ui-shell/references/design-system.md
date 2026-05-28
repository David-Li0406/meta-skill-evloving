# Fluent-Inspired Design System

## Principles

- Soft surfaces, subtle elevation, and clear focus states.
- Typography-driven hierarchy with consistent spacing.
- Use native WPF styles, templates, and brushes.

## Resource keys

Prefer explicit resource keys for consistency:

```
Brushes/Surface
Brushes/SurfaceAlt
Brushes/Accent
Typography/Body
Typography/Title
```

## Control styling

- Define base styles for `Button`, `TextBox`, `ListBox`, `ToggleButton`.
- Use control templates only when necessary; start with setters.
- Keep focus visuals visible and consistent across controls.

## Iconography

- Use a single icon set and map to `Geometry` resources.
- Keep icons at consistent visual weight and size.
