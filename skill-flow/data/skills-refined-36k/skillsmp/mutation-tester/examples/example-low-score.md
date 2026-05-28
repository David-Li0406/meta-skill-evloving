# Example: Low Mutation Score (Requires More Tests)

## Scenario
Mutation testing reveals weak test coverage.

## Mutation Testing Output

```bash
$ npx stryker run --mutate "src/utils/format.ts"

Mutation Score: 42.0%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Mutant Type        | Killed | Survived | Score |
|--------------------|--------|----------|-------|
| ArithmeticOperator | 2      | 4        | 33%   |
| ConditionalExpr    | 1      | 3        | 25%   |
| StringLiteral      | 3      | 2        | 60%   |

Killed: 6 | Survived: 9 | Timeout: 0 | No Coverage: 2
```

## Analysis

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ Mutation Testing FAILED                                  │
│                                                             │
│   File: src/utils/format.ts                                 │
│   Score: 42.0% ❌ (threshold: 60%)                          │
│                                                             │
│   Killed mutants: 6                                         │
│   Survived mutants: 9                                       │
│   No coverage: 2                                            │
│                                                             │
│   Quality assessment: WEAK                                  │
│   Tests are not catching many potential bugs.               │
└─────────────────────────────────────────────────────────────┘
```

## Surviving Mutants to Fix

```
CRITICAL - These mutants reveal missing tests:

1. src/utils/format.ts:8:5
   Mutation: formatCurrency(100) → formatCurrency(-100)
   Missing test: Negative number formatting

2. src/utils/format.ts:15:12
   Mutation: if (value > 0) → if (value >= 0)
   Missing test: Zero value edge case

3. src/utils/format.ts:22:8
   Mutation: decimal.toFixed(2) → decimal.toFixed(0)
   Missing test: Decimal precision

4. src/utils/format.ts:30:3
   Mutation: return "" → return "0"
   Missing test: Empty input handling
```

## Required Actions

Return to RED phase with new tests:

```typescript
// Add these test cases to format.test.ts

describe('formatCurrency edge cases', () => {
  it('should format negative numbers', () => {
    expect(formatCurrency(-100)).toBe('-$100.00');
  });

  it('should handle zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  it('should preserve decimal precision', () => {
    expect(formatCurrency(99.999)).toBe('$100.00');
  });

  it('should handle empty input', () => {
    expect(formatCurrency(undefined)).toBe('$0.00');
  });
});
```

## Re-run After Adding Tests

```bash
$ npx stryker run --mutate "src/utils/format.ts"

Mutation Score: 78.0% ✅ (improved from 42%)
```

## Decision

After adding edge case tests:
- Score improved to 78% (above 60% threshold)
- **PASS** - Continue to next phase
