---
name: task-tracker
description: Use this skill for personal task management, including daily standups and weekly reviews, to track both work and personal tasks effectively.
---

# Skill body

## What This Skill Does

1. **Lists tasks** - Shows what's on your plate, filtered by priority, status, or deadline.
2. **Daily standup** - Displays today's #1 priority, blockers, and what was completed (supports both Work and Personal tasks).
3. **Weekly review** - Summarizes last week, archives completed items, and plans for the upcoming week.
4. **Add tasks** - Create new tasks with specified priority and due date.
5. **Complete tasks** - Mark tasks as done.
6. **Extract from notes** - Pull action items from meeting notes.
7. **Dual support** - Manage separate workflows for Work and Personal tasks.

## File Structure

```
~/clawd/memory/work/
├── TASKS.md              # Active tasks (source of truth)
├── ARCHIVE-2026-Q1.md    # Completed tasks by quarter
└── WORKFLOW.md           # Workflow documentation
```

**TASKS.md format:**
```markdown
# Work Tasks

## 🔴 High Priority (This Week)
- [ ] **Set up Apollo.io** — Access for Lilla
  - Due: ASAP
  - Blocks: Lilla (podcast outreach)

## 🟡 Medium Priority (This Week)
- [ ] **Review newsletter concept** — Fi
```

## Configuration

Configure paths via environment variables in your shell profile or `.clawdbot/.env`:

```bash
# Required: Point to your task files
export TASK_TRACKER_WORK_FILE="$HOME/Obsidian/03-Areas/Work/Work Tasks.md"
export TASK_TRACKER_PERSONAL_FILE="$HOME/Obsidian/03-Areas/Personal/Personal Tasks.md"
```