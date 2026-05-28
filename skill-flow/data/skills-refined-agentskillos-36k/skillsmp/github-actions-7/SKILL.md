---
name: GitHub Actions
description: Comprehensive GitHub Actions workflow templates and CI/CD automation. This skill should be used when creating CI/CD pipelines, setting up automated workflows, or implementing GitHub Actions for projects of any complexity. Includes intelligent project analysis, security-hardened templates, and production-ready patterns.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
license: MIT
---

# GitHub Actions

Comprehensive GitHub Actions workflow templates and CI/CD automation patterns. Generate production-ready workflows with intelligent project analysis, security hardening, and best practices built-in.

## Quick Start - Top 5 Workflows

These five workflows cover 80% of common use cases. Start here before exploring advanced patterns.

### 1. Basic CI/CD (Node.js)

**When to use:** Node.js/TypeScript projects requiring automated testing and deployment

**Key features:**
- Automated testing on Node 16/18/20
- Dependency caching (npm/yarn/pnpm)
- Parallel lint and test execution
- Build artifact upload
- Deployment to staging/production

**Template:** `assets/workflows/basic/nodejs-ci.yml`

**Example trigger:**
```
"Set up CI/CD for my Node.js API"
"Create GitHub Actions workflow for TypeScript project"
```

### 2. Docker Build & Push

**When to use:** Containerized applications requiring automated image builds

**Key features:**
- Multi-stage Docker builds
- Layer caching for faster builds
- Automatic tagging with Git SHA and branch
- Push to Docker Hub/GHCR
- Security scanning integration

**Template:** `assets/workflows/docker/docker-build-push.yml`

**Example trigger:**
```
"Create Docker build workflow"
"Automate Docker image builds on GitHub"
```

### 3. Kubernetes Deployment

**When to use:** Applications deploying to Kubernetes clusters

**Key features:**
- kubectl configuration with AWS/GKE/Azure
- Helm chart deployment
- Environment-specific configs (dev/staging/prod)
- Deployment verification with health checks
- Automatic rollback on failure

**Template:** `assets/workflows/kubernetes/k8s-deploy.yml`

**Example trigger:**
```
"Deploy to Kubernetes with GitHub Actions"
"Create K8s deployment workflow"
```

### 4. Monorepo CI

**When to use:** Monorepos using Turborepo, Nx, or Lerna

**Key features:**
- Path filtering to run affected jobs
- Incremental build caching
- Parallel task execution
- Per-package deployment triggers
- Change detection

**Template:** `assets/workflows/monorepo/monorepo-path-filter.yml`

**Example trigger:**
```
"Set up CI for my Turborepo monorepo"
"Optimize GitHub Actions for Nx workspace"
```

### 5. Security Scanning

**When to use:** Any project requiring automated security checks

**Key features:**
- CodeQL static analysis
- Dependency vulnerability scanning
- Container image scanning (Trivy)
- Secret scanning alerts
- Automatic PR creation for fixes

**Template:** `assets/workflows/security/codeql-analysis.yml`

**Example trigger:**
```
"Add security scanning to my repo"
"Set up automated dependency checks"
```

## Instructions

### Phase 1: Project Analysis

**Analyze project structure automatically:**

```bash
# Use the detection script
bash .claude/skills/github-actions/scripts/detect-project.sh
```

**Manual analysis checklist:**

1. **Identify project type:**
   - Check for `package.json` (Node.js/TypeScript)
   - Check for `requirements.txt` or `pyproject.toml` (Python)
   - Check for `go.mod` (Go)
   - Check for `pom.xml` (Java/Maven)
   - Check for `Dockerfile` (containerized)

2. **Identify deployment target:**
   - Check for `kubernetes/` or `k8s/` directories
   - Check for `docker-compose.yml`
   - Check for Terraform/Helm charts
   - Check for Vercel/Netlify config

3. **Identify monorepo setup:**
   - Check for `turbo.json` (Turborepo)
   - Check for `nx.json` (Nx)
   - Check for `lerna.json`
   - Check for `pnpm-workspace.yaml`

