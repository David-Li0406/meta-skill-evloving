---
name: jj-todo-workflow
description: Use this skill to manage a structured TODO commit workflow with JJ (Jujutsu), allowing for task planning, progress tracking, and dependency management in a directed acyclic graph (DAG) format.
---

# JJ TODO Workflow

This skill enables the management of a DAG of empty revisions as TODO markers, representing tasks to be done. Revision descriptions act as specifications for what to implement. There are two roles: **Planners** (who create empty revisions with specifications) and **Workers** (who implement them). 

## Quick Start (Planners & Workers)

Here's a complete cycle from planning to completion:

```bash
# 1. Plan: Create a simple TODO chain
jjtask create @ "Add user validation" "Check email format and password strength"
# Created: abc123 as child of @

jjtask create abc123 "Add validation tests" "Test valid/invalid emails and passwords"
# Created: def456 as child of abc123

# 2. Start working on first TODO
jj edit abc123
jjtask flag @ wip   # Now [task:wip]

# ... implement validation ...

# 3. Verify ALL acceptance criteria met
make test  # Or equivalent in your project

# 4. Ask to move to next task
jjtask next
# Review current specs and next possible TODOs

# 5. Once everything is properly done, move to next TODO
jjtask next --mark-as done def456   # Marks abc123 as [task:done], starts def456 as [task:wip]
```

## Status Flags

We use description prefixes to track status at a glance. The `[task:*]` namespace makes them greppable and avoids conflicts with other conventions.

| Flag              | Meaning                                                                              |
| ----------------- | ------------------------------------------------------------------------------------ |
| `[task:draft]`    | Placeholder created, needs full specification                                        |
| `[task:todo]`     | Not started, empty revision with complete specs                                      |
| `[task:wip]`      | Work in progress                                                                     |
| `[task:blocked]`  | Waiting on external dependency                                                       |
| `[task:standby]`  | Awaits some decision                                                                  |
| `[task:untested]` | Implementation done, but not tested enough to be validated                           |
| `[task:review]`   | Needs review (tricky code, design choice)                                            |
| `[task:done]`     | Complete, all acceptance criteria met                                                |

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

- Print out current task's description for review
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

- Supervisor Agent does the initial planning and creates the graph of TODO revisions.
- Sub-agent(s) just "run" through the graph, following the structure and requirements, implementing each revision **sequentially**.

**IMPORTANT:** Sub-agents MUST work sequentially through tasks, not in parallel.

## When to Stop and Report (Workers)

**Follow the prescribed workflow only.**
If you encounter any issues, STOP and report to the user, notably if:

- Made changes in wrong revision
- Notice that previous work needs fixes and should be amended
- Uncertain about how to proceed
- Dependencies or requirements unclear

## Tips

### Keep TODOs Small (Planners)

Each TODO should be completable in one focused session. If it's too big, split into multiple TODOs.

### Use `--no-edit` Religiously (Planners & Workers)

When creating TODOs, always use `jjtask create` or `jj new --no-edit`.

### Completion Discipline: No "Good Enough" (Workers)

**Do NOT mark a task as done unless ALL acceptance criteria are met.**

### Check Dependencies Before Starting (Workers)

If working with parallel branches or complex DAGs, check dependencies before starting on a new TODO.

## Helper Scripts (Planners & Workers)

Helper scripts in `scripts/`. Invoke with full path to avoid PATH setup.

| Script                                              | Purpose                                                     |
| --------------------------------------------------- | ----------------------------------------------------------- |
| `jjtask create <PARENT> <TITLE> [DESC]`            | Create TODO as child of PARENT                             |
| `jjtask parallel <PARENT> <T1> <T2>...`            | Create parallel TODOs                                      |
| `jjtask next [--mark-as STATUS] [REV]`             | Review specs, optionally move                              |
| `jjtask flag <REV> <TO_FLAG>`                       | Update status flag                                         |
| `jjtask find [FLAG]`                                | Find tasks (flags or custom revset)                       |

## References

Advanced topics and detailed guides:

- `references/parallel-agents.md` - Using JJ workspaces for parallel agent execution
- `references/batch-operations.md` - Batch description transformations
- `references/command-syntax.md` - JJ command flag details