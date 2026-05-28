---
name: project-workflow
description: Provides workflow guidelines for problem-solving, git commits, GitHub issues, PRs, build management, and testing. Use when planning tasks, creating issues, submitting PRs, managing builds, or writing tests.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
model: sonnet
---

# Project Workflow Skill

## When to Use

- Planning and organizing tasks
- Creating GitHub issues or PRs
- Writing commit messages
- Managing builds and dependencies
- Setting up testing infrastructure

## Reference Documents (Import Syntax)

### Workflow
@./reference/workflow.md
@./reference/question-handling.md
@./reference/workflow-problem-solving.md
@./reference/performance-analysis.md

### GitHub
@./reference/github-issue-5w1h.md
@./reference/github-pr-5w1h.md
@./reference/git-commit-format.md

### Project Management
@./reference/problem-solving.md
@./reference/build.md
@./reference/testing.md

## Core Principles

1. **Systematic approach**: Follow procedures step by step
2. **Minimal changes**: Modify existing files, create new ones only when necessary
3. **Conventional commits**: Use proper type(scope): description format
4. **5W1H framework**: Apply What, Why, Who, When, Where, How for issues and PRs
5. **Layered testing**: Unit tests (many) -> Integration tests (some) -> E2E tests (few)