4. **Identify existing workflows:**
   - List `.github/workflows/` directory
   - Identify gaps in current CI/CD

### Phase 2: Template Selection

**Select appropriate template based on analysis:**

**Language-specific:**
- Node.js/TypeScript → `basic/nodejs-ci.yml`
- Python → `basic/python-ci.yml`
- Go → `basic/go-ci.yml`
- Java → `basic/java-ci.yml`

**Deployment patterns:**
- Docker → `docker/docker-build-push.yml`
- Kubernetes → `kubernetes/k8s-deploy.yml`
- Serverless → `advanced/release-workflow.yml`

**Repository structure:**
- Monorepo → `monorepo/monorepo-path-filter.yml`
- Polyrepo → Use basic templates

**Security requirements:**
- Basic security → `security/dependency-review.yml`
- Comprehensive → `security/codeql-analysis.yml` + `security/trivy-scan.yml`

### Phase 3: Customization

**Customize selected templates:**

1. **Update triggers:**
   ```yaml
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]
     schedule:
       - cron: '0 0 * * 0'  # Weekly
   ```

2. **Configure environment variables:**
   ```yaml
   env:
     NODE_VERSION: '20'
     REGISTRY: ghcr.io
     IMAGE_NAME: ${{ github.repository }}
   ```

3. **Adjust job permissions:**
   ```yaml
   permissions:
     contents: read
     pull-requests: write
     deployments: write
   ```

4. **Add secrets:**
   - Go to repo Settings → Secrets and variables → Actions
   - Add required secrets (AWS credentials, Docker tokens, etc.)

### Phase 4: Testing & Validation

**Validate workflow before committing:**

```bash
# Validate YAML syntax
bash .claude/skills/github-actions/scripts/validate-yaml.sh .github/workflows/your-workflow.yml

# Dry-run with act (requires act installed)
act -n -W .github/workflows/your-workflow.yml
```

**Test in practice:**

1. Create feature branch
2. Push workflow to `.github/workflows/`
3. Create test PR to validate execution
4. Check Actions tab for results
5. Iterate based on errors

### Phase 5: Optimization

**Optimize workflow performance:**

