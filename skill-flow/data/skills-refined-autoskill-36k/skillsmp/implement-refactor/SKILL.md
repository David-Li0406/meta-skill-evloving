---
name: implement-refactor
description: 'Execute refactoring tasks from a task file with parallel agent orchestration'
argument-hint: <plugin-slug or task-file-path>
---

# Implement Refactor

This command continues from `/plugin-refactor:assessorin-for-refactor`. After planning completes, use this to execute the refactoring tasks.

<refactor_input>
$ARGUMENTS
</refactor_input>

---

## Resolve Task File

If `$1` is:

- A `.md` path: Use directly
- A slug (e.g., `python3-development`): GLOB for `.claude/plan/tasks-refactor-{slug}.md`

---

## Load and Analyze

### 1. Read Task File

READ the task file completely. Extract:

- All tasks with ID, name, status, dependencies, priority, **Agent**
- Design spec path (from header or linked file)
- Parallelization information

**IMPORTANT**: Each task specifies its assigned **Agent** field. Use this to route to the correct specialized agent during execution.

### 2. Read Design Spec

The task file links to its design spec (e.g., `refactor-design-{slug}.md`). READ it to understand the overall refactoring plan.

### 3. Build Dependency Graph

Identify:

- **Ready tasks**: Status `❌ NOT STARTED` with all dependencies `✅ COMPLETE` or "None"
- **Blocked tasks**: Have incomplete dependencies
- **Parallel groups**: Tasks that can run together (from "Can Parallelize With" field)

### 4. Create Progress Todos

```
TodoWrite(todos=[
    {"content": "Task {ID}: {Name}", "status": "pending", "activeForm": "Implementing {Name}"},
    ... for each task ...
    {"content": "Final: Verify refactoring complete", "status": "pending", "activeForm": "Verifying completion"}
])
```

---

## Execute Tasks

### Agent Routing Strategy

Route each task to the appropriate specialized agent based on the **Agent** field in the task:

| Issue Type     | Agent                            | When to Use                                            |
| -------------- | -------------------------------- | ------------------------------------------------------ |
| SKILL_SPLIT    | `plugin-refactor:refactor-skill` | Tasks splitting large skills into smaller focused ones |
| AGENT_OPTIMIZE | `subagent-refactorer`            | Tasks improving agent prompts and descriptions         |
| DOC_IMPROVE    | `claude-context-optimizer`       | Tasks improving skill/agent documentation quality      |
| ORPHAN_RESOLVE | `claude-context-optimizer`       | Tasks integrating orphaned reference files             |
| STRUCTURE_FIX  | `claude-context-optimizer`       | Tasks fixing broken links or structural issues         |
| Validation     | `plugin-assessor`                | Post-refactoring validation tasks                      |
| Documentation  | `plugin-docs-writer`             | README and documentation generation tasks              |

### Launch Strategy

For each ready task, READ the **Agent** field from the task and launch that agent:

```
Task(
    subagent_type="{task.agent}",  # From task's **Agent** field
    description="Task {ID}: {Name}",
    prompt="/start-refactor-task {task_file_path} --task {task_id}"
)
```

**Parallel execution**: If multiple tasks can parallelize, launch them in a SINGLE message with multiple Task calls.

**Example parallel launch**:

```
# Launch skill split tasks in parallel (no shared files)
Task(
    subagent_type="plugin-refactor:refactor-skill",
    description="Task 1: Split python3 core skill",
    prompt="/start-refactor-task .claude/plan/tasks-refactor-python3-development.md --task 1"
)
Task(
    subagent_type="subagent-refactorer",
    description="Task 2: Optimize python-cli-architect agent",
    prompt="/start-refactor-task .claude/plan/tasks-refactor-python3-development.md --task 2"
)
```

### On Task Completion

When a sub-agent completes:

1. Verify task status changed to `✅ COMPLETE` in task file
2. Mark TodoWrite item as `completed`
3. Recalculate ready tasks (dependencies may be satisfied now)
4. Launch newly-ready tasks

### Progress Loop

```
WHILE tasks remain incomplete:
    ready = tasks where status=❌ and dependencies satisfied
    IF ready is empty AND incomplete tasks exist:
        → Deadlock. Report blocked tasks and their dependencies.

    parallel_groups = group ready tasks by "Can Parallelize With"
    FOR each group:
        Launch all tasks in group (single message if multiple)
        Wait for completion
        Update status
```

