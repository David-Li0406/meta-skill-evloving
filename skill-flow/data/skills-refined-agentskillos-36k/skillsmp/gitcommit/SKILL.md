---
name: git:commit
description: Smart Commit - creates a conventional commit with auto-detected or user-selected type
---

# Smart Commit

Analyzes staged changes and creates a commit following Conventional Commits specification. Automatically detects the commit type when obvious, or asks the user to choose when ambiguous.

## When to use

Use this skill when the user needs to:
- Create a well-formatted commit message
- Follow Conventional Commits specification
- Commit changes without thinking about message format

## Instructions

### Step 1: Check Staged Changes

1. Run `git status --porcelain` to see current state
2. Run `git diff --cached --stat` to see staged changes summary
3. Run `git diff --cached` to get the full diff for analysis

If no changes are staged:
- Show unstaged changes and ask if user wants to stage them
- Offer to run `git add -A` or let user specify files
- After staging, continue with analysis

### Step 2: Analyze Changes

Examine the diff to understand what changed:

1. **Files affected** - Which files were modified/added/deleted
2. **Nature of changes** - New feature, bug fix, refactoring, etc.
3. **Scope** - Which part of the codebase (component, module, service)

### Step 3: Determine Commit Type

**Auto-detect when obvious:**

| Pattern | Type | Confidence |
|---------|------|------------|
| New files in `src/` with new functionality | `feat` | High |
| Changes to test files only | `test` | High |
| Changes to docs/README/CHANGELOG | `docs` | High |
| `package.json` deps only | `chore` | High |
| CI/CD config files only (`.github/`, `.gitlab-ci.yml`) | `ci` | High |
| Fix in code with "bug", "error", "issue" context | `fix` | Medium |
| Code restructuring without behavior change | `refactor` | Medium |
| Performance-related changes | `perf` | Medium |

**Ask user when ambiguous:**

If confidence is low or multiple types could apply, present options:

```
Changes detected in: src/auth/login.ts, src/auth/utils.ts

What type of change is this?
- feat: New feature
- fix: Bug fix
- refactor: Code restructuring
- perf: Performance improvement
- Other (specify)
```

### Step 4: Determine Scope

1. Identify the main area affected:
   - Single directory/module → use as scope (e.g., `auth`, `api`, `ui`)
   - Multiple related areas → use common parent or primary area
   - Widespread changes → omit scope

2. Use lowercase, short scope names (1-2 words max)

### Step 5: Generate Commit Message

Format: `<type>(<scope>): <description>`

**Rules:**
- Description in imperative mood ("add" not "added")
- Start with lowercase
- No period at the end
- Max 72 characters for first line
- Be specific but concise

**Good examples:**
```
feat(auth): add password reset flow
fix(api): handle null response from payment service
refactor(utils): extract date formatting to shared module
docs(readme): add installation instructions
test(auth): add unit tests for login validation
chore(deps): update axios to 1.6.0
```

**Bad examples:**
```
feat: stuff                    # Too vague
fix(auth): Fixed the bug       # Past tense, capitalized
feat(authentication-module): add new feature  # Scope too long, description vague
```

**Important:** Do NOT add `Co-Authored-By`, `Signed-off-by`, or any other trailers to the commit message.

### Step 6: Present and Confirm

Show the user:
```
Staged: 3 files (+45, -12 lines)

Commit message:
  feat(auth): add password reset flow

Proceed with commit? [Y/n]
```

If user approves, run `git commit -m "<message>"`

If user wants to modify, let them edit and retry.

### Step 7: Handle Breaking Changes

If the change breaks backward compatibility:

1. Add exclamation mark after type/scope, for example: **feat(api)!: change response format**
2. Or add BREAKING CHANGE: in commit body for details:

```
feat(api)!: change response format

BREAKING CHANGE: Response now returns data in `items` array instead of `data` object.
Migration: Update client code to access response.items instead of response.data
```

## Conventional Commits Reference

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, white-space (no code change) |
| `refactor` | Code change that neither fixes nor adds feature |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Other changes (tooling, config) |
| `revert` | Reverts a previous commit |

## Arguments

- `<args>` - Optional. Can include:
  - Commit type: `feat`, `fix`, `docs`, etc.
  - Scope: `(auth)`, `(api)`, etc.
  - Full message: `"feat(auth): add login"`

Examples:
- `git:commit` - Auto-detect type and generate message
- `git:commit fix` - Create a fix commit
- `git:commit feat(auth)` - Create a feat commit with auth scope
- `git:commit "docs: update readme"` - Use exact message provided
