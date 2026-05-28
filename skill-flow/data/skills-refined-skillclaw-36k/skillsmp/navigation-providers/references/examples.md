# Navigation Providers - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating provider patterns.

## Example 1: ScreenEntryProvider Implementation

**File**: `entry-providers/providers.tsx:129`

This example shows the complete ScreenEntryProvider implementation with full context hierarchy.

```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import type { PropsWithChildren } from 'react';
import { DevToolsBubble } from 'react-native-react-query-devtools';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Toast } from '@features/toast-feature';
import { QueryCacheManager } from '@libs/cache';
import { ErrorBoundary } from '@libs/error-boundary';
import { ApolloProviderWrapper } from '@libs/graphql/providers/ApolloProviderWrapper';
import { AppWithTranslation } from '@libs/localization';
import { useLoyaltyStateManager } from '@libs/loyalty-state-manager';
import { queryClient } from '@libs/query';
import { ZestProvider } from '@libs/zest';

/**
 * Global manager that handles loyalty state changes and invalidates caches.
 * This ensures that when loyalty program state changes, all related data is refreshed.
 */
const GlobalLoyaltyStateManager: React.FC = () => {
  useLoyaltyStateManager();
  return null;
};

/**
 * ScreenEntryProvider is a higher-order component that provides essential context
 * for components displayed in a single full-screen mode.
 */
export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
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
        {__DEV__ && <DevToolsBubble queryClient={queryClient} />}
      </ApolloProviderWrapper>
    </QueryClientProvider>
  );
};
```

**Key patterns demonstrated:**
- QueryClientProvider at outermost level
- ApolloProviderWrapper for GraphQL
- QueryCacheManager and GlobalLoyaltyStateManager for state management
- SafeAreaProvider for safe area insets
- AppWithTranslation for i18n
- ZestProvider for design system
- ErrorBoundary innermost to catch all errors
- DevToolsBubble only in development
- Global managers as components returning null
- Explicit provider nesting order

## Example 2: NavigationEntryProvider Implementation

**File**: `entry-providers/providers.tsx:86`

This example shows NavigationEntryProvider with conditional repository loading.

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { RepositoryLoader } from '@libs/repository-loader';
import type { NavigationEntryProviderProps } from './types';

/**
 * NavigationEntryProvider wraps a navigation stack.
 * It provides the necessary context for navigation and deep linking within the app.
 * Now supports optional repository loading to ensure critical data is available before rendering.
 *
 * @param props.requiredRepositories - Optional map of repository keys to required properties
 * @param props.repositoryLoadingFallback - Optional custom loading component
 * @param props.linking - Optional deep linking configuration
 *
 * @example
 * // Basic usage without repository loading
 * <NavigationEntryProvider linking={linkingConfig}>
 *   <Stack.Navigator>
 *     // ... screens
 *   </Stack.Navigator>
 * </NavigationEntryProvider>
 *
 * // Usage with repository loading
 * <NavigationEntryProvider
 *   linking={linkingConfig}
 *   requiredRepositories={{
 *     [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
 *     [REPOSITORY_KEYS.auth]: ['authToken']
 *   }}
 *   repositoryLoadingFallback={LoadingSpinner}
 * >
 *   <Stack.Navigator>
 *     // ... screens
 *   </Stack.Navigator>
 * </NavigationEntryProvider>
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
- Generic type parameter <StackType extends object>
- ScreenEntryProvider wraps everything
- NavigationContainer with linking config
- Conditional RepositoryLoader rendering
- Object.keys check for required repositories
- Toast component included in both branches
- JSDoc comments with examples
- Multiple usage patterns documented

## Example 3: WidgetEntryProvider Implementation

**File**: `entry-providers/providers.tsx:172`

This example shows lightweight WidgetEntryProvider for embeddable components.

```typescript
/**
 * WidgetEntryProvider is designed for wrapping individual
 * Components (i.e.: Widgets) that will be displayed within a Screen.
 *
 * This provider is typically used for smaller, self-contained components that do not
 * require full-screen context.
 *
 * @example
 * import { WidgetEntryProvider } from './providers';
 *
 * const AuthFormWrapper = () => (
 *   <WidgetEntryProvider>
 *     <AuthForm />
 *   </WidgetEntryProvider>
 * );
 */
export const WidgetEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
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
- Same structure as ScreenEntryProvider
- Missing SafeAreaProvider (widgets manage own insets)
- No DevToolsBubble (not needed for widgets)
- Lighter weight than ScreenEntryProvider
- Still includes query clients and theme
- ErrorBoundary included for error handling
- JSDoc with usage example

## Example 4: withNavigationEntryProvider HOC

**File**: `entry-providers/providers.tsx:227`

This example shows HOC pattern for wrapping components with NavigationEntryProvider.

