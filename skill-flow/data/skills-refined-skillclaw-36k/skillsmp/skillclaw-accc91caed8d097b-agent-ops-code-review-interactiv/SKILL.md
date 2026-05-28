---
name: agent-ops-code-review-interactive
description: Use this skill when you need a structured workflow for conducting interactive code reviews on agent iterations, capturing comments, and tracking their resolution status.
---

# Interactive Code Review Skill

## Purpose

Provide a structured code review workflow after agent implementation iterations. This skill allows capturing comments with categories and tracking resolution status.

## Storage Format

Reviews are stored in `.agent/reviews/`:

```
.agent/reviews/
├── YYYY-MM-DD-<short_hash>.md    # Review for specific commit
├── active-review.md               # Currently open review
└── README.md                      # Review folder documentation
```

## Review Document Format

```markdown
# Code Review: <commit_hash>

**Date**: YYYY-MM-DD HH:MM  
**Author**: [user|agent]  
**Commit**: <full_hash>  
**Branch**: <branch_name>  

## Summary

<brief description of changes reviewed>

## Changed Files

| File | Lines Changed | Status |
|------|---------------|--------|
| src/foo.py | +15 -3 | reviewed |
| tests/test_foo.py | +25 | pending |

## Comments

### [CATEGORY] File:Line — Comment Title

**File**: `path/to/file.py`  
**Line**: 42-45  
**Category**: fix | question | suggestion | concern | praise  
**Status**: open | addressed | wont_fix | deferred  
**Priority**: critical | high | normal | low  

<comment body>

#### Response (if any)

<agent or user response>

---

### [SUGGESTION] src/utils.py:78 — Consider extracting helper

**File**: `src/utils.py`  
**Line**: 78  
**Category**: suggestion  
**Status**: addressed  
**Priority**: normal  

This block of code appears in multiple places. Consider extracting to a helper function.

#### Response

Extracted to `_format_output()` helper in commit abc123.

---

## Metrics

- Total Comments: X
- Open: X
- Addressed: X
- Won't Fix: X
- Deferred: X
```

## Comment Categories

| Category | Icon | Use For |
|----------|------|---------|
| `fix` | 🔧 | Required changes, bugs, errors |
| `question` | ❓ | Clarification needed |
| `suggestion` | 💡 | Optional improvements |
| `concern` | ⚠️ | Potential issues, risks |
| `praise` | 👍 | Good patterns, well done |

## Status Transitions

```
open → addressed    (when fix is committed)
open → wont_fix     (when decided not to fix with reason)
open → deferred     (when moved to future work)
```