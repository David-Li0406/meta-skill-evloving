# Session Summary Template

Use this template when generating session summaries. Copy and adapt as needed.

---

```markdown
# Session Summary: [FEATURE_NAME]

**Date:** YYYY-MM-DD HH:mm
**Session Focus:** [Brief description of what was worked on]

---

## Overview

[1-2 paragraph summary of the session's goals and outcomes]

---

## Completed Work

### [Category 1 - e.g., "Backend Changes"]
- [Specific accomplishment with context]
- [Another accomplishment]

### [Category 2 - e.g., "Frontend Updates"]
- [Specific accomplishment]
- [Another accomplishment]

### [Category 3 - e.g., "Bug Fixes"]
- [What was fixed and why]

---

## Key Files Modified

| File | Changes |
|------|---------|
| `path/to/file1.tsx` | [Brief description of changes] |
| `path/to/file2.ts` | [Brief description of changes] |
| `path/to/file3.ts` | [Brief description of changes] |

---

## Design Patterns Used

- **[Pattern Name]**: [How it was applied and why]
- **[Convention from CLAUDE.md]**: [Reference to project conventions followed]

---

## Current Plan Progress

| Task | Status | Notes |
|------|--------|-------|
| Task 1 | **COMPLETED** | [Any notes] |
| Task 2 | **COMPLETED** | [Any notes] |
| Task 3 | **PENDING** | [What remains] |

---

## Remaining Tasks / Next Steps

| Task | Priority | Notes |
|------|----------|-------|
| [Next task] | High | [Context or dependencies] |
| [Another task] | Medium | [Context] |

### Blockers or Decisions Needed
- [Any blockers discovered]
- [Decisions that need user input]

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `path/to/critical/file.tsx` | [Why this file is important] |
| `path/to/related/file.ts` | [Relationship to the work] |

---

## Session Retrospective

### Token Usage Analysis

**Estimated Total Tokens:** ~XXX,XXX tokens
**Efficiency Score:** YY/100

#### Token Breakdown:
| Category | Tokens | Percentage |
|----------|--------|------------|
| File Operations | XX,XXX | XX% |
| Code Generation | XX,XXX | XX% |
| Planning/Design | XX,XXX | XX% |
| Explanations | XX,XXX | XX% |
| Search Operations | X,XXX | X% |

#### Optimization Opportunities:

1. ⚠️ **[Issue Type]**: [Specific description]
   - Current approach: [What was done]
   - Better approach: [Recommendation]
   - Potential savings: ~XXX tokens

2. ⚠️ **[Issue Type]**: [Specific description]
   - Current approach: [What was done]
   - Better approach: [Recommendation]
   - Potential savings: ~XXX tokens

[Continue for top 5 most impactful opportunities]

#### Good Practices:

1. ✅ **[Practice]**: [What worked well and why]
2. ✅ **[Practice]**: [What worked well and why]

[Note 2-3 notable good practices observed]

### Command Accuracy Analysis

**Total Commands:** XXX
**Success Rate:** YY.Y%
**Failed Commands:** ZZ (Z.Z%)

#### Failure Breakdown:
| Error Type | Count | Percentage |
|------------|-------|------------|
| Path errors | X | XX% |
| Syntax errors | X | XX% |
| Permission errors | X | XX% |
| Logic errors | X | XX% |

#### Recurring Issues:

1. ⚠️ **[Error Type]** (X occurrences)
   - Root cause: [Why this happened]
   - Example: [Specific instance from session]
   - Prevention: [How to avoid in future]
   - Impact: [Severity level and consequences]

2. ⚠️ **[Error Type]** (X occurrences)
   - Root cause: [Analysis of root cause]
   - Example: [Instance]
   - Prevention: [Strategy]
   - Impact: [Severity]

[Continue for top 3 most important recurring issues]

#### Improvements from Previous Sessions:

1. ✅ **[Improvement]**: [What was learned/applied from past sessions]
2. ✅ **[Improvement]**: [Pattern that worked well]

[Note improvements and good patterns observed]

---

## Lessons Learned

### What Worked Well
- [Efficient pattern or approach that saved time/tokens]
- [Good decision that prevented errors]
- [Effective tool or technique used]

### What Could Be Improved
- [Pattern to avoid next time]
- [Alternative approach to consider]
- [Verification step to add]

### Action Items for Next Session
- [ ] [Specific improvement to implement]
- [ ] [Pattern to remember]
- [ ] [Tool usage adjustment]
- [ ] [Verification checklist item]

---

## Resume Prompt

```
Resume [FEATURE_NAME] session.

## Context
Previous session completed:
- [Key accomplishment 1]
- [Key accomplishment 2]
- [Key accomplishment 3]

Session summary: .claude/summaries/MM-DD-YYYY/YYYYMMDD-HHmm_feature-name.md

## Key Files to Review First
- path/to/main/file.tsx (primary changes)
- path/to/related/file.ts (supporting changes)

## Current Status
[Brief status statement]

## Next Steps
1. [Immediate next task]
2. [Following task]
3. [Third task]

## Important Notes
- [Any critical context]
- [Environment setup if needed]
```

---

## Notes

- [Any additional context for future reference]
- [Lessons learned or patterns discovered]
```

---

## Template Usage Tips

1. **File Naming**: `.claude/summaries/MM-DD-YYYY/YYYYMMDD-HHmm_feature-name.md`
   - Example: `.claude/summaries/01-05-2026/20260105-1430_phase1-foundation.md`
2. **Feature Name**: Use kebab-case for the filename (e.g., `enrollment-improvements`)
3. **Completed Work**: Group by category for easier scanning
4. **Files Table**: Include only files with significant changes
5. **Resume Prompt**: Make it copy-paste ready for the next session
6. **Status**: Use bold for emphasis (COMPLETED, PENDING, IN_PROGRESS)
