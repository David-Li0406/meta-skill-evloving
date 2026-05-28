---
name: data-transformation
description: "WHAT: Transform API responses into domain models with transformers, helpers, and utilities. WHEN: converting API data shapes, implementing data pipelines, organizing transformation logic. KEYWORDS: transformer, helper, utils, API response, domain model, data shape, conversion, mapping."
---

# Data Transformation Patterns

## Core Principles

Use **transformer functions** for API response shaping, **helper functions** for business logic, and **utility functions** for pure operations. Always organize these in separate files within feature directories.

**Why this matters**: Separation of concerns makes data transformation testable, maintainable, and reusable across the application.

## When to Use This Skill

Use this skill when you need to:

- Transform API responses into application domain models
- Implement data conversion logic between different shapes
- Organize data transformation code in React Native applications
- Structure business logic and calculations
- Create testable transformation pipelines

## File Organization Pattern

Organize data transformation files by feature:

```
features/
└── [feature-name]/
    └── hooks/
        └── [hook-name]/
            ├── index.ts                 # Public exports
            ├── types.ts                 # Type definitions
            ├── [hookName].ts            # Main hook
            ├── transformers.ts          # API transformations
            ├── helpers.ts               # Business logic
            └── utils.ts                 # Pure utilities
```

**Key rule**: Keep transformers, helpers, and utils in separate files for focused testing and clear boundaries.

## Transformer Functions

### Purpose

Transformers convert API responses into application domain models. They should:

- Only handle data shape conversion
- Not contain business logic
- Validate inputs and throw clear errors
- Use explicit types for inputs and outputs

### Implementation Pattern

```typescript
// transformers.ts

/**
 * Transforms the reactivation price API response into the format
 * expected by the ReactivationBannerVoucher model.
 */
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  const product = response.products[0];

  if (!product) {
    throw new Error('No product found in price response');
  }

  const calculatedValues = getCalculatedPriceValues(response, product);

  return {
    initialPrice: calculatedValues.productUnitPrice,
    discountedPrice: calculatedValues.productPaidPrice,
    currency: product.price.currency,
    savings: calculatedValues.productUnitPrice - calculatedValues.productPaidPrice,
    analyticsEventValues: {
      productPriceId: product.priceId,
      totalPrice: calculatedValues.totalPrice,
      deliveryPrice: calculatedValues.deliveryPrice,
      originalTotalPrice: calculatedValues.originalTotalPrice,
    },
  };
};
```

### Common Transformer Patterns

```typescript
// Single entity transformation
export const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.user_id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
});

// Collection transformation
export const transformRecipeList = (apiRecipes: ApiRecipe[]): Recipe[] => {
  return apiRecipes.map(transformRecipe);
};

// Nested transformation
export const transformOrder = (apiOrder: ApiOrder): Order => ({
  id: apiOrder.order_id,
  user: transformUser(apiOrder.user_data),
  items: apiOrder.line_items.map(transformOrderItem),
  total: convertMoneyToNumber(apiOrder.total_amount),
});
```

## Helper Functions

### Purpose

Helpers contain business logic and calculations. They should:

- Encapsulate business rules
- Be pure functions when possible
- Have clear single responsibilities
- Be easily testable in isolation

### Implementation Pattern

```typescript
// helpers.ts

/**
 * Calculates all price-related values from the API response.
 * Encapsulates all mathematical operations in one place for better testability.
 */
export const getCalculatedPriceValues = (
  response: ReactivationPriceResponse,
  product: ReactivationPriceResponse['products'][0]
): GetCalculatedPriceValuesReturn => {
  const productUnitPrice = convertMoneyToNumber(product.price);
  const productPaidPrice = convertMoneyToNumber(product.paidPrice);
  const deliveryPrice = convertMoneyToNumber(response.deliveryPrice);
  const originalTotalPrice = convertMoneyToNumber(response.originalTotalPrice);
  const totalPrice = convertMoneyToNumber(response.totalPrice);

  return {
    productUnitPrice,
    productPaidPrice,
    deliveryPrice,
    originalTotalPrice,
    totalPrice,
    savings: productUnitPrice - productPaidPrice,
  };
};

/**
 * Determines if a recipe can be added to cart based on stock and user plan.
 */
export const canAddToCart = (recipe: Recipe, userPlan: Plan, cartSize: number): boolean => {
  if (!recipe.inStock) return false;
  if (cartSize >= userPlan.maxItems) return false;
  if (recipe.requiresPremium && !userPlan.isPremium) return false;

  return true;
};
```

