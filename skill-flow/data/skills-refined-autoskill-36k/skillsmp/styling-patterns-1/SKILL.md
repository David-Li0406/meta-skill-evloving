---
name: styling-patterns
description: "WHAT: Zest design tokens with useZestStyles and createStylesConfig for React Native styling. WHEN: component styling, layout composition, conditional styles, platform-specific shadows. KEYWORDS: createStylesConfig, useZestStyles, useZestTheme, design tokens, alias, global, spacing, borderRadius, colors."
---

# Styling Patterns with Zest Design System

## Core Principles

**Follow the styling hierarchy: Zest components → useZestStyles → useZestTheme.** Use design tokens for all values and extract style configs outside components for performance.

**Why**: Zest provides consistent theming, accessibility, responsive design, and automatic platform adaptations across the app.

## When to Use This Skill

Use these patterns when:

- Styling any React Native component
- Creating custom layouts or compositions
- Implementing responsive designs
- Handling platform-specific styling (iOS vs Android)
- Applying conditional or dynamic styles
- Ensuring consistent spacing and colors
- Building theme-aware interfaces

## The Styling Hierarchy

### Level 1: Zest Components with Variants (Preferred)

Always start with built-in Zest components and variants:

```typescript
import { Button, Text, View } from '@zest/react-native';

export const RecipeCard = ({ recipe, onAdd }: Props) => {
  return (
    <View>
      <Text type="headline-lg">{recipe.name}</Text>
      <Text type="body-md-regular">{recipe.description}</Text>
      <Button
        variant="primary"
        size="lg"
        appearance="brand"
        onPress={onAdd}
      >
        Add to Cart
      </Button>
    </View>
  );
};
```

**Why**: Zest components handle responsive design, accessibility, theming, and platform differences automatically.

### Level 2: useZestStyles for Custom Layouts

Use `createStylesConfig` and `useZestStyles` for custom layouts:

```typescript
import { createStylesConfig, useZestStyles } from '@zest/react-native';

export const stylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
    borderRadius: 'global.borderRadius.md',
    gap: 'global.spacing.sm',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    color: 'alias.color.neutral.foreground.default',
  },
  // Callback pattern for computed/negative values
  sectionContainer: {
    marginTop: 'global.spacing.sm1',
    marginHorizontal: (theme) => -theme.global.spacing.xs,
  },
});

export const RecipeCard = ({ recipe }: Props) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{recipe.name}</Text>
        <FavoriteButton recipeId={recipe.id} />
      </View>
      <Text type="body-md-regular">{recipe.description}</Text>
    </View>
  );
};
```

**Why**: `createStylesConfig` provides type-safe token access and theme integration.

**Key point**: Extract `stylesConfig` outside the component to prevent re-creation on every render.

**Callback pattern**: Use `(theme) => value` for computed values like negative margins.

### Level 3: useZestTheme for Dynamic Values

Use `useZestTheme` only for computed or conditional styles:

```typescript
import { useZestTheme } from '@zest/react-native';
import { useMemo } from 'react';

export const RecipeCard = ({ recipe, isActive }: Props) => {
  const theme = useZestTheme();
  const styles = useZestStyles(stylesConfig);

  const dynamicStyle = useMemo(() => ({
    backgroundColor: isActive
      ? theme.alias.color.brand.background.default
      : theme.alias.color.neutral.background.subtle,
    borderWidth: isActive ? 2 : 1,
    borderColor: isActive
      ? theme.alias.color.brand.border.default
      : theme.alias.color.neutral.border.default,
  }), [theme, isActive]);

  return (
    <View style={[styles.container, dynamicStyle]}>
      <Text style={styles.title}>{recipe.name}</Text>
    </View>
  );
};
```

**Why**: Direct theme access is needed for runtime-computed styles that can't be pre-defined.

**Important**: Always memoize dynamic styles with `useMemo` to prevent object recreation on every render.

## Design Tokens

### Color Tokens

Use alias color tokens for semantic meaning:

