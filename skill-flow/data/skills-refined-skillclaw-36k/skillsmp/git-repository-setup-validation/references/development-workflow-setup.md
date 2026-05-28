# Development Workflow Setup Guidelines

Guidelines for setting up development branch workflow for agentic development.

---

## Overview

**Workflow Pattern**: Development Branch Integration

```
main (protected)
  └── development (unprotected integration branch)
       ├── epic-X-name (epic branch)
       │    ├── feature-X.Y-name (feature branch)
       │    │    └── [commits for waves X.Y.1, X.Y.2, ...]
       │    └── feature-X.Z-name (feature branch)
       │         └── [commits for waves X.Z.1, X.Z.2, ...]
       ├── wave-A.B.C-standalone (standalone wave)
       └── hotfix-description (hotfix branch)
```

**Key Principles**:
1. `main` is protected production branch
2. `development` is unprotected integration branch
3. All work branches from `development`
4. PRs merge through: feature → epic → development → main
5. Only `development → main` PRs allowed

---

## Branch Purposes

### Main Branch

**Purpose**: Production-ready code

**Protection**: MUST be protected
- Require PR reviews
- Require status checks (PR branch validation)
- Restrict direct pushes
- Require linear history

**Merge Source**: Only `development` branch

**Characteristics**:
- Always deployable
- Linear history
- Tagged releases
- Never work directly on main

---

### Development Branch

**Purpose**: Integration branch for all active work

**Protection**: Should NOT be protected
- Allows direct merges from feature/epic branches
- No PR overhead for agent-driven merges
- Flexible for rapid iteration

**Merge Sources**:
- Epic branches (after feature integration)
- Feature branches (standalone features)
- Standalone wave branches
- Hotfix branches

**Merge Target**: `main` (via PR)

**Characteristics**:
- May have failing tests temporarily
- Receives frequent merges
- Integrates multiple work streams
- Testing ground before main

**Exception**: If team requires PR reviews for development:
- Only require PR reviews (1 approver)
- Do NOT require status checks
- Do NOT restrict branches
- Keep it lightweight

---

### Epic Branches

**Purpose**: Long-lived branches for multi-feature epics

**Protection**: NOT protected

**Merge Sources**: Feature branches within epic

**Merge Target**: `development`

**Naming**: `epic-{number}-{short-description}`
- Example: `epic-1-progressive-coherence`

**When to Use**:
- Epic has 2+ features
- Epic will take >1 week to complete
- Want to integrate features before merging to development
- Multiple agents working on epic simultaneously

---

### Feature Branches

**Purpose**: Medium-lived branches for implementing features

**Protection**: NOT protected

**Merge Sources**: None (agents commit waves directly)

**Merge Target**: Epic branch or `development` (if standalone)

**Naming**: `feature-{epic}.{feature}-{short-description}`
- Example: `feature-1.10-infrastructure`

**When to Use**:
- Feature has 2+ waves
- Feature is part of epic OR standalone with multiple waves

**Work Pattern**:
- Commit waves directly to feature branch (NO wave branches)
- Wave 1: commit 1
- Wave 2: commit 2
- Wave 3: commit 3
- Merge entire feature when all waves complete

---

### Standalone Wave Branches

**Purpose**: Short-lived branches for single-wave implementations

**Protection**: NOT protected

**Merge Sources**: None (leaf branches)

**Merge Target**: `development`

**Naming**: `wave-{epic}.{feature}.{wave}-{short-description}`
- Example: `wave-3.1.1-standalone-skill`

**When to Use**:
- Single wave implementation (not part of epic)
- Quick enhancement or fix
- Standalone work that doesn't fit into feature

---

### Hotfix Branches

**Purpose**: Emergency fixes for production issues

**Protection**: NOT protected

**Merge Sources**: None

**Merge Target**: `development` and sometimes `main` (dual PR)

**Naming**: `hotfix-{short-description}`
- Example: `hotfix-auth-token-validation`

**When to Use**:
- Critical production bug
- Security vulnerability
- Data integrity issue

---

## Workflow Validation

### Required Workflows

**1. PR Branch Validation** (`.github/workflows/pr-branch-check.yml`)

**Purpose**: Enforce only `development → main` PRs allowed

**Triggers**: Pull requests to `main`

**Checks**:
- Source branch must be `development`
- Fails if PR from any other branch

**Example**:
```yaml
name: PR Branch Check

on:
  pull_request:
    branches:
      - main

jobs:
  check-source-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Validate PR Source Branch
        run: |
          if [ "${{ github.head_ref }}" != "development" ]; then
            echo "❌ PRs to main must come from development"
            exit 1
          fi
          echo "✅ PR from development to main allowed"
```

