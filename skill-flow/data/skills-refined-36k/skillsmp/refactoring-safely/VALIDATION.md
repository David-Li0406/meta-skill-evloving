# Validation and Rollback

Ensuring refactors don't break functionality and recovering when they do.

## Test Coverage Before Refactoring

### Assessing Coverage

```bash
# Generate coverage report
bun test --coverage

# Check specific file coverage
bun test --coverage src/module-to-refactor.ts
```

### Coverage Thresholds

| Code Type | Minimum Before Refactoring |
|-----------|---------------------------|
| Critical business logic | 90%+ |
| API endpoints | 85%+ |
| Data transformations | 80%+ |
| Utility functions | 75%+ |
| UI components | 60%+ |

### Adding Missing Tests

Before refactoring code with low coverage:

```typescript
// 1. Write characterization tests - capture current behavior
describe('currentBehavior', () => {
  test('returns X when given Y', () => {
    // Document what it does NOW, not what it SHOULD do
    expect(functionToRefactor(input)).toMatchSnapshot();
  });

  test('handles edge case Z', () => {
    // Even if behavior seems wrong, capture it
    expect(functionToRefactor(edgeCase)).toBe(unexpectedResult);
  });
});

// 2. Only AFTER tests exist, do refactoring
// 3. Fix bugs in SEPARATE commits after refactoring
```

## Validation Strategies

### 1. Type Checking

```bash
# Run type checker
bun run typecheck

# Or directly
bunx tsc --noEmit
```

Type errors after refactoring indicate:
- Missing imports
- Changed interfaces
- Incompatible types

### 2. Test Suite

```bash
# Full test run
bun test

# Watch mode during refactoring
bun test --watch

# Specific files
bun test src/refactored-module.test.ts
```

### 3. Linting

```bash
# Check for issues
bun run lint

# Auto-fix what's possible
bun run lint:fix
```

### 4. Manual Smoke Testing

After automated tests pass:

- [ ] Start the application
- [ ] Test primary user flows
- [ ] Check for console errors
- [ ] Verify API responses (if applicable)

### 5. Comparison Testing

For critical functions, compare old and new behavior:

```typescript
import { oldImplementation } from './old';
import { newImplementation } from './new';

describe('behavior comparison', () => {
  const testCases = [
    { input: 'case1', description: 'normal case' },
    { input: 'case2', description: 'edge case' },
    // ... many test cases
  ];

  for (const { input, description } of testCases) {
    test(`same behavior: ${description}`, () => {
      const oldResult = oldImplementation(input);
      const newResult = newImplementation(input);
      expect(newResult).toEqual(oldResult);
    });
  }
});
```

## Validation Workflow

### Pre-Refactor Validation

```bash
# 1. Ensure clean state
git status  # Should be clean

# 2. Run all checks
bun run typecheck && bun test && bun run lint

# 3. Create baseline commit
git commit -m "chore: checkpoint before refactoring"

# 4. Note the commit hash
git log -1 --format=%H  # Save this for rollback
```

### During Refactoring

```bash
# After each change
bun test  # Quick feedback

# Periodically
bun run typecheck  # Catch type issues

# Commit frequently
git commit -m "refactor: extract validation logic"
```

### Post-Refactor Validation

```bash
# 1. Full validation suite
bun run typecheck && bun test && bun run lint

# 2. Check for regressions
bun test --coverage  # Coverage shouldn't decrease

# 3. Manual smoke test
bun run dev  # Start app, test key flows

# 4. Review changes
git diff main  # Or diff against baseline
```

## Rollback Strategies

### Strategy 1: Git Reset (Uncommitted Changes)

```bash
# Discard all changes
git checkout -- .

# Or reset specific file
git checkout -- src/broken-file.ts
```

### Strategy 2: Git Revert (Committed Changes)

```bash
# Revert last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Revert range of commits
git revert <older-commit>..<newer-commit>
```

### Strategy 3: Git Reset (Committed, Not Pushed)

```bash
# Reset to previous commit, keep changes staged
git reset --soft HEAD~1

# Reset to previous commit, keep changes unstaged
git reset HEAD~1

# Reset to previous commit, discard changes
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard <baseline-commit-hash>
```