1. **Enable caching:**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: ~/.npm
       key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
   ```

2. **Parallelize jobs:**
   ```yaml
   jobs:
     test:
       strategy:
         matrix:
           node-version: [16, 18, 20]
         fail-fast: false
   ```

3. **Use composite actions for reusable steps**

4. **Implement incremental builds for monorepos**

5. **Optimize Docker layer caching**

## Pattern Library

All templates are organized in `assets/workflows/` by category.

### Basic CI Workflows

| Template | Use Case | Languages |
|----------|----------|-----------|
| `basic/nodejs-ci.yml` | Standard CI/CD | Node.js, TypeScript |
| `basic/python-ci.yml` | Testing + linting | Python 3.9-3.12 |
| `basic/go-ci.yml` | Build + test | Go 1.21+ |
| `basic/java-ci.yml` | Maven/Gradle builds | Java 17+, Kotlin |

### Docker Workflows

| Template | Use Case | Features |
|----------|----------|----------|
| `docker/docker-build-push.yml` | Standard container builds | Layer caching, multi-stage |
| `docker/docker-multi-arch.yml` | Cross-platform builds | amd64, arm64, arm/v7 |
| `docker/docker-scan.yml` | Container security | Trivy scanning |

### Kubernetes Workflows

| Template | Use Case | Platforms |
|----------|----------|-----------|
| `kubernetes/k8s-deploy.yml` | Standard K8s deployment | Generic K8s |
| `kubernetes/k8s-approval-workflow.yml` | Production deployments | Manual approval required |
| `kubernetes/k8s-multi-env.yml` | Multi-environment | Dev, staging, production |

### Monorepo Workflows

| Template | Tool | Features |
|----------|------|----------|
| `monorepo/monorepo-path-filter.yml` | Path filtering | Run on affected paths |
| `monorepo/monorepo-turbo.yml` | Turborepo | Remote caching, pipeline |
| `monorepo/monorepo-nx.yml` | Nx | Affected graph, caching |

### Scheduled Workflows

| Template | Schedule | Purpose |
|----------|----------|---------|
| `scheduled/daily-security-scan.yml` | Daily (00:00) | Security vulnerability checks |
| `scheduled/weekly-dependency-update.yml` | Weekly (Sun 00:00) | Dependency updates |
| `scheduled/monthly-report.yml` | Monthly (1st) | Generate metrics reports |

### Security Workflows

| Template | Scanning Type | Coverage |
|----------|---------------|----------|
| `security/codeql-analysis.yml` | Static analysis | Security + quality bugs |
| `security/dependency-review.yml` | Dependencies | Supply chain security |
| `security/trivy-scan.yml` | Container + FS | Vulnerabilities, secrets |

### Advanced Patterns

| Template | Pattern | Use Case |
|----------|---------|----------|
| `advanced/matrix-build.yml` | Matrix strategy | Test on multiple OS/versions |
| `advanced/performance-test.yml` | Performance | Load testing, benchmarks |
| `advanced/release-workflow.yml` | Release automation | Versioning, changelog |
| `advanced/cache-optimization.yml` | Caching strategies | Maximum speed |

## Examples

### Example 1: Node.js API with Docker + K8s Deployment

**Scenario:** Full-stack Node.js API deploying to EKS

**Workflow components needed:**
1. `basic/nodejs-ci.yml` - Testing
2. `docker/docker-build-push.yml` - Container builds
3. `kubernetes/k8s-deploy.yml` - EKS deployment

**Implementation:**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    uses: ./.github/workflows/basic/nodejs-ci.yml

  build:
    needs: test
    uses: ./.github/workflows/docker/docker-build-push.yml
    with:
      push: true
      tags: |
        ghcr.io/${{ github.repository }}:${{ github.sha }}
        ghcr.io/${{ github.repository }}:latest

  deploy:
    needs: build
    uses: ./.github/workflows/kubernetes/k8s-deploy.yml
    with:
      environment: production
      cluster: my-eks-cluster
    secrets: inherit
```

### Example 2: Monorepo with Nx + Staged Deployments

**Scenario:** Nx monorepo with 20 packages, selective deployment

**Workflow:**
```yaml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: nrwl/nx-set-shas@v4
      - run: npx nx affected --base=$NX_BASE --head=$NX_HEAD --graph=graph.json
      - uses: actions/upload-artifact@v4
        with:
          name: affected-graph
          path: graph.json

  build:
    needs: affected
    uses: ./.github/workflows/monorepo/monorepo-nx.yml
    with:
      target: build
      affected-only: true

  test:
    needs: affected
    uses: ./.github/workflows/monorepo/monorepo-nx.yml
    with:
      target: test
      affected-only: true

  deploy:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    uses: ./.github/workflows/monorepo/monorepo-nx.yml
    with:
      target: deploy
      affected-only: true
```

### Example 3: Python ML Pipeline with Scheduled Training

**Scenario:** ML model training + API deployment

**Workflows:**
1. `basic/python-ci.yml` - CI (on PR)
2. `scheduled/monthly-report.yml` - Training job
3. `docker/docker-build-push.yml` - Model serving
4. `kubernetes/k8s-deploy.yml` - Deployment

**Scheduled training:**
```yaml
# .github/workflows/train-model.yml
name: Train ML Model

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly
  workflow_dispatch:

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements-training.txt
          pip install awscli

      - name: Download training data
        run: aws s3 sync s3://training-data /data

      - name: Train model
        run: python scripts/train.py --output /model

      - name: Upload model
        run: aws s3 cp /model/model.pkl s3://models/${{ github.run_number }}.pkl

      - name: Deploy to production
        if: success()
        run: kubectl set image deployment/ml-api app=ghcr.io/myorg/api:${{ github.run_number }}
```

### Example 4: Security-First Pipeline

**Scenario:** Finance project requiring comprehensive security checks

