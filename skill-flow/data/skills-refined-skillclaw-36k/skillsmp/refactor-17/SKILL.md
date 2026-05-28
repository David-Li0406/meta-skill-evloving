---
name: refactor
description: Improve code quality while preserving behavior. Handles tech debt, pattern migrations, and structural improvements. Test suite is the contract - all tests must continue passing.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Refactor Skill

## Purpose

Improve code quality without changing behavior. Make code more maintainable, readable, and efficient while ensuring all existing tests continue to pass.

## When to Use

- **Tech debt reduction**: Accumulated quality issues need addressing
- **Pattern migration**: Codebase needs to adopt new patterns consistently
- **Dependency updates**: Major version upgrades require code changes
- **Performance optimization**: Code needs optimization without feature changes
- **Post-merge cleanup**: Feature landed but left structural debt
- **Post-implementation cleanup**: Spec group completed, code quality improvements identified

## Relationship to Spec Groups

Unlike implementation (`/implement`) which follows spec groups, refactoring uses **test suite as contract**. However:

- **Post-spec refactoring**: After a spec group completes, `/code-review` may identify quality improvements. These become refactor tasks (separate from original spec).
- **Context preservation**: If refactoring targets code from a recent spec group, note the spec group ID for traceability.
- **No spec required**: Refactoring doesn't need a spec group - the test suite IS the specification.

## Key Principle: Test Suite is Contract

Unlike implementation (spec-driven), refactoring uses the **test suite as the contract**.

| Aspect     | Implementation      | Refactoring               |
| ---------- | ------------------- | ------------------------- |
| Contract   | Spec with ACs       | Test suite                |
| Success    | All ACs implemented | All tests still pass      |
| Constraint | Follow spec exactly | Preserve behavior exactly |

## Refactoring Process

### Step 1: Verify Test Coverage

Before ANY refactoring:

```bash
# Check test coverage of targets
npm test -- --coverage --collectCoverageFrom="src/services/target.ts"
```

**Required**: >80% coverage on refactoring targets.

**If coverage <80%**: STOP. Tests must be added first. This is a separate task.

### Step 2: Establish Baseline

```bash
# Run full test suite
npm test

# Record baseline
npm test -- --json > /tmp/baseline-tests.json

# Type check
npx tsc --noEmit

# Lint
npm run lint
```

Document baseline:

```markdown
## Baseline (pre-refactor)

- Tests: 147 passing, 0 failing
- Type errors: 0
- Lint warnings: 12
- Coverage: 84%
```

### Step 3: Incremental Changes

**Never refactor everything at once.** Work incrementally:

```
1. Identify smallest change that improves code
2. Make change
3. Run tests
4. Commit if green
5. Repeat
```

Each commit should be:

- **Atomic**: One logical change
- **Green**: All tests pass
- **Reversible**: Easy to revert if needed

### Step 4: Common Refactoring Patterns

#### Extract Method

```typescript
// Before: 50-line function
async processOrder(order: Order) {
  // validation logic (20 lines)
  // calculation logic (15 lines)
  // persistence logic (15 lines)
}

// After: Extracted methods
async processOrder(order: Order) {
  await this.validateOrder(order);
  const totals = this.calculateTotals(order);
  await this.persistOrder(order, totals);
}
```

#### Replace Conditionals with Polymorphism

```typescript
// Before: Type checking
function getPrice(type: string) {
  if (type === 'premium') return 99;
  if (type === 'basic') return 49;
  return 0;
}

// After: Polymorphism
interface PricingStrategy {
  getPrice(): number;
}
class PremiumPricing implements PricingStrategy {
  getPrice() {
    return 99;
  }
}
```

#### Dependency Injection

```typescript
// Before: Hard-coded dependency
class OrderService {
  private db = new Database();
}

// After: Injected dependency
class OrderService {
  constructor(private db: Database) {}
}
```

### Step 5: Validate After Each Change

```bash
# After EVERY change
npm test

# Verify same test count
npm test -- --json | jq '.numTotalTests'

# Verify no failures
npm test -- --json | jq '.numFailedTests' # Must be 0
```

**If tests fail**: Your change altered behavior. Revert immediately.

### Step 6: Document Changes

```markdown
## Refactoring Log

**Related Spec Group** (if applicable): sg-order-processing

### Change 1: Extract validation logic

- **Files**: src/services/order.ts
- **Pattern**: Extract Method
- **Rationale**: 50-line method violated SRP (identified in /code-review)
- **Atomic Specs Affected**: as-001, as-002 (test evidence still valid)
- **Tests**: 147 passing ✓
- **Commit**: abc123

### Change 2: Add dependency injection

- **Files**: src/services/order.ts, src/di/container.ts
- **Pattern**: Dependency Injection
- **Rationale**: Enable testing without real database
- **Atomic Specs Affected**: None (infrastructure change)
- **Tests**: 147 passing ✓
- **Commit**: def456
```

### Step 7: Final Validation

```bash
# Full test suite
npm test

# Type check
npx tsc --noEmit

# Lint (should improve, not regress)
npm run lint

# Build
npm run build

# Coverage (should not decrease)
npm test -- --coverage
```

