---
name: file-organization
description: "WHAT: 6-tier module system for React Native code organization. WHEN: structuring new features, creating modules, refactoring code architecture. KEYWORDS: modules, features, operations, libs, tiers, folder structure, architecture, organization, imports, dependencies."
---

# File Organization Standards

Standards for organizing files and folders in React Native projects using a modular, scalable architecture.

## When to Use

Use these standards when:
- Creating new modules, features, or screens
- Refactoring existing code to reduce coupling
- Planning architecture for new capabilities
- Reviewing code for proper tier placement
- Setting up path aliases and imports
- Establishing team ownership boundaries

## Core Principles

### 6-Tier Module System

The architecture uses six tiers that organize code with unidirectional dependencies:

```
Entry Providers (Tier 1)  →  Top-level initialization
        ↓
Modules (Tier 2)          →  Domain-specific containers
        ↓
Features (Tier 3)         →  Reusable UI components
        ↓
Operations (Tier 4)       →  Business logic (no UI)
        ↓
Data Access (Tier 5)      →  API layer
        ↓
Libs (Tier 6)             →  Infrastructure utilities
```

**Import Rule**: Higher tiers can import from lower tiers, but NOT vice versa.

**Why**: Unidirectional dependencies prevent circular imports, reduce coupling, and make the blast radius of changes predictable.

### Tier Descriptions

| Tier | Purpose | Examples |
|------|---------|----------|
| **Entry Providers** | Initialize services, wrap entry points | `ScreenCommonProvider`, `registerScreen` |
| **Modules** | Domain-specific containers | `sign-in`, `home`, `onboarding` |
| **Features** | Reusable UI with business logic | `auth-form`, `product-card` |
| **Operations** | Business logic without UI | `useSignIn`, `meal-selection` |
| **Data Access** | API calls and data fetching | `signIn()`, `useGetRecipes` |
| **Libs** | Infrastructure utilities | `analytics`, `error-boundary` |

## Tier 1: Entry Providers

Entry providers initialize infrastructure and serve as entry points for screens.

**Structure:**
```
src/entry-providers/
├── .claim.json              # Ownership: mobile-foundation
├── index.ts
├── providers.tsx            # ScreenCommonProvider
├── registers.ts             # registerScreen function
└── types.ts
```

**Example:**
```typescript
// Initializes QueryClient, SafeArea, Translation, Zest, ErrorBoundary
export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => (
  <QueryClientProvider client={queryClient}>
    <SafeAreaProvider>
      <AppWithTranslation>
        <ZestProvider>
          <ErrorBoundary scope={{ moduleName: 'App' }}>
            {children}
          </ErrorBoundary>
        </ZestProvider>
      </AppWithTranslation>
    </SafeAreaProvider>
  </QueryClientProvider>
);
```

**Rules:**
- ✅ Can import from Libs only
- ✅ Can cross-import from other Entry Providers
- ✅ Must be owned by mobile-foundation team

**Why**: Centralizes infrastructure setup, ensuring consistent initialization across all screens.

## Tier 2: Modules

Modules are domain-specific containers grouping screens, stacks, and non-reusable components.

**Structure:**
```
src/modules/{module-name}/
├── .claim.json              # Team ownership
├── index.ts
├── stacks/
│   └── {stack-name}/
│       └── {StackName}Stack.tsx
├── screens/
│   └── {screen-name}/
│       ├── index.ts
│       ├── {ScreenName}.tsx
│       ├── {ScreenName}.test.tsx
│       ├── constants.ts     # TEST_IDS
│       └── hooks/
└── components/              # Non-reusable components
```

**Example:**
```typescript
// src/modules/sign-in/screens/sign-in/SignIn.tsx
const SignInModule = () => (
  <ErrorBoundary scope={{ moduleName: 'SignIn' }}>
    <Header />
    <AuthForm />  {/* From @features */}
  </ErrorBoundary>
);

const SignInModuleWrapper = () => (
  <ScreenEntryProvider>
    <SignInModule />
  </ScreenEntryProvider>
);

registerScreen('SignIn', () => SignInModuleWrapper);
```

**Rules:**
- ✅ Can import from Features, Operations, Data Access, Libs
- ❌ Cannot cross-import from other Modules
- ✅ Can contain non-reusable components
- ✅ Each module has team ownership (.claim.json)

**Why**: Modules isolate domain logic, reducing blast radius when changes are made to a specific business area.

## Tier 3: Features

Features are **reusable UI components** with business logic, used across multiple modules.

