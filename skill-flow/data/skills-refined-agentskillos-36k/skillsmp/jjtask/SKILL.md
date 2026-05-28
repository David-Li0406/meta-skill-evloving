---
name: jjtask
description: Structured TODO commit workflow using JJ (Jujutsu). Use to plan tasks as empty commits with [task:*] flags, track progress through status transitions, manage parallel task DAGs with dependency checking. Enforces completion discipline. Enables to divide work between Planners and Workers.
---

<context>
Designed for JJ 0.36.x+. Uses revset aliases and templates defined in jjtask config.
</context>

<objective>
Manage a DAG of empty revisions as TODO markers representing tasks. Revision descriptions act as specifications. Two roles: Planners (create empty revisions with specs) and Workers (implement them). For JJ basics (revsets, commands, recovery), see the `/jj` skill.
</objective>

<quick_start>

```bash
# 1. Plan: Create TODO chain (parent required - ensures clean DAG)
jjtask create @ "Add user validation" "Check email format and password strength"
# Created: abc123 as child of @

jjtask create abc123 "Add validation tests" "Test valid/invalid emails and passwords"
# Created: def456 as child of abc123 -> forms chain: @ -> abc123 -> def456

# 2. Start working
jj edit abc123
jjtask flag @ wip

# ... implement validation ...

# 3. Review specs and move to next
jjtask next
# Shows current specs and available next tasks

# 4. Mark done and continue
jjtask next --mark-as done def456   # Marks abc123 done, starts def456
```
</quick_start>

<success_criteria>
- Task created with correct parent relationship
- Status flags reflect actual task state
- DAG shows clear priority (chained tasks) and parallelism (sibling tasks)
- All acceptance criteria met before marking done
- No orphaned tasks far from @
</success_criteria>

<status_flags>

| Flag              | Meaning                                      |
| ----------------- | -------------------------------------------- |
| `[task:draft]`    | Placeholder, needs full specification        |
| `[task:todo]`     | Ready to work, complete specs                |
| `[task:wip]`      | Work in progress                             |
| `[task:blocked]`  | Waiting on external dependency               |
| `[task:standby]`  | Awaits decision                              |
| `[task:untested]` | Implementation done, needs testing           |
| `[task:review]`   | Needs review                                 |
| `[task:done]`     | Complete, all acceptance criteria met        |

Progression: `draft` -> `todo` -> `wip` -> `done`

```bash
jjtask flag @ wip       # Start work
jjtask flag @ untested  # Implementation done
jjtask flag @ done      # Complete
```
</status_flags>

<description_management>

Flag changes only update status. To modify description content:

```bash
# Add completion notes when marking done
jjtask flag @ done
jj desc -r @ -m "$(jjtask show-desc @)

## Completion
- What was done
- Deviations from spec"

# Check off acceptance criteria
jjtask desc-transform @ 's/- \[ \] First criterion/- [x] First criterion/'

# Append a section
jjtask desc-transform @ 's/$/\n\n## Notes\nAdditional context here/'

# Batch update multiple tasks
jjtask batch-desc 's/old-term/new-term/g' 'tasks_todo()'
```

When to use what:
- `jjtask flag` - status only
- `jj desc -r REV -m "..."` - replace entire description
- `jjtask desc-transform` - partial find/replace with sed
- `jjtask batch-desc` - same transform across multiple tasks
</description_management>

<finding_tasks>

```bash
jjtask find             # Pending tasks with DAG structure
jjtask find todo        # Only [task:todo]
jjtask find wip         # Only [task:wip]
jjtask find done        # Only [task:done]
jjtask find all         # All tasks including done
```
</finding_tasks>

<parallel_tasks>

```bash
# Create parallel branches
jjtask parallel <parent-id> "Widget A" "Widget B" "Widget C"

# Merge point (all parents must complete)
jj new --no-edit <A-id> <B-id> <C-id> -m "[task:todo] Integration\n\n..."
```
</parallel_tasks>

<todo_description_format>

```
Short title (< 50 chars)

## Context
Why this task exists, what problem it solves.

## Requirements
- Specific requirement 1
- Specific requirement 2

## Acceptance criteria
- Criterion 1 (testable)
- Criterion 2 (testable)
```
</todo_description_format>

<completion_discipline>

Do NOT mark done unless ALL acceptance criteria are met.

Mark done when:
- Every requirement implemented
- All acceptance criteria pass
- Tests pass

Never mark done when:
- "Good enough" or "mostly works"
- Tests failing
- Partial implementation
</completion_discipline>

<anti_patterns>
<pitfall name="stop-and-report">
If you encounter these issues, STOP and report:
- Made changes in wrong revision
- Previous work needs fixes
- Uncertain about how to proceed
- Dependencies unclear

Do NOT attempt to fix using JJ operations not in this workflow.
</pitfall>
</anti_patterns>

<dag_validation>

