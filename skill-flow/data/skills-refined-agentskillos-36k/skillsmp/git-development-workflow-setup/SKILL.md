---
name: git-development-workflow-setup
description: Configure repository with development branch workflow, main branch protection, and PR validation per agent-guide-development-branch-setup.md. Executes setup steps atomically. Use for new repository setup, fixing validation failures, or recovering from configuration drift. Always uses Git MCP server for safe execution.
---

# Git Development Workflow Setup

Automated setup of development branch workflow with proper branch protection and PR validation for agentic development.

## Quick Start

**Setup new repository:**
```
"Setup development workflow for this repository with main branch protection"
```

**Fix validation failures:**
```
"Fix repository configuration - validation failed on main branch protection and missing development branch"
```

## Core Workflow

### Step 1: Check Current Configuration

Before making changes, validate current state:

```
mcp__git__list_branches()
mcp__git__get_branch_protection(branch: "main")
```

**Capture**:
- Which branches exist
- Current protection settings on main
- Whether development branch exists
- Current repository state

**Document baseline** for rollback if needed.

---

### Step 2: Create Development Branch (If Missing)

Check if development branch exists:

```bash
# Via Git MCP server
mcp__git__list_branches()
```

**If development exists**:
- ✅ Skip creation
- Verify branch has commits
- Ensure branch pushed to remote

**If development missing**:
```
mcp__git__create_branch(
  branch_name: "development",
  from_branch: "main"
)
mcp__git__push_branch(
  branch: "development",
  set_upstream: true
)
```

**Verification**:
```
mcp__git__get_branch_info(branch: "development")
```

**Success criteria**:
- Development branch created from main
- Development branch pushed to remote
- Development branch accessible

---

### Step 3: Create PR Branch Validation Workflow

Create workflow file to enforce `development → main` PR policy:

**File**: `.github/workflows/pr-branch-check.yml`

**Content**:
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
          SOURCE_BRANCH="${{ github.head_ref }}"
          TARGET_BRANCH="${{ github.base_ref }}"

          echo "🔍 Checking PR branch policy..."
          echo "   Source: $SOURCE_BRANCH"
          echo "   Target: $TARGET_BRANCH"

          if [ "$TARGET_BRANCH" = "main" ] && [ "$SOURCE_BRANCH" != "development" ]; then
            echo ""
            echo "❌ ERROR: PRs to 'main' must come from 'development' branch"
            echo ""
            echo "Current PR: $SOURCE_BRANCH → main"
            echo "Required:   development → main"
            echo ""
            echo "Please create your PR from the 'development' branch instead."
            exit 1
          fi

          echo "✅ Branch policy check passed!"
          echo "   PR from '$SOURCE_BRANCH' to '$TARGET_BRANCH' is allowed"
```

**Create via MCP**:
```
mcp__git__write_file(
  path: ".github/workflows/pr-branch-check.yml",
  content: [workflow content above]
)
```

**Commit and push**:
```
mcp__git__commit(
  message: "Add PR branch validation workflow\n\n- Enforces PRs to main must come from development\n- Automatic check runs on all PRs to main\n- Prevents agents/users from creating PRs from wrong branches",
  files: [".github/workflows/pr-branch-check.yml"]
)
mcp__git__push(branch: "development")
```

**Verification**:
- Workflow file exists in repository
- Workflow committed to development branch
- Workflow accessible on GitHub

---

### Step 4: Configure Main Branch Protection

Apply branch protection rules to main:

**Protection settings**:
```json
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
```

**Apply via GitHub API**:
```bash
gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input protection.json
```

**Via MCP** (if available):
```
mcp__git__set_branch_protection(
  branch: "main",
  protection_rules: {
    require_pr_reviews: true,
    dismiss_stale_reviews: true,
    require_status_checks: ["check-source-branch"],
    strict_status_checks: true,
    require_linear_history: true,
    allow_force_pushes: false,
    allow_deletions: false
  }
)
```

**Verification**:
```
mcp__git__get_branch_protection(branch: "main")
```

**Success criteria**:
- PR reviews required
- Status checks include "check-source-branch"
- Linear history required
- Force pushes blocked
- Direct pushes restricted

---

### Step 5: Verify Development Branch Not Protected

Ensure development branch allows direct merges:

```
mcp__git__get_branch_protection(branch: "development")
```

**Expected**: No protection or 404 (branch not protected)

**If development is protected**:
```
mcp__git__remove_branch_protection(branch: "development")
```

**Verification**:
- Development branch has NO protection rules
- Can merge directly to development
- No PR required for merges to development

---

### Step 6: Generate Setup Report

Document what was configured:

```markdown
## Repository Setup Report

**Repository**: myorg/myrepo
**Date**: 2025-01-30T10:30:00Z
**Status**: ✅ COMPLETE

### Actions Performed

1. **Development Branch**
   - ✅ Created from main
   - ✅ Pushed to remote
   - ✅ Verified accessible

