---
name: cicd-automation
description: Use this skill when designing CI/CD pipelines, automating deployments, or configuring workflows with GitHub Actions.
---

# CI/CD Automation Skill

## Pipeline Design Principles

### Stages
1. **Build**: Compile, bundle, create artifacts
2. **Test**: Unit, integration, E2E tests
3. **Scan**: Security, dependencies, quality
4. **Deploy**: Staging, then production
5. **Verify**: Smoke tests, health checks

### Best Practices
- Fail fast (run quick checks first)
- Parallelize independent jobs
- Cache dependencies aggressively
- Use immutable artifacts
- Never store secrets in code

## GitHub Actions Patterns

### Basic CI Workflow
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup Node
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Run linter
      run: npm run lint
```

### Matrix Testing
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

### Caching
```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Deployment Workflow
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to staging
      run: ./deploy.sh staging
      env:
        DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to production
      run: ./deploy.sh production
      env:
        DEPLOY_KEY: ${{ secrets.PROD_DEPLOY_KEY }}
```

### Reusable Workflows
```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build
on:
  workflow_call:
    inputs:
      environment:
```