### Step 8: Completion Report

```markdown
## Refactoring Complete

**Scope**: Tech debt in authentication services
**Related Spec Group** (if applicable): sg-logout-button
**Files Modified**: 4
**Commits**: 6

**Metrics**:
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Tests | 147 | 147 | - |
| Coverage | 84% | 86% | +2% |
| Lint warnings | 12 | 4 | -8 |
| Cyclomatic complexity | 24 | 12 | -50% |

**Changes Made**:

1. Extracted validation logic into AuthValidator class
2. Added dependency injection to AuthService
3. Consolidated error handling patterns
4. Removed dead code (3 unused methods)

**Behavior Changes**: None (all tests pass unchanged)

**Atomic Spec Impact**: None (all Test Evidence in as-001, as-002, as-003 still valid)
```

## Rules

### DO:

- Run tests after every change
- Make atomic, reversible commits
- Document rationale for each change
- Match existing codebase patterns
- Improve metrics (coverage, complexity, lint)

### DON'T:

- Modify tests (usually)
- Change public API signatures
- Add new features
- Fix bugs (that's implementation)
- Introduce new patterns

### Test Modification Rules

Tests define correct behavior. You do NOT modify tests unless:

1. **Refactoring test files themselves** (same assertions, better structure)
2. **Test explicitly tests implementation detail** (document and flag for review)

If tests fail after your change:

- Your refactoring changed behavior → **Revert**
- Test was wrong → **Flag for separate review** (don't modify during refactor)

## Handling Edge Cases

### Insufficient Test Coverage

```markdown
## Blocked: Insufficient Test Coverage

Target: src/services/legacy-auth.ts
Current coverage: 34%
Required: 80%

**Cannot safely refactor without tests.**

Recommendation: Add tests first (separate task)
```

### Test Failures After Change

```markdown
## Refactoring Reverted

Change: Extracted validation into separate method
Result: 3 tests failed
Analysis: Tests were asserting on internal method call order

**Recommendation**: Tests need updating to test behavior, not implementation.
This requires explicit approval before proceeding.
```

### Coverage Decrease

```markdown
## Blocked: Coverage Decreased

Before: 84%
After: 79%

Analysis: Removed dead code that had tests covering unreachable paths

**Options**:

1. Remove obsolete tests (requires approval)
2. Keep dead code (defeats purpose)

Recommendation: Option 1 with careful review
```

## Integration with Other Skills

**Before refactoring**:

- Ensure sufficient test coverage exists
- If not, use `/test` to add coverage first

**After refactoring**:

- Use `/code-review` to validate quality improvements
- Use `/security` if changes touch security-sensitive code

**Spec group context** (when applicable):

- If refactoring code from a recent spec group:
  - Note the spec group ID in refactoring log for traceability
  - Verify atomic spec test evidence still passes after refactoring
  - Do NOT update atomic specs (refactoring doesn't change behavior)

Refactoring is typically standalone - not part of feature workflow. However, it may follow a spec group when code review identifies quality improvements.

## Constraints

### Behavior Preservation is Non-Negotiable

If you can't prove behavior is preserved (tests pass), don't make the change.

### No Feature Changes

Refactoring is NOT:

- Adding new functionality
- Fixing bugs
- Changing behavior "for the better"

If you find bugs during refactoring:

1. Document them
2. Complete refactoring
3. Report bugs as separate issue

### Scope Discipline

Refactoring scope expands easily. Resist.

```markdown
# Bad (scope creep)

Started: Refactor OrderService
Also did: Fixed bug in PaymentService
Also did: Updated logging format

# Good (bounded)

Scope: Extract validation logic from OrderService
Done: Extract validation logic from OrderService
Out of scope: Similar issues in PaymentService (logged for future)
```

## Examples

### Example 1: Extract Method

**Before**:

```typescript
async processOrder(order: Order) {
  // 20 lines of validation
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ... more validation

  // 15 lines of calculation
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  // ... more calculation

  // 15 lines of persistence
  await this.db.save(order);
  // ... more persistence
}
```

**After**:

```typescript
async processOrder(order: Order) {
  this.validateOrder(order);
  const total = this.calculateTotal(order);
  await this.persistOrder(order, total);
}

private validateOrder(order: Order) { /* extracted */ }
private calculateTotal(order: Order) { /* extracted */ }
private async persistOrder(order: Order, total: number) { /* extracted */ }
```

**Validation**: All 12 order tests still pass ✓

### Example 2: Blocked by Coverage

**Request**: Refactor legacy payment service

**Analysis**:

```bash
npm test -- --coverage --collectCoverageFrom="src/services/payment.ts"
# Coverage: 23%
```

**Response**:

```markdown
## Blocked: Insufficient Coverage

Cannot safely refactor src/services/payment.ts with 23% coverage.

**Recommendation**:

1. Create separate task to add tests
2. Achieve >80% coverage
3. Then proceed with refactoring

This protects against accidentally changing behavior.
```
