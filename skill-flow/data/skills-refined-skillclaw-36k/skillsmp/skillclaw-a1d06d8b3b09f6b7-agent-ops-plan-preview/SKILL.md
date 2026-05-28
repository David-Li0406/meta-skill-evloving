---
name: agent-ops-plan-preview
description: Use this skill to transform implementation plans into concise, stakeholder-friendly summaries, including file change overviews and component listings.
---

# Plan Preview Workflow

## Purpose

Generate concise, stakeholder-ready summaries from detailed implementation plans. This skill enables developers, tech leads, and project owners to understand and approve planned changes without reviewing full technical details.

## Input Sources

Accept plans from one of the following sources:

| Source | Format | Example |
|--------|--------|---------|
| Issue ID | `{TYPE}-{NUMBER}@{HASH}` | `PLAN-0295@a1b2c3` |
| File path | Absolute or relative path | `.agent/issues/references/PLAN-0295@a1b2c3-plan.md` |
| Current context | Plan in conversation | (no argument needed) |

**Resolution order**:
1. If an issue ID is provided → resolve to `.agent/issues/references/{id}-plan.md`
2. If a file path is provided → read directly
3. If neither → check if the plan exists in the current conversation context

## Procedure

### Step 1: Resolve Input

```
IF issue_id provided:
    path = .agent/issues/references/{issue_id}-plan.md
    IF NOT exists(path):
        ERROR "Plan file not found for issue {issue_id}"
ELSE IF file_path provided:
    path = file_path
ELSE:
    Scan conversation context for plan content
```

### Step 2: Language Selection

**Ask user** (one question):

> "What language should the summary be in? (default: English)"

Common choices:
- English (default)
- Norwegian (Norsk)
- Other (specify)

**Wait for response before proceeding.**

### Step 3: Confidence Level Selection

**Ask user** (one question):

> "What confidence level is this plan? This affects detail level in the summary:
> - **LOW** — More details, explicit changes, method signatures
> - **NORMAL** — Balanced overview (default)
> - **HIGH** — Sparse, broad outlines only"

**Wait for response before proceeding.**

### Step 4: Extract Plan Elements

Parse the implementation plan and extract elements **based on confidence level**:

#### Detail Level by Confidence

| Element | LOW Confidence | NORMAL Confidence | HIGH Confidence |
|---------|----------------|-------------------|-----------------|
| **Objective** | 2-3 sentences with context | 1-2 sentences | 1 sentence |
| **Approach** | 5-7 sentences, edge cases noted | 2-3 sentences | 1 sentence max |
| **Files** | Full paths + line estimates + change summaries | File names only | File names only |

### Step 5: Generate Summary

Compile the extracted elements into a concise summary tailored to the selected language and confidence level. Include optional flow diagrams if applicable.

### Step 6: Output Summary

Present the final summary to the user for review and approval.