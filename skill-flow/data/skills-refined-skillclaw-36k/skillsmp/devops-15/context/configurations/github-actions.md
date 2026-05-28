# GitHub Actions Configuration Templates

## Overview
This document provides production-ready GitHub Actions workflow templates for common CI/CD scenarios. Adapt these templates for your specific needs.

## Basic CI/CD Workflow (Node.js)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  release:
    types: [ published ]

env:
  NODE_VERSION: '18.x'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Code Quality Stage
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Check formatting
        run: npm run format:check

  # Testing Stage
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb

      - name: Generate coverage report
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
          fail_ci_if_error: true

  # Security Scanning Stage
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run dependency audit
        run: npm audit --audit-level=moderate

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run CodeQL analysis
        uses: github/codeql-action/init@v3
        with:
          languages: javascript

      - name: Perform CodeQL analysis
        uses: github/codeql-action/analyze@v3

  # Build and Push Docker Image
  build:
    name: Build and Push Image
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.event_name != 'pull_request'
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.version }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  # Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          # Update task definition with new image
          # Deploy to ECS service
          echo "Deploying to staging..."

      - name: Run smoke tests
        run: |
          curl -f https://staging.example.com/health || exit 1

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Staging deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()

  # Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.event_name == 'release'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to production
        run: |
          echo "Deploying to production..."

      - name: Run smoke tests
        run: |
          curl -f https://example.com/health || exit 1

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

## Python Application Workflow

```yaml
name: Python CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests with pytest
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Monorepo Workflow (Nx/Turborepo)

```yaml
name: Monorepo CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'packages/api/**'
            web:
              - 'packages/web/**'
            shared:
              - 'packages/shared/**'

  test:
    needs: changes
    if: ${{ needs.changes.outputs.packages != '[]' }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJSON(needs.changes.outputs.packages) }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests for ${{ matrix.package }}
        run: npx nx test ${{ matrix.package }} --coverage

      - name: Build ${{ matrix.package }}
        run: npx nx build ${{ matrix.package }}
```

## Docker Build and Push

```yaml
name: Docker Build

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            username/myapp
            ghcr.io/username/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=username/myapp:buildcache
          cache-to: type=registry,ref=username/myapp:buildcache,mode=max
```

## Terraform Workflow

```yaml
name: Terraform

on:
  push:
    branches: [ main ]
    paths:
      - 'terraform/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./terraform

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Terraform Format
        run: terraform fmt -check

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Scheduled Jobs

```yaml
name: Scheduled Maintenance

on:
  schedule:
    # Run every day at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup old artifacts
        run: |
          # Clean up old data, run maintenance tasks
          echo "Running cleanup..."

  dependency-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update dependencies
        run: |
          npm update
          npm audit fix

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: 'chore: update dependencies'
          title: 'chore: automated dependency updates'
          branch: dependency-updates
```

## Reusable Workflow

**`.github/workflows/reusable-test.yml`:**
```yaml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '18'
      runs-on:
        required: false
        type: string
        default: 'ubuntu-latest'
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ${{ inputs.runs-on }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Run tests
        run: npm test
```

**Using the reusable workflow:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '18'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Matrix Build (Multiple Versions/OS)

```yaml
name: Cross-Platform Testing

on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [16, 18, 20]
        include:
          # Additional config for specific combinations
          - os: ubuntu-latest
            node: 20
            experimental: true
        exclude:
          # Skip certain combinations
          - os: macos-latest
            node: 16

    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental || false }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}

      - run: npm ci
      - run: npm test
```

## Composite Action (Custom Action)

**`.github/actions/setup-project/action.yml`:**
```yaml
name: 'Setup Project'
description: 'Setup Node.js and install dependencies'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '18'

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci
      shell: bash

    - name: Cache build output
      uses: actions/cache@v3
      with:
        path: dist
        key: build-${{ github.sha }}
```

**Using the composite action:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-project
        with:
          node-version: '18'
```

## Best Practices

### 1. Security
```yaml
- Use secrets for sensitive data
- Use GITHUB_TOKEN for API access
- Limit permissions per job
- Scan dependencies regularly
- Never log secrets
```

### 2. Performance
```yaml
- Cache dependencies (npm, pip, maven)
- Use matrix builds for parallelization
- Avoid redundant work with path filters
- Use conditional job execution
- Optimize Docker layer caching
```

### 3. Reliability
```yaml
- Set timeouts on jobs
- Use continue-on-error for experimental jobs
- Implement retry logic for flaky tests
- Pin action versions (not @main)
- Test workflows in branches before merging
```

### 4. Maintainability
```yaml
- Use reusable workflows
- Create composite actions
- Document complex workflows
- Use consistent naming
- Keep workflows DRY
```

## Common Patterns

### Conditional Execution
```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh

- name: Comment on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: 'Tests passed!'
      })
```

### Environment Variables
```yaml
env:
  GLOBAL_VAR: value

jobs:
  job1:
    env:
      JOB_VAR: value
    steps:
      - name: Step with env
        env:
          STEP_VAR: value
        run: echo "$GLOBAL_VAR $JOB_VAR $STEP_VAR"
```

### Artifacts
```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v3
  with:
    name: build-output
    path: dist/
    retention-days: 7

- name: Download artifacts
  uses: actions/download-artifact@v3
  with:
    name: build-output
    path: dist/
```

### Manual Approval (Environments)
```yaml
deploy:
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://example.com
  steps:
    - run: ./deploy.sh
```