```typescript
import type {
  WithNavigationEntryProviderHOC,
} from './types';

/**
 * Enhanced HOC to wrap a component with NavigationEntryProvider that supports repository loading.
 *
 * You can use this HOC to wrap a stack navigator component with the `NavigationEntryProvider`.
 * This is useful when you want to utilize provider context for zest or localization
 * directly in the stack navigator, and optionally ensure critical data is loaded first.
 *
 * @example
 * // Inside Stack Navigator index.tsx with repository loading
 * import { withNavigationEntryProvider, registerStack } from '@entry-providers';
 * import { REPOSITORY_KEYS } from '@data-access/native/constants';
 *
 * import { OnboardingStack } from './OnboardingStack';
 * import { OnboardingStackProps, OnboardingStackParamsList } from './types';
 *
 * registerStack('Onboarding', () =>
 *  withNavigationEntryProvider<OnboardingStackParamsList, OnboardingStackProps>(
 *    OnboardingStack,
 *    undefined, // linking config
 *    {
 *      [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
 *      [REPOSITORY_KEYS.auth]: ['authToken']
 *    }, // required repositories
 *    LoadingSpinner // loading fallback
 *  )
 * );
 *
 * @template TParams - Navigation parameter list type.
 * @template P - Props of the wrapped component.
 */
export const withNavigationEntryProvider: WithNavigationEntryProviderHOC = (
  WrappedComponent,
  linking,
  requiredRepositories,
  repositoryLoadingFallback
) => {
  const ComponentWithProvider = (props: object & JSX.IntrinsicAttributes) => (
    <NavigationEntryProvider
      linking={linking}
      requiredRepositories={requiredRepositories}
      repositoryLoadingFallback={repositoryLoadingFallback}
    >
      <WrappedComponent
        {...(props as React.ComponentProps<typeof WrappedComponent>)}
      />
    </NavigationEntryProvider>
  );

  ComponentWithProvider.displayName = `withNavigationEntryProvider(${
    WrappedComponent.displayName || WrappedComponent.name || 'Component'
  })`;

  return ComponentWithProvider;
};
```

**Key patterns demonstrated:**
- HOC function pattern
- Takes WrappedComponent and config params
- Returns new component with provider
- Sets displayName for debugging
- Fallback chain for displayName (displayName || name || 'Component')
- Type casting for props (object & JSX.IntrinsicAttributes)
- Comprehensive JSDoc with example
- Template types documented

## Example 5: withWidgetEntryProvider HOC

**File**: `entry-providers/providers.tsx:279`

This example shows HOC pattern for wrapping widgets.

```typescript
/**
 * Enhanced HOC to wrap a component with WidgetEntryProvider.
 *
 * You can use this HOC to wrap a widget component with the `WidgetEntryProvider`.
 * This is useful when you want to utilize provider context for zest or localization
 * directly in the widget.
 *
 * @example
 * // Inside Widget index.tsx
 * import { withWidgetEntryProvider, registerWidget } from '@entry-providers';
 *
 * import { FactorFormPopUp } from './FactorFormPopUp';
 *
 * registerWidget('FactorFormPopUp', () =>
 *  withWidgetEntryProvider<FactorFormPopUpProps>(
 *    FactorFormPopUp,
 *  )
 * );
 *
 * @template P - Props of the wrapped component.
 */
export const withWidgetEntryProvider: WithWidgetEntryProviderHOC = (
  WrappedComponent
) => {
  const ComponentWithProvider = (props: object & JSX.IntrinsicAttributes) => (
    <WidgetEntryProvider>
      <WrappedComponent
        {...(props as React.ComponentProps<typeof WrappedComponent>)}
      />
    </WidgetEntryProvider>
  );

  ComponentWithProvider.displayName = `withWidgetEntryProvider(${
    WrappedComponent.displayName || WrappedComponent.name || 'Component'
  })`;

  return ComponentWithProvider;
};
```

**Key patterns demonstrated:**
- Simpler HOC (no linking or repository params)
- Same displayName pattern
- Same type casting pattern
- JSDoc with example
- Template type documented

## Example 6: Using withNavigationEntryProvider

**File**: `modules/social-recipe-bridge/stacks/social-recipe-bridge/SocialRecipeBridgeStack.tsx:79`

This example shows real usage of withNavigationEntryProvider HOC.

