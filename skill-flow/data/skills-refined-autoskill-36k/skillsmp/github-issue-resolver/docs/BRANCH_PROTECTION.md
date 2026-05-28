# Branch Protection Rules

This document describes the branch protection rules configured for the OpenShift Cluster Health MCP repository to maintain code quality, security, and stability.

## Overview

Branch protection ensures that all changes to critical branches go through a rigorous review and validation process. This prevents accidental or unauthorized changes and maintains the integrity of the codebase.

This implementation follows **[ADR-014: Branch Protection Strategy](adrs/014-branch-protection-strategy.md)**, which documents the architectural decisions and rationale for our tiered protection model.

## Protected Branches

### Main Branch (`main`)

The `main` branch serves as the primary development branch targeting OpenShift 4.18 (Kubernetes 1.31).

**Protection Settings:**
- **Required Reviews**: 1 approval from code owners
- **Required Status Checks**: All 6 CI checks must pass
- **Require Branches Up-to-Date**: Yes
- **Require Conversation Resolution**: Yes
- **Force Push**: Disabled
- **Branch Deletion**: Disabled
- **Admin Bypass**: Allowed (for emergencies only)

**Status Checks Required:**
1. **Test** - Unit tests with race detection
2. **Lint** - Code quality checks with golangci-lint
3. **Build** - Binary compilation and size verification
4. **Security** - Trivy vulnerability scanning
5. **Helm** - Helm chart validation
6. **build-and-push** - Container image build verification

### Release Branches

The following release branches are protected with stricter requirements:

- **`release-4.18`** - OpenShift 4.18 (Kubernetes 1.31)
- **`release-4.19`** - OpenShift 4.19 (Kubernetes 1.32)
- **`release-4.20`** - OpenShift 4.20 (Kubernetes 1.33)

**Protection Settings:**
- **Required Reviews**: 2 approvals from code owners (higher bar than main)
- **Required Status Checks**: All 6 CI checks must pass
- **Require Branches Up-to-Date**: Yes
- **Require Conversation Resolution**: Yes
- **Force Push**: Disabled
- **Branch Deletion**: Disabled
- **Admin Bypass**: Allowed (for emergencies only)

**Status Checks Required:**
Same as main branch (Test, Lint, Build, Security, Helm, build-and-push)

### End of Life (EOL) Branches

The following release branches have been deleted as their corresponding OpenShift versions reached end of life:

- **`release-4.17`** - Deleted 2026-01-17 (OpenShift 4.17 EOL)

See [ADR-014: Branch Protection Strategy](adrs/014-branch-protection-strategy.md) for branch lifecycle management process.

## Required Status Checks Explained

### 1. Test

**What it checks:** Unit tests with race condition detection

**Workflow:** `.github/workflows/ci.yml`

**Command:** `go test -v -race -coverprofile=coverage.out ./...`

**Why it's required:** Ensures all unit tests pass and no race conditions are introduced. Maintains code correctness and thread safety.

**Common failures:**
- Test failures due to logic errors
- Race condition detection
- Insufficient test coverage

**How to fix:** Run `make test` locally to reproduce and fix issues.

### 2. Lint

**What it checks:** Code quality and style compliance

**Workflow:** `.github/workflows/ci.yml`

**Tool:** golangci-lint (latest version)

**Why it's required:** Enforces consistent code style, catches common bugs, and improves code maintainability.

**Common failures:**
- Unused variables or imports
- Missing error checks
- Code complexity issues
- Style violations

**How to fix:** Run `make lint` locally and address reported issues.

### 3. Build

**What it checks:** Binary compilation and size limits

**Workflow:** `.github/workflows/ci.yml`

**Command:** `CGO_ENABLED=0 go build -ldflags="-s -w" -o bin/mcp-server ./cmd/mcp-server`

**Size limit:** 50MB maximum

**Why it's required:** Ensures the code compiles successfully and the binary size is within acceptable limits for container images.

**Common failures:**
- Compilation errors
- Binary size exceeds 50MB

**How to fix:** Run `make build` locally to reproduce compilation errors. Use `make build-prod` to check binary size.

### 4. Security

**What it checks:** Security vulnerabilities in code and dependencies

**Workflow:** `.github/workflows/ci.yml`

