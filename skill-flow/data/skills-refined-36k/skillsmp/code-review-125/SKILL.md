---
name: code-review
description: Review implementation for code quality, style consistency, and best practices. Runs before security review. READ-ONLY - reports issues but does not fix them.
allowed-tools: Read, Glob, Grep
user-invocable: true
---

# Code Review Skill

## Purpose

Review implementation for quality issues before security review. Catch maintainability problems, style inconsistencies, and best practice violations. Produce pass/fail report with findings.

**Key Input**: Spec group at `.claude/specs/groups/<spec-group-id>/`

## Usage

```
/code-review <spec-group-id>                   # Review all changes for spec group
/code-review <spec-group-id> <atomic-spec-id>  # Review changes for specific atomic spec
```

## When to Use

**Mandatory for**:
- Any implementation completing the spec workflow
- Multi-file changes
- Public API additions or modifications
- Changes to core services

**Optional for**:
- Single-file bug fixes
- Documentation-only changes
- Test-only changes
- Configuration changes

## Review Pipeline Position

```
Implementation → Unify → Code Review → Security Review → Merge
                            ↑
                        You are here
```

Code Review runs BEFORE Security Review because:
- Quality issues may mask security issues
- Consistent code is easier to security-review
- Catches different class of problems

## Prerequisites

Before code review, verify:

1. **Spec group exists** at `.claude/specs/groups/<spec-group-id>/`
2. **Convergence validated** - `/unify` has passed
3. **All atomic specs implemented** - status is `implemented`
4. **Tests passing** - all tests pass

If prerequisites not met → STOP and run `/unify` first.

## Code Review Process

### Step 1: Load Review Context

```bash
# Load manifest
cat .claude/specs/groups/<spec-group-id>/manifest.json

# Verify convergence passed
# convergence.all_acs_implemented: true
# convergence.all_tests_passing: true

# Load spec and atomic specs
cat .claude/specs/groups/<spec-group-id>/spec.md
ls .claude/specs/groups/<spec-group-id>/atomic/

# What files changed (from atomic spec evidence)
# Read Implementation Evidence sections from each atomic spec
```

### Step 2: Identify Files to Review

Build file list from atomic spec Implementation Evidence:

```bash
# For each atomic spec, extract Implementation Evidence
# These are the files that need review

# Alternatively, use git diff if on a feature branch
git diff --name-only main..HEAD
```

### Step 3: Review Categories

Check each category systematically:

#### A. Code Style & Consistency

- Naming conventions (camelCase, PascalCase per project standard)
- File organization (imports, exports, structure)
- Formatting consistency
- Comment quality (useful vs obvious vs missing)
- AC references in comments (should reference atomic spec IDs)

#### B. Code Quality & Maintainability

- Function length (>50 lines is suspect)
- Cyclomatic complexity (>10 is suspect)
- Deep nesting (>3 levels is suspect)
- Code duplication
- Dead code
- Magic numbers/strings

#### C. TypeScript Best Practices

- `any` usage (should be rare and justified)
- Missing return types on public methods
- Proper null/undefined handling
- Generic usage appropriateness
- Type assertions (`as`) overuse

#### D. Error Handling

- Empty catch blocks
- Swallowed errors (catch and return null)
- Missing error types
- Inconsistent error handling patterns
- Error messages quality

#### E. API Design

- Inconsistent parameter ordering
- Missing or inconsistent return types
- Breaking changes to public API
- Undocumented public methods

#### F. Spec Conformance

- Implementation matches atomic spec ACs
- No undocumented features added
- Error handling per spec
- Edge cases per spec addressed

#### G. Testing Gaps

- Public methods without tests
- Edge cases not covered
- Test quality (meaningful assertions)
- Test isolation (no shared state)
- Tests reference correct atomic spec IDs

### Step 4: Severity Classification

| Level | Meaning | Blocks Merge |
|-------|---------|--------------|
| **Critical** | Will cause runtime failure | Yes |
| **High** | Significant maintainability issue | Yes |
| **Medium** | Should fix but not blocking | No |
| **Low** | Suggestion for improvement | No |

### Step 5: Generate Review Report

```markdown
## Code Review Report

**Spec Group**: <spec-group-id>
**Files Reviewed**: 6
**Review Date**: 2026-01-14

### Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 3 |

**Verdict**: ✅ PASS

### Per Atomic Spec Review

#### as-001: Logout Button UI
- Files: src/components/UserMenu.tsx
- Quality: ✅ Clean
- Spec Conformance: ✅ Matches ACs

#### as-002: Token Clearing
- Files: src/services/auth-service.ts
- Quality: ⚠️ 1 Medium finding (M1)
- Spec Conformance: ✅ Matches ACs

#### as-003: Post-Logout Redirect
- Files: src/router/auth-router.ts
- Quality: ✅ Clean
- Spec Conformance: ✅ Matches ACs

#### as-004: Error Handling
- Files: src/services/auth-service.ts
- Quality: ⚠️ 1 Medium finding (M2)
- Spec Conformance: ✅ Matches ACs

### Findings

#### Medium Severity

**M1: Function approaching length limit**
- **File**: src/services/auth-service.ts:45-90
- **Atomic Spec**: as-002
- **Issue**: `logout` function is 45 lines (approaching 50 line threshold)
- **Impact**: May become harder to maintain as feature grows
- **Suggestion**: Consider extracting token clearing logic

**M2: Missing return type**
- **File**: src/services/auth-service.ts:95
- **Atomic Spec**: as-004
- **Issue**: `handleLogoutError` has no return type annotation
- **Impact**: Type safety lost for consumers
- **Suggestion**: Add `Promise<void>` return type

#### Low Severity

[... suggestions ...]

### Positive Observations

- Good traceability - code comments reference atomic spec IDs
- Consistent use of Result type pattern
- Clear separation of concerns in handlers
- Test coverage matches Implementation Evidence

### Recommendations

1. Consider extracting token clearing logic (M1) in follow-up
2. Add return types to all public methods (M2)
3. Add JSDoc to public APIs (L1, L2) for better DX
```

