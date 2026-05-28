---
name: git-and-ci
description: Use this skill when you need guidelines for Git commands and GitHub Actions for continuous integration.
---

# Git and CI Guidelines

## Git Commands

### Instructions

When working with git repositories:

1. Always use `git` or `gh` commands.
2. Never use `gt` command.

### When to Use

Apply this guideline when:
- Running any git operations.
- Suggesting git commands to the user.
- Writing scripts that involve version control.

## GitHub Actions

### Instructions

Use GitHub Actions for CI-related tasks. They should typically invoke the Taskfile to run standard build and test steps.

### Example

```bash
# Example step in .github/workflows/ci.yml
- name: Validate
  run: task validate
```

### When to Use

Utilize this guideline when setting up continuous integration workflows in GitHub.