**Tool:** Trivy filesystem scanner

**Why it's required:** Prevents introduction of known security vulnerabilities. Critical for production deployments.

**Common failures:**
- Known CVEs in dependencies
- Security-sensitive code patterns
- Vulnerable package versions

**How to fix:** Run `make security-gosec` locally. Update vulnerable dependencies or use alternative packages.

### 5. Helm

**What it checks:** Helm chart validation

**Workflow:** `.github/workflows/ci.yml`

**Command:** `helm lint charts/openshift-cluster-health-mcp`

**Why it's required:** Ensures Helm chart syntax is correct and templates render properly.

**Common failures:**
- YAML syntax errors
- Invalid template syntax
- Missing required values

**How to fix:** Run `make helm-lint` locally and fix reported issues.

### 6. build-and-push

**What it checks:** Container image builds successfully

**Workflow:** `.github/workflows/container.yml`

**Platform:** linux/amd64

**Why it's required:** Ensures the Dockerfile is valid and the container image builds successfully.

**Common failures:**
- Dockerfile syntax errors
- Missing dependencies
- Image size too large

**How to fix:** Run `make docker-build` locally to reproduce and fix issues.

## Making Changes to Protected Branches

### Step-by-Step Process

1. **Sync your fork** with the upstream repository:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

2. **Create a feature branch** from the appropriate base:
   ```bash
   # For features targeting main
   git checkout -b feature/my-feature main

   # For fixes to release-4.19
   git checkout -b fix/my-fix release-4.19
   ```

3. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "feat(scope): descriptive message"
   ```

4. **Run local validation** before pushing:
   ```bash
   make test          # Run unit tests
   make lint          # Run linters
   make build         # Verify compilation
   make helm-lint     # Validate Helm charts (if modified)
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

6. **Open a Pull Request** on GitHub:
   - Fill out the PR template completely
   - Link related issues
   - Wait for CI checks to complete

7. **Address review feedback**:
   - Make requested changes
   - Push updates to the same branch
   - Mark conversations as resolved
   - Request re-review

8. **Merge** once approved:
   - All CI checks must be green
   - Required approvals obtained
   - All conversations resolved
   - Branch is up-to-date with base

## Bypassing Branch Protection

### When is it allowed?

Branch protection can be bypassed **only by repository administrators** and **only in emergency situations**:

- Critical security patch needed immediately
- Production outage requiring hotfix
- Broken CI pipeline blocking all PRs

### How to bypass (Admins only)

1. **Attempt the push** - GitHub will show bypass option for admins
2. **Document the reason** in the commit message
3. **Create a tracking issue** explaining the bypass
4. **Post-merge review** - Create a PR for the commit to be reviewed retroactively

**Example commit message:**
```
fix: emergency hotfix for CVE-2024-XXXXX

EMERGENCY BYPASS: Critical security vulnerability in kubernetes client.
Normal PR process would delay patch by 24+ hours.

Tracking issue: #456
Post-merge review PR: #457
```

### Best Practices

- **Avoid bypassing whenever possible** - Use only as a last resort
- **Document thoroughly** - Explain why it was necessary
- **Review afterward** - Create a follow-up PR for code review
- **Learn from it** - Update processes to avoid future bypasses

## Troubleshooting Common Issues

### Issue: "Required status check is not present"

**Cause:** GitHub doesn't recognize the status check name, or the check hasn't run yet on this PR.

**Solution:**
1. Ensure CI workflows are running (check Actions tab)
2. Verify the status check name matches exactly (case-sensitive)
3. Wait for at least one PR to complete all checks (GitHub learns available checks from completed runs)
4. Push a new commit to re-trigger CI

### Issue: "Review required from code owner"

**Cause:** Changes affect files with designated code owners in `.github/CODEOWNERS`, but no code owner has reviewed yet.

**Solution:**
1. Check `.github/CODEOWNERS` to see who owns the modified files
2. Request review from the designated code owner
3. Wait for their approval

### Issue: "Branch is out of date"

**Cause:** Base branch has new commits since your PR was opened. Protection requires branches to be up-to-date before merging.