**Workflow:**
```yaml
name: Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily security scan

jobs:
  # Static analysis
  codeql:
    uses: ./.github/workflows/security/codeql-analysis.yml

  # Dependency review
  dependency-review:
    uses: ./.github/workflows/security/dependency-review.yml

  # Secret scanning
  trivy:
    uses: ./.github/workflows/security/trivy-scan.yml
    with:
      scan-type: 'fs'
      scan-ref: '.'
      exit-code: '1'

  # Container scan (if building Docker)
  docker-scan:
    if: github.event_name == 'push'
    uses: ./.github/workflows/docker/docker-scan.yml
    with:
      image: ghcr.io/${{ github.repository }}:${{ github.sha }}

  # Deploy only if all security checks pass
  deploy:
    needs: [codeql, dependency-review, trivy, docker-scan]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying to production"
```

### Example 5: Multi-Environment Release with Approval

**Scenario:** Production deployment requires manual approval

**Workflow:**
```yaml
name: Release Pipeline

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    uses: ./.github/workflows/docker/docker-build-push.yml
    with:
      tags: |
        ghcr.io/${{ github.repository }}:${{ github.ref_name }}
        ghcr.io/${{ github.repository }}:latest

  deploy-staging:
    needs: build
    uses: ./.github/workflows/kubernetes/k8s-deploy.yml
    with:
      environment: staging
    secrets: inherit

  deploy-production:
    needs: deploy-staging
    uses: ./.github/workflows/kubernetes/k8s-approval-workflow.yml
    with:
      environment: production
      approvers: ['@devops-team', '@tech-lead']
    secrets: inherit
```

## Best Practices

### Security

**Always follow security best practices:**

1. **Principle of least privilege:**
   ```yaml
   permissions:
     contents: read      # Minimum required
     issues: read        # Only if needed
     pull-requests: write  # Only if commenting
   ```

2. **Never hardcode secrets:**
   ```yaml
   # BAD
   env:
     AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE

   # GOOD
   env:
     AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
   ```

3. **Use pinned action versions:**
   ```yaml
   # BAD
   - uses: actions/checkout@main

   # GOOD
   - uses: actions/checkout@v4
   ```

4. **Enable dependency reviews:**
   ```yaml
   - uses: actions/dependency-review-action@v4
   ```

5. **Scan containers:**
   ```yaml
   - uses: aquasecurity/trivy-action@master
   ```

### Performance

**Optimize workflow speed:**

1. **Aggressive caching:**
   ```yaml
   - name: Cache node modules
     uses: actions/cache@v4
     with:
       path: |
         ~/.npm
         node_modules
       key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
       restore-keys: |
         ${{ runner.os }}-node-
   ```

2. **Parallelize independent jobs:**
   ```yaml
   jobs:
     lint:
       runs-on: ubuntu-latest
     test:
       runs-on: ubuntu-latest
     build:
       needs: [lint, test]  # Runs after both complete
   ```

3. **Use matrix strategy wisely:**
   ```yaml
   strategy:
     matrix:
       node: [16, 18, 20]
       os: [ubuntu-latest, windows-latest]
     fail-fast: false  # Don't cancel all if one fails
   ```

4. **Docker layer caching:**
   ```yaml
   - uses: docker/build-push-action@v5
     with:
       cache-from: type=gha
       cache-to: type=gha,mode=max
   ```

### Maintainability

**Keep workflows maintainable:**

1. **Use reusable workflows:**
   ```yaml
   # .github/workflows/reusable-test.yml
   on:
     workflow_call:
       inputs:
         node-version:
           required: true
           type: string

   # .github/workflows/ci.yml
   jobs:
     test:
       uses: ./.github/workflows/reusable-test.yml
       with:
         node-version: '20'
   ```

2. **Composite actions for common logic:**
   ```yaml
   # .github/actions/setup-build/action.yml
   name: 'Setup Build Environment'
   runs:
     using: 'composite'
     steps:
       - uses: actions/setup-node@v4
       - run: npm ci
         shell: bash
   ```

3. **Local action references:**
   ```yaml
   - uses: ./.github/actions/setup-build
   ```

4. **Document complex workflows:**
   ```yaml
   # This job deploys to production and requires manual approval
   # It only runs on the main branch after all tests pass
   deploy-production:
     if: github.ref == 'refs/heads/main'
     # ... rest of job
   ```

