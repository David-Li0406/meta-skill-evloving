# File Size Thresholds

Thresholds for file and function size indicators of technical debt.

## File Lines

Lines of code per file.

| Range | Level | Score | Description |
|-------|-------|-------|-------------|
| 0-200 | Excellent | 0 | Well-sized file |
| 201-500 | Acceptable | 10 | Acceptable size |
| 501-1000 | Warning | 30 | Consider splitting |
| 1001-2000 | High | 60 | Should be split |
| 2001+ | Critical | 100 | God file - urgent refactor |

## Function Lines

Lines of code per function/method.

| Range | Level | Score |
|-------|-------|-------|
| 0-20 | Excellent | 0 |
| 21-50 | Acceptable | 10 |
| 51-100 | Warning | 40 |
| 101-200 | High | 70 |
| 201+ | Critical | 100 |

## Class Lines

Lines of code per class.

| Range | Level | Score |
|-------|-------|-------|
| 0-200 | Excellent | 0 |
| 201-500 | Acceptable | 15 |
| 501-1000 | Warning | 40 |
| 1001+ | Critical | 80 |

## Language Adjustments

Adjust thresholds based on language conventions.

| Language | File Multiplier | Reason |
|----------|-----------------|--------|
| Java | 1.5x | Verbose language |
| Go | 0.8x | Single package files |
| Python | 1.0x | Standard |
| JavaScript | 1.0x | Standard |
| TypeScript | 1.1x | Type annotations |

## Exclude Patterns

Files to exclude from scoring:

- `**/generated/**`
- `**/*.generated.*`
- `**/vendor/**`
- `**/node_modules/**`
- `**/*.min.js`
- `**/*.bundle.js`

## Adjusted Patterns

Files with modified scoring:

| Pattern | Multiplier | Reason |
|---------|------------|--------|
| `**/migrations/**` | 0.5x | DB migrations often long |
| `**/*.test.*` | 0.7x | Tests can be verbose |
| `**/types/**` | 0.5x | Type definitions |

## Remediation Strategies

### Large Files

1. Identify logical groupings within the file
2. Extract related functions to separate modules
3. Use barrel files to maintain clean imports
4. Ensure tests cover extracted code

### Long Functions

1. Extract helper functions for discrete operations
2. Apply single responsibility principle
3. Use early returns to reduce nesting
4. Add meaningful names for extracted functions

### Large Classes

1. Identify multiple responsibilities
2. Extract secondary concerns to separate classes
3. Use composition over inheritance
4. Consider the facade pattern for complex interfaces