**Solution:**
```bash
# Update your local base branch
git fetch upstream
git checkout main
git merge upstream/main

# Merge into your feature branch
git checkout feature/my-feature
git merge main

# Or rebase (cleaner history)
git rebase main

# Push the update
git push origin feature/my-feature --force-with-lease
```

### Issue: "Conversations must be resolved"

**Cause:** There are unresolved comment threads on the PR.

**Solution:**
1. Review all comment threads
2. Address each comment
3. Click "Resolve conversation" when addressed
4. Request re-review if needed

### Issue: "Cannot push to protected branch"

**Cause:** Attempting to push directly to a protected branch instead of using a PR.

**Solution:**
1. Create a feature branch: `git checkout -b feature/my-change`
2. Push to the feature branch: `git push origin feature/my-change`
3. Open a Pull Request from the feature branch

### Issue: "CI check failing but passes locally"

**Cause:** Different environment, dependencies, or configuration between local and CI.

**Solution:**
1. Check the CI logs for detailed error messages
2. Ensure your local Go version matches CI (1.24+)
3. Run `go mod tidy` to sync dependencies
4. Check for OS-specific issues (CI runs on Ubuntu Linux)
5. Verify environment variables are correctly set

### Issue: "Lint check failing with 'missing error check'"

**Cause:** golangci-lint detected an error that isn't being checked.

**Solution:**
```go
// Bad
data, _ := json.Marshal(obj)

// Good
data, err := json.Marshal(obj)
if err != nil {
    return fmt.Errorf("failed to marshal: %w", err)
}
```

Run `make lint` locally to catch these before pushing.

## Branch Protection Settings Reference

### Comparison Table

| Setting | main | release-* |
|---------|------|-----------|
| Required Approvals | 1 | 2 |
| Dismiss Stale Reviews | ✅ | ✅ |
| Require Code Owner Review | ✅ | ✅ |
| Required Status Checks | 6 checks | 6 checks |
| Require Up-to-Date Branch | ✅ | ✅ |
| Require Conversation Resolution | ✅ | ✅ |
| Enforce for Admins | ✅ (can bypass) | ✅ (can bypass) |
| Allow Force Push | ❌ | ❌ |
| Allow Deletions | ❌ | ❌ |

### Why Different Approval Counts?

- **Main branch (1 approval)**: Faster iteration for development features. Single approval balances velocity with quality.

- **Release branches (2 approvals)**: Higher scrutiny for production-bound code. Two approvals ensure multiple perspectives and catch edge cases.

## Metrics and Monitoring

### Success Indicators

Track these metrics to ensure branch protection is working effectively:

- **PR Merge Rate**: Percentage of PRs merged vs. closed without merging
- **Time to Merge**: Average time from PR creation to merge
- **CI Pass Rate**: Percentage of CI runs that pass on first attempt
- **Bypass Frequency**: Number of admin bypasses (should be near zero)
- **Code Review Turnaround**: Time from PR submission to first review

### Expected Baselines

- PR Merge Rate: >80%
- Time to Merge: <48 hours
- CI Pass Rate: >85%
- Bypass Frequency: <1 per month
- Review Turnaround: <24 hours

## Related Documentation

- **[ADR-014: Branch Protection Strategy](adrs/014-branch-protection-strategy.md)** - Architectural decision and rationale
- [CONTRIBUTING.md](../.github/CONTRIBUTING.md) - Contribution guidelines
- [CODEOWNERS](../.github/CODEOWNERS) - Code ownership definitions
- [GitHub Actions Workflows](../.github/workflows/) - CI/CD configuration
- [Architecture Decision Records](./adrs/) - Technical decision documentation

## Updating Branch Protection

To modify branch protection rules:

1. **Discuss the change** in a GitHub issue first
2. **Update this documentation** to reflect proposed changes
3. **Run the setup script** with updated settings:
   ```bash
   # Edit scripts/setup-branch-protection.sh
   ./scripts/setup-branch-protection.sh
   ```
4. **Verify the changes**:
   ```bash
   ./scripts/verify-branch-protection.sh
   ```
5. **Communicate to contributors** about the change

## Questions?

If you have questions about branch protection:

- **General questions**: Open a GitHub Discussion
- **Specific issues**: Open a GitHub Issue
- **Urgent matters**: Contact repository administrators directly

For security-sensitive questions, use private channels or security@yourorg.com.