### Cost Optimization

**Reduce Actions minutes usage:**

1. **Conditional job execution:**
   ```yaml
   expensive-job:
     if: github.event_name == 'push' && github.ref == 'refs/heads/main'
   ```

2. **Skip CI on documentation changes:**
   ```yaml
   on:
     push:
       paths-ignore:
         - '**.md'
         - 'docs/**'
   ```

3. **Use self-hosted runners for heavy workloads**
4. **Optimize caching to reduce install time**
5. **Cancel in-flight runs on new commits:**
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```

## Common Issues

### Issue: "Permission denied" when pushing to registry

**Cause:** Insufficient permissions

**Solution:**
```yaml
permissions:
  contents: read
  packages: write  # Add this

- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Issue: Cache not restoring

**Cause:** Cache key mismatch

**Solution:**
```yaml
# Use restore-keys for partial matches
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

### Issue: Matrix job fails but others continue

**Cause:** fail-fast default is true

**Solution:**
```yaml
strategy:
  matrix:
    node: [16, 18, 20]
  fail-fast: false  # Let all matrix jobs complete
```

### Issue: Workflow not triggering

**Cause:** Path filters or branch rules

**Solution:**
```yaml
on:
  push:
    branches:
      - 'main'  # Not '**/main' or '/main'
    paths:
      - 'src/**'  # Path is relative to repo root
```

### Issue: Secret not available in reusable workflow

**Cause:** Reusable workflows don't inherit secrets

**Solution:**
```yaml
jobs:
  call-workflow:
    uses: org/repo/.github/workflows/reusable.yml@main
    secrets: inherit  # Explicitly inherit all secrets
```

### Issue: Docker build timeout

**Cause:** Build taking too long

**Solution:**
```yaml
- uses: docker/build-push-action@v5
  with:
    push: true
    timeout: 3600000  # 1 hour in milliseconds
```

### Issue: kubectl fails to connect

**Cause:** Kubeconfig not set up correctly

**Solution:**
```yaml
- name: Configure kubectl
  uses: azure/k8s-set-context@v4
  with:
    method: kubeconfig
    kubeconfig: ${{ secrets.KUBE_CONFIG }}

- name: Verify connection
  run: kubectl get nodes
```

### Issue: Monorepo builds unnecessary packages

**Cause:** No change detection

**Solution:**
```yaml
- name: Detect changes
  uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      backend:
        - 'backend/**'
      frontend:
        - 'frontend/**'

jobs:
  build-backend:
    if: steps.filter.outputs.backend == 'true'
```

## Advanced Topics

### Complex Workflow Orchestration

**Chain multiple workflows:**

```yaml
# workflow-a.yml
on:
  workflow_run:
    workflows: ['Workflow B']
    types:
      - completed

jobs:
  on-success:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Workflow B succeeded, running A"
```

### Dynamic Matrix Generation

**Generate matrix from configuration:**

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          echo "matrix={\"include\":[{\"project\":\"a\",\"config\":\"debug\"},{\"project\":\"b\",\"config\":\"release\"}]}" >> $GITHUB_OUTPUT

  build:
    needs: setup
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJson(needs.setup.outputs.matrix) }}
    steps:
      - run: echo "Building ${{ matrix.project }} with ${{ matrix.config }}"
```

### Conditional Artifacts

**Upload artifacts only on failure:**

```yaml
- name: Run tests
  id: tests
  continue-on-error: true
  run: npm test

- name: Upload test results
  if: failure() || steps.tests.outcome == 'failure'
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results/
```

### Manual Inputs

**Accept user input for workflow dispatch:**

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - production
      version:
        description: 'Version to deploy'
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ github.event.inputs.version }} to ${{ github.event.inputs.environment }}"
```

### Environment Protection Rules

**Require approval for production:**

```yaml
deploy-prod:
  environment:
    name: production
    url: https://prod.example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy
      run: |
        # This will pause and require approval
        kubectl apply -f k8s/production/
