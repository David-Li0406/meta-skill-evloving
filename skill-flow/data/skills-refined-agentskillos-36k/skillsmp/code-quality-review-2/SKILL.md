---
name: code-quality-review
description: |
  Code quality verification skill for reviewer agents.
  Provides checklists for logic clarity, error handling, maintainability, and performance.
  Use during VERIFICATION phase to assess implementation quality.
---

# Code Quality Review

Systematic code quality assessment for ultrawork verification phase.

## What This Skill Provides

Structured checklists for evaluating code quality across multiple dimensions:
- Logic and readability
- Error handling and resilience
- Code style and maintainability
- Performance and efficiency

## When to Use This Skill

- During VERIFICATION phase after workers complete tasks
- When reviewing evidence before marking tasks as complete
- Before approving design decisions that impact code quality
- When auditing implementations for production readiness

## Quality Dimensions

### 1. Logic and Readability

**Checklist:**

```
[ ] Functions have single, clear responsibilities
[ ] Functions are under 50 lines
[ ] Files are under 800 lines
[ ] Nesting depth is 4 levels or less
[ ] Control flow is straightforward (no convoluted conditionals)
[ ] Variable and function names are descriptive
[ ] No magic numbers (constants are named)
[ ] Complex logic has explanatory comments
[ ] Boolean conditions are readable (avoid double negatives)
[ ] Early returns reduce nesting
```

**Red Flags:**
- Functions doing multiple unrelated things
- Variable names like `x`, `tmp`, `data`, `thing`
- Magic numbers: `if (status === 42)`
- Deep nesting: `if { if { if { if { ... }}}}`
- Complex conditions: `if (!(!isValid && !isExpired))`

**Examples:**

```javascript
// ❌ Bad: Unclear logic, magic numbers
function process(x) {
  if (x > 100 && x < 500) {
    return x * 0.95;
  }
  return x;
}

// ✅ Good: Clear intent, named constants
const BULK_ORDER_MIN = 100;
const BULK_ORDER_MAX = 500;
const BULK_DISCOUNT_RATE = 0.95;

function applyBulkDiscount(orderTotal) {
  const isBulkOrder = orderTotal >= BULK_ORDER_MIN && orderTotal <= BULK_ORDER_MAX;
  return isBulkOrder ? orderTotal * BULK_DISCOUNT_RATE : orderTotal;
}
```

### 2. Error Handling

**Checklist:**

```
[ ] All async operations have error handling
[ ] try/catch blocks used for risky operations
[ ] Errors are logged with context
[ ] User-facing errors are sanitized
[ ] Error messages are actionable
[ ] No silent failures (empty catch blocks)
[ ] Edge cases are handled (null, undefined, empty arrays)
[ ] Input validation exists for external data
[ ] Database operations handle connection failures
[ ] API calls have timeout handling
```

**Red Flags:**
- Empty catch blocks: `catch (e) {}`
- Unhandled promise rejections
- Missing null checks before property access
- Generic error messages: `throw new Error('error')`
- Exposing stack traces to users

**Examples:**

```javascript
// ❌ Bad: Silent failure
try {
  await saveUser(user);
} catch (e) {
  // Silent failure - data loss risk
}

// ✅ Good: Proper error handling
try {
  await saveUser(user);
} catch (error) {
  logger.error('Failed to save user', { userId: user.id, error });
  throw new Error('Unable to save user data. Please try again.');
}
```

### 3. Code Duplication

**Checklist:**

```
[ ] No copy-pasted code blocks
[ ] Repeated logic is extracted to functions
[ ] Similar patterns use shared utilities
[ ] Constants are defined once
[ ] Configuration is centralized
[ ] Validation logic is reusable
[ ] Data transformation uses shared helpers
```

**Red Flags:**
- Same code in multiple places with minor variations
- Repeated validation patterns
- Multiple implementations of same algorithm
- Copy-pasted API error handling

**Examples:**

```javascript
// ❌ Bad: Duplication
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ✅ Good: Single source of truth
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
function validateEmail(email) {
  return EMAIL_REGEX.test(email);
}
```

### 4. Code Style

**Checklist:**

```
[ ] Consistent indentation (spaces/tabs)
[ ] Consistent naming convention (camelCase, PascalCase, etc.)
[ ] Consistent quote style (single/double)
[ ] No trailing whitespace
[ ] Proper spacing around operators
[ ] Consistent brace style
[ ] No commented-out code
[ ] No console.log statements in production code
[ ] Imports are organized (grouped, sorted)
[ ] No unused imports or variables
```

**Red Flags:**
- Mixed quote styles in same file
- Inconsistent naming: `getUserData()`, `get_user_info()`
- Large blocks of commented code
- Debug statements: `console.log('HERE')`