```typescript
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { withNavigationEntryProvider } from '@entry-providers';
import { TracingProvider } from '@libs/tracing';
import { SocialRecipeBridgeStackRoutes } from '../../types';
import { SocialRecipeBridgeScreen } from '../../screens/social-recipe-bridge/SocialRecipeBridgeScreen';
import { CookbookFaqScreen } from '../../screens/cookbook-faq';
import { RecipeDetailScreen } from '../../screens/recipe-detail';
import { EditRecipeScreen } from '../../screens/edit-recipe';
import { linkingConfig } from './linking';

export type SocialRecipeBridgeStackParamsList = {
  [SocialRecipeBridgeStackRoutes.SocialRecipeBridge]: SocialRecipeBridgeScreenParams;
  [SocialRecipeBridgeStackRoutes.CookbookFaq]: undefined;
  [SocialRecipeBridgeStackRoutes.RecipeDetail]: RecipeDetailScreenParams;
  [SocialRecipeBridgeStackRoutes.EditRecipe]: EditRecipeScreenParams;
};

const Stack = createNativeStackNavigator<
  SocialRecipeBridgeStackParamsList,
  StackNavigatorIDs.SocialRecipeBridge
>();

export const SocialRecipeBridgeStackInternal = ({
  initialRouteName,
}: Navigation.StackNavigatorInitialProps<SocialRecipeBridgeStackParamsList>) => {
  return (
    <Stack.Navigator
      id={StackNavigatorIDs.SocialRecipeBridge}
      initialRouteName={initialRouteName}
      screenOptions={{
        headerShown: true,
      }}
    >
      <Stack.Screen
        name={SocialRecipeBridgeStackRoutes.SocialRecipeBridge}
        component={SocialRecipeBridgeScreen}
      />
      <Stack.Screen
        name={SocialRecipeBridgeStackRoutes.CookbookFaq}
        component={CookbookFaqScreen}
      />
      <Stack.Screen
        name={SocialRecipeBridgeStackRoutes.RecipeDetail}
        component={RecipeDetailScreen}
      />
      <Stack.Screen
        name={SocialRecipeBridgeStackRoutes.EditRecipe}
        component={EditRecipeScreen}
        options={{
          headerShown: true,
          headerBackButtonMenuEnabled: false,
        }}
      />
    </Stack.Navigator>
  );
};

const SocialRecipeBridgeStack = (
  initialProps: Navigation.StackNavigatorInitialProps<SocialRecipeBridgeStackParamsList>
) => (
  <TracingProvider
    moduleType="stack"
    moduleName="social-recipe-bridge"
    squad="client-platform"
  >
    <SocialRecipeBridgeStackInternal {...initialProps} />
  </TracingProvider>
);

// Wrap with NavigationEntryProvider using HOC
export const SocialRecipeBridgeStackWithProvider = withNavigationEntryProvider(
  SocialRecipeBridgeStack,
  linkingConfig
);
```

**Key patterns demonstrated:**
- Type definitions for stack params
- createNativeStackNavigator with typed params
- Internal stack component (SocialRecipeBridgeStackInternal)
- Wrapper stack with TracingProvider
- Final export wrapped with withNavigationEntryProvider
- Linking config passed to HOC
- No required repositories (undefined)
- Stack.Navigator with id and initialRouteName
- Multiple Stack.Screen definitions
- Per-screen options customization

## Example 7: Custom Context with Error Handling

**File**: `features/reactivation-banner-feature/state-management/context/ReactivationBannerContext.tsx:10`

This example shows custom context creation with error handling and useMemo optimization.

```typescript
import React, { createContext, useContext, useMemo } from 'react';
import { useReactivationBanner } from '../hooks';
import type {
  ReactivationBannerContextType as ContextType,
  ReactivationBannerProviderProps,
} from './types';

const ReactivationBannerContext = createContext<ContextType>({} as ContextType);

export const ReactivationBannerProvider: React.FC<
  ReactivationBannerProviderProps
> = ({
  children,
  subscriptionId,
  deeplinkVoucherCode,
  dcId,
  shouldTriggerReactivationWebView,
}) => {
  const reactivationBannerParams = useMemo(() => {
    return {
      subscriptionId,
      deeplinkVoucherCode,
      dcId,
      shouldTriggerReactivationWebView,
    };
  }, [
    subscriptionId,
    deeplinkVoucherCode,
    dcId,
    shouldTriggerReactivationWebView,
  ]);

  // Use custom hook to compute context value
  const contextValue = useReactivationBanner(reactivationBannerParams);

  return (
    <ReactivationBannerContext.Provider value={contextValue}>
      {children}
    </ReactivationBannerContext.Provider>
  );
};

export const useReactivationBannerContext = (): ContextType => {
  const context = useContext(ReactivationBannerContext);

  if (!context) {
    throw new Error(
      'useReactivationBannerContext must be used within ReactivationBannerProvider'
    );
  }
  return context;
};
```

**Key patterns demonstrated:**
- createContext with type assertion ({} as ContextType)
- Custom hook for context usage (useReactivationBannerContext)
- Error throwing if context is undefined
- Clear error message naming provider
- useMemo for params object
- Custom hook integration (useReactivationBanner)
- All props listed in useMemo dependency array
- Type imports from ./types

## Summary

The YourCompany codebase consistently follows these provider patterns:

1. **Entry provider hierarchy**: NavigationEntryProvider → ScreenEntryProvider → WidgetEntryProvider
2. **Provider nesting order**: Data providers (Query/Apollo) → Platform (SafeArea) → App (i18n/Theme) → ErrorBoundary
3. **HOC pattern** for reusable provider wrapping with displayName
4. **Custom contexts** with error handling and useMemo optimization
5. **Repository loading** for conditional data validation before rendering
6. **Global managers** as components returning null
7. **Conditional rendering** for optional features (DevToolsBubble, RepositoryLoader)
8. **Type safety** with generic types and typed props
9. **JSDoc comments** documenting usage patterns
10. **displayName fallback chain** for debugging (displayName || name || 'Component')

These patterns ensure consistent context hierarchy, proper error handling, and optimal performance throughout the app.
