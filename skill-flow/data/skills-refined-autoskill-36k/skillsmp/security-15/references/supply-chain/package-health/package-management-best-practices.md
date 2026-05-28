<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Package Management Best Practices

Comprehensive guide to dependency management, version control, and operational health for software packages.

## Version Pinning

### Why Pin Versions?

**Benefits**:
- **Reproducible builds**: Same dependencies every time
- **Predictable behavior**: No surprise updates
- **Security control**: Explicit security updates
- **Deployment safety**: Tested combinations only

**Risks of Not Pinning**:
- Breaking changes in minor/patch updates
- Inconsistent behavior across environments
- Supply chain attacks via version ranges
- Hidden dependency updates

### Pinning Strategies

#### Exact Pinning (Strictest)
```json
{
  "dependencies": {
    "express": "4.18.2",
    "lodash": "4.17.21"
  }
}
```

**Pros**: Complete control, maximum predictability
**Cons**: Manual updates required, security patches delayed

#### Lock Files (Recommended)
```bash
# npm
npm install  # Creates package-lock.json

# Yarn
yarn install  # Creates yarn.lock

# pnpm
pnpm install  # Creates pnpm-lock.yaml
```

**Pros**: Balance of flexibility and control
**Cons**: Lock file drift, merge conflicts

#### Semantic Version Ranges (Flexible)
```json
{
  "dependencies": {
    "express": "^4.18.0",  // >=4.18.0 <5.0.0
    "lodash": "~4.17.0"    // >=4.17.0 <4.18.0
  }
}
```

**Pros**: Automatic patch updates
**Cons**: Unpredictable builds, potential breaks

### Version Range Operators

| Operator | Meaning | Example | Matches |
|----------|---------|---------|---------|
| (none) | Exact | `1.2.3` | 1.2.3 only |
| `^` | Compatible | `^1.2.3` | 1.2.3 - 1.x.x |
| `~` | Approximate | `~1.2.3` | 1.2.3 - 1.2.x |
| `>` | Greater than | `>1.2.3` | 1.2.4+ |
| `>=` | Greater or equal | `>=1.2.3` | 1.2.3+ |
| `<` | Less than | `<1.2.3` | <1.2.3 |
| `<=` | Less or equal | `<=1.2.3` | ≤1.2.3 |
| `*` | Any version | `*` | Any |
| `x` | Wildcard | `1.2.x` | 1.2.0 - 1.2.x |

### Best Practice Recommendations

**Production Applications**:
```json
{
  "dependencies": {
    "express": "4.18.2"  // Exact versions
  },
  "devDependencies": {
    "jest": "^29.0.0"    // Ranges OK for dev tools
  }
}
```

**Libraries/Frameworks**:
```json
{
  "peerDependencies": {
    "react": "^18.0.0"  // Flexible for consumers
  },
  "dependencies": {
    "prop-types": "15.8.1"  // Exact for internals
  }
}
```

## Lock File Management

### Lock File Purpose

Lock files record the **exact** versions of all dependencies (including transitives) that were installed.

**Benefits**:
- Reproducible installs across machines
- Prevents "works on my machine" issues
- Historical record of dependencies
- Faster installs (resolved already)

### Lock File Best Practices

#### Always Commit Lock Files
```bash
# .gitignore - DO NOT ignore lock files
# package-lock.json  ❌
# yarn.lock          ❌
# pnpm-lock.yaml     ❌
```

#### Keep Lock Files Fresh
```bash
# Update dependencies
npm update

# Regenerate lock file
rm package-lock.json
npm install

# Audit and fix
npm audit fix
```

#### Handle Lock File Conflicts
```bash
# Accept theirs (merge)
git checkout --theirs package-lock.json
npm install

# Accept ours (current branch)
git checkout --ours package-lock.json
npm install

# Manual resolution required for package.json conflicts
```

### Lock File Auditing

```bash
# Check for vulnerabilities
npm audit

# Fix automatically (non-breaking)
npm audit fix

# Fix with breaking changes
npm audit fix --force

# View audit as JSON
npm audit --json
```

## Dependency Updates

### Update Strategies

#### 1. Scheduled Updates (Recommended)
- Weekly/biweekly update cycles
- Review changes before merging
- Test thoroughly
- Batch non-critical updates

#### 2. Immediate Security Updates
- Security patches applied ASAP
- Emergency deployment process
- Minimal testing for critical fixes
- Rollback plan ready

#### 3. Major Version Updates
- Quarterly or as needed
- Dedicated update sprints
- Breaking change analysis
- Incremental migration

### Update Tools

#### Dependabot (GitHub)
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "automerge"
```

#### Renovate
```json
{
  "extends": ["config:base"],
  "schedule": ["before 5am on monday"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "pin"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["breaking-change"]
    }
  ]
}
```

### Update Workflow

```bash
# 1. Check for outdated packages
npm outdated