```typescript
export const stylesConfig = createStylesConfig({
  // Backgrounds
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
  },
  activeContainer: {
    backgroundColor: 'alias.color.brand.background.default',
  },
  errorContainer: {
    backgroundColor: 'alias.color.semantic.error.background.default',
  },
  subtleContainer: {
    backgroundColor: 'alias.color.neutral.background.subtle',
  },

  // Foregrounds (text and icons)
  text: {
    color: 'alias.color.neutral.foreground.default',
  },
  subtleText: {
    color: 'alias.color.neutral.foreground.subtle',
  },
  brandText: {
    color: 'alias.color.brand.foreground.default',
  },
  inverseText: {
    color: 'alias.color.neutral.foreground.inverse',
  },

  // Borders
  border: {
    borderColor: 'alias.color.neutral.border.default',
    borderWidth: 1,
  },
  brandBorder: {
    borderColor: 'alias.color.brand.border.default',
    borderWidth: 2,
  },
});
```

**Color token structure:**
- `alias.color.{semantic}.{element}.{variant}`
- Semantic: `neutral`, `brand`, `semantic.error`, `semantic.success`
- Element: `background`, `foreground`, `border`
- Variant: `default`, `subtle`, `inverse`

**Why**: Alias colors adapt to theme changes and provide semantic meaning.

### Spacing Tokens

Use global spacing tokens for consistent layout:

```typescript
export const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',           // 16px - most common
    paddingHorizontal: 'global.spacing.md',
    gap: 'global.spacing.sm',               // 8px - very common for gaps
    marginBottom: 'global.spacing.lg',      // 24px
  },
  compactContainer: {
    padding: 'global.spacing.sm2',          // 12px - frequently used
    gap: 'global.spacing.xs',               // 4px
  },
  spaciousContainer: {
    padding: 'global.spacing.xl',           // 32px
    gap: 'global.spacing.md',
  },
});
```

**Available spacing tokens (by usage frequency):**

| Token | Value | Usage |
|-------|-------|-------|
| `global.spacing.md` | 16px | Most common padding |
| `global.spacing.sm` | 8px | Very common for gaps |
| `global.spacing.sm2` | 12px | Frequently used |
| `global.spacing.xs` | 4px | Compact spacing |
| `global.spacing.xxs` | 2px | Minimal spacing |
| `global.spacing.lg` | 24px | Large spacing |
| `global.spacing.xl` | 32px | Extra large spacing |
| `global.spacing.xxl` | 48px | Spacious layouts |

**Why**: Spacing tokens ensure consistent visual rhythm. The `sm2` token (12px) is used extensively for intermediate spacing needs between `sm` and `md`.

### Border Radius Tokens

Use border radius tokens for consistent roundness:

```typescript
export const stylesConfig = createStylesConfig({
  card: {
    borderRadius: 'global.borderRadius.md',    // 8px - cards
  },
  button: {
    borderRadius: 'global.borderRadius.lg',    // 12px - buttons
  },
  badge: {
    borderRadius: 'global.borderRadius.full',  // 9999px - pills
  },
  input: {
    borderRadius: 'global.borderRadius.sm',    // 4px - inputs
  },
});
```

**Available border radius tokens:**

- `global.borderRadius.sm` - 4px (inputs, small elements)
- `global.borderRadius.md` - 8px (cards, containers)
- `global.borderRadius.lg` - 12px (buttons, prominent elements)
- `global.borderRadius.xl` - 16px (large elements)
- `global.borderRadius.full` - 9999px (circular/pill shapes)

**Why**: Consistent border radius creates cohesive visual design.

### Typography Tokens

Use typography tokens for text sizing and hierarchy:

```typescript
export const stylesConfig = createStylesConfig({
  headline: {
    fontSize: 'global.fontSize.headline.headlineXl',           // 32px
    fontWeight: 700,
    lineHeight: 'global.lineHeight.xl',                        // 40px
    fontFamily: 'global.fontFamily.headline',
  },
  body: {
    fontSize: 'global.fontSize.body.bodyMd',                   // 16px
    fontWeight: 400,
    lineHeight: 'global.lineHeight.md',                        // 24px
    fontFamily: 'global.fontFamily.bodyRegular',
  },
  caption: {
    fontSize: 'global.fontSize.body.bodyXs',                   // 12px
    fontWeight: 400,
    lineHeight: 'global.lineHeight.sm',                        // 16px
    fontFamily: 'global.fontFamily.bodyRegular',
  },
});
```

