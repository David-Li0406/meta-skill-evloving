---
name: init-workspace
description: Initialize a working directory for development tasks
---

# init-workspace

## Overview

This skill helps you initialize a working environment for development tasks using an automated setup script.

**After initialization:** Use `/execute-workspace` to work through TODO items and complete the task.

## Steps

### 1. Understand the Task Requirements

Before running the setup script, ensure you have:

- Task type (feature, bugfix, research, etc.)
- Brief description
- Target repository path in org/repo format (e.g., github.com/sters/complex-ai-workspace)
- Ticket ID (optional)

**Note:** Base branch is automatically detected from the remote default (main/master). You don't need to specify it.

### 2. Run Setup Script

Execute the setup script with the required parameters:

```bash
./.claude/skills/init-workspace/scripts/setup-workspace.sh <task-type> <description> <org/repo-name> [ticket-id]
```

**Examples:**

```bash
# Basic usage - base branch is auto-detected
./.claude/skills/init-workspace/scripts/setup-workspace.sh feature user-auth github.com/sters/complex-ai-workspace

# With ticket ID
./.claude/skills/init-workspace/scripts/setup-workspace.sh feature user-auth github.com/sters/complex-ai-workspace PROJ-123

# Bug fix
./.claude/skills/init-workspace/scripts/setup-workspace.sh bugfix login-error github.com/sters/complex-ai-workspace

# Research task
./.claude/skills/init-workspace/scripts/setup-workspace.sh research performance-analysis github.com/sters/complex-ai-workspace
```

The script will automatically:

- Create a working directory with proper naming convention
- Clone or update the target repository
- Create a git worktree in the working directory
- Generate README.md with task template
- Generate `TODO-<repository-name>.md` with task-specific checklist

### 3. Customize Documentation

After setup completes:

- Open the generated `README.md` and fill in task details
- Review and customize `TODO-<repository-name>.md` checklist as needed

## Next Steps

After initialization is complete, use `/execute-workspace` to:
- Work through TODO items
- Delegate to workspace-repo-todo-executor agent
- Run tests and linters
- Verify completion
