# CI/CD Patterns

## Pipeline Stages

```
┌─────────┐   ┌──────┐   ┌───────┐   ┌────────┐   ┌────────┐
│  Lint   │──▶│ Test │──▶│ Build │──▶│ Deploy │──▶│ Verify │
└─────────┘   └──────┘   └───────┘   └────────┘   └────────┘
```

### Stage Purposes

| Stage | Purpose | Fail Fast |
|-------|---------|-----------|
| Lint | Code style, static analysis | Yes |
| Test | Unit, integration tests | Yes |
| Build | Compile, bundle | Yes |
| Security | Vulnerability scanning | Yes |
| Deploy | Release to environment | No |
| Verify | Smoke tests, health checks | Yes |

## GitHub Actions Patterns

### Basic Pipeline

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### Matrix Builds

```yaml
test:
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest, windows-latest]
      node: [18, 20, 22]
    fail-fast: false
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node }}
    - run: npm ci
    - run: npm test
```

### Caching

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Or use setup action's built-in cache
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
```

### Security Scanning

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    # Dependency vulnerabilities
    - run: npm audit --audit-level=high

    # Secret scanning
    - uses: gitleaks/gitleaks-action@v2

    # SAST
    - uses: github/codeql-action/init@v3
      with:
        languages: javascript
    - uses: github/codeql-action/analyze@v3
```

### Deployment

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: [lint, test, build]
  if: github.ref == 'refs/heads/main'
  environment:
    name: production
    url: https://example.com
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: dist
    - name: Deploy
      run: |
        # Deploy commands here
      env:
        DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

## Branch Protection

```yaml
# Required status checks
required_status_checks:
  - lint
  - test
  - build
  - security

# Require PR reviews
required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true

# Prevent force push
allow_force_pushes: false

# Require linear history
required_linear_history: true
```

## Environment Strategy

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Development │───▶│   Staging   │───▶│ Production  │
│  (auto)     │    │  (auto)     │    │  (manual)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### GitHub Environments

```yaml
deploy-staging:
  environment:
    name: staging
    url: https://staging.example.com
  # Auto-deploy on main

deploy-production:
  environment:
    name: production
    url: https://example.com
  needs: deploy-staging
  # Requires manual approval
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No CI | Broken main branch | Add basic pipeline |
| Skip on draft PR | Surprises at review | Run lint at minimum |
| Long pipelines | Slow feedback | Parallelize, cache |
| No caching | Slow builds | Cache dependencies |
| Secrets in logs | Credential leak | Mask, use secrets |
| No test artifacts | Hard to debug | Upload on failure |
| No timeouts | Stuck builds | Set job timeouts |

## Performance Optimization

### Parallel Jobs

```yaml
jobs:
  lint:
    # ...
  test-unit:
    # ...
  test-integration:
    # ...
  # All run in parallel

  build:
    needs: [lint, test-unit, test-integration]
    # Waits for all
```

### Conditional Jobs

```yaml
test-integration:
  if: |
    github.event_name == 'push' ||
    contains(github.event.pull_request.labels.*.name, 'integration')
```

### Selective Runs

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package*.json'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

## Monitoring

### Job Annotations

```yaml
- name: Test
  run: npm test
  continue-on-error: false

- name: Annotate failures
  if: failure()
  run: echo "::error::Tests failed"
```

### Slack Notifications

```yaml
notify:
  needs: [deploy]
  if: always()
  runs-on: ubuntu-latest
  steps:
    - uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "text": "Deploy ${{ needs.deploy.result }}"
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Quick Reference

```bash
# Debug workflow locally
act -j test

# Validate workflow syntax
gh workflow view .github/workflows/ci.yml

# Re-run failed jobs
gh run rerun <run-id> --failed

# View workflow runs
gh run list --workflow=ci.yml
```