# 2. Review what would change
npm update --dry-run

# 3. Update patch versions only
npm update

# 4. Update specific package
npm update express

# 5. Update to latest (including breaking)
npm install express@latest

# 6. Test
npm test

# 7. Commit
git add package.json package-lock.json
git commit -m "chore: update dependencies"
```

## Library Standardization

### Why Standardize?

**Problems with Multiple Versions**:
- Increased bundle size
- Potential conflicts
- Security patch complexity
- Maintenance overhead

**Example Issue**:
```json
{
  "dependencies": {
    "lodash": "4.17.21",
    "some-lib": "*"  // Depends on lodash@4.17.20
  }
}
```
Result: Two lodash versions in node_modules

### Standardization Strategies

#### 1. Dedupe Dependencies
```bash
# npm 7+
npm dedupe

# Yarn
yarn dedupe

# pnpm (automatic)
pnpm install
```

#### 2. Override Transitive Versions
```json
{
  "overrides": {
    "lodash": "4.17.21"
  }
}
```

#### 3. Peer Dependencies
```json
{
  "peerDependencies": {
    "react": "^18.0.0"
  }
}
```
Forces consumers to provide the version.

### Duplicate Detection

```bash
# Find duplicate packages
npm ls lodash

# Example output:
# ├─┬ express@4.18.2
# │ └── lodash@4.17.20
# └── lodash@4.17.21

# Fix with dedupe
npm dedupe
npm ls lodash
# └── lodash@4.17.21 (deduped)
```

### Consolidation Process

1. **Identify Duplicates**
   ```bash
   npm ls --depth=0 | grep lodash
   ```

2. **Analyze Impact**
   - Which versions are needed?
   - Breaking changes between versions?
   - Can all dependents use same version?

3. **Update and Test**
   ```bash
   npm install lodash@latest
   npm dedupe
   npm test
   ```

4. **Use Resolutions** (if needed)
   ```json
   {
     "resolutions": {
       "**/lodash": "4.17.21"
     }
   }
   ```

## Deprecation Handling

### Identifying Deprecated Packages

#### npm Warnings
```bash
npm install
# npm WARN deprecated request@2.88.2: request has been deprecated
```

#### Programmatic Check
```bash
npm view request

# Output includes:
# deprecated = 'request has been deprecated, see https://...'
```

#### deps.dev API
```bash
curl https://api.deps.dev/v3alpha/systems/npm/packages/request | \
  jq '.versions[] | select(.isDefault==true) | .deprecationReason'
