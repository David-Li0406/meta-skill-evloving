# Examples: GitHub PR Flow

The following examples illustrate common PR workflows.

## Example 1: Standard Feature PR

```javascript
// 1. Create feature branch from main
create_branch({
  owner: "org",
  repo: "repo",
  branch: "feat/user-dashboard",
  from_branch: "main",
});

// 2. (Make file changes using github-kernel tools)

// 3. Create draft PR for early feedback
create_pull_request({
  owner: "org",
  repo: "repo",
  title: "feat: add user dashboard feature",
  body: `## Description
Implements user dashboard with activity feed and statistics.

## Changes
- Added dashboard component
- Integrated activity feed API
- Created user statistics display

## Testing
- Unit tests added for all components
- Integration tests verified

## Impact
- No breaking changes
- Requires dashboard API endpoint`,
  head: "feat/user-dashboard",
  base: "main",
  draft: true,
});

// 4. Mark as ready when complete
update_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 45,
  draft: false,
});

// 5. Sync with latest main before merge
update_pull_request_branch({
  owner: "org",
  repo: "repo",
  pullNumber: 45,
});

// 6. Merge using squash strategy
merge_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 45,
  merge_method: "squash",
});
```

## Example 2: Hotfix with Dual PRs (Production)

```javascript
// 1. Create hotfix branch from release
create_branch({
  owner: "org",
  repo: "repo",
  branch: "hotfix/security-patch",
  from_branch: "release/v2.1",
});

// 2. (Apply security fixes using github-kernel)

// 3. Create PR targeting release branch
create_pull_request({
  owner: "org",
  repo: "repo",
  title: "fix: critical security patch for CVE-2026-1234",
  body: `## 🚨 URGENT SECURITY HOTFIX

### Vulnerability
Fixes **CVE-2026-1234** - Critical XSS vulnerability

### Changes Applied
- ✅ Input sanitization implemented
- ✅ CSP headers added
- ✅ Output escaping enhanced

### Security Impact
- **Severity**: CRITICAL
- **Attack Vector**: XSS injection
- **Mitigation**: Complete input validation

⚠️ **NEEDS IMMEDIATE REVIEW AND DEPLOYMENT**`,
  head: "hotfix/security-patch",
  base: "release/v2.1",
  draft: false,
});

// 4. Create companion PR targeting main
create_pull_request({
  owner: "org",
  repo: "repo",
  title: "fix: critical security patch for CVE-2026-1234 (backport to main)",
  body: `## 🚨 SECURITY HOTFIX (Backport to Main)

### Vulnerability
Fixes **CVE-2026-1234** - Critical XSS vulnerability

**Related PR**: This backports the hotfix from release/v2.1 to main.`,
  head: "hotfix/security-patch",
  base: "main",
  draft: false,
});
```

## Example 3: Updating PR After Creation

```javascript
// Fix PR title to follow conventions
update_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 44,
  title: "feat: implement OAuth2 authentication",
  body: `## Description
Replaces basic authentication with OAuth2 flow.

## Changes
- OAuth2 protocol integration
- Token handling and refresh
- Authorization code flow with PKCE

## Testing
- All authentication flows tested
- Security scans passed`,
});
```

## Example 4: Handling Already-Synced Branch

```javascript
// Attempt to sync branch
update_pull_request_branch({
  owner: "org",
  repo: "repo",
  pullNumber: 45,
});

// Response: 422 "no new commits on base branch"
// ✅ This is OK - branch is already up-to-date
// Proceed with review/merge
```

## Example 5: Multi-Step Update Workflow

```javascript
// 1. Update PR metadata
update_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 50,
  title: "feat: add payment processing",
  reviewers: ["tech-lead", "security-team"],
});

// 2. Sync with base branch
update_pull_request_branch({
  owner: "org",
  repo: "repo",
  pullNumber: 50,
});

// 3. After approvals, merge
merge_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 50,
  merge_method: "squash",
  commit_title: "feat: add payment processing",
  commit_message: "Implements Stripe integration with webhook support",
});
```

## Example 6: Draft to Ready Workflow

```javascript
// Create as draft for WIP
create_pull_request({
  owner: "org",
  repo: "repo",
  title: "feat: analytics dashboard",
  body: "WIP: Building analytics dashboard",
  head: "feat/analytics",
  base: "main",
  draft: true,
});

// Mark ready after implementation complete
update_pull_request({
  owner: "org",
  repo: "repo",
  pullNumber: 52,
  draft: false,
  body: `## Description
Complete analytics dashboard with real-time metrics.

## Changes
- Dashboard UI implemented
- Real-time data streaming
- Metric visualization charts

## Testing
- E2E tests added
- Performance benchmarked`,
});
```

## Best Practices Summary

1. **Always use conventional commit format** in PR titles
2. **Structure PR descriptions** with clear sections
3. **Sync branches** before review and before merge
4. **Use draft PRs** for work-in-progress
5. **Include CVE/security info** for security fixes
6. **Choose merge strategy** based on commit history needs
7. **Handle 422 errors gracefully** (already up-to-date is success)
8. **Create dual PRs** for hotfixes affecting multiple branches
