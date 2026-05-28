---
name: git-and-ci-guidelines
description: Use this skill when you need to follow best practices for Git operations and GitHub Actions in your projects.
---

# Skill body

## Git Guidelines

When working with git repositories:

1. Always use `git` or `gh` commands.
2. Never use `gt` command.

## When to Use Git Guidelines

Apply these guidelines when:
- Running any git operations.
- Suggesting git commands to the user.
- Writing scripts that involve version control.

## CI Guidelines with GitHub Actions

Use GitHub Actions for CI-related tasks. They should typically invoke the Taskfile to run standard build and test steps. Here’s an example step in a `.github/workflows/ci.yml` file:

```yaml
- name: Validate
  run: task validate
```

## When to Use CI Guidelines

Apply these guidelines when:
- Setting up continuous integration for your projects.
- Writing workflows for automated testing and deployment.