```

**Configure in repo settings:**
Settings → Environments → New Environment → Add protection rules:
- Required reviewers: @tech-lead, @devops-team
- Wait timer: 30 minutes
- Deployment branches: Only main

## Integration with Other Tools

### AWS Integration

**Deploy to ECS:**
```yaml
- name: Deploy to ECS
  uses: aws-actions/amazon-ecs-deploy-task-definition@v2
  with:
    task-definition: task-definition.json
    service: my-service
    cluster: my-cluster
    wait-for-service-stability: true
```

**Deploy to Lambda:**
```yaml
- name: Deploy Lambda
  uses: appleboy/lambda-action@v1
  with:
    aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws_region: us-east-1
    function_name: my-function
    zip_file: function.zip
```

### Azure Integration

**Deploy to AKS:**
```yaml
- name: Deploy to AKS
  uses: azure/k8s-deploy@v5
  with:
    manifests: |
      k8s/deployment.yml
      k8s/service.yml
    images: |
      ghcr.io/${{ github.repository }}:${{ github.sha }}
    kubeconfig: ${{ secrets.KUBE_CONFIG }}
```

### GCP Integration

**Deploy to Cloud Run:**
```yaml
- name: Deploy to Cloud Run
  uses: google-github-actions/deploy-cloudrun@v2
  with:
    service: my-service
    region: us-central1
    source: .
```

### Slack Notifications

**Send build status:**
```yaml
- name: Slack Notification
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Build ${{ job.status }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Troubleshooting

### Enable debug logging

**Add secrets to repo:**
```
ACTIONS_STEP_DEBUG = true
ACTIONS_RUNNER_DEBUG = true
```

**Re-run with debug:**
Actions tab → Select workflow run → Re-run jobs → Enable debug logging

### Common error codes

| Error | Cause | Solution |
|-------|-------|----------|
| `Resource not accessible` | Insufficient permissions | Add `permissions: contents: write` |
| `Cache not found` | No cache hit expected | Add `restore-keys` for fallback |
| `Job cancelled` | Concurrency group set | Adjust `concurrency` settings |
| `Container not found` | Wrong image tag | Check `{{ github.sha }}` vs `latest` |
| `Context deadline exceeded` | Network timeout | Increase `timeout-minutes` |

### Workflow visualization

**Use act to test locally:**
```bash
# Install act
brew install act

# Dry-run workflow
act -n

# Run specific job
act -j test

# Use specific secrets file
act --secret-file .secrets
```

## Additional Resources

### Official Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Contexts](https://docs.github.com/en/actions/reference/context-and-expression-syntax-for-github-actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

### Templates & Examples

- [GitHub Actions Starter Workflows](https://github.com/actions/starter-workflows)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)

### Reference Documentation

For in-depth technical guidance, see:
- `references/caching-strategies.md` - Advanced caching patterns
- `references/security-hardening.md` - Security best practices
- `references/performance-optimization.md` - Performance tuning
- `references/troubleshooting.md` - Detailed troubleshooting guide

### Helper Scripts

Located in `scripts/` directory:
- `detect-project.sh` - Auto-detect project type
- `generate-workflow.sh` - Generate custom workflows
- `validate-yaml.sh` - Validate workflow YAML

### Example Workflows

Complete examples in `assets/examples/`:
- `nodejs-full-cicd.yml` - Complete Node.js pipeline
- `python-ml-pipeline.yml` - ML training pipeline
- `go-microservice.yml` - Go microservice deployment
- `java-spring-boot.yml` - Spring Boot CI/CD
- `monorepo-nextjs.yml` - Next.js monorepo
- `eks-production.yml` - Production EKS deployment

## Trigger Phrases

Use any of these phrases to activate this skill:

- "Create GitHub Actions workflow for [project type]"
- "Set up CI/CD pipeline"
- "Add automated testing to my repo"
- "Configure Docker builds with GitHub Actions"
- "Deploy to Kubernetes with GitHub Actions"
- "Set up security scanning"
- "Optimize my GitHub Actions workflows"
- "Create monorepo CI/CD"
- "Add scheduled jobs to my repo"
- "Generate workflow template"
