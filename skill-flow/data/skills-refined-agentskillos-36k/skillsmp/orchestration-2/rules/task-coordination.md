---
title: Task Coordination
impact: HIGH
tags: orchestration, tasks, coordination
references:
  - https://x.com/trq212/status/2014480496013803643
---

# Claude Code Tasks Integration

Tasks are Claude Code's native primitive for tracking and coordinating work across sessions and agents.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Task List** | Collection of tasks, stored in `~/.claude/tasks/` |
| **Task List ID** | Identifier for sharing tasks (`CLAUDE_CODE_TASK_LIST_ID`) |
| **Dependencies** | Tasks can block each other via `blockedBy`/`blocks` |
| **Broadcasting** | Changes sync across sessions using same Task List |

## When to Use Tasks

| Scenario | Use Tasks? | Why |
|----------|------------|-----|
| Multi-file feature | YES | Track progress across files |
| Multi-agent swarm | YES | Coordinate parallel workers |
| Plan mode | YES | Convert plan to trackable tasks |
| Cross-session work | YES | Persist state across sessions |
| Simple single-file fix | OPTIONAL | May be overkill |

## Task Tools

```
TaskCreate   - Create new task with subject + description
TaskUpdate   - Update status, add dependencies, mark complete
TaskList     - View all tasks and their status
TaskGet      - Get full details of a specific task
```

## The Orchestration Flow with Tasks

```
1. DECOMPOSE
   ┌──────────────────────────────────────────┐
   │  User: "Add auth to the API"             │
   │                                          │
   │  TaskCreate: "Design auth approach"      │
   │  TaskCreate: "Implement JWT middleware"  │
   │  TaskCreate: "Add auth to routes"        │
   │  TaskCreate: "Write auth tests"          │
   └──────────────────────────────────────────┘

2. SET DEPENDENCIES
   ┌──────────────────────────────────────────┐
   │  TaskUpdate: "Implement JWT"             │
   │    addBlockedBy: ["Design auth"]         │
   │                                          │
   │  TaskUpdate: "Add to routes"             │
   │    addBlockedBy: ["Implement JWT"]       │
   │                                          │
   │  TaskUpdate: "Write tests"               │
   │    addBlockedBy: ["Add to routes"]       │
   └──────────────────────────────────────────┘

3. FIND READY WORK
   ┌──────────────────────────────────────────┐
   │  TaskList -> Find tasks with:            │
   │    - status: 'pending'                   │
   │    - blockedBy: [] (empty/resolved)      │
   │    - owner: null (unclaimed)             │
   └──────────────────────────────────────────┘

4. SPAWN WORKERS
   ┌──────────────────────────────────────────┐
   │  Task(subagent_type="worker", prompt=    │
   │    "TaskGet(id) for full details.        │
   │     Complete task. TaskUpdate when done."│
   │    run_in_background=True)               │
   └──────────────────────────────────────────┘

5. MARK COMPLETE
   ┌──────────────────────────────────────────┐
   │  Worker: TaskUpdate(status="completed")  │
   │                                          │
   │  Orchestrator: TaskList -> more ready?   │
   │    -> Spawn more workers                 │
   └──────────────────────────────────────────┘
```

## Cross-Session Coordination

Share tasks across Clorch sessions using environment variable:

```bash
# Terminal 1: Start with shared task list
CLAUDE_CODE_TASK_LIST_ID=myproject-feature claude

# Terminal 2: Join same task list
CLAUDE_CODE_TASK_LIST_ID=myproject-feature claude
```

Both sessions see the same tasks. Changes broadcast automatically.

## Task List ID Conventions

| Pattern | Use Case |
|---------|----------|
| `{project}-{feature}` | Feature development |
| `{project}-{date}` | Daily work session |
| `ralph-{project}` | Ralph autonomous loop |
| `plan-{plan-id}` | Plan mode implementation |

## Worker Preamble for Tasks

Include this in worker prompts:

```
TASK COORDINATION:
1. TaskGet({task_id}) for full requirements
2. Work on assigned task only
3. TaskUpdate(status="in_progress") when starting
4. TaskUpdate(status="completed") when done
5. If blocked, TaskUpdate(addBlockedBy=[blocker_id])
```

## Plan Mode → Tasks

When exiting plan mode, convert plan to tasks:

```
Plan:
1. Design database schema
2. Create models
3. Add API endpoints
4. Write tests

→ TaskCreate for each step
→ TaskUpdate to set dependencies
→ ExitPlanMode triggers swarm
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Create 50 tiny tasks | Group related work into meaningful tasks |
| Skip dependencies | Set blockedBy for sequential work |
| Forget to mark complete | Always TaskUpdate when done |
| Duplicate across sessions | Use shared Task List ID |

## Integration with Swarm Patterns

Tasks replace ad-hoc tracking in swarms:

```
OLD (without Tasks):
- Track progress mentally
- Hope agents don't duplicate work
- Manually coordinate

NEW (with Tasks):
- TaskList shows what's done/pending
- blockedBy prevents race conditions
- Workers claim tasks via owner field
```

## Monitoring Progress

```bash
# View task files directly
ls ~/.claude/tasks/

# In session
TaskList  # See all tasks
TaskGet(id)  # See specific task details
```
