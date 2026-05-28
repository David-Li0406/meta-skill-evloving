---
name: conventional-commits
description: Use this skill to create and manage commit messages following the Conventional Commits standard based on staged changes or pasted diffs.
---

# Conventional Commits Guide

## Purpose

- Communicate changes in a consistent format.
- Assist in automatic CHANGELOG generation and release note creation.

## Format

```
<type>(<scope>): <subject>

[body]

[footer]
```

- `<scope>` is optional. Specify if the target is clear; omit if uncertain.
- Indicate breaking changes with `<type>!` or in the footer.

### Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting changes (no code change)
- **refactor**: Refactoring
- **perf**: Performance improvement
- **test**: Adding or modifying tests
- **build**: Build or dependency changes
- **ci**: CI configuration
- **chore**: Miscellaneous tasks
- **revert**: Reverting changes

## English Commit Message Rules

- `<subject>` should be written in the imperative mood.
- Start with a lowercase letter.
- Do not end with a period.

## Steps to Create a Commit Message

### Step 1: Check Staged Changes

Run:
```bash
GIT_PAGER=cat git diff --staged
```

**Handle edge cases:**
- **Empty output** → Respond: "No staged changes. Please stage files using `git add` or paste the diff manually."
- **Command failure** → Prompt the user to paste the staged diff.

### Step 2: Analyze Changes

Identify:
1. **Main purpose** — What is the core intent of the change?
2. **Scope of impact** — Which module/component/file is primarily affected?
3. **Breaking changes** — Does it break existing APIs or behaviors?

### Step 3: Generate Commit Message

#### Quick Reference

| Type | When to Use |
|------|-------------|
| `feat` | User-facing new feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting changes |
| `refactor` | Code refactoring |
| `perf` | Performance optimization |
| `test` | Adding or modifying tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration |
| `chore` | Maintenance or tooling |
| `revert` | Reverting a previous commit |

#### Format Rules

```
<type>[(scope)]: <subject>

[body]

[footer]
```

### Step 4: Self-Check

Before outputting, check:
- [ ] Subject ≤72 characters
- [ ] Uses imperative mood ("add" not "added")
- [ ] Type matches the primary change
- [ ] No vague verbs unless essential
- [ ] Breaking changes noted in footer if applicable

## Common Mistakes

- Outputting explanations instead of the commit message.
- Using vague verbs or past tense.
- Forcing a scope when changes span multiple areas.
- Omitting `BREAKING CHANGE:` for breaking changes.

## Example Commit Messages

```
feat(api): add batch export endpoint
fix(ui): handle empty state rendering
docs: update install instructions
refactor(auth): split token validation
perf(db): reduce query round trips
test: cover edge cases in parser
build: bump pnpm to 9.0
ci: add lint job
chore: clean up temp scripts
revert: revert "feat: add oauth login"
```

## Best Practices

1. **Atomic Commits**: Each commit should represent a single, complete change.
2. **Frequent Commits**: Commit often, keeping commits small and focused.
3. **Pre-commit Checks**: Review changes with `git diff` and `git status` before committing.

## Conclusion

Good commit messages should:
1. Follow a consistent format.
2. Clearly describe the change.
3. Explain the reason for the change.
4. Be concise and clear.
5. Facilitate tracking and rollback.