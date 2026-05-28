# Branching Strategy Comparison

Comprehensive comparison of GitHub Flow, Git Flow, and Trunk-based Development.

## Overview Comparison

| Feature | GitHub Flow | Git Flow | Trunk-based Development |
|---------|-------------|----------|------------------------|
| **Complexity** | Simple | Complex | Very Simple |
| **Learning Curve** | Low | High | Low |
| **Branch Count** | 2-5 | 10-20+ | 1-3 |
| **Deploy Frequency** | Multiple/day | Weekly/monthly | Multiple/day |
| **Release Process** | Continuous | Scheduled | Continuous |
| **Team Size** | 2-50 | 10-100+ | 5-100+ |
| **Best For** | Web apps, SaaS | Enterprise, versioned software | High-velocity teams |
| **Merge Strategy** | Squash/merge | Merge commits | Rebase |
| **Production Branches** | 1 (main) | 1 (main) | 1 (main) |
| **Integration Branch** | None (main) | develop | None (main) |
| **Feature Lifetime** | Days-weeks | Weeks-months | Hours-days |
| **Hotfix Process** | Same as features | Special hotfix branch | Same as features |

## GitHub Flow

### Overview

GitHub Flow is a lightweight, branch-based workflow designed for teams and projects with continuous deployment.

### Branch Structure

