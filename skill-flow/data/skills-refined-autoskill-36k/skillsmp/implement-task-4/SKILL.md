---
name: implement-task
description: >
  Implement tasks using appropriate coding agents with continuous build verification.
  Use when user provides a task to implement.
  Delegates to Fast/Coding/Complex Coding agents based on complexity. Follows implement-build-test-fix loop.
---

# Implement and Iterate Task

Implement tasks using appropriate coding agents with continuous build verification.

**Usage**: When user provides a task to implement

## Instructions

- Respect AGENTS.md
- Use MCP servers to assist
- Delegate to appropriate coding agents when possible:
  - **Fast Coding Agent**: Simple tasks, single-file edits
  - **Coding Agent**: Medium complexity, multi-file changes
  - **Complex Coding Agent**: High-complexity architectural work
- Spawn as many agents as needed
- Always use modern language syntax when possible
- When user is happy, run the accept ADR flow to finalize the feature

## Iteration Loop

1. **Implement** sub-task
2. **Build & Test**
3. **Fix** if needed (repeat 1-2)
4. **Next** sub-task
