# Quality Review Report

**Generated**: {TIMESTAMP}
**Scope**: {FILES_REVIEWED} files ({LINES_REVIEWED} lines)
**Duration**: {REVIEW_DURATION}

## Summary

✅ **Files Reviewed**: {FILES_REVIEWED}
📊 **Total Issues**: {TOTAL_ISSUES}
🚨 **Critical (P0)**: {P0_COUNT}
🔶 **High (P1)**: {P1_COUNT}
🟡 **Medium (P2)**: {P2_COUNT}
🔵 **Low (P3)**: {P3_COUNT}

## Agent Results

- ✅ **Duplicate Code Detector**: {DUPLICATE_STATUS}
- ✅ **User Voice (jenny)**: {JENNY_STATUS}
- ✅ **Code Review**: {CODE_REVIEW_STATUS}
- {DEEP_BUG_HUNTER_STATUS}

---

## Critical Issues (P0) - Fix Immediately 🚨

{IF_NO_P0_ISSUES}
✅ No critical issues found! Code is safe for production.
{ENDIF}

{FOR_EACH_P0_ISSUE}

### {ISSUE_NUMBER}. {ISSUE_TITLE}

**File**: `{FILE_PATH}:{LINE_NUMBER}`
**Category**: {CATEGORY} ({SOURCE_AGENT})
**Impact**: {IMPACT_DESCRIPTION}

**Problem**:

```
{PROBLEM_DESCRIPTION}
```

**Fix**:

```{LANGUAGE}
{FIX_CODE_EXAMPLE}
```

**Why this matters**: {DETAILED_EXPLANATION}

---

{END_FOR_EACH}

## High Priority Issues (P1) - Fix Soon 🔶

{IF_NO_P1_ISSUES}
✅ No high priority issues found.
{ENDIF}

{FOR_EACH_P1_ISSUE}

### {ISSUE_NUMBER}. {ISSUE_TITLE}

**File**: `{FILE_PATH}:{LINE_NUMBER}`
**Category**: {CATEGORY} ({SOURCE_AGENT})
**Impact**: {IMPACT_DESCRIPTION}

**Problem**:

```
{PROBLEM_DESCRIPTION}
```

**Fix**:

```{LANGUAGE}
{FIX_CODE_EXAMPLE}
```

---

{END_FOR_EACH}

## Medium Priority Issues (P2) - Address This Week 🟡

{IF_NO_P2_ISSUES}
✅ No medium priority issues found.
{ENDIF}

{FOR_EACH_P2_ISSUE}

### {ISSUE_NUMBER}. {ISSUE_TITLE}

**File**: `{FILE_PATH}:{LINE_NUMBER}`
**Category**: {CATEGORY} ({SOURCE_AGENT})

**Issue**: {BRIEF_DESCRIPTION}
**Fix**: {BRIEF_FIX_DESCRIPTION}

{IF_HAS_REFERENCE}
**Reference**: See `{PATTERN_FILE_REFERENCE}`
{ENDIF}

---

{END_FOR_EACH}

## Low Priority Issues (P3) - Technical Debt 🔵

{IF_NO_P3_ISSUES}
✅ No low priority issues found.
{ENDIF}

{FOR_EACH_P3_ISSUE}

### {ISSUE_NUMBER}. {ISSUE_TITLE}

**File**: `{FILE_PATH}:{LINE_NUMBER}`
**Suggestion**: {IMPROVEMENT_SUGGESTION}

---

{END_FOR_EACH}

## Recommendations

### Immediate Actions (Before Commit)

{FOR_EACH_P0_ISSUE}

- [ ] Fix P0 #{ISSUE_NUMBER}: {ISSUE_TITLE_SHORT}
      {END_FOR}
      {IF_NO_P0}
      ✅ Safe to commit - no critical issues blocking
      {ENDIF}

### Short-Term (1-2 Days)

{FOR_EACH_P1_ISSUE}

- [ ] Fix P1 #{ISSUE_NUMBER}: {ISSUE_TITLE_SHORT}
      {END_FOR}
      {IF_NO_P1}
      ✅ No urgent fixes required
      {ENDIF}

### Medium-Term (This Week)

{FOR_EACH_P2_ISSUE}

- [ ] Address P2 #{ISSUE_NUMBER}: {ISSUE_TITLE_SHORT}
      {END_FOR}

### Long-Term (Technical Debt)

{FOR_EACH_P3_ISSUE}

- [ ] Consider P3 #{ISSUE_NUMBER}: {ISSUE_TITLE_SHORT}
      {END_FOR}

---

## Detailed Findings by Agent

### Duplicate Code Detector

