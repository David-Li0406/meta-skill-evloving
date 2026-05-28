# Zest Integration - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating Zest design system integration patterns.

## Example 1: ScreenEntryProvider with ZestProvider

**File**: `entry-providers/providers.tsx:129`

This example shows the complete provider composition pattern with ZestProvider at the core.

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { QueryClientProvider } from '@tanstack/react-query';
import type { PropsWithChildren } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { ErrorBoundary } from '@libs/error-boundary';
import { ApolloProviderWrapper } from '@libs/graphql/providers/ApolloProviderWrapper';
import { AppWithTranslation } from '@libs/localization';
import { queryClient } from '@libs/query';
import { ZestProvider } from '@libs/zest';

/**
 * @description
 * `ScreenEntryProvider` is a higher-order component that provides essential context
 * for components displayed in a single full-screen mode. It supports initialization and handling
 * of services required to to Screens to function properly.
 */
export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProviderWrapper>
        <QueryCacheManager />
        <GlobalLoyaltyStateManager />
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

**Key patterns demonstrated:**
- Provider composition order: QueryClient → Apollo → SafeArea → i18n → Zest → ErrorBoundary
- ZestProvider wrapped inside AppWithTranslation (i18n)
- ZestProvider wraps ErrorBoundary (theme available in error UI)
- QueryCacheManager and GlobalLoyaltyStateManager as sibling components
- PropsWithChildren type for children prop
- JSDoc documentation for provider purpose

## Example 2: NavigationEntryProvider Composition

**File**: `entry-providers/providers.tsx:86`

This example shows NavigationEntryProvider wrapping ScreenEntryProvider for navigation stacks.

```typescript
/**
 * @description
 * `NavigationEntryProvider` is a higher-order component designed to wrap a navigation stack.
 * It provides the necessary context for navigation and deep linking within the app.
 * Now supports optional repository loading to ensure critical data is available before rendering.
 */
export const NavigationEntryProvider = <StackType extends object>({
  children,
  linking,
  requiredRepositories,
  repositoryLoadingFallback,
}: NavigationEntryProviderProps<StackType>) => (
  <ScreenEntryProvider>
    <NavigationContainer linking={linking}>
      {requiredRepositories && Object.keys(requiredRepositories).length > 0 ? (
        <RepositoryLoader
          requiredRepositories={requiredRepositories}
          loadingFallback={repositoryLoadingFallback}
        >
          {children}
          <Toast />
        </RepositoryLoader>
      ) : (
        <>
          {children}
          <Toast />
        </>
      )}
    </NavigationContainer>
  </ScreenEntryProvider>
);
```

**Key patterns demonstrated:**
- ScreenEntryProvider wrapper (includes ZestProvider)
- NavigationContainer for navigation context
- Optional RepositoryLoader for data pre-loading
- Conditional rendering based on requiredRepositories
- Toast component as sibling to children
- Generic type parameter for StackType
- linking prop for deep linking configuration

## Example 3: WidgetEntryProvider Composition

**File**: `entry-providers/providers.tsx:172`

This example shows WidgetEntryProvider for isolated widgets (no SafeAreaProvider or NavigationContainer).

```typescript
/**
 * @description
 * `WidgetEntryProvider` is a higher-order component designed for wrapping individual
 * Components (i.e.: Widgets) that will be displayed within a Screen. It supports
 * initialization and handling of services required to to Screens to function properly.
 *
 * This provider is typically used for smaller, self-contained components that do not
 * require full-screen context.
 */
export const WidgetEntryProvider: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProviderWrapper>
        <QueryCacheManager />
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

**Key patterns demonstrated:**
- Lighter provider composition (no SafeAreaProvider)
- Suitable for isolated widgets within screens
- Still includes QueryClient, Apollo, i18n, Zest, ErrorBoundary
- Omits SafeAreaProvider (not needed for widgets)
- Omits NavigationContainer (widgets don't navigate)
- JSDoc explains use case (smaller components)

## Example 4: Custom ZestProvider with Brand

**File**: `libs/zest/ZestProvider.tsx:1`

This example shows custom ZestProvider wrapper that fetches brand from native repository.

```typescript
import type { ReactNode } from 'react';

import { AppConfigDataAccess } from '@data-access/native';

import type { Brand } from '@zest/react-native';
import { ZestThemeProvider } from '@zest/react-native';

export type ZestProviderProps = {
  children: ReactNode;
};

