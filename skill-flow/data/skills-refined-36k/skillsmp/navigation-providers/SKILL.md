---
name: navigation-providers
description: "WHAT: Entry provider hierarchy for navigation stacks, screens, and widgets. WHEN: wrapping stacks with context, creating standalone screens, building embeddable widgets. KEYWORDS: provider, NavigationEntryProvider, ScreenEntryProvider, WidgetEntryProvider, context, HOC, entry, createContext."
---

# Navigation Providers

## Core Principles

**Use entry providers to establish application context hierarchy.** Providers wrap components with necessary context like navigation, theming, data access, query clients, and error boundaries.

**Always throw error if context is used without provider.** This prevents runtime errors and makes debugging easier by failing fast with clear error messages.

**Memoize provider values with useMemo.** This prevents unnecessary re-renders of context consumers when provider props haven't changed.

**Why**: Providers establish the runtime environment and ensure all components have access to required services in the correct order.

## When to Use This Skill

Use these patterns when:

- Wrapping navigation stacks with full app context
- Creating standalone screens without navigation container
- Building embeddable widgets with minimal context
- Implementing custom context providers for feature-specific state
- Ensuring critical data is loaded before rendering (repository loading)
- Creating HOCs for reusable provider wrapping
- Testing components that require provider context
- Optimizing performance by preventing unnecessary re-renders

## Entry Provider Hierarchy

### NavigationEntryProvider

Highest-level provider for navigation-based modules with full app context:

```typescript
import { NavigationEntryProvider } from '@entry-providers';
import { REPOSITORY_KEYS } from '@data-access/native/constants';

<NavigationEntryProvider
  linking={linkingConfig}
  requiredRepositories={{
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
    [REPOSITORY_KEYS.auth]: ['authToken'],
  }}
  repositoryLoadingFallback={LoadingSpinner}
>
  <Stack.Navigator>
    <Stack.Screen name="Home" component={HomeScreen} />
    <Stack.Screen name="Recipe" component={RecipeScreen} />
  </Stack.Navigator>
</NavigationEntryProvider>
```

**Why**: NavigationEntryProvider wraps the entire navigation stack with all necessary context including navigation container, deep linking, and repository loading validation.

**Includes:**
- ScreenEntryProvider (all screen-level providers)
- NavigationContainer (React Navigation)
- Deep linking configuration
- Repository loading validation

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:86`

### ScreenEntryProvider

Mid-level provider for individual screens without navigation container:

```typescript
import { ScreenEntryProvider } from '@entry-providers';

<ScreenEntryProvider>
  <RecipeDetailsScreen />
</ScreenEntryProvider>
```

**Why**: ScreenEntryProvider provides screen-level context without navigation overhead, perfect for standalone screens.

**Includes:**
- QueryClientProvider (TanStack Query)
- ApolloProvider (GraphQL)
- SafeAreaProvider (Safe area insets)
- AppWithTranslation (i18n)
- ZestProvider (Design system)
- ErrorBoundary (Error handling)

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:129`

### WidgetEntryProvider

Lightweight provider for widgets and embeddable components:

```typescript
import { WidgetEntryProvider } from '@entry-providers';

<WidgetEntryProvider>
  <RecipeCard recipe={recipe} />
</WidgetEntryProvider>
```

**Why**: WidgetEntryProvider provides minimal context for embeddable components, excluding navigation and safe area handling.

**Includes:**
- QueryClientProvider (TanStack Query)
- ApolloProvider (GraphQL)
- AppWithTranslation (i18n)
- ZestProvider (Design system)
- ErrorBoundary (Error handling)

**Excludes:**
- NavigationContainer (not needed for widgets)
- SafeAreaProvider (widgets manage their own insets)

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:172`

## Provider Implementation

### ScreenEntryProvider Structure

The provider nests context providers in specific order:

```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import { ApolloProviderWrapper } from '@libs/graphql/providers/ApolloProviderWrapper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AppWithTranslation } from '@libs/localization';
import { ZestProvider } from '@libs/zest';
import { ErrorBoundary } from '@libs/error-boundary';
import { queryClient } from '@libs/query';
import { QueryCacheManager } from '@libs/cache';

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

**Why**: Explicit provider hierarchy ensures correct context nesting and initialization order. Inner providers can depend on outer providers.

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:129`

### NavigationEntryProvider Structure

Adds navigation and repository loading to ScreenEntryProvider:

```typescript
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

**Why**: NavigationEntryProvider adds navigation and repository loading to ScreenEntryProvider. Conditional RepositoryLoader only renders when required repositories are specified.

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:86`

## Higher-Order Components

### withNavigationEntryProvider

HOC for wrapping components with NavigationEntryProvider:

```typescript
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

**Why**: HOC pattern enables reusable provider wrapping with proper display names for debugging.

**Usage:**

