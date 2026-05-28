---
name: task_runner
description: Guidelines for standard tasks in Taskfile.yml.
---

# Task Runner

## Standard Tasks
[Taskfile](https://taskfile.dev/) is the mandatory task runner. Most projects should implement the following standard tasks in `Taskfile.yml`:

- `generate`: Generates code as required (e.g., from Protocol Buffers, mocks).
- `build`: Compiles the application binary.
- `setup`: Installs required tools and dependencies.
- `validate`: Runs lints, unit tests, smoke tests, and the build. Run this before committing.
- `test`: Runs unit tests.
- `lint`: Runs code linters.
