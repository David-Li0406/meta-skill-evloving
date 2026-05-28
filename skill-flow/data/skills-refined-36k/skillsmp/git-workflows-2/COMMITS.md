# Commit Workflows

Detailed guide for Claude Code's commit process, conventions, and best practices.

## Claude's Commit Process

When asked to commit, Claude follows a strict protocol:

### Step 1: Information Gathering

Run these commands in parallel to understand the current state:

```bash
# All run simultaneously
git status                    # Untracked and modified files
git diff                      # Unstaged changes
git diff --staged             # Staged changes
git log --oneline -5          # Recent commit style reference
```

### Step 2: Change Analysis

Claude analyzes the gathered information:

1. **Identify scope**: What files/components are affected?
2. **Determine type**: Is this a feature, fix, refactor, etc.?
3. **Check for secrets**: Never commit `.env`, credentials, API keys
4. **Assess completeness**: Are all related changes included?

### Step 3: Draft Commit Message

Claude drafts a message that:
- Uses conventional commit format
- Focuses on "why" not "what"
- Matches the repository's existing style
- Summarizes changes in 1-2 sentences

### Step 4: Execute Commit

```bash
# Stage files
git add <specific-files>

# Commit with heredoc (required for proper formatting)
git commit -m "$(cat <<'EOF'
type(scope): concise description

Explanation of why this change was made.
Additional context if needed.

Co-authored-by: Claude <claude@anthropic.com>
EOF
)"

# Verify success
git status
```

### Step 5: Handle Failures

If the commit fails due to pre-commit hooks:
- NEVER use `--amend`
- Fix the identified issues
- Create a NEW commit

## Conventional Commits Specification

Format: `type(scope): description`

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation | `docs(readme): add installation guide` |
| `style` | Formatting | `style: apply prettier formatting` |
| `refactor` | Code restructure | `refactor(utils): simplify date parsing` |
| `perf` | Performance | `perf(query): add database index` |
| `test` | Tests | `test(auth): add login unit tests` |
| `build` | Build system | `build: update webpack config` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `revert` | Revert commit | `revert: revert "feat(auth): add OAuth2"` |

### Scope Guidelines

Scope should identify the affected component:

| Pattern | Examples |
|---------|----------|
| Feature area | `auth`, `api`, `dashboard`, `settings` |
| Layer | `frontend`, `backend`, `database` |
| Technology | `typescript`, `docker`, `webpack` |
| Package | `shared`, `core`, `utils` |

Scope is optional when changes span multiple areas:
```
feat: implement user profile system
```

### Description Rules

- Use imperative mood: "add" not "adds" or "added"
- No period at the end
- Max 50 characters for type + scope + description
- Lowercase (unless proper noun)

Good:
```
feat(auth): add password reset flow
fix(api): handle empty response body
refactor(utils): simplify error handling
```

Avoid:
```
feat(auth): Added password reset flow.  # Past tense, period
fix(api): Handles empty response body   # Third person
refactor(utils): simplifying errors     # Present participle
```

## Heredoc Syntax (Required)

Always use heredoc for commit messages. This ensures proper formatting of multi-line messages:

### Basic Format

```bash
git commit -m "$(cat <<'EOF'
type(scope): short description

Longer body explaining the change.
Can span multiple lines.
EOF
)"
```

### Why Heredoc?

1. **Preserves newlines**: Multi-line messages format correctly
2. **Handles special characters**: No escaping needed for quotes, `$`, etc.
3. **Readable**: Easy to write and review
4. **Consistent**: Same format works everywhere

### Single-Line Alternative

For simple commits, single-line is acceptable:
```bash
git commit -m "fix(api): correct null handling in user endpoint"
```

## Co-authored-by Attribution

When Claude contributes significantly, add attribution:

```bash
git commit -m "$(cat <<'EOF'
feat(api): implement rate limiting

Add request rate limiting with configurable thresholds.
Uses sliding window algorithm for accuracy.

Co-authored-by: Claude <claude@anthropic.com>
EOF
)"
```

### When to Include

- Claude wrote substantial code
- Claude designed the solution
- Pair programming with Claude

### Format

```
Co-authored-by: Name <email@example.com>
```

Must be:
- At the end of the commit body
- After a blank line
- Exact format (GitHub recognizes this)

## Multi-File Commits

### Grouping Strategy

Group related changes in single commits:

