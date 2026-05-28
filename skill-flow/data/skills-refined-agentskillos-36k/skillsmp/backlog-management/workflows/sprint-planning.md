# Sprint Planning Workflow

## When to Use

Use this workflow when:
- Starting a new sprint
- Reviewing sprint progress
- Closing out a completed sprint

---

## Planning a New Sprint

### 1. Review Available Items

```bash
# Best: Get ALL plannable items sorted by priority
python .claude/plans/backlog/scripts/queries.py ready

# Or query by specific priority:
python .claude/plans/backlog/scripts/queries.py priority critical --status pending
python .claude/plans/backlog/scripts/queries.py priority high --status pending
python .claude/plans/backlog/scripts/queries.py priority medium --status pending
python .claude/plans/backlog/scripts/queries.py priority low --status pending

# Check blocked items
python .claude/plans/backlog/scripts/queries.py status blocked -v
```

**Priority Selection Guidelines:**
| Priority | When to Include |
|----------|-----------------|
| Critical | Always - these block production readiness |
| High | Usually - important features/fixes |
| Medium | Often - good for filling out sprints, quick wins |
| Low | Sometimes - bundle with related work, polish sprints |

### 2. Determine Sprint ID

```bash
# Find last sprint
tail -3 .claude/plans/backlog/data/sprints.csv
```

### 3. Create Sprint Plan File

Create `.claude/plans/sprints/SPRINT-XXX-name.md`:

```markdown
# SPRINT-XXX: Sprint Name

## Sprint Goal
What's the main objective?

## Planned Items
| ID | Title | Est. Tokens |
|----|-------|-------------|
| BACKLOG-YYY | Title 1 | ~20K |
| BACKLOG-ZZZ | Title 2 | ~15K |

**Total Estimate:** ~35K tokens

## Tasks
- [ ] TASK-YYY-1: First task
- [ ] TASK-YYY-2: Second task

## Dependencies
List any external dependencies or blockers.

## Risks
Potential issues to watch for.
```

### 4. Update sprints.csv

Add the new sprint:

```csv
SPRINT-XXX,Sprint Name,planning,
```

### 5. Assign Items to Sprint

Update backlog.csv to assign items:

```csv
BACKLOG-YYY,Title,category,priority,in-progress,SPRINT-XXX,~20K,-,-,[BACKLOG-YYY.md]
```

### 6. Log Sprint Start

Add to changelog.csv:

```csv
2026-01-17,assign,Started SPRINT-XXX with 3 items,BACKLOG-YYY;BACKLOG-ZZZ
```

---

## During Sprint

### Track Progress

```bash
# Check sprint items
python .claude/plans/backlog/scripts/queries.py sprint SPRINT-XXX -v
```

### Update Status

As items progress, update backlog.csv:
- `pending` → `in-progress` when work starts
- `in-progress` → `completed` when done
- `in-progress` → `blocked` if stuck

---

## Closing a Sprint

### 1. Verify All Items

```bash
# Check if any items still in progress
python .claude/plans/backlog/scripts/queries.py sprint SPRINT-XXX -v | grep -i "in.progress"
```

### 2. Update Sprint Status

In sprints.csv, change status and add completion summary:

```csv
SPRINT-XXX,Sprint Name,completed,"BACKLOG-YYY, BACKLOG-ZZZ (2 items, PRs #123-125)"
```

### 3. Update Sprint Plan File

Add completion notes:

```markdown
## Completion Summary
- **Status:** Completed
- **Items:** 2/2 completed
- **PRs:** #123, #124, #125
- **Total Tokens:** 38K (vs 35K estimate, +9%)

## Retrospective
What went well, what could improve.
```

### 4. Log Completion

```csv
2026-01-17,complete,Completed SPRINT-XXX (2 items),BACKLOG-YYY;BACKLOG-ZZZ
```

---

## Sprint Velocity Reference

Check historical data for planning:

```bash
python .claude/plans/backlog/scripts/queries.py stats
```

Typical sprint sizes:
- **Small sprint:** 2-3 items, ~30-50K tokens
- **Medium sprint:** 4-6 items, ~50-100K tokens
- **Large sprint:** 7+ items, ~100K+ tokens

---

## Merge Safety Rules

From PM guidelines:
1. **One feature per PR** - Don't bundle unrelated changes
2. **Tests before merge** - CI must pass
3. **No direct commits** - All work through branches
4. **Review required** - SR Engineer approval for significant PRs
