# Validation Checklist

Complete checklist for repository setup validation.

---

## Quick Validation (Before Starting Work)

**Time**: 1-2 minutes

### Critical Checks Only

- [ ] Repository exists and is accessible
- [ ] `main` branch exists
- [ ] `development` branch exists
- [ ] Main branch has protection rules
- [ ] Can create branches from development

**Status Criteria**:
- **PASS**: All 5 checks pass
- **FAIL**: Any check fails

---

## Standard Validation (Regular Checks)

**Time**: 3-5 minutes

### Branch Structure

- [ ] `main` branch exists
- [ ] `development` branch exists
- [ ] Development branch has commits (not empty)
- [ ] Development branch active (commits within last 2 weeks)
- [ ] Development is ahead of or synchronized with main

### Main Branch Protection

- [ ] Require pull request reviews enabled
- [ ] Require status checks enabled
- [ ] Status checks include "check-source-branch"
- [ ] Direct pushes restricted (admins only or no one)
- [ ] Require linear history enabled

### Development Branch

- [ ] Development branch NOT protected
- [ ] Can merge directly to development (no PR required)
- [ ] Development branch accessible to agents

### Workflows

- [ ] `.github/workflows/pr-branch-check.yml` exists
- [ ] PR branch check workflow committed to default branch
- [ ] Workflow validates source branch on PRs to main

**Status Criteria**:
- **PASS**: All checks pass
- **WARNING**: Optional checks fail (linear history, dismiss stale)
- **FAIL**: Any critical check fails

---

## Comprehensive Validation (Audit/Setup)

**Time**: 5-10 minutes

### 1. Branch Structure

#### Main Branch
- [ ] Main branch exists
- [ ] Main branch is default branch
- [ ] Main branch has commits
- [ ] Main branch protected

#### Development Branch
- [ ] Development branch exists
- [ ] Development branch created from main
- [ ] Development branch has commits
- [ ] Development branch active (last commit <2 weeks ago)
- [ ] Development 0-50 commits ahead of main (reasonable)

#### Branch Relationships
- [ ] Development diverged from main at reasonable point
- [ ] No orphaned branches (all branches connect to main/development)
- [ ] Active work branches exist (if work in progress)

---

### 2. Main Branch Protection (Detailed)

#### Pull Request Requirements
- [ ] Require pull request reviews: **enabled**
- [ ] Required approving review count: **0 or more**
- [ ] Dismiss stale pull request approvals: **enabled** (recommended)
- [ ] Require review from Code Owners: **enabled if CODEOWNERS exists**

#### Status Check Requirements
- [ ] Require status checks to pass: **enabled**
- [ ] Require branches to be up to date: **enabled** (recommended)
- [ ] Status checks contexts include: **"check-source-branch"**
- [ ] Status checks contexts include: CI checks (if applicable)

#### Branch Restrictions
- [ ] Restrict who can push to matching branches: **enabled or N/A**
- [ ] Users/teams with push access: **empty or admins only**
- [ ] Include administrators: **optional**

#### Additional Protections
- [ ] Require linear history: **enabled** (recommended)
- [ ] Allow force pushes: **disabled**
- [ ] Allow deletions: **disabled**

---

### 3. Development Branch Setup

#### Branch Configuration
- [ ] Development branch exists
- [ ] Development branch NOT protected (allows direct merges)
- [ ] Development branch accessible to all developers/agents
- [ ] Development branch is working branch (not just backup)

#### Optional Protection (If Team Requires)
- [ ] Require pull request reviews: **optional (lightweight)**
- [ ] Required approving review count: **1 maximum**
- [ ] NO status checks required
- [ ] NO branch restrictions

---

### 4. Workflow Files

#### PR Branch Validation Workflow
- [ ] `.github/workflows/pr-branch-check.yml` exists
- [ ] Workflow triggers on PRs to main
- [ ] Workflow validates source branch is development
- [ ] Workflow exits with error if source not development
- [ ] Workflow committed to repository

#### CI/CD Workflows (Optional)
- [ ] `.github/workflows/ci.yml` exists (if applicable)
- [ ] CI workflow runs on push to branches
- [ ] CI workflow runs on PRs
- [ ] Tests defined and execute

#### Development Testing Workflows (Optional)
- [ ] `.github/workflows/dev-tests.yml` exists (if applicable)
- [ ] Development tests run on push to development
- [ ] Integration tests execute

---

### 5. CODEOWNERS Configuration (Optional)

#### File Exists
- [ ] `.github/CODEOWNERS` file exists
- [ ] File is properly formatted
- [ ] Contains at least one code owner
- [ ] Code owners valid (users/teams exist)

#### Integration with Protection
- [ ] Main branch protection requires Code Owners review
- [ ] Code owners notified on PRs affecting their files

---

### 6. Repository Configuration

#### Access and Permissions
- [ ] Repository accessible to development team
- [ ] Agents have appropriate access (read/write to development)
- [ ] Admin access restricted
- [ ] Branch permissions configured

