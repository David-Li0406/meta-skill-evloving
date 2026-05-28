---
name: frontend-design
description: Create UI components following this Expo template's design system. Use when building components, screens, or interfaces for this React Native project.
---

This skill guides creation of UI components for this Expo React Native template. Follow these patterns for consistent, theme-aware, cross-platform components.

## Quick Start

Essential imports for any UI component:

```tsx
import { View, StyleSheet, Platform } from "react-native";
import { useTheme } from "@/client/hooks/useTheme";
import { spacing } from "@/client/constants/spacing";
import type { Theme } from "@/client/constants/colors";
```

## Theming System

### useTheme() Hook

Central access point for all theming:

```tsx
const { theme, scheme, getShadowStyle, getContrastingColor, withAlpha } = useTheme();

// Access semantic colors
backgroundColor: theme.colors.background
color: theme.colors.foreground
borderColor: theme.colors.border

// Cross-platform shadows
const shadow = getShadowStyle("soft"); // "base" | "soft" | "sharp" | "subtle"

// Color utilities
const textColor = getContrastingColor(bgColor, palette.white, palette.black);
const fadedColor = withAlpha(theme.colors.primary, 0.5);
```

### Semantic Colors (99% of usage)

| Color | Purpose |
|-------|---------|
| `background` / `foreground` | Page background and primary text |
| `card` / `cardForeground` | Card surfaces and text |
| `primary` / `primaryForeground` | Brand color and text on it |
| `secondary` / `secondaryForeground` | Secondary actions |
| `muted` / `mutedForeground` | Subtle backgrounds and placeholder text |
| `destructive` / `destructiveForeground` | Error/danger states |
| `success` / `warning` | Status colors |
| `border` | Borders and dividers |
| `overlay` | Modal overlays |

### Palette (Only for Contrast Calculations)

```tsx
import { palette } from "@/client/constants/colors";

// ONLY use palette for WCAG contrast calculations
const textColor = getContrastingColor(bgColor, palette.white, palette.black);

// NEVER use palette for regular styling - use theme.colors instead
```

## Spacing System

8px-based scale from `@/client/constants/spacing`:

| Token | Value | Token | Value |
|-------|-------|-------|-------|
| `xxs` | 2px | `radiusXs` | 2px |
| `xs` | 4px | `radiusSm` | 4px |
| `sm` | 8px | `radiusMd` | 8px |
| `md` | 16px | `radiusLg` | 12px |
| `lg` | 24px | `radiusXl` | 16px |
| `xl` | 32px | `radiusFull` | 9999px |
| `xxl` | 48px | | |

Icon sizes: `iconXs` (12), `iconSm` (16), `iconMd` (24), `iconLg` (32), `iconXl` (48)

## Typography

### StyledText Components

```tsx
import { SansSerifText, SansSerifBoldText, SerifText } from "@/client/components/ui/StyledText";

// Semantic shortcuts
import { TitleText, HeadingText, BodyText, CaptionText } from "@/client/components/ui/StyledText";
```

Font families: `Lato_400Regular`, `Lato_700Bold`, `Merriweather_400Regular`, `Merriweather_700Bold`

## Styling Patterns

### StyleSheet Factory Pattern

```tsx
const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      backgroundColor: theme.colors.card,
      borderRadius: spacing.radiusMd,
      borderWidth: 1,
      borderColor: theme.colors.border,
      padding: spacing.md,
    },
  });

// In component
const { theme } = useTheme();
const styles = createStyles(theme);
```

### CRITICAL: React Native Web Nested Array Fix

React Native Web crashes with nested style arrays. Use these patterns:

**Solution 1: Spread Arrays** (for simple components)
```tsx
function Component({ style: styleOverride, ...props }) {
  return (
    <View
      style={[
        styles.base,
        ...(styleOverride && typeof styleOverride !== "function"
          ? Array.isArray(styleOverride) ? styleOverride : [styleOverride]
          : []),
      ]}
    />
  );
}
```

**Solution 2: Plain Objects with Flatten** (REQUIRED for @rn-primitives menu components)
```tsx
function MenuComponent({ style: styleOverride, ...props }) {
  return (
    <Primitive
      style={{
        ...baseStyle,
        ...(styleOverride && typeof styleOverride !== "function"
          ? StyleSheet.flatten(styleOverride)
          : {}),
      }}
    />
  );
}
```

