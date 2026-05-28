---
name: github-actions-debug
description: Use this skill when debugging GitHub Actions workflows, CI/CD pipeline failures, or Terraform errors to identify and resolve issues effectively.
---

# Skill body

## When to Use

- User mentions a failed deployment or CI/CD failure
- GitHub Actions workflow failures
- Terraform state lock errors
- Authentication or authorization failures
- Resource issues during deployment
- Test failures in CI environment
- Artifact upload/download issues
- Timeout issues

## Debugging Process

### Step 1: Check Recent Workflow Runs

```bash
gh run list --workflow=<workflow_file> --limit 10
```

### Step 2: View Failed Logs

```bash
gh run view <run-id> --log-failed
```

### Step 3: Identify the Issue

Look for these common patterns in the logs:

#### Terraform State Lock
**Pattern:** `Error acquiring the state lock` or `state blob is already locked`

**Cause:** Previous workflow was cancelled mid-execution, leaving the state locked.

**Fix:**
1. Extract the Lock ID from the error (looks like `efd4cede-d5a2-61c3-31db-462852989510`)
2. Run: `cd infra && terraform force-unlock -force <lock-id>`
3. Re-run the workflow: `gh run rerun <run-id>`

#### Authentication Failures
**Pattern:** `AuthorizationFailed`, `AADSTS`, `unauthorized`

**Fix:** Check that `AZURE_CREDENTIALS` secret is valid. The service principal may need credential rotation.

#### Resource Not Found
**Pattern:** `ResourceNotFound` or `does not exist`

**Fix:** Resource was deleted outside Terraform. Run `terraform refresh` or re-import.

#### Azure Quota Exceeded
**Pattern:** `QuotaExceeded`

**Fix:** Request quota increase in Azure portal or clean up unused resources.

#### Test Failures
**Pattern:** `FAILED`, `pytest`, `AssertionError`

**Fix:** Review test output and fix failing tests.

#### Gradle Build Failures
**Error:** Gradle daemon issues or out of memory

**Solution**:
- Check `android/gradle-ci.properties` settings
- Verify heap size (3GB for CI)
- Ensure parallel builds limited (2 workers for CI)
- Disable daemon in CI: `org.gradle.daemon=false`

### Step 4: Apply Necessary Fixes

Make the required changes to workflow files or source code based on the identified issues.

### Step 5: Verify

Re-run the workflow to confirm that the issues have been resolved:

```bash
gh run rerun <run-id>
```