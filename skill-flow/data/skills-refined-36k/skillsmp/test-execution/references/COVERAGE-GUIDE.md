# Test Coverage Guide

Understanding and optimizing test coverage.

## Coverage Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Lines** | Percentage of code lines executed | 80%+ |
| **Branches** | Percentage of decision branches taken | 80%+ |
| **Functions** | Percentage of functions called | 90%+ |
| **Statements** | Percentage of statements executed | 80%+ |

## Coverage Report Example

```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   85.71 |    80.00 |   90.00 |   85.71 |
 src/               |   85.71 |    80.00 |   90.00 |   85.71 |
  calculator.ts     |   100   |   100    |   100   |   100   |
  validator.ts      |   71.43 |    60.00 |   80.00 |   71.43 |
--------------------|---------|----------|---------|---------|
```

## Configuration

### Vitest

```javascript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'test/',
        '**/*.d.ts',
        '**/*.config.*'
      ],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 90,
        statements: 80
      }
    }
  }
});
```

### Jest

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'html', 'lcov'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 90,
      lines: 80,
      statements: 80
    }
  },
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{js,ts}'
  ]
};
```

## Running Coverage

```bash
# Vitest
npm run test -- --coverage

# Jest
npm test -- --coverage

# Generate HTML report
npm run test:coverage
```

## Understanding Uncovered Code

### Branch Coverage

```javascript
function getStatus(score) {
  if (score >= 90) {      // Branch 1
    return 'A';
  } else if (score >= 80) {  // Branch 2
    return 'B';
  } else {                // Branch 3 (might be missed)
    return 'C';
  }
}

// Tests needed:
it('should return A for score >= 90', ...);
it('should return B for score 80-89', ...);
it('should return C for score < 80', ...);
```

### Line Coverage

```javascript
function processUser(user) {
  if (!user) {           // Line 1
    return null;         // Line 2 (needs test with null user)
  }

  const name = user.name;  // Line 3
  return name.toUpperCase();  // Line 4
}
```

## Improving Coverage

### Finding Gaps

1. Run coverage report
2. Open HTML report in browser
3. Look for red/yellow highlighted lines
4. Write tests for uncovered paths

### Common Uncovered Areas

| Area | Why Missed | Solution |
|------|-----------|----------|
| Error handlers | Only test happy path | Test error cases |
| Edge cases | Not considered | Add boundary tests |
| Default branches | Obvious cases skipped | Explicit tests |
| Catch blocks | No error simulation | Mock errors |

### Coverage vs Quality

```
High coverage ≠ Good tests

❌ Bad: 100% coverage with no assertions
✅ Good: 80% coverage with meaningful assertions
```

## Excluding Code

### Ignore Comments

```javascript
// Vitest/Jest
/* istanbul ignore next */
function debugOnly() {
  console.log('debug');
}

/* istanbul ignore if */
if (process.env.DEBUG) {
  enableDebugMode();
}
```

### Configuration Exclusions

```javascript
coveragePathIgnorePatterns: [
  '/node_modules/',
  '/test/',
  '/dist/',
  '/__mocks__/'
]
```

## CI Integration

### GitHub Actions

```yaml
- name: Run tests with coverage
  run: npm run test:coverage

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/lcov.info
    fail_ci_if_error: true

- name: Check coverage threshold
  run: |
    COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below threshold"
      exit 1
    fi
```

## Best Practices

1. **Set realistic thresholds** - Start at current level, increase gradually
2. **Don't chase 100%** - Diminishing returns after 80-90%
3. **Focus on critical paths** - Business logic > utility functions
4. **Review coverage in PRs** - Don't let it decrease
5. **Exclude generated code** - Config files, types, mocks
