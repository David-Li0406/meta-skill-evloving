---
name: task-tracker
description: Use this skill for personal task management with daily standups and weekly reviews, supporting both work and personal tasks.
---

# Task Tracker

A personal task management skill for daily standups and weekly reviews. Tracks work and personal tasks, surfaces priorities, and manages blockers.

---

## What This Skill Does

1. **Lists tasks** - Shows what's on your plate, filtered by priority, status, or deadline.
2. **Daily standup** - Shows today's #1 priority, blockers, and what was completed (Work & Personal).
3. **Weekly review** - Summarizes last week, archives done items, plans this week.
4. **Add tasks** - Create new tasks with priority and due date.
5. **Complete tasks** - Mark tasks as done.
6. **Extract from notes** - Pull action items from meeting notes.
7. **Dual support** - Separate workflows for Work and Personal tasks.

---

## Configuration

Configure paths via environment variables in your shell profile or `.clawdbot/.env`:

```bash
# Required: Point to your task files
export TASK_TRACKER_WORK_FILE="$HOME/Obsidian/03-Areas/Work/Work Tasks.md"
export TASK_TRACKER_PERSONAL_FILE="$HOME/Obsidian/03-Areas/Personal/Personal Tasks.md"

# Optional: Custom archive location
export TASK_TRACKER_ARCHIVE_DIR="$HOME/clawd/memory/work"

# Optional: Legacy fallback (if Obsidian files don't exist)
export TASK_TRACKER_LEGACY_FILE="$HOME/clawd/memory/work/TASKS.md"
```

**Default paths (if not configured):**
- Work: `~/Obsidian/03-Areas/Work/Work Tasks.md`
- Personal: `~/Obsidian/03-Areas/Personal/Personal Tasks.md`
- Legacy: `~/clawd/memory/work/TASKS.md`

---

## Task Format

Tasks use the **emoji date format** for compatibility:

```markdown
- [ ] **Task name** 🗓️2026-01-22 area:: Sales
  - Additional notes here
```

### File Structure (Eisenhower Matrix)

```markdown
# Work Tasks

## 🔴 Q1: Do Now (Urgent & Important)
- [ ] **Critical task** 🗓️2026-01-22 area:: Operations

## 🟡 Q2: Schedule (Important, Not Urgent)
- [ ] **Strategic task** 🗓️2026-01-26 area:: Planning

## 🟠 Q3: Waiting (Blocked on External)
- [ ] **Blocked task** owner:: Sarah

## 👥 Team Tasks (Monitor/Check-in)
- [ ] **Team member's task** owner:: Alex

## ⚪ Q4: Backlog (Someday/Maybe)
- [ ] **Future idea**

## ✅ Done
- [x] **Completed task** (Jan 22)
```

### Personal Tasks Structure

```markdown
# Personal Tasks

## 🔴 Must Do Today
- [ ] **Urgent personal task** 🗓️2026-01-22

## 🟡 Should Do This Week
- [ ] **Important task** 🗓️2026-01-26

## 🟠 Waiting On
- [ ] **Waiting for response**

## ⚪ Backlog
- [ ] **Someday task**

## ✅ Done
- [x] **Completed** (Jan 22)
```

---

## Quick Start

### List Work Tasks
```bash
python3 scripts/tasks.py list
```

### List Personal Tasks
```bash
python3 scripts/tasks.py --personal list
```

### Daily Standup
```bash
# Work standup
python3 scripts/standup.py

# Personal standup
python3 scripts/personal_standup.py
```

### Weekly Review
```bash
python3 scripts/weekly_review.py
```

---

## Commands Reference

### List Tasks
```bash
# All tasks
tasks.py list
tasks.py --personal list

# Only high priority
tasks.py list --priority high
tasks.py --personal list --priority high

# Due today or this week
tasks.py list --due today
tasks.py list --due this-week
```

### Add Task
```bash
# Work task
tasks.py add "Draft project proposal" --priority high --due 2026-01-23

# Personal task
tasks.py --personal add "Call mom" --priority high --due 2026-01-22
```

### Complete Task
```bash
tasks.py done "proposal"  # Fuzzy match - finds "Draft project proposal"
tasks.py --personal done "call mom"
```

### Show Blockers
```bash
tasks.py blockers              # All blocking tasks
tasks.py blockers --person sarah  # Only blocking Sarah
```

### Extract from Meeting Notes
```bash
extract_tasks.py --from-text "Meeting: discuss Q1 planning, Sarah to own budget review"
```

---

## Priority Levels

| Icon | Meaning | When to Use |
|------|---------|-------------|
| 🔴 **High** | Critical, blocking, deadline-driven | Revenue impact, blocking others |
| 🟡 **Medium** | Important but not urgent | Reviews, feedback, planning |
| 🟠 **Waiting** | Blocked on external | Tasks waiting on others |
| 👥 **Team** | Monitor team tasks | Delegated, check-in only |
| ⚪ **Backlog** | Someday/maybe | Low priority |

---

## Automation (Cron)

Set up cron jobs for automated standups:

| Job | Schedule | Command |
|-----|----------|---------|
| Daily Work Standup | Weekdays 8:30 AM | `python3 scripts/standup.py` |
| Daily Personal Standup | Daily 8:00 AM | `python3 scripts/personal_standup.py` |
| Weekly Review | Mondays 9:00 AM | `python3 scripts/weekly_review.py` |

---

## Natural Language Triggers

| You Say | Skill Does |
|---------|-----------|
| "daily standup" | Runs work standup |
| "personal standup" | Runs personal standup |
| "weekly review" | Runs weekly review |
| "what's on my plate?" | Lists all work tasks |
| "personal tasks" | Lists all personal tasks |
| "what's blocking Sarah?" | Shows tasks blocking Sarah |
| "mark proposal done" | Completes matching work task |
| "add task: X" | Adds work task X |
| "add personal task: X" | Adds personal task X |

---

## Troubleshooting

**"Tasks file not found"**
```bash
# Configure your paths
export TASK_TRACKER_WORK_FILE="$HOME/path/to/Work Tasks.md"
export TASK_TRACKER_PERSONAL_FILE="$HOME/path/to/Personal Tasks.md"
```

**Tasks not showing up**
- Check task format uses `- [ ] **Task name**`
- Verify section headers start with emoji: `## 🔴`, `## 🟡`, etc.
- Run `tasks.py list` to debug parsing

---

## Files

| File | Purpose |
|------|---------|
| `scripts/tasks.py` | Main CLI - list, add, done, blockers (supports --personal) |
| `scripts/standup.py` | Work daily standup generator |
| `scripts/personal_standup.py` | Personal daily standup generator |
| `scripts/weekly_review.py` | Weekly review generator |
| `scripts/extract_tasks.py` | Extract tasks from meeting notes |
| `scripts/utils.py` | Shared utilities |
| `assets/templates/` | Template task files |