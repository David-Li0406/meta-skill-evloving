---
name: review
description: Performs comprehensive code review with stack detection, deep logic tracing, and double-verification of bugs before reporting
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Skill
---

# Code Reviewer

## Purpose

Review code changes for quality, security, performance, and adherence to project patterns.

**This skill supports iterative review loops** - it will be called multiple times as part of a review-fix cycle.

## When to Invoke

- After implementing a feature or making significant changes
- Before committing code to version control
- During pull request review
- When refactoring existing code
- **As part of iterative review-fix loops** (called repeatedly)

## Review Modes

### Mode 1: Initial Review (Full Scope)

First review in a cycle - comprehensive analysis of everything.

**Scope:**

- Security (critical)
- Bugs (critical)
- Performance (warnings)
- Patterns (warnings)
- Style (suggestions)
- Documentation (suggestions)

### Mode 2: Follow-up Review (Focused)

Subsequent reviews - focus only on remaining issues.

**Scope:**

- Only review the specific issues that were reported
- Verify fixes resolved the problems
- Check for new issues introduced by fixes
- Report any NEW issues found

### Mode 3: Verification Review (Final Check)

Final review - confirm all issues resolved.

**Scope:**

- Verify all previously reported issues are fixed
- No new issues introduced
- Ready to proceed

## Iterative Review Protocol

When called as part of a review-fix loop:

### First Call (Initial Review)

```
Context: "Initial review after implementation"
Output: Full comprehensive review with all issues
Focus: All aspects (security, bugs, patterns, performance)
```

### Subsequent Calls (Follow-up Review)

```
Context: "Follow-up review - verify fixes for: {previous_issues}"
Output: Report on:
  1. Which previous issues are now FIXED ✓
  2. Which previous issues REMAIN ✗
  3. Any NEW issues introduced by fixes
Focus: Only remaining + new issues (don't re-report fixed items)
```

### Final Call (Verification)

```
Context: "Final verification review"
Output: Confirmation that:
  1. All issues from previous reviews are RESOLVED
  2. No new issues introduced
  3. Ready to proceed to next phase
```

## Output Format for Iterative Reviews

### Initial Review Output

```markdown
## Code Review: Initial

### Summary

{Quick overview}

### Critical Issues (Must Fix)

1. {Issue description}
   - Location: {file:line}
   - Impact: {why it's critical}
   - Fix: {suggested fix}

### Warnings (Should Fix)

{Similar format}

### Suggestions (Nice to Have)

{Similar format}

### What Was Done Well

{Positive feedback}

---

**Total:** X critical, Y warnings, Z suggestions
```

### Follow-up Review Output

```markdown
## Code Review: Follow-up (Iteration N)

### Previous Issues Status

✅ Fixed: {list of resolved issues}
❌ Remaining: {list of unresolved issues}

### New Issues Found

{Any new issues introduced by fixes}

### Updated Summary

**Remaining:** X critical, Y warnings

### Next Steps

{What to focus on next}
```

### Verification Review Output

```markdown
## Code Review: Final Verification

### All Previous Issues: ✅ RESOLVED

### No New Issues Introduced

### Status: READY TO PROCEED

All quality checks passed. Code is ready for:
{next phase - e.g., quality gates, commit, etc.}
```

## Capabilities

### Quality Checks

- Adherence to CQRS pattern (for backend code)
- Proper use of domain-driven design principles
- Code organization and structure
- Naming conventions
- Documentation completeness

### Security Checks

- SQL injection vulnerabilities
- XSS vulnerabilities in frontend code
- Proper authentication/authorization
- PII encryption for sensitive data
- Input validation
- Dependency vulnerabilities

### Performance Checks

- N+1 query patterns
- Missing database indexes
- Inefficient re-renders in React
- Bundle size impact
- Memory leaks
- Unnecessary re-computations

### Pattern Compliance

- CQRS pattern usage (commands/queries/events)
- Repository pattern for data access
- Server Components first (Next.js)
- tRPC for type-safe APIs
- Testcontainers for integration tests
- Proper error handling

### Test Coverage

- Unit test coverage (target: 80%)
- Integration test usage
- Test quality and meaningful assertions
- Edge case coverage

## How to Use

### As a Skill

```
Skill('review')
```

### With Specific Focus

```
Skill('review', 'Review the auth module for security issues')
Skill('review', 'Review the user list component for performance')
```

### In Iterative Loop

```
# Iteration 1
Skill('review')  # Full review
→ Returns: 3 critical, 2 warnings

# Iteration 2 (after fixes)
Skill('review', 'Verify fixes for: security-1, security-2, security-3')
→ Returns: 2 fixed, 1 remaining, 1 new

# Iteration 3 (final)
Skill('review', 'Final verification')
→ Returns: All resolved, ready to proceed
```

## Review Checklist

- [ ] Code follows CQRS pattern (backend)
- [ ] No security vulnerabilities
- [ ] Proper error handling
- [ ] Tests present and passing
- [ ] No performance issues
- [ ] Types are properly defined
- [ ] Documentation is clear
- [ ] Naming follows conventions
- [ ] No hardcoded values
- [ ] Environment variables used for secrets

## Stopping Conditions

**STOP the review loop when:**

1. All critical issues resolved
2. All warnings addressed (or user accepts)
3. No new issues introduced
4. Ready for next phase

**ESCALATE when:**

1. Same issue persists across 3 reviews
2. Fix introduces new critical issue
3. Cannot verify fix effectiveness
4. Require user decision on trade-offs