```typescript
import { withNavigationEntryProvider } from '@entry-providers';
import { REPOSITORY_KEYS } from '@data-access/native/constants';

export const SocialRecipeBridgeStackWithProvider = withNavigationEntryProvider(
  SocialRecipeBridgeStack,
  linkingConfig,
  {
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
  },
  LoadingSpinner
);
```

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/stacks/social-recipe-bridge/SocialRecipeBridgeStack.tsx:79`

### withWidgetEntryProvider

HOC for wrapping components with WidgetEntryProvider:

```typescript
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

**Usage:**

```typescript
import { withWidgetEntryProvider } from '@entry-providers';

const RecipeCardWithProviders = withWidgetEntryProvider(RecipeCard);
```

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:279`

## Custom Context Pattern

### Create Context with Error Handling

Always throw error if context is used without provider:

```typescript
import { createContext, useContext, useMemo } from 'react';

type ContextType = {
  subscriptionId: string;
  deeplinkVoucherCode: string;
  dcId?: string;
  shouldTriggerReactivationWebView?: boolean;
};

const ReactivationBannerContext = createContext<ContextType>({} as ContextType);

export const useReactivationBannerContext = (): ContextType => {
  const context = useContext(ReactivationBannerContext);

  if (!context) {
    throw new Error(
      'useReactivationBannerContext must be used within ReactivationBannerProvider'
    );
  }

  return context;
};

export const ReactivationBannerProvider: React.FC<PropsWithChildren> = ({
  children,
  subscriptionId,
  deeplinkVoucherCode,
  dcId,
  shouldTriggerReactivationWebView,
}) => {
  const contextValue = useMemo(() => ({
    subscriptionId,
    deeplinkVoucherCode,
    dcId,
    shouldTriggerReactivationWebView,
  }), [subscriptionId, deeplinkVoucherCode, dcId, shouldTriggerReactivationWebView]);

  return (
    <ReactivationBannerContext.Provider value={contextValue}>
      {children}
    </ReactivationBannerContext.Provider>
  );
};
```

**Why**: Error throwing prevents runtime errors from missing providers and makes debugging easier. useMemo prevents unnecessary re-renders.

**Production Example**: `git-resources/shared-mobile-modules/src/features/reactivation-banner-feature/state-management/context/ReactivationBannerContext.tsx:10`

### Context with Hook Integration

Integrate custom hooks with context providers:

```typescript
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
```

**Why**: Custom hooks can encapsulate complex logic and side effects, keeping provider component clean. useMemo ensures params object reference stability.

**Production Example**: `git-resources/shared-mobile-modules/src/features/reactivation-banner-feature/state-management/context/ReactivationBannerContext.tsx:12`

## Provider Composition Rules

### 1. Order Matters

Providers must be nested in specific order:

1. Data providers (QueryClient, Apollo) - outermost
2. Platform providers (SafeArea)
3. App providers (i18n, Theme)
4. Error boundaries - innermost (catch all errors)

```typescript
// ✅ Correct order
<QueryClientProvider>
  <ApolloProvider>
    <SafeAreaProvider>
      <AppWithTranslation>
        <ZestProvider>
          <ErrorBoundary>
            {children}
          </ErrorBoundary>
        </ZestProvider>
      </AppWithTranslation>
    </SafeAreaProvider>
  </ApolloProvider>
</QueryClientProvider>
```

**Why**: Inner providers can depend on outer providers, but not vice versa. ErrorBoundary should be innermost to catch all errors.

### 2. Single Source of Truth

Never create multiple instances of the same provider type:

```typescript
// ❌ Wrong - Multiple QueryClientProviders
<QueryClientProvider client={queryClient1}>
  <Screen1 />
  <QueryClientProvider client={queryClient2}>
    <Screen2 />
  </QueryClientProvider>
</QueryClientProvider>

// ✅ Correct - Single instance
<QueryClientProvider client={queryClient}>
  <Screen1 />
  <Screen2 />
</QueryClientProvider>
```

**Why**: Multiple instances cause data inconsistencies and cache duplication.

### 3. Repository Loading

Use requiredRepositories to validate data before rendering:

```typescript
<NavigationEntryProvider
  requiredRepositories={{
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
    [REPOSITORY_KEYS.auth]: ['authToken'],
    [REPOSITORY_KEYS.plan]: ['currentPlan'],
  }}
  repositoryLoadingFallback={LoadingSpinner}
>
  <App />
</NavigationEntryProvider>
```

**Why**: Ensures critical data is loaded before rendering, preventing downstream errors from missing data.

## Testing with Providers

### Test Wrapper

Create test wrapper with all providers:

```typescript
// __tests__/testUtils.tsx
import { ReactNode } from 'react';
import { ScreenEntryProvider } from '@entry-providers';

export const TestProviders = ({ children }: { children: ReactNode }) => (
  <ScreenEntryProvider>
    {children}
  </ScreenEntryProvider>
);

