---
name: zest-integration
description: "WHAT: Zest React Native integration with ZestProvider, useZestTheme, and useZestStyles hooks. WHEN: setting up providers, accessing theme tokens, creating themed styles, dark mode support. KEYWORDS: ZestProvider, useZestTheme, useZestStyles, createStylesConfig, alias tokens, global tokens, dark mode, ScreenEntryProvider."
---

# Zest Design System Integration

## Core Principles

**Always wrap app root with ZestProvider.** ZestProvider must be at the app root (ScreenEntryProvider, NavigationEntryProvider, or WidgetEntryProvider) to ensure all components have access to theme context. Never nest ZestProviders or use inside components.

**Use useZestStyles for static styling, useZestTheme for dynamic styling.** useZestStyles with createStylesConfig resolves token strings ('alias.color.brand.background.default') to values automatically. useZestTheme provides direct access to theme object for conditional or computed styles with useMemo.

**Use semantic alias tokens for colors, global tokens for measurements.** Alias tokens (alias.color.*) provide semantic meaning and adapt to theme changes (light/dark mode). Global tokens (global.spacing.*, global.borderRadius.*) provide consistent primitive values across all components.

**Extract StylesConfig outside components for performance.** Always define StylesConfig outside component functions to prevent recreation on every render. Use static token strings for consistent styling that updates automatically with theme changes.

**Why**: Proper Zest integration ensures consistent theming, automatic dark mode support, type-safe token access, and optimal performance through proper provider composition and style memoization.

## When to Use This Skill

Use these patterns when:

- Setting up app-level providers and theme context
- Accessing theme tokens for colors, spacing, typography
- Creating components that need theme-aware styling
- Supporting dark mode with automatic theme switching
- Building responsive layouts with consistent spacing
- Applying platform-specific theming (iOS/Android shadows)
- Testing components that depend on theme context
- Creating conditional styles based on theme values
- Implementing custom theme configurations per brand
- Ensuring consistent design system adoption

## ZestProvider Setup

### App Root Integration

Wrap the app root with ZestProvider in ScreenEntryProvider for global theme access.

```typescript
// entry-providers/providers.tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ApolloProviderWrapper } from '@libs/graphql/providers/ApolloProviderWrapper';
import { AppWithTranslation } from '@libs/localization';
import { ZestProvider } from '@libs/zest';
import { ErrorBoundary } from '@libs/error-boundary';

export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProviderWrapper>
        <SafeAreaProvider>
          <AppWithTranslation>
            <ZestProvider>
              <ErrorBoundary scope={{ moduleName: 'App' }}>
                {children}
              </ErrorBoundary>
            </ZestProvider>
          </AppWithTranslation>
        </SafeAreaProvider>
      </ApolloProviderWrapper>
    </QueryClientProvider>
  );
};
```

**Why**: ZestProvider at root level ensures all nested components have access to theme context via useZestTheme and useZestStyles hooks. Provider composition order matters: QueryClient → Apollo → SafeArea → i18n → Zest → ErrorBoundary.

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:129`

### Provider Composition Pattern

Three provider patterns for different contexts: ScreenEntryProvider (full screens), NavigationEntryProvider (navigation stacks), WidgetEntryProvider (isolated widgets).

```typescript
// NavigationEntryProvider - wraps navigation stacks
export const NavigationEntryProvider = ({ children, linking }) => (
  <ScreenEntryProvider>
    <NavigationContainer linking={linking}>
      {children}
      <Toast />
    </NavigationContainer>
  </ScreenEntryProvider>
);

// WidgetEntryProvider - wraps standalone widgets
export const WidgetEntryProvider: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProviderWrapper>
        <AppWithTranslation>
          <ZestProvider>
            <ErrorBoundary scope={{ moduleName: 'App' }}>
              {children}
            </ErrorBoundary>
          </ZestProvider>
        </AppWithTranslation>
      </ApolloProviderWrapper>
    </QueryClientProvider>
  );
};
```

**Why**: Different provider compositions for different contexts ensures appropriate services are available. ScreenEntryProvider includes SafeAreaProvider for full screens, WidgetEntryProvider omits it for isolated components, NavigationEntryProvider adds NavigationContainer.

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:86`

