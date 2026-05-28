# CI/CD Patterns and Best Practices

## Overview
This document describes common CI/CD pipeline patterns, best practices, and anti-patterns to avoid. Use these patterns when setting up or improving continuous integration and deployment workflows.

## Pipeline Architecture Patterns

### 1. Multi-Stage Pipeline

**Pattern:**
```yaml
Stages:
  1. Code Quality → 2. Test → 3. Security → 4. Build → 5. Deploy

Characteristics:
  - Sequential stages with gates
  - Fail fast at each stage
  - Only successful builds proceed
  - Each stage is independent
```

**When to use:**
- Standard application deployments
- Need quality gates before deployment
- Want clear separation of concerns

**Implementation:**
```yaml
# GitHub Actions example structure
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [checkout, setup, lint]

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps: [checkout, setup, test]

  security:
    needs: test
    runs-on: ubuntu-latest
    steps: [checkout, security-scan]

  build:
    needs: security
    runs-on: ubuntu-latest
    steps: [checkout, build, push-image]

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps: [checkout, deploy-to-staging]
```

### 2. Parallel Execution Pipeline

**Pattern:**
```yaml
Stages run in parallel:
  ├─ Unit Tests
  ├─ Integration Tests
  ├─ Linting
  ├─ Security Scanning
  └─ Code Coverage

Then sequential:
  → Build → Deploy
```

**When to use:**
- Fast feedback is critical
- Independent test suites
- Reduce total pipeline time

**Benefits:**
- Faster feedback (parallel execution)
- Better resource utilization
- Identifies multiple issues simultaneously

### 3. Matrix Build Pipeline

**Pattern:**
```yaml
Test across multiple configurations:
  - Node.js versions: [14, 16, 18, 20]
  - OS: [ubuntu, macos, windows]
  - Database: [postgres, mysql]

Total combinations: 4 × 3 × 2 = 24 builds
```

**When to use:**
- Supporting multiple versions
- Multi-platform applications
- Testing compatibility

**Implementation:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [14, 16, 18, 20]
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

### 4. Trunk-Based Development Pipeline

**Pattern:**
```yaml
Main branch (trunk):
  - All commits trigger CI
  - Short-lived feature branches
  - Continuous integration to main
  - Feature flags for incomplete features
  - Deploy from main frequently

Flow:
  Feature branch → PR → CI → Merge to main → Deploy
```

**When to use:**
- High-velocity teams
- Continuous deployment culture
- Need for rapid iteration

**Best practices:**
- Keep branches short-lived (< 2 days)
- Use feature flags for incomplete work
- Maintain main branch always deployable
- Deploy to production frequently (multiple times/day)

### 5. GitFlow Pipeline

**Pattern:**
```yaml
Branches:
  - main: Production-ready code
  - develop: Integration branch
  - feature/*: Feature development
  - release/*: Release preparation
  - hotfix/*: Production fixes

CI triggers:
  - feature/* → Run tests only
  - develop → Deploy to dev environment
  - release/* → Deploy to staging
  - main → Deploy to production
```

**When to use:**
- Scheduled releases
- Multiple environments
- Need for release branches
- Regulated industries

## Branch Strategy Patterns

### 1. Main-Only Strategy

**Pattern:**
```yaml
- Single main branch
- All commits to main
- CI/CD on every commit
- Feature flags for toggles
```

**Pros:**
- Simplest workflow
- Continuous integration
- Fast feedback

**Cons:**
- Requires discipline
- Need feature flags
- All code must be production-ready

### 2. Feature Branch Strategy

**Pattern:**
```yaml
- main branch (production)
- feature/* branches
- Pull request workflow
- CI on PR
- Merge to main deploys
```

**Pros:**
- Code review before merge
- Isolated feature development
- Clear history

**Cons:**
- Can lead to long-lived branches
- Integration issues if branches diverge

### 3. Environment Branch Strategy

**Pattern:**
```yaml
Branches:
  - develop → Dev environment
  - staging → Staging environment
  - main → Production environment

Promotion:
  develop → staging → main
```

**Pros:**
- Clear environment mapping
- Promotion workflow
- Easy to understand

