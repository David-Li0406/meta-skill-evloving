---
name: git-repository-setup-validation
description: Validate repository has development branch workflow with main branch protection configured per agent-guide-development-branch-setup.md. Returns validation status and recommendations. Use before starting work, during repository setup review, or when troubleshooting git workflow issues. Always uses Git MCP server for safe validation.
---

# Git Repository Setup Validation

Validate repository configuration for agentic development workflow with proper branch protection and development branch setup.

## Quick Start

**Validate current repository:**
```
"Validate this repository has proper development workflow setup"
```

**Validate specific repository:**
```
"Validate repository myorg/myrepo has main branch protection and development branch configured"
```

## Core Workflow

### Step 1: Validate Repository Structure

Check repository has required branches:

```
mcp__git__list_branches()
```

**Required branches**:
- `main` (protected)
- `development` (integration branch)

**Validation checks**:
- ✅ Both branches exist
- ✅ `development` branch has recent activity (not stale)
- ❌ FAIL: Missing `main` or `development` branch

---

### Step 2: Check Main Branch Protection

Query main branch protection settings:

```
mcp__git__get_branch_protection(
  branch: "main"
)
```

**Required protections**:
- ✅ Require pull request reviews before merging
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners (if CODEOWNERS file exists)
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Restrict who can push to matching branches (admin only)
- ✅ Require linear history (no merge commits)

**Optional protections**:
- Include administrators in restrictions
- Allow force pushes (disabled)
- Allow deletions (disabled)

---

### Step 3: Validate Development Branch Setup

Check development branch is configured as integration branch:

```
mcp__git__get_branch_info(
  branch: "development"
)
```

**Validation checks**:
- ✅ `development` branch exists
- ✅ `development` is not protected (allows direct merges from feature branches)
- ✅ `development` has commits (not empty)
- ✅ `development` is ahead of `main` or synchronized

**Branch relationships**:
- `development` should be primary integration branch
- All feature/epic/wave branches created from `development`
- `development` merges to `main` via PR

---

### Step 4: Check Git Workflow Configuration

Validate repository has proper workflow files:

```
mcp__git__list_files(
  path: ".github/workflows"
)
```

**Expected files**:
- `pr-validation.yml` — PR validation workflow
- `branch-protection.yml` — Enforce branch protection
- Optional: `ci.yml`, `deploy.yml`

**Validation**:
- ✅ At least one PR validation workflow exists
- ✅ Workflows reference proper branches (`main`, `development`)

---

### Step 5: Verify CODEOWNERS (Optional)

Check if CODEOWNERS file exists:

```
mcp__git__list_files(
  path: ".github"
)
```

**If CODEOWNERS exists**:
- ✅ File is properly formatted
- ✅ Contains at least one code owner
- ✅ Main branch protection requires Code Owners review

---

### Step 6: Generate Validation Report

Compile validation results:

```markdown
## Repository Setup Validation Report

**Repository**: myorg/myrepo
**Date**: 2025-01-30
**Status**: ✅ PASS / ⚠️ WARNING / ❌ FAIL

### Branch Structure
- ✅ `main` branch exists
- ✅ `development` branch exists
- ✅ `development` has recent activity

### Main Branch Protection
- ✅ Require pull request reviews
- ✅ Dismiss stale reviews
- ✅ Require status checks
- ⚠️ Code Owners review not required (CODEOWNERS missing)
- ✅ Restrict direct pushes
- ✅ Require linear history

### Development Branch
- ✅ Not protected (allows feature merges)
- ✅ Has commits
- ✅ Synchronized with main

### Workflow Configuration
- ✅ PR validation workflow exists
- ✅ Workflows reference correct branches

### Recommendations
- Consider adding CODEOWNERS file for code review automation
- Update PR validation workflow to include lint checks
```

---

## Key Concepts

**Development Branch Workflow**:
- `main` is protected production branch
- `development` is integration branch (unprotected)
- Feature/epic/wave branches created from `development`
- PRs merge to `development`, then `development` merges to `main`

**Branch Protection Rationale**:
- Prevents accidental direct commits to `main`
- Enforces code review process
- Ensures CI/CD checks pass before merge
- Maintains linear history for clean git log

