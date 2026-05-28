# Testing Patterns for Bug Reproducers

## General Test Structure

```typescript
import { describe, it, expect } from 'vitest';

describe('Component or Function', () => {
  it('should handle expected case (fixes #123)', () => {
    // Arrange: setup inputs
    const input = { /* test data */ };

    // Act: trigger the bug
    const result = functionUnderTest(input);

    // Assert: verify expected behavior
    expect(result).toEqual({ /* expected output */ });
  });
});
```

## Vitest CLI

```bash
npm run test              # Run all tests in watch mode
npm run test:ui           # Run tests with interactive UI
npm run test:run          # Run tests once (CI mode)
npm run test:configs      # Run only config test vectors
```

## Config Test Failures

For config-related bugs, create test vector in `configs/<country>/<year>/tests/`:

```json
{
  "name": "Test case name (fixes #123)",
  "inputs": {
    "gross_annual": 50000,
    "filing_status": "single"
  },
  "expected": {
    "net": 38746,
    "effective_rate": 0.22508,
    "breakdown": {
      "income_tax": 12345,
      "general_credit": -3068
    }
  },
  "tolerance": 10,
  "tolerance_percent": 0.005
}
```

Then run: `npm run test:configs`

## Debugging Test Failures

Add console logging in the code being tested:

```typescript
// In source file
console.log('Input:', input);
console.log('Intermediate value:', intermediate);
console.log('Output:', result);

// In test file - can check output
const { log } = console;
const logs = [];
console.log = (msg) => logs.push(msg);
// ... run test ...
console.log = log;
```

Or check test output directly:
```bash
npm run test:run -- --reporter=verbose
```

## Common Bug Patterns

### Off-by-one errors
```typescript
it('should include all items (fixes #123)', () => {
  const items = [1, 2, 3, 4, 5];
  const result = getFirstN(items, 2);
  expect(result).toEqual([1, 2]); // Often bugs give [1] or [1,2,3]
});
```

### Missing null/undefined checks
```typescript
it('should handle undefined input gracefully (fixes #123)', () => {
  expect(() => processData(undefined)).not.toThrow();
  expect(processData(undefined)).toEqual(defaultValue);
});
```

### Type mismatches
```typescript
it('should convert string to number correctly (fixes #123)', () => {
  const result = calculateTax("50000");
  expect(typeof result).toBe('number');
  expect(result).toBeCloseTo(12345, 0);
});
```

### Logic inversions
```typescript
it('should apply tax when income exceeds threshold (fixes #123)', () => {
  const belowThreshold = calculateTax(5000); // threshold is 10000
  const aboveThreshold = calculateTax(15000);
  expect(belowThreshold).toBe(0);
  expect(aboveThreshold).toBeGreaterThan(0);
});
```

### Rounding errors
```typescript
it('should round correctly (fixes #123)', () => {
  const result = calculateNetSalary(60000.01);
  expect(result).toBeCloseTo(expectedValue, 2); // Allow 2 decimal places
});
```