**Cons:**
- Can lead to merge conflicts
- Manual promotion steps
- Drift between environments

## Testing Patterns

### 1. Test Pyramid

**Pattern:**
```yaml
         ┌───────────┐
         │    E2E    │  ← Few, slow, expensive
         ├───────────┤
         │Integration│  ← Some, medium speed
         ├───────────┤
         │   Unit    │  ← Many, fast, cheap
         └───────────┘

Ratio: 70% Unit, 20% Integration, 10% E2E
```

**Implementation in CI:**
```yaml
Unit Tests:
  - Run on every commit
  - Fast execution (< 5 min)
  - High coverage (> 80%)
  - No external dependencies

Integration Tests:
  - Run on PR and main
  - Medium execution (5-15 min)
  - Test component interactions
  - Use test databases

E2E Tests:
  - Run on release candidates
  - Slow execution (15-60 min)
  - Test critical user flows
  - Run against staging environment
```

### 2. Parallel Test Execution

**Pattern:**
```yaml
Split tests into parallel jobs:
  - Job 1: Unit tests group 1
  - Job 2: Unit tests group 2
  - Job 3: Integration tests
  - Job 4: E2E tests

Total time: max(job times) instead of sum(job times)
```

**Implementation:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        test-group: [unit-1, unit-2, integration, e2e]
    steps:
      - run: npm test -- --group=${{ matrix.test-group }}
```

### 3. Test Result Caching

**Pattern:**
```yaml
Cache test results:
  - Hash of source files
  - Only re-run affected tests
  - Skip unchanged test suites
```

**Benefits:**
- Faster CI execution
- Reduced resource usage
- Quick feedback for small changes

## Build Optimization Patterns

### 1. Dependency Caching

**Pattern:**
```yaml
Cache dependencies between builds:
  - Node.js: node_modules/
  - Python: .venv/, pip cache
  - Java: .m2/
  - Docker: layer cache

Cache key: hash of dependency files
  - package-lock.json
  - requirements.txt
  - pom.xml
```

**Implementation:**
```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 2. Incremental Builds

**Pattern:**
```yaml
Only rebuild changed components:
  - Detect changed files
  - Identify affected modules
  - Build only necessary components
  - Use build cache for unchanged
```

