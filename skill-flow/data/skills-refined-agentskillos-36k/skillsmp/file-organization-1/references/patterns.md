# File Organization Patterns

Common organizational patterns and anti-patterns for the 6-tier architecture.

## Pattern: Unidirectional Dependencies

Higher tiers import from lower tiers only.

✅ **Good:**
```typescript
// src/features/auth-form/AuthForm.tsx (Tier 3)
import { useSignIn } from '@operations/auth';        // Tier 4 ✓
import { Button } from '@zest/react-native';         // Lib ✓

// src/operations/auth/useSignIn.ts (Tier 4)
import { signIn } from '@data-access/native/auth';  // Tier 5 ✓
import { usePerformanceTracker } from '@libs/observability';  // Tier 6 ✓

// src/data-access/native/auth/signIn.ts (Tier 5)
import { sendEvent } from '@libs/native-modules/events';  // Tier 6 ✓
```

❌ **Bad:**
```typescript
// src/libs/utils/helper.ts (Tier 6)
import { useSignIn } from '@operations/auth';  // ❌ Importing UP the hierarchy

// src/data-access/native/auth.ts (Tier 5)
import { AuthForm } from '@features/auth-form';  // ❌ Importing UP the hierarchy

// src/operations/auth/useSignIn.ts (Tier 4)
import { SignInModule } from '@modules/sign-in';  // ❌ Importing UP the hierarchy
```

**Why:** Unidirectional flow prevents circular dependencies and makes dependency graphs predictable.

## Pattern: Module Isolation

Modules cannot import from other modules.

✅ **Good:**
```typescript
// src/modules/home/screens/home/Home.tsx
import { ProductCard } from '@features/product-card-feature';  // ✓ Shared feature

// src/modules/onboarding/screens/welcome/Welcome.tsx
import { ProductCard } from '@features/product-card-feature';  // ✓ Both use shared feature
```

❌ **Bad:**
```typescript
// src/modules/onboarding/screens/welcome/Welcome.tsx
import { ProductCard } from '@modules/home/components/ProductCard';  // ❌ Cross-module import

// src/modules/social-recipe-bridge/screens/cookbook/Cookbook.tsx
import { Header } from '@modules/home/components/Header';  // ❌ Cross-module import
```

**Solution:** Extract reusable components to shared features:

```typescript
// src/features/product-card-feature/ProductCard.tsx
export const ProductCard = () => {
  // Implementation
};

// Both modules can now import from feature
import { ProductCard } from '@features/product-card-feature';
```

**Why:** Module isolation prevents tight coupling and ensures changes to one module don't affect others.

## Pattern: Features Are Reusable

Features must be used in at least 2 modules.

✅ **Good:**
```typescript
// src/features/product-card-feature/ProductCard.tsx
// Used in: home module, menu module, favorites module

// src/features/auth-form/AuthForm.tsx
// Used in: sign-in module, sign-up module
```

❌ **Bad:**
```typescript
// src/features/welcome-banner/WelcomeBanner.tsx
// Only used in onboarding module - should be in module instead

// Should be:
// src/modules/onboarding/components/WelcomeBanner.tsx
```

**Why:** Features promote reusability. Single-use components belong in modules.

## Pattern: Operations Contain Business Logic

Operations handle business logic without UI.

✅ **Good:**
```typescript
// src/operations/meal-selection/useMealSelection.ts
import { useMutation } from '@tanstack/react-query';
import { addMeal, removeMeal } from '@data-access/query/meals';
import { useAnalytics } from '@libs/analytics';

export const useMealSelection = () => {
  const { track } = useAnalytics();

  const add = useMutation({
    mutationFn: addMeal,
    onSuccess: (data) => {
      track('Meal_Added', { mealId: data.id });
    },
  });

  const remove = useMutation({
    mutationFn: removeMeal,
    onSuccess: (data) => {
      track('Meal_Removed', { mealId: data.id });
    },
  });

  return { add, remove };
};
```

❌ **Bad:**
```typescript
// src/features/meal-card/useMealSelection.ts
// Business logic in feature - should be in operations

// src/features/meal-card/MealCard.tsx
const MealCard = ({ meal }) => {
  // ❌ Business logic directly in component
  const addMeal = async () => {
    const response = await fetch('/api/meals', { method: 'POST' });
    analytics.track('Meal_Added');
    // ...
  };
};
```

**Why:** Separating business logic from UI makes it reusable and testable.

## Pattern: Data Access Is the Single API Layer

All API calls go through data access.

✅ **Good:**
```typescript
// src/data-access/native/auth/signIn.ts
import { sendEvent } from '@libs/native-modules/events';

export const signIn = async (signInData: SignInData) => {
  return await sendEvent('signIn', {
    payload: JSON.stringify(signInData),
  });
};

// src/operations/auth/useSignIn.ts
import { signIn } from '@data-access/native/auth';  // ✓ Uses data access layer

export const useSignIn = () => {
  return useMutation({
    mutationFn: signIn,
  });
};
```

