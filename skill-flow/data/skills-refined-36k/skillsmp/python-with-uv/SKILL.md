---
name: python-with-uv
description: Run Python projects and tests using uv.
---

# Python with uv

This skill provides instructions for using `uv` to run Python projects and tests.

## When to Use this Skill
This skill is activated when the user asks to:

- Run Python projects using `uv`.
- Run Python tests using `uv`.
- Set up or configure `uv` for a Python project.

## Instructions
When this skill is active, strictly follow these steps in order:

1.  **Check for uv**: Check if `uv` is installed.
    *   Command: `uv --version`
1b.  **Install uv**: If `uv` is not installed, instruct the user to install it. A common method is using `wget`:
    *   Command: `wget -qO- https://astral.sh/uv/install.sh | sh`
2.  **Sync Depdendencies**: Run `uv sync` to sync dependencies.
    *   Command: `uv sync`
3.  **Run Python Project**: To run a Python project, use the `uv run` command followed by the Python script or module.
    *   Command: `uv run main.py` or `uv run -m your_module`
4.  **Run Python Tests**: To run tests (e.g., with pytest), use `uv run` with the test runner command.
    *   Command: `uv run pytest`

## Critical Constraints (The "Guardrails")
-   **NEVER** instruct the user to use `pip` or `pipenv` for dependency management if `uv` is available and specified.
-   **ALWAYS** ensure that `uv` is installed before attempting to use it.
-   **CHECK** that the specified Python script or test command is valid before executing.

## Examples

### Example 1
User: How do I run my Python project with uv?
Assistant:
Okay, I can help you run your Python project with `uv`.

First, sync your dependencies:
`uv sync`

Then, to run your Python project, use the `uv run` command followed by your script name:
`uv run main.py`

### Example 2
User: Use uv to run my pytest tests.
Assistant:
I can help you run your pytest tests with `uv`.

First, sync your dependencies:
`uv sync`
`uv` is not recognized as an internal or external command, operable program or batch file.

Since `uv` is not installed, I can install it using `wget`:
`wget -qO- https://astral.sh/uv/install.sh | sh`

After installing `uv`, I will sync your dependencies:
`uv sync`

Finally, to execute your tests using `uv`, run:
`uv run pytest`