#### Repository Settings
- [ ] Default branch is `main`
- [ ] Merge button settings appropriate (squash, rebase, or merge)
- [ ] Automatically delete head branches: **enabled** (recommended)
- [ ] Allow auto-merge: **optional**

---

## Validation Results Format

### Status Levels

**PASS (✅)**
- All critical checks pass
- All recommended checks pass
- Ready for development work

**WARNING (⚠️)**
- All critical checks pass
- Some recommended checks fail
- Can proceed with work, but improvements recommended

**FAIL (❌)**
- One or more critical checks fail
- Must fix before proceeding
- Repository not properly configured

---

### Sample Report

```markdown
## Repository Validation Report

**Repository**: myorg/myrepo
**Date**: 2025-01-30T10:30:00Z
**Status**: ⚠️ WARNING

### Branch Structure ✅ PASS
- ✅ Main branch exists
- ✅ Development branch exists
- ✅ Development active (last commit 2 hours ago)
- ✅ Development 15 commits ahead of main

### Main Branch Protection ✅ PASS
- ✅ Require PR reviews enabled
- ✅ Require status checks enabled (check-source-branch)
- ✅ Direct pushes restricted
- ⚠️ Linear history not required (recommended)
- ⚠️ Stale reviews not dismissed (recommended)

### Development Branch ✅ PASS
- ✅ Not protected (allows direct merges)
- ✅ Has commits
- ✅ Synchronized with main

### Workflows ⚠️ WARNING
- ✅ PR branch validation workflow exists
- ⚠️ CI workflow missing (optional but recommended)

### CODEOWNERS ⚠️ WARNING
- ⚠️ CODEOWNERS file missing (optional)
- ⚠️ Code Owners review not required

### Overall Assessment
Repository is properly configured for development work. Some recommended features missing (linear history, CI workflows, CODEOWNERS). Can proceed with work, consider adding recommended features for better workflow.

### Recommendations
1. Enable "Require linear history" on main branch protection
2. Enable "Dismiss stale reviews" on main branch protection
3. Add CI workflow for automated testing
4. Consider adding CODEOWNERS file for code review automation
```

---

## Checklist by Role

### Developer Starting Work

**Before implementing feature**:
- [ ] Quick validation passes
- [ ] Can create branch from development
- [ ] Development branch up-to-date

**If validation fails**:
- [ ] Run comprehensive validation
- [ ] Identify missing configuration
- [ ] Contact repository admin or run setup skill

---

### Repository Administrator

**Initial repository setup**:
- [ ] Run comprehensive validation
- [ ] Fix all critical failures
- [ ] Address warnings where possible
- [ ] Document any exceptions

**Periodic audit** (monthly):
- [ ] Run comprehensive validation
- [ ] Review protection settings for drift
- [ ] Update workflows if needed
- [ ] Verify CODEOWNERS current

---

### Agent (Lighthouse LM)

**Before starting work**:
- [ ] Invoke `git-repository-setup-validation` skill
- [ ] Check validation status
- [ ] If FAIL, invoke `git-development-workflow-setup` skill
- [ ] Re-run validation to confirm

**During work**:
- [ ] Follow branching strategy per validation
- [ ] Respect branch protection rules
- [ ] Use proper merge targets

---

## Validation Commands

### Quick Validation
```bash
python scripts/validate_repository.py \
  --repo "{owner}/{repo}" \
  --quick
```

### Standard Validation
```bash
python scripts/validate_repository.py \
  --repo "{owner}/{repo}" \
  --check-branches \
  --check-protection \
  --check-workflows
```

### Comprehensive Validation
```bash
python scripts/validate_repository.py \
  --repo "{owner}/{repo}" \
  --check-all \
  --generate-report
```

### Specific Component Checks
```bash
# Check branch protection only
python scripts/check_branch_protection.py \
  --repo "{owner}/{repo}" \
  --branch "main"

# Check workflow files only
python scripts/validate_workflow_files.py \
  --repo "{owner}/{repo}"
```

---

## Automated Validation

### Pre-Work Hook

Run validation before starting work:

```bash
#!/bin/bash
# .git/hooks/pre-work-validation.sh

echo "🔍 Validating repository setup..."

python scripts/validate_repository.py \
  --repo "$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\).git/\1/')" \
  --quick

if [ $? -ne 0 ]; then
  echo "❌ Repository validation failed"
  echo "Run 'python scripts/validate_repository.py --check-all' for details"
  exit 1
fi

echo "✅ Repository validation passed"
```

---

### CI Validation

Run validation in CI pipeline:

```yaml
name: Repository Validation

on:
  schedule:
    - cron: '0 0 * * 1' # Weekly on Monday
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Repository Setup
        run: |
          python scripts/validate_repository.py \
            --repo "${{ github.repository }}" \
            --check-all \
            --fail-on-warning
```

---

**Last Updated**: 2025-01-30