❌ **Bad:**
```typescript
// src/operations/auth/useSignIn.ts
import { sendEvent } from '@libs/native-modules/events';  // ❌ Bypassing data access

export const useSignIn = () => {
  return useMutation({
    mutationFn: async (data) => {
      // ❌ Direct API call in operation
      return await sendEvent('signIn', { payload: JSON.stringify(data) });
    },
  });
};
```

**Why:** Centralizing API calls in data access makes mocking easier and ensures consistent patterns.

## Pattern: Path Aliases Over Relative Imports

Use configured path aliases instead of relative paths.

✅ **Good:**
```typescript
import { ScreenCommonProvider } from '@entry-providers';
import { AuthForm } from '@features/auth-form';
import { useSignIn } from '@operations/auth';
import { signIn } from '@data-access/native/auth';
import { usePerformanceTracker } from '@libs/observability';
```

❌ **Bad:**
```typescript
import { ScreenCommonProvider } from '../../../entry-providers';
import { AuthForm } from '../../features/auth-form';
import { useSignIn } from '../operations/auth';
```

**Why:** Path aliases are clearer, easier to refactor, and don't break when files move.

## Pattern: Barrel Exports for Public APIs

Use index.ts to export public APIs.

✅ **Good:**
```typescript
// src/features/product-card-feature/index.ts
export { ProductCard } from './ProductCard';
export { LoadingProductCard } from './variants/loading';
export type { ProductCardProps } from './types';

// Usage
import { ProductCard } from '@features/product-card-feature';
```

❌ **Bad:**
```typescript
// Direct imports bypassing barrel
import { ProductCard } from '@features/product-card-feature/ProductCard';
import { LoadingProductCard } from '@features/product-card-feature/variants/loading/LoadingProductCard';
```

**Why:** Barrel exports hide internal structure and provide a clean public API.

## Pattern: Co-Located Tests

Place test files next to source files.

✅ **Good:**
```
src/features/auth-form/
├── AuthForm.tsx
├── AuthForm.test.tsx          # Co-located
├── components/
│   ├── Input.tsx
│   └── Input.test.tsx         # Co-located
└── hooks/
    ├── useFormValidation.ts
    └── useFormValidation.test.ts  # Co-located
```

❌ **Bad:**
```
src/features/auth-form/
├── AuthForm.tsx
├── components/
│   └── Input.tsx
└── __tests__/                 # Separate tests directory
    ├── AuthForm.test.tsx      # Hard to find
    └── Input.test.tsx
```

**Why:** Co-located tests are easier to maintain and ensure tests are updated with code changes.

## Pattern: Feature Variants for State Variations

Use variants/ subdirectory for different states of the same feature.

✅ **Good:**
```
src/features/product-card-feature/
├── index.ts
├── ProductCard.tsx            # Main component
└── variants/
    ├── loading/
    │   └── LoadingProductCard.tsx
    ├── edit/
    │   └── EditProductCard.tsx
    └── compact/
        └── CompactProductCard.tsx
```

❌ **Bad:**
```
src/features/
├── product-card-feature/
├── product-card-loading-feature/     # ❌ Separate features
├── product-card-edit-feature/        # ❌ Should be variants
└── product-card-compact-feature/     # ❌ Should be variants
```

**Why:** Variants keep related state variations organized within a single feature.

## Pattern: Team Ownership

Every module, feature, and operation has clear ownership.

✅ **Good:**
```json
// src/modules/social-recipe-bridge/.claim.json
{
  "team": "team-social-recipes"
}
```

```json
// src/features/product-card-feature/.claim.json
{
  "team": "team-product-experience"
}
```

```json
// src/libs/analytics/.claim.json
{
  "team": "mobile-foundation"
}
```

❌ **Bad:**
```
src/modules/social-recipe-bridge/
├── index.ts
└── screens/
    # Missing .claim.json - no clear owner
```

**Why:** Clear ownership enables automated CODEOWNERS generation and team accountability.

## Anti-Pattern: Violating Dependency Direction

Never import from higher tiers.

❌ **Bad:**
```typescript
// src/libs/utils/formatter.ts (Tier 6)
import { useCustomerData } from '@operations/customer';  // ❌ Tier 4

// src/data-access/native/events.ts (Tier 5)
import { useAnalytics } from '@operations/analytics';  // ❌ Tier 4

// src/operations/cart/useCart.ts (Tier 4)
import { CartModule } from '@modules/cart';  // ❌ Tier 2
```

**Fix:** Move logic to appropriate tier or pass as dependency:

✅ **Good:**
```typescript
// src/operations/cart/useCart.ts (Tier 4)
import { getCart } from '@data-access/query/cart';  // ✓ Tier 5
import { formatCurrency } from '@libs/utils/formatter';  // ✓ Tier 6
```

## Anti-Pattern: Mixing UI and Business Logic

Don't put complex business logic in features.

