---
name: ci-cd-pipelines
description: Use this skill when you need to create, configure, or optimize CI/CD pipelines using tools like GitHub Actions, GitLab CI, or Jenkins.
---

# Skill body

Comprehensive guidance for implementing continuous integration (CI) and continuous deployment (CD) pipelines.

## GitHub Actions

### Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### Full Production Pipeline

```yaml
name: Production Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

## CI/CD Standards

### Pipeline Trigger Requirements

CI pipelines MUST run on:

- All pull requests to protected branches
- All pushes to protected branches (develop, main)
- Scheduled intervals (daily/weekly for security scans)

### Required Pipeline Jobs

CI pipelines MUST include these jobs in order:

| Order | Job            | Purpose                        | Required |
| ----- | -------------- | ------------------------------ | -------- |
| 1     | Format check   | Verify code formatting         | MUST     |
| 2     | Lint           | Static analysis with errors    | MUST     |
| 3     | Test           | Run all tests                  | MUST     |
| 4     | Documentation  | Verify docs build              | MUST     |
| 5     | Security audit | Check for vulnerabilities      | MUST     |
| 6     | MSV check      | Verify minimum version support | MUST     |
| 7     | Coverage       | Measure test coverage          | SHOULD   |
| 8     | Benchmarks     | Performance regression check   | SHOULD   |

### CI Configuration Requirements

- **Pinned Action Versions (MUST)**: CI workflows MUST use pinned action versions. Prefer commit SHAs over tags.
- **Caching (MUST)**: CI MUST cache dependencies and build artifacts.
```yaml
# Example: Caching dependencies
- uses: actions/cache@v4
  with:
    path: |
      node_modules
      .next/cache
    key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
```