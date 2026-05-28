# Styling Patterns - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating Zest styling patterns.

## Example 1: Basic Layout with Design Tokens

**File**: `shared-mobile-modules/src/modules/store/screens/upsell/styles.ts`

```typescript
import { createStylesConfig } from '@zest/react-native';

export const stylesConfig = createStylesConfig({
  container: {
    flex: 1,
    backgroundColor: 'alias.color.elevation.background.base.default',
    position: 'relative',
  },
  contentContainer: {
    flex: 1,
  },
});
```

**Key patterns demonstrated:**
- Extract `stylesConfig` outside component
- Use `alias.color.*` tokens for colors
- Flexbox layout with `flex: 1`
- Clean separation of container and content styles

## Example 2: Complex Header with Typography and Spacing Tokens

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/styles.ts`

```typescript
import { createStylesConfig } from '@zest/react-native';

export const weekHeaderStylesConfig = createStylesConfig({
  header: {
    backgroundColor: 'alias.color.brand.background.default',
    borderColor: 'alias.color.brand.background.default',
    borderWidth: 'global.borderWidth.lg',
    minHeight: 60,
    width: '100%',
  },
  container: {
    flex: 1,
    paddingVertical: 'global.spacing.xxs',
    paddingHorizontal: 'global.spacing.md2',
    justifyContent: 'center',
    alignItems: 'center',
  },
  weekContainer: {
    alignItems: 'center',
  },
  deliveryDay: {
    fontFamily: 'global.fontFamily.bodyRegular',
    fontWeight: 400,
    fontSize: 'global.fontSize.body.bodyXs',
    color: 'alias.color.neutral.foreground.inverse',
  },
  deliveryDate: {
    fontFamily: 'global.fontFamily.headline',
    fontWeight: 700,
    fontSize: 'global.fontSize.headline.headlineSm',
    lineHeight: 'global.lineHeight.md2',
    color: 'alias.color.neutral.foreground.inverse',
  },
  skippedDateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  skippedDate: {
    color: 'alias.color.neutral.foreground.inverse',
    fontFamily: 'global.fontFamily.headline',
    fontWeight: 700,
    fontSize: 'global.fontSize.headline.headlineMd',
    lineHeight: 'global.lineHeight.md2',
    textAlign: 'center',
  },
  skippedIcon: {
    marginRight: 'global.spacing.xxs',
    color: 'alias.color.neutral.foreground.inverse',
  },
});
```

**Key patterns demonstrated:**
- Brand color for header background
- Inverse foreground colors for text on brand background
- Typography tokens: `global.fontSize.*`, `global.fontFamily.*`, `global.lineHeight.*`
- Spacing tokens: `global.spacing.xxs`, `global.spacing.md2`
- Border width token: `global.borderWidth.lg`
- Flexbox alignment patterns
- Multiple related styles in single config

## Example 3: Interactive Component with Zest Components

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/single-week-header/back-button/BackButton.tsx`

```typescript
import { Pressable } from 'react-native';
import { useShallow } from 'zustand/react/shallow';

import { useMealSelection } from '@operations/meal-selection/useMealSelection';

import { Icon, useZestStyles } from '@zest/react-native';

import { stylesConfig } from './styles';

interface BackButtonProps {
  onPress: () => void;
}

export const BackButton: React.FC<BackButtonProps> = ({ onPress }) => {
  const styles = useZestStyles(stylesConfig);
  const isSaving = useMealSelection(useShallow((state) => state.isSaving));

  return (
    <Pressable
      style={styles.backButton}
      key="back"
      onPress={onPress}
      disabled={isSaving}
      accessibilityRole="button"
      accessibilityLabel="Back Button"
      accessibilityHint="Go back to the previous screen"
      testID="back-button"
    >
      <Icon
        icon="ChevronLeftOutline24"
        color="alias.color.neutral.foreground.inverse"
        altText="Back Button"
      />
    </Pressable>
  );
};
```

**Key patterns demonstrated:**
- `useZestStyles` hook with imported config
- Zest `Icon` component with color token
- Conditional disabling based on state
- Full accessibility properties
- Test ID for testing
- Inline color token on Zest component

## Example 4: Styling Hierarchy in Practice

**Location**: `shared-mobile-modules/src/modules/store/screens/upsell/components/upsell-header/UpsellHeader.tsx`

