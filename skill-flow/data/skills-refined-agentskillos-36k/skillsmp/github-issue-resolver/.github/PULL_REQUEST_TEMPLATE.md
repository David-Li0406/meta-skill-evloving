# Description

<!-- Provide a clear and concise description of your changes -->
<!-- Explain what problem this PR solves or what feature it adds -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] CI/CD update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement

## Target Branch

<!-- Check the branch this PR is targeting -->

- [ ] `main` (OpenShift 4.18 / Kubernetes 1.31)
- [ ] `release-4.18` (OpenShift 4.18)
- [ ] `release-4.19` (OpenShift 4.19 / Kubernetes 1.32)
- [ ] `release-4.20` (OpenShift 4.20 / Kubernetes 1.33)

## Testing Performed

<!-- Describe the tests you ran to verify your changes -->
<!-- Check all that apply and provide details -->

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Tested on OpenShift cluster (specify version: ___)
- [ ] Tested with Coordination Engine integration
- [ ] Tested with KServe integration

**Test Details:**
<!-- Describe your testing process and results -->

## Checklist

<!-- Ensure all items are completed before requesting review -->

- [ ] Code follows project style guidelines (`make lint` passes)
- [ ] Tests pass locally (`make test` passes)
- [ ] Binary builds successfully (`make build` passes)
- [ ] Helm chart validation passes (`make helm-lint` passes, if charts modified)
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow Conventional Commits format
- [ ] No new security vulnerabilities introduced (`make security-gosec` passes)
- [ ] Code is properly commented, especially complex logic
- [ ] All conversations resolved (before merging)

## Related Issues

<!-- Link related issues using GitHub keywords -->
<!-- Examples: Fixes #123, Resolves #456, Relates to #789 -->

## Additional Context

<!-- Add any other context, screenshots, or information about the PR here -->
<!-- If this is a breaking change, describe migration path for users -->

## Rollback Plan

<!-- For significant changes, describe how to rollback if needed -->
<!-- Example: Revert this PR, or redeploy previous version, or specific steps -->

---

**For Reviewers:**

- [ ] Code review completed
- [ ] Architecture/design approved
- [ ] Security considerations reviewed
- [ ] Documentation is clear and complete
- [ ] Tests provide adequate coverage
