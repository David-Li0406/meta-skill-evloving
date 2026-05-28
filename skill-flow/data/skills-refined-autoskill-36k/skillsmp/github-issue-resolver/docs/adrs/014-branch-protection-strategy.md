# ADR-014: Branch Protection Strategy

## Status

**ACCEPTED** - 2026-01-17

## Context

The OpenShift Cluster Health MCP Server is a critical component of the OpenShift AI Ops Platform that integrates with OpenShift Lightspeed to provide cluster health monitoring and AI-powered operations. As the project matures and moves toward production deployments, we need a formal branch protection strategy to ensure code quality, prevent unauthorized changes, and maintain stability across multiple OpenShift release branches.

### Repository Structure

The repository maintains multiple branches to align with OpenShift release cycles:

- **`main`**: Primary development branch targeting OpenShift 4.18 (Kubernetes 1.31)
- **Release branches**: Version-specific branches for OpenShift releases
  - `release-4.18`: OpenShift 4.18 (Kubernetes 1.31)
  - `release-4.19`: OpenShift 4.19 (Kubernetes 1.32)
  - `release-4.20`: OpenShift 4.20 (Kubernetes 1.33)

### Development Workflow Characteristics

1. **Continuous Integration**: GitHub Actions runs 6 required CI checks (Test, Lint, Build, Security, Helm, Container Build)
2. **Code Ownership**: `.github/CODEOWNERS` defines ownership for different parts of the codebase
3. **Multiple Contributors**: Open source project with external contributors and maintainers
4. **Production Impact**: Changes directly affect OpenShift Lightspeed integration and cluster operations
5. **Security Sensitive**: Requires Kubernetes cluster access and handles sensitive operational data

### Risk Factors

| Risk | Impact | Probability |
|------|--------|-------------|
| **Untested code in production** | Critical | Medium |
| **Security vulnerabilities merged** | Critical | Low |
| **Breaking changes without review** | High | Medium |
| **Accidental force push** | High | Low |
| **Direct commits to main/release** | Medium | Medium |

### Industry Best Practices

- **GitHub Flow**: All changes via pull requests, never direct commits
- **Required Reviews**: Minimum 1-2 approvals based on branch criticality
- **Status Checks**: All CI tests must pass before merge
- **Conversation Resolution**: All review comments addressed before merge
- **No Force Push**: Protect git history integrity

## Decision

We will implement **tiered branch protection** with different requirements based on branch criticality:

### Protection Tier 1: Main Branch (`main`)

**Purpose**: Active development branch, faster iteration for new features

**Protection Rules**:
- **Required Approvals**: 1 approval from code owners
- **Required Status Checks**: All 6 CI checks must pass
  1. Test - Unit tests with race detection
  2. Lint - Code quality checks (golangci-lint)
  3. Build - Binary compilation and size verification
  4. Security - Trivy vulnerability scanning
  5. Helm - Helm chart validation
  6. build-and-push - Container image build verification
- **Require Branches Up-to-Date**: Yes (must merge latest main before merging PR)
- **Require Conversation Resolution**: Yes (all review threads must be resolved)
- **Force Push**: Disabled
- **Branch Deletion**: Disabled
- **Admin Bypass**: Allowed (for emergencies only)

### Protection Tier 2: Release Branches (`release-4.x`)

**Purpose**: Production-bound code for specific OpenShift versions

**Protection Rules**:
- **Required Approvals**: 2 approvals from code owners (higher bar than main)
- **Required Status Checks**: Same 6 CI checks as main
- **Require Branches Up-to-Date**: Yes
- **Require Conversation Resolution**: Yes
- **Force Push**: Disabled
- **Branch Deletion**: Disabled
- **Admin Bypass**: Allowed (for emergencies only)

### Rationale for Different Approval Counts

- **Main branch (1 approval)**: Balances velocity with quality. Single approval allows faster iteration for development features while maintaining code review discipline.

- **Release branches (2 approvals)**: Higher scrutiny for production-bound code. Two approvals ensure multiple perspectives, catch edge cases, and reduce risk of regressions in stable releases.

### Branch Lifecycle Management