## Utility Functions

### Purpose

Utils are pure functions with no business logic dependencies. They should:

- Be completely generic
- Have no domain-specific knowledge
- Be reusable across features
- Have no side effects

### Implementation Pattern

```typescript
// utils.ts

/**
 * Converts API Money object to number in smallest currency unit (cents).
 */
export const convertMoneyToNumber = (money: Money): number => {
  return Math.round(parseFloat(money.amount) * 100);
};

/**
 * Formats price for display.
 */
export const formatPrice = (cents: number, currency: string): string => {
  const amount = cents / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};

/**
 * Validates email format.
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
```

## Type Definitions

Always define explicit types for transformation inputs and outputs:

```typescript
// types.ts

export interface ReactivationPriceResponse {
  products: Array<{
    priceId: string;
    price: Money;
    paidPrice: Money;
  }>;
  deliveryPrice: Money;
  originalTotalPrice: Money;
  totalPrice: Money;
}

export interface VoucherPriceInfo {
  initialPrice: number;
  discountedPrice: number;
  currency: string;
  savings: number;
  analyticsEventValues: {
    productPriceId: string;
    totalPrice: number;
    deliveryPrice: number;
    originalTotalPrice: number;
  };
}
```

**Why**: Explicit types provide compile-time safety and serve as documentation.

## Error Handling

Always validate transformer inputs and provide clear error messages:

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

  // Transform validated data
  return {
    /* ... */
  };
};
```

**Why**: Early validation prevents downstream errors and provides clear error messages.

## Testing Strategy

### Test transformers in isolation:

```typescript
describe('transformReactivationPriceResponse', () => {
  it('transforms valid response correctly', () => {
    const response: ReactivationPriceResponse = {
      products: [
        {
          priceId: 'price-123',
          price: { amount: '29.99', currency: 'USD' },
          paidPrice: { amount: '19.99', currency: 'USD' },
        },
      ],
      deliveryPrice: { amount: '5.00', currency: 'USD' },
      originalTotalPrice: { amount: '34.99', currency: 'USD' },
      totalPrice: { amount: '24.99', currency: 'USD' },
    };

    const result = transformReactivationPriceResponse(response);

    expect(result.initialPrice).toBe(2999);
    expect(result.discountedPrice).toBe(1999);
    expect(result.savings).toBe(1000);
  });

  it('throws error when no products', () => {
    const response: ReactivationPriceResponse = {
      products: [],
      // ...
    };

    expect(() => transformReactivationPriceResponse(response)).toThrow(
      'No product found in price response'
    );
  });
});
```

### Test helpers separately:

```typescript
describe('canAddToCart', () => {
  it('returns true when all conditions are met', () => {
    const recipe = { inStock: true, requiresPremium: false };
    const plan = { maxItems: 5, isPremium: false };

    expect(canAddToCart(recipe, plan, 3)).toBe(true);
  });

  it('returns false when out of stock', () => {
    const recipe = { inStock: false, requiresPremium: false };
    const plan = { maxItems: 5, isPremium: false };

    expect(canAddToCart(recipe, plan, 3)).toBe(false);
  });
});
```

## Common Mistakes to Avoid

❌ **Don't mix transformation with business logic**:

```typescript
// Bad: Mixing concerns
export const transformUser = (apiUser: ApiUser): User => {
  const user = {
    id: apiUser.user_id,
    name: `${apiUser.first_name} ${apiUser.last_name}`,
    email: apiUser.email_address,
  };

  // Business logic in transformer - WRONG!
  if (user.email.includes('@premium.com')) {
    user.isPremium = true;
  }

  return user;
};
```

❌ **Don't put everything in one file**:

```typescript
// Bad: One file with transformers, helpers, and utils mixed
export const transform = (data) => { /* ... */ };
export const calculate = (data) => { /* ... */ };
export const format = (data) => { /* ... */ };
```

✅ **Do separate concerns**:

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

## Documentation Guidelines

Add JSDoc comments for complex transformations:

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

## Quick Reference

**Transformers**: API shape → Domain model (no business logic)
**Helpers**: Business logic and calculations
**Utils**: Pure, generic functions

For detailed examples from production code, see [references/examples.md](references/examples.md).
For specific API documentation, see [references/api-docs.md](references/api-docs.md).
