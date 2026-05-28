# Report Structure

```markdown
# Implementation Fidelity Review

**Spec:** {spec-title} ({spec-id})
**Scope:** {review-scope}
**Date:** {review-date}

## Summary

- **Tasks Reviewed:** {count}
- **Files Analyzed:** {count}
- **Overall Fidelity:** {percentage}%
- **Deviations Found:** {count}

## Fidelity Score

- Exact Matches: {count} tasks
- Minor Deviations: {count} tasks
- Major Deviations: {count} tasks
- Missing Functionality: {count} items

## Detailed Findings

### Task: {task-id} - {task-title}

**Specified:**
- {requirement-1}
- {requirement-2}

**Implemented:**
- {actual-1}
- {actual-2}

**Assessment:** {exact-match|minor-deviation|major-deviation}

**Deviations:**
1. {deviation-description}
   - **Impact:** {low|medium|high}
   - **Recommendation:** {action}

## Recommendations

1. {recommendation-1}
2. {recommendation-2}

## Journal Analysis

**Documented Deviations:**
- {task-id}: {deviation-summary} (from journal on {date})

**Undocumented Deviations:**
- {task-id}: {deviation-summary} (should be journaled)
```