1. **Creation**: Release branches created from `main` when OpenShift version support begins
2. **Active Support**: Branches receive bugfixes and security patches
3. **End of Life (EOL)**: Branches deleted when OpenShift version is EOL
   - Example: `release-4.17` deleted on 2026-01-17 (OpenShift 4.17 EOL)
4. **Automation**: Scripts in `scripts/` directory manage protection setup and verification

## Rationale

### Why Branch Protection?

1. **Quality Assurance**: Required CI checks prevent broken code from merging
2. **Code Review Discipline**: Mandatory approvals ensure peer review of all changes
3. **Security**: Prevent accidental merge of vulnerable dependencies or insecure code
4. **Audit Trail**: All changes documented in pull requests with review history
5. **Collaboration**: Structured review process encourages knowledge sharing
6. **Rollback Safety**: Protected history enables reliable rollbacks if issues arise

### Why Tiered Protection?

1. **Development Velocity**: Main branch needs faster iteration (1 approval)
2. **Release Stability**: Release branches require higher scrutiny (2 approvals)
3. **Risk-Based Approach**: Protection level matches potential impact
4. **Industry Standard**: Mirrors practices from Kubernetes, OpenShift, and other CNCF projects

### Why These Specific CI Checks?

| Check | Rationale | Failure Impact |
|-------|-----------|----------------|
| **Test** | Ensures functionality correctness, catches regressions | Code may break at runtime |
| **Lint** | Enforces code style, catches common bugs | Technical debt, maintainability issues |
| **Build** | Validates compilation, checks binary size | Deployment failures |
| **Security** | Scans for CVEs and vulnerabilities | Security breaches, compliance violations |
| **Helm** | Validates Kubernetes deployment config | Installation failures |
| **build-and-push** | Ensures container image builds | Deployment blockers |

## Alternatives Considered

### No Branch Protection

**Pros**:
- Maximum development flexibility
- No merge delays
- Simpler workflow for new contributors

**Cons**:
- ❌ **High risk of broken main/release branches**
- ❌ No code review enforcement
- ❌ Security vulnerabilities can slip through
- ❌ No CI validation before merge
- ❌ Unacceptable for production-critical code

**Verdict**: Rejected - too risky for enterprise integration

### Same Protection for All Branches

**Pros**:
- Consistent policy
- Simpler to explain
- No confusion about requirements

**Cons**:
- ❌ Slows down main branch development
- ❌ Doesn't reflect different risk profiles
- ❌ One-size-fits-all approach

**Verdict**: Rejected - tiered approach better balances velocity and safety

### Protected Main Only

**Pros**:
- Simpler initial setup
- Less maintenance

**Cons**:
- ❌ **Release branches unprotected**
- ❌ Production code vulnerable to direct commits
- ❌ Inconsistent protection model

**Verdict**: Rejected - release branches need protection

### Higher Approval Count (3+ approvals)

**Pros**:
- More perspectives on code
- Higher confidence in changes

**Cons**:
- ❌ Significantly slows down development
- ❌ Difficult to find 3 available reviewers
- ❌ Diminishing returns after 2 reviewers
- ❌ Not aligned with industry standards (most projects use 1-2)

**Verdict**: Rejected - 2 approvals sufficient for release branches

### Separate Repository for Releases

**Pros**:
- Complete isolation of release code
- Different access control per repo

**Cons**:
- ❌ Operational complexity (multiple repos)
- ❌ Difficult to backport fixes
- ❌ Fragmented contribution workflow
- ❌ Industry anti-pattern (Kubernetes uses single repo)

**Verdict**: Rejected - single repo with protected branches is standard

## Implementation Details

### Automation Scripts

```bash
# Setup branch protection (idempotent)
./scripts/setup-branch-protection.sh

# Verify protection is correctly configured
./scripts/verify-branch-protection.sh
```

### Script Capabilities

1. **`setup-branch-protection.sh`**:
   - Checks GitHub CLI authentication
   - Verifies admin permissions
   - Configures protection via GitHub API
   - Handles missing branches gracefully
   - Idempotent (safe to run multiple times)

2. **`verify-branch-protection.sh`**:
   - Validates all protection settings
   - Checks required status checks
   - Verifies approval requirements
   - Reports misconfigurations
   - Returns exit code for CI integration

### Protected Branches Configuration