2. **PR Branch Validation Workflow**
   - ✅ Created .github/workflows/pr-branch-check.yml
   - ✅ Committed to development
   - ✅ Enforces development → main PR policy

3. **Main Branch Protection**
   - ✅ Require PR reviews: enabled
   - ✅ Require status checks: enabled (check-source-branch)
   - ✅ Dismiss stale reviews: enabled
   - ✅ Require linear history: enabled
   - ✅ Block force pushes: enabled
   - ✅ Block deletions: enabled

4. **Development Branch Protection**
   - ✅ No protection rules (allows direct merges)

### Verification

Run validation to confirm setup:
- Invoke `git-repository-setup-validation` skill
- Expected result: PASS

### Next Steps

1. Start creating feature branches from development
2. Follow agentic branching strategy
3. Create PRs from development to main when ready
```

---

## Key Concepts

**Atomic Setup**:
- Each step independent and verifiable
- Can resume from any point if interrupted
- Rollback available if needed

**Idempotent Operations**:
- Safe to run multiple times
- Checks before creating/modifying
- Skips steps if already configured

**Git MCP Server Benefits**:
- Safe execution with validation
- Structured error handling
- Consistent configuration
- Audit trail of setup steps

**Development Branch Philosophy**:
- Unprotected to allow rapid iteration
- Integration branch for all work
- Merges to main via PR for quality gate

**Main Branch Philosophy**:
- Protected to prevent accidents
- Only accepts PRs from development
- Linear history for clean git log
- Always deployable

---

## Available Resources

### Scripts

- **scripts/setup_repository.py** — Complete automated setup
  ```bash
  python scripts/setup_repository.py \
    --repo "myorg/myrepo" \
    --create-development \
    --add-pr-workflow \
    --protect-main \
    --verify
  # Returns: Setup report with verification status
  ```

- **scripts/create_pr_workflow.py** — Create PR branch validation workflow
  ```bash
  python scripts/create_pr_workflow.py \
    --output ".github/workflows/pr-branch-check.yml"
  # Returns: Workflow file created
  ```

- **scripts/configure_branch_protection.py** — Configure main branch protection
  ```bash
  python scripts/configure_branch_protection.py \
    --repo "myorg/myrepo" \
    --branch "main" \
    --config "protection-config.json"
  # Returns: Protection configured successfully
  ```

- **scripts/remove_branch_protection.py** — Remove branch protection
  ```bash
  python scripts/remove_branch_protection.py \
    --repo "myorg/myrepo" \
    --branch "development"
  # Returns: Protection removed
  ```

### References

- **references/setup-steps.md** — Detailed setup steps with explanations
- **references/protection-config-templates.md** — Branch protection configuration templates
- **references/rollback-procedures.md** — How to rollback setup if needed

---

## Setup Scenarios

### Scenario 1: New Repository

**Situation**: Just created repository, needs complete setup

**Steps**:
1. Check current state (baseline)
2. Create development branch from main
3. Create PR validation workflow
4. Configure main branch protection
5. Verify setup with validation skill

**Example**:
```bash
python scripts/setup_repository.py \
  --repo "myorg/new-repo" \
  --create-development \
  --add-pr-workflow \
  --protect-main \
  --verify
```

**Expected result**: Complete setup from scratch

---

### Scenario 2: Fix Validation Failures

**Situation**: Validation skill returned FAIL status

**Steps**:
1. Review validation report
2. Identify missing components
3. Run setup for missing components only
4. Re-run validation

**Example**:
```bash
# Validation shows: missing development branch and main protection

python scripts/setup_repository.py \
  --repo "myorg/existing-repo" \
  --create-development \
  --protect-main \
  --skip-workflow  # Workflow already exists
  --verify
```

**Expected result**: Fix only what's missing, verify pass

---

### Scenario 3: Configuration Drift Recovery

**Situation**: Repository was configured but settings changed

**Steps**:
1. Document current state
2. Identify drift from standard
3. Re-apply configuration
4. Verify restoration

**Example**:
```bash
# Main branch protection was disabled

python scripts/configure_branch_protection.py \
  --repo "myorg/drifted-repo" \
  --branch "main" \
  --config "standard-protection.json" \
  --force
```

**Expected result**: Restore standard configuration

---

### Scenario 4: Development Branch Already Protected

**Situation**: Development branch has protection rules (incorrect)

**Steps**:
1. Check current protection on development
2. Remove protection rules
3. Verify development unprotected

**Example**:
```bash
python scripts/remove_branch_protection.py \
  --repo "myorg/overprotected-repo" \
  --branch "development" \
  --confirm
