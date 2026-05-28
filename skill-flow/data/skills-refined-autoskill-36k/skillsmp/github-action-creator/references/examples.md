# Examples: GitHub Action Workflows

The following examples illustrate compliant workflows for different scenarios.

> **Note**: For advanced patterns (reusable workflows, caching, service containers, OIDC, artifacts), see [advanced-patterns.md](advanced-patterns.md).

## Node.js CI Workflow

```yaml
name: Node CI

on:
  push:
    branches: ["main"]

jobs:
  build-and-test:
    name: Build and Test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "22"
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test

      - name: Publish Job Summary
        if: always()
        run: |
          echo "### CI Result" >> $GITHUB_STEP_SUMMARY
          echo "- **Node Version:** 22" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

---

## Manual Release Workflow Using GitHub CLI

```yaml
name: Manual Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: Semantic version (e.g. 1.2.0)
        required: true
        type: string
      environment:
        description: Deployment target
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  create-release:
    name: Create Release
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Create Release
        run: gh release create v${{ inputs.version }} --notes "Release for ${{ inputs.environment }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish Summary
        run: |
          echo "## Release Created" >> $GITHUB_STEP_SUMMARY
          echo "- **Tag:** v${{ inputs.version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Target:** ${{ inputs.environment }}" >> $GITHUB_STEP_SUMMARY
```

---

## Matrix Strategy Workflow

```yaml
name: Cross-Platform Tests

on:
  pull_request:
    branches: ["main"]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test on ${{ matrix.os }} with Node ${{ matrix.node-version }}
    runs-on: ${{ matrix.os }}
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 22]

    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test

      - name: Publish Job Summary
        if: always()
        run: |
          echo "### Test Result" >> $GITHUB_STEP_SUMMARY
          echo "- **OS:** ${{ matrix.os }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Node:** ${{ matrix.node-version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

---

## Advanced Pipeline with Dependencies

```yaml
name: Build and Deploy

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  deployments: write
  id-token: write

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test

      - name: Publish Summary
        if: always()
        run: |
          echo "### Test Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY

  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: test
    timeout-minutes: 15
    outputs:
      build-id: ${{ steps.build-info.outputs.build-id }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Generate Build Info
        id: build-info
        run: |
          BUILD_ID="build-${{ github.sha }}-$(date +%s)"
          echo "build-id=$BUILD_ID" >> $GITHUB_OUTPUT

      - name: Publish Summary
        run: |
          echo "### Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Build ID:** ${{ steps.build-info.outputs.build-id }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    timeout-minutes: 20
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy Application
        run: |
          echo "Deploying build: ${{ needs.build.outputs.build-id }}"
          # Add deployment logic here

      - name: Publish Summary
        run: |
          echo "### Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Build ID:** ${{ needs.build.outputs.build-id }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment:** production" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

---

## Self-Hosted Runner with Labels

```yaml
name: Build on Self-Hosted

on:
  push:
    branches: ["main"]

jobs:
  build:
    name: Build on Custom Runner
    # Run on self-hosted runner with specific labels
    runs-on: [self-hosted, linux, x64, gpu]
    timeout-minutes: 30
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"

      - name: Install Dependencies
        run: npm ci

      - name: Build Application
        run: npm run build

      - name: Publish Summary
        if: always()
        run: |
          echo "### Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Runner:** Self-hosted (linux, x64, gpu)" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY

  # Alternative: Use runner group
  build-with-group:
    name: Build on Runner Group
    runs-on:
      group: production-runners
      labels: [linux, build]
    timeout-minutes: 30
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Build
        run: npm run build

      - name: Publish Summary
        run: |
          echo "### Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Runner Group:** production-runners" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

---

## Complete workflow_dispatch Input Types

