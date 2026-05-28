# Report Template

Use this template to document test coverage evaluation and implementation results.

---

```markdown
## Test Coverage Report: [filename]

TARGET FILE: `[path]`
FILE TYPE: [Component/Service/Utility/Hook/Page]
RISK LEVEL: [High/Medium/Low]
DATE: [date]

---

## PART 1: EVALUATION PHASE

### Risk Assessment

**Complexity Score**: [Low/Medium/High]
- Lines of code: [number]
- Dependencies: [number] external dependencies
- User interactions: [number]
- Business logic complexity: [assessment]

**Required Test Levels** (based on Risk Matrix):
- [x/o] Unit Tests
- [x/o/N/A] Integration Tests
- [x/o/N/A] E2E Tests

### Test Discovery

| Level | Status | Location | Test Count | Notes |
|-------|--------|----------|------------|-------|
| Unit | [found/warning/missing] | [path or "Missing"] | [N tests] | [notes] |
| Integration | [found/warning/missing/N/A] | [path or "Missing"] | [N tests] | [notes] |
| E2E | [found/warning/missing/N/A] | [path or "Missing"] | [N tests] | [notes] |

**Test Pyramid Health**: [Good/Needs Improvement/Poor]

### Pattern Compliance Check

#### Unit Tests
[If unit tests exist]

**Strengths**:
- [Specific good practices observed]
- [Reference to pattern doc section]

**Violations**:
- [Pattern violation] (See: testing-patterns.md Pattern #N)
  ```typescript
  // Current (WRONG):
  [code snippet]

  // Should be:
  [corrected code snippet]
  ```

**Warnings**:
- [Minor issues that should be addressed]

#### E2E Tests
[If E2E tests exist]

**Strengths**:
- [Good practices observed]

**Critical Violations**:
- [Specific violation] (See: playwright-best-practices.md Pattern #N)
  - Location: [file:line]
  - Impact: [Why this matters]
  - Fix Required: [What needs to change]

### Gap Analysis

#### Critical Gaps (P0)
**[Gap Description]**
- **Impact**: [Why this matters]
- **Required Test**: [What needs to be created]
- **Pattern Reference**: [Link to pattern doc]

#### Important Gaps (P1)
**[Gap Description]**
- **Impact**: [Why this matters]
- **Recommended Test**: [What should be created]

---

## PART 2: IMPLEMENTATION PHASE

### Actions Taken

**Pattern Violations Fixed**:
- [x] Fixed [violation description] at [file:line]
- [x] Updated [test name] to follow [pattern doc]

**Tests Created**:
- [x] Created [test file path]
  - [N] P0 critical tests
  - [N] P1 important tests
  - [N] P2 edge case tests

**Tests Updated**:
- [x] Enhanced [existing test file]
  - Added [N] missing test cases
  - Fixed [N] pattern violations
  - Improved [N] shallow assertions

### Test Coverage Achieved

#### What's Now Tested
- [x] Main user flow (P0) - [N tests]
- [x] Form validation (P0) - [N tests]
- [x] Error handling (P1) - [N tests]
- [x] Edge cases (P2) - [N tests]

#### Test Statistics
**Unit Tests**: [N] test cases
- P0 Critical: [N] tests
  - [test description 1]
  - [test description 2]
- P1 Important: [N] tests
- P2 Edge Cases: [N] tests

**Integration Tests**: [N] test cases (if applicable)
**E2E Tests**: [N] test cases (if applicable)

**TOTAL**: [N] test cases across all levels

### Validation Results
```
All [N] tests passing
Test suite completed in [X]ms
No pattern violations detected
```

---

## SUMMARY

**[N] strengths** | **[N] warnings** | **[N] critical gaps fixed**

**Overall Assessment**: [Excellent/Good/Acceptable/Needs Follow-Up]

### Still Outstanding (if any)

- [ ] [Remaining gap] - [Priority] - [Reason not addressed]

### Recommendations

1. **[Highest Priority]**: [Specific action]
   - Files: [paths]
   - Pattern Reference: [doc]
   - Effort: [Low/Medium/High]

2. **[Next Priority]**: [Specific action]

### Pattern Documentation References

Patterns followed in this implementation:
- testing-patterns.md (React component testing)
- vitest-testing-patterns.md (Service/utility testing)
- playwright-best-practices.md (E2E testing)
- [Any other relevant patterns]

---

## End of Report
```