**Structure:**
```
src/features/{feature-name}/
├── .claim.json              # Team ownership
├── index.ts
├── {FeatureName}.tsx
├── {FeatureName}.test.tsx
├── types.ts
├── constants.ts
├── components/              # Sub-components
└── variants/                # Optional: loading, edit, view states
    ├── loading/
    └── edit/
```

**Example:**
```typescript
// src/features/auth-form/AuthForm.tsx
import { Button, Input } from '@zest/react-native';
import { useSignIn } from '@operations/auth';  // Business logic from operations

export const AuthForm = () => {
  const mutation = useSignIn();

  const onSubmit = () => {
    mutation.mutate({
      username: usernameRef.current,
      password: passwordRef.current,
    });
  };

  return (
    <>
      <Input placeholder="Username" />
      <Input placeholder="Password" secureTextEntry />
      <Button title="Sign In" onPress={onSubmit} />
    </>
  );
};
```

**Rules:**
- ✅ Must be reusable (used in 2+ modules)
- ✅ Can import from Operations, Data Access, Libs, other Features
- ❌ Cannot import from Modules or Entry Providers
- ✅ Use variants/ for different states (loading, edit, view)

**Why**: Features promote UI reusability and maintain consistent patterns across the app.

## Tier 4: Operations

Operations contain reusable business logic without UI components.

**Structure:**
```
src/operations/{operation-name}/
├── .claim.json              # Team ownership
├── index.ts
├── mutations/               # Business mutations
│   └── onAddProduct.ts
├── selectors.ts             # State selectors
└── utils.ts
```

**Example:**
```typescript
// src/operations/auth/useSignIn.ts
import { useMutation } from '@tanstack/react-query';
import { signIn } from '@data-access/native/auth';
import { usePerformanceTracker } from '@libs/observability';

export const useSignIn = () => {
  const { startTrace, stopTrace } = usePerformanceTracker('SignIn');

  return useMutation({
    mutationFn: (data: SignInData) => signIn(data),
    onMutate: () => startTrace(),
    onSettled: () => stopTrace(),
  });
};
```

**Rules:**
- ✅ Business logic without UI
- ✅ Can import from Data Access, Libs, other Operations
- ❌ Cannot import from Features, Modules, Entry Providers

**Why**: Operations centralize business logic for reuse across features, wrapping data access with additional concerns (analytics, performance tracking).

## Tier 5: Data Access

Data Access is the API layer managing all external data sources.

**Structure:**
```
src/data-access/
├── .claim.json              # Ownership: mobile-foundation
├── graphql/                 # GraphQL queries
│   ├── queries/
│   └── mutations/
├── native/                  # Native module data
│   └── repositories/
├── query/                   # TanStack Query hooks
│   ├── hooks/
│   └── services/
└── maestro/                 # Test data
```

**Example:**
```typescript
// src/data-access/native/signIn.ts
import { sendEvent } from '@libs/native-modules/events';

export const signIn = async (signInData: SignInData) => {
  return await sendEvent('signIn', {
    payload: JSON.stringify(signInData),
  });
};
```

**Rules:**
- ✅ Can only import from Libs
- ❌ Cannot cross-import from other Data Access modules
- ✅ Use repository pattern for native data
- ✅ Use TanStack Query for REST APIs
- ✅ Use GraphQL for complex fetching

**Why**: Centralizing data access makes testing easier (single mock point) and maintains consistency in API patterns.

## Tier 6: Libs

Libs are business-agnostic infrastructure utilities.

**Structure:**
```
src/libs/{lib-name}/
├── .claim.json              # Ownership: mobile-foundation
├── index.ts
├── {LibName}.ts
└── types.ts
```

**Example:**
```typescript
// src/libs/observability/usePerformanceTracker.ts
import { SharedModulesPerformanceTracker } from '@libs/native-modules/performanceTracker';

export const usePerformanceTracker = (traceName: string) => {
  const { start, stop } = SharedModulesPerformanceTracker;

  return {
    startTrace: () => start(traceName),
    stopTrace: () => stop(traceName),
  };
};
```

**Rules:**
- ✅ Business-agnostic utilities
- ✅ Can import from other Libs
- ❌ Cannot import from higher tiers
- ✅ Must be owned by mobile-foundation team

**Why**: Libs provide infrastructure that all tiers depend on without introducing business coupling.

## Naming Conventions

### Folders: kebab-case
```
✅ Good:
- social-recipe-bridge/
- product-card-feature/
- error-boundary/

❌ Bad:
- SocialRecipeBridge/
- product_card_feature/
- mealSelection/
```

### Component Files: PascalCase
```
✅ Good:
- CookbookFaqScreen.tsx
- ProductCard.tsx
- AuthForm.tsx

❌ Bad:
- cookbookFaqScreen.tsx
- product-card.tsx
```

