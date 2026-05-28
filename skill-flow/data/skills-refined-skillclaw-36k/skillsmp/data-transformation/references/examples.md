# Data Transformation Examples from Production

This document contains real-world examples from the YourCompany shared-mobile-modules codebase demonstrating data transformation patterns.

## Complete Feature Example: Reactivation Banner Price Details

This example shows a complete data transformation pipeline for handling voucher price details in the reactivation banner feature.

### Directory Structure

```
features/reactivation-banner-feature/
└── state-management/
    └── hooks/
        └── use-voucher-price-details/
            ├── index.ts                          # Public exports
            ├── types.ts                          # Type definitions
            ├── useVoucherPriceDetails.ts         # Main hook
            ├── transformers.ts                   # API transformations
            ├── helpers.ts                        # Business logic
            └── utils.ts                          # Pure utilities
```

### 1. Public Exports (index.ts)

```typescript
export { useVoucherPriceDetails } from './useVoucherPriceDetails';
export { transformReactivationPriceResponse } from './transformers';
```

**Pattern**: Only export what consumers need. Keep internal helpers private.

### 2. Transformer Function (transformers.ts)

```typescript
import type { ReactivationPriceResponse } from '@data-access/query/reactivation';
import { convertMoneyToNumber } from '@libs/currency';
import type { VoucherPriceInfo } from '../../models';
import { getCalculatedPriceValues } from './helpers';

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

  // Delegate all calculations to the helper method
  const calculatedValues = getCalculatedPriceValues(response, product);

  return {
    // UI-focused fields
    initialPrice: calculatedValues.productUnitPrice,
    discountedPrice: calculatedValues.productPaidPrice,
    initialPricePerServing: convertMoneyToNumber(
      product.pricePerServing.original
    ),
    discountedPricePerServing: convertMoneyToNumber(
      product.pricePerServing.withDiscount
    ),

    // Analytics event values
    analyticsEventValues: {
      productPriceId: product.priceId,
      totalPrice: calculatedValues.totalPrice,
      totalPriceWithDiscount: calculatedValues.totalPriceWithDiscount,
      shippingPrice: calculatedValues.shippingPrice,
      shippingDiscount: calculatedValues.shippingDiscount,
      currency: response.currencyCode,
      productSku: product.id,
      boxPrice: calculatedValues.boxPrice,
      boxPriceWithDiscount: calculatedValues.boxPriceWithDiscount,
      servingPrice: calculatedValues.servingPrice,
      servingPriceWithDiscount: calculatedValues.servingPriceWithDiscount,
    },
  };
};
```

**Key patterns**:
- Input validation with clear error messages
- Delegation to helper for complex calculations
- Separation of UI fields and analytics data
- Pure transformation with no side effects

### 3. Helper Functions (helpers.ts)

