---
name: gobby-expand
description: Use this skill when you need to expand a task into subtasks, whether through a task reference or a plan file, utilizing codebase analysis and visible reasoning.
---

# /gobby-expand - Task Expansion Skill

Expand a task into atomic subtasks. You perform the analysis and reasoning, which is visible in the conversation. This skill survives session compaction, as the specification is saved before execution.

## Input Formats

- `#N` - Task reference (e.g., `/gobby-expand #42`)
- `path.md` - Plan file (creates root task first, e.g., `/gobby-expand docs/plan.md`)

## Session Context

**IMPORTANT**: Use the `session_id` from your SessionStart hook context:
```
session_id: fd59c8fc-...
```

## Workflow

### Phase 0: Check for Resume

First, check if there's a pending expansion to resume:

```python
result = call_tool("gobby-tasks", "get_expansion_spec", {"task_id": "<ref>"})
if result.get("pending"):
    # Skip directly to Phase 4 with saved spec
    print(f"Resuming expansion with {result['subtask_count']} subtasks")
    # Jump to Phase 4
```

If `pending=True`, skip to **Phase 4** immediately.

### Phase 1: Prepare

1. **Parse input**: Task reference (`#N`) or file path (`plan.md`).

2. **If file path**: Read file content and create the root task:
   ```python
   content = Read(file_path)
   # Extract first heading as title
   result = call_tool("gobby-tasks", "create_task", {
       "title": "<first_heading>",
       "description": content,
       "task_type": "epic",
       "session_id": "<session_id>"
   })
   task_id = result["task"]["id"]
   ```

3. **Get task details**:
   ```python
   task = call_tool("gobby-tasks", "get_task", {"task_id": "<ref>"})
   ```

4. **Check for existing children** and handle re-expansion:
   ```python
   children = call_tool("gobby-tasks", "list_tasks", {"parent_task_id": task_id})
   if children["tasks"]:
       # IMPORTANT: Re-expansion preserves the parent task and its associations.
       # Only child tasks are deleted; the parent task_id remains intact.

       # Prompt user for confirmation before deleting children
       print(f"Task #{task_id} has {len(children['tasks'])} existing subtasks.")
       print("Re-expansion will delete all subtasks and their descendants.")
       # In practice, use AskUserQuestion tool for confirmation:
       # response = AskUserQuestion("Confirm re-expansion? This deletes all subtasks.", ...)
       # if not confirmed: return

       # Delete only the child tasks (NOT the parent)
       for child in children["tasks"]:
           call_tool("gobby-tasks", "delete_task", {"task_id": child["id"]})
   ```

### Phase 2: Analyze and Expand

- Perform analysis and reasoning to break down the task into subtasks based on the task details and context.

### Phase 3: Create Subtasks

- For each identified subtask, create it using:
   ```python
   call_tool("gobby-tasks", "create_task", {
       "title": "<subtask_title>",
       "description": "<subtask_description>",
       "parent_task_id": task_id,
       "session_id": "<session_id>"
   })
   ```

### Phase 4: Finalize

- Confirm the completion of the expansion and provide feedback to the user.
```python
print("Task expansion completed successfully.")
```