### Custom ZestProvider with Brand (REQUIRED)

Wrap ZestThemeProvider with brand-specific configuration. **Brand is REQUIRED** - the provider will not render without it.

```typescript
// libs/zest/ZestProvider.tsx
import { AppConfigDataAccess } from '@data-access/native';
import { ZestThemeProvider, type Brand } from '@zest/react-native';

export const ZestProvider = ({ children }: ZestProviderProps) => {
  const { data: brand } = AppConfigDataAccess.queries.useBrandState();

  // Brand is REQUIRED - don't render until brand is available
  if (!brand) {
    return <></>;
  }

  // ZestThemeProvider expects Brand type from Zest
  return <ZestThemeProvider brand={brand as unknown as Brand} {...props} />;
};
```

**Why**: Custom ZestProvider fetches brand from native repository and passes to ZestThemeProvider. **Brand is required** - this enables brand-specific theme configuration (YourCompany, GreenChef, EveryPlate, Factor) with automatic theme switching based on app configuration.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/zest/ZestProvider.tsx:1`

## Accessing Theme

### useZestTheme Hook for Dynamic Styling

Access theme values directly for conditional or computed styles.

```typescript
import { useZestTheme } from '@zest/react-native';
import { useMemo } from 'react';

export const PlatformStatusBar = ({ barStyle, backgroundColor }) => {
  const theme = useZestTheme();

  return (
    <StatusBar
      barStyle={barStyle}
      backgroundColor={
        backgroundColor || theme.alias.color.brand.background.default
      }
    />
  );
};
```

**Why**: useZestTheme provides direct access to theme object for dynamic styles. Use when styles depend on props, state, or conditional logic. For static styles, prefer useZestStyles with createStylesConfig for better performance.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/components/PlatformStatusBar.tsx:20`

### useZestTheme with useMemo

Memoize theme-based computed styles to prevent recalculation on every render.

```typescript
import { useZestTheme } from '@zest/react-native';
import { useMemo } from 'react';

export const useProductLabel = ({ data, showSoldOut }) => {
  const theme = useZestTheme();

  return useMemo(() => {
    const labelText = (showSoldOut ? 'SOLD OUT' : data?.text ?? '').toUpperCase();

    if (!labelText) {
      return undefined;
    }

    if (showSoldOut) {
      return {
        backgroundColor: 'global.color.cherry.100' as ColorType,
        foregroundColor: 'global.color.cherry.600' as ColorType,
        borderColor: 'global.color.cherry.600' as ColorType,
      };
    }

    return {
      backgroundColor:
        (data?.style?.backgroundColor as ColorType) ??
        theme.alias.color.button.background,
      foregroundColor:
        (data?.style?.foregroundColor as ColorType) ??
        theme.alias.color.button.foreground,
    };
  }, [data, showSoldOut, theme]);
};
```

**Why**: useMemo prevents style recalculation on every render. Dependencies array [data, showSoldOut, theme] ensures styles update only when necessary. Theme-based conditional logic requires useZestTheme + useMemo pattern.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/shoppable-product/useProductLabel.ts:33`

### useZestTheme in Navigation Configuration

Use theme values for React Navigation header styling.

```typescript
import { useZestTheme } from '@zest/react-native';
import { useLayoutEffect } from 'react';
import type { NativeStackNavigationOptions } from '@react-navigation/native-stack';