---

## Completion and Verification Loop

When all tasks show `✅ COMPLETE`:

### Invoke Complete Refactor

AUTOMATICALLY invoke the complete-refactor command to trigger verification:

```
Skill(skill="complete-refactor", args="{task_file_path}")
```

This runs 4 phases:

1. **Plugin Validation** - Re-assess plugin structure, verify improvements
2. **Code Review** - Validates refactored code against project standards
3. **Documentation Audit** - Checks for documentation drift
4. **Gap Identification** - Creates follow-up tasks if issues found

### Check for Follow-up Tasks

After complete-refactor finishes, CHECK if follow-up tasks were created:

```
GLOB for: .claude/plan/tasks-refactor-{plugin-slug}-followup*.md
```

**IF follow-up tasks exist:**

1. DISPLAY:

```
================================================================================
                    FOLLOW-UP TASKS IDENTIFIED
================================================================================

The review found issues that need resolution:
- {list of follow-up task files}

Continuing recursive refactoring...
================================================================================
```

2. RECURSIVELY call implement-refactor on each follow-up task:

```
Skill(skill="implement-refactor", args="{followup_task_file_path}")
```

3. REPEAT until no more follow-up tasks are generated

**IF no follow-up tasks:**

1. UPDATE REFACTOR-PLAN.md: Move entry from Active to Completed with scores
2. DISPLAY final summary:

```
================================================================================
                    PLUGIN REFACTORING COMPLETE
================================================================================

Plugin: {plugin_name}
Task File: {task_file_path}

COMPLETED TASKS:
✅ Task {ID}: {Name}
✅ Task {ID}: {Name}
...

VERIFICATION PASSED:
✅ Plugin Validation: Score improved from X to Y
✅ Code Review: No issues found
✅ Documentation: Synced with implementation

All quality gates passed. Plugin refactoring is complete.
================================================================================
```

---

## Recursive Development Cycle

This command implements a **recursive refactoring loop**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMPLEMENT-REFACTOR                            │
│                                                                  │
│  ┌──────────────┐    ┌───────────────────┐    ┌──────────────┐ │
│  │ Execute      │───▶│ Complete          │───▶│ Follow-up    │ │
│  │ All Tasks    │    │ Refactor          │    │ Tasks?       │ │
│  └──────────────┘    └───────────────────┘    └──────┬───────┘ │
│                                                       │         │
│                              ┌────────────────────────┴───┐     │
│                              │                            │     │
│                              ▼                            ▼     │
│                         ┌────────┐                  ┌─────────┐ │
│                         │ YES    │                  │ NO      │ │
│                         └───┬────┘                  └────┬────┘ │
│                             │                            │      │
│                             ▼                            ▼      │
│                    ┌─────────────────┐          ┌────────────┐  │
│                    │ Recurse:        │          │ DONE       │  │
│                    │ implement-      │          │ Plugin     │  │
│                    │ refactor on     │          │ Refactored │  │
│                    │ follow-up tasks │          └────────────┘  │
│                    └────────┬────────┘                          │
│                             │                                   │
│                             └───────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

The cycle continues until the review finds no more issues.

---

## Error Handling

### Task Failure

If a sub-agent reports failure:

1. Keep task as `🔄 IN PROGRESS`
2. Display error details
3. Ask user: "(1) Retry, (2) Skip, (3) Abort"

### Dependency Deadlock

If no tasks are ready but tasks remain:

1. Display blocked tasks and their unmet dependencies
2. Ask user to resolve manually

### Design Conflicts

If sub-agent reports design spec conflicts with actual skill structure:

1. STOP implementation
2. Report the conflict
3. The design spec may need revision before continuing

---

## Orchestrator Responsibilities

You coordinate. Sub-agents implement.

- **You** read task files and identify what's ready
- **You** launch sub-agents with `/start-refactor-task`
- **You** track overall progress with TodoWrite
- **Sub-agents** do the actual refactoring work
- **Sub-agents** run verification steps
- **Sub-agents** report completion or blocking issues

If a sub-agent is blocked by concurrent edits from another agent, that's expected in parallel execution. Help them understand the changes and continue.