**Typography token structure:**
- Font size: `global.fontSize.{category}.{size}`
- Line height: `global.lineHeight.{size}`
- Font family: `global.fontFamily.{style}`

**Why**: Typography tokens ensure consistent text sizing, hierarchy, and readability.

## Platform-Specific Styling

### Shadows with Platform.select()

Use `Platform.select()` for platform-specific implementations:

```typescript
import { Platform } from 'react-native';
import { createStylesConfig } from '@zest/react-native';

export const stylesConfig = createStylesConfig({
  card: {
    backgroundColor: 'alias.color.neutral.background.default',
    borderRadius: 'global.borderRadius.md',
    padding: 'global.spacing.md',
    ...Platform.select({
      ios: {
        shadowColor: 'alias.color.neutral.foreground.default',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 2,
      },
    }),
  },
});
```

**Why**: iOS uses shadow properties while Android uses elevation. `Platform.select()` applies the correct styling for each platform.

## Conditional Styling

### Style Arrays for Multiple Conditions

Use style arrays to combine base and conditional styles:

```typescript
export const RecipeCard = ({ recipe, isSelected, isFeatured }: Props) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={[
      styles.container,
      isSelected && styles.selectedContainer,
      isFeatured && styles.featuredContainer,
      !recipe.available && styles.disabledContainer,
    ]}>
      <Text style={[
        styles.title,
        isSelected && styles.selectedText,
      ]}>
        {recipe.name}
      </Text>
    </View>
  );
};

export const stylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
    borderRadius: 'global.borderRadius.md',
    borderWidth: 1,
    borderColor: 'alias.color.neutral.border.default',
  },
  selectedContainer: {
    backgroundColor: 'alias.color.brand.background.subtle',
    borderWidth: 2,
    borderColor: 'alias.color.brand.border.default',
  },
  featuredContainer: {
    backgroundColor: 'alias.color.semantic.success.background.subtle',
  },
  disabledContainer: {
    opacity: 0.5,
  },
  title: {
    color: 'alias.color.neutral.foreground.default',
  },
  selectedText: {
    color: 'alias.color.brand.foreground.default',
    fontWeight: 'bold',
  },
});
```

**Why**: Style arrays enable flexible conditional styling without creating new objects on every render. React Native applies styles from left to right, with later styles overriding earlier ones.

## Layout Patterns

### Flexbox with Gap

Use Flexbox with `gap` for responsive layouts:

```typescript
export const stylesConfig = createStylesConfig({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 'global.spacing.sm',
  },
  spaceBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  column: {
    flexDirection: 'column',
    gap: 'global.spacing.md',
  },
});
```

**Why**:
- Flexbox provides flexible, responsive layouts
- `gap` provides cleaner spacing than individual margins
- No need to apply margins to individual children

### Responsive Design

Use `useWindowDimensions` for screen-size responsive layouts:

```typescript
import { useWindowDimensions } from 'react-native';

export const RecipeGrid = ({ recipes }: Props) => {
  const { width } = useWindowDimensions();
  const styles = useZestStyles(stylesConfig);

  const numColumns = width > 768 ? 3 : 2;

  return (
    <FlatList
      data={recipes}
      numColumns={numColumns}
      key={numColumns} // Force re-render on column change
      contentContainerStyle={styles.grid}
      renderItem={({ item }) => <RecipeCard recipe={item} />}
    />
  );
};

export const stylesConfig = createStylesConfig({
  grid: {
    padding: 'global.spacing.md',
    gap: 'global.spacing.md',
  },
});
```

**Why**: Responsive layouts adapt to different screen sizes, orientations, and device types.

**Important**: Use `key={numColumns}` to force FlatList re-render when column count changes.

## Performance Patterns

### Extract StylesConfig Outside Component

Always extract `stylesConfig` outside the component:

