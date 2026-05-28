---
name: safe-code-refactoring
description: Use this skill to systematically improve code structure, readability, and maintainability while ensuring functionality remains unchanged through safe refactoring practices.
---

# Safe Code Refactoring

## Purpose
Improve code structure, readability, and maintainability without changing its external behavior or functionality.

## When to Use
- Code is hard to understand or modify
- Duplicated code exists
- Functions are too long or complex
- Code smells are present
- Preparing for new features

## Key Principles
1. **Test First**: Ensure all tests pass before starting any refactoring.
2. **Small, Incremental Changes**: Make one change at a time and test after each change.
3. **Preserve Functionality**: Refactoring should not change the external behavior of the code.
4. **Commit Often**: Create savepoints for rollback and document changes clearly.

## Refactoring Patterns

### Extract Method
Break down large functions into smaller, focused ones:
```javascript
// Before
function processOrder(order) {
  // validate order
  // calculate totals
  // apply discounts
  // save to database
}

// After
function processOrder(order) {
  validateOrder(order);
  const totals = calculateTotals(order);
  const discountedTotal = applyDiscounts(totals, order.customer);
  saveOrder(order, discountedTotal);
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

## Workflow for Safe Refactoring

### Phase 1: Assessment & Planning
1. **Identify Refactoring Need**: Look for code smells like long methods, duplicate code, or poor naming.
2. **Capture Current Behavior**: Ensure all tests pass and document current behavior.
3. **Plan the Refactoring**: Define the goal and identify risk areas.

### Phase 2: Execution
1. **Establish Baseline**: Run tests and create a checkpoint commit.
2. **Make Changes**: Apply one refactoring move at a time.
3. **Run Tests**: Verify tests pass after each change.
4. **Commit Changes**: Document each change clearly.

### Phase 3: Verification
1. **Test Suite Validation**: Run the full test suite to ensure all tests pass.
2. **Manual Smoke Testing**: Test main workflows and edge cases.
3. **Performance Check**: Compare performance before and after refactoring.

### Phase 4: Rollback Strategy
- If tests fail, revert to the last known good state immediately.
- Use Git commands to undo changes or restore previous commits.

## Best Practices
- Always have tests before refactoring.
- Make small, incremental changes.
- Avoid mixing refactoring with feature additions.
- Document changes and commit frequently.

## Common Refactoring Anti-Patterns
- **Big Bang Refactoring**: Avoid refactoring the entire codebase at once.
- **Refactoring Without Tests**: Always verify current behavior with tests first.
- **Silent Behavior Changes**: Refactoring should not change behavior; if it does, it's not refactoring.

## Conclusion
Safe code refactoring is essential for maintaining code quality and ensuring that functionality remains intact. By following systematic approaches and best practices, you can improve your codebase effectively and safely.