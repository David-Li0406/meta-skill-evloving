# JavaScript/TypeScript Clean Code Rules

## Naming Conventions

### Variables and Functions
- Use camelCase: `getUserName`, `totalPrice`
- Boolean variables: prefix with `is`, `has`, `should`: `isActive`, `hasPermission`
- Constants: UPPER_SNAKE_CASE: `MAX_RETRY_COUNT`

### Common Anti-patterns
- Avoid: `data`, `info`, `obj`, `val`, `temp`, `result` without context
- Avoid: single letters except `i`, `j`, `k` for loops
- Avoid: Hungarian notation (`strName`, `intCount`)

### Good Examples
```javascript
// Bad
const d = new Date();
const u = getU();
let flag = true;

// Good
const createdAt = new Date();
const currentUser = getCurrentUser();
let isAuthenticated = true;
```

## Function Length

**Target: Maximum 20 lines** (excluding blank lines and closing braces)

Functions exceeding 20 lines often indicate:
- Multiple responsibilities (violates Single Responsibility Principle)
- Nested logic that could be extracted
- Opportunity for helper functions

### Refactoring Example
```javascript
// Bad: 35 lines, does too much
function processOrder(order) {
  // Validation
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  // Apply discount
  if (order.coupon) {
    const discount = getDiscount(order.coupon);
    total -= total * discount;
  }
  // Add shipping
  const shipping = calculateShipping(order.address);
  total += shipping;
  // Save to database
  const savedOrder = await db.orders.create({
    ...order,
    total,
    status: 'pending'
  });
  // Send confirmation email
  await sendEmail(order.email, 'Order confirmed', generateEmailBody(savedOrder));
  return savedOrder;
}

// Good: Split into focused functions
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  const savedOrder = await saveOrder(order, total);
  await sendOrderConfirmation(savedOrder);
  return savedOrder;
}
```

## Comment Guidelines

### Redundant Comments (Remove)
```javascript
// Set the name - REDUNDANT
user.name = 'John';

// Loop through items - REDUNDANT
for (const item of items) {

// Increment counter - REDUNDANT
counter++;

// Return the result - REDUNDANT
return result;
```

### Valuable Comments (Keep)
```javascript
// HACK: API returns null instead of empty array for new users
const orders = response.data || [];

// Performance: Using Set for O(1) lookup instead of array
const uniqueIds = new Set(ids);

// FIXME: This breaks when timezone changes, need to use UTC
const deadline = new Date('2024-01-01');

// Regex matches ISO 8601 format (e.g., 2024-01-15T10:30:00Z)
const isoDatePattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
```

## Arrow Functions vs Function Declarations

Use arrow functions for:
- Callbacks and array methods
- Short, single-expression functions

Use function declarations for:
- Top-level functions
- Methods requiring `this` context
- Functions needing hoisting

## Async/Await

Prefer `async/await` over Promise chains for readability:

```javascript
// Less clear
function getUser(id) {
  return fetchUser(id)
    .then(user => fetchProfile(user.profileId))
    .then(profile => ({ ...user, profile }))
    .catch(handleError);
}

// More clear
async function getUser(id) {
  try {
    const user = await fetchUser(id);
    const profile = await fetchProfile(user.profileId);
    return { ...user, profile };
  } catch (error) {
    handleError(error);
  }
}
```