```

**Expected result**: Development branch unprotected

---

## Output Format

**Setup Report Structure**:
```json
{
  "repository": "myorg/myrepo",
  "setup_date": "2025-01-30T10:30:00Z",
  "status": "COMPLETE",
  "actions": [
    {
      "step": "create_development_branch",
      "status": "SUCCESS",
      "message": "Development branch created from main"
    },
    {
      "step": "create_pr_workflow",
      "status": "SUCCESS",
      "message": "PR branch validation workflow created and committed"
    },
    {
      "step": "configure_main_protection",
      "status": "SUCCESS",
      "message": "Main branch protection configured"
    },
    {
      "step": "verify_development_unprotected",
      "status": "SUCCESS",
      "message": "Development branch has no protection"
    }
  ],
  "verification": {
    "validation_run": true,
    "validation_status": "PASS"
  },
  "rollback_available": true
}
```

---

## Integration with Workflow

**After validation failure**:
```markdown
## Repository Setup Recovery

1. Run validation skill → FAIL
2. Review validation report
3. Invoke `git-development-workflow-setup` skill
4. Re-run validation skill → PASS
5. Begin work
```

**For new repositories**:
```markdown
## Initial Repository Setup

1. Create repository on GitHub
2. Clone repository locally
3. Invoke `git-development-workflow-setup` skill
4. Wait for setup completion
5. Run validation skill to confirm
6. Create first feature branch
```

---

## Success Criteria

- ✅ Development branch created (if missing)
- ✅ Development branch pushed to remote
- ✅ PR validation workflow created
- ✅ PR validation workflow committed
- ✅ Main branch protection configured
- ✅ Status checks include "check-source-branch"
- ✅ Development branch NOT protected
- ✅ Validation skill returns PASS

---

## Tips for Effective Setup

1. **Run validation first** - Know what needs fixing
2. **Document baseline** - Capture state before changes
3. **Verify each step** - Don't skip verification
4. **Re-run validation** - Confirm setup successful
5. **Keep rollback option** - Document how to undo
6. **Test with test branch** - Verify protection works
7. **Communicate changes** - Notify team of setup

---

## Common Issues and Solutions

### Issue 1: Development Branch Already Exists
**Problem**: Development branch exists with different configuration
**Solution**: Skip creation, verify branch configuration correct

### Issue 2: Workflow File Already Exists
**Problem**: PR validation workflow already present
**Solution**: Compare with standard, update if different, skip if same

### Issue 3: Cannot Configure Main Protection
**Problem**: Insufficient permissions to configure branch protection
**Solution**: Request admin access or have admin run setup

### Issue 4: Status Check Not Available
**Problem**: "check-source-branch" not yet available (workflow not run)
**Solution**: Configure protection but workflow will activate on first PR

### Issue 5: Development Protected by Org Policy
**Problem**: Organization requires all branches protected
**Solution**: Use minimal protection on development (PR reviews only, no status checks)

---

## Setup Checklist

Before setup:
- [ ] Repository exists
- [ ] Have admin access to repository
- [ ] Have gh CLI authenticated (or MCP server configured)
- [ ] Validated current state with validation skill

During setup:
- [ ] Development branch created or verified
- [ ] PR validation workflow created
- [ ] Workflow committed and pushed
- [ ] Main branch protection configured
- [ ] Development branch unprotected
- [ ] Each step verified

After setup:
- [ ] Run validation skill (should pass)
- [ ] Test creating branch from development
- [ ] Test cannot push to main directly
- [ ] Test cannot create PR from feature to main
- [ ] Test CAN create PR from development to main
- [ ] Document setup completion

---

## Rollback Procedures

### Rollback Development Branch Creation

```bash
# Delete local branch
git branch -D development

# Delete remote branch
git push origin --delete development
```

### Rollback PR Workflow

```bash
# Remove workflow file
git rm .github/workflows/pr-branch-check.yml
git commit -m "Remove PR branch validation workflow"
git push
```

### Rollback Main Protection

```bash
# Remove all protection
gh api repos/{owner}/{repo}/branches/main/protection -X DELETE
```

### Complete Rollback

```bash
# Run rollback script
python scripts/rollback_setup.py \
  --repo "myorg/myrepo" \
  --restore-baseline baseline-$(date +%Y%m%d).json
```

---

## Example: Complete Setup

```bash
# Step 1: Validate current state
python scripts/validate_repository.py --repo "myorg/new-repo" --check-all

# Output: FAIL - missing development, main not protected

# Step 2: Run complete setup
python scripts/setup_repository.py \
  --repo "myorg/new-repo" \
  --create-development \
  --add-pr-workflow \
  --protect-main \
  --verify \
  --generate-report

# Output:
# ✅ Created development branch from main
# ✅ Created PR branch validation workflow
# ✅ Committed workflow to development
# ✅ Configured main branch protection
# ✅ Verified development not protected
# ✅ Setup complete

# Step 3: Verify setup
python scripts/validate_repository.py --repo "myorg/new-repo" --check-all

# Output: PASS - Repository properly configured

# Step 4: Test protection
git checkout development
git checkout -b test-feature
# Try to create PR from test-feature to main (should fail)
# Try to create PR from development to main (should succeed)
```

---

**Last Updated**: 2025-01-30