export const ZestProvider = (props: ZestProviderProps) => {
  const { data: brand } = AppConfigDataAccess.queries.useBrandState();

  // This is a fallback in case the brand is not available
  if (!brand) {
    return <></>;
  }

  // Convert it as unknown as the brand we get from the query
  // is not the same as the one from the ZestThemeProvider
  return <ZestThemeProvider brand={brand as unknown as Brand} {...props} />;
};
```

**Key patterns demonstrated:**
- Custom wrapper around ZestThemeProvider
- AppConfigDataAccess.queries.useBrandState() for brand data
- Fallback to empty fragment if brand not available
- Type casting (as unknown as Brand) for type compatibility
- Props spreading with {...props}
- ReactNode type for children
- Comment explaining type casting rationale

## Example 5: useZestTheme for Dynamic Styling

**File**: `libs/utils/components/PlatformStatusBar.tsx:1`

This example shows useZestTheme for dynamic theme access with fallback logic.

```typescript
import { StatusBar } from 'react-native';

import { useZestTheme } from '@zest/react-native';

import { PlatformIs } from '../platform';

interface PlatformStatusBarProps {
  barStyle?: 'light-content' | 'dark-content';
  backgroundColor?: string;
}

/**
 * Platform-aware StatusBar component that only renders on Android
 * Uses theme colors by default but allows customization
 */
