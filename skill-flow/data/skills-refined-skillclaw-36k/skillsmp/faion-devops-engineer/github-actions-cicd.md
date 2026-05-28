---
id: github-actions-cicd
name: "GitHub Actions CI/CD"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# GitHub Actions CI/CD

## Overview

GitHub Actions is a CI/CD platform integrated directly into GitHub repositories. It enables automated workflows triggered by events like pushes, pull requests, and releases, with support for matrix builds, reusable workflows, and extensive marketplace actions.

## When to Use

- Projects hosted on GitHub
- Open source projects needing free CI/CD
- Teams already using GitHub ecosystem
- Workflows requiring GitHub integration (issues, PRs, releases)
- Multi-platform builds (Linux, Windows, macOS)

## Key Concepts

| Concept | Description |
|---------|-------------|
| Workflow | Automated process defined in YAML |
| Job | Set of steps running on same runner |
| Step | Individual task (action or shell command) |
| Action | Reusable unit of code |
| Runner | Server executing workflows |
| Event | Trigger that starts workflow |
| Artifact | Files persisted between jobs |
| Secret | Encrypted environment variable |

### Workflow Structure

```
.github/
├── workflows/
│   ├── ci.yml           # CI pipeline
│   ├── cd.yml           # CD pipeline
│   ├── release.yml      # Release workflow
│   └── scheduled.yml    # Scheduled tasks
├── actions/
│   └── custom-action/   # Custom composite action
│       └── action.yml
└── CODEOWNERS           # Code review assignments
```

## Implementation

### CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.12'

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier
        run: npm run format:check

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, test]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
          retention-days: 7

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Run CodeQL analysis
        uses: github/codeql-action/init@v3
        with:
          languages: javascript

      - name: Perform CodeQL analysis
        uses: github/codeql-action/analyze@v3

  docker:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build-push.outputs.digest }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        id: build-push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true
```

### CD Pipeline

```yaml
# .github/workflows/cd.yml
name: CD

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false

jobs:
  staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.28.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster --region eu-central-1

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
            -n staging

          kubectl rollout status deployment/app -n staging --timeout=5m

      - name: Run smoke tests
        run: |
          npm ci
          npm run test:smoke -- --url=https://staging.example.com

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Staging deployment failed for ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": ":x: *Staging deployment failed*\nRepo: ${{ github.repository }}\nCommit: ${{ github.sha }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: staging
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.28.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name production-cluster --region eu-central-1

      - name: Deploy with canary
        run: |
          # Deploy canary (10% traffic)
          kubectl set image deployment/app-canary \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
            -n production

          kubectl rollout status deployment/app-canary -n production --timeout=5m

          # Wait and validate
          sleep 300

          # If canary healthy, deploy to main
          kubectl set image deployment/app \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
            -n production

          kubectl rollout status deployment/app -n production --timeout=10m

      - name: Create Sentry release
        uses: getsentry/action-release@v1
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: ${{ vars.SENTRY_ORG }}
          SENTRY_PROJECT: ${{ vars.SENTRY_PROJECT }}
        with:
          environment: production
          version: ${{ github.sha }}

      - name: Notify on success
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Production deployment successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": ":white_check_mark: *Production deployment successful*\nRepo: ${{ github.repository }}\nCommit: ${{ github.sha }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          registry-url: 'https://npm.pkg.github.com'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --latest --strip header

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.content }}
          draft: false
          prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') || contains(github.ref, 'rc') }}
          files: |
            dist/*.tar.gz
            dist/*.zip

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ steps.version.outputs.version }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Reusable Workflow

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
      cluster-name:
        required: true
        type: string
      namespace:
        required: true
        type: string
    secrets:
      AWS_ROLE_ARN:
        required: true
      SLACK_WEBHOOK:
        required: false

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment }}
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name ${{ inputs.cluster-name }} --region eu-central-1

      - name: Deploy
        run: |
          kubectl set image deployment/app app=${{ inputs.image-tag }} -n ${{ inputs.namespace }}
          kubectl rollout status deployment/app -n ${{ inputs.namespace }} --timeout=10m

      - name: Notify
        if: always() && secrets.SLACK_WEBHOOK != ''
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Deployment to ${{ inputs.environment }}: ${{ job.status }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Matrix Build

```yaml
# .github/workflows/matrix.yml
name: Matrix Build

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 20
            coverage: true

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- ${{ matrix.coverage && '--coverage' || '' }}

      - name: Upload coverage
        if: matrix.coverage
        uses: codecov/codecov-action@v4
```

### Custom Composite Action

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Node.js environment with caching'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
  install-deps:
    description: 'Install dependencies'
    required: false
    default: 'true'

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - name: Get npm cache directory
      id: npm-cache-dir
      shell: bash
      run: echo "dir=$(npm config get cache)" >> $GITHUB_OUTPUT

    - name: Cache npm dependencies
      id: cache
      uses: actions/cache@v4
      with:
        path: |
          ${{ steps.npm-cache-dir.outputs.dir }}
          node_modules
        key: ${{ runner.os }}-node-${{ inputs.node-version }}-${{ hashFiles('**/package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-node-${{ inputs.node-version }}-

    - name: Install dependencies
      if: inputs.install-deps == 'true' && steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

## Best Practices

1. **Use concurrency controls** - Prevent duplicate runs with concurrency groups
2. **Pin action versions** - Use SHA or version tags, not @main
3. **Use environments** - Define staging/production with protection rules
4. **Cache dependencies** - Reduce build times with caching
5. **Use OIDC for cloud auth** - Avoid long-lived credentials
6. **Implement matrix builds** - Test across versions and platforms
7. **Create reusable workflows** - DRY principle for common patterns
8. **Use composite actions** - Package common steps
9. **Set timeout limits** - Prevent runaway jobs
10. **Secure secrets** - Use GitHub Secrets, never hardcode

## Common Pitfalls

1. **Unpinned actions** - Using @main can introduce breaking changes. Pin to specific versions.

2. **Missing concurrency** - Parallel runs can cause conflicts. Use concurrency groups.

3. **Hardcoded secrets** - Secrets in workflow files are exposed. Use GitHub Secrets.

4. **No caching** - Repeated dependency downloads slow builds. Always cache.

5. **Ignoring job outputs** - Data doesn't persist between jobs. Use artifacts or outputs.

6. **Missing workflow_dispatch** - Cannot manually trigger. Add for debugging.

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
