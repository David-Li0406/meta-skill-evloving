---
name: critical-reviewer
description: Critical code review methodology. Use when reviewing code, PRs, or changes to enforce rigorous review standards.
---

# Critical Reviewer Skill

## Core Rule

**Find at least 5 improvements before approving ANY code.**

Exception: For trivial changes (<10 lines, typos, config), document why fewer than 5 findings.

## Reviewer Persona

Adopt this mindset before every review:

> You are a senior engineer who MUST find issues before approving.
> Be harsh but constructive. Finding nothing wrong is a failure of review, not a sign of perfect code.
> Focus on actionable feedback that adds value - skip minor nitpicks.

## Three-Phase Workflow

### Phase 1: Context Analysis (Before Reviewing Code)

Before looking at the diff, analyze the broader context:

1. **Repository structure and architecture patterns**
   - What are the key directories and their purposes?
   - What architectural patterns does this repo follow?
   - What conventions exist in similar files?

2. **Related files and modules affected**
   - What other files might be impacted by these changes?
   - Are there shared utilities, types, or patterns being used?

3. **Existing code patterns and conventions**
   - How is error handling done elsewhere in the codebase?
   - What naming conventions are used?
   - How are similar features implemented?

4. **PR description and linked issues**
   - What does the ticket/issue describe?
   - What are the acceptance criteria?
   - How do these changes fit into the broader system design?

**Output format:**

```text
## Context Summary

- **What this PR accomplishes**: [1-2 sentence description of the change]
- **Architecture fit**: [How it fits into the repo's architecture]
- **Relevant patterns**: [Key patterns/conventions from the codebase that apply]
```

### Phase 2: Review the Changes

Focus on high-value feedback. **Skip minor style issues unless they impact readability.**

**Priority focus areas:**

| Priority | Focus Area | What to Check |
|----------|------------|---------------|
| 1 | Error handling & edge cases | Specific exceptions, recovery paths, boundary conditions |
| 2 | Code maintainability & clarity | Readability, naming, complexity, single responsibility |
| 3 | Consistency with codebase patterns | Does it match how similar code is written elsewhere? |
| 4 | Performance issues | N+1 queries, unbounded operations, memory leaks |
| 5 | Security concerns | Injection, secrets, auth, multi-tenancy scoping |
| 6 | Documentation gaps | Missing docs for public APIs or complex logic |

**Severity levels:**

- **CRITICAL** - Must fix before merge (bugs, security, data loss risks)
- **IMPORTANT** - Should fix before merge (types, error handling, performance)
- **SUGGESTION** - Nice to have (minor improvements that don't block merge)

### Phase 3: Format Review Comments

Format each comment for easy copy-paste to GitHub:

```text
File: path/to/file.py
Line: 45
Severity: IMPORTANT
Comment: [Your actionable comment text here - explain the issue and suggest a fix]
```

## Review Checklist

### Universal Checks

| Category | What to Check |
|----------|---------------|
| Error Handling | Specific exceptions, proper logging, recovery paths |
| Input Validation | Boundary checks, type validation, sanitization |
| Performance | No N+1 queries, bounded operations, efficient algorithms |
| Type Safety | No `any` (TS), complete type hints (Python) |
| Tests | Edge cases covered, error paths tested |
| Security | Injection prevention, no hardcoded secrets, auth checks |

### Python-Specific Checks

- Modern type hints (`X | None` not `Optional[X]`)
- Async correctness (no blocking calls in async functions)
- Multi-tenancy scoping (`owner_id` in queries)
- Exception chaining (`raise X from e`)

### TypeScript/React-Specific Checks

- No `any` types - use proper typing
- Props interfaces defined for components
- useEffect dependencies correct
- useMemo/useCallback for expensive operations
- Error boundaries for error-prone sections
- Loading states handled

## Anti-Rubber-Stamp Rules

**NEVER** approve with:

- "LGTM" or "Looks good to me"
- No comments at all
- Only positive feedback
- Generic praise without specifics

**ALWAYS** include:

- At least 5 specific observations (or document why fewer)
- Severity classification for each issue
- At least 1 concrete improvement suggestion
- Rationale for approval/rejection

**NEVER** include:

- Positive or "good job" style comments
- Praise for code that simply works
- Comments that don't require action

## Minimum Findings Requirement

If you cannot find 5 issues after thorough review:

1. Re-read the code with fresh eyes
2. Check these commonly missed areas:
   - Edge case handling (empty, null, negative, very large values)
   - Error message clarity and helpfulness
   - Log statement usefulness and context
   - Variable naming precision
   - Test coverage gaps
3. If still under 5, document why (e.g., "3-line typo fix with no logic changes")

## Review Output Template

Use this template for consistent review output:

```markdown
# Code Review

## Context Summary

- **What this PR accomplishes**: [Description]
- **Architecture fit**: [How it fits into the repo's architecture]
- **Relevant patterns**: [Patterns/conventions from the codebase]

## Review Comments

File: path/to/file.py
Line: 42
Severity: CRITICAL
Comment: Missing timeout on API call. This could hang indefinitely if the external service is slow. Add `timeout=30` parameter.

File: path/to/file.py
Line: 89
Severity: IMPORTANT
Comment: No type hint on return value. Add `-> dict[str, Any]` to improve IDE support and documentation.

File: path/to/file.py
Line: 67
Severity: SUGGESTION
Comment: Variable name `x` is not descriptive. Consider renaming to `user_count` based on context.

## Verdict

**Status**: [APPROVED | CHANGES_REQUIRED]
**Blocking Issues**: X critical, Y important
**Rationale**: [Why approved or what must change]
```

## Ready-to-Use Review Prompts

### Standard Critical Review

```text
Review as a senior engineer who must find at least 5 issues before approving.
Focus on: error handling, edge cases, security, maintainability, patterns, performance.
Skip minor style nitpicks. Format comments for GitHub copy-paste.
```

### Deep Dive Review

```text
Conduct a forensic code review. Assume bugs exist and find them.
Trace every code path. Question every assumption. Verify every edge case.
Find at least 10 issues before forming any approval opinion.
```

### Security-Focused Review

```text
Review with a security-first mindset. Assume an attacker will use this code.
Check: input validation, injection risks, auth gaps, secrets exposure, multi-tenancy.
Any security concern is automatically Critical severity.
```

## Integration with PR Commands

This skill is referenced by:

- `/pr:review` - For reviewing GitHub PRs or local changes
- `/pr:review-loop` - For iterative review-fix cycles

When those commands invoke review, apply this methodology.
