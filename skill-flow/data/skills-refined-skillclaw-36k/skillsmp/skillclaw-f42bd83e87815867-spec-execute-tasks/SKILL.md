---
name: spec:execute-tasks
description: Use this skill when you need to execute tasks from a specification's tasks document, either all at once or one at a time.
---

# Skill body

## When to use

Use this skill when the user needs to:
- Implement an entire feature based on the tasks document
- Execute all remaining tasks from a specification
- Complete the full implementation plan
- Implement one task at a time with review between tasks
- Continue work on a partially completed specification

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
2. If no spec name is provided, list available specs in `.specs/` and ask the user to choose
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 2: Parse Tasks

1. Identify all tasks and subtasks using checkbox markers:
   - `[ ]` - Pending task (to be executed)
   - `[-]` - In progress task (continue execution)
   - `[x]` - Completed task (skip)
2. Build a task list with:
   - Task number (e.g., "1.1", "2.3")
   - Task description
   - File paths mentioned
   - Requirements references
3. Determine execution order based on task numbering

### Step 3: Execute Tasks

#### Option A: Execute All Tasks

1. For each pending task:
   - **Mark as in-progress** - Update the checkbox to `[-]` in tasks.md
   - **Launch subagent** - Use the Task tool with `subagent_type: "general-purpose"` to execute the task:
     - Provide the full task description, file paths, and requirements
     - Include relevant context from the spec (requirements.md, design.md)
   - **Wait for completion** - Let the subagent complete its work
   - **Verify result** - Review the output and mark the task as complete

#### Option B: Execute Next Task

1. Scan the document for checkbox markers
2. Find the first task that is:
   - Marked as `[-]` (in progress) - resume this task first
   - Or marked as `[ ]` (pending) - start this task
3. Skip tasks marked as `[x]` (completed)
4. If all tasks are complete, inform the user
5. **Mark as in-progress** - Update the checkbox to `[-]` in tasks.md
6. **Show task info** - Display to the user:
   - Task number and description
   - Files to create/modify
   - Requirements being addressed
7. **Read context** - Load relevant files mentioned in the task
8. **Implement the task** - Follow the task description:
   - Create new files as specified
   - Modify existing files as described
   - Follow project patterns and conventions
9. **Verify implementation** - Ensure the change is correct
10. **Mark as complete** - Update the checkbox to `[x]` in tasks.md
11. **Commit the changes** - Create a git commit for the completed task (see Committing Changes section)

### Step 4: Handle Checkpoint Tasks

If the next task is a checkpoint:
1. Run any verification steps as specified in the task description.