```yaml
# Maintained branches (as of 2026-01-17)
protected_branches:
  - name: main
    required_approvals: 1
    openshift_version: "4.18"
    kubernetes_version: "1.31"

  - name: release-4.18
    required_approvals: 2
    openshift_version: "4.18"
    kubernetes_version: "1.31"

  - name: release-4.19
    required_approvals: 2
    openshift_version: "4.19"
    kubernetes_version: "1.32"

  - name: release-4.20
    required_approvals: 2
    openshift_version: "4.20"
    kubernetes_version: "1.33"

# Deleted branches (EOL)
deleted_branches:
  - name: release-4.17
    deleted_date: "2026-01-17"
    reason: "OpenShift 4.17 End of Life"
```

### GitHub API Protection Payload

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Test", "Lint", "Build", "Security", "Helm", "build-and-push"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "required_conversation_resolution": true,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

## Consequences

### Positive

- ✅ **Quality Assurance**: All merges pass comprehensive CI testing
- ✅ **Code Review Culture**: Enforced peer review improves code quality and knowledge sharing
- ✅ **Security**: Vulnerability scanning prevents CVEs from reaching production
- ✅ **Audit Trail**: Complete history of who approved what changes and why
- ✅ **Rollback Safety**: Protected git history enables safe rollbacks
- ✅ **Contributor Confidence**: Contributors know their PRs will be properly reviewed
- ✅ **Production Stability**: Higher bar for release branches reduces regression risk
- ✅ **Automated Enforcement**: GitHub enforces rules consistently, no manual gating

### Negative

- ⚠️ **Slower Merges**: PRs must wait for approvals and CI checks
- ⚠️ **Reviewer Bottleneck**: Requires available code owners for reviews
- ⚠️ **Learning Curve**: New contributors must understand PR workflow
- ⚠️ **Emergency Friction**: Urgent fixes require admin bypass (documented process)

### Mitigation Strategies

| Concern | Mitigation |
|---------|-----------|
| **Slow review turnaround** | Multiple code owners, 24-hour review SLA in CONTRIBUTING.md |
| **Reviewer unavailability** | Cross-train team members, ensure 3+ code owners per area |
| **Emergency hotfixes** | Documented bypass process (see BRANCH_PROTECTION.md) |
| **CI flakiness** | Regularly monitor CI stability, fix flaky tests immediately |
| **Stale PRs** | Automated stale PR detection, regular PR grooming sessions |

## Branch Lifecycle Process

### Adding a New Release Branch

When a new OpenShift version is released:

1. **Create branch from main**:
   ```bash
   git checkout main
   git pull
   git checkout -b release-4.21
   git push origin release-4.21
   ```

2. **Update protection scripts**:
   - Add branch to `scripts/setup-branch-protection.sh`
   - Add branch to `scripts/verify-branch-protection.sh`

3. **Update documentation**:
   - Add branch to `docs/BRANCH_PROTECTION.md`
   - Update this ADR's "Protected Branches Configuration" section

4. **Apply protection**:
   ```bash
   ./scripts/setup-branch-protection.sh
   ./scripts/verify-branch-protection.sh
   ```

### Retiring an EOL Release Branch

When an OpenShift version reaches end of life:

1. **Verify no active work**:
   ```bash
   gh pr list --base release-4.x
   gh issue list --label "release-4.x"
   ```

2. **Check for unique commits**:
   ```bash
   git log --oneline origin/release-4.x --not origin/main
   ```

3. **Delete remote branch**:
   ```bash
   git push origin --delete release-4.x
   ```

4. **Update protection scripts**:
   - Remove branch from setup/verify scripts

5. **Update documentation**:
   - Document deletion in this ADR
   - Update BRANCH_PROTECTION.md

## Success Criteria

### Phase 1 Success (Week 1) - ✅ COMPLETED

- ✅ Branch protection scripts created (`setup-branch-protection.sh`, `verify-branch-protection.sh`)
- ✅ Protection applied to main and 3 release branches
- ✅ Documentation created (`docs/BRANCH_PROTECTION.md`)
- ✅ Verification passing for all protected branches

### Phase 2 Success (Month 1)

