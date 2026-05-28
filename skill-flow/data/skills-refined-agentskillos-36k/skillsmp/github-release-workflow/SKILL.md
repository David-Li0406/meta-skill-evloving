---
name: GitHub Release Workflow
description: Guide for creating releases following GitFlow, version bumping, changelog updates, and CI/CD pipeline
---

# GitHub Release Workflow Skill

This skill guides the complete release process for the SOMA theme, from version preparation to production deployment.

## When to Use This Skill

Use this skill when you need to:
- Create a new version release (patch, minor, major)
- Update CHANGELOG.md with release notes
- Follow GitFlow branching strategy
- Deploy to production via CI/CD
- Hotfix production issues

## Release Types

| Type | Version Change | When to Use |
|------|----------------|-------------|
| **Patch** | 3.1.15 → 3.1.16 | Bug fixes, small improvements |
| **Minor** | 3.1.x → 3.2.0 | New features, backward compatible |
| **Major** | 3.x.x → 4.0.0 | Breaking changes |

## GitFlow Branch Strategy

```
main (production)
 ↑
 └── week-N (sprint branch)
      ↑
      ├── feature/description
      ├── fix/description
      └── release/vX.Y.Z
```

### Branch Rules

| Branch | Purpose | Merge Target |
|--------|---------|--------------|
| `main` | Production code | ← week-N only |
| `week-N` | Sprint development | ← feature/*, fix/* |
| `feature/*` | New features | → week-N |
| `fix/*` | Bug fixes | → week-N |
| `hotfix/*` | Emergency fixes | → main |
| `release/*` | Release preparation | → week-N → main |

## Standard Release Process

### Step 1: Pre-Release Checks

```bash
cd wp-content/themes/soma

# Run ALL quality checks (must pass)
composer phpcs        # 0 errors required
composer phpstan      # Level 6+, 0 critical errors
composer test         # All 108+ tests must pass
npm run prod          # Frontend build must succeed
```

### Step 2: Create Release Branch

```bash
# From current sprint branch
git checkout week-N
git pull origin week-N
git checkout -b release/vX.Y.Z
```

### Step 3: Update Version Files

**File 1: `style.css`**
```css
/*
Theme Name: SOMA
...
Version: X.Y.Z    ← Update this
*/
```

**File 2: `CHANGELOG.md`**

```markdown
## [Unreleased]
↓ Change to ↓
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

### Step 4: Commit Version Bump

```bash
git add style.css CHANGELOG.md
git commit -m "chore: Prepare release vX.Y.Z"
git push -u origin release/vX.Y.Z
```

### Step 5: Create PR to Sprint Branch

**🏷️ REQUIRED: Always include labels in PR creation**

```bash
gh pr create \
  --title "Release vX.Y.Z" \
  --body "## Release vX.Y.Z

### Changes
See CHANGELOG.md for details.

### Quality Gates
- ✅ PHPCS clean
- ✅ PHPStan Level 6
- ✅ All tests passing
- ✅ Frontend build successful" \
  --base week-N \
  --label "release,chore" | cat

# Wait for CI, then merge
gh pr merge NUMBER --squash --delete-branch | cat
```

### Step 6: Merge Sprint to Main

```bash
# Create PR from sprint to main
gh pr create \
  --title "Release vX.Y.Z to production" \
  --base main \
  --head week-N \
  --label "release" | cat

# After CI passes and approval
gh pr merge NUMBER --squash | cat
```

### Step 7: Create Release Tag (CRITICAL)

```bash
# ⚠️ CRITICAL: Tags MUST be created from main AFTER merge
git checkout main
git pull origin main

# Verify you're on the correct commit
git log -1 --oneline

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z: Description"

# Push tag (triggers CI/CD)
git push origin vX.Y.Z
```

### Step 8: Monitor Deployment

```bash
# Watch workflow execution
gh run watch

# Or list runs
gh run list --workflow=ci-cd.yml --limit 5 | cat

# View release
gh release view vX.Y.Z | cat
```

## Hotfix Workflow (Emergency)

```bash
# 1. Create hotfix from main (NOT week-N)
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# 2. Apply fix and run quality checks
composer test && npm run prod

# 3. Update version (patch increment only)
# style.css: 3.1.15 → 3.1.16
# CHANGELOG.md: Add hotfix entry

# 4. Commit and push
git add .
git commit -m "fix: Critical security vulnerability"
git push -u origin hotfix/critical-issue

# 5. Create PR directly to main
gh pr create \
  --title "HOTFIX: Critical issue" \
  --base main \
  --label "bug,security,alta-prioridad" | cat

# 6. After emergency approval, merge and tag
gh pr merge NUMBER --squash | cat
git checkout main
git pull origin main
git tag -a v3.1.16 -m "Hotfix v3.1.16: Security patch"
git push origin v3.1.16

# 7. Backport to sprint (if needed)
git checkout week-N
git cherry-pick COMMIT_SHA
git push origin week-N
```

