---
name: taskwarrior-integration
description: Use this skill when you want to enforce a complete Taskwarrior integration protocol for coding tasks, ensuring all work is tracked and managed effectively.
---

# Skill body

This skill **enforces mandatory Taskwarrior integration** for ALL coding activities. It ensures every piece of work is:

1. **Decomposed** into trackable Taskwarrior tasks BEFORE code is written.
2. **Tracked** with proper attributes (project, priority, due date, tags).
3. **Time-accounted** via automatic Timewarrior integration.
4. **Dependency-managed** for complex multi-step projects.
5. **Completed** with proper task lifecycle (add → start → done).

**CRITICAL: NO CODE IS WRITTEN until Taskwarrior tasks are created and started.**

## When This Skill Activates

Trigger this skill when you mention:
- "taskwarrior"
- "task warrior"
- "tw" (as abbreviation)
- "create a task for this"
- "track this work"
- "add to taskwarrior"
- "start a task"
- "task management"
- "time tracking"

## Complete Taskwarrior Integration Protocol

### Phase 1: Task Decomposition (MANDATORY FIRST STEP)

**Before writing ANY code**, decompose the request into Taskwarrior tasks:

**For Simple Requests (1 task):**
```bash
task add "Brief description of work" project:ProjectName priority:H/M/L due:today/tomorrow/YYYY-MM-DD +tag1 +tag2
```

**For Complex Requests (multiple tasks with dependencies):**
```bash
# Parent task
task add "Main project goal" project:ProjectName priority:H due:3days +architecture +planning

# Subtasks with dependencies
task add "Subtask 1" project:ProjectName depends:1 priority:M +implementation
task add "Subtask 2" project:ProjectName depends:2 priority:M +testing
task add "Subtask 3" project:ProjectName depends:3 priority:L +documentation
```

**Required Task Attributes:**
- **project:** Categorize the work (e.g., project:DevOps, project:WebDev).
- **priority:** H (high), M (medium), or L (low) based on urgency.
- **due:** Realistic deadline (today, tomorrow, YYYY-MM-DD, or relative like 3days).
- **tags:** At least 2 relevant tags (+feature, +bugfix, +refactor, +testing, +deployment, +security, etc.).

### Phase 2: Task Activation & Time Tracking

**After creating tasks**, activate them to start time tracking with Timewarrior.