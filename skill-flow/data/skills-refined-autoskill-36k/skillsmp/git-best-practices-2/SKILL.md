---
name: git-best-practices
description: Safe-by-default git workflow and Conventional Commits. Triggers on git operations, reviewing diffs, staging files, creating commits, or branch changes. Prevents destructive operations without consent.
---

# Git Best Practices

## Safety Rules

- **Read-only by default**: `git status`, `git diff`, `git log` are always safe
- **Push requires explicit request**: Never push unless user asks
- **Checkout allowed for**: PR review, explicit user request
- **Branch changes require consent**: Ask before creating/switching branches
- **Destructive ops forbidden** unless explicit user consent:
  - `reset --hard`
  - `clean`
  - `restore`
  - `rm`
  - Force push

## Commit Planning

When reviewing changes for commits:

1. Review all staged and unstaged changes
2. Identify untracked files, ignored files, and anything that should not be committed
3. Propose clean commit groups that are logically related and minimal
4. Explain which files belong to each commit and why
5. If there are dependencies between commits, order them
6. If files should be removed or ignored, say so explicitly

## Conventional Commits

Format: `<type>[optional scope][optional !]: <description>`

### Types

| Type | Use for |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no code change) |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvements |
| `test` | Adding or correcting tests |
| `build` | Build system or dependencies |
| `ci` | CI configuration |
| `chore` | Other changes (tooling, config) |
| `revert` | Reverting a previous commit |

### Scope

- Use the smallest sensible scope
- Omit scope if unclear or too broad
- Examples: `feat(auth):`, `fix(api):`, `docs(readme):`

### Breaking Changes

Mark with `!` before the colon OR add a `BREAKING CHANGE:` footer:

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: /v1/users endpoint removed, use /v2/users
```

### Body and Footers

- Use body only when the subject line needs elaboration
- Footers follow git-trailer style: `Token: value`
- Common footers: `BREAKING CHANGE:`, `Fixes:`, `Refs:`, `Co-authored-by:`

### Examples

```
feat(auth): add OAuth2 login flow

fix: prevent race condition in queue processing

docs: update API authentication examples

refactor(db)!: migrate from MySQL to PostgreSQL

BREAKING CHANGE: database connection config format changed
```

## Workflow

After reviewing changes, end with:
1. Short summary of proposed commits
2. Clear question for next steps (stage/commit/push)

If anything is ambiguous, ask short, direct questions with options.
