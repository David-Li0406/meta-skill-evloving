# Data Transformation - Implementation Patterns

Implementation patterns and anti-patterns for data transformation in React web applications.

## Pattern: Separate Transformers, Helpers, and Utils

Keep transformers, business logic, and utilities in separate files.

✅ **Good:**
```typescript
// transformers.ts - API shape to domain model
export const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.user_id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
});

// helpers.ts - Business logic
export const isPremiumUser = (user: User): boolean => {
  return user.email.includes('@premium.com');
};

// utils.ts - Pure utilities
export const formatEmail = (email: string): string => {
  return email.toLowerCase().trim();
};
```

❌ **Bad:**
```typescript
// index.ts - Everything mixed together
export const transformUser = (apiUser: ApiUser): User => {
  const user = {
    id: apiUser.user_id,
    name: `${apiUser.first_name} ${apiUser.last_name}`,
    email: apiUser.email_address.toLowerCase().trim(), // Utility in transformer
  };

  // Business logic in transformer
  if (user.email.includes('@premium.com')) {
    user.isPremium = true;
  }

  return user;
};
```

**Why:** Separation of concerns:
- Transformers handle shape conversion only
- Helpers contain business logic
- Utils provide pure, reusable functions
- Each layer is independently testable
- Clear boundaries reduce bugs

## Pattern: Validate Input in Transformers

Always validate required fields before transformation.

✅ **Good:**
```typescript
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  const product = response.products[0];

  if (!product) {
    throw new Error('No product found in price response');
  }

  if (!product.priceId || !product.price || !product.paidPrice) {
    throw new Error('Invalid product data in response');
  }

  // Safe to transform now
  return {
    initialPrice: convertMoneyToNumber(product.price),
    discountedPrice: convertMoneyToNumber(product.paidPrice),
  };
};
```

❌ **Bad:**
```typescript
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // No validation - crashes if product is undefined
  const product = response.products[0];

  return {
    initialPrice: convertMoneyToNumber(product.price), // Crashes here
    discountedPrice: convertMoneyToNumber(product.paidPrice),
  };
};
```

**Why:** Input validation:
- Prevents downstream crashes
- Provides clear error messages
- Catches API contract violations early
- Makes debugging easier
- Explicit about requirements

## Pattern: Use Explicit Types

Define explicit types for all inputs and outputs.

✅ **Good:**
```typescript
export interface ReactivationPriceResponse {
  products: Array<{
    priceId: string;
    price: Money;
    paidPrice: Money;
  }>;
  deliveryPrice: Money;
  totalPrice: Money;
}

export interface VoucherPriceInfo {
  initialPrice: number;
  discountedPrice: number;
  currency: string;
  savings: number;
}

export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // Implementation with type safety
};
```

❌ **Bad:**
```typescript
export const transformReactivationPriceResponse = (
  response: any // No type safety
): any => {
  // No compile-time checks
  return {
    initialPrice: response.products[0].price.amount, // Could be wrong
  };
};
```

**Why:** Explicit types:
- Provide compile-time safety
- Serve as documentation
- Catch errors early
- Enable IDE autocomplete
- Make refactoring safer

## Pattern: Delegate Complex Calculations to Helpers

Keep transformers simple by delegating calculations.

✅ **Good:**
```typescript
// transformers.ts
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  const product = response.products[0];

  if (!product) {
    throw new Error('No product found');
  }

  // Delegate calculation to helper
  const calculatedValues = getCalculatedPriceValues(response, product);

  return {
    initialPrice: calculatedValues.productUnitPrice,
    discountedPrice: calculatedValues.productPaidPrice,
    savings: calculatedValues.savings,
  };
};

// helpers.ts
export const getCalculatedPriceValues = (
  response: ReactivationPriceResponse,
  product: ReactivationPriceResponse['products'][0]
): CalculatedPriceValues => {
  const productUnitPrice = convertMoneyToNumber(product.price);
  const productPaidPrice = convertMoneyToNumber(product.paidPrice);

  return {
    productUnitPrice,
    productPaidPrice,
    savings: productUnitPrice - productPaidPrice,
  };
};
```

❌ **Bad:**
```typescript
// transformers.ts - Too much logic
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  const product = response.products[0];

  // Complex calculations inline
  const productUnitPrice = Math.round(parseFloat(product.price.amount) * 100);
  const productPaidPrice = Math.round(parseFloat(product.paidPrice.amount) * 100);
  const deliveryPrice = Math.round(parseFloat(response.deliveryPrice.amount) * 100);
  const savings = productUnitPrice - productPaidPrice;

  // More calculations...
  return {
    initialPrice: productUnitPrice,
    discountedPrice: productPaidPrice,
    savings,
  };
};
```

**Why:** Delegation:
- Keeps transformers focused on shape conversion
- Makes complex logic testable in isolation
- Improves readability
- Enables reuse of calculations
- Easier to maintain

## Pattern: Pure Transformers

Transformers should have no side effects.

