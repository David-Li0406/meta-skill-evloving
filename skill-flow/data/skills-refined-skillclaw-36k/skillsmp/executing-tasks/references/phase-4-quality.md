---
title: Phase 4 - Quality Gates
description: Verification commands, error handling patterns, and result recording for task execution quality phase
keywords: quality, verification, testing, errors, validation
file-type: reference
skill: executing-tasks
---

# Phase 4: Quality Gates

## Verification Commands

| Check Type | Command | Pass Criteria |
|------------|---------|---------------|
| Type safety | `npm run typecheck` | Exit code 0 |
| Unit tests | `npm run test` | All tests pass |
| Specific test | `npm run test -- <path>` | Target tests pass |
| Linting | `npm run lint` | No errors (warnings OK) |
| Build | `npm run build` | Successful compilation |

**Execution order:**
1. typecheck (fast, catches type errors)
2. lint (fast, catches style issues)
3. test (slower, catches behavior issues)
4. build (slowest, catches integration issues)

## Error Handling Patterns

| Error Type | Response | Re-execution |
|------------|----------|--------------|
| Type error | Fix type issue | Yes, from Phase 3 |
| Test failure | Fix implementation or test | Yes, from Phase 3 |
| Lint error | Apply autofix or manual fix | Yes, quick loop |
| Build error | Investigate dependency/config | Yes, from Phase 3 |
| Flaky test | Identify flakiness, fix or skip | Document and proceed |

**Error handling flow:**
```
Quality Check Failed
       |
       v
  [Analyze Error]
       |
       +---> Type/Implementation Error --> Fix --> Re-execute Phase 3
       |
       +---> Test Flakiness --> Document --> Proceed with note
       |
       +---> Environment Issue --> Fix config --> Re-execute Phase 4
```

## Recording Results

**Document in task notes:**
- Commands executed with timestamps
- Pass/fail status for each check
- Error messages for failures
- Resolution steps taken

**Quality gate record format:**
```
## Quality Check Results - [timestamp]
- typecheck: PASS
- lint: PASS (3 warnings)
- test: PASS (45 tests)
- build: PASS
```

## Quality Checklist

- [ ] Run typecheck, record result
- [ ] Run lint, record result
- [ ] Run relevant tests, record result
- [ ] Run build if applicable
- [ ] All checks pass OR failures documented with resolution
- [ ] Ready for progress update