export const useNavigationHeader = ({ navigation, options = {} }) => {
  const theme = useZestTheme();

  useLayoutEffect(() => {
    const defaultOptions: NativeStackNavigationOptions = {
      headerShown: true,
      headerTitleAlign: 'left',
      headerTitleStyle: {
        fontFamily: theme.global.fontFamily.headline,
        fontSize: theme.global.fontSize.headline.headlineMd,
        color: theme.alias.color.neutral.foreground.inverse,
      },
      headerStyle: {
        backgroundColor: theme.alias.color.brand.background.default,
      },
      headerTintColor: theme.alias.color.neutral.foreground.inverse,
    };

    navigation.setOptions({
      ...defaultOptions,
      ...options,
      headerTitleStyle: {
        ...((defaultOptions.headerTitleStyle as object) || {}),
        ...((options.headerTitleStyle as object) || {}),
      },
    });
  }, [navigation, options, theme]);
};
```

**Why**: React Navigation requires object styles (not token strings), so useZestTheme provides direct access to resolved values. useLayoutEffect with [navigation, options, theme] dependencies ensures header updates when theme changes.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/navigation-header/useNavigationHeader.ts:29`

### useZestStyles Hook for Static Styling

Use useZestStyles with createStylesConfig for token-based styling that updates automatically.

```typescript
import { useZestStyles, createStylesConfig, Text } from '@zest/react-native';

// ✅ Extract outside component
export const weekHeaderStylesConfig = createStylesConfig({
  header: {
    backgroundColor: 'alias.color.brand.background.default',
    borderColor: 'alias.color.brand.background.default',
    borderWidth: 'global.borderWidth.lg',
    minHeight: 60,
    width: '100%',
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
});

export const ActiveWeekContent = ({ week }) => {
  const styles = useZestStyles(weekHeaderStylesConfig);

  return (
    <>
      <Text style={styles.deliveryDay}>{week.deliveryDay}</Text>
      <Text style={styles.deliveryDate}>{week.deliveryDate}</Text>
    </>
  );
};
```

**Why**: useZestStyles resolves token strings to actual values and updates when theme changes (light/dark mode). createStylesConfig outside component prevents recreation on every render. Token strings provide type safety and automatic updates.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/styles.ts:1`

## Theme Structure

### Token Hierarchy Overview

Zest theme has three layers: **components** (component-specific), **global** (primitive values), and **alias** (semantic tokens).

The hierarchy flows: **components → global → alias**

```typescript
theme = {
  components: {
    // Component-specific tokens (highest priority)
    button: {
      borderRadius: 'global.borderRadius.md',
      padding: 'global.spacing.md',
    },
    text: {
      color: 'alias.color.neutral.foreground.default',
    },
  },
  global: {
    // Primitive values - fixed design constants
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32,
    },
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 12,
      full: 9999,
    },
    typography: {
      body: {
        md: {
          fontSize: 16,
          lineHeight: 24,
          fontWeight: 400,
        },
      },
      headline: {
        xl: {
          fontSize: 32,
          lineHeight: 40,
          fontWeight: 700,
        },
      },
    },
    fontFamily: {
      bodyRegular: 'HelveticaNeue-Regular',
      headline: 'HelveticaNeue-Bold',
    },
  },
  alias: {
    // Semantic tokens - contextual meaning
    color: {
      brand: {
        background: { default: '#FF6B35' },
        foreground: { default: '#FFFFFF' },
        border: { default: '#FF6B35' },
      },
      neutral: {
        background: { default: '#FFFFFF', subtle: '#F5F5F5' },
        foreground: { default: '#1A1A1A', subtle: '#666666', inverse: '#FFFFFF' },
        border: { default: '#E0E0E0' },
      },
      semantic: {
        error: {
          background: { default: '#FEE2E2' },
          foreground: { default: '#DC2626' },
        },
        success: {
          background: { default: '#D1FAE5' },
          foreground: { default: '#059669' },
        },
        warning: {
          background: { default: '#FEF3C7' },
          foreground: { default: '#D97706' },
        },
      },
    },
  },
};
```

**Why**: Two-layer structure separates primitive values (global) from semantic meaning (alias). Global tokens ensure consistency, alias tokens provide contextual meaning and adapt to theme changes (light/dark mode, brand switching).

### Global Tokens for Primitives

Use global tokens for fixed design values: spacing, borderRadius, typography, fontFamily.

```typescript
// Spacing
theme.global.spacing.xs; // 4px
theme.global.spacing.sm; // 8px
theme.global.spacing.md; // 16px
theme.global.spacing.lg; // 24px
theme.global.spacing.xl; // 32px

