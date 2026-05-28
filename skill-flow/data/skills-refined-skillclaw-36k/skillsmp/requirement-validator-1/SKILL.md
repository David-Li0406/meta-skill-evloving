---
name: requirement-validator
description: Validate pseudo-code completeness and identify gaps
allowed-tools: Read, Grep
model: sonnet
---

# Requirement Validator

Check pseudo-code for completeness and identify missing requirements.

## WHAT THIS DOES

Analyzes pseudo-code and generates a validation report with:

- ✓ PASSED CHECKS (what's good)
- ⚠ WARNINGS (nice-to-have improvements)
- ✗ CRITICAL ISSUES (must-fix problems)
- 📋 EDGE CASES (scenarios to consider)

## VALIDATION CHECKLIST

### Check 1: Required Parameters

Are core parameters present?

```text
✓ PASS: Function name descriptive, type specified, core params present
✗ FAIL: Missing required parameter: [name]
```

### Check 2: Security Requirements

Is authentication/authorization specified?

```text
✓ PASS: Auth type specified, permissions defined
✗ FAIL: Security not addressed (auth/permissions missing)
⚠ WARN: Auth mentioned but flow undefined
```

### Check 3: Error Handling

Are error scenarios covered?

```text
✓ PASS: Error handling strategy defined
✗ FAIL: No error handling specified
⚠ WARN: Only happy path covered, error cases missing
```

### Check 4: Validation Rules

Are inputs validated?

```text
✓ PASS: Input validation rules specified
✗ FAIL: User input not validated
⚠ WARN: Validation incomplete (missing [field])
```

### Check 5: Edge Cases

Are boundary conditions addressed?

```text
✓ PASS: Edge cases considered (null, empty, overflow)
⚠ WARN: Edge case not addressed: [scenario]
```

## OUTPUT FORMAT

```text
═══════════════════════════════════════
Validation Report
═══════════════════════════════════════

✓ PASSED CHECKS
- [Check 1 passed]
- [Check 2 passed]
- [Check 3 passed]

⚠ WARNINGS (Medium Priority)
- [Warning 1: what's missing]
- [Warning 2: what could be better]

✗ CRITICAL ISSUES (Must Fix)
- [Critical 1: what's broken]
- [Critical 2: what's missing]

📋 EDGE CASES TO CONSIDER
- [Edge case 1: scenario not covered]
- [Edge case 2: boundary condition]

## Summary

Passed: [N] | Warnings: [N] | Critical: [N] | Edge Cases: [N]

Overall: [READY FOR IMPLEMENTATION | NEEDS FIXES | MAJOR GAPS]
```

## EXAMPLE

### Input

```text
build_api(
  type="rest",
  endpoints=["/users", "/tasks"]
)
```

### Output

```text
═══════════════════════════════════════
Validation Report
═══════════════════════════════════════

✓ PASSED CHECKS
- Function name is descriptive and clear
- API type is specified (REST)
- Core endpoints are defined

⚠ WARNINGS (Medium Priority)
- HTTP methods not specified for endpoints (assume CRUD?)
- No rate limiting mentioned (recommend adding)
- No pagination strategy for list endpoints

✗ CRITICAL ISSUES (Must Fix)
- Authentication/authorization not specified
- Error handling strategy not defined
- Input validation rules missing
- Database choice not specified

📋 EDGE CASES TO CONSIDER
- Concurrent request handling (race conditions)
- Large dataset pagination and performance
- Token expiration and refresh flow
- Partial failure scenarios (one endpoint fails)
- API versioning strategy

## Summary

Passed: 3 | Warnings: 3 | Critical: 4 | Edge Cases: 5

Overall: MAJOR GAPS - Critical issues must be addressed before implementation
```

## SEVERITY LEVELS

| Level | Description | Action Required |
| --- | --- | --- |
| ✓ PASSED | Requirement met | None |
| ⚠ WARNING | Nice to have | Recommended |
| ✗ CRITICAL | Must address | Required |
| 📋 EDGE CASE | Consider scenario | Evaluate |

## QUICK RULES

1. **Always check** security (auth/permissions)
2. **Always check** error handling
3. **Always check** validation rules
4. **Flag as critical** if missing security or errors
5. **Flag as warning** if incomplete but present
6. **List edge cases** for complex scenarios

## VERSION

**2.0.0** - Simplified (295 → 170 lines)