❌ **Bad:**
```typescript
// src/features/meal-card/MealCard.tsx
const MealCard = ({ meal }) => {
  // ❌ Complex business logic in feature
  const calculateDiscount = () => {
    const basePrice = meal.price;
    const loyaltyDiscount = user.loyaltyPoints * 0.01;
    const seasonalDiscount = isSeasonalPeriod() ? 0.15 : 0;
    return basePrice * (1 - loyaltyDiscount - seasonalDiscount);
  };

  const handleAddToCart = async () => {
    // ❌ API calls in feature
    const response = await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ mealId: meal.id }),
    });
  };

  return <Card price={calculateDiscount()} onPress={handleAddToCart} />;
};
```

✅ **Good:**
```typescript
// src/operations/pricing/usePricing.ts
export const usePricing = (meal: Meal) => {
  const { user } = useUser();

  const calculateDiscount = () => {
    const basePrice = meal.price;
    const loyaltyDiscount = user.loyaltyPoints * 0.01;
    const seasonalDiscount = isSeasonalPeriod() ? 0.15 : 0;
    return basePrice * (1 - loyaltyDiscount - seasonalDiscount);
  };

  return { finalPrice: calculateDiscount() };
};

// src/operations/cart/useAddToCart.ts
export const useAddToCart = () => {
  return useMutation({
    mutationFn: (mealId) => addToCart(mealId),
  });
};

// src/features/meal-card/MealCard.tsx
const MealCard = ({ meal }) => {
  const { finalPrice } = usePricing(meal);
  const { mutate: addToCart } = useAddToCart();

  return <Card price={finalPrice} onPress={() => addToCart(meal.id)} />;
};
```

**Why:** Separating concerns makes business logic testable and reusable.

## Anti-Pattern: Data Access Cross-Imports

Data access modules cannot import from each other.

❌ **Bad:**
```typescript
// src/data-access/query/customer/profile.ts
import { getCustomerOrders } from '@data-access/query/orders';  // ❌ Cross-import

// src/data-access/native/auth.ts
import { getUserProfile } from '@data-access/native/user';  // ❌ Cross-import
```

✅ **Good:**
```typescript
// src/operations/customer/useCustomerProfile.ts
import { getCustomerProfile } from '@data-access/query/customer';
import { getCustomerOrders } from '@data-access/query/orders';

export const useCustomerProfile = () => {
  const profile = useQuery({ queryFn: getCustomerProfile });
  const orders = useQuery({ queryFn: getCustomerOrders });

  return { profile, orders };
};
```

**Why:** Keeping data access modules independent prevents coupling at the API layer.

## Anti-Pattern: Reusable Components in Modules

Don't put reusable UI in module directories.

❌ **Bad:**
```typescript
// src/modules/home/components/ProductCard.tsx
// Used in: home module, menu module, favorites module
// ❌ Should be in features/
```

✅ **Good:**
```typescript
// src/features/product-card-feature/ProductCard.tsx
// Used in: home module, menu module, favorites module
// ✓ Correctly placed as reusable feature
```

**Why:** Reusable components belong in features so they can be shared without cross-module dependencies.

## Anti-Pattern: Deep Nesting

Don't create overly deep directory structures.

❌ **Bad:**
```
src/modules/home/screens/main/components/sections/hero/variants/mobile/components/card/
```

✅ **Good:**
```
src/modules/home/
├── screens/
│   └── main/
│       ├── MainScreen.tsx
│       └── components/
│           └── HeroSection.tsx
└── components/
    └── HeroCard.tsx
```

**Why:** Flat structures are easier to navigate and refactor.

## Anti-Pattern: Missing Ownership

Every tier must have ownership defined.

❌ **Bad:**
```
src/modules/checkout/
├── index.ts
├── screens/
│   └── payment/
# Missing .claim.json
```

✅ **Good:**
```
src/modules/checkout/
├── .claim.json              # {"team": "team-checkout"}
├── index.ts
└── screens/
    └── payment/
```

**Why:** Clear ownership enables team accountability and automated CODEOWNERS.

## Anti-Pattern: Inconsistent Naming

Maintain consistent naming conventions.

❌ **Bad:**
```
src/features/
├── ProductCard/             # PascalCase folder
├── recipe_image/            # snake_case folder
└── mealSelection/           # camelCase folder

src/features/product-card/
├── product-card.tsx         # kebab-case file
├── ProductCard.tsx          # PascalCase file (inconsistent)
└── useProductCard.ts        # camelCase file
```

✅ **Good:**
```
src/features/
├── product-card-feature/    # kebab-case folder
├── recipe-image/            # kebab-case folder
└── meal-selection/          # kebab-case folder

src/features/product-card-feature/
├── ProductCard.tsx          # PascalCase component
├── ProductCard.test.tsx     # PascalCase test
├── useProductCard.ts        # camelCase hook
└── types.ts                 # lowercase utility
```

**Why:** Consistent naming makes code predictable and easier to navigate.