{IF_DUPLICATES_FOUND}
Found **{DUPLICATE_COUNT} duplications** that should use existing utilities:

{FOR_EACH_DUPLICATION}
**{DUPLICATED_FILE}:{LINE}**

- Duplicates: `{EXISTING_UTILITY_PATH}`
- Use instead: `{IMPORT_STATEMENT}`
- Reason: {WHY_USE_EXISTING}
  {END_FOR}
  {ELSE}
  ✅ No code duplications found. All code properly uses existing utilities.
  {ENDIF}

### User Voice (jenny)

{IF_JENNY_ISSUES_FOUND}
Found **{JENNY_COUNT} completeness/expectation issues**:

{FOR_EACH_JENNY_ISSUE}
**{CATEGORY}** - {ISSUE_TITLE}

- What's missing: {DESCRIPTION}
- Why user would care: {USER_IMPACT}
- Suggested fix: {FIX_SUMMARY}
  {END_FOR}
  {ELSE}
  ✅ Implementation appears complete and matches user expectations.
  {ENDIF}

### Code Review

{IF_CODE_ISSUES_FOUND}
Found **{CODE_ISSUE_COUNT} code quality issues**:

**Bugs & Correctness**: {BUG_COUNT} issues
**Performance**: {PERF_COUNT} issues
**Security**: {SECURITY_COUNT} issues
**Antipatterns**: {ANTIPATTERN_COUNT} issues

{FOR_EACH_CODE_ISSUE}

- {SEVERITY} - {FILE}:{LINE} - {BRIEF_DESCRIPTION}
  {END_FOR}
  {ELSE}
  ✅ No code quality issues found.
  {ENDIF}

### Deep Bug Hunter

{IF_DEEP_BUG_HUNTER_RAN}
{IF_ROOT_CAUSES_FOUND}
Investigated **{ROOT_CAUSE_COUNT} root causes**:

{FOR_EACH_ROOT_CAUSE}
**Root Cause #{NUMBER}**: {ROOT_CAUSE_TITLE}

- Chain of events: {EVENT_CHAIN}
- Why not caught earlier: {REASON_MISSED}
- Comprehensive fix: {FIX_DESCRIPTION}
- Prevention: {PREVENTIVE_MEASURES}
  {END_FOR}
  {ELSE}
  ✅ Deep investigation found no additional root causes.
  {ENDIF}
  {ELSE}
  ⏭️ Deep bug hunter not triggered (no critical issues found in earlier phases)
  {ENDIF}

---

## Severity Definitions

**P0 (Critical)** 🚨

- Bugs that break core functionality
- Security vulnerabilities (SQL injection, XSS, data leaks)
- Data corruption issues
- Missing multi-tenant isolation
- Production outage risks

**P1 (High)** 🔶

- Logic errors affecting user workflows
- Performance issues causing noticeable slowness
- Incorrect business logic implementations
- Missing error handling for common cases
- Type safety issues that could cause runtime errors

**P2 (Medium)** 🟡

- Code duplications (violates DRY principle)
- Antipatterns from react-typescript-antipatterns.md
- Specification gaps (not following CLAUDE.md patterns)
- Missing optimizations (useMemo, useCallback)
- Suboptimal algorithms

**P3 (Low)** 🔵

- Style inconsistencies
- Minor performance improvements
- Code clarity improvements
- Documentation gaps
- Non-critical refactoring opportunities

---

## Next Steps

{IF_HAS_P0_ISSUES}

### ⚠️ Critical Issues Found - Action Required

**DO NOT COMMIT** until P0 issues are fixed. These are blocking issues that will break production.

Recommended workflow:

1. Fix all P0 issues immediately
2. Run `check-your-work` again to verify fixes
3. Run `npm run typecheck` to ensure no type errors
4. Run manual tests to verify functionality
5. Then commit safely
   {ELSE}

### ✅ Safe to Commit

No critical issues found. You can proceed with committing your changes.

{IF_HAS_P1_ISSUES}
Consider fixing P1 issues before commit for better code quality.
{ENDIF}

{IF_HAS_P2_OR_P3_ISSUES}
P2/P3 issues can be addressed in follow-up PRs or added to technical debt backlog.
{ENDIF}
{ENDIF}

---

## Questions or Concerns?

If any findings are unclear or you disagree with the assessment:

1. Review the detailed explanation in the issue description
2. Check the referenced pattern file (if applicable)
3. Ask for clarification: "Can you explain why [specific issue] is a problem?"
4. Discuss with team if you believe the pattern should be updated

Remember: These are recommendations based on project patterns. Use your judgment for domain-specific concerns.

---

**Report generated by check-your-work skill v{VERSION}**
**Review completed at {TIMESTAMP}**
