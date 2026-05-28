---
name: execute-workspace
description: Execute tasks in an initialized workspace by working through TODO items
---

# execute-workspace

## Overview

This skill helps you execute work in an already initialized workspace. It works through TODO items, delegates to sub-agents, and verifies completion.

**Prerequisites:** The workspace must be initialized first using `/init-workspace`.

## Steps

### 1. Execute Work According to TODO

- Work through `TODO-<repository-name>.md` checklist items sequentially
- Check off items as you complete them
- Update the TODO file if you discover additional tasks
- Add notes or blockers under each item if needed
- If you encounter issues, document them in the TODO file
- Regularly save and commit your progress
- Do not proceed to next items if current item has blockers

**Handling User Requests During Execution:**

When the user provides additional requirements or requests changes during execution, the **main orchestrating agent** (not the sub-agent) should:

- Read the corresponding `TODO-<repository-name>.md` file
- Add new TODO items or update existing ones to reflect the new requirements
- Update the README.md if the task scope or objectives has changed
- Either continue execution directly or re-delegate to the workspace-repo-todo-executor sub-agent with updated context

Note: The sub-agent operates autonomously on the TODO list and does not handle interactive user requests. User interactions should be handled by the main agent before delegation.

### 2. Delegate to workspace-repo-todo-executor SubAgent

Use the `workspace-repo-todo-executor` sub-agent to autonomously execute TODO items, run tests/linters, and commit changes.

**How to invoke:**

Use the Task tool to launch the workspace-repo-todo-executor agent:

```yaml
Task tool:
  subagent_type: workspace-repo-todo-executor
  prompt: |
    Execute tasks in workspace: workspace/feature-user-auth-20260116
    Repository path: github.com/sters/complex-ai-workspace
    Repository name: complex-ai-workspace
    Repository worktree path: workspace/feature-user-auth-20260116/github.com/sters/complex-ai-workspace
```

**What the agent does:**

- Reads README.md and `TODO-<repository-name>.md` to understand the task
- Executes TODO items sequentially
- Updates the TODO file as items are completed
- Runs tests and linters
- Makes commits with descriptive messages
- Reports completion summary

**When to use SubAgent delegation:**

- Task has 5+ TODO items
- Task requires research and implementation
- Task is self-contained and well-defined
- You need to maintain focus on high-level coordination

### 3. Verification Before Completion

Before considering the task complete:

- [ ] All TODO items are checked off (or all phases completed)
- [ ] All tests pass
- [ ] No linter errors
- [ ] Documentation is updated
- [ ] Changes are committed and pushed (if applicable)