export const PlatformStatusBar = ({
  barStyle = 'light-content',
  backgroundColor,
}: PlatformStatusBarProps) => {
  const theme = useZestTheme();

  if (!PlatformIs.android()) {
    return null;
  }

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

**Key patterns demonstrated:**
- useZestTheme() for direct theme access
- theme.alias.color.brand.background.default for brand color
- backgroundColor prop with theme fallback (backgroundColor || theme.alias...)
- Platform-specific rendering (Android-only)
- Early return pattern for iOS (return null)
- Default parameter values (barStyle = 'light-content')
- JSDoc documentation explaining behavior

## Example 6: useZestTheme in Navigation Header

**File**: `libs/navigation-header/useNavigationHeader.ts:1`

This example shows useZestTheme with useLayoutEffect for React Navigation header styling.

```typescript
import type { NavigationProp } from '@react-navigation/native';
import type { NativeStackNavigationOptions } from '@react-navigation/native-stack';
import { useLayoutEffect } from 'react';

import { useZestTheme } from '@zest/react-native';

/**
 * Hook to apply styled header configuration to navigation screens
 * Provides customizable defaults that match the brand styling
 */
export const useNavigationHeader = ({
  navigation,
  options = {},
}: UseNavigationHeaderProps) => {
  const theme = useZestTheme();

  useLayoutEffect(() => {
    const defaultOptions: NativeStackNavigationOptions = {
      headerShown: true,
      headerBackVisible: true,
      headerTitleAlign: 'left',
      headerBackButtonDisplayMode: 'minimal',
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
      headerStyle: {
        ...((defaultOptions.headerStyle as object) || {}),
        ...((options.headerStyle as object) || {}),
      },
    });
  }, [navigation, options, theme]);
};
```

**Key patterns demonstrated:**
- useZestTheme() in custom hook
- useLayoutEffect for synchronous header updates
- theme.global.fontFamily.headline for typography
- theme.global.fontSize.headline.headlineMd for font size
- theme.alias.color.neutral.foreground.inverse for text on brand background
- theme.alias.color.brand.background.default for header background
- Spread operators for merging default and custom options
- Type casting to object for style merging
- Dependencies array [navigation, options, theme]
- NativeStackNavigationOptions type for type safety

## Example 7: useZestTheme with useMemo

**File**: `operations/shoppable-product/useProductLabel.ts:1`

This example shows useZestTheme with useMemo for conditional theme-based styling.

```typescript
import { useMemo } from 'react';

import type { ShoppableProductCardFragmentFragment } from '@data-access/graphql';

import type { LabelProps } from '@features/product-card-feature/types';

import { useT9n } from '@libs/localization';

import { useZestTheme, type ColorType } from '@zest/react-native';

/**
 * Hook to get label properties for shoppable products.
 * Handles both regular product labels and sold out labels.
 */
export const useProductLabel = ({
  data,
  showSoldOut,
}: UseProductLabelProps): LabelProps | undefined => {
  const { translateRaw } = useT9n('recipe-detail');
  const theme = useZestTheme();

  return useMemo(() => {
    const labelText = (
      (showSoldOut
        ? translateRaw('recipe-detail.sold-out-label')
        : data?.text) ?? ''
    ).toUpperCase();

    if (!labelText || labelText === '') {
      return undefined;
    }

    if (showSoldOut) {
      return {
        text: labelText,
        backgroundColor: 'global.color.cherry.100' as ColorType,
        foregroundColor: 'global.color.cherry.600' as ColorType,
        borderColor: 'global.color.cherry.600' as ColorType,
      };
    }

    return {
      text: labelText,
      backgroundColor:
        (data?.style?.backgroundColor as ColorType) ??
        theme.alias.color.button.background,
      foregroundColor:
        (data?.style?.foregroundColor as ColorType) ??
        theme.alias.color.button.foreground,
    };
  }, [data, showSoldOut, theme, translateRaw]);
};
```

**Key patterns demonstrated:**
- useZestTheme() with useMemo for performance
- useMemo dependencies [data, showSoldOut, theme, translateRaw]
- Conditional theme-based logic (showSoldOut ? cherry : button colors)
- theme.alias.color.button.background fallback
- ColorType type casting for color strings
- Early return for empty label (return undefined)
- Ternary operators for conditional values
- Optional chaining (data?.style?.backgroundColor)
- Nullish coalescing (??) for fallbacks

## Example 8: useZestStyles with createStylesConfig

**File**: `modules/store/screens/storefront/components/week-header/styles.ts:1`

This example shows createStylesConfig with token strings extracted outside component.

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
- createStylesConfig() for type-safe token strings
- Extracted outside component (exported const)
- Token strings: 'alias.color.brand.background.default'
- Token strings: 'global.spacing.md2', 'global.borderWidth.lg'
- Token strings: 'global.fontFamily.headline', 'global.fontSize.body.bodyXs'
- Numeric values where tokens don't exist (minHeight: 60, fontWeight: 400)
- Percentage strings ('100%')
- Standard React Native style properties (flex, justifyContent, alignItems)
- Multiple style objects in single config

## Example 9: useZestStyles in Component

**File**: `modules/store/screens/storefront/components/week-header/single-week-header/active-week-content/ActiveWeekContent.tsx:1`

This example shows useZestStyles consuming the extracted StylesConfig.

```typescript
import type { WeekContentProps } from '@modules/store/screens/storefront/components/week-header/single-week-header/types';
import { weekHeaderStylesConfig } from '@modules/store/screens/storefront/components/week-header/styles';

import { Text, useZestStyles } from '@zest/react-native';

/**
 * ActiveWeekContent displays the delivery date information for a non-skipped week.
 * It shows the delivery day and date in standard formatting.
 */
export const ActiveWeekContent: React.FC<WeekContentProps> = ({ week }) => {
  const styles = useZestStyles(weekHeaderStylesConfig);

  return (
    <>
      <Text style={styles.deliveryDay}>{week.deliveryDay}</Text>
      <Text style={styles.deliveryDate}>{week.deliveryDate}</Text>
    </>
  );
};
```

**Key patterns demonstrated:**
- Import weekHeaderStylesConfig from separate file
- useZestStyles(weekHeaderStylesConfig) for token resolution
- styles.deliveryDay and styles.deliveryDate resolved automatically
- Text component from @zest/react-native
- React.FC with typed props (WeekContentProps)
- JSDoc documentation
- Fragment wrapper (<>...</>)
- Simple component structure

## Example 10: Testing with ZestProvider

**File**: `libs/zest/ZestProvider.test.tsx:1`

This example shows testing pattern with ZestProvider wrapper.

```typescript
import { screen } from '@testing-library/react-native';

import { renderWithProviders } from 'jest-utils';

import { Text } from '@zest/react-native';

import { ZestProvider } from './ZestProvider';

describe('<ZestProvider />', () => {
  it('should render children', () => {
    renderWithProviders(
      <ZestProvider>
        <Text testID="hello-world">{'hello world'}</Text>
      </ZestProvider>
    );

    expect(screen.getByTestId('hello-world')).toBeTruthy();
  });
});
```

**Key patterns demonstrated:**
- renderWithProviders helper wraps ZestProvider
- screen.getByTestId for element queries
- testID prop for test targeting
- Text component from @zest/react-native
- expect().toBeTruthy() for presence assertion
- describe and it blocks for test organization
- String literal in curly braces ({'hello world'})

## Summary

The YourCompany codebase consistently follows these Zest integration patterns:

1. **Provider Composition** - ZestProvider wrapped in ScreenEntryProvider, NavigationEntryProvider, WidgetEntryProvider with specific order
2. **Custom ZestProvider** - Wrapper around ZestThemeProvider with brand detection from native repository
3. **useZestTheme Hook** - Direct theme access for dynamic styling, always with useMemo for performance
4. **useZestStyles Hook** - Token-based styling with createStylesConfig extracted outside components
5. **Token Strings** - 'alias.color.brand.background.default', 'global.spacing.md' for automatic resolution
6. **Two-Layer Tokens** - Global tokens (primitives) and alias tokens (semantic colors)
7. **Theme Fallbacks** - backgroundColor || theme.alias.color.brand.background.default pattern
8. **useLayoutEffect** - For synchronous header updates in navigation hooks
9. **useMemo** - For theme-based computed styles to prevent recalculation
10. **Testing** - renderWithProviders or custom renderWithZest wrapper for theme context

These patterns ensure consistent theming, automatic dark mode support, optimal performance, and maintainable code throughout the app.
