---
name: spec:execute-tasks
description: Use this skill when you need to execute tasks from a specification's tasks document, either all at once or one at a time.
---

# Execute Tasks

This skill allows you to execute tasks from a specification's tasks document, either by running all pending tasks sequentially or by executing the next pending task individually.

## When to use

Use this skill when the user needs to:
- Implement an entire feature based on the tasks document.
- Execute all remaining tasks from a specification.
- Implement one task at a time with review between tasks.
- Continue work on a partially completed specification.

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
2. If no spec name is provided, list available specs in `.specs/` and ask the user to choose.
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built.
   - `design.md` - understand how it should be built.
   - `tasks.md` - get the list of tasks to execute.

### Step 2: Identify Tasks

1. For executing all tasks:
   - Identify all tasks and subtasks using checkbox markers:
     - `[ ]` - Pending task (to be executed)
     - `[-]` - In progress task (continue execution)
     - `[x]` - Completed task (skip)
   - Build a task list with task numbers, descriptions, file paths, and requirements references.
   - Determine execution order based on task numbering.

2. For executing the next task:
   - Scan the document for checkbox markers.
   - Find the first task that is marked as `[-]` (in progress) or `[ ]` (pending).
   - Skip tasks marked as `[x]` (completed).
   - If all tasks are complete, inform the user.

### Step 3: Execute Tasks

1. **Mark as in-progress** - Update the checkbox to `[-]` in tasks.md.
2. **Show task info** - Display to the user:
   - Task number and description.
   - Files to create/modify.
   - Requirements being addressed.
3. **Read context** - Load relevant files mentioned in the task.
4. **Implement the task** - Follow the task description:
   - Create new files as specified.
   - Modify existing files as described.
   - Follow project patterns and conventions.
5. **Verify implementation** - Ensure the change is correct.
6. **Mark as complete** - Update the checkbox to `[x]` in tasks.md.
7. **Commit the changes** - Create a git commit for the completed task (see Committing Changes section).

### Step 4: Handle Checkpoints

When encountering a checkpoint task:
1. Run any verification commands specified.
2. Ensure tests pass if mentioned.
3. Summarize progress to the user.
4. Continue to the next task unless there are failures.

### Step 5: Final Summary

After completing all tasks:
1. Summarize what was implemented.
2. List any issues encountered.
3. Suggest next steps (e.g., testing, review).

## Committing Changes

After completing each task, create a git commit unless the user has specified otherwise:

1. Stage the changed files related to the task.
2. Create a commit with a descriptive message referencing the task number.
3. Do NOT include Co-Authored-By in commit messages.

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
- The user explicitly asked not to commit.
- The task only modified the tasks.md file (checkpoint tasks).

## Error Handling

- If a task fails, mark it as `[-]` and report the issue.
- Ask the user how to proceed (skip, retry, abort).
- Do not proceed with dependent tasks if a prerequisite fails.

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow").

If not provided, list available specs and ask the user to choose.