```yaml
name: Manual Workflow with All Input Types

on:
  workflow_dispatch:
    inputs:
      # String input
      version:
        description: Version number (e.g., 1.2.3)
        required: true
        type: string
        default: "1.0.0"
      
      # Boolean input
      dry-run:
        description: Run in dry-run mode (no changes made)
        required: false
        type: boolean
        default: false
      
      # Choice input
      log-level:
        description: Logging verbosity level
        required: true
        type: choice
        options:
          - debug
          - info
          - warning
          - error
        default: info
      
      # Environment input
      deployment-target:
        description: Deployment environment
        required: true
        type: environment

jobs:
  execute:
    name: Execute Workflow
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: ${{ inputs.deployment-target }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Display Input Values
        run: |
          echo "Version: ${{ inputs.version }}"
          echo "Dry Run: ${{ inputs.dry-run }}"
          echo "Log Level: ${{ inputs.log-level }}"
          echo "Environment: ${{ inputs.deployment-target }}"

      - name: Execute Task
        run: |
          if [ "${{ inputs.dry-run }}" = "true" ]; then
            echo "Running in DRY-RUN mode"
          else
            echo "Executing actual deployment for version ${{ inputs.version }}"
          fi

      - name: Publish Summary
        if: always()
        run: |
          echo "## Execution Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Version:** ${{ inputs.version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Dry Run:** ${{ inputs.dry-run }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Log Level:** ${{ inputs.log-level }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment:** ${{ inputs.deployment-target }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

---

## Security Best Practices Example

This example demonstrates secure workflow patterns including permissions, script injection prevention, and secret handling.

```yaml
name: Secure CI/CD Pipeline

on:
  pull_request:
    types: [opened, synchronize]
  push:
    branches: [main]

# Explicit minimal permissions
permissions:
  contents: read
  pull-requests: write
  issues: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  security-check:
    name: Security Validation
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
      security-events: write
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6
        with:
          persist-credentials: false  # Don't persist credentials

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Run Security Audit
        run: npm audit --audit-level=moderate

      - name: Publish Summary
        if: always()
        run: |
          echo "## Security Check" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY

  build-and-test:
    name: Build and Test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6
        with:
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test

      - name: Build
        run: npm run build

      # Safe handling of PR information (prevents script injection)
      - name: Comment on PR (Safe Pattern)
        if: github.event_name == 'pull_request'
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
          PR_AUTHOR: ${{ github.event.pull_request.user.login }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          COMMENT="## Build Success\n\n"
          COMMENT+="- **PR:** #$PR_NUMBER\n"
          COMMENT+="- **Title:** $PR_TITLE\n"
          COMMENT+="- **Author:** @$PR_AUTHOR\n"
          COMMENT+="- **Status:** ✅ Build passed"
          
          # Safe: All untrusted input through environment variables
          gh pr comment "$PR_NUMBER" --body "$COMMENT"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish Summary
        if: always()
        run: |
          echo "## Build and Test Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Node Version:** 20" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY

  deploy:
    name: Deploy to Staging
    needs: [security-check, build-and-test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions:
      contents: read
      id-token: write  # For OIDC
      deployments: write
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6
        with:
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Build Production
        run: npm run build

      # Example: Secure secret handling
      - name: Deploy with Secret
        env:
          DEPLOY_TOKEN: ${{ secrets.STAGING_DEPLOY_TOKEN }}
          DEPLOY_URL: https://staging.example.com
        run: |
          # Never echo or log secrets
          # Use secrets only in secure contexts
          echo "Deploying to $DEPLOY_URL"
          # curl -H "Authorization: Bearer $DEPLOY_TOKEN" ...
          echo "Deployment complete"

      - name: Publish Summary
        if: always()
        run: |
          echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment:** staging" >> $GITHUB_STEP_SUMMARY
          echo "- **URL:** https://staging.example.com" >> $GITHUB_STEP_SUMMARY
          echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**Security Features Demonstrated**:

1. **Minimal Permissions**: Explicit `permissions:` at workflow and job level
2. **Script Injection Prevention**: All untrusted input via `env:` variables
3. **Credential Security**: `persist-credentials: false` when not needed
4. **Secret Handling**: Secrets never echoed or logged
5. **Environment Protection**: Staging environment with approval gates
6. **OIDC Ready**: `id-token: write` for cloud authentication
