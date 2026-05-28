---
name: Git Commit Convention
description: Enforces the Bedriftsgrafen project's strict git commit message format and policies.
---

# Git Commit Convention Skill

## Purpose
This skill ensures all git commits made in the `bedriftsgrafen.no` repository adhere to the strict project standards.

## Commit Message Format

The commit message MUST follow this specific format:

```text
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

### Scope
The scope should be the name of the module affected (e.g., `api`, `auth`, `frontend`, `db`).

### Subject
- Imperative mood ("add" not "added")
- No capitalizing first letter
- No dot (.) at the end

## Pre-Commit Checklist
Before generating the commit command, you MUST ensure:
1.  **Tests Pass**: All relevant tests (unit/integration) must pass.
2.  **Linting**: Code must be linted (`ruff` for backend, `eslint` for frontend).
3.  **Type Check**: Types must be valid (`mypy` for backend, `tsc` for frontend).

## Usage
When asked to commit changes, construct the `git commit` command using the `run_command` tool with the `-m` flag containing the formatted message.
