# Setup Steps - Detailed Guide

Detailed walkthrough of each setup step with explanations and verification.

---

## Overview

**Setup Process**: 6 main steps

1. Check current configuration (baseline)
2. Create development branch (if missing)
3. Create PR branch validation workflow
4. Configure main branch protection
5. Verify development branch not protected
6. Generate setup report and validate

**Total Time**: 5-10 minutes

**Prerequisites**:
- Repository exists
- Admin access to repository
- `gh` CLI authenticated OR Git MCP server configured
- Git client installed

---

## Step 1: Check Current Configuration

**Purpose**: Establish baseline before making changes

**Actions**:
- List all branches
- Check main branch protection status
- Check development branch existence
- Capture current state for rollback

**Commands**:
```bash
# List branches
git fetch --all
git branch -a

# Check main protection (via gh CLI)
gh api repos/{owner}/{repo}/branches/main/protection

# Or via Git MCP
mcp__git__list_branches()
mcp__git__get_branch_protection(branch: "main")
```

**Expected Output**:
```json
{
  "branches": ["main"],
  "main_protected": false,
  "development_exists": false,
  "baseline_captured": true
}
```

**Verification**:
- Know which branches exist
- Know current protection status
- Baseline documented

**Why This Matters**:
- Prevents duplicate work
- Enables rollback if needed
- Documents configuration history

---

## Step 2: Create Development Branch

**Purpose**: Create integration branch for all work

**Pre-Check**:
```bash
# Check if development exists locally
git branch --list development

# Check if development exists remotely
git ls-remote --heads origin development
```

**If Development Exists**:
```bash
# Just checkout and update
git checkout development
git pull origin development
echo "✅ Development branch already exists"
```

**If Development Missing**:
```bash
# Create from main
git checkout main
git pull origin main
git checkout -b development
git push -u origin development
echo "✅ Development branch created from main"
```

**Via Git MCP**:
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

**Expected Output**:
```
Switched to a new branch 'development'
Branch 'development' set up to track remote branch 'development' from 'origin'.
```

**Verification**:
```bash
# Verify branch exists locally
git branch --show-current
# Output: development

# Verify branch exists remotely
git ls-remote --heads origin development
# Output: refs/heads/development

# Verify branch tracks remote
git branch -vv
# Output: * development abc1234 [origin/development] ...
```

**Why This Matters**:
- Development branch is integration point for all work
- Keeps main clean and protected
- Allows rapid iteration without PR overhead

**Common Issues**:
- **Development exists but not tracking remote**: `git branch -u origin/development`
- **Development exists but behind main**: `git pull origin main` then `git push`
- **Development exists but diverged**: Decide on merge or rebase strategy

---

## Step 3: Create PR Branch Validation Workflow

**Purpose**: Enforce only `development → main` PRs allowed

**Create Workflow Directory**:
```bash
mkdir -p .github/workflows
```

**Create Workflow File**:

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

**Via Script**:
```bash
python scripts/create_pr_workflow.py \
  --output ".github/workflows/pr-branch-check.yml"
```

**Via Git MCP**:
```
mcp__git__write_file(
  path: ".github/workflows/pr-branch-check.yml",
  content: [workflow yaml above]
)
```

**Commit and Push**:
```bash
git add .github/workflows/pr-branch-check.yml
git commit -m "Add PR branch validation workflow

- Enforces PRs to main must come from development
- Automatic check runs on all PRs to main
- Prevents agents/users from creating PRs from wrong branches"
git push origin development
```

**Expected Output**:
```
[development abc1234] Add PR branch validation workflow
 1 file changed, 35 insertions(+)
 create mode 100644 .github/workflows/pr-branch-check.yml
```

**Verification**:
```bash
# Verify file exists
ls -la .github/workflows/pr-branch-check.yml

# Verify file committed
git log -1 --stat

# Verify file on remote
gh api repos/{owner}/{repo}/contents/.github/workflows/pr-branch-check.yml
```

**Why This Matters**:
- Automated enforcement of branching policy
- Prevents accidental PRs from wrong branches
- Clear error messages for developers
- Works for both human and agent developers