### Step 6: Handle Blocking Issues

If Critical or High severity issues found:

```markdown
## Code Review Report

**Spec Group**: <spec-group-id>
**Verdict**: ❌ BLOCKED (2 High severity issues)

### Blocking Issues

**H1: Swallowed exception in error handling**
- **File**: src/services/auth-service.ts:78
- **Atomic Spec**: as-004
- **Issue**: Catch block returns null, hiding failure cause
- **AC Violation**: as-004 AC1 requires error message display
- **Impact**: Logout failures will be silent, hard to debug
- **Required Fix**: Throw AuthError with cause chain

**H2: Implementation deviates from spec**
- **File**: src/services/auth-service.ts:67
- **Atomic Spec**: as-002
- **Issue**: Clears ALL localStorage, spec says only auth_token
- **AC Violation**: as-002 AC1 specifies "clear authentication token"
- **Impact**: User data loss
- **Required Fix**: Change `localStorage.clear()` to `localStorage.removeItem('auth_token')`

**Action**: Fix blocking issues, then re-run code review.
```

### Step 7: Update Manifest

Update manifest.json with code review status:

```json
{
  "convergence": {
    "code_review_passed": true
  },
  "decision_log": [
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "code_review_complete",
      "details": "0 critical, 0 high, 2 medium, 3 low - PASS"
    }
  ]
}
```

## Review Guidelines

### Be Specific and Actionable

**Bad**:
```markdown
Code quality could be better in auth.ts
```

**Good**:
```markdown
**Quality: Function too long** (Medium)
- File: src/services/auth-service.ts:45-120
- Atomic Spec: as-002
- Issue: `validateSession` is 75 lines with 8 branches
- Impact: Hard to test, hard to modify safely
- Suggestion: Extract token parsing (L45-65) and permission check (L80-100)
```

### Check Spec Conformance

Always verify implementation matches atomic spec:

```markdown
**Spec Conformance: Extra feature added** (High)
- File: src/services/auth-service.ts:85
- Atomic Spec: as-002
- Issue: Auto-retry on failure added (not in spec)
- AC Violation: No AC mentions retry logic
- Impact: Undocumented behavior, may cause unexpected side effects
- Required Fix: Remove or add to spec via amendment
```

### Reference Atomic Specs in Findings

Every finding should reference the atomic spec it relates to:

```markdown
**H1: Missing error handling**
- **File**: src/router/auth-router.ts:45
- **Atomic Spec**: as-003  ← Always include this
- **Issue**: ...
```

### Acknowledge Good Patterns

Include positive observations:
- Well-structured code
- Good test coverage
- Clear AC references in code
- Good traceability

### Scope to Changes

Review what changed, not the entire codebase.

**In scope**: Files listed in atomic spec Implementation Evidence
**Out of scope**: Pre-existing issues in unchanged files

Note pre-existing issues as "Pre-existing" - they don't block merge.

## Review Checklist

For each atomic spec:

```markdown
□ Implementation Evidence files reviewed
□ Code matches ACs in atomic spec
□ No undocumented features added
□ Naming follows project conventions
□ No obvious code duplication
□ Functions are reasonably sized (<50 lines)
□ Nesting depth acceptable (<4 levels)
□ Error handling matches spec
□ No `any` without justification
□ Public APIs have return types
□ Tests reference correct atomic spec IDs
```

## Integration with Other Skills

**Before code review**:
- `/unify` to ensure spec-impl-test convergence

**After code review**:
- If PASS → Proceed to `/security`
- If BLOCKED → Use `/implement` to fix issues, then re-run `/code-review`

**Full review chain after code-review**:
1. `/security` - Security review (always)
2. `/browser-test` - UI validation (if UI changes)
3. `/docs` - Documentation generation (if public API)
4. Commit

## Constraints

### READ-ONLY

You report findings but do not modify code. Let Implementer fix issues.

### Not Security Review

Focus on code quality. Security Reviewer handles:
- Injection vulnerabilities
- Authentication/authorization flaws
- Secrets exposure
- OWASP Top 10

Flag obvious security issues, but security review is the comprehensive check.

## Examples

### Example 1: Clean Pass

**Input**: Well-structured logout implementation (spec group sg-logout-button)

**Review**:
- as-001: ✅ Clean implementation
- as-002: ✅ Clean implementation
- as-003: ✅ Clean implementation
- as-004: ✅ Clean implementation

**Output**: ✅ PASS - No findings, proceed to security review

### Example 2: Pass with Recommendations

**Input**: Feature implementation with minor issues

**Review**:
- as-001: ✅ Clean
- as-002: ⚠️ 1 Medium (long function)
- as-003: ✅ Clean
- as-004: ⚠️ 1 Medium (missing JSDoc)

**Output**: ✅ PASS with recommendations - Proceed, address in follow-up

### Example 3: Blocked

**Input**: Implementation with spec deviation

**Review**:
- as-002: ❌ High (clears all localStorage instead of just auth_token)

**Output**: ❌ BLOCKED - Fix H1 before proceeding
