---
description: Generate weekly or monthly session summaries from retrospectives and activity logs
---

# Summary - Session Summaries

Generate weekly or monthly summaries from retrospectives, learnings, and activity logs.

## Usage

```
/summary weekly          # Generate current week summary
/summary monthly         # Generate current month summary
/summary weekly 2026-01  # Generate for specific week/month
```

**Output:** `$PROJECT_ROOT/docs/summaries/YYYY-MM-weekN.md` or `YYYY-MM.md`

## Instructions

### 1. Determine Period

Parse arguments:
- `weekly` → current week (Mon-Sun)
- `monthly` → current month
- Optional date parameter for historical summaries

```bash
export TZ='Asia/Bangkok'
YEAR=$(date '+%Y')
MONTH=$(date '+%m')
WEEK=$(date '+%V')
```

### 2. Gather Data

```bash
export TZ='Asia/Bangkok'

# Activity log entries for the period
grep "^$YEAR-$MONTH" docs/logs/activity.log

# Retrospectives for the period
find docs/retrospective/$YEAR-$MONTH -name "*.md" -type f | sort

# Learnings for the period
find docs/learnings/$YEAR-$MONTH -name "*.md" -type f | sort

# Git commits for the period
git log --oneline --since="[start-date]" --until="[end-date]"

# Knowledge base updates
git log --oneline --since="[start-date]" --until="[end-date]" -- docs/knowledge-base/
```

### 3. Analyze and Generate

Read each retrospective/learning file and extract:
- Task descriptions
- Types (feature, bugfix, refactor, etc.)
- Key decisions
- Open items (unchecked checkboxes)

### 4. Create Summary File

Use the template below.

### 5. Commit

```bash
git add docs/summaries/
git commit -m "docs: [weekly|monthly] summary for [period]"
```

## Weekly Template

```markdown
# Week [N] Summary ([start-date] - [end-date])

## Overview

| Metric | Value |
|--------|-------|
| Sessions | [count] |
| Issues Closed | [count] |
| PRs Merged | [count] |
| Learnings Captured | [count] |

## Sessions

| Date | Task | Type | Status | Issue |
|------|------|------|--------|-------|
| MM-DD | [task description] | feat/fix/refactor | completed/pending | #N |

## Key Accomplishments

- [accomplishment 1]
- [accomplishment 2]

## Learnings Captured

- `docs/learnings/[path]` - [title]

## Knowledge Distilled

- `docs/knowledge-base/[topic].md` - [title]

## Decisions Made

| Decision | Context | Rationale |
|----------|---------|-----------|
| [decision] | [context] | [rationale] |

## Open Items

- [ ] [carried over items from retrospectives]

## Next Week Focus

- [suggested focus areas based on open items]
```

## Monthly Template

```markdown
# [Month Year] Summary

## Overview

| Metric | Value |
|--------|-------|
| Total Sessions | [count] |
| Issues Closed | [count] |
| PRs Merged | [count] |
| Learnings | [count] |
| Knowledge Base Updates | [count] |

## Weekly Breakdown

| Week | Sessions | Key Focus |
|------|----------|-----------|
| W1 | [count] | [focus] |
| W2 | [count] | [focus] |
| W3 | [count] | [focus] |
| W4 | [count] | [focus] |

## Top Accomplishments

1. [accomplishment]
2. [accomplishment]
3. [accomplishment]

## Patterns & Trends

- [observed pattern in work]
- [recurring themes]

## Open Items Carried Over

- [ ] [items still pending]

## Next Month Priorities

- [priority 1]
- [priority 2]
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/td` | Create retrospective (data source) |
| `/mem` | Capture learnings (data source) |
| `/consolidate` | Consolidate auto-captured files |
| `/summary` | Generate summaries (you are here) |
