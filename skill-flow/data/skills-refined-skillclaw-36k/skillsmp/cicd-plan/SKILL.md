---
name: cicd-plan
description: Generate a CI/CD pipeline plan for any stack. Use when user asks for CI/CD setup, GitHub Actions workflow, deployment pipeline, or automated testing configuration.
---

# CI/CD Pipeline Plan Generator

Generate a complete CI/CD pipeline plan including build, test, security scanning, and deployment stages.

## Standalone Usage

Can be invoked directly:
- "Create a GitHub Actions workflow for my Node.js app"
- "Set up CI/CD for a Next.js + Vercel deployment"
- "Generate a deployment pipeline for AWS ECS"

## Pipeline Components

### 1. Repository Strategy
- Monorepo vs multi-repo
- Branch protection rules
- Code ownership

### 2. Branching Strategy
- trunk-based (recommended for most)
- GitHub flow
- GitFlow (for release-heavy projects)

### 3. CI Stages
- Build
- Test (unit, integration)
- Lint
- Security scan

### 4. CD Stages
- Deploy to dev
- Deploy to staging
- Deploy to production (with approval)

### 5. Quality Gates
- Test coverage thresholds
- Security vulnerability checks
- Code review requirements

## Output Contract

```yaml
cicd_plan:
  stack: "<stack description>"
  platform: "<github-actions|gitlab-ci|azure-devops|circleci>"

  repository:
    strategy: "<monorepo|multi-repo>"
    structure:
      - "<directory structure>"

  branching:
    strategy: "<trunk-based|github-flow|gitflow>"
    branches:
      - name: "main"
        purpose: "Production-ready code"
        protection:
          - "Require pull request"
          - "Require 1 approval"
          - "Require CI pass"
          - "No force push"
      - name: "feature/*"
        purpose: "Feature development"

  ci_pipeline:
    triggers:
      - "push to main"
      - "pull_request to main"

    stages:
      - name: "build"
        steps:
          - "Checkout code"
          - "Setup runtime"
          - "Install dependencies"
          - "Build application"
        artifacts:
          - "<build output>"

      - name: "test"
        steps:
          - "Run unit tests"
          - "Run integration tests"
          - "Generate coverage report"
        thresholds:
          coverage: "<X%>"

      - name: "lint"
        steps:
          - "Run linter"
          - "Check formatting"

      - name: "security"
        steps:
          - "Dependency vulnerability scan"
          - "SAST (static analysis)"
          - "Secret detection"
        tools:
          - "<snyk|dependabot|trivy>"

  cd_pipeline:
    artifacts:
      registry: "<ECR|GCR|ACR|Docker Hub|Vercel>"
      tagging: "<git-sha|semver|timestamp>"

    environments:
      - name: "development"
        trigger: "push to main"
        approval: "none"
        url: "<dev-url>"
        strategy: "rolling"

      - name: "staging"
        trigger: "after dev success"
        approval: "none"
        url: "<staging-url>"
        strategy: "rolling"

      - name: "production"
        trigger: "manual | tag"
        approval: "required"
        approvers: ["<team>"]
        url: "<prod-url>"
        strategy: "<rolling|blue-green|canary>"

  secrets:
    approach: "<github-secrets|vault|aws-secrets-manager>"
    required:
      - name: "<SECRET_NAME>"
        description: "<what it's for>"

  quality_gates:
    - "All tests pass"
    - "Coverage >= X%"
    - "No critical vulnerabilities"
    - "Linting passes"
    - "Approval for production"

  rollback:
    strategy: "<automatic|manual>"
    procedure:
      - "<step 1>"
      - "<step 2>"

  preview_environments:
    enabled: true|false
    trigger: "pull_request"
    provider: "<vercel|netlify|railway|custom>"

  notifications:
    - channel: "<slack|email|teams>"
      events: ["failure", "deployment"]

  config_files:
    - filename: ".github/workflows/ci.yml"
      content: |
        <workflow content>

    - filename: ".github/workflows/cd.yml"
      content: |
        <workflow content>
```

## GitHub Actions Templates

### Node.js / Next.js CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Test
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

      - name: Build
        run: npm run build

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

### CD to Vercel

```yaml
# .github/workflows/cd.yml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy-preview:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### CD to AWS ECS

```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: myapp
  ECS_CLUSTER: myapp-cluster
  ECS_SERVICE: myapp-service

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster $ECS_CLUSTER \
            --service $ECS_SERVICE \
            --force-new-deployment
```

### .NET CI/CD

```yaml
name: .NET CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore

      - name: Test
        run: dotnet test --no-build --verbosity normal --collect:"XPlat Code Coverage"

      - name: Publish
        run: dotnet publish -c Release -o publish
```

## Branching Strategies

### Trunk-Based (Recommended)
```
main ──●──●──●──●──●── (always deployable)
        \   /
         ──── feature/xyz (short-lived, < 1 day)
```

### GitHub Flow
```
main ──●──────●──────●── (deploy on merge)
        \    /  \    /
         ────    ────  (feature branches)
```

### GitFlow
```
main ────────●────────●── (releases only)
              \      /
develop ──●──●──●──●──●── (integration)
           \  /  \  /
            ──    ──  (features)
```
