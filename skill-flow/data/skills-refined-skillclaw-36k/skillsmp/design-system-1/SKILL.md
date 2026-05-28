---
name: design-system
description: RemoteViewer.Client design system with spacing, colors, typography, and components. Use when building UI, styling components, or working with Avalonia XAML.
---

# Design System

The client uses a comprehensive design system with markup extensions, design tokens, and reusable components. All UI should use these tokens instead of hardcoded values.

## Markup Extensions

Located in `Themes/` folder. Add `xmlns:theme="using:RemoteViewer.Client.Themes"` to use.

### Spacing (Margin/Padding)
```xml
Padding="{theme:Spacing MD}"              <!-- All sides: 12 -->
Margin="{theme:Spacing X=LG, Y=SM}"       <!-- Horizontal: 16, Vertical: 8 -->
Margin="{theme:Spacing Top=XL, Right=MD}" <!-- Individual sides -->
```

Values: `None=0, XXS=2, XS=4, SM=8, MD=12, LG=16, XL=24, XXL=32`

The same extension works for `Spacing` (double) and `GridLength` properties:
```xml
<StackPanel Spacing="{theme:Spacing SM}">           <!-- 8px between items -->
<ColumnDefinition Width="{theme:Spacing SM}"/>      <!-- 8px spacer column -->
```

## Design Tokens

### Colors (use DynamicResource for theme support)
- **Muted text**: `SystemControlDisabledBaseMediumLowBrush` (Avalonia built-in)
- **Accent**: `AccentButtonBackground`, `AccentButtonForeground` (Avalonia built-in)
- **Surfaces**: `SurfaceElevatedBrush`, `SurfaceOverlayBrush`, `CardBackgroundBrush`
- **Semantic**: `SuccessBrush`, `ErrorBrush`, `WarningBrush`

## Typography Classes

Apply via `Classes="class-name"` on TextBlock:

- **Headings**: `h1` (22px Bold), `h2` (15px SemiBold), `h3` (13px SemiBold)
- **Small text**: `m1` (12px), `m2` (10px)
- **Special**: `credential` (18px Bold monospace)
- **Color modifier**: `muted`

## Button Styles

All buttons automatically get `CornerRadius="6"` from the base style.

```xml
<Button>                             <!-- Default button (uses Avalonia defaults) -->
<Button Classes="accent">            <!-- Accent/primary button (Avalonia built-in) -->
<Button Classes="icon-button">       <!-- 32x32 transparent icon button for toolbars -->
```

## Card Component (Controls/Card.axaml)

A flexible card container with size options.

```xml
<controls:Card>                <!-- Default: 8px radius, 14px padding -->
<controls:Card Size="Large">   <!-- 12px radius, 16px padding -->
<controls:Card Size="XLarge">  <!-- 20px radius, 32x28 padding (for overlays) -->
<controls:Card Size="ListItem"><!-- Uses SurfaceOverlayBrush background -->
```

## Icon Component (Controls/Icon.axaml)

A unified icon control with optional badge mode.

```xml
<controls:Icon Kind="Check" Size="MD"/>                    <!-- 24px icon -->
<controls:Icon Kind="Check" Size="LG" ShowAsBadge="True"/> <!-- Icon in circular badge -->
```

**Properties:**
- `Kind`: MaterialIconKind enum value
- `Size`: XXS (12px), XS (16px), SM (20px), MD (24px), LG (32px), XL (40px), XXL (48px)
- `ShowAsBadge`: When true, displays icon in a circular background
- `BadgeBackground`: Custom badge background brush (defaults to `BadgeBackgroundBrush`)

## Components

- **Card**: Flexible container with size options (`Controls/Card.axaml`)
- **Icon**: Unified icon with size presets and optional badge mode (`Controls/Icon.axaml`)
- **DialogHeader**: Standardized dialog header with icon, title, subtitle (`Controls/DialogHeader.axaml`)
