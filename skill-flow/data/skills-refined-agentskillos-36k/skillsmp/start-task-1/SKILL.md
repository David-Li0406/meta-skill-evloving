---
name: start-task
description: Initialize a new parallel task environment using git worktrees. required for every new task.
---

# START-TASK

> **Identity**: Project Manager / Environment Initializer
> **Goal**: Create a clean, isolated environment for a new task.

## Usage

Run this skill when the user indicates they want to start a new piece of work (feature, bugfix, chore).

## Automated Steps

The `setup_worktree.py` script will:

1. Validates the task name (kebab-case).
2. Creates a new git branch.
3. Creates a worktree in `.worktrees/<task-name>`.
4. Initializes a `task.md` template in the new worktree.

## Instructions

1.  **Ask for Task Name**: If not provided, ask the user for a descriptive, kebab-case name (e.g., `feature-auth-login`).
2.  **Execute Script**: Run the python script with the task name.
    ```bash
    python3 .agent/skills/start-task/scripts/setup_worktree.py --name <task_name>
    ```
3.  **Context Switch**:
    - Stop editing in the current directory.
    - Instruct the user that you are switching ("Moving to worktree...").
    - (Agentic Note): You cannot physically "cd" in the same session usually, but you should treat the new directory as your workspace for the next steps.

## Scripts

- `scripts/setup_worktree.py`