// Border Radius
theme.global.borderRadius.sm; // 4px
theme.global.borderRadius.md; // 8px
theme.global.borderRadius.lg; // 12px
theme.global.borderRadius.full; // 9999px

// Typography
theme.global.typography.headline.xl.fontSize; // 32px
theme.global.typography.headline.xl.lineHeight; // 40px
theme.global.typography.body.md.fontSize; // 16px
theme.global.typography.body.md.lineHeight; // 24px

// Font Family
theme.global.fontFamily.bodyRegular; // 'HelveticaNeue-Regular'
theme.global.fontFamily.headline; // 'HelveticaNeue-Bold'
```

**Why**: Global tokens provide consistent measurements and typography across all components. These values rarely change and form the foundation of the design system.

### Alias Tokens for Semantic Colors

Use alias tokens for colors with semantic meaning that adapt to theme variants.

```typescript
// Brand colors (primary actions, headers)
theme.alias.color.brand.background.default; // Primary brand color
theme.alias.color.brand.foreground.default; // Text on brand backgrounds
theme.alias.color.brand.border.default; // Brand-colored borders

// Neutral colors (default UI, backgrounds, text)
theme.alias.color.neutral.background.default; // White/dark background
theme.alias.color.neutral.background.subtle; // Subtle gray background
theme.alias.color.neutral.foreground.default; // Primary text color
theme.alias.color.neutral.foreground.subtle; // Secondary text color
theme.alias.color.neutral.foreground.inverse; // Text on dark backgrounds

// Semantic colors (status indication)
theme.alias.color.semantic.error.background.default; // Error background
theme.alias.color.semantic.error.foreground.default; // Error text
theme.alias.color.semantic.success.background.default; // Success background
theme.alias.color.semantic.success.foreground.default; // Success text
theme.alias.color.semantic.warning.background.default; // Warning background
```

**Why**: Alias tokens provide semantic meaning and automatically adapt to theme changes. In dark mode, alias tokens change while global tokens remain constant. Use alias for all colors, global for spacing/typography.

### Token Strings in StylesConfig

Reference tokens as strings in createStylesConfig for automatic resolution.

```typescript
export const stylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
    borderRadius: 'global.borderRadius.md',
  },
  text: {
    color: 'alias.color.neutral.foreground.default',
    fontSize: 'global.typography.body.md.fontSize',
    fontFamily: 'global.fontFamily.bodyRegular',
  },
  brandButton: {
    backgroundColor: 'alias.color.brand.background.default',
    borderColor: 'alias.color.brand.border.default',
    borderWidth: 'global.borderWidth.md',
  },
  // Callback pattern for computed/negative values
  sectionContainer: {
    marginTop: 'global.spacing.sm1',
    marginHorizontal: (theme) => -theme.global.spacing.xs,
  },
});
```

**Callback pattern**: Use `(theme) => value` for computed values like negative margins that can't be expressed as string tokens.

**Why**: Token strings enable type-safe references and automatic resolution by useZestStyles. Strings update automatically when theme changes (light/dark mode), preventing stale values.

## Dark Mode Support

### Theme Variants with useColorScheme

Support light and dark theme variants automatically.

```typescript
import { useColorScheme } from 'react-native';
import { ZestProvider } from '@libs/zest';

