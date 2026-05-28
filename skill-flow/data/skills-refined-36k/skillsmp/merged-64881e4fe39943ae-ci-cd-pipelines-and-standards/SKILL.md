---
name: ci-cd-pipelines-and-standards
description: Use this skill when you need to create, configure, or understand CI/CD pipelines, including best practices and standards for continuous integration and deployment.
---

# CI/CD Pipelines and Standards

Comprehensive guidance for implementing continuous integration and continuous deployment pipelines that meet industry standards.

## Tooling

> **Available Tools**: If using Claude Code, the `gh:ci-assist` skill can help migrate and configure CI pipelines. Also see `gh:migrate` for CI/CD migration from other platforms.

## Pipeline Trigger Requirements

### When CI MUST Run

CI MUST run on:

- All pull requests to protected branches
- All pushes to protected branches (develop, main)
- Scheduled intervals (daily/weekly for security scans)

### Concurrency Controls (MUST)

CI MUST implement concurrency controls to cancel superseded runs:

```yaml
# GitHub Actions example
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Required Pipeline Jobs

### Job Order (MUST)

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

### All Jobs Must Pass (MUST)

All CI jobs MUST pass before a PR can be merged. Configure branch protection to enforce this.

## CI Configuration Requirements

### Pinned Action Versions (MUST)

CI workflows MUST use pinned action versions. Prefer commit SHAs over tags:

```yaml
# Good - SHA pinned
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0

# Acceptable - tag pinned
- uses: actions/checkout@v4.1.0

# Bad - floating tag
- uses: actions/checkout@v4
```

### Caching (MUST)

CI MUST cache dependencies and build artifacts:

```yaml
# Example: Rust caching
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

### Multi-Platform Testing (MUST)

CI MUST test on all supported operating systems and architectures:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    # Add architecture if cross-compiling
```

## CI Environment Requirements

### Explicit Configuration (MUST)

CI environment variables MUST be explicitly configured (no reliance on runner defaults):

```yaml
env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1
  CI: true
```

### Secrets Management (MUST)

Sensitive values MUST be stored as secrets, never in workflow files:

```yaml
# Good
env:
  API_KEY: ${{ secrets.API_KEY }}

# Bad - never do this
env:
  API_KEY: "sk-abc123..."
```

### Minimal Permissions (MUST)

CI MUST use minimal permissions (principle of least privilege):

```yaml
permissions:
  contents: read
  pull-requests: write # Only if needed
```

## Implementation Checklist

- [ ] Configure CI to run on PRs and protected branch pushes
- [ ] Set up scheduled security scans
- [ ] Implement all required jobs in correct order
- [ ] Pin action versions (preferably SHA)
- [ ] Configure caching for dependencies
- [ ] Set up multi-platform matrix
- [ ] Explicitly configure environment variables
- [ ] Store secrets securely
- [ ] Apply minimal permissions
- [ ] Enable concurrency controls

## CI/CD Pipeline Examples

### GitHub Actions Basic Workflow

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: "0 0 * * *" # Daily security scan

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

env:
  CI: true

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check formatting
        run: make format-check

  lint:
    runs-on: ubuntu-latest
    needs: format
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: make lint-strict

  test:
    runs-on: ${{ matrix.os }}
    needs: lint
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: make test

  security:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Security audit
        run: make audit
```

### GitLab CI/CD Example

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

### Jenkins Pipeline Example

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

## Additional Resources

### Reference Files

- **`references/ci-workflows.md`** - Complete CI workflow templates
- **`references/ci-caching.md`** - Caching strategies by language

### Examples

- **`examples/ci-rust.yml`** - Rust CI workflow
- **`examples/ci-typescript.yml`** - TypeScript CI workflow
- **`examples/ci-python.yml`** - Python CI workflow
- **`examples/ci-java.yml`** - Java CI workflow