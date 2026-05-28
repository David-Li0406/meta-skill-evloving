---
name: jj-todo-workflow
description: Use this skill to manage tasks as empty commits in a structured workflow with JJ (Jujutsu), enabling clear planning and execution through defined roles of Planners and Workers.
---

# JJ TODO Workflow

The core idea is to use a Directed Acyclic Graph (DAG) of empty revisions as TODO markers, representing tasks to be done, and then come back later to edit these revisions to implement the tasks. This enables structured development with clear milestones, where revision descriptions act as specifications for what to implement.

**Roles:**
- **Planners**: Create empty revisions and their specifications.
- **Workers**: Implement the tasks defined in the revisions.

## Quick Start (Planners & Workers)

Here's a complete cycle from planning to completion:

```bash
# 1. Plan: Create a simple TODO chain
jjtask create @ "Add user validation" "Check email format and password strength"
# Created: abc123 as child of @

jjtask create abc123 "Add validation tests" "Test valid/invalid emails and passwords"
# Created: def456 as child of abc123

# 2. Start working on the first TODO
jj edit abc123
jjtask flag @ wip   # Now [task:wip]

# ... implement validation ...

# 3. Verify ALL acceptance criteria met
make test  # Or equivalent in your project

# 4. Review specs and move to the next task
jjtask next
# Shows current specs and available next tasks

# 5. Once everything is properly done, mark the current task as done and move to the next
jjtask next --mark-as done def456   # Marks abc123 as [task:done], starts def456 as [task:wip]
```

## Status Flags

We use description prefixes to track status at a glance. The `[task:*]` namespace makes them easily searchable.

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

**Progression**: `draft` -> `todo` -> `wip` -> `done`