export const App = () => {
  const systemColorScheme = useColorScheme(); // 'light', 'dark', or null

  return (
    <ZestProvider theme={systemColorScheme || 'light'}>
      {children}
    </ZestProvider>
  );
};
```

**Why**: useColorScheme detects system theme preference (Settings → Display → Dark Mode). ZestProvider accepts 'light' or 'dark' and automatically switches alias token values. Global tokens remain constant across themes.

### Theme Detection Best Practices

Always provide a fallback theme when useColorScheme returns null.

```typescript
import { useColorScheme } from 'react-native';

const App = () => {
  const colorScheme = useColorScheme(); // Can be null on initial render

  return (
    <ZestProvider theme={colorScheme || 'light'}>
      {children}
    </ZestProvider>
  );
};
```

**Why**: useColorScheme returns null on initial render before system preferences load. Fallback to 'light' prevents missing theme errors and ensures consistent default experience.

## Responsive Design with Zest

### Combine with useWindowDimensions

Use Zest tokens with responsive layouts for consistent spacing across screen sizes.

```typescript
import { useWindowDimensions, FlatList } from 'react-native';
import { useZestStyles, createStylesConfig } from '@zest/react-native';

export const ResponsiveGrid = () => {
  const { width } = useWindowDimensions();
  const styles = useZestStyles(stylesConfig);

  const isTablet = width > 768;
  const numColumns = isTablet ? 3 : 2;

  return (
    <FlatList
      data={items}
      numColumns={numColumns}
      key={numColumns} // Force re-render on column change
      contentContainerStyle={styles.grid}
      renderItem={({ item }) => <ItemCard item={item} />}
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

**Why**: Combining useWindowDimensions (responsive breakpoints) with Zest tokens (consistent spacing) creates layouts that adapt to screen size while maintaining design system consistency.

## Testing with Zest

### Wrap Tests with ZestProvider

Always wrap test components with ZestProvider to provide theme context.

```typescript
import { render } from '@testing-library/react-native';
import { ZestProvider } from '@zest/react-native';

const renderWithZest = (component: React.ReactElement) => {
  return render(
    <ZestProvider>
      {component}
    </ZestProvider>
  );
};

test('renders with Zest theme', () => {
  const { getByText } = renderWithZest(<CustomComponent />);
  expect(getByText('Content')).toBeTruthy();
});
```

**Why**: Components using useZestTheme or useZestStyles require ZestProvider in tests. Without provider, hooks throw errors and tests fail. Create renderWithZest helper for consistent test setup.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/zest/ZestProvider.test.tsx:9`

### Test Theme Values with renderHook

Verify hooks return correct theme values.

```typescript
import { renderHook } from '@testing-library/react-hooks';
import { useZestTheme } from '@zest/react-native';
import { ZestProvider } from '@zest/react-native';

test('useZestTheme returns theme values', () => {
  const wrapper = ({ children }) => <ZestProvider>{children}</ZestProvider>;

  const { result } = renderHook(() => useZestTheme(), { wrapper });

  expect(result.current.global.spacing.md).toBe(16);
  expect(result.current.alias.color.brand.background.default).toBeDefined();
});
```

**Why**: Testing theme access ensures components can access tokens correctly. renderHook with wrapper provides provider context for hooks. Verify both global and alias tokens resolve correctly.

## Performance Optimization

### Extract StylesConfig Outside Component

Always define StylesConfig outside component functions to prevent recreation on every render.

```typescript
// ✅ Good: Extracted outside
export const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',
    backgroundColor: 'alias.color.neutral.background.default',
  },
});

export const Component = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};

// ❌ Bad: Defined inside component
export const Component = () => {
  const styles = useZestStyles({
    container: { padding: 'global.spacing.md' }, // Re-created every render
  });
  return <View style={styles.container} />;
};
```

**Why**: Defining StylesConfig inside component causes recreation on every render, triggering unnecessary style resolution. Extract outside component for one-time initialization and consistent references.

### Memoize Theme-Based Computed Styles

Use useMemo for dynamic styles that depend on theme to prevent recalculation.

```typescript
import { useZestTheme } from '@zest/react-native';
import { useMemo } from 'react';

