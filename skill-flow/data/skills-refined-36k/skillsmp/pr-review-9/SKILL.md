---
name: pr-review
description: Full PR review workflow with checklist verification and release notes. Use when reviewing PRs before merge.
license: MIT
compatibility: Requires git CLI and gh (GitHub CLI).
metadata:
  author: shipitsmarter
  version: "2.0"
---

# PR Review Skill

Complete pull request review: verify checklist, check code quality, write release notes, update PR on GitHub.

**For quick code quality checks only**, use the `code-review` skill instead.

---

## Trigger

When user asks to:
- Review a PR
- Check PR checklist
- Write release notes for a PR
- Validate code before merge

---

## Process Overview

| Step | Action | Tool/Skill |
|------|--------|------------|
| 0 | Check branch is up-to-date | `git-branch-update` skill |
| 1 | Detect PR, gather context | `gh pr view` |
| 2 | Run automated checks | `npm run lint && type-check` |
| 3 | Review code conventions | `code-review` skill |
| 4 | Evaluate test coverage | Decision framework below |
| 5 | Check plan completion | If plan file exists |
| 6 | Generate review report | Template below |
| 7 | Update PR (with confirmation) | `gh api` |

---

## Step 0: Verify Branch is Mergeable

**Use the `git-branch-update` skill** if branch is behind main.

Quick check:
```bash
git fetch origin main
git rev-list --left-right --count origin/main...HEAD
# If first number > 0, branch needs update
```

**Always ask before rebasing/merging** - don't auto-update.

---

## Step 1: Detect PR & Gather Context

```bash
# Get PR details
gh pr view --json number,title,body,url,headRefName

# Get all commits
git log origin/main..HEAD --oneline

# Get changed files
gh pr diff --name-only

# Get full diff
gh pr diff
```

---

## Step 2: Run Automated Checks

```bash
npm run lint
npm run type-check
npm run build-only:prod
```

Any errors are **blocking issues**. Report them first.

---

## Step 3: Review Code Conventions

**Load the `code-review` skill** for detailed convention checking:
- Component script order
- Import rules
- TypeScript rules  
- Template rules
- Debug code removal

---

## Step 4: Evaluate Test Coverage

| Change Type | Tests Needed |
|-------------|--------------|
| New composable (`use*.ts`) | Unit tests |
| New utility function | Unit tests |
| New page/view | E2E test |
| Bug fix | Test reproducing the bug |
| Refactoring only | Existing tests pass |
| Styling/text only | No tests |

**Check for missing tests:**
```bash
# Find source files without tests
gh pr diff --name-only | grep -E '\.(vue|ts)$' | grep -v '\.spec\.'
```

---

## Step 5: Check Plan Completion (If Applicable)

> **Note:** This step only applies if your project uses plan files. Skip if not applicable.

If a plan file exists for this feature, verify:
- [ ] All tasks completed
- [ ] Open questions resolved
- [ ] Release type defined (silent/standard/gradual/breaking)

For **gradual releases** (feature flags), also check:
- [ ] Feature flag name defined
- [ ] Documentation updated

---

## Step 6: Generate Review Report

```markdown
## PR Review: #<number> - <title>

**Branch:** `<branch>` → `main`  
**Files changed:** <count>

### Checklist Status

| Item | Status |
|------|--------|
| Lint & type-check | ✅ Pass |
| Code conventions | ✅ Pass |
| Unit tests | ⚠️ Missing for 1 file |
| Sanity check | ✅ Pass |

### Issues

**Blocking:**
- [List or "None"]

**Warnings:**
- [Optional fixes]

### Release Notes

#### 🚀 New
- **Feature name** - User-facing benefit description

#### ⚙️ Improved
- [Improvements]

#### 🐞 Fixed
- [Bug fixes]

### Verdict

**[APPROVE / CHANGES REQUESTED / NEEDS DISCUSSION]**
```

---

## Step 7: Update PR on GitHub

**Always ask for confirmation before updating.**

```markdown
Review complete. Do you want me to:
1. Check off passing items in the PR checklist?
2. Add release notes to the PR description?

Confirm? [y/N]
```

### Update PR Body

```bash
# Write new body to temp file
cat > /tmp/pr-body.md << 'EOF'
[PR body content with release notes and checklist]
EOF

# Update via API (more reliable than gh pr edit)
gh api repos/{owner}/{repo}/pulls/{pr_number} -X PATCH -f body="$(cat /tmp/pr-body.md)"
```

---

## Release Notes Format

```markdown
## Release Notes

### 🚀 New
- **Feature name** - User benefit, not technical details

### ⚙️ Improved  
- **Area** - What's better for users

### 🐞 Fixed
- **Issue** - What was broken, now resolved

### ⚙️ Internal
- Technical changes (for non-user-facing PRs)
```

**Writing tips:**
- Focus on user benefits
- Active voice: "You can now..." not "Added ability to..."
- 1-2 sentences per item

---

## PR Checklist Reference

Standard checklist items to verify:

```markdown
- [ ] No errors from eslint & prettier
- [ ] Components nicely structured
- [ ] Core functionality covered with unit tests
- [ ] Changes comply with conventions
- [ ] Sanity check completed
```

---

## Quick Commands

```bash
# Full check suite
npm run lint && npm run type-check && npm run build-only:prod

# PR details
gh pr view

# Changed files
gh pr diff --name-only

# Full diff
gh pr diff

# Open in browser
gh pr view --web
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `code-review` | Quick convention check (no PR workflow) |
| `git-branch-update` | Update branch with main |
| `vue-component` | Component conventions detail |
| `unit-testing` | Write missing unit tests |
| `playwright-test` | Write missing E2E tests |
