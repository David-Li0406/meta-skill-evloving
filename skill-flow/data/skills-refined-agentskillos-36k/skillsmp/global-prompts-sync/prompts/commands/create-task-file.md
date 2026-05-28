---
name: create-task-file
description: Create a new daily task file using the daily-task-creator skill
model: Grok Code Fast 1 (copilot)
---
# Create Task File

Use the `daily-task-creator` skill to create a new task file.

## Instructions

1. **Locate the Skill**: Find the `daily-task-creator` skill in the workspace.
2. **Execute**: Run the script associated with the skill (typically `scripts/create_task.py`) to generate a new task file in the `.tmp` directory.
3. **Verify**: Confirm the file was created (e.g., `task-YYYYMMDD-N.md`) and inform the user of the file path.