✅ **Good:**
```typescript
export const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.user_id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
});
```

❌ **Bad:**
```typescript
let lastTransformedUser: User | null = null; // Global state

export const transformUser = (apiUser: ApiUser): User => {
  const user = {
    id: apiUser.user_id,
    name: `${apiUser.first_name} ${apiUser.last_name}`,
    email: apiUser.email_address,
  };

  // Side effect - mutates global state
  lastTransformedUser = user;

  // Side effect - logs to console
  console.log('Transformed user:', user);

  return user;
};
```

**Why:** Pure functions:
- Same input always produces same output
- No hidden dependencies
- Easier to test
- Predictable behavior
- No race conditions

## Pattern: Map Collections with Array Methods

Use `.map()` for transforming arrays.

✅ **Good:**
```typescript
export const transformRecipeList = (apiRecipes: ApiRecipe[]): Recipe[] => {
  return apiRecipes.map(transformRecipe);
};

// With filtering
export const transformActiveRecipes = (apiRecipes: ApiRecipe[]): Recipe[] => {
  return apiRecipes
    .filter(recipe => recipe.status === 'active')
    .map(transformRecipe);
};
```

❌ **Bad:**
```typescript
export const transformRecipeList = (apiRecipes: ApiRecipe[]): Recipe[] => {
  const recipes: Recipe[] = [];

  // Imperative loop
  for (let i = 0; i < apiRecipes.length; i++) {
    recipes.push(transformRecipe(apiRecipes[i]));
  }

  return recipes;
};
```

**Why:** Array methods:
- More concise and readable
- Functional programming style
- Less error-prone
- Easier to chain operations
- Standard JavaScript patterns

## Pattern: Compose Nested Transformations

Transform nested objects by composing transformers.

✅ **Good:**
```typescript
export const transformOrder = (apiOrder: ApiOrder): Order => ({
  id: apiOrder.order_id,
  user: transformUser(apiOrder.user_data),
  items: apiOrder.line_items.map(transformOrderItem),
  shippingAddress: transformAddress(apiOrder.shipping_address),
  total: convertMoneyToNumber(apiOrder.total_amount),
});
```

❌ **Bad:**
```typescript
export const transformOrder = (apiOrder: ApiOrder): Order => ({
  id: apiOrder.order_id,
  // Inline transformation - not reusable
  user: {
    id: apiOrder.user_data.user_id,
    name: `${apiOrder.user_data.first_name} ${apiOrder.user_data.last_name}`,
  },
  items: apiOrder.line_items.map(item => ({
    id: item.item_id,
    name: item.item_name,
    // Nested inline transformations become unreadable
  })),
});
```

**Why:** Composition:
- Reuses existing transformers
- Maintains single responsibility
- More maintainable
- Easier to test each piece
- Follows DRY principle

## Pattern: Use Helper Functions for Business Logic

Extract business rules into helper functions.

✅ **Good:**
```typescript
// helpers.ts
export const canAddToCart = (
  recipe: Recipe,
  userPlan: Plan,
  cartSize: number
): boolean => {
  if (!recipe.inStock) return false;
  if (cartSize >= userPlan.maxItems) return false;
  if (recipe.requiresPremium && !userPlan.isPremium) return false;

  return true;
};

// In component
const addToCart = (recipe: Recipe) => {
  if (canAddToCart(recipe, userPlan, cart.items.length)) {
    dispatch(addItem(recipe));
  } else {
    showError('Cannot add this recipe');
  }
};
```

❌ **Bad:**
```typescript
// In component - business logic inline
const addToCart = (recipe: Recipe) => {
  // Business logic scattered in UI code
  if (!recipe.inStock) {
    showError('Out of stock');
    return;
  }

  if (cart.items.length >= userPlan.maxItems) {
    showError('Cart full');
    return;
  }

  if (recipe.requiresPremium && !userPlan.isPremium) {
    showError('Premium required');
    return;
  }

  dispatch(addItem(recipe));
};
```

**Why:** Helper functions:
- Centralize business logic
- Easily testable
- Reusable across components
- Clear naming documents intent
- Easier to modify rules

## Pattern: Use Utils for Pure Generic Functions

Keep utilities completely generic.

✅ **Good:**
```typescript
// utils.ts - Generic, reusable
export const formatPrice = (cents: number, currency: string): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(cents / 100);
};

export const truncateToTwoDecimals = (value: number): number => {
  return Math.trunc(value * 100) / 100;
};
```

❌ **Bad:**
```typescript
// utils.ts - Domain-specific business logic
export const formatRecipePrice = (recipe: Recipe): string => {
  // Business logic in util
  const price = recipe.requiresPremium
    ? recipe.premiumPrice
    : recipe.regularPrice;

  return formatPrice(price, recipe.currency);
};
```

**Why:** Generic utils:
- Reusable across entire codebase
- No domain coupling
- Easier to test
- Clear responsibility
- Can be extracted to shared library

## Pattern: Organize by Feature

