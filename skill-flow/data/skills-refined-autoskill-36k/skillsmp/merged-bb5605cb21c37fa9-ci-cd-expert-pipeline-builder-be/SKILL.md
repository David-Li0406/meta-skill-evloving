---
name: ci-cd-expert-pipeline-builder-best-practices
description: Use this skill to generate, optimize, and implement CI/CD pipelines across platforms with best practices for automation, security, and deployment strategies.
---

# CI/CD Expert Pipeline Builder Best Practices

This skill provides expert guidance for generating, optimizing, and implementing Continuous Integration and Continuous Deployment (CI/CD) pipelines across platforms like GitHub Actions, Jenkins, and GitLab CI. It includes best practices for automation, security, deployment strategies, and testing.

## Core Concepts

### CI/CD Fundamentals
- Continuous Integration (CI)
- Continuous Delivery vs Deployment
- Build automation
- Test automation
- Artifact management
- Deployment strategies (blue-green, canary, rolling)

### Pipeline Design
A typical CI/CD pipeline includes these stages:
```
Build -> Test -> Security -> Deploy (Staging) -> Deploy (Production)
```

#### 1. Build Stage
```yaml
build:
  stage: build
  script:
    - npm ci --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
```
Best practices:
- Use dependency caching to speed up builds.
- Generate build artifacts for downstream stages.

#### 2. Test Stage
```yaml
test:
  stage: test
  parallel:
    matrix:
      - TEST_TYPE: [unit, integration, e2e]
  script:
    - npm run test:${TEST_TYPE}
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```
Testing layers:
- **Unit tests**: Fast, isolated, run on every commit.
- **Integration tests**: Test component interactions.
- **End-to-end tests**: Validate user workflows.

#### 3. Security Stage
```yaml
security:
  stage: security
  parallel:
    matrix:
      - SCAN_TYPE: [sast, dependency, secrets]
  script:
    - ./security-scan.sh ${SCAN_TYPE}
  allow_failure: false
```
Security scanning types:
- **SAST**: Static Application Security Testing.
- **Dependency scanning**: Check for vulnerable packages.

#### 4. Deploy Stage
```yaml
deploy:staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy.sh staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy:production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - ./deploy.sh production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

## Deployment Strategies

### Blue-Green Deployment
Maintain two identical environments to ensure zero-downtime deployments and easy rollback.

### Canary Deployment
Gradually roll out to a subset of users, monitoring metrics before full deployment.

### Rolling Deployment
Update instances incrementally, ensuring health checks determine rollout pace.

## Best Practices

1. **Automate everything**: Automate all possible processes in the pipeline.
2. **Fail fast**: Implement quick feedback loops to catch issues early.
3. **Security**: Maintain security at every stage, including scanning for vulnerabilities.
4. **Caching**: Use caching strategies to speed up builds and tests.
5. **Monitoring**: Track pipeline metrics to improve performance and reliability.

## Advanced Features

### Multi-Environment Deployments
Implement strategies for deploying to multiple environments (development, staging, production) with appropriate configurations.

### Artifact Management
Store and manage build artifacts effectively, ensuring they are available for future deployments.

### Continuous Improvement
Regularly review pipeline performance and security, and adapt processes based on metrics and feedback.

## Resources
- GitHub Actions: https://docs.github.com/en/actions
- Jenkins: https://www.jenkins.io/doc/
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Argo CD: https://argo-cd.readthedocs.io/
- Tekton: https://tekton.dev/docs/