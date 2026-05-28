---
name: commit-helper
description: Generate conventional commit messages from staged changes. Runs autonomously using Haiku model. Use after completing TDD cycles, after refactoring sessions, or when ready to commit.
context: agent
---

# Commit Helper

Autonomous commit message generation that analyses staged changes and generates conventional commit messages.

## When to Use

- After completing a TDD cycle (tests pass)
- After a refactoring session
- After completing a task in the XP workflow
- Whenever you have staged changes ready to commit

## What It Does

1. Checks git status for staged changes
2. Reads the staged diff
3. Checks recent commits for style consistency
4. Analyses change type and scope
5. Generates a conventional commit message

## Conventional Commit Format

```
<type>: <summary>

[optional body]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behaviour change) |
| `test` | Adding/updating tests |
| `docs` | Documentation only |
| `chore` | Build, tooling, dependencies |

### Summary Rules

- Under 50 characters
- Imperative mood ("add" not "added")
- No period at end
- Capitalise first letter

## Safety Rules

- **NEVER** add contributors unless explicitly requested
- **NEVER** commit files containing secrets
- **NEVER** use `--amend` unless explicitly requested
