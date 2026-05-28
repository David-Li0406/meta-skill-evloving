---
name: spec:do-next
description: Execute Next Task - runs the next pending task from the tasks document
---

# Execute Next Task

Executes the next pending task from a specification's tasks document. This skill finds the first incomplete task and implements it.

## When to use

Use this skill when the user needs to:
- Implement one task at a time with review between tasks
- Continue work on a partially completed specification
- Execute tasks incrementally with manual control

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all three files** to understand the full context before executing tasks.

## Instructions

### Step 1: Locate and Read Specification Documents

1. If `<args>` contains a spec name, look in `.specs/<spec-name>/`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 2: Find the Next Task

1. Scan the document for checkbox markers
2. Find the first task that is:
   - Marked as `[-]` (in progress) - resume this task first
   - Or marked as `[ ]` (pending) - start this task
3. Skip tasks marked as `[x]` (completed)
4. If all tasks are complete, inform the user

### Step 3: Execute the Task

1. **Mark as in-progress** - Update the checkbox to `[-]` in tasks.md
2. **Show task info** - Display to the user:
   - Task number and description
   - Files to create/modify
   - Requirements being addressed
3. **Read context** - Load relevant files mentioned in the task
4. **Implement the task** - Follow the task description:
   - Create new files as specified
   - Modify existing files as described
   - Follow project patterns and conventions
5. **Verify implementation** - Ensure the change is correct
6. **Mark as complete** - Update the checkbox to `[x]` in tasks.md
7. **Commit the changes** - Create a git commit for the completed task (see Committing Changes section)

### Step 4: Handle Checkpoint Tasks

If the next task is a checkpoint:
1. Run any verification commands specified
2. Report the verification results
3. Mark as complete if all checks pass
4. Report issues if any checks fail

### Step 5: Report Completion

After completing the task:
1. Summarize what was implemented
2. Show the next pending task (if any)
3. Ask if the user wants to continue with the next task

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

## Error Handling

- If the task fails, keep it marked as `[-]`
- Report the issue to the user
- Suggest fixes or ask for guidance

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