```bash
# Good: Related changes together
git add src/api/auth.ts src/api/auth.test.ts src/types/auth.ts
git commit -m "$(cat <<'EOF'
feat(auth): add JWT token validation

Implement token validation with:
- Signature verification
- Expiration checking
- Claim validation
EOF
)"

# Avoid: Unrelated changes together
git add src/api/auth.ts package.json README.md  # Different concerns
```

### Atomic Commits

Each commit should:
- Represent a single logical change
- Be independently deployable
- Pass all tests

### Partial Staging

Stage specific changes with:
```bash
# Stage specific files
git add src/feature.ts src/feature.test.ts

# Stage hunks (but NOT interactive mode)
git add -p src/mixed-changes.ts  # Use with caution
```

## Amend Rules (Critical Safety)

### When Amend is SAFE

All three conditions must be true:
1. User explicitly requested amend, OR pre-commit hook auto-modified files
2. HEAD commit was created by Claude in this conversation
3. Commit has NOT been pushed to remote

### Verification Commands

```bash
# Check who created the commit
git log -1 --format='%an %ae'

# Check if pushed
git status
# Look for: "Your branch is ahead of 'origin/branch' by X commits"
```

### Safe Amend Sequence

```bash
# 1. Verify authorship
git log -1 --format='%an %ae'
# Confirm it's Claude's commit

# 2. Verify not pushed
git status
# Must show "ahead" or no upstream

# 3. Stage new changes
git add <files>

# 4. Amend
git commit --amend --no-edit    # Keep same message
# OR
git commit --amend -m "..."     # New message
```

### When Amend is NEVER Safe

- Commit was rejected by hook (create new commit instead)
- Commit has been pushed to remote
- Commit was made by someone else
- User didn't request it

## Commit Validation Checklist

Before committing:

- [ ] Ran `git status` to see all changes
- [ ] Ran `git diff` to review changes
- [ ] No sensitive files (.env, credentials, keys)
- [ ] Commit message uses conventional format
- [ ] Commit message explains "why"
- [ ] Using heredoc for multi-line messages
- [ ] Related changes grouped together
- [ ] Tests pass (if required)

## Examples

### Feature Commit

```bash
git add src/features/dashboard/ src/types/dashboard.ts
git commit -m "$(cat <<'EOF'
feat(dashboard): add user activity widget

Display recent user actions in dashboard sidebar.
Widget shows last 10 activities with timestamps.

- Add ActivityWidget component
- Create useActivityFeed hook
- Define Activity type
EOF
)"
```

### Bug Fix Commit

```bash
git add src/api/users.ts
git commit -m "$(cat <<'EOF'
fix(api): handle null user preferences

Prevent crash when user has no saved preferences.
Return default preferences object instead of null.

Fixes #123
EOF
)"
```

### Refactor Commit

```bash
git add src/utils/
git commit -m "$(cat <<'EOF'
refactor(utils): consolidate date formatting functions

Merge duplicate date utilities into single module.
Improves consistency and reduces bundle size.

No functional changes.
EOF
)"
```

### Documentation Commit

```bash
git add README.md docs/
git commit -m "$(cat <<'EOF'
docs: add API authentication guide

Document authentication flow for new developers.
Include examples for all auth endpoints.
EOF
)"
```

### Multi-Author Commit

```bash
git commit -m "$(cat <<'EOF'
feat(search): implement fuzzy search algorithm

Add Levenshtein distance matching for typo tolerance.
Configurable threshold for match sensitivity.

Co-authored-by: Claude <claude@anthropic.com>
Co-authored-by: Developer <dev@example.com>
EOF
)"
```

## Handling Pre-Commit Hooks

### When Hooks Auto-Modify Files

If pre-commit hook (like prettier, eslint --fix) modifies files:

```bash
# 1. Commit attempt
git commit -m "..."
# Hook runs, modifies files, commit may succeed

# 2. If commit succeeded but files were modified
git add <auto-modified-files>
git commit --amend --no-edit  # Safe: same session, not pushed
```

### When Hooks Reject Commit

If pre-commit hook fails and blocks commit:

```bash
# 1. Commit attempt fails
git commit -m "..."
# Error: Pre-commit hook failed

# 2. Fix the issues
# Run linter, fix errors...

# 3. Create NEW commit (never amend)
git add <fixed-files>
git commit -m "..."  # New commit attempt
```

## Empty Commits

Never create empty commits. If `git status` shows:
- "nothing to commit, working tree clean"
- No untracked files
- No modifications

Do NOT attempt to commit. Report to user that there are no changes.
