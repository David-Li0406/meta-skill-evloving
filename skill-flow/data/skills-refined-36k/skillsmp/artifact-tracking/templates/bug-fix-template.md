---
# === BUG FIX TRACKING TEMPLATE ===
# Monthly tracking of significant bug fixes
# One file per month: bug-fixes-tracking-MM-YY.md (e.g., bug-fixes-tracking-11-25.md)

# Metadata: Monthly Organization
type: bug-fixes
month: "[MM-YY]"                         # e.g., "11-25" for November 2025
year: [YYYY]                             # e.g., 2025
month_name: "[MONTH_NAME]"               # e.g., "November"

# Tracking Metrics
total_fixes: [COUNT]                     # Total fixes in month, e.g., 5
critical_fixes: [COUNT]                  # Severity: critical, e.g., 1
high_fixes: [COUNT]                      # Severity: high, e.g., 2
medium_fixes: [COUNT]                    # Severity: medium, e.g., 2
low_fixes: [COUNT]                       # Severity: low, e.g., 0

# Components Affected (for trending analysis)
components_affected: [
  # e.g., "blocks-editor", "prompt-modal", "api-endpoints"
]

# Categories (for pattern analysis)
categories: [
  # e.g., "frontend", "backend", "database", "integration"
]
---

# Bug Fixes - [MONTH_NAME] [YEAR]

**Month**: [MONTH_NAME] [YEAR]
**Total Fixes**: [COUNT]
**Critical**: [COUNT] | **High**: [COUNT] | **Medium**: [COUNT] | **Low**: [COUNT]
**Components**: [list of affected systems]

---

## Summary

Brief overview of major bug fix themes this month, e.g.:
- Fixed 3 critical UI rendering issues
- Resolved 2 backend race conditions
- Patched 1 security vulnerability

---

## Critical Fixes

### FIX-001: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🔴 Critical
**Component**: [Component name]
**Category**: [Category: frontend|backend|database|integration]

**Issue**: [Detailed description of what was broken]

**Root Cause**: [Why it happened - technical explanation]

**Fix**: [What was changed to resolve it]

**Files Modified**:
- `path/to/file1.tsx` - [What changed and why]
- `path/to/file2.py` - [What changed and why]

**Impact**: [What was affected and how many users/systems]

**Testing**: [How was it tested to ensure no regression]

**Commit**: [git commit hash or reference]

**Related**: [Link to related issues, discussions, or ADRs]

---

### FIX-002: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🔴 Critical
**Component**: [Component name]
**Category**: [Category]

[Follow same structure as FIX-001]

---

## High Priority Fixes

### FIX-003: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟠 High
**Component**: [Component name]
**Category**: [Category]

**Issue**: [What was broken]

**Root Cause**: [Why it happened]

**Fix**: [Solution applied]

**Files Modified**:
- `path/to/file.ts` - [What changed]

**Impact**: [Who/what was affected]

**Testing**: [Verification method]

**Commit**: [Reference]

---

### FIX-004: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟠 High
**Component**: [Component name]
**Category**: [Category]

[Follow same structure as FIX-003]

---

### FIX-005: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟠 High
**Component**: [Component name]
**Category**: [Category]

[Follow same structure as FIX-003]

---

## Medium Priority Fixes

### FIX-006: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟡 Medium
**Component**: [Component name]
**Category**: [Category]

**Issue**: [Brief description]

**Root Cause**: [Why it happened]

**Fix**: [Solution]

**Files Modified**:
- `path/to/file.ts` - [Change]

**Impact**: [Who/what affected]

**Commit**: [Reference]

---

### FIX-007: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟡 Medium
**Component**: [Component name]
**Category**: [Category]

[Follow same structure as FIX-006]

---

## Low Priority Fixes

### FIX-008: [Brief Title]

**Date Fixed**: [YYYY-MM-DD]
**Severity**: 🟢 Low
**Component**: [Component name]
**Category**: [Category]

**Issue**: [Brief description]

**Fix**: [Solution]

**Commit**: [Reference]

---

## By Component

### [Component Name]

**Fixes This Month**:
- FIX-001: [Brief title]
- FIX-003: [Brief title]

**Pattern**: [If multiple fixes in one component, describe the pattern]

**Recommendation**: [If pattern suggests deeper issue, suggest action]

---

### [Component Name]

**Fixes This Month**:
- FIX-002: [Brief title]

**Pattern**: [Description]

---

## By Category

### Frontend

| Fix | Title | Severity | Impact |
|-----|-------|----------|--------|
| FIX-001 | [Title] | Critical | [Impact] |
| FIX-004 | [Title] | High | [Impact] |

### Backend

| Fix | Title | Severity | Impact |
|-----|-------|----------|--------|
| FIX-002 | [Title] | Critical | [Impact] |
| FIX-005 | [Title] | High | [Impact] |

### Database

| Fix | Title | Severity | Impact |
|-----|-------|----------|--------|
| FIX-006 | [Title] | Medium | [Impact] |

### Integration

| Fix | Title | Severity | Impact |
|-----|-------|----------|--------|
| FIX-007 | [Title] | Medium | [Impact] |

---

## Trend Analysis

### Component Hotspots

Components with multiple fixes this month (may indicate systemic issues):

| Component | Fix Count | Trend | Action |
|-----------|-----------|-------|--------|
| [Name] | 2-3 | Increasing | Consider refactor |
| [Name] | 1-2 | Stable | Monitor |

### Category Breakdown

| Category | Count | Percentage | Notes |
|----------|-------|-----------|-------|
| Frontend | [N] | [%] | [Trend] |
| Backend | [N] | [%] | [Trend] |
| Database | [N] | [%] | [Trend] |
| Integration | [N] | [%] | [Trend] |

### Root Cause Analysis

**Most Common Root Causes This Month**:
1. [Root cause pattern]: [N] fixes - [Recommendation for prevention]
2. [Root cause pattern]: [N] fixes - [Recommendation for prevention]

---

## Recommendations for Next Month

### Prevent Recurrence

- **Action 1**: [What should we do to prevent these bugs in future]
  - Priority: [High|Medium|Low]
  - Effort: [Small|Medium|Large]
  - Impact: [Expected prevention rate]

- **Action 2**: [Another preventive action]
  - Priority: [High|Medium|Low]
  - Effort: [Small|Medium|Large]

### Areas to Monitor

- **Component**: [Why to watch this component]
- **Component**: [Why to watch this component]

### Technical Debt to Address

- [Technical debt item discovered during fixes]
  - Related fixes: [FIX-XXX]
  - Impact if not addressed: [Consequence]
  - Estimated effort: [Time to fix]

---

## Related Links

- **Previous Month**: `bug-fixes-tracking-10-25.md`
- **Next Month**: `bug-fixes-tracking-12-25.md`
- **Observation Log**: `.claude/worknotes/observations/observation-log-11-25.md`
- **Phase Progress**: `.claude/progress/[prd]/phase-N-progress.md`
