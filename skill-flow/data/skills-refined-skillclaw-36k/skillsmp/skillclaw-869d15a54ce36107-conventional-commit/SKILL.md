---
name: conventional-commit
description: Use this skill when creating well-formatted git commits following the Conventional Commits specification.
---

# Skill body

Create atomic, well-formatted git commits using Conventional Commits.

## Workflow

1. Run `git status` to check staged files.
2. Review changes using `git diff --staged` to analyze the changes.
3. If no files are staged, run `git add <files>` to stage specific changes (avoid using `git add .` without reviewing).
4. If changes touch multiple unrelated concerns, split them into separate commits.
5. For each commit, create a message following the format rules below.

## Commit Message Format

**Format:**
```
<type>(<scope>): <subject>
```

- **type**: feat, fix, docs, style, refactor, perf, test, chore, build, ci, revert
- **scope**: Optional area of change (e.g., auth, api, config)
- **subject**: Imperative mood, max 100 characters, no period at the end.

**Rules:**
- Use imperative mood (e.g., "add feature" not "added feature").
- Lowercase after the colon.
- No period at the end.
- No extended body or description text unless necessary.

## Splitting Commits

Split when changes involve:
- Different concerns or unrelated parts of the codebase.
- Different types of changes (features mixed with fixes).
- Large changes that would be clearer when separated.

Each commit should be atomic and serve a single purpose.

## Safety Rules

- **NEVER** skip hooks with `--no-verify`.
- **NEVER** force push to main/master.
- **NEVER** commit secrets (e.g., .env files, credentials).
- **ASK** the user if commit scope or message is unclear.

## Examples

Good:
- `feat(auth): add user authentication system`
- `fix(api): resolve memory leak in rendering`
- `docs: update API endpoint documentation`
- `refactor(parser): simplify error handling`
- `chore(deps): update package dependencies`

Splitting example:
1. `feat(api): add new API type definitions`
2. `docs: update documentation for new types`
3. `test: add unit tests for new endpoints`