# Branch Protection Requirements

Required protection settings for main branch in agentic development workflow.

---

## Main Branch Protection

### Critical Requirements

**1. Require Pull Request Reviews**
- **Setting**: `required_pull_request_reviews.enabled = true`
- **Why**: Prevents direct commits to main branch
- **Impact**: All changes must go through PR process
- **Validation**: Check API response has `required_pull_request_reviews` object

**2. Require Status Checks to Pass**
- **Setting**: `required_status_checks.contexts = ["check-source-branch"]`
- **Why**: Ensures PR branch validation workflow passes
- **Impact**: PRs from non-development branches will be blocked
- **Validation**: Check `required_status_checks.contexts` contains "check-source-branch"

**3. Restrict Direct Pushes**
- **Setting**: `restrictions` configured or `enforce_admins = false` with no push access
- **Why**: Prevents accidental direct commits
- **Impact**: Only PRs can update main branch
- **Validation**: Check `restrictions` exists or verify no direct push access

**4. Require Linear History**
- **Setting**: `required_linear_history = true`
- **Why**: Keeps git history clean and readable
- **Impact**: Merge commits not allowed, must use squash or rebase
- **Validation**: Check `required_linear_history = true`

---

### Recommended Settings

**5. Dismiss Stale Pull Request Approvals**
- **Setting**: `required_pull_request_reviews.dismiss_stale_reviews = true`
- **Why**: New commits require fresh review
- **Impact**: Approvals reset when new commits pushed
- **Validation**: Check `dismiss_stale_reviews = true`

**6. Require Code Owners Review**
- **Setting**: `required_pull_request_reviews.require_code_owner_reviews = true`
- **Why**: Subject matter experts approve changes to their areas
- **Impact**: CODEOWNERS must approve PRs affecting their files
- **Validation**: Check `require_code_owner_reviews = true` AND CODEOWNERS file exists

**7. Strict Status Checks**
- **Setting**: `required_status_checks.strict = true`
- **Why**: Branch must be up-to-date with main before merge
- **Impact**: Forces conflict resolution before merge
- **Validation**: Check `strict = true`

---

### Optional Settings

**8. Include Administrators**
- **Setting**: `enforce_admins = true`
- **Why**: Even admins follow branch protection rules
- **Impact**: Admins cannot bypass protection
- **Validation**: Check `enforce_admins = true`

**9. Block Force Pushes**
- **Setting**: `allow_force_pushes = false`
- **Why**: Prevents history rewriting
- **Impact**: Cannot force push to main
- **Validation**: Check `allow_force_pushes = false`

**10. Block Branch Deletion**
- **Setting**: `allow_deletions = false`
- **Why**: Prevents accidental branch deletion
- **Impact**: Main branch cannot be deleted
- **Validation**: Check `allow_deletions = false`

---

## Development Branch Protection

### Requirements

**Development branch should NOT be protected**
- **Why**: Allows direct merges from feature/epic/wave branches
- **Impact**: Agents can merge without PR overhead
- **Validation**: Check development branch has NO protection rules

**Exception**: If team requires PR reviews for development
- Only require PR reviews
- Do NOT require status checks or restrictions
- Allow more relaxed review requirements

---

## Validation Levels

### CRITICAL (Must Have)

❌ **FAIL if missing**:
1. Main branch requires PR reviews
2. Main branch requires status checks (check-source-branch)
3. Main branch restricts direct pushes
4. Development branch exists

### WARNING (Should Have)

⚠️ **WARN if missing**:
5. Dismiss stale reviews enabled
6. Require Code Owners review (if CODEOWNERS exists)
7. Require linear history
8. Strict status checks

### OPTIONAL (Nice to Have)

ℹ️ **INFO if missing**:
9. Enforce admins in restrictions
10. Block force pushes
11. Block branch deletion

---

## API Response Structure

### Get Branch Protection

**Endpoint**: `GET /repos/{owner}/{repo}/branches/{branch}/protection`

**Response Structure**:
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
  "enforce_admins": {
    "enabled": false
  },
  "required_linear_history": {
    "enabled": true
  },
  "allow_force_pushes": {
    "enabled": false
  },
  "allow_deletions": {
    "enabled": false
  }
}
```

---

## Validation Script Logic

```python
def validate_main_protection(protection_data):
    """Validate main branch protection settings."""

    results = {
        "critical": [],
        "warnings": [],
        "optional": []
    }

    # CRITICAL: PR reviews required
    if not protection_data.get("required_pull_request_reviews"):
        results["critical"].append("❌ Pull request reviews not required")
    else:
        results["critical"].append("✅ Pull request reviews required")

    # CRITICAL: Status checks required
    status_checks = protection_data.get("required_status_checks", {})
    if "check-source-branch" not in status_checks.get("contexts", []):
        results["critical"].append("❌ PR branch validation check not required")
    else:
        results["critical"].append("✅ PR branch validation check required")

    # CRITICAL: Direct pushes restricted
    # (Check either restrictions exist or no push access configured)
    restrictions = protection_data.get("restrictions")
    if restrictions is None:
        results["critical"].append("⚠️ No push restrictions (verify access via other means)")
    else:
        results["critical"].append("✅ Direct push restrictions configured")

    # WARNING: Dismiss stale reviews
    pr_reviews = protection_data.get("required_pull_request_reviews", {})
    if pr_reviews.get("dismiss_stale_reviews"):
        results["warnings"].append("✅ Stale reviews dismissed on new commits")
    else:
        results["warnings"].append("⚠️ Stale reviews NOT dismissed (recommended)")

    # WARNING: Require linear history
    if protection_data.get("required_linear_history", {}).get("enabled"):
        results["warnings"].append("✅ Linear history required")
    else:
        results["warnings"].append("⚠️ Linear history not required (recommended)")

    # OPTIONAL: Enforce admins
    if protection_data.get("enforce_admins", {}).get("enabled"):
        results["optional"].append("✅ Admins included in restrictions")
    else:
        results["optional"].append("ℹ️ Admins not included in restrictions")

    # OPTIONAL: Block force pushes
    if not protection_data.get("allow_force_pushes", {}).get("enabled"):
        results["optional"].append("✅ Force pushes blocked")
    else:
        results["optional"].append("ℹ️ Force pushes allowed")

    # Determine overall status
    overall_status = "PASS"
    if any("❌" in item for item in results["critical"]):
        overall_status = "FAIL"
    elif any("⚠️" in item for item in results["warnings"]):
        overall_status = "WARNING"

    return {
        "status": overall_status,
        "results": results
    }
```

---

## Common Configuration Patterns

### Pattern 1: Basic Protection (Minimum)
```json
{
  "required_status_checks": {
    "strict": false,
    "contexts": ["check-source-branch"]
  },
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "enforce_admins": false,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

### Pattern 2: Recommended Protection
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

### Pattern 3: Strict Protection (With Code Owners)
```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["check-source-branch", "ci", "tests"]
  },
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": {
    "users": [],
    "teams": ["maintainers"]
  },
  "enforce_admins": true,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

---

**Last Updated**: 2025-01-30
