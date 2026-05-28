---
name: jj-todo-workflow
description: Use this skill to manage a structured TODO commit workflow with JJ (Jujutsu), enabling task planning, progress tracking, and parallel task management through a directed acyclic graph (DAG) of empty revisions.
---

# JJ TODO Workflow

The core idea is to use a DAG of empty revisions as TODO markers, representing tasks to be done, and then come back later to edit these revisions to actually do the tasks. This enables structured development with clear milestones. Revision descriptions (i.e. commit messages) act as specifications for what to implement.

This skill involves two roles: **Planners** (who lay out the empty revisions and their specs) and **Workers** (who implement them). Depending on the situation, you may be acting as just Planner, just Worker, or both.

## Quick Start (Planners & Workers)

Here's a complete cycle from planning to completion:

```bash
# 1. Plan: Create a simple TODO chain
jjtask create @ "Add user validation" "Check email format and password strength"
# Created: abc123 (stays on current @)

jjtask create abc123 "Add validation tests" "Test valid/invalid emails and passwords"
# Created: def456 (@ still hasn't moved)

# 2. Start working on first TODO
jj edit abc123
jjtask flag @ wip   # Now [task:wip]

# ... implement validation ...

# 3. Verify ALL acceptance criteria met
make test  # Or equivalent in your project

# 4. Ask to move to next task
jjtask next
### ... review current specs (to ensure compliance) and next possible TODOs ...

# 5. Once we're sure everything is properly done, move to next TODO
jjtask next --mark-as done def456   # Marks abc123 as [task:done], starts def456 as [task:wip]
```

## Status Flags (Planners & Workers)

We use description prefixes to track status at a glance. The `[task:*]` namespace makes them greppable and avoids conflicts with other conventions.

Here are the allowed status flags:

| Flag              | Meaning                                                                              |
| ----------------- | ------------------------------------------------------------------------------------ |
| `[task:draft]`    | Placeholder created, needs full specification                                        |
| `[task:todo]`     | Not started, empty revision with complete specs                                      |
| `[task:wip]`      | Work in progress                                                                     |
| `[task:blocked]`  | Waiting on external dependency                                                       |
| `[task:standby]`  | Awaits some decision (broken and hard to fix, usefulness called into question, etc.) |
| `[task:untested]` | Implementation done, but not tested enough to be validated                           |
| `[task:review]`   | Needs review (tricky code, design choice)                                            |
| `[task:done]`     | Complete, all acceptance criteria met                                                |

### Updating Flags (Workers & Planners)

```bash
jjtask flag @ draft     # Mark as needing specification (Planners)
jjtask flag @ todo      # Mark as ready to work on (Planners)
jjtask flag @ wip       # Start work (Workers)
jjtask flag @ untested  # Implementation done, tests missing (Workers)
jjtask flag @ done      # Complete (Workers)
```

### Finding Flagged Revisions (Planners & Workers)

```bash
jjtask find             # All tasks
jjtask find draft       # Only [task:draft]
jjtask find todo        # Only [task:todo]
jjtask find wip         # Only [task:wip]
jjtask find done        # Only [task:done]
```

## Basic Workflow (Planners & Workers)

### 1. Plan: Create TODO Chain (Planners)

```bash
# Create linear chain of tasks
jjtask create @ "Task 1: Setup data model" "...details..."
jjtask create <T1-id> "Task 2: Implement core logic" "..."
jjtask create <T2-id> "Task 3: Add API endpoints" "..."
jjtask create <T3-id> "Task 4: Write tests" "..."
```

### 2. Work: Edit Each TODO (Workers)

```bash
# Read the specs
jjtask show-desc <task-id>    # Print description of a revision
 
# Start working on it
jj edit <task-id>
jjtask flag @ wip

# ... implement ...

# Mark progress
jjtask flag @ untested
```

### 3. Complete and Move to Next (Workers)

`jjtask next` script is there to smooth out the "transition to next task" process.

#### Without args

