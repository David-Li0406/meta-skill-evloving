# Data Transformation - API Reference

Comprehensive API reference for data transformation patterns including transformers, helpers, and utility functions.

## Official Documentation

- **TypeScript**: https://www.typescriptlang.org/docs/
- **JavaScript Array Methods**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

## File Structure

### Transformers File (transformers.ts)

Contains functions that convert API responses into application domain models.

```typescript
/**
 * Transform API response to domain model
 * @param response - API response object
 * @returns Domain model object
 * @throws Error if validation fails
 */
export const transformEntityName = (
  response: ApiResponse
): DomainModel => {
  // Validation
  if (!response.requiredField) {
    throw new Error('Missing required field');
  }

  // Transformation
  return {
    id: response.entity_id,
    name: response.entity_name,
  };
};
```

### Helpers File (helpers.ts)

Contains business logic and calculations.

```typescript
/**
 * Calculate business logic result
 * @param input - Input parameters
 * @returns Calculated result
 */
export const calculateBusinessLogic = (
  input: InputType
): ResultType => {
  // Business logic implementation
  return result;
};
```

### Utils File (utils.ts)

Contains pure utility functions with no domain knowledge.

```typescript
/**
 * Pure utility function
 * @param input - Generic input
 * @returns Transformed output
 */
export const utilityFunction = (input: any): any => {
  // Pure transformation
  return output;
};
```

## Transformer Functions

### Single Entity Transformation

Transform a single API entity to domain model.

```typescript
export const transformUser = (apiUser: ApiUser): User => ({
  id: apiUser.user_id,
  name: `${apiUser.first_name} ${apiUser.last_name}`,
  email: apiUser.email_address,
  createdAt: new Date(apiUser.created_at),
});
```

**Parameters:**
- `apiUser: ApiUser` - API response for a single user

**Returns:**
- `User` - Domain model user object

**Throws:**
- None (assumes valid input)

### Collection Transformation

Transform an array of API entities.

```typescript
export const transformUserList = (apiUsers: ApiUser[]): User[] => {
  return apiUsers.map(transformUser);
};
```

**Parameters:**
- `apiUsers: ApiUser[]` - Array of API user responses

**Returns:**
- `User[]` - Array of domain model users

### Nested Transformation

Transform entities with nested relationships.

```typescript
export const transformOrder = (apiOrder: ApiOrder): Order => ({
  id: apiOrder.order_id,
  user: transformUser(apiOrder.user_data),
  items: apiOrder.line_items.map(transformOrderItem),
  total: convertMoneyToNumber(apiOrder.total_amount),
  createdAt: new Date(apiOrder.created_at),
});
```

**Parameters:**
- `apiOrder: ApiOrder` - API response for an order

**Returns:**
- `Order` - Domain model order with nested user and items

### With Validation

Transform with input validation and error handling.

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

  const calculatedValues = getCalculatedPriceValues(response, product);

  return {
    initialPrice: calculatedValues.productUnitPrice,
    discountedPrice: calculatedValues.productPaidPrice,
    currency: product.price.currency,
    savings: calculatedValues.productUnitPrice - calculatedValues.productPaidPrice,
  };
};
```

**Parameters:**
- `response: ReactivationPriceResponse` - API response with price data

**Returns:**
- `VoucherPriceInfo` - Transformed price information

**Throws:**
- `Error` - When no products found
- `Error` - When product data is invalid

## Helper Functions

### Business Logic Calculation

Calculate values based on business rules.

```typescript
export const getCalculatedPriceValues = (
  response: ReactivationPriceResponse,
  product: ReactivationPriceResponse['products'][0]
): CalculatedPriceValues => {
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
```

**Parameters:**
- `response: ReactivationPriceResponse` - Full API response
- `product: ReactivationPriceResponse['products'][0]` - Single product from response

**Returns:**
- `CalculatedPriceValues` - All calculated price values

### Conditional Logic

Implement business rules with boolean logic.

```typescript
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
```

**Parameters:**
- `recipe: Recipe` - Recipe to add
- `userPlan: Plan` - User's subscription plan
- `cartSize: number` - Current cart size

**Returns:**
- `boolean` - Whether recipe can be added

### Status Determination

Determine entity status based on business rules.

```typescript
export const getOrderStatus = (order: Order): OrderStatus => {
  if (order.cancelledAt) return 'cancelled';
  if (order.deliveredAt) return 'delivered';
  if (order.shippedAt) return 'shipped';
  if (order.confirmedAt) return 'confirmed';

  return 'pending';
};
```

**Parameters:**
- `order: Order` - Order to check

**Returns:**
- `OrderStatus` - Current order status

## Utility Functions

### Money Conversion

Convert API money objects to numbers.

```typescript
export const convertMoneyToNumber = (money: Money): number => {
  return Math.round(parseFloat(money.amount) * 100);
};
```

**Parameters:**
- `money: Money` - API money object with amount and currency

**Returns:**
- `number` - Amount in cents (smallest currency unit)

### Number Formatting

Format numbers for display.

```typescript
export const truncateToTwoDecimals = (value: number): number => {
  return Math.trunc(value * 100) / 100;
};
```

**Parameters:**
- `value: number` - Number to truncate

**Returns:**
- `number` - Number truncated to 2 decimal places

### Price Formatting

Format prices for display with currency.

```typescript
export const formatPrice = (cents: number, currency: string): string => {
  const amount = cents / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};
```

**Parameters:**
- `cents: number` - Amount in cents
- `currency: string` - Currency code (e.g., 'USD')

**Returns:**
- `string` - Formatted price string (e.g., '$29.99')

### Email Validation

Validate email format.

```typescript
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
```

**Parameters:**
- `email: string` - Email address to validate

**Returns:**
- `boolean` - Whether email format is valid

### Date Utilities

Format and manipulate dates.

```typescript
export const formatDate = (date: Date, format: DateFormat): string => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: format === 'short' ? 'short' : 'long',
    day: 'numeric',
  }).format(date);
};