### 5. Performance

**Checklist:**

```
[ ] Algorithms use appropriate complexity (O(n) vs O(n²))
[ ] Expensive operations are cached
[ ] Database queries use indexes
[ ] N+1 query problems avoided
[ ] Large datasets are paginated
[ ] Unnecessary re-renders prevented (React)
[ ] Heavy computations are memoized
[ ] File operations are batched
[ ] Network requests are minimized
```

**Red Flags:**
- Nested loops over large datasets
- Database queries inside loops
- Missing pagination on list endpoints
- Re-computing same values in renders
- Loading entire dataset when pagination possible

**Examples:**

```javascript
// ❌ Bad: O(n²) complexity, N+1 queries
for (const order of orders) {
  const user = await db.users.findById(order.userId); // N+1!
  results.push({ ...order, user });
}

// ✅ Good: Single query with join
const ordersWithUsers = await db.orders
  .find({ id: { $in: orderIds } })
  .populate('user');
```

### 6. Testing

**Checklist:**

```
[ ] New code has corresponding tests
[ ] Tests verify actual behavior (not just pass)
[ ] Edge cases are tested
[ ] Error paths are tested
[ ] Test names describe what is tested
[ ] Tests are isolated (no shared state)
[ ] Mocks are used for external dependencies
[ ] Test coverage is adequate (not necessarily 100%)
```

**Red Flags:**
- No tests for new functionality
- Tests that always pass (no assertions)
- Flaky tests (sometimes pass/fail)
- Tests depending on execution order
- Testing implementation details instead of behavior

## Review Process

### Step 1: Static Analysis

```bash
# Check for syntax errors
npm run lint

# Check for type errors (TypeScript)
npm run type-check

# Check for security issues
npm audit
```

### Step 2: Code Reading

Read the modified files completely. Check:
- Does the code do what it claims?
- Are edge cases handled?
- Is error handling comprehensive?
- Is the logic clear?

### Step 3: Test Review

```bash
# Run tests
npm test

# Check coverage
npm run test:coverage
```

Verify:
- Tests actually test behavior
- Edge cases are covered
- Error conditions are tested

### Step 4: Performance Check

Look for:
- Algorithm complexity
- Database query patterns
- Caching opportunities
- Resource leaks

## Quality Scoring

| Category | Weight | Score |
|----------|--------|-------|
| Logic Clarity | 25% | 0-10 |
| Error Handling | 25% | 0-10 |
| Maintainability | 20% | 0-10 |
| Performance | 15% | 0-10 |
| Testing | 15% | 0-10 |

**Overall Score = Weighted Average**

- **8-10**: Excellent, ready to merge
- **6-7**: Good, minor improvements recommended
- **4-5**: Fair, significant improvements needed
- **0-3**: Poor, major rework required

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Large function | Extract smaller functions |
| Deep nesting | Use early returns, extract conditions |
| Magic numbers | Define named constants |
| No error handling | Add try/catch, validate inputs |
| Duplicated code | Extract shared utility |
| Poor naming | Rename to describe purpose |
| Missing tests | Write tests for new code |
| O(n²) loops | Use hash maps, optimize algorithm |

## Evidence Requirements

When reviewing code quality, collect evidence:

```
### Code Quality Assessment
- Logic Clarity: 8/10
  - Functions under 50 lines: ✓
  - Clear naming: ✓
  - No magic numbers: ✓

- Error Handling: 7/10
  - Try/catch present: ✓
  - Null checks: ✓
  - Missing timeout handling: ✗

- Maintainability: 9/10
  - No duplication: ✓
  - Consistent style: ✓
  - Well-tested: ✓

Overall: 8/10 - Ready to merge
```

## Integration with Ultrawork

During VERIFICATION phase:

```bash
# Review implemented files
reviewer --task-id 1

# Add quality assessment to evidence
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --add-evidence "Code Quality: 8/10 (Logic: 8, Errors: 7, Maintainability: 9)"
```

## Best Practices

1. **Be specific** - Don't just say "improve naming", suggest actual names
2. **Provide examples** - Show good and bad code side-by-side
3. **Prioritize issues** - Critical bugs before style nitpicks
4. **Consider context** - Prototype code has different standards than production
5. **Be constructive** - Suggest solutions, not just problems
6. **Verify fixes** - Re-review after changes are made

## Quick Reference

**Must-have quality standards:**
- Clear, descriptive naming
- Proper error handling
- No duplication
- Tests for new code
- No obvious performance issues

**Nice-to-have quality improvements:**
- Comprehensive documentation
- 100% test coverage
- Optimal algorithm complexity
- Perfect code style consistency
