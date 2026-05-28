---
name: git
description: |
  Git automation skill. Provides task selection UI when /git command is executed.
  Choose from commit, push, sync, merge operations.
model: opus
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Git Automation Skill

Select a task when the `/git` command is executed.

## Argument Parsing

Parse the `args` parameter when the skill is invoked to separate the action and message.

### Parsing Rules

| Input Example | Parsing Result |
|---------------|----------------|
| (none) | action=none, message=none |
| `"Login feature"` | action=none, message="Login feature" |
| `commit` | action=commit, message=none |
| `commit "Login feature"` | action=commit, message="Login feature" |
| `sync` | action=sync, message=none |
| `sync "Login feature"` | action=sync, message="Login feature" |
| `push` | action=push |
| `merge` | action=merge |

### Parsing Method

1. If args starts with quotes → treat entire content as message (no action)
2. If args starts with `commit`, `sync`, `push`, `merge` → use that value as action, rest as message
3. Otherwise → no action, treat entire content as message

## Execution Flow

### 1. If no action → Display task selection UI

**Call AskUserQuestion tool to provide task selection UI.**

#### If no message:

```json
{
  "questions": [
    {
      "header": "Git Task",
      "question": "Which Git operation would you like to perform?",
      "multiSelect": false,
      "options": [
        { "label": "commit", "description": "Analyze changes and commit" },
        { "label": "push", "description": "Push current branch" },
        { "label": "sync", "description": "Full workflow: add → commit → push" },
        { "label": "merge", "description": "Trunk-based merge (current branch → main)" }
      ]
    }
  ]
}
```

#### If message exists (e.g., `/git "Login feature"`):

```json
{
  "questions": [
    {
      "header": "Git Task",
      "question": "Which Git operation would you like to perform? (message: \"Login feature\")",
      "multiSelect": false,
      "options": [
        { "label": "commit", "description": "Commit with provided message" },
        { "label": "sync", "description": "add → commit → push with provided message" },
        { "label": "push", "description": "Push current branch (message not used)" },
        { "label": "merge", "description": "Trunk-based merge (message not used)" }
      ]
    }
  ]
}
```

**When Other is selected from UI:**
- Treat input as message for commit/sync operations

### 2. If action exists → Execute that operation directly

| action | message | behavior |
|--------|---------|----------|
| commit | none | Auto-generate message and commit |
| commit | exists | Commit with provided message |
| sync | none | Auto-generate message then add → commit → push |
| sync | exists | add → commit → push with provided message |
| push | - | Push immediately |
| merge | - | Ask about branch deletion, then merge |

### 3. Reference Documents by Operation

| Operation | Reference Document |
|-----------|-------------------|
| commit | [references/commit.md](references/commit.md) |
| push | [references/push.md](references/push.md) |
| sync | [references/sync.md](references/sync.md) |
| merge | [references/merge.md](references/merge.md) |

## Common Rules

### Commit Message Format (Conventional Commits)

```
<emoji> <type>[scope][!]: <description>

- [detailed change 1]
- [detailed change 2]
```

### Type & Emoji Map

| Type | Emoji | Usage |
|------|-------|-------|
| `feat` | ✨ | New feature |
| `fix` | 🐛 | Bug fix |
| `docs` | 📝 | Documentation changes |
| `style` | 💄 | Code style |
| `refactor` | ♻️ | Refactoring |
| `perf` | ⚡ | Performance improvement |
| `test` | ✅ | Tests |
| `chore` | 🔧 | Config/build |
| `ci` | 🚀 | CI/CD |
| `build` | 📦 | Build system |
| `revert` | ⏪ | Revert |

Detailed rules: [references/commit-prefix-rules.md](references/commit-prefix-rules.md)

### Commit Message Rules

- **Subject under 72 characters** (including emoji + type + scope)
- **Imperative mood** ("Add" not "Added")
- **Atomic commits** (single purpose)
- Split unrelated changes

### Language Rules

- Commit messages: **Korean**
- Variable/function names: **English**

### Prohibited [Important]

- ❌ **Do NOT use `Co-Authored-By` pattern** (e.g., `Co-Authored-By: Claude ...`)
- ❌ **Do NOT use non-standard types** (types not in the table above)
- ❌ **Do NOT use `hotfix:` type** → Use `fix`
- ❌ **Do NOT use `merge:` type** → Use Git auto-generated message
- ❌ **No force push**

## Reference Documents

- [Commit Workflow](references/commit.md)
- [Push Workflow](references/push.md)
- [Sync Workflow](references/sync.md)
- [Merge Workflow](references/merge.md)
- [Commit Prefix Rules](references/commit-prefix-rules.md)