## CHANGELOG.md Format

```markdown
# Changelog

All notable changes to the SOMA WordPress theme will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [X.Y.Z] - YYYY-MM-DD

### Category/Feature Name

#### ✨ Added
- **Feature Name** - Brief description (#issue-number)

#### 🔄 Changed
- **Component** - What changed and why

#### 🐛 Fixed
- **Bug Name** - What was fixed (#issue-number)

#### 🗑️ Removed
- **Feature** - What was removed and why

### 📦 Files Changed

#### Added
- `path/to/new/file.php` - Purpose

#### Modified
- `path/to/modified/file.php` - What changed

---

### 🔗 Related Issues & PRs
- **Issue #XX**: [Title](URL) - Closed
- **PR #XX**: [Title](URL) - Merged
```

## CI/CD Pipeline Stages

When you push a tag `vX.Y.Z`:

### Stage 1: Quality Gates (~2 min)
- `code-quality`: PHPCS + PHPStan
- `php-tests`: PHPUnit tests
- `frontend-build`: npm production build

### Stage 2: Build & Release (~3 min)
- Install production dependencies
- Create release ZIP (excluding dev files)
- Extract changelog for release notes
- Create GitHub Release
- Upload ZIP artifact

### Stage 3: Deploy (~2 min)
- Download release ZIP
- SFTP upload to production
- Create backup of current theme
- Extract new version

### Stage 4: Summary
- Report all stage results

## Version Commit Messages

```bash
# Release preparation
git commit -m "chore: Prepare release v3.1.16"

# Changelog update
git commit -m "docs: Update CHANGELOG for v3.1.16"

# Combined
git commit -m "chore(release): Bump version to 3.1.16 and update changelog"
```

## GitHub CLI Commands Reference

```bash
# Always use | cat to prevent pagination

# Issues
gh issue list --milestone "Week N" | cat
gh issue close NUMBER --comment "Fixed in PR #XX" | cat

# Pull Requests
gh pr create --base week-N --title "Title" | cat
gh pr list | cat
gh pr checks NUMBER | cat
gh pr merge NUMBER --squash --delete-branch | cat

# Releases
gh release list | cat
gh release view vX.Y.Z | cat
# NEVER use gh release create - releases created by CI/CD

# Workflows
gh run list --workflow=ci-cd.yml | cat
gh run watch
gh run view RUN_ID | cat

# Milestones
gh api repos/sanruiz/fibra/milestones | jq '.[] | {number, title, state}' | cat
gh api repos/sanruiz/fibra/milestones/N -X PATCH -f state=closed | cat
```

## Common Issues

### Tag Created from Wrong Branch

**Problem**: Tag created from `week-N` instead of `main` becomes orphaned after squash merge.

**Solution**:
```bash
# Delete wrong tag
git tag -d vX.Y.Z
git push origin --delete vX.Y.Z

# Create correct tag from main
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

### CI Failing on Release

**Problem**: Quality checks failing during release

**Solution**:
```bash
# Check what failed
gh pr checks NUMBER | cat

# Fix locally first
composer phpcs
composer phpstan
composer test

# Then update release branch
```

### Deployment Failed

**Problem**: Stage 3 (Deploy) failed

**Solutions**:
1. Check SFTP credentials in repo secrets
2. Verify server connectivity
3. Re-trigger workflow:
```bash
gh workflow run ci-cd.yml -f version=X.Y.Z
```

## Pre-Release Checklist

- [ ] All feature PRs merged to `week-N`
- [ ] Quality checks pass locally
  - [ ] `composer phpcs` (0 errors)
  - [ ] `composer phpstan` (Level 6+)
  - [ ] `composer test` (all passing)
  - [ ] `npm run prod` (successful)
- [ ] Version updated in `style.css`
- [ ] CHANGELOG.md updated with release notes
- [ ] Related issues closed
- [ ] PR created with appropriate labels (`--label "release,..."`)
- [ ] PR approved and merged
- [ ] Tag created from `main` (not `week-N`)
- [ ] CI/CD pipeline completed successfully
- [ ] Production site verified

## Post-Release Checklist

- [ ] Verify deployment on production
- [ ] Test critical user paths
- [ ] Check error logs (`soma-logs/soma.log`)
- [ ] Close milestone if applicable
- [ ] Announce release (if public)
- [ ] Merge main back to week-N (if continuing sprint)
