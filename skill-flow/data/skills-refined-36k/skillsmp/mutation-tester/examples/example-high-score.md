# Example: High Mutation Score (Passing)

## Scenario
Running mutation testing on a well-tested authentication module.

## Mutation Testing Output

```bash
$ npx stryker run --mutate "src/utils/auth.ts"

Stryker 7.0.0 - Your test quality gauge

Running initial test run...
All tests passed!

Creating mutants...
Created 24 mutants in src/utils/auth.ts

Running mutation testing...
████████████████████████ 100% | 24/24 mutants tested

Mutation Score: 87.5%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Mutant Type        | Killed | Survived | Score |
|--------------------|--------|----------|-------|
| ArithmeticOperator | 3      | 0        | 100%  |
| BooleanLiteral     | 4      | 1        | 80%   |
| ConditionalExpr    | 6      | 0        | 100%  |
| StringLiteral      | 5      | 1        | 83%   |
| ArrayDeclaration   | 3      | 1        | 75%   |

Killed: 21 | Survived: 3 | Timeout: 0 | No Coverage: 0
```

## Analysis

```
┌─────────────────────────────────────────────────────────────┐
│ Mutation Testing Results                                    │
│                                                             │
│   File: src/utils/auth.ts                                   │
│   Score: 87.5% ✅ (threshold: 80% for auth)                 │
│                                                             │
│   Killed mutants: 21                                        │
│   Survived mutants: 3                                       │
│                                                             │
│   Quality assessment: EXCELLENT                             │
│   Tests are catching bugs effectively.                      │
└─────────────────────────────────────────────────────────────┘
```

## Surviving Mutants (for reference)

```
Surviving mutant 1:
  src/utils/auth.ts:15:12
  Changed: if (isValid) → if (false)
  Reason: Edge case not covered

Surviving mutant 2:
  src/utils/auth.ts:28:5
  Changed: "token expired" → ""
  Reason: Error message not asserted

Surviving mutant 3:
  src/utils/auth.ts:42:8
  Changed: roles = [] → roles = ["admin"]
  Reason: Empty array case not tested
```

## Decision

Since score (87.5%) >= threshold (80% for auth):
- **PASS** - Continue to next phase
- Optional: Add tests for surviving mutants in future iteration
