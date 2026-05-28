---
name: github-workflow
description: PR workflow, release notes, build management, and GitHub conventions. Use when creating PRs, writing commit messages, or preparing releases.
license: MIT
compatibility: Requires git CLI and gh (GitHub CLI) for PR operations.
metadata:
  author: shipitsmarter
  version: "1.0"
---

# GitHub Workflow Skill

Quick reference for Git and GitHub conventions. For comprehensive PR review process, see the **pr-review** skill.

> **Note:** This skill provides quick-lookup conventions. For full PR review automation, checklist verification, and code review process, use the `pr-review` skill instead.

---

## Branch naming

Branch names MUST follow this pattern:

```
<type>/<kebab-case-description>
```

**Allowed types:**
- `feat` - New feature
- `fix` - Bug fix
- `chore` - Maintenance tasks
- `docs` - Documentation only
- `refactor` - Code refactoring
- `test` - Adding/fixing tests
- `style` - Code style changes
- `perf` - Performance improvements
- `build` - Build system changes
- `ci` - CI configuration
- `revert` - Reverting changes

**Examples:**
- `feat/shipment-bulk-actions`
- `fix/address-validation-error`
- `chore/update-dependencies`
- `docs/api-integration-guide`

**Invalid:**
- `feature/my-feature` (wrong prefix)
- `feat/MyFeature` (not kebab-case)
- `my-feature` (missing type prefix)

---

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<optional scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature for users |
| `fix` | Bug fix for users |
| `docs` | Documentation changes |
| `style` | Formatting, semicolons, etc. |
| `refactor` | Code change that doesn't fix or add features |
| `perf` | Performance improvements |
| `test` | Adding or fixing tests |
| `chore` | Maintenance tasks |
| `build` | Build system or dependencies |
| `ci` | CI configuration |
| `revert` | Reverting a previous commit |

### Examples

```
feat(shipment): add bulk action buttons to list view

fix(address): resolve validation error on special characters

chore: update viya-ui-warehouse to v2.3.0

refactor(pickup): extract date picker logic to composable
```

### Rules (enforced by commitlint)

- Subject must NOT be in UPPER_CASE
- Subject should be lowercase (sentence case allowed in body)
- No period at the end of subject line

---

## Pull request template

PRs should include:

```markdown
## Title
Short summary what this PR is about

## Description and/or Additional context
More detailed description, links to related issues/PRs

## Steps how to check/verify
Steps to reproduce or verify the changes

## Screenshots
[If UI changes]

## Affected customers (if any)
[List affected tenants/customers]

## Planned release date
[Target release date]

## My PR created in accordance:
- [ ] no errors from eslint & prettier
- [ ] components are nicely structured
- [ ] core functionality covered with unit tests
- [ ] changes comply with general conventions
- [ ] sanity check done (no console.logs, unnecessary comments)
- [ ] I confirm I've checked all boxes truthfully :)
```

---

## Writing PR descriptions

### Voice & tone

- Friendly, confident, customer-focused
- Focus on benefits, not just features
- Avoid internal jargon

### Structure for feature PRs

```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- Added bulk action buttons to shipment list
- Implemented selection state management
- Added confirmation dialogs for destructive actions

## Testing
How to test these changes:
1. Navigate to Shipments list
2. Select multiple shipments
3. Click bulk action button
4. Verify confirmation dialog appears

## Screenshots
[Include before/after if UI changes]
```

### Structure for bug fix PRs

```markdown
## Summary
Fixes [issue description or link]

## Root cause
Brief explanation of what was causing the bug.

## Solution
How the fix addresses the root cause.

## Testing
Steps to verify the fix works.
```

---

## Release notes

Release notes are auto-generated from PR labels.

### Labels for release categorization

| Label | Release section |
|-------|-----------------|
| `Semver-Major`, `breaking-change` | Breaking Changes |
| `Semver-Minor`, `enhancement` | Exciting New Features |
| `*` (default) | Other Changes |
| `ignore-for-release` | Excluded from notes |

### Writing user-facing release notes

When a PR includes user-facing changes, write the PR title for customers:

**Good (customer-focused):**
- "Add bulk actions for managing multiple shipments at once"
- "Fix address validation failing on special characters"
- "Improve shipment list loading performance"

**Bad (developer-focused):**
- "Refactor ShipmentList component"
- "Fix issue #123"
- "Update state management"

---

## Checking build status

After pushing, verify the CI build passes:

```bash
# Check PR status using GitHub CLI
gh pr checks

# View PR in browser
gh pr view --web

# Check workflow runs
gh run list --limit 5
```

### Common build failures

| Issue | Solution |
|-------|----------|
| Lint errors | Run `npm run lint:fix` |
| Type errors | Run `npm run type-check` |
| Test failures | Run `npm test` locally |
| Build errors | Run `npm run build-only:prod` |

---

## Pre-commit hooks

The following checks run automatically on commit:

1. **Branch name validation** - Enforces naming pattern
2. **Warehouse version check** - Ensures compatible UI library
3. **Lint-staged** - Runs linting on staged files

If a commit fails:

```bash
# Fix lint errors
npm run lint:fix

# Format code
npm run format

# Try committing again
git commit -m "your message"
```

---

## Keeping PRs up to date

### Rebasing on main

```bash
# Fetch latest main
git fetch origin main

# Rebase your branch
git rebase origin/main

# Force push (only for your own branches)
git push --force-with-lease
```

### Updating PR description

As you iterate, keep the PR description current:
- Update testing steps if behavior changed
- Add new screenshots for UI changes
- Note any breaking changes

---

## Merging PRs

### Before merging

- [ ] Branch is up to date with main
- [ ] All CI checks pass
- [ ] At least one approval from reviewer
- [ ] PR description is up to date
- [ ] No unresolved comments

### Merge strategy

Use **Squash and merge** for most PRs to keep history clean.

---

## GitHub CLI commands

```bash
# Create PR
gh pr create --title "feat: add feature" --body "Description"

# List your PRs
gh pr list --author @me

# Check out a PR locally
gh pr checkout 123

# View PR status
gh pr status

# Request review
gh pr edit --add-reviewer username

# Merge PR
gh pr merge --squash
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **pr-review** | Full PR review automation with checklist verification |
| **docs-writing** | Writing user documentation for releases |

---

## Quick Checklist

For quick self-review before requesting PR review:

- [ ] Branch up to date with main
- [ ] Branch name: `<type>/kebab-case-name`
- [ ] Commit messages: conventional commits
- [ ] PR description: uses template
- [ ] Title: customer-focused (for user-facing changes)
- [ ] Labels: appropriate labels added
- [ ] CI: all checks pass

For comprehensive review, use: `pr-review` skill
