---
name: git-commit
description: Use this skill when you need to create a meaningful commit with a well-structured message that reflects the changes made in your code.
---

# Skill body

## Instructions

Use this skill when executing the `/commit-and-push` or `/commit-and-pr` slash commands.

## Guidelines

- Only commit when:
  1. All tests pass.
  2. All compiler/linter warnings are resolved.
  3. The changes represent a single logical unit of work.
  4. The commit message clearly indicates structural or functional changes.
- Prefer small, frequent commits over large, infrequent ones.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Body should include**:
- What was changed and why.
- Background of the issue and rationale for the solution.
- Implementation decisions.
- Potential impacts.
- Wrap at 72 characters.

## Execution Steps

1. Review changes with `git status` and `git diff`.
2. Analyze the type and scope of changes.
3. Generate a commit message in Conventional Commits format.
4. Confirm with the user before executing the commit.

### Conventional Commits Format

```
type(scope): description

[optional body]

[optional footer]
```

### Type

| Type | Description |
|------|-------------|
| feat | A new feature |
| fix | A bug fix |
| docs | Documentation only changes |
| style | Changes that do not affect the meaning of the code (white-space, formatting, etc.) |
| refactor | Code changes that neither fix a bug nor add a feature |
| perf | Performance improvements |
| test | Adding or updating tests |
| chore | Changes to the build process or auxiliary tools |

### Scope

Indicates the scope of the changes (optional). Example: `auth`, `api`, `ui`.

### Description

- Write in imperative mood (Add, Fix, Update, etc.).
- Limit to 50 characters.
- Do not end with a period.

## Notes

- Exclude files containing sensitive information (e.g., `.env`).
- Suggest splitting large changes.
- Use `--amend` only if explicitly instructed.
- Do not automatically push (only if explicitly instructed).