---
name: git-commit
description: Use this skill when creating well-formatted git commits following Conventional Commits specifications.
---

# Git Commit Skill

Create atomic, well-formatted git commits using Conventional Commit conventions.

## Workflow

1. Run `git status` to check staged files.
2. Review changes using `git diff --staged` to analyze the changes.
3. If no files are staged, stage specific files with `git add <files>` (avoid using `git add .` without review).
4. If changes touch multiple unrelated concerns, split them into separate commits.
5. For each commit, create a message following the format rules below.

## Commit Message Format

**Format:**
```
<type>(<scope>): <subject>
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
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `revert`: Reverts a previous commit

**Rules:**
- Use imperative mood (e.g., "add feature" not "added feature").
- Keep the subject line to a maximum of 100 characters.
- No period at the end.
- No extended body or description text unless necessary.

## Splitting Commits

Split commits when changes involve:
- Different concerns or unrelated parts of the codebase.
- Different types of changes (features mixed with fixes).
- Different file types (source vs documentation).
- Large changes that would be clearer when separated.

Each commit should be atomic and serve a single purpose.

## Safety Rules

- **NEVER** skip hooks with `--no-verify`.
- **NEVER** force push to main/master.
- **NEVER** commit secrets (e.g., .env files, credentials).
- **ASK** the user if commit scope or message is unclear.
- **SPLIT** large changes into atomic commits.

## Critical: No AI Attribution

- NEVER add `Co-Authored-By:` lines.
- NEVER mention AI or any assistant in commit messages.
- Commits must appear as written by a human developer.

## Examples

Good:
- `feat(auth): add user authentication system`
- `fix(api): resolve memory leak in rendering`
- `docs(api): update API endpoint documentation`
- `refactor(parser): simplify error handling`
- `chore(dependencies): update package dependencies`

Splitting example:
1. `feat(api): add new API type definitions`
2. `docs(api): update documentation for new types`
3. `test(api): add unit tests for new endpoints`

For full type definitions, see [CONVENTIONS.md](CONVENTIONS.md).
For message examples, see [EXAMPLES.md](EXAMPLES.md).