- ⏳ 100% of merges go through PR process (no direct commits)
- ⏳ All 6 CI checks passing before merge
- ⏳ Average review turnaround <24 hours
- ⏳ Zero admin bypasses (except documented emergencies)

### Phase 3 Success (Month 3)

- ⏳ PR merge rate >80% (vs. closed without merging)
- ⏳ CI first-pass rate >85% (PRs passing CI on first attempt)
- ⏳ Contributor satisfaction with process (survey)
- ⏳ Zero production incidents from unreviewed code

## Monitoring and Metrics

### Key Performance Indicators

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| **PR Merge Rate** | >80% | PRs merged / PRs opened |
| **Time to Merge** | <48 hours | PR creation to merge time |
| **CI Pass Rate** | >85% | First CI run success rate |
| **Review Turnaround** | <24 hours | PR creation to first review |
| **Admin Bypass Rate** | <1/month | Count of bypasses |
| **Stale PR Count** | <5 | PRs open >14 days |

### Quarterly Review

Every quarter, review:
- Branch protection effectiveness
- CI check coverage
- Approval requirements (1 vs 2)
- Need for new status checks
- Process bottlenecks

## Emergency Bypass Process

### When to Bypass

Admin bypass is allowed **only** for:
- Critical security patch (CVE requires immediate fix)
- Production outage hotfix (P0 incident)
- Broken CI pipeline blocking all PRs

### How to Bypass

1. **Attempt push** - GitHub shows bypass option for admins
2. **Document reason** in commit message
3. **Create tracking issue** explaining bypass
4. **Post-merge review** - Create PR for retroactive review

**Example commit message**:
```
fix: emergency hotfix for CVE-2026-XXXXX

EMERGENCY BYPASS: Critical security vulnerability in Go stdlib.
Normal PR process would delay patch by 24+ hours during outage.

Tracking issue: #456
Post-merge review PR: #457
```

### Post-Bypass Actions

- Within 1 hour: Create tracking issue
- Within 4 hours: Create follow-up PR for code review
- Within 24 hours: Conduct post-mortem and document learnings

## Related ADRs

- [ADR-001: Go Language Selection](001-go-language-selection.md) - Technical choices inform CI requirements
- [ADR-002: Official MCP Go SDK Adoption](002-official-mcp-go-sdk-adoption.md) - SDK compatibility testing
- [ADR-008: Distroless Container Images](008-distroless-container-images.md) - Container build verification
- [ADR-010: Version Compatibility Upgrade Roadmap](010-version-compatibility-upgrade-roadmap.md) - Release branch strategy

## References

- **GitHub Documentation**: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **GitHub Flow**: [Understanding the GitHub flow](https://guides.github.com/introduction/flow/)
- **OpenShift Contribution Guidelines**: [openshift/origin CONTRIBUTING.md](https://github.com/openshift/origin/blob/master/CONTRIBUTING.md)
- **Kubernetes Contribution Guide**: [kubernetes/community contributors](https://github.com/kubernetes/community/tree/master/contributors/guide)
- **CNCF Best Practices**: [CNCF Project Governance](https://github.com/cncf/project-template)
- **Internal Documentation**:
  - [docs/BRANCH_PROTECTION.md](../BRANCH_PROTECTION.md) - Detailed operational guide
  - [.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md) - Contribution workflow
  - [.github/CODEOWNERS](../../.github/CODEOWNERS) - Code ownership mapping

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Reviewer bottleneck** | Medium | Medium | Multiple code owners, 24-hour review SLA |
| **CI pipeline failure** | Low | High | Monitoring, redundant checks, fast fix process |
| **Contributor frustration** | Low | Low | Clear documentation, responsive reviews |
| **Admin bypass abuse** | Very Low | High | Audit log monitoring, post-bypass review |
| **Stale PRs accumulation** | Medium | Low | Automated reminders, weekly grooming |

## Approval

- **Project Lead**: Approved - 2026-01-17
- **Platform Team**: Approved - 2026-01-17
- **Security Team**: Approved - 2026-01-17
- **Date**: 2026-01-17

## Revision History

| Date | Version | Change | Approver |
|------|---------|--------|----------|
| 2026-01-17 | 1.0 | Initial ADR: Branch protection strategy with tiered protection | Platform Team |
