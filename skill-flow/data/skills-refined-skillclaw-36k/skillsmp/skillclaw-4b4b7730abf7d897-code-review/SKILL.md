---
name: code-review
description: Use this skill when reviewing code before commit, conducting quality gates, or when "review", "fresh eyes", "pre-commit review", or "quality gate" are mentioned.
---

# Fresh Eyes Review

Systematic pre-commit quality gate → checklist-based review → findings → summary.

<when_to_use>

- Pre-commit code review and quality gates
- Pre-merge pull request reviews
- Systematic code audits before deployment
- Quality verification for critical changes
- Second-opinion review requests

NOT for: quick sanity checks, trivial typo fixes, formatting-only changes

</when_to_use>

<announcement_protocol>

## Starting Review

**Review Scope:** { files/areas under review }  
**Focus Areas:** { specific concerns or general quality gate }  
**Checklist:** { full or targeted categories }  

## During Review

Emit findings as discovered:
- **{SEVERITY}** `{FILE_PATH}:{LINE}` — { issue description }
- **Impact:** { consequences if shipped }
- **Fix:** { concrete remediation }

## Completing Review

**Review Complete**

**Findings Summary:**
- ◆◆ Severe: {COUNT} — blocking issues
- ◆ Moderate: {COUNT} — should fix before merge
- ◇ Minor: {COUNT} — consider addressing

**Recommendation:** { ship / fix blockers / needs rework }

{ detailed findings below if any found }

</announcement_protocol>

<checklist>

## Type Safety

- ✓ No `any` types without justification comment
- ✓ Null/undefined handled explicitly (optional chaining, nullish coalescing)
- ✓ Type guards used for union types
- ✓ Discriminated unions for state machines
- ✓ Generic constraints specified where needed
- ✓ Return types explicit on public functions
- ✓ No type assertions without safety comment

## Error Handling

- ✓ All error paths handled (no silent failures)
- ✓ Meaningful error messages with context
- ✓ Errors propagated or logged appropriately
- ✓ Result types used for expected failures
- ✓ Try/catch blocks have specific error handling
- ✓ Promise rejections handled
- ✓ Resource cleanup in finally blocks

## Security

- ✓ User input validated before use
- ✓ No hardcoded secrets or credentials
- ✓ Authentication/authorization checks present
- ✓ Parameterized queries (no SQL injection)
- ✓ XSS prevention (sanitized output)
- ✓ CSRF protection where applicable
- ✓ Sensitive data encrypted/hashed
- ✓ Rate limiting on public endpoints

## Testing

- ✓ Tests exist for new functionality
- ✓ Edge cases covered
- ✓ Error scenarios tested
- ✓ Actual assertions

</checklist>