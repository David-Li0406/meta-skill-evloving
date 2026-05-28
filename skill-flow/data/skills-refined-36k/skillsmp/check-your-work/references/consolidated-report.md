# Phase 5: Consolidated Report

## Goal
Combine all findings, prioritize by severity, guide user through remediation.

## Finding Structure

```typescript
interface Finding {
  severity: "P0" | "P1" | "P2" | "P3";
  category: "bug" | "security" | "performance" | "duplication" | "spec-gap" | "antipattern";
  file: string;
  line?: number;
  description: string;
  impact: string;
  fix: string;
  codeExample?: string;
  source: "duplicate-detector" | "jenny" | "code-review" | "deep-bug-hunter";
}

interface ValidatedFinding extends Finding {
  validationStatus: "CONFIRMED" | "DOWNGRADED" | "N/A";
  validationReasoning: string;
  originalSeverity?: "P0" | "P1"; // If downgraded
}
```

## Severity Classification

### P0 (Critical)
- Bugs that break core functionality
- Security vulnerabilities (SQL injection, XSS, data leaks)
- Data corruption issues
- Missing multi-tenant isolation (organization_id)
- Production outage risks

### P1 (High)
- Logic errors affecting user workflows
- Performance issues causing noticeable slowness
- Incorrect implementations of business logic
- Missing error handling for common cases
- Type safety issues that could cause runtime errors

### P2 (Medium)
- Code duplications (violates DRY principle)
- Antipatterns from react-typescript-antipatterns.md
- Specification gaps (not following CLAUDE.md patterns)
- Missing optimizations (useMemo, useCallback)
- Suboptimal algorithms

### P3 (Low)
- Style inconsistencies
- Minor performance improvements
- Code clarity improvements
- Documentation gaps
- Non-critical refactoring opportunities

## Report Sections

1. **Summary**: Files reviewed, line count, issue count by severity
2. **Validation Summary**: P0/P1 flagged → confirmed/downgraded/false positive
3. **Critical Issues (P0)**: With validation status, reasoning, impact, fix
4. **High Priority (P1)**: Same format as P0
5. **Medium Priority (P2)**: Including downgraded findings
6. **Low Priority (P3)**: Style, minor improvements
7. **Recommendations**: Immediate (before commit), short-term, long-term

## User Decision Options

Use AskUserQuestion with:
1. **Fix P0 critical issues now** - Recommended before commit
2. **Fix P0 + P1 issues now** - Thorough before commit
3. **Create todo list for all issues** - Track for incremental fixes
4. **Show full report only** - View only, no automated action

## Interpreting Results

| Result | Meaning | Action |
|--------|---------|--------|
| No issues | Code is production-ready | Proceed with commit |
| Only P2/P3 | Functionally correct, has debt | Safe to commit, track issues |
| P1 issues | Recommend fixing | Fix before commit or track |
| P0 issues | **DO NOT COMMIT** | Fix immediately and re-run |