- **main**: Production-ready code, always deployable
- **feature/***: Short-lived feature branches

### Workflow

```
main ──────●────────●────────●────────●───────>
            \      /          \      /
             \    /            \    /
              feature-1         feature-2
```

**Steps**:
1. Create feature branch from `main`
2. Develop and commit
3. Push and open PR
4. Code review
5. Merge to `main` (triggers deploy)
6. Delete feature branch

### Branch Naming Conventions

```
feature/add-oauth-login
feature/user-dashboard
bugfix/fix-login-redirect
hotfix/patch-security-vulnerability
docs/update-api-documentation
refactor/optimize-database-queries
```

### When to Use

**✅ Good For**:
- Web applications
- SaaS products
- Projects with CI/CD
- Small to medium teams (2-50)
- Continuous deployment
- Simple release process

**❌ Not Good For**:
- Multiple production versions
- Scheduled releases
- Complex release management
- Long-lived features (>2 weeks)

### Advantages

1. **Simple**: Easy to understand and implement
2. **Fast**: Minimal overhead, quick iterations
3. **Always Deployable**: Main branch always production-ready
4. **CI/CD Friendly**: Integrates well with automated deployment
5. **Clear Process**: One workflow for all changes

### Disadvantages

1. **No Release Branches**: Hard to maintain multiple versions
2. **Risky for Complex Projects**: All changes go straight to production
3. **Limited Staging**: No dedicated integration branch
4. **Feature Flags Required**: For incomplete features in production

### Example Workflow

```bash
# Start feature
git checkout main
git pull origin main
git checkout -b feature/add-search

# Develop
git add src/search.ts
git commit -m "feat(search): add search functionality"

# Push and create PR
git push -u origin feature/add-search
gh pr create --title "Add search functionality"

# After approval, merge via GitHub UI
# Automatically deploys to production

# Clean up
git checkout main
git pull origin main
git branch -d feature/add-search
```

### Real-World Examples

**Companies using GitHub Flow**:
- GitHub
- GitLab
- Shopify
- Heroku
- Netlify

## Git Flow

### Overview

Git Flow is a robust branching model designed for projects with scheduled release cycles and multiple production versions.

### Branch Structure

- **main**: Production releases only (tagged)
- **develop**: Integration branch for features
- **feature/***: Feature development
- **release/***: Release preparation
- **hotfix/***: Production hotfixes

### Workflow

```
main ────────●─────────●─────────●───────>
              ↑         ↑         ↑
             / \       / \       / \
develop ────●───●─────●───●─────●───●───>
           / \   \   / \   \
          /   \   \ /   \   \
    feature-1  \  release-1.0  feature-2
                \
              hotfix-1.0.1
```

**Feature Development**:
1. Branch from `develop`
2. Develop feature
3. Merge back to `develop`

**Release**:
1. Branch `release/X.Y.0` from `develop`
2. Bug fixes and version bump
3. Merge to `main` and tag
4. Merge back to `develop`

**Hotfix**:
1. Branch from `main`
2. Fix critical bug
3. Merge to `main` and tag
4. Merge back to `develop`

### Branch Naming Conventions

```
feature/payment-integration
feature/user-authentication
release/1.2.0
release/2.0.0
hotfix/1.1.1
hotfix/critical-security-patch
```

### When to Use

**✅ Good For**:
- Enterprise software
- Desktop applications
- Mobile apps with app store releases
- Projects with scheduled releases
- Multiple production versions
- Large teams (10-100+)
- Complex QA processes

**❌ Not Good For**:
- Continuous deployment
- Small teams
- Simple web applications
- Projects needing rapid iteration

### Advantages

1. **Organized**: Clear structure for all scenarios
2. **Multiple Versions**: Easy to maintain multiple releases
3. **Parallel Development**: Features and releases can happen simultaneously
4. **Explicit Releases**: Clear release process with dedicated branch
5. **Hotfix Support**: Structured process for emergency fixes

### Disadvantages

1. **Complex**: Many branches and merge operations
2. **Overhead**: Significant process overhead
3. **Merge Hell**: Frequent merges between branches
4. **Learning Curve**: Takes time to master
5. **Overkill for Simple Projects**: Too much for small projects

### Example Workflow

#### Feature Development

```bash
# Start feature from develop
git checkout develop
git pull origin develop
git checkout -b feature/payment-integration

# Develop
git add src/payment/
git commit -m "feat(payment): add Stripe integration"

# Finish feature
git checkout develop
git merge --no-ff feature/payment-integration
git push origin develop
git branch -d feature/payment-integration
```

#### Release Process

```bash
# Start release
git checkout develop
git checkout -b release/1.2.0

# Bump version
npm version 1.2.0
git commit -am "chore: bump version to 1.2.0"

# Bug fixes during release preparation
git commit -am "fix(release): resolve last-minute bugs"

# Finish release
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/1.2.0
git push origin develop

# Clean up
git branch -d release/1.2.0
```

#### Hotfix Process

```bash
# Start hotfix from main
git checkout main
git checkout -b hotfix/1.2.1

# Fix bug
git commit -am "fix(auth): patch security vulnerability"

# Bump version
npm version patch
git commit -am "chore: bump version to 1.2.1"

# Finish hotfix
git checkout main
git merge --no-ff hotfix/1.2.1
git tag -a v1.2.1 -m "Hotfix version 1.2.1"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge --no-ff hotfix/1.2.1
git push origin develop

# Clean up
git branch -d hotfix/1.2.1
```

### Real-World Examples

**Companies using Git Flow**:
- Atlassian (Jira, Confluence)
- Microsoft (some products)
- Adobe (some products)
- Large enterprise software companies

## Trunk-based Development

### Overview

Trunk-based Development is a source-control branching model where developers collaborate on code in a single branch (trunk/main) with very short-lived feature branches.

### Branch Structure

- **main**: The trunk, always deployable
- **feature/***: Very short-lived (hours to 1 day max)

### Workflow

```
main ──●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●───>
        \/ \/ \/ \/ \/ \/ \/ \/
         feature branches (hours)
```

**Key Characteristics**:
- Feature branches live < 1 day
- Commit directly to main OR very short branches
- Feature flags for incomplete features
- Continuous integration and deployment
- High test automation requirement

### When to Use

**✅ Good For**:
- High-velocity teams
- Continuous deployment
- Teams with strong CI/CD
- Experienced developers
- Projects with feature flags
- Google-scale development

**❌ Not Good For**:
- Junior teams
- Weak CI/CD infrastructure
- Projects requiring long development cycles
- Open source with external contributors

### Advantages

1. **Maximum Velocity**: Fastest development speed
2. **Simple**: Minimal branching overhead
3. **Always Integrated**: Code always together, no merge hell
4. **Fast Feedback**: Issues found quickly
5. **Deployment Ready**: Always ready to deploy

### Disadvantages

1. **High Discipline Required**: Team must be very disciplined
2. **Strong CI/CD Needed**: Requires mature automation
3. **Feature Flags Essential**: Incomplete features need flags
4. **Risk**: Bad commits can break production quickly
5. **Learning Curve**: Requires mindset shift

### Requirements

**Essential**:
1. **Automated Testing**: Comprehensive test suite (>80% coverage)
2. **CI/CD Pipeline**: Fast, reliable automation
3. **Feature Flags**: System to toggle incomplete features
4. **Code Review**: Fast review process (< 2 hours)
5. **Monitoring**: Strong observability and rollback capability

### Example Workflow

#### Small Change (Direct to Main)

```bash
# Pull latest
git checkout main
git pull origin main

# Make small change
git add src/utils/helper.ts
git commit -m "refactor(utils): extract date formatting helper"

# Push directly to main
git push origin main
```

#### Short-lived Feature Branch

```bash
# Create short-lived branch
git checkout main
git pull origin main
git checkout -b feature/add-button

# Develop (< 1 day)
git add src/components/Button.tsx
git commit -m "feat(ui): add primary button component"

# Push and merge quickly
git push -u origin feature/add-button
gh pr create --title "Add button component"

# After quick review (< 2 hours), merge and deploy
# Delete branch immediately

# Back to main
git checkout main
git pull origin main
git branch -d feature/add-button
```

#### Using Feature Flags

```bash
# Add incomplete feature with flag
git add src/features/new-dashboard.tsx
git commit -m "feat(dashboard): add new dashboard (behind feature flag)

Feature is behind ENABLE_NEW_DASHBOARD flag.
Will be enabled after user testing."

git push origin main
# Deploys to production, but feature is hidden
```

### Feature Flag Example

```typescript
// Feature flag check
if (featureFlags.isEnabled('NEW_DASHBOARD')) {
  return <NewDashboard />;
}
return <OldDashboard />;
```

```bash
# Enable for testing
curl -X POST /api/feature-flags \
  -d '{"flag": "NEW_DASHBOARD", "enabled": true, "users": ["test@example.com"]}'

# Enable for everyone after testing
curl -X POST /api/feature-flags \
  -d '{"flag": "NEW_DASHBOARD", "enabled": true, "users": "*"}'

# Remove old code after successful rollout
git rm src/components/OldDashboard.tsx
git commit -m "chore(dashboard): remove old dashboard code"
```

### Real-World Examples

**Companies using Trunk-based Development**:
- Google (monorepo)
- Facebook/Meta
- Netflix
- Amazon
- Etsy

## Decision Matrix

### Choose GitHub Flow When:

- ✅ Deploying continuously to production
- ✅ Working on web applications or SaaS
- ✅ Team size: 2-50 developers
- ✅ Simple release process
- ✅ One production environment
- ✅ Features can be deployed independently

### Choose Git Flow When:

- ✅ Scheduled release cycles (weekly, monthly)
- ✅ Multiple production versions to maintain
- ✅ Complex QA and release process
- ✅ Desktop or mobile applications
- ✅ Large teams (10-100+)
- ✅ Regulatory compliance requirements

### Choose Trunk-based Development When:

- ✅ Deploying multiple times per day
- ✅ Strong CI/CD infrastructure in place
- ✅ Experienced development team
- ✅ Feature flag system available
- ✅ High test coverage (>80%)
- ✅ Fast code review process (< 2 hours)

## Migration Paths

### From Git Flow to GitHub Flow

1. Stop creating `develop` branch
2. Create features from `main`
3. Merge features directly to `main`
4. Deploy `main` continuously
5. Use hotfix branches only if needed

### From GitHub Flow to Trunk-based Development

1. Reduce feature branch lifetime (< 1 day)
2. Implement feature flag system
3. Increase test coverage
4. Speed up CI/CD pipeline
5. Train team on discipline required
6. Consider direct commits for small changes

### From Git Flow to Trunk-based Development

This is a major change requiring:
1. Strong CI/CD implementation
2. Feature flag system
3. High test coverage
4. Team training
5. Gradual transition over months

## Summary Table

| Aspect | GitHub Flow | Git Flow | Trunk-based |
|--------|-------------|----------|-------------|
| **Deploy Frequency** | Daily | Weekly/Monthly | Multiple/day |
| **Branch Lifetime** | Days-weeks | Weeks-months | Hours-days |
| **Complexity** | ⭐ Low | ⭐⭐⭐ High | ⭐⭐ Medium |
| **Setup Time** | Minutes | Hours | Hours (tooling) |
| **Learning Curve** | Days | Weeks | Days |
| **Team Discipline** | Medium | Low | High |
| **CI/CD Requirement** | Medium | Low | High |
| **Test Coverage Need** | Medium | Low | High |
| **Feature Flags** | Optional | Not needed | Essential |
| **Suitable Team Size** | 2-50 | 10-100+ | 5-100+ |
| **Best For** | Web apps | Enterprise | High-velocity |

## Recommendations

**Startups and Small Teams**: Start with **GitHub Flow**
- Simple, fast, easy to learn
- Grow into trunk-based as team matures

**Enterprise and Complex Projects**: Use **Git Flow**
- Structured, supports multiple versions
- Good for scheduled releases

**High-Performance Teams**: Adopt **Trunk-based Development**
- Maximum velocity
- Requires investment in tooling and process

**Hybrid Approach**: Many teams use combinations
- GitHub Flow for main product
- Git Flow for enterprise version
- Trunk-based for internal tools

The best strategy depends on your team, project, and constraints. Start simple and evolve as needs change.