```typescript
import type { ReactivationPriceResponse } from '@data-access/query/reactivation';
import { convertMoneyToNumber } from '@libs/currency';
import { getHFWeek } from '@libs/date';
import type { GetCalculatedPriceValuesReturn } from './types';
import { truncateToTwoDecimals } from './utils';

/**
 * Calculates all price-related values from the API response.
 * Encapsulates all mathematical operations in one place for better testability and maintainability.
 *
 * @param response - The reactivation price API response
 * @param product - The first product from the response
 * @returns Object containing all calculated price values (raw and truncated for analytics)
 */
export const getCalculatedPriceValues = (
  response: ReactivationPriceResponse,
  product: ReactivationPriceResponse['products'][0]
): GetCalculatedPriceValuesReturn => {
  // Extract basic product information
  const productUnitPrice = convertMoneyToNumber(product.price);
  const productPaidPrice = convertMoneyToNumber(product.paidPrice);
  const shippingAmount = convertMoneyToNumber(response.shipping.base);
  const shippingDiscountAmount = convertMoneyToNumber(
    response.shipping.discount
  );
  const totalServings = product.meals * product.size;

  // Calculate total prices (raw values)
  const totalPriceRaw =
    convertMoneyToNumber(response.subtotal) +
    convertMoneyToNumber(response.totalTax) +
    convertMoneyToNumber(response.shipping.base);

  const totalPriceWithDiscountRaw = convertMoneyToNumber(response.grandTotal);

  // Calculate analytics price fields with truncation
  const totalPrice = truncateToTwoDecimals(totalPriceRaw);
  const totalPriceWithDiscount = truncateToTwoDecimals(
    totalPriceWithDiscountRaw
  );
  const boxPrice = truncateToTwoDecimals(productUnitPrice);
  const boxPriceWithDiscount = truncateToTwoDecimals(productPaidPrice);
  const servingPrice = truncateToTwoDecimals(
    totalServings > 0 ? productUnitPrice / totalServings : 0
  );
  const servingPriceWithDiscount = truncateToTwoDecimals(
    totalServings > 0 ? productPaidPrice / totalServings : 0
  );
  const shippingPrice = truncateToTwoDecimals(shippingAmount);
  const shippingDiscount = truncateToTwoDecimals(shippingDiscountAmount);

  return {
    productUnitPrice,
    productPaidPrice,
    shippingAmount,
    shippingDiscountAmount,
    totalServings,
    totalPriceRaw,
    totalPriceWithDiscountRaw,
    totalPrice,
    totalPriceWithDiscount,
    boxPrice,
    boxPriceWithDiscount,
    servingPrice,
    servingPriceWithDiscount,
    shippingPrice,
    shippingDiscount,
  };
};

/**
 * Builds API request parameters for voucher price details.
 */
export const getFetchVoucherPriceDetailsParams = (
  voucher: ReactivationBannerVoucher,
  subscription: ReactivationBannerSubscription
): ReactivationPriceParams => {
  return {
    voucherCode: voucher.code,
    planID: subscription?.planId,
    customerUUID: subscription?.customerUUID,
    delivery: {
      handle: subscription?.deliveryHandle,
      date: subscription?.deliveryDate,
      hfWeek: getHFWeek(),
    },
    products: [{ handle: subscription?.productHandle }],
    shippingAddress: subscription?.shippingAddress,
  };
};
```

**Key patterns**:
- Detailed JSDoc documentation
- Clear step-by-step calculations with comments
- Delegation to utility functions for reusable operations
- Returns comprehensive data structure for different uses
- Guards against division by zero

### 4. Utility Functions (utils.ts)

```typescript
/**
 * Truncates a number to 2 decimal places for analytics consistency.
 * Used to ensure price values match analytics platform expectations.
 */
export const truncateToTwoDecimals = (value: number): number => {
  return Math.floor(value * 100) / 100;
};
```

**Key patterns**:
- Pure function with no dependencies
- Single responsibility
- Clear documentation of purpose
- Can be reused across features

## Additional Examples from Codebase

### Nested Transformation Pattern

```typescript
// features/dynamic-screen-feature/widgets/hooks/transformDeliveryBenefitsResponse.ts

export const transformDeliveryBenefitsResponse = (
  response: DeliveryBenefitsApiResponse
): DeliveryBenefits => {
  return {
    benefits: response.data.map(transformBenefit),
    metadata: transformMetadata(response.metadata),
  };
};

const transformBenefit = (apiBenefit: ApiBenefit): Benefit => ({
  id: apiBenefit.benefit_id,
  title: apiBenefit.title_text,
  description: apiBenefit.description_text,
  icon: transformIcon(apiBenefit.icon_data),
});
```

**Pattern**: Break down complex nested transformations into smaller, focused functions.

### Collection Transformation Pattern

```typescript
// Transforming arrays of API data
export const transformRecipeList = (apiRecipes: ApiRecipe[]): Recipe[] => {
  return apiRecipes.map(transformRecipe);
};

// With filtering and sorting
export const transformAvailableRecipes = (
  apiRecipes: ApiRecipe[],
  userPlan: Plan
): Recipe[] => {
  return apiRecipes
    .filter((recipe) => isRecipeAvailable(recipe, userPlan))
    .map(transformRecipe)
    .sort((a, b) => a.priority - b.priority);
};
```

**Pattern**: Chain transformation with business logic filters when appropriate.

## Anti-Patterns to Avoid

### ❌ Mixing Transformation with Side Effects

