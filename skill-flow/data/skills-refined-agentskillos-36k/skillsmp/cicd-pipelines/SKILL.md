---
name: CI/CD Pipelines
description: This skill should be used when the user asks to "create CI/CD pipeline", "configure GitHub Actions", "set up GitLab CI", "Jenkins pipeline", "continuous integration", "continuous deployment", "automated testing", "preview deployments", "release automation", "build pipeline", or needs help with CI/CD configuration and automation.
version: 1.0.0
---

# CI/CD Pipelines

Comprehensive guidance for implementing continuous integration and continuous deployment pipelines.

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

### Matrix Builds

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        run: ./deploy.sh ${{ inputs.environment }}
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

```yaml
# Calling workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets:
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

## GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: node:20
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm test
    - npm run lint
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  only:
    - develop

deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  when: manual
  only:
    - main
```

## Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'npm ci'
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                    publishHTML([
                        reportDir: 'coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'kubectl apply -f k8s/staging/'
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh 'kubectl apply -f k8s/production/'
            }
        }
    }

    post {
        failure {
            slackSend channel: '#deployments',
                      message: "Pipeline failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        success {
            slackSend channel: '#deployments',
                      message: "Pipeline succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
    }
}
```

## Preview Deployments

### Vercel Preview

```yaml
# Automatic with Vercel GitHub integration
# Or manual:
- name: Deploy Preview
  run: vercel --token=${{ secrets.VERCEL_TOKEN }}
  env:
    VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
    VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

### Kubernetes Preview Environments

```yaml
- name: Create Preview Environment
  run: |
    NAMESPACE="preview-pr-${{ github.event.pull_request.number }}"
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

    helm upgrade --install preview-${{ github.event.pull_request.number }} ./chart \
      --namespace $NAMESPACE \
      --set image.tag=${{ github.sha }} \
      --set ingress.host=pr-${{ github.event.pull_request.number }}.preview.example.com
```

## Testing Strategies

### Unit Tests

```yaml
- name: Unit Tests
  run: npm test -- --coverage --ci
- uses: codecov/codecov-action@v4
```

### Integration Tests

```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: postgres
    ports:
      - 5432:5432

steps:
  - name: Integration Tests
    run: npm run test:integration
    env:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
```

### E2E Tests

```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: E2E Tests
  run: npm run test:e2e

- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
```

## Security Scanning

```yaml
- name: Security Scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: '${{ env.IMAGE_NAME }}:${{ github.sha }}'
    format: 'table'
    exit-code: '1'
    severity: 'CRITICAL,HIGH'

- name: SAST Scan
  uses: github/codeql-action/analyze@v3
```

## Secrets Management

```yaml
# Using GitHub Secrets
env:
  API_KEY: ${{ secrets.API_KEY }}

# Using external secrets manager
- name: Get Secrets
  uses: aws-actions/aws-secretsmanager-get-secrets@v2
  with:
    secret-ids: |
      prod/api-key
```

## Notifications

```yaml
- name: Slack Notification
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Deployment to ${{ inputs.environment }} completed"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Pipeline Best Practices

### Speed Optimization

- Cache dependencies aggressively
- Run jobs in parallel where possible
- Use matrix builds efficiently
- Skip unnecessary steps with conditionals
- Use shallow clones for large repos

### Reliability

- Implement retries for flaky steps
- Use timeouts to prevent hanging jobs
- Add proper error handling
- Implement rollback mechanisms
- Monitor pipeline metrics

### Security

- Use minimal permissions
- Scan for vulnerabilities
- Protect deployment branches
- Require approvals for production
- Rotate secrets regularly

## Additional Resources

### Reference Files

- **`references/github-actions-patterns.md`** - Advanced GitHub Actions patterns
- **`references/pipeline-optimization.md`** - Performance optimization guide

### Example Files

- **`examples/full-ci-cd.yml`** - Complete CI/CD workflow
- **`examples/monorepo-pipeline.yml`** - Monorepo pipeline configuration