```typescript
import { View } from 'react-native';
import { Text, useZestStyles } from '@zest/react-native';

import { stylesConfig } from './styles';

interface UpsellHeaderProps {
  title: string;
  subtitle?: string;
}

export const UpsellHeader: React.FC<UpsellHeaderProps> = ({ title, subtitle }) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <Text type="headline-lg" style={styles.title}>
        {title}
      </Text>
      {subtitle && (
        <Text type="body-md-regular" style={styles.subtitle}>
          {subtitle}
        </Text>
      )}
    </View>
  );
};
```

**Key patterns demonstrated:**
- Level 1: Zest `Text` component with `type` prop for typography
- Level 2: `useZestStyles` for custom layout
- Combining Zest component variants with custom styles
- Conditional rendering with consistent styling

## Anti-Patterns to Avoid

### ❌ Hardcoded Values

```typescript
// DON'T: From legacy code
const styles = StyleSheet.create({
  container: {
    padding: 16,              // Should use global.spacing.md
    backgroundColor: '#F5F5F5', // Should use alias.color token
    borderRadius: 8,          // Should use global.borderRadius.md
  },
});
```

### ❌ Inline Style Objects

```typescript
// DON'T: Creates new object every render
<View style={{
  padding: 16,
  backgroundColor: '#FFFFFF',
}}>
```

### ❌ Creating Styles Inside Component

```typescript
// DON'T: Re-creates config on every render
export const MyComponent = () => {
  const stylesConfig = createStylesConfig({
    container: { padding: 'global.spacing.md' },
  });
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

## Common Token Usage Patterns

### Most Frequently Used Spacing Tokens

Based on codebase analysis:

1. **`global.spacing.md`** (16px) - Default padding for containers
2. **`global.spacing.sm`** (8px) - Gap between flex items
3. **`global.spacing.sm2`** (12px) - Intermediate spacing
4. **`global.spacing.xs`** (4px) - Compact spacing
5. **`global.spacing.xxs`** (2px) - Minimal spacing (icons, badges)

### Most Frequently Used Color Patterns

1. **Background**: `alias.color.neutral.background.default`
2. **Text**: `alias.color.neutral.foreground.default`
3. **Brand accent**: `alias.color.brand.background.default`
4. **Inverse (on brand)**: `alias.color.neutral.foreground.inverse`
5. **Borders**: `alias.color.neutral.border.default`

### Typography Hierarchy

From production usage:

1. **Headlines**: `global.fontSize.headline.{size}` + `global.fontFamily.headline` + weight 700
2. **Body text**: `global.fontSize.body.{size}` + `global.fontFamily.bodyRegular` + weight 400
3. **Line heights**: `global.lineHeight.{size}` matching font size

## Integration with Other Patterns

### With Zustand State

```typescript
export const RecipeCard = ({ recipeId }: Props) => {
  const styles = useZestStyles(stylesConfig);
  const isSelected = useRecipeStore(
    useShallow((state) => state.selectedIds.includes(recipeId))
  );

  return (
    <View style={[
      styles.container,
      isSelected && styles.selectedContainer,
    ]}>
      {/* content */}
    </View>
  );
};
```

### With Test IDs

```typescript
export const RecipeCard = () => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container} testID={TEST_IDS.RECIPE_CARD}>
      <Text style={styles.title} testID={TEST_IDS.RECIPE_TITLE}>
        Recipe Name
      </Text>
    </View>
  );
};
```

## Performance Considerations

### Good: Extracted Config

```typescript
// Created once at module load
export const stylesConfig = createStylesConfig({
  container: { padding: 'global.spacing.md' },
});

// Multiple instances share the same config
export const RecipeCard = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

### Good: Memoized Dynamic Styles

```typescript
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

## Summary

The YourCompany codebase consistently follows these patterns:

1. **Extract all `stylesConfig` outside components** for performance
2. **Use design tokens exclusively** - never hardcoded values
3. **Prefer Zest components** with built-in variants first
4. **Use `useZestStyles`** for custom layouts and compositions
5. **Use `useZestTheme`** only for computed/dynamic styles
6. **Memoize dynamic styles** with `useMemo`
7. **Use style arrays** for conditional styling
8. **Apply full accessibility** properties alongside styling

These patterns ensure consistent theming, performance, accessibility, and maintainability across the entire application.