When reviewing tasks with `jjtask find`, look for structural issues:

Good DAG - chained tasks show priority, parallel tasks are siblings:
```
o  E [todo] Feature complete   <- gate: all children done, tests pass, reviewed
|-+-,
| | o  D2 [todo] Write docs    <- parallel with D1
| o |  D1 [todo] Add tests     <- parallel with D2
|-' |
o   |  C [todo] Implement      <- after B
o  -'  B [todo] Design API     <- after A
o  A [todo] Research           <- do first
@  current work
```
Reading bottom-up: A -> B -> C -> (D1 || D2) -> E (gate)

Task E is a "gate" - marks feature complete only when all children done.

Bad DAG - all siblings, no priority visible:
```
| o  E [todo] Deploy
|-'
| o  D [todo] Write docs
|-'
| o  C [todo] Implement
|-'
| o  B [todo] Design API
|-'
| o  A [todo] Research
|-'
@  current work
```
Problem: Which task comes first? No way to tell.
Fix: Chain dependent tasks with `jj rebase -s B -o A`

Dependency problems:
- Task mentions another task but isn't a child of it -> `jj rebase -s TASK -o DEPENDENCY`
- Task requires output from another but they're siblings -> rebase to make sequential
- Keywords: "after", "requires", "depends on", "once X is done", "needs"

Parallelization opportunities:
- Sequential tasks that don't share state -> could be parallel siblings
- Independent features under same parent -> good candidates for parallel agents

Structural issues:
- Orphaned tasks far from @ -> `jjtask hoist` or manual rebase
- Done tasks with pending children -> children may be blocked
- Draft tasks mixed with todo -> drafts need specs before work begins
</dag_validation>

<hoisting>

When you make commits, tasks created earlier stay behind. Run `jjtask hoist` to move pending tasks up:

```bash
jjtask hoist
# Moves pending task roots to be children of @
```
</hoisting>

<finalizing>

```bash
# Strip [task:done] prefix for final commit
jjtask finalize @
```
</finalizing>

<commands>

| Command                             | Purpose                           |
| ----------------------------------- | --------------------------------- |
| `jjtask create PARENT TITLE [DESC]`    | Create TODO as child of PARENT    |
| `jjtask parallel PARENT T1 T2...`      | Create parallel TODOs             |
| `jjtask next [--mark-as STATUS] [REV]` | Review specs, optionally move     |
| `jjtask flag REV FLAG`                 | Update status flag                |
| `jjtask find [FLAG] [-r REVSET]`       | Find tasks (flags or custom revset)|
| `jjtask hoist`                         | Rebase pending tasks to @         |
| `jjtask finalize [REV]`                | Strip task prefix for final commit|
| `jjtask show-desc [REV]`               | Print revision description        |
| `jjtask desc-transform REV SED`        | Transform description with sed    |
| `jjtask batch-desc SED REVSET`         | Transform multiple descriptions   |
| `jjtask checkpoint [NAME]`             | Create named checkpoint           |
| `jjtask all <cmd> [args]`              | Run jj command across all repos   |
| `jjtask prime`                         | Output session context for hooks  |
| `jjtask parallel-start [--mode] TASK`  | Start parallel agent session      |
| `jjtask parallel-stop [TASK]`          | Stop parallel session             |
| `jjtask parallel-status [TASK]`        | Show parallel session status      |
| `jjtask agent-context ID`              | Get context for parallel agent    |
</commands>

<multi_repo>

Create `.jj-workspaces.yaml` in project root:

```yaml
repos:
  - path: frontend
    name: frontend
  - path: backend
    name: backend
```

Scripts show output grouped by repo. Use `jjtask all log` or `jjtask all diff` across repos.
</multi_repo>

<parallel_agents>

Multiple Claude agents can work simultaneously on the same repo.

Detecting parallel context - check `jjtask prime` output for "Parallel Session Active" section, or run:
```bash
jjtask agent-context <your-agent-id>
```

Rules for parallel work:
1. ONLY modify files in your assignment - other files belong to other agents
2. Check assignments: `jjtask parallel-status`
3. Mark your task done when complete: `jjtask flag @ done`

Shared mode (agents share @):
- Your changes appear immediately to others
- File discipline critical - stay in your assigned patterns
- Conflicts possible if patterns overlap

Workspace mode (isolated directories):
- You have your own working copy in `.jjtask-workspaces/<agent>/`
- Other agents can't affect your files
- Complete isolation until session ends

Commands:
```bash
jjtask agent-context <id>     # Your assignment and context
jjtask parallel-status        # All agents' progress
jjtask parallel-recover       # Fix workspace issues
```

See `references/parallel-agents.md` for full documentation.
</parallel_agents>

<references>
- `references/parallel-agents.md` - Multi-agent parallel execution
- `references/batch-operations.md` - Batch description transformations
- `references/command-syntax.md` - JJ command flag details
</references>
