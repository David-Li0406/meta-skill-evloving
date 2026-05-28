# Code Review Templates

## Full Review Template

```markdown
# Code Review: [PR Title / Module Name]

**Reviewer:** Claude
**Date:** YYYY-MM-DD
**Files Reviewed:** X files
**Lines Changed:** +X / -X

---

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Architecture | :white_check_mark: / :warning: / :x: | X |
| Code Quality | :white_check_mark: / :warning: / :x: | X |
| Security | :white_check_mark: / :warning: / :x: | X |
| Performance | :white_check_mark: / :warning: / :x: | X |
| Testing | :white_check_mark: / :warning: / :x: | X |

**Overall:** :white_check_mark: Approve / :warning: Approve with Comments / :x: Request Changes

---

## Critical Issues :x:

> Issues that must be fixed before merging

### 1. [Issue Title]
**File:** `path/to/file.py:123`
**Severity:** Critical

**Problem:**
```python
# Current code
vulnerable_code_here
```

**Impact:** [Describe security/stability impact]

**Suggested Fix:**
```python
# Recommended fix
safe_code_here
```

---

## Major Issues :warning:

> Issues that should be addressed

### 1. [Issue Title]
**File:** `path/to/file.py:456`
**Severity:** Major

**Problem:** [Description]

**Suggestion:** [How to fix]

---

## Minor Issues :bulb:

> Code quality improvements

1. **[file.py:78]** Consider using `enumerate()` instead of manual index tracking
2. **[file.py:92]** Variable `x` could have a more descriptive name
3. **[file.py:145]** This function is 45 lines; consider splitting

---

## Suggestions :thought_balloon:

> Optional improvements for future consideration

1. Consider adding caching for frequently accessed data
2. This module might benefit from async batch processing
3. Adding metrics here would help with observability

---

## Positive Highlights :star:

> Good practices worth noting

1. Excellent use of Value Objects for domain validation
2. Clean separation of concerns in the use case
3. Comprehensive error handling with proper context preservation
4. Good test coverage for edge cases

---

## Files Reviewed

| File | Status | Notes |
|------|--------|-------|
| `domain/entities/user.py` | :white_check_mark: | Clean entity design |
| `application/commands/create_user.py` | :warning: | Missing transaction handling |
| `infrastructure/adapters/user_repo.py` | :white_check_mark: | Good mapping implementation |

---

## Checklist

### Architecture
- [x] Dependencies point inward
- [x] Ports defined correctly
- [ ] No business logic in controllers
- [x] DTOs used for API responses

### Code Quality
- [x] Type hints present
- [x] Functions are focused
- [ ] No code duplication
- [x] Clear naming

### Security
- [x] No hardcoded secrets
- [x] Input validation present
- [x] Auth checks in place
- [x] Sensitive data not logged

### Testing
- [ ] Unit tests added
- [ ] Edge cases covered
- [x] Existing tests pass
```

---

## Quick Review Template

For smaller changes or quick reviews:

```markdown
## Quick Review: [PR Title]

**Status:** :white_check_mark: Approve / :warning: Minor changes / :x: Needs work

### Summary
[1-2 sentence summary]

### Issues Found
- :x: **Critical:** None
- :warning: **Major:** [List or None]
- :bulb: **Minor:** [List or None]

### Quick Feedback
[Specific comments on the code]
```

---

## Architecture Review Template

For architecture-focused reviews:

```markdown
## Architecture Review: [Module/Feature Name]

### Layer Compliance

| Layer | Compliance | Issues |
|-------|-----------|--------|
| Domain | :white_check_mark: / :x: | |
| Application | :white_check_mark: / :x: | |
| Infrastructure | :white_check_mark: / :x: | |
| Presentation | :white_check_mark: / :x: | |

### Dependency Analysis

```
[Diagram or description of dependencies]
```

### Port/Adapter Mapping

| Port | Adapter | Status |
|------|---------|--------|
| `UserRepository` | `PostgresUserRepository` | :white_check_mark: |

### CQRS Compliance

| Use Case | Type | Correct | Notes |
|----------|------|---------|-------|
| CreateUser | Command | :white_check_mark: | |
| ListUsers | Query | :white_check_mark: | |

### Recommendations
1. ...
```

---

## Security Review Template

```markdown
## Security Review: [Module/Feature Name]

### OWASP Top 10 Check

| Vulnerability | Status | Notes |
|--------------|--------|-------|
| Injection | :white_check_mark: / :x: | |
| Broken Auth | :white_check_mark: / :x: | |
| Sensitive Data | :white_check_mark: / :x: | |
| XXE | :white_check_mark: / :x: | N/A |
| Access Control | :white_check_mark: / :x: | |
| Misconfiguration | :white_check_mark: / :x: | |
| XSS | :white_check_mark: / :x: | N/A |
| Deserialization | :white_check_mark: / :x: | |
| Components | :white_check_mark: / :x: | |
| Logging | :white_check_mark: / :x: | |

### Critical Findings
[List or "None found"]

### Recommendations
1. ...
```

---

## PR Comment Templates

### Requesting Changes

```markdown
:x: **Changes Requested**

This PR has issues that need to be addressed before merging:

1. **[Critical]** [Issue description]
2. **[Major]** [Issue description]

Please fix these issues and request another review.
```

### Approving with Comments

```markdown
:white_check_mark: **Approved with Comments**

LGTM! A few minor suggestions:

1. [Optional improvement]
2. [Optional improvement]

Feel free to address these in this PR or a follow-up.
```

### Approving

```markdown
:white_check_mark: **Approved**

Excellent work! Clean implementation with good test coverage.

Highlights:
- [Positive note]
- [Positive note]
```

---

## Inline Comment Templates

### Bug Found

```markdown
:bug: **Bug**

This will cause [issue] when [condition].

Suggested fix:
```python
# fix here
```
```

### Performance Concern

```markdown
:zap: **Performance**

This is O(n²) due to [reason]. Consider using [alternative] for O(n) complexity.
```

### Security Issue

```markdown
:lock: **Security**

This is vulnerable to [attack type]. See OWASP [link].

Fix:
```python
# secure version
```
```

### Style Suggestion

```markdown
:art: **Style**

Consider using [pattern/approach] here for better [readability/maintainability].
```

### Question

```markdown
:question: **Question**

Why is [this approach] used here instead of [alternative]? Is there a specific reason?
```

### Praise

```markdown
:star: **Nice!**

Great use of [pattern/technique] here. This makes the code much more [readable/maintainable/testable].
```