**Workflow Behavior**:
- Triggers on any PR to main
- Checks source branch is development
- Exits with error (status 1) if wrong source
- GitHub blocks PR merge if workflow fails

---

## Step 4: Configure Main Branch Protection

**Purpose**: Protect main branch from direct commits and enforce PR policy

**Protection Configuration**:

**File**: `protection-config.json`
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

**Apply via gh CLI**:
```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  --input protection-config.json
```

**Or via curl**:
```bash
curl -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/{owner}/{repo}/branches/main/protection \
  -d @protection-config.json
```

**Via Script**:
```bash
python scripts/configure_branch_protection.py \
  --repo "{owner}/{repo}" \
  --branch "main" \
  --config "protection-config.json"
```

**Expected Output**:
```json
{
  "url": "https://api.github.com/repos/{owner}/{repo}/branches/main/protection",
  "required_status_checks": {
    "url": "...",
    "strict": true,
    "contexts": ["check-source-branch"],
    "contexts_url": "..."
  },
  "required_pull_request_reviews": {...},
  "enforce_admins": {...},
  "required_linear_history": {"enabled": true},
  "allow_force_pushes": {"enabled": false},
  "allow_deletions": {"enabled": false}
}
```

**Verification**:
```bash
# Check protection applied
gh api repos/{owner}/{repo}/branches/main/protection

# Or via Git MCP
mcp__git__get_branch_protection(branch: "main")

# Try to push directly to main (should fail)
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test direct commit"
git push origin main
# Expected: ERROR - push declined due to branch protection
```

**Why This Matters**:
- Prevents accidental direct commits to main
- Enforces PR review process
- Ensures CI checks pass (PR branch validation)
- Maintains clean git history

**Protection Rules Explained**:

1. **required_status_checks**: Requires "check-source-branch" to pass before merge
2. **strict: true**: Branch must be up-to-date with main before merge
3. **required_pull_request_reviews**: PRs must be reviewed (count 0 = just need PR, no approval)
4. **dismiss_stale_reviews**: New commits reset approvals
5. **required_linear_history**: No merge commits, squash or rebase only
6. **allow_force_pushes: false**: Cannot rewrite history on main
7. **allow_deletions: false**: Cannot delete main branch

---

## Step 5: Verify Development Branch Not Protected

**Purpose**: Ensure development allows direct merges from feature branches

**Check Protection**:
```bash
gh api repos/{owner}/{repo}/branches/development/protection
```

**Expected Output**:
```
{
  "message": "Branch not protected",
  "documentation_url": "..."
}
```

