---
name: code-refactoring
description: Use this skill when you need to improve code structure, readability, and maintainability without changing its external behavior.
---

# Skill body

## Purpose
Improve code structure, readability, and maintainability without changing its external behavior or functionality.

## When to Use
- Code is hard to understand or modify
- Duplicated code exists
- Functions are too long or complex
- Code smells are present
- Preparing for new features

## Key Principles
1. **Make it Work, Make it Right, Make it Fast**
   - Ensure tests pass before and after refactoring
   - Improve code structure and readability first
   - Optimize performance only when needed

2. **Small, Incremental Changes**
   - Make one change at a time
   - Test after each change
   - Commit working code frequently

3. **Maintain Functionality**
   - Don't change behavior during refactoring
   - Use tests to verify correctness
   - Document any behavioral changes if necessary

## Common Refactoring Patterns

### Extract Method
Break down large functions into smaller, focused ones:
```javascript
// Before
function processOrder(order) {
  // validate order (10 lines)
  // calculate totals (15 lines)
  // apply discounts (20 lines)
  // save to database (10 lines)
}

// After
function processOrder(order) {
  validateOrder(order);
  const totals = calculateTotals(order);
  const discountedTotal = applyDiscounts(totals, order.customer);
  saveOrder(order, discountedTotal);
}
```

### Extract Variable
Replace complex expressions with well-named variables:
```javascript
// Before
if (user.age >= 18 && user.country === 'US' && user.hasValidId) {
  // ...
}

// After
const isEligibleVoter = user.age >= 18 &&
                        user.country === 'US' &&
                        user.hasValidId;
if (isEligibleVoter) {
  // ...
}
```

### Remove Duplication (DRY)
Consolidate repeated code into reusable functions:
```javascript
// Before
function calculateTaxForUS(amount) {
  return amount * 0.08;
}
function calculateTaxForCA(amount) {
  return amount * 0.13;
}

// After
function calculateTax(amount, region) {
  const taxRates = { US: 0.08, CA: 0.13 };
  return amount * (taxRates[region] || 0);
}
```

### Simplify Conditionals
Make complex conditions more readable:
```javascript
// Before
if (!(status === 'active' || status === 'pending') || disabled) {
  return;
}

// After
const isInactiveStatus = status !== 'active' && status !== 'pending';
if (isInactiveStatus || disabled) {
  return;
}
```

### Rename for Clarity
Use descriptive names that reveal intent:
```javascript
// Before
const d = new Date();
// After
const currentDate = new Date();
```

## Best Practices
- Always have tests before refactoring
- Make small, incremental changes
- Run tests after each change
- Avoid refactoring and adding features simultaneously