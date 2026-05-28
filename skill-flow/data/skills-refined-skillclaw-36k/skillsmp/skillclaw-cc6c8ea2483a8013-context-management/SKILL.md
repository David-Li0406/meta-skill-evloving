---
name: context-management
description: Use this skill when managing context windows, surviving compaction, and persisting state across long tasks or multiple agents.
---

# Context Management

Manage your context window, survive compaction, and persist state across turns.

<when_to_use>

- Planning long-running or multi-step tasks
- Coordinating multiple subagents
- Approaching context limits (degraded responses, repetition)
- Need to preserve state across compaction or sessions
- Orchestrating complex workflows with handoffs

NOT for: simple single-turn tasks, quick Q&A, tasks completing in one response

</when_to_use>

<problem>

Claude Code operates in a ~128K token context window that compacts automatically as it fills. When compaction happens:

**What survives**:
- Task state (full task list persists)
- Tool results (summarized)
- User messages (recent ones)
- System instructions

**What disappears**:
- Your reasoning and analysis
- Intermediate exploration results
- File contents you read (unless in tool results)
- Decisions you made but didn't record

**The consequence**: Without explicit state management, you "wake up" after compaction with amnesia — you know what to do, but not what you've done or decided.

</problem>

<tasks>

## Tasks: Your Survivable State

Tasks are not just a tracker — they're your **persistent memory layer**. Use TaskCreate, TaskUpdate, TaskList, and TaskGet to manage state that survives compaction.

### What Goes in Tasks

| Category | Example |
|----------|---------|
| Current work | `Implementing auth refresh flow` (status: in_progress) |
| Completed work | `JWT validation logic added to middleware` (status: completed) |
| Discovered work | `Handle token expiry edge case` (status: pending) |
| Key decisions | Embed in task description: "Using RS256 per security review" |
| Agent handoffs | `[reviewer] Review auth implementation` + metadata: `{agentId: "abc123"}` |
| Blockers | Create blocker task, use `blockedBy` field |

### Task Discipline

**Exactly one `in_progress`** at any time. Call `TaskUpdate` to mark `in_progress` before starting.

**Mark complete immediately**. Don't batch completions — `TaskUpdate` with `completed` as you finish.

**Include agent IDs** for resumable sessions in task metadata.

**Expand dynamically**. Add tasks as you discover work; don't forget to update the state.

</tasks>