### Hook Files: camelCase with "use" prefix
```
✅ Good:
- useSignIn.ts
- usePerformanceTracker.ts

❌ Bad:
- UseSignIn.ts
- signIn.ts (missing "use")
```

### Utility Files: camelCase or lowercase
```
✅ Good:
- constants.ts
- types.ts
- styles.ts
- utils.ts
```

## Path Aliases

Use configured aliases for clean imports:

| Alias | Maps To | Tier |
|-------|---------|------|
| `@entry-providers/*` | `src/entry-providers/*` | Tier 1 |
| `@modules/*` | `src/modules/*` | Tier 2 |
| `@features/*` | `src/features/*` | Tier 3 |
| `@operations/*` | `src/operations/*` | Tier 4 |
| `@data-access/*` | `src/data-access/*` | Tier 5 |
| `@libs/*` | `src/libs/*` | Tier 6 |

**Example:**
```typescript
// ✅ Good: Use path aliases
import { ScreenCommonProvider } from '@entry-providers';
import { AuthForm } from '@features/auth-form';
import { useSignIn } from '@operations/auth';
import { signIn } from '@data-access/native';

// ❌ Bad: Deep relative paths
import { AuthForm } from '../../../features/auth-form';
```

## Barrel Exports (index.ts)

Each directory exports its public API through index.ts files.

```typescript
// src/features/product-card-feature/index.ts
export { ProductCard } from './ProductCard';
export { LoadingProductCard } from './variants/loading';
export type { ProductCardProps, ProductVariant } from './types';
```

**Why**: Barrel exports hide internal structure and enable clean import paths.

## Team Ownership (.claim.json)

Each module, feature, and operation includes team ownership:

```json
{
  "team": "team-social-recipes"
}
```

**Ownership Requirements:**
- Modules, Features, Operations, Screens must have owners
- Entry Providers, Libs, Data Access must be owned by mobile-foundation
- Approval required for changes to mobile-foundation-owned code

**Why**: Ownership files enable automated CODEOWNERS generation and clear team responsibilities.

## Common Mistakes

### ❌ Don't Violate Dependency Direction
```typescript
// ❌ Bad: Lower tier importing from higher
// src/libs/utils/helper.ts
import { useSignIn } from '@operations/auth';

// ✅ Good: Higher tier importing from lower
// src/operations/auth/useSignIn.ts
import { performanceTracker } from '@libs/observability';
```

### ❌ Don't Cross-Import Between Modules
```typescript
// ❌ Bad: Module importing from another module
import { RecipeCard } from '@modules/social-recipe-bridge/components';

// ✅ Good: Extract to shared feature
// src/features/recipe-card/RecipeCard.tsx
import { RecipeCard } from '@features/recipe-card';
```

### ❌ Don't Put Reusable UI in Modules
```typescript
// ❌ Bad: Reusable component in module
// src/modules/home/components/ProductCard.tsx  (used in multiple modules)

// ✅ Good: Reusable component in features
// src/features/product-card-feature/ProductCard.tsx
```

### ❌ Don't Put Business Logic in Features
```typescript
// ❌ Bad: Complex business logic in feature
// src/features/product-card/useProductLogic.ts

// ✅ Good: Business logic in operations
// src/operations/product-selection/useProductLogic.ts
```

## Quick Reference

| Tier | Can Import From | Cross-Imports | Ownership |
|------|----------------|---------------|-----------|
| Entry Providers | Libs only | ✅ Allowed | mobile-foundation |
| Modules | Features, Operations, Data Access, Libs | ❌ Forbidden | Team-owned |
| Features | Operations, Data Access, Libs, Features | ✅ Allowed | Team-owned |
| Operations | Data Access, Libs, Operations | ✅ Allowed | Team-owned |
| Data Access | Libs only | ❌ Forbidden | mobile-foundation |
| Libs | Libs only | ✅ Allowed | mobile-foundation |

## Testing Requirements

- ✅ Co-locate tests next to source files
- ✅ Unit tests for business logic (Operations)
- ✅ Component tests for UI (Features)
- ✅ Use `@testing-library/react-native`

```
src/features/product-card-feature/
├── ProductCard.tsx
├── ProductCard.test.tsx          # Co-located
└── components/
    ├── CardImage.tsx
    └── CardImage.test.tsx         # Co-located
```

**Why**: Co-located tests are easier to maintain and ensure tests are updated when code changes.

## Additional Resources

For detailed implementation guidance and examples, see:
- [references/examples.md](references/examples.md) - Real code structure examples
- [references/patterns.md](references/patterns.md) - Organizational patterns and anti-patterns