export const renderWithProviders = (ui: ReactElement) => {
  return render(<TestProviders>{ui}</TestProviders>);
};
```

**Usage:**

```typescript
import { renderWithProviders } from '@__tests__/testUtils';

test('renders recipe card', () => {
  renderWithProviders(<RecipeCard recipe={mockRecipe} />);
  expect(screen.getByText('Chicken Tikka')).toBeTruthy();
});
```

**Why**: Test wrapper ensures components have required context during tests without duplicating provider setup.

## Performance Considerations

### Memoize Provider Values

Prevent unnecessary re-renders by memoizing provider values:

```typescript
export const MyProvider: React.FC<PropsWithChildren> = ({
  children,
  value1,
  value2,
}) => {
  const value = useMemo(() => ({
    value1,
    value2,
  }), [value1, value2]);

  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  );
};
```

**Why**: Memoization prevents context consumers from re-rendering when values haven't changed.

### Split Contexts

Split large contexts into smaller, focused contexts:

```typescript
// ❌ Large monolithic context
const AppContext = createContext({
  user,
  theme,
  settings,
  analytics,
  // ... many values
});

// ✅ Split into focused contexts
const UserContext = createContext({ user });
const ThemeContext = createContext({ theme });
const SettingsContext = createContext({ settings });
```

**Why**: Smaller contexts reduce re-renders by limiting dependencies. Components only re-render when their specific context changes.

## Common Mistakes to Avoid

❌ **Don't create providers without error handling**:

```typescript
// ❌ Wrong - No error check
const Context = createContext<ContextType>({} as ContextType);
const useMyContext = () => useContext(Context);
```

✅ **Do throw error for missing provider**:

```typescript
// ✅ Correct - Error thrown if provider missing
const useMyContext = () => {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be used within MyProvider');
  }
  return context;
};
```

❌ **Don't nest providers incorrectly**:

```typescript
// ❌ Wrong - QueryClient should be outer
<ZestProvider>
  <QueryClientProvider>
    <App />
  </QueryClientProvider>
</ZestProvider>
```

✅ **Do follow correct nesting order**:

```typescript
// ✅ Correct - Data providers first, theme providers after
<QueryClientProvider>
  <ZestProvider>
    <App />
  </ZestProvider>
</QueryClientProvider>
```

❌ **Don't create unnecessary custom providers**:

```typescript
// ❌ Wrong - Simple state doesn't need provider
const MyStateProvider = ({ children }) => {
  const [state, setState] = useState();
  return <Context.Provider value={{ state, setState }}>{children}</Context.Provider>;
};
```

✅ **Do use appropriate state management**:

```typescript
// ✅ Correct - Use Zustand store for simple state
import { create } from 'zustand';

const useMyStore = create((set) => ({
  state: null,
  setState: (state) => set({ state }),
}));
```

❌ **Don't forget to memoize context values**:

```typescript
// ❌ Wrong - New object reference on every render
const MyProvider = ({ children, value1, value2 }) => {
  const value = { value1, value2 }; // New object every render
  return <MyContext.Provider value={value}>{children}</MyContext.Provider>;
};
```

✅ **Do memoize with useMemo**:

```typescript
// ✅ Correct - Stable object reference
const MyProvider = ({ children, value1, value2 }) => {
  const value = useMemo(() => ({ value1, value2 }), [value1, value2]);
  return <MyContext.Provider value={value}>{children}</MyContext.Provider>;
};
```

## Quick Reference

**Use NavigationEntryProvider for stacks:**
```typescript
<NavigationEntryProvider linking={linkingConfig}>
  <Stack.Navigator />
</NavigationEntryProvider>
```

**Use ScreenEntryProvider for standalone screens:**
```typescript
<ScreenEntryProvider>
  <RecipeDetailsScreen />
</ScreenEntryProvider>
```

**Use WidgetEntryProvider for widgets:**
```typescript
<WidgetEntryProvider>
  <RecipeCard />
</WidgetEntryProvider>
```

**Create custom context with error handling:**
```typescript
const MyContext = createContext<ContextType>({} as ContextType);

const useMyContext = () => {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be used within MyProvider');
  }
  return context;
};

const MyProvider = ({ children, ...props }) => {
  const value = useMemo(() => ({ ...props }), [props]);
  return <MyContext.Provider value={value}>{children}</MyContext.Provider>;
};
```

**Wrap stack with HOC:**
```typescript
export const StackWithProvider = withNavigationEntryProvider(
  MyStack,
  linkingConfig,
  { [REPOSITORY_KEYS.appConfig]: ['locale'] },
  LoadingSpinner
);
```

**Key Libraries:**
- React Navigation 7.0.13
- TanStack Query 5.59.16
- Apollo Client 3.13.6
- React Native 0.75.4
- @zest/react-native 1.3.1

For production examples, see [references/examples.md](references/examples.md).
