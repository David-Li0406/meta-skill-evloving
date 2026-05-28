# Advanced Patterns: GitHub Actions

This document covers advanced GitHub Actions patterns for mature workflows, including reusable workflows, service containers, caching strategies, and cloud authentication.

---

## Table of Contents

1. [Reusable Workflows](#reusable-workflows)
2. [Advanced Caching Strategies](#advanced-caching-strategies)
3. [Service Containers](#service-containers)
4. [Environment Protection Rules](#environment-protection-rules)
5. [Artifact Management](#artifact-management)
6. [OIDC Authentication](#oidc-authentication-cloud-providers)
7. [Composite Actions](#composite-actions)
8. [Advanced Matrix Strategies](#advanced-matrix-strategies)
9. [Dependabot for Actions](#dependabot-for-actions)

---

## Reusable Workflows

Reusable workflows reduce duplication and enforce standards across multiple repositories.

### Basic Reusable Workflow

**File**: `.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build Workflow

on:
  workflow_call:
    inputs:
      node-version:
        description: Node.js version to use
        required: false
        type: string
        default: "20"
      environment:
        description: Deployment environment
        required: true
        type: string
    secrets:
      deploy-token:
        description: Deployment token
        required: true
    outputs:
      build-version:
        description: Version of the build artifact
        value: ${{ jobs.build.outputs.version }}

permissions:
  contents: read

jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    timeout-minutes: 15
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Extract Version
        id: version
        run: |
          VERSION=$(node -p "require('./package.json').version")
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.deploy-token }}
          ENVIRONMENT: ${{ inputs.environment }}
        run: |
          echo "Deploying version ${{ steps.version.outputs.version }} to $ENVIRONMENT"
          # Deployment logic here

      - name: Publish Summary
        if: always()
        run: |
          echo "## Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Version:** ${{ steps.version.outputs.version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Node:** ${{ inputs.node-version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment:** ${{ inputs.environment }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

### Calling a Reusable Workflow

**File**: `.github/workflows/deploy-staging.yml`

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

permissions:
  contents: read

jobs:
  call-reusable-build:
    name: Build and Deploy
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: "22"
      environment: staging
    secrets:
      deploy-token: ${{ secrets.STAGING_DEPLOY_TOKEN }}

  post-deployment:
    name: Post-Deployment Tasks
    needs: call-reusable-build
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Notify Team
        run: |
          echo "Deployed version: ${{ needs.call-reusable-build.outputs.build-version }}"
          # Send notification

      - name: Publish Summary
        run: |
          echo "## Deployment Complete" >> $GITHUB_STEP_SUMMARY
          echo "- **Version:** ${{ needs.call-reusable-build.outputs.build-version }}" >> $GITHUB_STEP_SUMMARY
```

### Organization-Level Reusable Workflows

```yaml
name: Use Org Template

on:
  push:
    branches: [main]

jobs:
  build:
    uses: my-org/.github/.github/workflows/standard-ci.yml@v1
    with:
      environment: production
    secrets: inherit  # Pass all secrets to reusable workflow
```

**Benefits**:

- Centralized CI/CD templates
- Consistent standards across repos
- Easier maintenance and updates

---

## Advanced Caching Strategies

### Multi-Level Caching

```yaml
name: Advanced Caching

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js with Auto-Cache
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm
          # Auto-caching enabled if package.json has "packageManager" field

      - name: Cache Build Outputs
        uses: actions/cache@v4
        with:
          path: |
            .next/cache
            dist/
            build/
          key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.ts', '**/*.tsx') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-
            ${{ runner.os }}-build-

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build
```

### Monorepo Caching

```yaml
- name: Setup Node.js for Monorepo
  uses: actions/setup-node@v6
  with:
    node-version: "20"
    cache: npm
    cache-dependency-path: |
      packages/*/package-lock.json
      apps/*/package-lock.json
```

### Cache Management

```yaml
- name: Cache with Fallback
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
      ${{ runner.os }}-

- name: Clear Old Caches (scheduled workflow)
  # Use GitHub API to delete old caches
  run: |
    gh cache delete --all --older-than 7d
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Security: Disable Auto-Caching

For workflows with sensitive dependencies:

```yaml
- name: Setup Node.js (No Cache for Security)
  uses: actions/setup-node@v6
  with:
    node-version: "20"
    package-manager-cache: false  # Disable automatic caching
```

---

## Service Containers

Service containers run alongside jobs for integration testing.

### PostgreSQL Database

```yaml
name: Integration Tests with Database

on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    name: Run Integration Tests
    runs-on: ubuntu-latest
    timeout-minutes: 20

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Run Database Migrations
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
        run: npm run db:migrate

      - name: Run Integration Tests
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
        run: npm run test:integration

      - name: Publish Summary
        if: always()
        run: |
          echo "## Test Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Database:** PostgreSQL 15" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

### Multiple Services (Database + Redis)

```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: postgres
    options: --health-cmd pg_isready --health-interval 10s

  redis:
    image: redis:7
    ports:
      - 6379:6379
    options: --health-cmd "redis-cli ping" --health-interval 10s

steps:
  - name: Run Tests
    env:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/testdb
      REDIS_URL: redis://redis:6379
    run: npm test
```

### Container Jobs

Run the entire job inside a container:

```yaml
jobs:
  build-in-container:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    container:
      image: node:20-alpine
      env:
        NODE_ENV: production
      options: --user root
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build
```

---

## Environment Protection Rules

Environments provide deployment gates, secrets scoping, and approval workflows.

### Basic Environment Usage

```yaml
name: Production Deployment

on:
  push:
    branches: [main]

permissions:
  contents: read
  deployments: write

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    timeout-minutes: 30
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Deploy
        env:
          PROD_API_KEY: ${{ secrets.PROD_API_KEY }}  # Environment-scoped secret
        run: |
          echo "Deploying to production..."
          # Deployment logic

      - name: Publish Summary
        run: |
          echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment:** production" >> $GITHUB_STEP_SUMMARY
          echo "- **URL:** https://example.com" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

### Environment Configuration (GitHub UI)

Environments can be configured in Settings → Environments:

- **Required Reviewers**: 1-6 reviewers must approve
- **Wait Timer**: Delay deployment by X minutes
- **Deployment Branches**: Restrict to specific branches
- **Environment Secrets**: Scope secrets to environment only

### Multi-Stage Deployment

```yaml
jobs:
  deploy-staging:
    name: Deploy to Staging
    environment:
      name: staging
      url: https://staging.example.com
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6
      - name: Deploy
        run: echo "Deploying to staging"

  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    environment:
      name: production
      url: https://production.example.com
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v6
      - name: Deploy
        run: echo "Deploying to production"
      - name: Notify
        if: success()
        run: echo "Production deployment successful!"
```

---

## Artifact Management

Share build outputs between jobs or preserve files for download.

### Upload and Download Artifacts

```yaml
name: Build and Test with Artifacts

on:
  push:

permissions:
  contents: read

jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: |
            dist/
            build/
          retention-days: 7  # Keep for 7 days
          if-no-files-found: error

  test:
    name: Test Built Application
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Download Build Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Run E2E Tests
        run: npm run test:e2e

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/
          retention-days: 30
```

### Multiple Artifacts

```yaml
- name: Upload Multiple Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: coverage-reports
    path: |
      coverage/
      !coverage/tmp/  # Exclude tmp directory
      reports/*.html
```

### Artifact Patterns

```yaml
# Upload logs only on failure
- name: Upload Logs on Failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: failure-logs-${{ github.run_id }}
    path: logs/

# Conditional artifact upload
- name: Upload Debug Artifacts
  if: github.event_name == 'workflow_dispatch' && inputs.debug == 'true'
  uses: actions/upload-artifact@v4
  with:
    name: debug-info
    path: debug/
```

---

## OIDC Authentication (Cloud Providers)

Use OpenID Connect to authenticate with cloud providers without long-lived credentials.

### AWS OIDC Authentication

```yaml
name: Deploy to AWS with OIDC

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write  # Required for OIDC

jobs:
  deploy:
    name: Deploy to AWS
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          role-session-name: github-actions-session
          aws-region: us-east-1

      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://my-bucket/
          echo "Deployed to AWS"

      - name: Publish Summary
        run: |
          echo "## AWS Deployment" >> $GITHUB_STEP_SUMMARY
          echo "- **Region:** us-east-1" >> $GITHUB_STEP_SUMMARY
          echo "- **Bucket:** s3://my-bucket/" >> $GITHUB_STEP_SUMMARY
```

### Azure OIDC Authentication

```yaml
name: Deploy to Azure with OIDC

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write

jobs:
  deploy:
    name: Deploy to Azure
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Azure Login (OIDC)
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy Web App
        run: |
          az webapp deploy --resource-group MyRG --name MyWebApp --src-path dist/
```

### GCP OIDC Authentication

```yaml
name: Deploy to GCP with OIDC

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write

jobs:
  deploy:
    name: Deploy to GCP
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Authenticate to Google Cloud (OIDC)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/github/providers/github-provider
          service_account: github-actions@my-project.iam.gserviceaccount.com

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy my-service --image gcr.io/my-project/my-image:latest
```

**Benefits of OIDC**:

- No long-lived credentials in GitHub Secrets
- Automatic token rotation
- Fine-grained IAM policies
- Reduced attack surface

---

## Composite Actions

Create reusable action logic that can be called from multiple workflows.

### Creating a Composite Action

**File**: `.github/actions/setup-project/action.yml`

```yaml
name: Setup Project
description: Install dependencies and setup environment for Node.js projects

inputs:
  node-version:
    description: Node.js version to use
    required: false
    default: "20"
  install-command:
    description: Command to install dependencies
    required: false
    default: npm ci

runs:
  using: composite
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v6
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm

    - name: Install Dependencies
      shell: bash
      run: ${{ inputs.install-command }}

    - name: Verify Installation
      shell: bash
      run: |
        echo "Node version: $(node --version)"
        echo "npm version: $(npm --version)"
```

### Using a Composite Action

```yaml
name: CI with Composite Action

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Project
        uses: ./.github/actions/setup-project
        with:
          node-version: "22"

      - name: Run Tests
        run: npm test
```

### Advanced Composite Action with Outputs

**File**: `.github/actions/build-info/action.yml`

```yaml
name: Get Build Info
description: Extract version and build metadata

outputs:
  version:
    description: Application version
    value: ${{ steps.version.outputs.version }}
  commit-sha:
    description: Short commit SHA
    value: ${{ steps.sha.outputs.sha }}

runs:
  using: composite
  steps:
    - name: Extract Version
      id: version
      shell: bash
      run: |
        VERSION=$(node -p "require('./package.json').version")
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Get Commit SHA
      id: sha
      shell: bash
      run: |
        SHORT_SHA=${GITHUB_SHA::7}
        echo "sha=$SHORT_SHA" >> $GITHUB_OUTPUT
```

---

## Advanced Matrix Strategies

Test across multiple configurations efficiently.

### Dynamic Matrix

```yaml
name: Dynamic Matrix Testing

on:
  pull_request:

permissions:
  contents: read

jobs:
  setup-matrix:
    name: Setup Test Matrix
    runs-on: ubuntu-latest
    timeout-minutes: 5
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Generate Matrix
        id: set-matrix
        run: |
          # Generate matrix based on changed files, config, etc.
          MATRIX='{"node-version":["18","20","22"],"os":["ubuntu-latest","windows-latest"]}'
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  test:
    name: Test ${{ matrix.os }} - Node ${{ matrix.node-version }}
    needs: setup-matrix
    runs-on: ${{ matrix.os }}
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix: ${{ fromJson(needs.setup-matrix.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### Matrix with Include/Exclude

```yaml
strategy:
  fail-fast: false
  max-parallel: 4  # Run max 4 jobs concurrently
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [18, 20, 22]
    exclude:
      # Skip Windows + Node 18 (unsupported)
      - os: windows-latest
        node-version: 18
    include:
      # Add experimental config
      - os: ubuntu-latest
        node-version: 23
        experimental: true
```

### Conditional Matrix Jobs

```yaml
strategy:
  matrix:
    config:
      - { os: ubuntu-latest, arch: x64, target: linux }
      - { os: windows-latest, arch: x64, target: windows }
      - { os: macos-latest, arch: arm64, target: darwin }

steps:
  - name: Build for ${{ matrix.config.target }}
    run: npm run build:${{ matrix.config.target }}
  
  - name: Test (Linux only)
    if: matrix.config.target == 'linux'
    run: npm run test:integration
```

---

## Dependabot for Actions

Automate GitHub Action version updates.

### Dependabot Configuration

**File**: `.github/dependabot.yml`

```yaml
version: 2
updates:
  # Update GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "America/New_York"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "chore(actions)"
      include: "scope"

  # Update npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    versioning-strategy: increase
    open-pull-requests-limit: 10
```

### Advanced Dependabot Config

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    # Group updates
    groups:
      actions-core:
        patterns:
          - "actions/*"
      aws-actions:
        patterns:
          - "aws-actions/*"
    # Ignore specific versions
    ignore:
      - dependency-name: "actions/checkout"
        versions: ["v3.x"]  # Stay on v4+
    # Auto-merge minor/patch updates
    reviewers:
      - "devops-team"
    assignees:
      - "tech-lead"
```

### Auto-Merge Dependabot PRs (Workflow)

```yaml
name: Auto-Merge Dependabot

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    name: Auto-Merge Dependabot PRs
    runs-on: ubuntu-latest
    timeout-minutes: 5
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Fetch PR Metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2

      - name: Auto-Merge Minor/Patch Updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch' || steps.metadata.outputs.update-type == 'version-update:semver-minor'
        run: |
          gh pr merge --auto --squash "${{ github.event.pull_request.number }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish Summary
        run: |
          echo "## Auto-Merge Decision" >> $GITHUB_STEP_SUMMARY
          echo "- **Update Type:** ${{ steps.metadata.outputs.update-type }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Action:** Auto-merge" >> $GITHUB_STEP_SUMMARY
```

---

## Summary

These advanced patterns enable:

- **Reusable Workflows**: DRY principles for CI/CD
- **Caching**: Performance optimization
- **Service Containers**: Integration testing
- **Environment Protection**: Safe deployments
- **Artifacts**: Job-to-job communication
- **OIDC**: Secure cloud authentication
- **Composite Actions**: Reusable step sequences
- **Matrix Strategies**: Comprehensive testing
- **Dependabot**: Automated updates

Use these patterns to build production-grade, maintainable GitHub Actions workflows.
