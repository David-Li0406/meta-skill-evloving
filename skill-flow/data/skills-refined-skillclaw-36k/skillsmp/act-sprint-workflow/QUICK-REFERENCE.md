# ACT Sprint Workflow - Quick Reference

## Commands Cheat Sheet

```bash
/sprint-workflow plan      # Sprint planning
/sprint-workflow today     # Daily standup
/sprint-workflow health    # System health check
/sprint-workflow create <title>  # Create issue
```

## Sprint Planning

**Command**: `/sprint-workflow plan`

**Shows**:
- Historical velocity (last 3 sprints)
- Backlog summary by priority
- Recommended issues for next sprint
- Breakdown by type/project/repo

**Use when**: Planning next sprint, reviewing capacity

---

## Daily Standup

**Command**: `/sprint-workflow today` or `/sprint-workflow standup`

**Shows**:
- Yesterday's commits and closed issues
- Today's assigned tasks
- Sprint progress %
- Recent deployments
- Blockers

**Use when**: Starting your work day, before team standup

---

## Health Check

**Command**: `/sprint-workflow health`

**Shows**:
- 6 projects × 4 health indicators
- Deployment age warnings
- HTTP/Database/Registry status
- Overall health score

**Use when**: Before deploys, troubleshooting, weekly reviews

---

## Issue Creation

**Command**: `/sprint-workflow create <title>`

**Auto-detects**:
- Type (Enhancement/Bug/Task from keywords)
- Priority (Critical/High/Medium/Low from keywords)
- Effort (S/M/L/XL from complexity)
- ACT Project (from current directory or keywords)
- Sprint (current sprint or Backlog)

**Type Keywords**:
- Enhancement: "Add", "Create", "Build", "Implement"
- Bug: "Fix", "Resolve", "Correct"
- Task: "Document", "Research", "Update"

**Priority Keywords**:
- Critical: "Critical", "Urgent", "Security", "Broken"
- High: "Important", "Should"
- Low: "Nice to have", "Eventually"

**Use when**: Creating issues quickly without manual field entry

---

## Conversational Triggers

Don't need to use `/sprint-workflow` explicitly:

| Say this | Triggers |
|----------|----------|
| "What should I work on today?" | Standup report |
| "How's our velocity?" | Sprint planning |
| "Are the sites healthy?" | Health check |
| "Create issue for..." | Issue automation |

---

## Dashboard URLs

- Main: http://localhost:3001/admin/dashboard
- Sprint Analytics: http://localhost:3001/admin/dashboard#sprint
- Health Matrix: http://localhost:3001/admin/dashboard#health

---

## Data Sources

| Source | What It Provides |
|--------|------------------|
| GitHub Projects API | Issues, sprints, field values |
| `/api/dashboard/velocity` | Historical sprint velocity |
| `/api/dashboard/sprint` | Current sprint progress |
| `/api/dashboard/health-matrix` | System health status |
| Git log | Recent commits, closed issues |
| Supabase `sprint_snapshots` | Daily progress data |

---

## Tips

✅ Run `/sprint-workflow today` every morning
✅ Run `/sprint-workflow plan` on Mondays
✅ Run `/sprint-workflow health` before deploys
✅ Use natural language - skill auto-detects intent

❌ Don't manually assign all issue fields
❌ Don't skip health checks before deployments
❌ Don't ignore velocity trends in planning
