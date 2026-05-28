---
name: agent-ops-focus-scan
description: Use this skill to analyze issues and identify the next work item while updating focus.md, ensuring an issue-first workflow and adhering to confidence-based batch limits.
---

# Focus Scan

## Purpose
Align session focus with the highest priority pending issue. **Enforces that all work is tracked as issues and respects confidence-based batch limits.**

## Context Optimization

**Read `index.md` first** for a quick issue overview. Only load full priority files when selecting specific issues to work on.

```
1. Read .agent/issues/index.md (compact summary)
2. Identify target priority level from index
3. Load only that priority file for full details
```

## CLI Commands

**Works with or without `aoc` CLI installed.** Focus scanning can be done via direct file reading.

### File-Based Priority Scan (Default)

```
1. Read .agent/issues/index.md (compact summary)
2. Identify target priority level from index
3. Load only that priority file for full details
4. Filter for status: todo or open
5. Select first actionable issue (respecting depends_on)
```

### Focus Update (File-Based)

1. Read current `.agent/focus.md`
2. Update "Doing now" section with the selected issue
3. Update "Next" section with the immediate step

### CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Command | Purpose |
|---------|---------|
| `aoc issues list --status todo,open --priority critical` | Find critical actionable issues |
| `aoc issues list --status todo,open --priority high` | Find high priority issues |
| `aoc issues list --status blocked` | Find blocked issues |
| `aoc issues show <ID>` | Check issue details |
| `aoc issues summary` | Quick status overview |

## Confidence-Based Batch Limits

| Confidence | Max Issues per Iteration | Rationale |
|------------|-------------------------|-----------|
| LOW | 1 (hard limit) | High uncertainty requires focused human oversight |
| NORMAL | Up to 3 | Standard workflow with reasonable batching |
| HIGH | Up to 5 | Well-understood work can be batched |

**Enforcement:**
- Read confidence from constitution or current task.
- If LOW confidence, select EXACTLY 1 issue — no batching.
- Present batch to user for confirmation if confidence is not HIGH.

## Issue-First Enforcement

Before starting any work:
1. **Check for existing issues** to ensure all tasks are tracked as issues.
2. **Prioritize based on confidence levels** to determine the appropriate number of issues to handle.