# Update Strategies

Safe approaches for updating dependencies.

## Semantic Versioning Understanding

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, no API changes
  │     └──────── New features, backwards compatible
  └────────────── Breaking changes
```

## Patch Updates (0.0.x)

### Risk Level: Low

Patch updates fix bugs without changing the API.

```bash
# Safe to update all patches at once
npm update  # Updates within semver range

# Or specifically
npm install package@~1.2.0  # 1.2.x only
```

### When to Be Careful

- Security patches may change behavior
- Some projects don't follow semver strictly
- Check if tests still pass

## Minor Updates (0.x.0)

### Risk Level: Medium

Minor updates add features but should be backwards compatible.

```markdown
## Minor Update Checklist

- [ ] Read changelog/release notes
- [ ] Check for deprecation warnings
- [ ] Run full test suite
- [ ] Test affected features manually
- [ ] Review bundle size impact
```

### Best Practices

```bash
# Update one at a time for important packages
npm install package@^1.3.0

# Run tests after each
npm test

# Commit individually for easy rollback
git commit -m "Update package 1.2.0 → 1.3.0"
```

## Major Updates (x.0.0)

### Risk Level: High

Major updates may include breaking changes.

### Planning Process

```markdown
## Major Update: [Package] v1 → v2

### 1. Research Phase
- [ ] Read migration guide
- [ ] Review breaking changes
- [ ] Check community feedback
- [ ] Identify affected code

### 2. Preparation Phase
- [ ] Create feature branch
- [ ] Update package
- [ ] Fix immediate breaks
- [ ] Update related packages

### 3. Migration Phase
- [ ] Address deprecation warnings
- [ ] Update usage patterns
- [ ] Update types (if TypeScript)
- [ ] Update tests

### 4. Verification Phase
- [ ] Run full test suite
- [ ] Build production bundle
- [ ] Test critical user flows
- [ ] Performance comparison

### 5. Rollout Phase
- [ ] Deploy to staging
- [ ] QA verification
- [ ] Monitor for issues
- [ ] Deploy to production
```

### Example: Express 4 → 5 Migration

```markdown
## Express 5 Migration

### Breaking Changes
1. Promise-based route handlers
2. Removed deprecated methods
3. Query parser changes

### Code Changes Required

**Before (Express 4):**
```javascript
app.get('/users', function(req, res, next) {
  User.find()
    .then(users => res.json(users))
    .catch(next);
});
```

**After (Express 5):**
```javascript
app.get('/users', async (req, res) => {
  const users = await User.find();
  res.json(users);
});
```

### Migration Steps
1. Update express: `npm install express@5`
2. Convert callbacks to async/await
3. Update error handlers
4. Remove deprecated middleware
5. Update tests
```

## Batch Update Strategies

### Conservative Approach

Update packages in groups by risk:

```bash
# Week 1: Patch updates
npm update

# Week 2: Low-risk minor updates
npm install dev-deps@minor

# Week 3: Higher-risk minor updates
npm install core-deps@minor

# Week 4: Address any issues
```

### Dependency Groups

```markdown
## Update Groups

### Group 1: Dev Tools (Low Risk)
- prettier, eslint, jest
- Usually safe to batch

### Group 2: Build Tools (Medium Risk)
- webpack, babel, typescript
- Update together, test build

### Group 3: Framework Core (High Risk)
- react, vue, express
- Update individually with full testing

### Group 4: Database/ORM (High Risk)
- prisma, typeorm, mongoose
- Update with migration testing
```

## Automated Updates

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev-dependencies:
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier"
          - "jest"
      production:
        patterns:
          - "*"
        exclude-patterns:
          - "@types/*"
          - "eslint*"
```

### Renovate Configuration

```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

## Rollback Procedures

### Quick Rollback

```bash
# If tests fail after update
git checkout package-lock.json
npm install

# Or revert to specific version
npm install package@previous-version
```

### Full Rollback

```bash
# Revert entire update commit
git revert <commit-hash>
npm install

# Or restore from backup
git checkout HEAD~1 -- package.json package-lock.json
npm install
```

## Update Documentation

### Change Log Entry

```markdown
## Dependencies Updated (2024-01-15)

### Security
- lodash 4.17.15 → 4.17.21 (CVE-2021-23337)

### Minor Updates
- jest 29.5.0 → 29.7.0
- typescript 5.0.4 → 5.3.0

### Major Updates
- react 17.0.2 → 18.2.0
  - Migration: [Link to migration PR]
  - Breaking changes handled: [List]
```