### Strategy 4: Branch Abandonment

```bash
# If on feature branch, just abandon it
git checkout main
git branch -D refactor/failed-attempt

# Start fresh
git checkout -b refactor/second-attempt
```

### Strategy 5: Partial Rollback

```bash
# Revert only specific files
git checkout <baseline-commit> -- src/specific-file.ts

# Keep other changes
git add src/specific-file.ts
git commit -m "revert: restore specific-file.ts"
```

## Recovery Checklist

When refactoring goes wrong:

### Immediate Actions

- [ ] Stop making changes
- [ ] Don't panic - git has your history
- [ ] Run `git status` to understand state
- [ ] Run `git log --oneline -10` to see recent commits

### Assessment

- [ ] Are tests failing?
- [ ] Is there a type error?
- [ ] Is it a runtime error?
- [ ] How many commits since last working state?

### Decision Tree

```
Tests failing?
├── Yes
│   ├── Can fix quickly (< 10 min)?
│   │   ├── Yes → Fix and continue
│   │   └── No → Rollback
│   └── Multiple failures?
│       ├── Yes → Rollback to last green commit
│       └── No → Debug the single failure
└── No
    └── Runtime error only?
        ├── Yes → Debug or rollback
        └── No → Continue refactoring
```

## Preventing Rollback Situations

### Commit Often

```bash
# After every successful change
git add -A && git commit -m "refactor: description"

# Small commits are easy to revert
git revert HEAD  # Revert just one small change
```

### Use Feature Flags

```typescript
const USE_NEW_IMPLEMENTATION = false;

function criticalFunction() {
  if (USE_NEW_IMPLEMENTATION) {
    return newImplementation();
  }
  return oldImplementation();
}

// Later, flip the flag after testing
// If issues, flip back instantly
```

### Parallel Testing

Run new implementation alongside old:

```typescript
function processData(input: Data) {
  const oldResult = oldImplementation(input);
  const newResult = newImplementation(input);

  if (JSON.stringify(oldResult) !== JSON.stringify(newResult)) {
    console.error('Implementation mismatch', { oldResult, newResult });
  }

  return oldResult; // Still use old until confident
}
```

### Incremental Rollout

```typescript
function processRequest(req: Request) {
  // Gradually increase percentage
  const useNew = Math.random() < 0.1; // 10% new implementation

  if (useNew) {
    return newHandler(req);
  }
  return oldHandler(req);
}
```

## Test-Specific Validation

### Snapshot Testing

```typescript
// Capture current behavior
test('output format', () => {
  const result = refactoredFunction(standardInput);
  expect(result).toMatchSnapshot();
});

// After refactoring, if snapshot changes unexpectedly:
// bun test -- -u  # Update snapshots (only if change is intentional)
```

### Golden File Testing

```typescript
import { readFileSync } from 'fs';

test('complex output matches golden file', () => {
  const result = generateReport(testData);
  const expected = readFileSync('test/golden/report.txt', 'utf8');
  expect(result).toBe(expected);
});
```

### Property-Based Testing

```typescript
import { fc } from '@fast-check/vitest';

test('refactored function maintains invariants', () => {
  fc.assert(
    fc.property(fc.string(), fc.integer(), (str, num) => {
      const result = refactoredFunction(str, num);

      // Properties that should always be true
      expect(result.length).toBeGreaterThanOrEqual(0);
      expect(typeof result).toBe('string');
    })
  );
});
```

## Documentation Updates

After successful refactoring:

- [ ] Update JSDoc comments
- [ ] Update README if API changed
- [ ] Update CHANGELOG
- [ ] Update architecture docs if structure changed
- [ ] Remove obsolete documentation

```typescript
/**
 * Processes user data with validation.
 *
 * @param data - Raw user input
 * @returns Validated and transformed user data
 *
 * @example
 * const user = processUserData({ name: 'Alice', email: 'alice@example.com' });
 *
 * @since 2.0.0 - Refactored to use new validation pipeline
 * @see ValidationPipeline
 */
export function processUserData(data: UserInput): ValidatedUser {
  // ...
}
```
