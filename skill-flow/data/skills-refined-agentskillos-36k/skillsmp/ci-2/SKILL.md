---
name: ci
description: Guidelines for GitHub Actions.
---

# CI

## GitHub Actions
Use GitHub Actions for CI related tasks. They should typically invoke the [Taskfile](../task_runner/SKILL.md) to run standard build and test steps:

```bash
# Example step in .github/workflows/ci.yml
- name: Validate
  run: task validate
```