```

### Deprecation Response Workflow

1. **Assess Impact**
   - Where is package used?
   - Is there a successor?
   - What's the migration path?

2. **Find Replacement**
   ```bash
   # Example: request → axios
   npm uninstall request
   npm install axios
   ```

3. **Update Code**
   ```javascript
   // Before
   const request = require('request');
   request.get('https://api.example.com', callback);

   // After
   const axios = require('axios');
   const response = await axios.get('https://api.example.com');
   ```

4. **Test Thoroughly**
   - Unit tests
   - Integration tests
   - Manual testing

5. **Document Migration**
   - Update README
   - Document breaking changes
   - Update team knowledge base

### Common Deprecated Packages

| Deprecated | Replacement | Notes |
|------------|-------------|-------|
| `request` | `axios`, `node-fetch` | Different API |
| `node-uuid` | `uuid` | Renamed |
| `bson` (old) | `bson` (new) | Version update |
| `colors` | `chalk`, `ansi-colors` | Security issues |
| `moment` | `date-fns`, `dayjs` | Large size |

## Health Score Calculation

### Custom Health Score Algorithm

```javascript
function calculateHealthScore(package) {
  // Weights
  const weights = {
    openssf: 0.30,      // OpenSSF Scorecard
    maintenance: 0.25,   // Maintenance activity
    security: 0.25,      // Security posture
    freshness: 0.10,     // Version currency
    popularity: 0.10     // Community adoption
  };

  // Calculate sub-scores (0-100)
  const scores = {
    openssf: getOpenssfScore(package) * 10,  // 0-10 → 0-100
    maintenance: getMaintenanceScore(package),
    security: getSecurityScore(package),
    freshness: getFreshnessScore(package),
    popularity: getPopularityScore(package)
  };

  // Weighted sum
  return Object.keys(weights).reduce((total, key) => {
    return total + (scores[key] * weights[key]);
  }, 0);
}
```

### Maintenance Score (0-100)

```javascript
function getMaintenanceScore(package) {
  const factors = {
    recentCommits: getCommitActivity(90),        // 0-30 points
    releaseFrequency: getReleaseFrequency(),     // 0-25 points
    issueResponseTime: getIssueResponseTime(),   // 0-20 points
    activeContributors: getContributorCount(),   // 0-15 points
    documentation: hasGoodDocs()                 // 0-10 points
  };

  return Object.values(factors).reduce((a, b) => a + b, 0);
}
```

**Criteria**:
- **Recent Commits** (30 points)
  - 30: Daily commits
  - 20: Weekly commits
  - 10: Monthly commits
  - 0: No commits in 90 days

- **Release Frequency** (25 points)
  - 25: Monthly releases
  - 15: Quarterly releases
  - 5: Yearly releases
  - 0: No releases in 2+ years

- **Issue Response** (20 points)
  - 20: <24 hours average
  - 15: <1 week average
  - 10: <1 month average
  - 0: Issues ignored

- **Contributors** (15 points)
  - 15: 10+ active contributors
  - 10: 5-9 contributors
  - 5: 2-4 contributors
  - 0: 1 contributor

- **Documentation** (10 points)
  - 10: Comprehensive docs
  - 5: Basic README
  - 0: No documentation

### Security Score (0-100)

```javascript
function getSecurityScore(package) {
  let score = 100;

  // Deduct for issues
  const critical = getCriticalVulns();
  const high = getHighVulns();
  const medium = getMediumVulns();

  score -= critical * 25;  // -25 per critical
  score -= high * 10;      // -10 per high
  score -= medium * 5;     // -5 per medium

  // Bonus for good practices
  if (hasSecurityPolicy()) score += 10;
  if (hasSignedReleases()) score += 10;
  if (hasBugBounty()) score += 5;

  return Math.max(0, Math.min(100, score));
}
```

### Freshness Score (0-100)

```javascript
function getFreshnessScore(package) {
  const latestVersion = getLatestVersion();
  const currentVersion = getCurrentVersion();
  const monthsBehind = getMonthsBehind(currentVersion, latestVersion);

  if (monthsBehind === 0) return 100;
  if (monthsBehind <= 3) return 80;
  if (monthsBehind <= 6) return 60;
  if (monthsBehind <= 12) return 40;
  if (monthsBehind <= 24) return 20;
  return 0;
}
```

## Security Update Policies

### Policy Framework

```yaml
# security-update-policy.yml
policies:
  critical:
    response_time: 24h
    auto_merge: false
    required_approvals: 2
    testing_required: minimal

  high:
    response_time: 7d
    auto_merge: false
    required_approvals: 1
    testing_required: standard

  medium:
    response_time: 30d
    auto_merge: true
    required_approvals: 0
    testing_required: standard

  low:
    response_time: 90d
    auto_merge: true
    required_approvals: 0
    testing_required: none
```

### Update Automation

```yaml
# .github/workflows/security-updates.yml
name: Security Updates
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check for security updates
        run: npm audit --audit-level=moderate

      - name: Apply security patches
        run: npm audit fix

      - name: Run tests
        run: npm test

      - name: Create PR
        if: success()
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'Security: Apply dependency patches'
          branch: security/dependency-updates
          labels: security,dependencies
```

## Tooling Recommendations

### Package Managers

**npm** (Default)
- Ubiquitous, well-supported
- Built into Node.js
- Good performance (v7+)

**Yarn** (Alternative)
- Faster installs
- Better workspace support
- Offline mode

**pnpm** (Recommended)
- Fastest installs
- Disk space efficient
- Strict dependency resolution

### Analysis Tools

**npm-check-updates**
```bash
npm install -g npm-check-updates

# Check for updates
ncu

# Update package.json
ncu -u
```

**depcheck**
```bash
npm install -g depcheck

# Find unused dependencies
depcheck
```

**license-checker**
```bash
npm install -g license-checker

# Audit licenses
license-checker --summary
```

## Best Practices Summary

### DO ✓
- ✓ Commit lock files
- ✓ Pin production dependencies
- ✓ Regular security audits
- ✓ Scheduled dependency updates
- ✓ Remove unused dependencies
- ✓ Dedupe when possible
- ✓ Document major updates
- ✓ Test before merging updates

### DON'T ✗
- ✗ Ignore lock files
- ✗ Use wildcards in production
- ✗ Skip security updates
- ✗ Update all dependencies at once
- ✗ Mix package managers
- ✗ Commit node_modules
- ✗ Use deprecated packages
- ✗ Ignore audit warnings

## References

- npm Documentation: https://docs.npmjs.com/
- Semantic Versioning: https://semver.org/
- OpenSSF Best Practices: https://bestpractices.coreinfrastructure.org/
- OWASP Dependency Check: https://owasp.org/www-project-dependency-check/
- Snyk Advisories: https://snyk.io/vuln/
