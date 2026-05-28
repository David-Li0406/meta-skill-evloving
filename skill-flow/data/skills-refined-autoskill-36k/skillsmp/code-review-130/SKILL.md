---
name: code-review
description: Universal code review checklist and guidelines. Use when reviewing PRs, checking code quality, or providing feedback on code changes.
---

# Code Review

Universal code review checklist and guidelines.

## Review Mindset

### Goals
- Improve code quality
- Catch bugs before production
- Share knowledge
- Maintain standards

### Approach
- Be constructive, not critical
- Focus on the code, not the person
- Explain the "why" behind suggestions

## Review Checklist

### 1. Correctness
- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error cases covered
- [ ] Tests verify behavior

### 2. Readability
- [ ] Clear naming
- [ ] Logical structure
- [ ] Appropriate comments
- [ ] Consistent style

### 3. Maintainability
- [ ] Single responsibility
- [ ] No magic numbers
- [ ] Appropriate abstractions
- [ ] No code duplication

### 4. Security
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention

### 5. Performance
- [ ] No N+1 queries
- [ ] Appropriate data structures
- [ ] Efficient algorithms
- [ ] Resource cleanup

### 6. Testing
- [ ] Tests exist
- [ ] Tests are meaningful
- [ ] Edge cases tested

## Providing Feedback

### Be Specific
```
# Bad
"This function is confusing"

# Good
"Consider splitting this into validate_input() and process_data()
to make each function's responsibility clearer."
```

### Explain Why
```
# Bad
"Use a Set instead of Array"

# Good
"Consider using a Set - lookup is O(1) vs O(n),
which matters since this runs for each cart item."
```

### Prioritize
- 🔴 **Blocker**: Must fix before merge
- 🟡 **Suggestion**: Should consider
- 🟢 **Nit**: Minor improvement

## Quick Reference

```markdown
### Verdict
- ✅ Approve
- ⚠️ Suggestions
- ❌ Changes required
```
