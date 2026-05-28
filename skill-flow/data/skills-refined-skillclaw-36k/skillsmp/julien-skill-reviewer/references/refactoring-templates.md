# Refactoring Templates

## Issue Report Format

```markdown
## Issue: [Dimension] - Score X/5

**Location**: SKILL.md lines Y-Z

**Problem**: [Specific issue description]

**Example**:
[Quote the problematic section]

**Impact**: [How this affects quality]

**Suggested Fix**: [Concrete improvement]
```

## Refactoring Plan Template

```markdown
# Refactoring Plan for [skill-name]

## Current Score: X.X/5.0
## Target Score: 4.5/5.0

## Priority 1: Critical Issues (Must Fix)

### Issue 1: [Title]
- **Current State**: [Description]
- **Target State**: [What it should be]
- **Actions**:
  1. [Specific action]
  2. [Specific action]
- **Files to Create/Modify**:
  - Create: references/xxx.md
  - Modify: SKILL.md (remove duplication)
- **Expected Impact**: [Dimension] X/5 → Y/5

## Priority 2: High Impact Improvements
[...]

## Priority 3: Polish and Refinement
[...]
```

## Initial Review Report

```markdown
# Skill Review: [skill-name]

## Executive Summary

- **Overall Score**: X.X/5.0
- **Status**: [Needs rework | Functional | Good | Excellent]
- **Recommendation**: [Action needed]
- **Estimated iterations**: [X]

## Detailed Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity | X/5 | |
| Completeness | X/5 | |
| Discoverability | X/5 | |
| Context Efficiency | X/5 | |
| Actionability | X/5 | |
| Resource Organization | X/5 | |
| Examples | X/5 | |
| Skill Chaining | X/5 | |
| Error Handling | X/5 | |
| **Average** | **X.X/5** | |

## Critical Issues (Priority 1)
[List]

## Recommended Improvements (Priority 2)
[List]

## Optional Polish (Priority 3)
[List]

## Refactoring Plan
[Detailed plan]

## Next Steps
[What to do]
```

## Post-Refactoring Report

```markdown
# Re-evaluation: [skill-name]

## Before/After Comparison

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Clarity | X/5 | Y/5 | +Z |
| ... | | | |
| **Average** | X.X/5 | Y.Y/5 | +Z.Z |

## Changes Made

1. ✅ [Change description]
2. ✅ [Change description]

## Files Modified

- Modified: SKILL.md (-150 lines, +50 lines)
- Created: references/xxx.md (+200 lines)

## Quality Achievement

✅ Production threshold reached: Y.Y/5 (target: 3.5/5)

## Remaining Opportunities
[Optional improvements]
```

## User Interaction Template

```markdown
I've identified X issues with this skill (current score: Y.Y/5.0).

Would you like me to:

A) Show the detailed refactoring plan (review first)
B) Execute Priority 1 fixes automatically
C) Walk through fixes one-by-one interactively
D) Focus on a specific dimension (e.g., just DRY violations)
```

## Iteration Continuation

```markdown
Current score: 3.2/5 (below production threshold)

Critical issues remaining:
1. [Issue description]
2. [Issue description]

Would you like me to:
A) Continue with next iteration
B) Focus on specific dimension
C) Show what's blocking the score
D) Stop and review manually
```