**Validation Levels**:
- **CRITICAL** (❌): Missing required branches or protection
- **WARNING** (⚠️): Optional features missing (CODEOWNERS, workflows)
- **PASS** (✅): All required checks pass

**Git MCP Server Benefits**:
- Safe read-only validation operations
- Structured error handling
- Consistent validation logic
- Audit trail of validation checks

---

## Available Resources

### Scripts

- **scripts/validate_repository.py** — Complete repository validation
  ```bash
  python scripts/validate_repository.py \
    --repo "myorg/myrepo" \
    --check-branches \
    --check-protection \
    --check-workflows
  # Returns: Validation report with status and recommendations
  ```

- **scripts/check_branch_protection.py** — Check main branch protection settings
  ```bash
  python scripts/check_branch_protection.py \
    --repo "myorg/myrepo" \
    --branch "main"
  # Returns: Protection settings with pass/fail status
  ```

- **scripts/validate_workflow_files.py** — Validate GitHub Actions workflows
  ```bash
  python scripts/validate_workflow_files.py \
    --repo "myorg/myrepo" \
    --required-workflows "pr-validation"
  # Returns: Workflow validation results
  ```

### References

- **references/branch-protection-requirements.md** — Required protection settings for main branch
- **references/development-workflow-setup.md** — Development branch workflow guidelines
- **references/validation-checklist.md** — Complete validation checklist with criteria

---

## Validation Scenarios

### Scenario 1: New Repository Setup

**Situation**: Just created repository, need to validate setup before starting work

**Steps**:
1. Validate branch structure exists
2. Check main branch protection configured
3. Verify development branch setup
4. Check for workflow files
5. Generate recommendations for missing items

**Example**:
```bash
python scripts/validate_repository.py \
  --repo "myorg/new-repo" \
  --check-branches \
  --check-protection \
  --check-workflows \
  --generate-report
```

**Expected result**: Report showing what's configured and what needs setup

---

### Scenario 2: Pre-Work Validation

**Situation**: About to start implementing feature, want to ensure repository properly configured

**Steps**:
1. Quick validation of critical requirements
2. Check branches exist and are synchronized
3. Verify main branch protection active
4. Confirm can create branches from development

**Example**:
```bash
# Quick validation
python scripts/validate_repository.py \
  --repo "myorg/active-repo" \
  --quick
```

**Expected result**: Quick pass/fail status (PASS if all critical checks pass)

---

### Scenario 3: Troubleshooting Git Issues

**Situation**: Experiencing git workflow issues, need to validate configuration

**Steps**:
1. Full validation of repository setup
2. Check branch relationships (development vs. main)
3. Verify protection settings match requirements
4. Identify configuration drift

**Example**:
```bash
python scripts/validate_repository.py \
  --repo "myorg/problem-repo" \
  --check-branches \
  --check-protection \
  --check-workflows \
  --check-relationships \
  --verbose
```

**Expected result**: Detailed report identifying configuration issues

---

### Scenario 4: Periodic Audit

**Situation**: Regular audit to ensure repository configuration hasn't drifted

**Steps**:
1. Validate all protection settings
2. Check for new workflow files
3. Verify branch activity
4. Generate compliance report

**Example**:
```bash
python scripts/validate_repository.py \
  --repo "myorg/production-repo" \
  --check-all \
  --generate-compliance-report
```

**Expected result**: Compliance report for documentation

---

## Output Format

**Validation Report Structure**:
```json
{
  "repository": "myorg/myrepo",
  "validation_date": "2025-01-30T10:30:00Z",
  "overall_status": "PASS",
  "checks": {
    "branch_structure": {
      "status": "PASS",
      "main_exists": true,
      "development_exists": true,
      "development_active": true
    },
    "main_protection": {
      "status": "PASS",
      "require_pr_reviews": true,
      "dismiss_stale_reviews": true,
      "require_code_owners": false,
      "require_status_checks": true,
      "restrict_pushes": true,
      "require_linear_history": true
    },
    "development_branch": {
      "status": "PASS",
      "not_protected": true,
      "has_commits": true,
      "synchronized_with_main": true
    },
    "workflows": {
      "status": "WARNING",
      "pr_validation_exists": true,
      "workflows_found": [".github/workflows/pr-validation.yml"]
    }
  },
  "recommendations": [
    "Consider adding CODEOWNERS file for automated code review assignments",
    "Add additional CI workflows for linting and testing"
  ]
}
```

