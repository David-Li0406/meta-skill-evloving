# Output Format Standards

All delegate outputs should follow these markdown formats for consistent parsing and readability.

## Standard Response Format

```
## Summary
one-line conclusion

## Confidence
high|medium|low

## Findings
- path/to/file.ts:42 - description (severity: critical|high|medium|low)
- path/to/other.ts:10 - another issue (severity: medium)

## Suggested Actions
1. [edit] path/to/file.ts - what to change
2. [create] path/to/new.ts - what to create
3. [run] npm test - verification command
```

## Analysis Response

For `sage` and analytical tasks:

```
## Summary
one-line conclusion

## Confidence
high|medium|low

## Problem
problem description

## Root Cause
identified cause

## Impact
affected areas and scope

## Trade-offs

### Option A
- Pros: benefit 1, benefit 2
- Cons: drawback 1, drawback 2

### Option B
- Pros: benefit 1, benefit 2
- Cons: drawback 1, drawback 2

## Recommendation
recommended approach

## Reasoning
step-by-step reasoning for the recommendation
```

## Search Response

For `pathfinder` and `scout` tasks:

```
## Summary
what was found

## Confidence
high|medium|low

## Results
- path/to/file.ts:10-25 (relevance: high)
  code or text excerpt
  why this is relevant

- path/to/other.ts:50 (relevance: medium)
  another excerpt
  relevance note

## Patterns
- identified pattern 1
- identified pattern 2

## Next Steps
- suggested follow-up search 1
- suggested follow-up search 2
```

## Patch Response

For edit suggestions:

```
## Summary
what changes are proposed

## Confidence
high|medium|low

## Patches

### path/to/file.ts

#### Lines 10-12
Before:
original line 1
original line 2

After:
new line 1
new line 2

Reason: what this change does

### path/to/other.ts

#### Lines 5-7
Before:
old code

After:
new code

Reason: explanation

## Verification
- npm test
- npm run typecheck
Expected: all pass
```

## Checklist Response

For review and validation tasks:

```
## Summary
overall assessment

## Confidence
high|medium|low

## Checklist
- [PASS] check description - explanation
- [FAIL] check description - path/to/file.ts:42 - what failed
- [WARN] check description - potential issue
- [SKIP] check description - why skipped

## Score
Passed: 5
Failed: 1
Warnings: 2
```

## Confidence Levels

| Level | Meaning | When to use |
|-------|---------|-------------|
| high | Strong evidence, clear conclusion | Verified against code/tests |
| medium | Reasonable inference, some uncertainty | Based on patterns, not verified |
| low | Speculation, needs verification | Incomplete context, edge cases |

## Error Response

When delegate cannot complete:

```
## Error
type: timeout|parse_error|insufficient_context|unsupported

## Message
description of failure

## Partial Result
any partial findings if available

## Suggestion
how to recover or retry
```
