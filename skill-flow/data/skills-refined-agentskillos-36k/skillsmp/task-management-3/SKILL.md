---
name: task-management
description: Create and manage .task files using AI Framework conventions
category: workflow
tools: [read, edit, create]
---
# Skill: Task Management

## Purpose

Manage `.task` files according to AI Framework conventions. This skill helps agents create, update, and maintain task files throughout their lifecycle.

## Template

Use [Planning/Task.task.template](../../Planning/Task.task.template) as the base template for all new tasks.

## Workflow

### Creating a New Task

1. **Select appropriate slice** (Framework/, Ai/, Git/, etc.)
2. **Name the file**: `{Slice}/{TaskName}.task`
3. **Add delegation prompt** at top with 4-backtick code block:

````markdown
**Task**: [{Slice}/{TaskName}.task]({Slice}/{TaskName}.task)
**Role**: {Role} (see [Framework/{Prompt}.prompt.md](Framework/{Prompt}.prompt.md))
**Target Audience**: {Agent} ({Model})

{1-2 sentence context}
````

4. **Define deliverables**: Use `- [ ] **D1**: {Description}` format
5. **Set metadata**:
   - Status: Not Started | In Progress | Complete | Blocked
   - Owner: Strategic Agent | Implementation Agent
   - Priority: Critical | High | Medium | Low
   - Effort: Small | Medium | Large
   - Priority Score: 1-15 (see [Planning/TaskPrioritySystem.md](../../Planning/TaskPrioritySystem.md))

6. **Add success criteria** with verification commands:
   - `dotnet build` succeeds (0 errors, 0 warnings)
   - `dotnet test` passes
   - Lint clean if applicable

### Updating Task Progress

1. **Mark deliverables complete**: Change `- [ ]` to `- [x]`
2. **Update Progress Log**: Add date and summary
3. **Link reports**: Reference `.report` files, don't inline
4. **Update status**: Change to "In Progress" or "Complete"

### Creating Progress Reports

1. **Name**: `{TaskName}.task.{Phase}.report` (alongside `.task`)
2. **Use template**: [Planning/ProgressReport.report.template](../../Planning/ProgressReport.report.template)
3. **Link in task**: Add filename reference in Progress Log
4. **Keep separate**: Reports are separate files, not inlined

### Creating Blocker Reports

1. **Name**: `{TaskName}.task.{BlockerName}.report` (alongside `.task`)
2. **Use template**: [Planning/BlockerReport.report.template](../../Planning/BlockerReport.report.template)
3. **Document in task**: Reference in Progress Log
4. **Delegate to Orchestrator**: Use code block delegation

### Archiving Completed Tasks

1. **When**: All deliverables complete, PR merged
2. **Where**: `{Slice}/archive/{TaskName}.YYYY-MM-DD.task`
3. **Include reports**: Move all `.report` files with task
4. **Update inventories**: Remove from active, add to archive inventory

## File Naming Conventions

| Type              | Pattern                                  | Example                                    |
|-------------------|------------------------------------------|--------------------------------------------|
| Task file         | `{Slice}/{TaskName}.task`                | `Framework/CopilotConfiguration.task`      |
| Progress report   | `{TaskName}.task.{Phase}.report`         | `CopilotConfiguration.task.Research.report`|
| Blocker report    | `{TaskName}.task.{Blocker}.report`       | `CopilotConfiguration.task.APIAccess.report`|
| Archived task     | `{Slice}/archive/{TaskName}.YYYY-MM-DD.task` | `Framework/archive/CopilotConfiguration.2025-12-26.task` |

## Task Statuses

| Status        | Meaning                                      | Next Action                    |
|---------------|----------------------------------------------|--------------------------------|
| Not Started   | Task created, not yet assigned               | Delegate to Planner or Implementer |
| In Progress   | Work actively underway                       | Continue work, update Progress Log |
| Complete      | All deliverables done, PR merged             | Archive task file              |
| Blocked       | Cannot proceed without external input        | Create blocker report, delegate to Orchestrator |

## Delegation Completion Checklist

Before delegating to next role:

- [ ] All deliverables marked `- [x]` complete
- [ ] Progress Log updated with completion summary
- [ ] Progress report created and linked
- [ ] Delegation block added to task file (4 backticks)
- [ ] PR created (if Implementation Agent)
- [ ] Verification complete (build, tests, lint)

## Common Patterns

### Plan Review Iteration

1. Planner creates initial plan in task file
2. Delegates to Implementer for review (Plan Review role)
3. Implementer provides feedback via report
4. Planner refines plan based on feedback
5. Repeat until both approve
6. Record sign-off in task Progress Log
7. Delegate to Implementer for execution

### Implementation to Review

1. Implementer completes all deliverables
2. Updates task file with completion status
3. Creates progress report with evidence
4. Adds reviewer delegation block to task
5. Posts PR comment with @copilot tag
6. Reviewer verifies and approves/requests changes

## Best Practices

- **Keep task files concise** - Link to reports for details
- **Update Progress Log frequently** - After each meaningful unit of work
- **Use checklists** - `- [x]` for done, `- [ ]` for pending
- **Reference files** - Use relative paths from task location
- **Archive when done** - Keep active task list clean
- **Track dependencies** - Note blocking/blocked-by relationships

## References

- Task template: [Planning/Task.task.template](../../Planning/Task.task.template)
- Progress report template: [Planning/ProgressReport.report.template](../../Planning/ProgressReport.report.template)
- Blocker report template: [Planning/BlockerReport.report.template](../../Planning/BlockerReport.report.template)
- Priority system: [Planning/TaskPrioritySystem.md](../../Planning/TaskPrioritySystem.md)
- Delegation format: [Framework/Delegation.instructions.md](../../Framework/Delegation.instructions.md)