- Print out current task's description so you can review and make sure everything is implemented as planned
- Print out next possible task(s)

```bash
# Review current specs and see what's next
jjtask next
```

#### With args

- Update the flag of current task
- Move (`jj edit`) to the next task
- Update new task's flag to `[task:wip]`

```bash
# Actually mark current done and start editing next:
jjtask next --mark-as done abc123
```

## Planning Parallel Tasks (DAG) (Planners)

Create branches that can be worked independently. Example:

```bash
# Linear foundation
jjtask create @ "Task 1: Core infrastructure"
jjtask create <T1-id> "Task 2: Base components"

# Parallel branches from Task 2
jjtask parallel <T2-id> "Widget A" "Widget B" "Widget C"

# ... edit their descriptions to add more details ...

# Merge point (all three parents must complete first)
jj new --no-edit <A-id> <B-id> <C-id> -m "[task:todo] Integration of widgets\n\n..."
```

## Writing Good TODO Descriptions (Planners)

### Structure

```
Short title (< 50 chars)

## Context
Why this task exists, what problem it solves.

## Requirements
- Specific requirement 1
- Specific requirement 2

## Acceptance criteria
- Criterion 1
- Criterion 2
```

**Important:** Acceptance criteria define when you can mark as `[task:done]`. Be specific and testable.

## AI-Assisted TODO Workflow

TODOs work great with AI sub-agents:

- Supervisor Agent does the initial planning and creates the graph of TODO revisions
- Supervisor Agent ensures all `[task:draft]` tasks are filled in and marked as `[task:todo]` before workers start
- Sub-agent(s) just "run" through the graph, following the structure and requirements, implementing each revision **sequentially**

**IMPORTANT:** Sub-agents MUST work sequentially through tasks, not in parallel. Running multiple agents concurrently on the same repository causes conflicts as they fight over the working copy (`@`).

## When to Stop and Report (Workers)

**Follow the prescribed workflow only.**
If you encounter any issues, STOP and report to the user, notably if:

- Made changes in wrong revision
- Notice that previous work needs fixes and should be amended
- Uncertain about how to proceed
- Dependencies or requirements unclear

## Documenting Implementation Deviations (Workers)

When implementation differs from specs, whatever the reason DOCUMENT IT and JUSTIFY IT:

```bash
# After implementing, add notes
jj desc -r @ -m "$(jjtask show-desc @)

## Post-Implementation notes
- Used argon2 instead of bcrypt. That's because contrary to admin case, here we also needed to comply with...
```

## Tips

### Keep TODOs Small (Planners)

Each TODO should be completable in one focused session. If it's too big, split into multiple TODOs.

### Use `--no-edit` Religiously (Planners & Workers)

When creating TODOs, always use `jjtask create` or `jj new --no-edit`.

### Completion Discipline: No "Good Enough" (Workers)

**Do NOT mark a task as done unless ALL acceptance criteria are met.**

✅ **Mark as done when:**

- Every requirement implemented
- All acceptance criteria pass
- Tests pass (if applicable)
- No known issues remain

❌ **Never mark as done when:**

- "Good enough" or "mostly works"
- Tests failing
- Partial implementation

## Helper Scripts (Planners & Workers)

Helper scripts in `scripts/`. Invoke with full path to avoid PATH setup.

| Script                                              | Purpose                                                     |
| --------------------------------------------------- | ----------------------------------------------------------- |
| `jjtask create <PARENT> <TITLE> [DESC]`            | Create TODO as child of PARENT                             |
| `jjtask parallel <PARENT> <T1> <T2>...`            | Create parallel TODOs                                      |
| `jjtask next [--mark-as STATUS] [REV]`             | Review specs, check dependencies, mark & optionally move    |
| `jjtask flag <REV> <TO_FLAG>`                       | Update status flag (auto-detects current)                   |
| `jjtask find [FLAG]`                                | Find flagged revisions                                      |

## References

Advanced topics and detailed guides:

- `references/parallel-agents.md` - Using JJ workspaces for parallel agent execution (Planners)