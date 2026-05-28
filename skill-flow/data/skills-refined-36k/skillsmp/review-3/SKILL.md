---
name: review
description: Daily and weekly review workflows. USE WHEN user says "morning routine", "evening routine", "weekly review", "start my day", "end of day".
---

# Review Skill

Morning, evening, and weekly review workflows.

## Routing

| User says | Workflow |
|-----------|----------|
| "morning routine", "start my morning" | `workflows/morning.md` |
| "evening routine", "end of day" | `workflows/evening.md` |
| "weekly review" | `workflows/weekly.md` |

## Templates

| Review | Template |
|--------|----------|
| Morning | `templates/morning-checkin.md` |
| Evening | `templates/evening-checkin.md` |
| Weekly | `templates/weekly-review.md` |

## Data Access

**Projects:**
```bash
ls Projects/*.md
cat "Projects/Project Name.md"
```

**Tasks:**
```bash
curl "http://127.0.0.1:8090/api/tasks"
curl "http://127.0.0.1:8090/api/tasks?status=in-progress"
```

**Recent daily notes:**
```bash
ls -t Daily/*.md | head -5
```
