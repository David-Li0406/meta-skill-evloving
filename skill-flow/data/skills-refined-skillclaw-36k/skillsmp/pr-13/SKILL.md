---
name: pr
description: How Matt creates pull requests - branch naming, commit style, PR workflow
---

# Pull Request Workflow

Follow this workflow when contributing changes to any repository.

## Never Push Directly to Main

Always create a branch and PR, even for small changes, unless specifically told otherwise. This applies to:

- Matt's own repos
- Open source contributions
- Work repos

## Branch Naming

Use descriptive kebab-case branch names:

```
feat/add-opencode-detection
fix/calendar-permission-error
docs/update-setup-guide
refactor/simplify-scheduler
```

Prefixes:

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code restructuring
- `chore/` - Maintenance, dependencies

## Workflow

### 1. Create a branch from main

```bash
git checkout main
git pull
git checkout -b feat/my-feature
```

### 2. Make changes and commit

Use conventional commit messages:

```bash
git add -A
git commit -m "feat: add OpenCode detection via OPENCODE env var"
```

Commit message format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code change that neither fixes nor adds
- `chore:` - Maintenance

### 3. Check for changesets

If the repo uses changesets (has `.changeset/` directory), and your change needs a release (features, fixes - not docs/chore), create one:

```bash
# Check if changesets is used
ls .changeset/config.json

# Create a changeset
pnpm changeset
# or
npx changeset
```

This opens an interactive prompt:

1. Select which packages changed (space to select, enter to confirm)
2. Choose bump type: `patch` (fixes), `minor` (features), `major` (breaking)
3. Write a summary of the change

This creates a markdown file in `.changeset/` like:

```markdown
---
"am-i-vibing": minor
---

Add OpenCode detection via OPENCODE env var
```

Commit the changeset file with your other changes.

**When to create a changeset:**

- `feat:` → minor bump
- `fix:` → patch bump
- `docs:`, `chore:`, `refactor:` → usually no changeset needed

### 4. Run tests

Before pushing, run tests to catch issues early:

```bash
pnpm test
# or
npm test
```

Fix any failing tests. If your change affects existing tests, update them.

### 5. Push the branch

```bash
git push -u origin feat/my-feature
```

### 6. Create PR with gh CLI

```bash
gh pr create --title "feat: add OpenCode detection" --body "$(cat <<'EOF'
## Summary

- Added OPENCODE env var to detection
- Renamed sst-opencode to opencode

## Testing

Ran `npx am-i-vibing` in OpenCode session - now detects correctly.
EOF
)"
```

### 7. After PR is merged

```bash
git checkout main
git pull
git branch -d feat/my-feature
```

## PR Body Template

```markdown
## Summary

[1-3 bullet points describing what changed]

## Testing

[How you verified the change works]

## Notes

[Any additional context, breaking changes, etc.]
```

## If You Accidentally Pushed to Main

If changes were pushed directly to main that should have been a PR:

```bash
# Create a branch at the current commit
git branch feat/my-feature

# Reset main to before your commits
git checkout main
git reset --hard origin/main~N  # N = number of commits to undo

# Push the reset (if you pushed to remote)
git push --force-with-lease

# Push the feature branch
git checkout feat/my-feature
git push -u origin feat/my-feature

# Create PR
gh pr create
```
