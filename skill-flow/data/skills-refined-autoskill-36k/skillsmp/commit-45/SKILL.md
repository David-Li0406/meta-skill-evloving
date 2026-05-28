---
name: commit
description: >-
  Create well-formatted commits with conventional commit messages.
  Use when: creating commits, staging changes, running git commit,
  or when asked to commit code. Triggers automatically for any git
  commit workflow.
---

# Commit Skill

Create atomic, well-formatted git commits using conventional commit conventions.

## Workflow

1. Run `git status` to check staged files
2. If no files staged, run `git add .` to stage all changes
3. Run `git diff --staged` to analyze the changes
4. If changes touch multiple unrelated concerns, split into separate commits
5. For each commit, create a message following the format rules below

## Commit Message Format

**Single line only, max 72 characters:**

```
<type>: <description>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or fixing tests
- `chore`: Build process, tools, dependencies

**Rules:**
- Imperative mood ("add feature" not "added feature")
- Lowercase after the colon
- No period at the end
- No extended body or description text

## Splitting Commits

Split when changes involve:
- Different concerns or unrelated parts of codebase
- Different types of changes (features mixed with fixes)
- Different file types (source vs documentation)
- Large changes that would be clearer separated

Each commit should be atomic and serve a single purpose.

## Critical: No AI Attribution

- NEVER add `Co-Authored-By:` lines
- NEVER mention Claude, AI, LLM, or any assistant
- NEVER add "Generated with" or similar footers
- Commits must appear as written by a human developer

## Examples

Good:
- `feat: add user authentication system`
- `fix: resolve memory leak in rendering`
- `docs: update API endpoint documentation`
- `refactor: simplify parser error handling`
- `chore: update package dependencies`

Splitting example:
1. `feat: add new API type definitions`
2. `docs: update documentation for new types`
3. `test: add unit tests for new endpoints`