```typescript
// ✅ Good: Defined outside component
export const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',
    backgroundColor: 'alias.color.neutral.background.default',
  },
});

export const RecipeCard = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};

// ❌ Bad: Defined inside component
export const RecipeCard = () => {
  const stylesConfig = createStylesConfig({  // Re-created on every render
    container: {
      padding: 'global.spacing.md',
    },
  });
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

**Why**: Extracting `stylesConfig` prevents unnecessary re-computation on every render. This is critical for performance in lists and frequently re-rendered components.

### Memoize Dynamic Styles

Use `useMemo` for styles computed at runtime:

```typescript
export const RecipeCard = ({ isActive, priority }: Props) => {
  const theme = useZestTheme();
  const styles = useZestStyles(stylesConfig);

  const dynamicStyle = useMemo(() => ({
    backgroundColor: isActive
      ? theme.alias.color.brand.background.default
      : theme.alias.color.neutral.background.default,
    borderWidth: priority === 'high' ? 2 : 1,
  }), [theme, isActive, priority]);

  return <View style={[styles.container, dynamicStyle]} />;
};
```

**Why**: Memoization prevents style object recreation on every render. Only recompute when dependencies change.

## Common Mistakes to Avoid

❌ **Don't use StyleSheet.create()**:

```typescript
// ❌ Bad - Bypasses design system
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F5F5F5',  // Hardcoded color
    padding: 16,                  // Hardcoded spacing
  },
});
```

❌ **Don't hardcode values**:

```typescript
// ❌ Bad - No theme integration
<View style={{
  padding: 16,
  backgroundColor: '#FFFFFF',
  borderRadius: 8,
}} />
```

❌ **Don't create styles inside component**:

```typescript
// ❌ Bad - Re-created every render
export const RecipeCard = () => {
  const styles = useZestStyles({
    container: { padding: 'global.spacing.md' },
  });
  return <View style={styles.container} />;
};
```

❌ **Don't skip memoization for dynamic styles**:

```typescript
// ❌ Bad - New object every render
export const RecipeCard = ({ isActive }: Props) => {
  const theme = useZestTheme();

  const dynamicStyle = {  // Re-created every render
    backgroundColor: isActive
      ? theme.alias.color.brand.background.default
      : theme.alias.color.neutral.background.default,
  };

  return <View style={dynamicStyle} />;
};
```

✅ **Do use Zest design tokens**:

```typescript
// ✅ Good - Type-safe tokens
export const stylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
    borderRadius: 'global.borderRadius.md',
  },
});
```

✅ **Do extract stylesConfig outside component**:

```typescript
// ✅ Good - Created once
export const stylesConfig = createStylesConfig({
  container: { padding: 'global.spacing.md' },
});

export const RecipeCard = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

✅ **Do memoize dynamic styles**:

```typescript
// ✅ Good - Only recomputes when dependencies change
export const RecipeCard = ({ isActive }: Props) => {
  const theme = useZestTheme();

  const dynamicStyle = useMemo(() => ({
    backgroundColor: isActive
      ? theme.alias.color.brand.background.default
      : theme.alias.color.neutral.background.default,
  }), [theme, isActive]);

  return <View style={dynamicStyle} />;
};
```

## Quick Reference

**Styling Hierarchy:**
1. First: Zest components with variants
2. Second: `useZestStyles` with `createStylesConfig`
3. Third: `useZestTheme` for dynamic values
4. Never: `StyleSheet.create()` or hardcoded values

**Design Tokens:**
- Colors: `alias.color.{semantic}.{element}.{variant}`
- Spacing: `global.spacing.{size}` (md=16px, sm=8px, sm2=12px)
- Border radius: `global.borderRadius.{size}` (md=8px, lg=12px)
- Typography: `global.fontSize.{category}.{size}`

**Performance:**
- ✅ Extract `stylesConfig` outside components
- ✅ Memoize dynamic styles with `useMemo`
- ✅ Use style arrays for conditional styling
- ✅ Use `gap` for flex container spacing

**Platform-Specific:**
- iOS: Use `shadowColor`, `shadowOffset`, `shadowOpacity`, `shadowRadius`
- Android: Use `elevation`
- Apply with `Platform.select()`

**Key Libraries:**
- @zest/react-native 1.5.3
- React Native 0.76+

For production examples, see [references/examples.md](references/examples.md).