### Platform-Specific Styling

```tsx
// Pointer cursor for interactive elements on web
...(Platform.OS === "web" && { cursor: "pointer" as any }),

// Z-index for web overlays
...(Platform.OS === "web" && { zIndex: 50 }),

// Remove focus outline on web
...(Platform.OS === "web" && { outlineStyle: "none" as any }),
```

## Component Patterns

### Size Variants

```tsx
type ComponentSize = "sm" | "md" | "lg";

const SIZE_CONFIGS: Record<ComponentSize, { height: number; fontSize: number }> = {
  sm: { height: 28, fontSize: 13 },
  md: { height: 32, fontSize: 14 },
  lg: { height: 36, fontSize: 15 },
};
```

### Preset/Variant Pattern

```tsx
type ButtonPreset = "default" | "outline" | "ghost" | "link" | "destructive";
```

### Composition Over Props

```tsx
// PREFERRED - flexible composition
<Button onPress={handler}>
  <SansSerifBoldText>Click Me</SansSerifBoldText>
</Button>

// Components accept children, not just text props
```

### @rn-primitives Integration

For complex interactive components, use `@rn-primitives`:

```tsx
import * as CheckboxPrimitive from "@rn-primitives/checkbox";

function Checkbox({ checked, onCheckedChange, style: styleOverride }) {
  const { theme } = useTheme();

  return (
    <CheckboxPrimitive.Root
      checked={checked}
      onCheckedChange={onCheckedChange}
      style={{
        borderColor: theme.colors.border,
        ...(Platform.OS === "web" && { cursor: "pointer" as any }),
        ...(styleOverride && typeof styleOverride !== "function"
          ? StyleSheet.flatten(styleOverride)
          : {}),
      }}
    >
      <CheckboxPrimitive.Indicator>
        <Icon as={Check} color={theme.colors.primary} />
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  );
}
```

## Component Development Checklist

- [ ] Extract `style` prop separately to avoid nested arrays
- [ ] Use `useTheme()` hook for all colors
- [ ] Import and use `spacing` constants (never hardcode)
- [ ] Add `cursor: "pointer"` for interactive elements on web
- [ ] Handle both light and dark themes
- [ ] Test on web for nested array crashes
- [ ] Run `npx tsc` to check TypeScript
- [ ] Add to showcase in `app/(main)/showcase.tsx`
- [ ] Consider `@rn-primitives` for complex interactive components
- [ ] Include accessibility attributes (`accessibilityRole`, etc.)

## Full Component Example

```tsx
import { View, Pressable, StyleSheet, Platform, type StyleProp, type ViewStyle } from "react-native";
import { useTheme } from "@/client/hooks/useTheme";
import { spacing } from "@/client/constants/spacing";
import { SansSerifText } from "@/client/components/ui/StyledText";
import type { Theme } from "@/client/constants/colors";

interface MyCardProps {
  title: string;
  description?: string;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
}

export function MyCard({ title, description, onPress, style: styleOverride }: MyCardProps) {
  const { theme, getShadowStyle } = useTheme();
  const styles = createStyles(theme);
  const shadowStyle = StyleSheet.flatten(getShadowStyle("soft"));

  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      style={({ pressed }) => [
        styles.container,
        shadowStyle,
        pressed && styles.pressed,
        ...(styleOverride && typeof styleOverride !== "function"
          ? Array.isArray(styleOverride) ? styleOverride : [styleOverride]
          : []),
      ]}
    >
      <SansSerifText style={styles.title}>{title}</SansSerifText>
      {description && (
        <SansSerifText style={styles.description}>{description}</SansSerifText>
      )}
    </Pressable>
  );
}

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      backgroundColor: theme.colors.card,
      borderRadius: spacing.radiusMd,
      borderWidth: 1,
      borderColor: theme.colors.border,
      padding: spacing.md,
      ...(Platform.OS === "web" && { cursor: "pointer" as any }),
    },
    pressed: {
      opacity: 0.8,
    },
    title: {
      fontSize: 16,
      fontWeight: "600",
      color: theme.colors.cardForeground,
      marginBottom: spacing.xs,
    },
    description: {
      fontSize: 14,
      color: theme.colors.mutedForeground,
    },
  });
```
