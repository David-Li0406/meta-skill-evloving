---
name: work-breakdown
description: Break down implementation plans into schedulable bd (beads) issues with proper epics, tasks, dependencies, and estimates.
---

# Work Breakdown Skill

Break down implementation plans into bd-compatible issues. This skill produces epics, tasks, dependencies, and estimates that can be directly executed via bd commands.

## When to Invoke

- User provides an implementation plan and asks to break it down

## Workflow

### Step 1: Read the Implementation Plan

If the user references a file, read it first. Extract:
- **Objective**: What is the end goal?
- **Phases**: Are there distinct implementation phases?
- **Deliverables**: What outputs are expected?
- **Dependencies**: What depends on what?

### Step 2: Identify Epics (Work Packages)

Group work into 3-7 epics. Common patterns:
- Phase 0: Setup/Infrastructure
- Phase 1-N: Feature implementation phases
- Testing & Quality
- Documentation & Deployment

### Step 3: Decompose into Tasks

For each epic, create tasks that are:
- **30-480 minutes** (0.5-8 hours) of focused work
- **Deliverable-oriented**: produces a testable output
- **Single-responsibility**: one executor can complete it
- Ensure your tasks are aligned with the development guidelines in @docs/MAINTENANCE.md

### Step 4: Map Dependencies

Identify blocking relationships:
- Task B cannot start until Task A completes
- Epic 2 depends on Epic 1 completion
- Testing depends on implementation

### Step 5: Assign Estimates and Priorities

Use bd-compatible values:
- **Priority**: 0 (critical) to 4 (backlog)
- **Estimate**: minutes (60=1hr, 240=4hrs)
- **Type**: epic, task, feature, bug, chore

### Step 6: Present WBS for Approval

Show the user:
1. Summary table with all tasks
2. Dependency graph (text representation)
3. Parallel opportunities
4. Total effort estimate

Ask: "Ready to create these issues in beads?"

### Step 7: Execute bd Commands

After user approval, execute commands in this order:

```bash
# 1. Create epics first (capture IDs from --json output)
bd create "Epic Name" -t epic -p [priority] -e [total_minutes] -d "Description" --json

# 2. Create tasks as children of epics
bd create "Task Name" -t task -p [priority] -e [minutes] --parent [epic_id] -d "Description" --json

# 3. Add dependencies between tasks
bd dep add [dependent_id] [blocker_id]

# 4. Show ready work
bd ready
```

## Output Format

Present the WBS as a markdown table:

```markdown
## Work Breakdown: [Project Name]

### Summary
- Total: N tasks across M epics
- Effort: X-Y hours
- Critical path: Task1 -> Task2 -> Task3

### Epic 1: [Name] (P1, ~Xhr)

| ID | Task | Type | Pri | Est | Depends | Risk |
|----|------|------|-----|-----|---------|------|
| 1.1 | [Title] | task | P2 | 120m | - | Low |
| 1.2 | [Title] | task | P2 | 180m | 1.1 | Med |

### Epic 2: [Name] (P2, ~Xhr)
...
```

## bd Quick Reference

| Field | Flag | Values |
|-------|------|--------|
| type | `-t` | epic, task, feature, bug, chore |
| priority | `-p` | 0-4 (0=critical) |
| estimate | `-e` | minutes |
| parent | `--parent` | epic ID |
| description | `-d` | text |
| labels | `-l` | comma-separated |

Dependencies: `bd dep add [child] [blocker]` - child depends on blocker

## Key Rules

1. **Always get approval** before creating issues
2. **Create epics first** to get their IDs for --parent
3. **Use --json** flag to capture created issue IDs
4. **Add dependencies after** all tasks exist
5. **Run `bd ready`** at the end to show actionable work
