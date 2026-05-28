# Complexity Thresholds

Thresholds for cyclomatic and cognitive complexity metrics used to identify technical debt.

## Cyclomatic Complexity

Number of linearly independent paths through code. Higher values indicate more complex control flow.

### Function-Level Thresholds

| Range | Level | Score | Action |
|-------|-------|-------|--------|
| 1-10 | Simple | 0 | None required |
| 11-20 | Moderate | 25 | Consider refactoring |
| 21-50 | Complex | 50 | Refactoring recommended |
| 51-100 | Very Complex | 75 | Refactoring required |
| 101+ | Unmaintainable | 100 | Critical - immediate refactoring |

### File-Level Thresholds

| Range | Level | Score |
|-------|-------|-------|
| 1-50 | Simple | 0 |
| 51-100 | Moderate | 25 |
| 101-200 | Complex | 50 |
| 201-500 | Very Complex | 75 |
| 501+ | Unmaintainable | 100 |

## Cognitive Complexity

Measure of how difficult code is to understand, accounting for nested structures and breaks in linear flow.

### Function-Level Thresholds

| Range | Level | Score |
|-------|-------|-------|
| 0-5 | Simple | 0 |
| 6-10 | Moderate | 25 |
| 11-15 | Complex | 50 |
| 16-25 | Very Complex | 75 |
| 26+ | Unmaintainable | 100 |

## Nesting Depth

Maximum nesting level of control structures (if, for, while, try, etc.).

| Depth | Level | Score |
|-------|-------|-------|
| ≤3 | Acceptable | 0 |
| 4 | Warning | 25 |
| 5 | High | 50 |
| 6 | Very High | 75 |
| 7+ | Critical | 100 |

## Parameter Count

Number of parameters in function signature. Too many parameters indicate potential design issues.

| Count | Level | Score |
|-------|-------|-------|
| ≤4 | Acceptable | 0 |
| 5 | Warning | 20 |
| 6-7 | High | 50 |
| 8+ | Critical | 80 |

## Language-Specific Thresholds

### JavaScript

| Metric | Warning | Critical |
|--------|---------|----------|
| Callback Depth | 3 | 5 |
| Promise Chain Length | 4 | 6 |

### Python

| Metric | Warning | Critical |
|--------|---------|----------|
| Class Method Count | 20 | 30 |
| Inheritance Depth | 3 | 5 |

### Java

| Metric | Warning | Critical |
|--------|---------|----------|
| Class Method Count | 25 | 40 |
| Inheritance Depth | 4 | 6 |

## Remediation Strategies

### High Cyclomatic Complexity

1. Extract methods/functions for distinct logical blocks
2. Replace complex conditionals with polymorphism
3. Use guard clauses to reduce nesting
4. Apply strategy pattern for branching logic

### High Cognitive Complexity

1. Simplify boolean expressions
2. Replace nested conditions with early returns
3. Extract helper functions with descriptive names
4. Break down long methods into smaller pieces

### Deep Nesting

1. Use guard clauses and early returns
2. Extract nested logic into separate functions
3. Consider using flat data structures
4. Apply the "fail fast" pattern