**Or HTTP 404** (branch protection doesn't exist)

**If Development IS Protected** (incorrect):
```bash
# Remove protection
gh api repos/{owner}/{repo}/branches/development/protection -X DELETE

# Via script
python scripts/remove_branch_protection.py \
  --repo "{owner}/{repo}" \
  --branch "development" \
  --confirm
```

**Expected Output**:
```
Branch protection removed from 'development'
```

**Verification**:
```bash
# Test direct push to development
git checkout development
echo "test" >> test.txt
git add test.txt
git commit -m "test direct commit to development"
git push origin development
# Expected: SUCCESS - push accepted
```

**Why This Matters**:
- Development is integration branch, needs flexibility
- Agents merge feature branches directly to development
- PR overhead would slow down agentic workflow
- Quality gate is at development → main, not before

**When Development Protection Is OK**:
- Organization policy requires all branches protected
- Team wants code review for all changes
- Use minimal protection (PR reviews only, no status checks)

**Minimal Protection for Development** (if required):
```json
{
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "required_status_checks": null,
  "restrictions": null,
  "enforce_admins": false,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

---

## Step 6: Generate Setup Report and Validate

**Purpose**: Document setup and verify success

**Generate Report**:
```bash
python scripts/setup_repository.py \
  --repo "{owner}/{repo}" \
  --generate-report
```

**Report Structure**:
```markdown
## Repository Setup Report

**Repository**: myorg/myrepo
**Date**: 2025-01-30T10:30:00Z
**Status**: ✅ COMPLETE

### Actions Performed

1. **Development Branch**
   - ✅ Created from main (or verified existing)
   - ✅ Pushed to remote
   - ✅ Verified accessible

2. **PR Branch Validation Workflow**
   - ✅ Created .github/workflows/pr-branch-check.yml
   - ✅ Committed to development
   - ✅ Pushed to remote

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

Validation skill status: PASS

### Configuration Files

- `.github/workflows/pr-branch-check.yml` - PR branch validation workflow
- `protection-config.json` - Branch protection configuration (for reference)

### Rollback Information

Baseline state captured: baseline-20250130-103000.json

To rollback:
```bash
python scripts/rollback_setup.py \
  --repo "myorg/myrepo" \
  --restore-baseline baseline-20250130-103000.json
```

### Next Steps

1. Start creating feature branches from development
2. Follow agentic branching strategy (invoke `git-agentic-branching-strategy` skill)
3. Create PRs from development to main when ready to release
```

**Run Validation**:
```bash
# Invoke validation skill
python scripts/validate_repository.py \
  --repo "{owner}/{repo}" \
  --check-all
```

**Expected Validation Result**: PASS

**Verification Tests**:
```bash
# Test 1: Can create branch from development
git checkout development
git checkout -b test-feature
git push origin test-feature
# Expected: SUCCESS

# Test 2: Cannot push directly to main
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
# Expected: ERROR - push declined

# Test 3: Cannot create PR from feature to main
gh pr create --base main --head test-feature
# Expected: ERROR - PR check will fail

# Test 4: CAN create PR from development to main
git checkout development
gh pr create --base main --head development
# Expected: SUCCESS - PR created and check passes
```

---

## Post-Setup Configuration

### Optional: Add CODEOWNERS File

```bash
# Create CODEOWNERS
cat > .github/CODEOWNERS <<'EOF'
# Default owners for everything
* @myorg/maintainers

# Specific paths
/docs/ @myorg/tech-writers
/src/api/ @myorg/backend-team
/src/ui/ @myorg/frontend-team
EOF

# Commit to development
git add .github/CODEOWNERS
git commit -m "Add CODEOWNERS file"
git push origin development

# Update main protection to require Code Owners review
gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input - <<'EOF'
{
  ...
  "required_pull_request_reviews": {
    ...
    "require_code_owner_reviews": true
  }
  ...
}
EOF
```

---

### Optional: Add CI Workflow

```bash
# Create CI workflow
cat > .github/workflows/ci.yml <<'EOF'
name: CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: ['**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup
        run: npm install
      - name: Lint
        run: npm run lint
      - name: Test
        run: npm test
      - name: Build
        run: npm run build
EOF

# Commit to development
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
git push origin development

# Update main protection to require CI checks
gh api repos/{owner}/{repo}/branches/main/protection -X PATCH --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["check-source-branch", "test"]
  }
}
EOF
```

---

## Troubleshooting

### Issue: Insufficient Permissions

**Symptom**: Cannot configure branch protection

**Error**:
```
403 Forbidden - Must have admin rights to repository
```

**Solution**:
- Request admin access to repository
- Have repository admin run setup
- Use organization-level policies instead

---

### Issue: Workflow Not Appearing

**Symptom**: PR branch check workflow created but not showing in PR

**Causes**:
- Workflow file has syntax error
- Workflow not committed to default branch
- Workflow trigger doesn't match PR

**Solution**:
```bash
# Validate workflow syntax
gh workflow list

# Check workflow file location
ls -la .github/workflows/pr-branch-check.yml

# Verify committed to development
git log -- .github/workflows/pr-branch-check.yml

# Trigger test
# Create test PR to main and check workflow runs
```

---

### Issue: Development Branch Protected by Org Policy

**Symptom**: Cannot remove protection from development

**Error**:
```
422 Unprocessable Entity - Organization policy requires branch protection
```

**Solution**:
- Use minimal protection on development (PR reviews only)
- Request org policy exception for development branch
- Document exception in org policy

---

**Last Updated**: 2025-01-30
