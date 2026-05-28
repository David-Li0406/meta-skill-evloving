---
name: critical-code-review
description: Use this skill when you need to perform a thorough analysis of code for correctness, edge cases, security, performance, and design issues, independent of any baseline comparisons.
---

# Critical Code Review

## Purpose

Perform a deep, thorough, excruciating review of code. This skill is about analyzing code quality, correctness, and design—NOT about running tests or comparing to baseline. Use it anytime you need to scrutinize code.

## API Detection

**Before starting review, check if project contains APIs:**

```yaml
api_indicators:
  - OpenAPI/Swagger spec (openapi.yaml, swagger.json, openapi.json)
  - API framework patterns (FastAPI, Flask, Express, ASP.NET controllers)
  - Route decorators (@app.route, @router.get, [HttpGet], etc.)
  - API test files (test_api_*, *_api_test.*, api.spec.*)
```

**If API detected:**
1. Note in review scope: "API endpoints detected"
2. After general review, invoke `agent-ops-api-review` for API-specific audit
3. Merge API review findings into final report

## When to Use

- **During planning**: Review existing code before modifying
- **During implementation**: Review your own changes
- **Before completion**: Final quality check
- **On demand**: User requests a code review
- **After recovery**: Verify recovery didn't introduce issues

## Review Dimensions

### 1) Correctness

**Logic Analysis**:
- Does the code do what it claims to do?
- Are all code paths reachable and correct?
- Are conditionals exhaustive (all cases handled)?
- Are loop invariants maintained?
- Are recursive functions guaranteed to terminate?

**Boundary Conditions**:
- Empty inputs (null, undefined, empty string, empty array)
- Single element cases
- Maximum values / overflow potential
- Off-by-one errors
- Unicode / special characters

**State Management**:
- Is state modified predictably?
- Are there race conditions?
- Is cleanup always performed (finally blocks, defer, etc.)?

### 2) Error Handling

**Questions to Ask**:
- What can fail here?
- Is every failure case handled?
- Are errors propagated appropriately?
- Are error messages informative?
- Is there silent failure hiding bugs?

**Checklist**:
- [ ] All external calls wrapped in try/catch or equivalent
- [ ] Errors logged with context
- [ ] User-facing errors are actionable
- [ ] No swallowed errors