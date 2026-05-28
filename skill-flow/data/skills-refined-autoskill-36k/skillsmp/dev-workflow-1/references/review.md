# Code Review

> For the reviewer role. Check against project standards and PR checklist.

## Review Checklist

Review items align with Priority Stack from Core Principles.

### 1. Security (Priority 1)
- [ ] No secrets, API keys, or passwords in code
- [ ] No sensitive data logged or exposed
- [ ] Input validation present where needed

### 2. Correctness (Priority 2)
- [ ] Logic matches stated intent
- [ ] Edge cases handled
- [ ] Error handling explicit (no silent catches)

### 3. Tests
- [ ] Tests exist for behavioral changes
- [ ] Tests cover happy path + edge cases
- [ ] All tests pass (CI green)

### 4. Code Quality
- [ ] Type annotations on function signatures
- [ ] Functions are small and testable
- [ ] No drive-by refactors unrelated to PR scope

### 5. Documentation
- [ ] `CHANGELOG.md` updated for behavioral changes
- [ ] `README.md` updated if CLI/config changed
- [ ] Code comments where logic is non-obvious

### 6. Task Tracking (if applicable)
- [ ] Task/roadmap status updated (if project uses task tracking)
- [ ] PR description links to task/issue

## Feedback Guidelines

| Issue Severity | Action |
|----------------|--------|
| Security/Data risk | Block merge |
| Logic error | Block merge |
| Missing tests | Block merge (for behavioral changes) |
| Missing docs/changelog | Block merge (for user-facing changes) |
| Style/naming | Comment as nit; don't block |
| Suggestion/improvement | Comment; author decides |

## Feedback Format

Be specific and actionable:

```
❌ "This is confusing"
✅ "Consider renaming `proc_data` to `process_user_input` for clarity"

❌ "Add tests"
✅ "Missing test for empty input case in `parse_config()`"
```

## PR Size Check

- >400 lines → Suggest splitting
- Mixed concerns (feature + refactor) → Suggest separate PRs

---

**→ After review:** Approve or Request Changes. If approved, author merges per `pullrequest.md` strategy.