export const StatusBadge = ({ status }: Props) => {
  const theme = useZestTheme();

  const badgeStyle = useMemo(() => ({
    backgroundColor:
      status === 'success'
        ? theme.alias.color.semantic.success.background.default
        : status === 'error'
        ? theme.alias.color.semantic.error.background.default
        : theme.alias.color.neutral.background.subtle,
    color:
      status === 'success'
        ? theme.alias.color.semantic.success.foreground.default
        : status === 'error'
        ? theme.alias.color.semantic.error.foreground.default
        : theme.alias.color.neutral.foreground.default,
  }), [theme, status]);

  return <View style={badgeStyle}>{/* content */}</View>;
};
```

**Why**: useMemo prevents style recalculation on every render. Dependencies [theme, status] ensure styles update only when theme or status changes. Without useMemo, conditional logic executes every render even when values don't change.

## Platform-Specific Theming

### Apply Platform-Specific Shadows

Use theme values with Platform.select for iOS/Android styling differences.

```typescript
import { Platform } from 'react-native';
import { useZestTheme } from '@zest/react-native';

export const PlatformCard = () => {
  const theme = useZestTheme();
  const styles = useZestStyles(stylesConfig);

  const platformShadow = Platform.select({
    ios: {
      shadowColor: theme.alias.color.neutral.foreground.default,
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 2,
    },
  });

  return (
    <View style={[styles.card, platformShadow]}>
      {/* content */}
    </View>
  );
};
```

**Why**: iOS uses shadowColor/shadowOffset/shadowOpacity/shadowRadius for shadows, Android uses elevation. Platform.select handles differences, theme provides consistent colors. Combine both for cross-platform consistency.

## Common Mistakes to Avoid

❌ **Don't nest multiple ZestProviders**:

```typescript
// ❌ Wrong - multiple providers
<ZestProvider>
  <App>
    <ZestProvider> {/* Wrong - already wrapped */}
      <Component />
    </ZestProvider>
  </App>
</ZestProvider>
```

**Why**: Nesting ZestProviders creates conflicting theme contexts and causes unexpected behavior. Only one ZestProvider should exist at app root.

✅ **Do wrap app root once with ZestProvider**:

```typescript
// ✅ Correct - single provider at root
<ZestProvider>
  <App>
    <Component /> {/* Inherits theme from root */}
  </App>
</ZestProvider>
```

**Why**: Single provider at root ensures all components share the same theme context consistently.

❌ **Don't use ZestProvider inside components**:

```typescript
// ❌ Wrong - provider inside component
const Component = () => (
  <ZestProvider> {/* Wrong - should be at root */}
    <Content />
  </ZestProvider>
);
```

**Why**: ZestProvider inside components causes multiple instances and prevents global theme changes from propagating correctly.

✅ **Do use ZestProvider at app root**:

```typescript
// ✅ Correct - provider at root
export const ScreenEntryProvider = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    <ZestProvider>
      {children}
    </ZestProvider>
  </QueryClientProvider>
);
```

**Why**: Root-level provider ensures all components have consistent access to theme context.

❌ **Don't hardcode theme values**:

```typescript
// ❌ Wrong - hardcoded colors
<View style={{ backgroundColor: '#FF6B35', padding: 16 }} />
```

**Why**: Hardcoded values don't respond to theme changes (light/dark mode, brand switching) and bypass design system consistency.

✅ **Do use theme tokens**:

```typescript
// ✅ Correct - token strings
const styles = useZestStyles(createStylesConfig({
  container: {
    backgroundColor: 'alias.color.brand.background.default',
    padding: 'global.spacing.md',
  },
}));

