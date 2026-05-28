---
name: spec:do-task
description: Execute Specific Task - runs a task by its number from the tasks document
---

# Execute Specific Task

Executes a specific task by its number from a specification's tasks document. This skill allows targeted execution of any task in the plan.

## When to use

Use this skill when the user needs to:
- Execute a specific task out of order
- Re-run a previously completed task
- Jump to a particular task in the implementation plan

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all three files** to understand the full context before executing tasks.

## Instructions

### Step 1: Parse Arguments

The `<args>` should contain:
- Task number (required) - e.g., "1", "1.2", "3.1"
- Spec name (optional) - e.g., "user-auth"

Format examples:
- `spec:do-task 1.2` - Execute task 1.2 from the current/only spec
- `spec:do-task user-auth 2.1` - Execute task 2.1 from the user-auth spec
- `spec:do-task 3` - Execute major task 3 (and all its subtasks)

### Step 2: Locate and Read Specification Documents

1. If spec name provided, look in `.specs/<spec-name>/`
2. If no spec name, check if there's only one spec in `.specs/`
3. If multiple specs exist without a name specified, list them and ask user to choose
4. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 3: Find the Specified Task

1. Search for the task matching the provided number
2. If task number is a major task (e.g., "2"), include all subtasks (2.1, 2.2, etc.)
3. If task not found, list available tasks and ask for correction

### Step 4: Execute the Task

1. **Mark as in-progress** - Update the checkbox to `[-]` in tasks.md
2. **Show task info** - Display to the user:
   - Task number and description
   - Files to create/modify
   - Requirements being addressed
   - Current status (pending/in-progress/completed)
3. **Read context** - Load relevant files mentioned in the task
4. **Implement the task** - Follow the task description:
   - Create new files as specified
   - Modify existing files as described
   - Follow project patterns and conventions
5. **Verify implementation** - Ensure the change is correct
6. **Mark as complete** - Update the checkbox to `[x]` in tasks.md
7. **Commit the changes** - Create a git commit for the completed task (see Committing Changes section)

### Step 5: Handle Subtasks

If executing a major task with subtasks:
1. Execute each subtask in order
2. Mark each subtask as complete when done
3. Mark the major task as complete when all subtasks finish

### Step 6: Report Completion

After completing the task:
1. Summarize what was implemented
2. Note if this was a re-execution of a completed task
3. Show related tasks that might need attention

## Committing Changes

After completing the task, create a git commit unless the user has specified otherwise:

1. Stage the changed files related to the task
2. Create a commit with a descriptive message referencing the task number
3. Do NOT include Co-Authored-By in commit messages

Commit message format (Conventional Commits):
```
<type>(<spec-name>): <description>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, etc.

Examples:
```
feat(user-auth): add login form component
fix(payment): resolve checkout validation error
refactor(api): simplify request handling
test(user-auth): add unit tests for login service
```

Skip committing if:
- The user explicitly asked not to commit
- The task only modified the tasks.md file (checkpoint tasks)

## Warning on Dependencies

If the specified task depends on incomplete prerequisite tasks:
1. Warn the user about missing dependencies
2. List the prerequisite tasks
3. Ask if they want to:
   - Execute prerequisites first
   - Proceed anyway
   - Cancel

## Error Handling

- If the task fails, keep it marked as `[-]`
- Report the issue to the user
- Suggest fixes or ask for guidance

## Arguments

- `<args>` - Task number and optionally spec name
  - Format: `[spec-name] <task-number>`
  - Task number: "1", "1.2", "2.3.1", etc.
  - Spec name: kebab-case identifier

Examples:
- `1.2` - Task 1.2 from the default/only spec
- `user-auth 3.1` - Task 3.1 from user-auth spec
- `payment-flow 2` - All of task 2 from payment-flow spec