---

## Integration with Workflow

**Before starting work**:
```markdown
## Step 0: Validate Repository Setup

Before creating branches or implementing:
- Invoke `git-repository-setup-validation` skill
- Verify PASS status
- If FAIL, run `git-development-workflow-setup` skill
- If WARNING, note recommendations but proceed
```

**During repository setup**:
```markdown
## Repository Setup Workflow

1. Create repository
2. Run `git-repository-setup-validation` skill
3. If validation fails, run `git-development-workflow-setup` skill
4. Re-run validation to confirm setup
5. Begin work
```

---

## Success Criteria

- ✅ Repository has `main` and `development` branches
- ✅ Main branch protection configured with required settings
- ✅ Development branch exists and is not protected
- ✅ Branch relationships correct (development from main)
- ✅ At least one PR validation workflow exists
- ✅ Validation report generated with clear status
- ✅ Recommendations provided for warnings

---

## Tips for Effective Validation

1. **Run before starting work** - Catch configuration issues early
2. **Automate periodic validation** - Schedule regular audits
3. **Document configuration drift** - Track when settings change
4. **Use with setup skill** - Pair validation with automated setup
5. **Share reports** - Use validation reports for team communication
6. **Validate after changes** - Re-run after modifying branch protection
7. **Use quick mode for regular checks** - Save time with quick validation

---

## Common Issues and Solutions

### Issue 1: Main Branch Not Protected
**Problem**: Main branch has no protection rules
**Solution**: Run `git-development-workflow-setup` skill to configure protection

### Issue 2: Development Branch Missing
**Problem**: Repository only has `main` branch
**Solution**: Create `development` branch from `main`, configure as integration branch

### Issue 3: Development Branch Protected
**Problem**: Development branch has same protections as main
**Solution**: Remove protection from development branch to allow direct merges from features

### Issue 4: No Workflow Files
**Problem**: Missing `.github/workflows/` directory or validation workflows
**Solution**: Add PR validation workflow from templates

### Issue 5: CODEOWNERS Not Enforced
**Problem**: CODEOWNERS file exists but Code Owners review not required
**Solution**: Update main branch protection to require Code Owners review

---

## Validation Checklist

Before starting work:
- [ ] Repository exists and is accessible
- [ ] `main` branch exists
- [ ] `development` branch exists
- [ ] Main branch protection configured
- [ ] Development branch not protected
- [ ] At least one workflow file exists

Critical validations:
- [ ] Main branch requires PR reviews
- [ ] Main branch restricts direct pushes
- [ ] Development branch allows direct merges
- [ ] Branches are synchronized

Optional validations:
- [ ] CODEOWNERS file exists
- [ ] Code Owners review required
- [ ] Multiple workflow files present
- [ ] Branch activity recent

---

## Example: Complete Validation

```bash
# Step 1: Validate repository structure
python scripts/validate_repository.py \
  --repo "myorg/myrepo" \
  --check-branches

# Output:
# ✅ main branch exists
# ✅ development branch exists
# ✅ development branch active (last commit 2 hours ago)

# Step 2: Validate main branch protection
python scripts/check_branch_protection.py \
  --repo "myorg/myrepo" \
  --branch "main"

# Output:
# ✅ Require PR reviews: enabled
# ✅ Dismiss stale reviews: enabled
# ⚠️ Require Code Owners: disabled (CODEOWNERS missing)
# ✅ Require status checks: enabled
# ✅ Restrict pushes: enabled (admins only)
# ✅ Require linear history: enabled

# Step 3: Validate workflow files
python scripts/validate_workflow_files.py \
  --repo "myorg/myrepo"

# Output:
# ✅ Found workflow: .github/workflows/pr-validation.yml
# ✅ Workflow references correct branches

# Step 4: Generate complete report
python scripts/validate_repository.py \
  --repo "myorg/myrepo" \
  --check-all \
  --generate-report

# Output: Full validation report with recommendations
```

---

**Last Updated**: 2025-01-30