<View style={styles.container} />
```

**Why**: Token strings automatically resolve to correct values and update when theme changes.

❌ **Don't create StylesConfig inside components**:

```typescript
// ❌ Wrong - recreated every render
export const Component = () => {
  const styles = useZestStyles({
    container: { padding: 'global.spacing.md' }, // Re-created
  });
  return <View style={styles.container} />;
};
```

**Why**: Creating StylesConfig inside component causes recreation on every render, triggering unnecessary style resolution and degrading performance.

✅ **Do extract StylesConfig outside component**:

```typescript
// ✅ Correct - created once
export const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',
  },
});

export const Component = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

**Why**: Extracting config prevents recreation and ensures consistent references for optimal performance.

❌ **Don't access theme without ZestProvider**:

```typescript
// ❌ Wrong - no ZestProvider wrapper
const App = () => (
  <Component /> {/* useZestTheme() will throw error */}
);

const Component = () => {
  const theme = useZestTheme(); // Error: no provider
  return <View />;
};
```

**Why**: useZestTheme and useZestStyles require ZestProvider to exist in parent tree. Without provider, hooks throw errors.

✅ **Do wrap app with ZestProvider**:

```typescript
// ✅ Correct - wrapped with provider
const App = () => (
  <ZestProvider>
    <Component /> {/* useZestTheme() works */}
  </ZestProvider>
);

const Component = () => {
  const theme = useZestTheme(); // Works correctly
  return <View />;
};
```

**Why**: ZestProvider in parent tree provides context for all nested components using theme hooks.

❌ **Don't skip dark mode support**:

```typescript
// ❌ Wrong - hardcoded light theme
<ZestProvider theme="light">
  {children}
</ZestProvider>
```

**Why**: Hardcoded theme ignores user's system preference and prevents dark mode support.

✅ **Do support dark mode with useColorScheme**:

```typescript
// ✅ Correct - respects system preference
import { useColorScheme } from 'react-native';

const App = () => {
  const colorScheme = useColorScheme();
  return (
    <ZestProvider theme={colorScheme || 'light'}>
      {children}
    </ZestProvider>
  );
};
```

**Why**: useColorScheme detects system preference and automatically switches theme, respecting user's choice.

## Quick Reference

**Basic ZestProvider setup**:
```typescript
import { ZestProvider } from '@libs/zest';

<ZestProvider>
  <App />
</ZestProvider>
```

**ScreenEntryProvider composition**:
```typescript
export const ScreenEntryProvider = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    <ApolloProviderWrapper>
      <SafeAreaProvider>
        <AppWithTranslation>
          <ZestProvider>
            <ErrorBoundary>
              {children}
            </ErrorBoundary>
          </ZestProvider>
        </AppWithTranslation>
      </SafeAreaProvider>
    </ApolloProviderWrapper>
  </QueryClientProvider>
);
```

**useZestTheme for dynamic styles**:
```typescript
const theme = useZestTheme();
const bgColor = theme.alias.color.brand.background.default;
```

**useZestStyles for static styles**:
```typescript
const stylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.brand.background.default',
    padding: 'global.spacing.md',
  },
});

const Component = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container} />;
};
```

**Dark mode support**:
```typescript
const colorScheme = useColorScheme();
<ZestProvider theme={colorScheme || 'light'}>
  {children}
</ZestProvider>
```

**Testing with ZestProvider**:
```typescript
const renderWithZest = (component) =>
  render(<ZestProvider>{component}</ZestProvider>);
```

**Theme token hierarchy**:
```typescript
// Global tokens (primitives)
'global.spacing.md'               // 16
'global.borderRadius.lg'          // 12
'global.typography.body.md.fontSize'  // 16

// Alias tokens (semantic)
'alias.color.brand.background.default'
'alias.color.neutral.foreground.default'
'alias.color.semantic.error.background.default'
```

**Key Libraries:**
- @zest/react-native 1.5.3
- React Native 0.76+

For production examples, see [references/examples.md](references/examples.md).