---

### Optional Workflows

**2. CI/CD** (`.github/workflows/ci.yml`)

**Purpose**: Run tests, linting, builds

**Triggers**: Push to any branch, PRs

**Checks**:
- Linting passes
- Tests pass
- Build succeeds

---

**3. Development Branch Tests** (`.github/workflows/dev-tests.yml`)

**Purpose**: Verify development branch stability

**Triggers**: Push to `development`

**Checks**:
- Integration tests pass
- E2E tests pass
- Deployment to staging succeeds

---

## Branch Relationships

### Verification Checks

**1. Development branch divergence from main**

```bash
# Check how far ahead development is
git rev-list --count main..development
```

**Expected**: 0-50 commits ahead

**Warning**: >50 commits suggests development should merge to main soon

---

**2. Branch synchronization**

```bash
# Check if development has changes not in main
git log main..development --oneline
```

**Expected**: Shows recent work not yet merged to main

---

**3. Branch activity**

```bash
# Check last commit date on development
git log -1 --format="%ar" development
```

**Expected**: Recent activity (within last week)

**Warning**: >2 weeks suggests stale branch

---

## Setup Checklist

### Initial Repository Setup

- [ ] Main branch exists
- [ ] Development branch created from main
- [ ] Development branch pushed to remote
- [ ] PR branch validation workflow created
- [ ] PR branch validation workflow committed to development
- [ ] Main branch protection configured
- [ ] Status check includes "check-source-branch"
- [ ] Development branch NOT protected
- [ ] CODEOWNERS file created (optional)
- [ ] README updated with workflow documentation

---

### Validation Checklist

- [ ] Can create branches from development
- [ ] Cannot push directly to main
- [ ] Cannot create PR to main from feature branch
- [ ] CAN create PR to main from development
- [ ] PR branch check workflow appears in PR status checks
- [ ] Development branch allows direct merges

---

## Common Setup Issues

### Issue 1: Development Branch Protected

**Problem**: Development branch has protection rules

**Impact**: Cannot merge feature branches without PRs

**Solution**: Remove protection from development branch
```bash
gh api repos/{owner}/{repo}/branches/development/protection -X DELETE
```

---

### Issue 2: Main Branch Allows Direct Pushes

**Problem**: Main branch not properly protected

**Impact**: Can accidentally commit directly to main

**Solution**: Configure main branch protection
```bash
gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input protection.json
```

---

### Issue 3: PR Branch Check Missing

**Problem**: No workflow to enforce development → main PRs

**Impact**: Can create PRs from any branch to main

**Solution**: Create `.github/workflows/pr-branch-check.yml` and commit to development

---

### Issue 4: Status Check Not Required

**Problem**: PR branch check exists but not required on main

**Impact**: PR can be merged even if check fails

**Solution**: Update main branch protection to require "check-source-branch" status check

---

### Issue 5: Development Branch Missing

**Problem**: Repository only has main branch

**Impact**: No integration branch for work

**Solution**: Create development branch from main
```bash
git checkout -b development
git push -u origin development
```

---

## Integration with Agentic Workflow

### Before Starting Work

1. Validate repository setup
2. Ensure development branch exists
3. Confirm main branch protected
4. Verify PR branch validation workflow present

### Creating Work Branches

1. Always branch from `development`
2. Use appropriate branch type (epic/feature/wave)
3. Follow naming conventions
4. Push branch to remote

### Merging Work

1. Merge feature → epic (if part of epic)
2. Merge epic → development
3. Merge standalone features/waves → development
4. Merge development → main (via PR)

### After Merge to Main

1. Tag release (optional)
2. Deploy to production (if applicable)
3. Sync development with main
4. Clean up old branches

---

## Example: Complete Setup Flow

```bash
# 1. Create development branch (if not exists)
git checkout -b development
git push -u origin development

# 2. Create PR branch validation workflow
mkdir -p .github/workflows
cat > .github/workflows/pr-branch-check.yml <<'EOF'
name: PR Branch Check
on:
  pull_request:
    branches:
      - main
jobs:
  check-source-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Validate PR Source Branch
        run: |
          if [ "${{ github.head_ref }}" != "development" ]; then
            echo "❌ PRs to main must come from development"
            exit 1
          fi
          echo "✅ PR from development to main allowed"
EOF

# 3. Commit workflow
git add .github/workflows/pr-branch-check.yml
git commit -m "Add PR branch validation workflow"
git push

# 4. Configure main branch protection
gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["check-source-branch"]
  },
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "enforce_admins": false,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

# 5. Verify setup
python scripts/validate_repository.py --repo "{owner}/{repo}" --check-all
```

---

**Last Updated**: 2025-01-30