```typescript
// BAD: Don't do this
export const transformUser = (apiUser: ApiUser): User => {
  // Side effect - calling analytics
  trackUserTransformation(apiUser.user_id);

  return {
    id: apiUser.user_id,
    name: `${apiUser.first_name} ${apiUser.last_name}`,
  };
};
```

### ❌ Business Logic in Transformers

```typescript
// BAD: Don't do this
export const transformProduct = (apiProduct: ApiProduct): Product => {
  const product = {
    id: apiProduct.product_id,
    name: apiProduct.name,
    price: convertMoneyToNumber(apiProduct.price),
  };

  // Business logic - should be in helper
  if (product.price > 50) {
    product.eligibleForFreeShipping = true;
  }

  return product;
};
```

### ✅ Correct Separation

```typescript
// transformers.ts
export const transformProduct = (apiProduct: ApiProduct): Product => ({
  id: apiProduct.product_id,
  name: apiProduct.name,
  price: convertMoneyToNumber(apiProduct.price),
});

// helpers.ts
export const isEligibleForFreeShipping = (product: Product): boolean => {
  return product.price > 50;
};
```

## Testing Examples

### Testing Transformers

```typescript
describe('transformReactivationPriceResponse', () => {
  it('transforms valid response with all fields', () => {
    const mockResponse: ReactivationPriceResponse = {
      products: [
        {
          priceId: 'price-123',
          id: 'product-456',
          price: { amount: '29.99', currency: 'USD' },
          paidPrice: { amount: '19.99', currency: 'USD' },
          pricePerServing: {
            original: { amount: '4.99', currency: 'USD' },
            withDiscount: { amount: '3.33', currency: 'USD' },
          },
          meals: 3,
          size: 2,
        },
      ],
      subtotal: { amount: '29.99', currency: 'USD' },
      totalTax: { amount: '2.40', currency: 'USD' },
      grandTotal: { amount: '27.39', currency: 'USD' },
      shipping: {
        base: { amount: '5.00', currency: 'USD' },
        discount: { amount: '5.00', currency: 'USD' },
      },
      currencyCode: 'USD',
    };

    const result = transformReactivationPriceResponse(mockResponse);

    expect(result.initialPrice).toBe(2999);
    expect(result.discountedPrice).toBe(1999);
    expect(result.initialPricePerServing).toBe(499);
    expect(result.discountedPricePerServing).toBe(333);
    expect(result.analyticsEventValues.currency).toBe('USD');
  });

  it('throws error when products array is empty', () => {
    const mockResponse: ReactivationPriceResponse = {
      products: [],
      // ... other fields
    };

    expect(() => transformReactivationPriceResponse(mockResponse)).toThrow(
      'No product found in price response'
    );
  });
});
```

### Testing Helpers

```typescript
describe('getCalculatedPriceValues', () => {
  it('calculates all price values correctly', () => {
    const mockResponse = createMockReactivationPriceResponse();
    const mockProduct = mockResponse.products[0];

    const result = getCalculatedPriceValues(mockResponse, mockProduct);

    expect(result.productUnitPrice).toBe(2999);
    expect(result.servingPrice).toBe(499); // 2999 / 6 servings truncated
    expect(result.totalPrice).toBeCloseTo(3739, 0); // subtotal + tax + shipping
  });

  it('handles zero servings without crashing', () => {
    const mockProduct = {
      ...createMockProduct(),
      meals: 0,
      size: 0,
    };

    const result = getCalculatedPriceValues(mockResponse, mockProduct);

    expect(result.servingPrice).toBe(0);
    expect(result.servingPriceWithDiscount).toBe(0);
  });
});
```

## Key Takeaways

1. **File Organization**: Separate transformers.ts, helpers.ts, utils.ts
2. **Transformers**: Pure data shape conversion, no business logic
3. **Helpers**: Business logic and complex calculations
4. **Utils**: Generic, reusable pure functions
5. **Types**: Explicit types for all inputs and outputs
6. **Validation**: Always validate transformer inputs
7. **Testing**: Test each layer in isolation
8. **Documentation**: JSDoc for complex functions

For API documentation references, see [api-docs.md](api-docs.md).