**Tools:**
- Nx (monorepo builds)
- Bazel (Google's build system)
- Turborepo (incremental builds)

### 3. Multi-Stage Docker Builds

**Pattern:**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/main.js"]
```

**Benefits:**
- Smaller final image
- Faster builds (layer caching)
- Separate build and runtime dependencies

## Deployment Patterns

### 1. Continuous Deployment

**Pattern:**
```yaml
Every commit to main:
  1. Run CI pipeline
  2. If all checks pass
  3. Automatically deploy to production
  4. Monitor for issues
  5. Auto-rollback on failure
```

**Requirements:**
- Comprehensive test coverage
- Robust monitoring
- Automated rollback
- High team maturity

### 2. Continuous Delivery

**Pattern:**
```yaml
Every commit to main:
  1. Run CI pipeline
  2. If all checks pass
  3. Deploy to staging automatically
  4. Run acceptance tests
  5. Await manual approval
  6. Deploy to production on approval
```

**When to use:**
- Need human validation
- Regulated industries
- Scheduled releases
- Risk-averse organizations

### 3. Environment Promotion Pipeline

**Pattern:**
```yaml
Environments: Dev → QA → Staging → Production

Promotion:
  - Auto-deploy to Dev on commit
  - Auto-promote to QA if tests pass
  - Manual promotion to Staging
  - Manual promotion to Production

Gates:
  - Dev: Basic tests pass
  - QA: Full test suite passes
  - Staging: Acceptance tests pass
  - Production: Manual approval
```

## Security Patterns

### 1. Security Scanning Pipeline

**Pattern:**
```yaml
Security gates:
  1. Dependency scanning (npm audit, Snyk)
  2. SAST - Static Application Security Testing
  3. Container scanning (Trivy, Clair)
  4. Secret scanning (prevent committed secrets)
  5. License compliance checking

Failure policy:
  - Critical: Block deployment
  - High: Block deployment
  - Medium: Create issue, allow with approval
  - Low: Create issue, allow deployment
```

### 2. Secrets Management

**Pattern:**
```yaml
Never commit secrets:
  - Use environment variables
  - Use secret management services
  - Rotate secrets regularly
  - Scan for leaked secrets

Secret storage:
  - GitHub Secrets
  - AWS Secrets Manager
  - HashiCorp Vault
  - Cloud provider secret stores
```

### 3. Least Privilege Access

**Pattern:**
```yaml
CI/CD permissions:
  - Read access: Public repos
  - Write access: Only to artifact storage
  - Deploy access: Only to target environments
  - Admin access: None (use service accounts)

Principle: Give CI/CD only permissions needed
```

## Monitoring Patterns

### 1. Pipeline Metrics

**Track and alert on:**
```yaml
Metrics:
  - Build success rate (target > 95%)
  - Build duration (track trends)
  - Test success rate
  - Deployment frequency
  - Lead time (commit to production)
  - Mean time to recovery (MTTR)

Alerts:
  - Build failure rate > 10%
  - Build time increases > 50%
  - Deployment failures
  - Security scan failures
```

### 2. Deployment Tracking

**Pattern:**
```yaml
Track every deployment:
  - Version deployed
  - Timestamp
  - Who triggered (user or automated)
  - Environment
  - Git commit SHA
  - Duration

Store in:
  - Deployment dashboard
  - Metrics system
  - Audit logs
```

## Anti-Patterns to Avoid

### 1. Slow Pipelines

**Problem:**
- CI takes > 30 minutes
- Developers wait for feedback
- Reduces development velocity

**Solutions:**
- Parallelize tests
- Use caching
- Optimize test suite
- Run expensive tests on schedule, not every commit

### 2. Flaky Tests

**Problem:**
- Tests fail randomly
- Reduces confidence in CI
- Developers ignore failures

**Solutions:**
- Fix or remove flaky tests
- Don't merge code with flaky tests
- Quarantine flaky tests temporarily
- Investigate root causes

### 3. Missing Test Coverage

**Problem:**
- Bugs reach production
- CI doesn't catch issues
- False confidence

**Solutions:**
- Enforce minimum coverage (e.g., 80%)
- Require tests for new features
- Track coverage trends
- Review coverage in PRs

### 4. Manual Deployment Steps

**Problem:**
- Slows down releases
- Error-prone
- Not reproducible

**Solutions:**
- Automate everything
- Document and script manual steps
- Use infrastructure as code
- Treat manual steps as tech debt

### 5. No Rollback Plan

**Problem:**
- Deployments stuck if issues occur
- Extended downtime
- Panic responses

**Solutions:**
- Test rollback procedures
- Automate rollback
- Keep previous versions available
- Document rollback steps

### 6. Ignoring Security Scans

**Problem:**
- Vulnerabilities in production
- Compliance violations
- Security incidents

**Solutions:**
- Block on critical vulnerabilities
- Fix vulnerabilities promptly
- Scan on every build
- Track vulnerability trends

## Best Practices Summary

### Speed
- Optimize for fast feedback (< 10 min for basic checks)
- Use parallelization
- Implement caching
- Run expensive tests less frequently

### Reliability
- Make CI deterministic
- Fix flaky tests immediately
- Use proper test isolation
- Clean up test data

### Security
- Scan dependencies
- Scan containers
- Prevent secret commits
- Enforce least privilege

### Observability
- Track pipeline metrics
- Alert on failures
- Monitor deployment success
- Measure lead time and MTTR

### Maintainability
- Keep pipeline code simple
- Document complex steps
- Modularize pipeline configuration
- Version pipeline configurations

## Pipeline Evolution Path

**Stage 1: Basic CI**
- Run tests on PR
- Prevent broken merges

**Stage 2: Comprehensive CI**
- Multi-stage pipeline
- Security scanning
- Quality gates

**Stage 3: Continuous Delivery**
- Automated staging deployment
- Acceptance testing
- Manual production approval

**Stage 4: Continuous Deployment**
- Fully automated production deployment
- Robust monitoring and rollback
- High deployment frequency

**Stage 5: Advanced Automation**
- Canary deployments
- Feature flags
- Automated rollback on metrics
- Self-healing systems
