---
name: task-creator
description: Create numbered task documents from template when user says "create task", "new task", or "make task". Auto-numbers files in ai_docs/tasks/ and follows task template workflow.
---

# Task Creator Skill

## Purpose
Automatically create numbered task documents using the comprehensive task template when the user requests to create a new task.

## When to Activate
Activate this skill when the user says any of these phrases (case-insensitive):
- "create task"
- "new task"
- "make task"
- "create a task"
- "help me create a task"
- "start a task"
- "create task document"
- "create task for [feature]"

## Workflow

### Step 1: Find Next Task Number
Scan `ai_docs/tasks/` directory to find the highest numbered task file and increment by 1.

```bash
# List all task files to find highest number
ls ai_docs/tasks/ | grep -E '^[0-9]{3}_' | sort -n | tail -1
```

### Step 2: Determine Task Name
- Extract the feature/topic from the user's request
- Convert to snake_case for filename
- Example: "implement user notifications" → `046_implement_user_notifications.md`

### Step 3: Create Task File
- Read the template from `ai_docs/dev_templates/task_template.md`
- Create new file at `ai_docs/tasks/XXX_feature_name.md`
- Fill in Task Title and Goal Statement based on user's request

### Step 4: Follow Template Instructions
The task template contains comprehensive instructions in section 16 (AI Agent Instructions):
- Strategic analysis evaluation (when needed vs direct implementation)
- Current codebase analysis
- Implementation planning phases
- Code quality standards
- Architecture compliance checks
- Comprehensive code review process

Simply follow the task template's workflow exactly as documented.

## Key Points

- **Auto-numbering is mandatory**: Always find and use the next sequential number
- **File location**: Always create in `ai_docs/tasks/` directory
- **Follow template workflow**: After creating the file, follow the task template's instructions exactly
- **The template does the heavy lifting**: Don't reinvent the workflow - delegate to the template

## Example Usage

**User says**: "create a task for adding email notifications"

**Actions**:
1. Scan `ai_docs/tasks/` → finds highest number is 045
2. Next number is 046
3. Create `ai_docs/tasks/046_add_email_notifications.md`
4. Fill in basic info (title, goal) from user's request
5. Follow task template instructions for remainder of workflow

## Success Criteria

- ✅ Task file created with correct sequential number
- ✅ File placed in `ai_docs/tasks/` directory
- ✅ Basic sections populated from user's request
- ✅ Task template workflow followed for remainder of process