Keep transformation files within feature directories.

✅ **Good:**
```
features/
└── reactivation-banner-feature/
    └── state-management/
        └── hooks/
            └── use-voucher-price-details/
                ├── index.ts                 # Exports
                ├── types.ts                 # Types
                ├── useVoucherPriceDetails.ts
                ├── transformers.ts          # API transformations
                ├── helpers.ts               # Business logic
                └── utils.ts                 # Pure utilities
```

❌ **Bad:**
```
src/
├── transformers/
│   └── all-transformers.ts  # All features mixed
├── helpers/
│   └── all-helpers.ts
└── utils/
    └── all-utils.ts
```

**Why:** Feature organization:
- Co-locates related code
- Easier to find and modify
- Clear feature boundaries
- Prevents sprawling files
- Better encapsulation

## Pattern: Document Complex Transformations

Add JSDoc for non-obvious transformations.

✅ **Good:**
```typescript
/**
 * Transforms reactivation price response into voucher price info.
 *
 * @param response - API response from reactivation price endpoint
 * @returns Voucher price information for display and analytics
 *
 * @throws Error if response contains no products
 * @throws Error if product data is invalid
 *
 * @example
 * const priceInfo = transformReactivationPriceResponse(apiResponse);
 * console.log(priceInfo.savings); // 1000 (in cents)
 */
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // Implementation
};
```

❌ **Bad:**
```typescript
// No documentation for complex transformation
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // What does this do? Why? When does it throw?
  const product = response.products[0];
  // ...
};
```

**Why:** Documentation:
- Explains non-obvious logic
- Documents error cases
- Provides usage examples
- Helps future maintainers
- Clarifies intent

## Anti-Pattern: Mixing Transformation and Business Logic

Don't mix shape conversion with business rules.

❌ **Bad:**
```typescript
export const transformUser = (apiUser: ApiUser): User => {
  const user = {
    id: apiUser.user_id,
    name: `${apiUser.first_name} ${apiUser.last_name}`,
    email: apiUser.email_address,
  };

  // Business logic in transformer
  if (user.email.includes('@premium.com')) {
    user.isPremium = true;
    user.discountRate = 0.2;
  }

  // More business logic
  if (user.id.startsWith('VIP')) {
    user.vipStatus = 'gold';
  }

  return user;
};
```

✅ **Good:**
```typescript
// transformers.ts - Only shape conversion
export const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.user_id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
});

// helpers.ts - Business logic
export const isPremiumUser = (user: User): boolean => {
  return user.email.includes('@premium.com');
};

export const getUserDiscountRate = (user: User): number => {
  return isPremiumUser(user) ? 0.2 : 0;
};

export const getVipStatus = (user: User): VipStatus => {
  if (user.id.startsWith('VIP')) return 'gold';
  return 'standard';
};
```

## Anti-Pattern: Implicit Dependencies

Don't rely on external state in transformers.

❌ **Bad:**
```typescript
// Depends on global config
const currencyConfig = { defaultCurrency: 'USD' };

export const transformPrice = (apiPrice: ApiPrice): Price => ({
  amount: parseFloat(apiPrice.amount),
  // Implicit dependency on global state
  currency: apiPrice.currency || currencyConfig.defaultCurrency,
});
```

✅ **Good:**
```typescript
export const transformPrice = (
  apiPrice: ApiPrice,
  defaultCurrency: string = 'USD'
): Price => ({
  amount: parseFloat(apiPrice.amount),
  // Explicit parameter
  currency: apiPrice.currency || defaultCurrency,
});
```

## Anti-Pattern: Skipping Validation

Don't assume API data is always valid.

❌ **Bad:**
```typescript
export const transformOrder = (apiOrder: ApiOrder): Order => ({
  // No validation - crashes if user_data is null
  user: transformUser(apiOrder.user_data),
  items: apiOrder.line_items.map(transformOrderItem),
});
```

✅ **Good:**
```typescript
export const transformOrder = (apiOrder: ApiOrder): Order => {
  if (!apiOrder.user_data) {
    throw new Error('Order missing user data');
  }

  if (!apiOrder.line_items || apiOrder.line_items.length === 0) {
    throw new Error('Order has no items');
  }

  return {
    user: transformUser(apiOrder.user_data),
    items: apiOrder.line_items.map(transformOrderItem),
  };
};
```

## Summary

**Key Patterns:**
- Separate transformers, helpers, and utils into different files
- Validate input before transformation
- Use explicit types for all inputs and outputs
- Delegate complex calculations to helpers
- Keep transformers pure (no side effects)
- Use `.map()` for array transformations
- Compose nested transformations
- Extract business logic into helpers
- Keep utils completely generic
- Organize by feature
- Document complex transformations

**Anti-Patterns to Avoid:**
- Mixing transformation and business logic
- Implicit dependencies on external state
- Skipping input validation
- Putting everything in one file
- Side effects in transformers
- Domain logic in utilities
- Inline transformations instead of composition