export const isDateInPast = (date: Date): boolean => {
  return date.getTime() < Date.now();
};
```

## Type Definitions

### API Response Types

Define types for API responses.

```typescript
export interface ReactivationPriceResponse {
  products: Array<{
    priceId: string;
    price: Money;
    paidPrice: Money;
    pricePerServing: {
      original: Money;
      withDiscount: Money;
    };
  }>;
  deliveryPrice: Money;
  originalTotalPrice: Money;
  totalPrice: Money;
  currencyCode: string;
}

export interface Money {
  amount: string;
  currency: string;
}
```

### Domain Model Types

Define types for transformed domain models.

```typescript
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

### Helper Return Types

Define types for helper function returns.

```typescript
export interface GetCalculatedPriceValuesReturn {
  productUnitPrice: number;
  productPaidPrice: number;
  deliveryPrice: number;
  originalTotalPrice: number;
  totalPrice: number;
  savings: number;
}
```

## Error Handling

### Validation Errors

Throw errors for invalid input.

```typescript
if (!response.products[0]) {
  throw new Error('No product found in price response');
}

if (!product.priceId) {
  throw new Error('Invalid product data: missing priceId');
}
```

### Type Guards

Use type guards for safe property access.

```typescript
const isValidProduct = (product: unknown): product is Product => {
  return (
    typeof product === 'object' &&
    product !== null &&
    'priceId' in product &&
    'price' in product
  );
};

if (!isValidProduct(product)) {
  throw new Error('Invalid product structure');
}
```

## Testing Patterns

### Transformer Tests

Test transformers with mock data.

```typescript
describe('transformUser', () => {
  it('transforms API user to domain user', () => {
    const apiUser: ApiUser = {
      user_id: '123',
      first_name: 'John',
      last_name: 'Doe',
      email_address: 'john@example.com',
    };

    const result = transformUser(apiUser);

    expect(result).toEqual({
      id: '123',
      name: 'John Doe',
      email: 'john@example.com',
    });
  });
});
```

### Helper Tests

Test business logic in isolation.

```typescript
describe('canAddToCart', () => {
  it('returns true when all conditions met', () => {
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

### Utility Tests

Test pure functions.

```typescript
describe('convertMoneyToNumber', () => {
  it('converts money to cents', () => {
    const money: Money = {
      amount: '29.99',
      currency: 'USD',
    };

    expect(convertMoneyToNumber(money)).toBe(2999);
  });
});
```

## Common Patterns

### Compose Transformers

Combine multiple transformers.

```typescript
export const transformOrderWithDetails = (apiOrder: ApiOrder): OrderWithDetails => ({
  ...transformOrder(apiOrder),
  user: transformUser(apiOrder.user_data),
  shippingAddress: transformAddress(apiOrder.shipping_address),
  items: apiOrder.line_items.map(item => ({
    ...transformOrderItem(item),
    recipe: transformRecipe(item.recipe_data),
  })),
});
```

### Conditional Transformation

Transform based on conditions.

```typescript
export const transformProduct = (apiProduct: ApiProduct): Product => {
  const baseProduct = {
    id: apiProduct.product_id,
    name: apiProduct.product_name,
  };

  if (apiProduct.discount) {
    return {
      ...baseProduct,
      discountedPrice: calculateDiscountedPrice(apiProduct),
      originalPrice: convertMoneyToNumber(apiProduct.price),
    };
  }

  return {
    ...baseProduct,
    price: convertMoneyToNumber(apiProduct.price),
  };
};
```

### Array Transformation with Filtering

Transform and filter in one pass.

```typescript
export const transformActiveRecipes = (apiRecipes: ApiRecipe[]): Recipe[] => {
  return apiRecipes
    .filter(recipe => recipe.status === 'active')
    .map(transformRecipe);
};
```

## Best Practices

1. **Always validate input** - Check for required fields before transformation
2. **Use explicit types** - Define types for inputs, outputs, and intermediates
3. **Keep transformers pure** - No side effects, same input = same output
4. **Separate concerns** - Transformers in transformers.ts, business logic in helpers.ts
5. **Handle errors gracefully** - Throw clear errors with actionable messages
6. **Document complex logic** - Add JSDoc comments for non-obvious transformations
7. **Test in isolation** - Unit test each transformer/helper/util separately
8. **Use type guards** - Validate structure at runtime when needed
