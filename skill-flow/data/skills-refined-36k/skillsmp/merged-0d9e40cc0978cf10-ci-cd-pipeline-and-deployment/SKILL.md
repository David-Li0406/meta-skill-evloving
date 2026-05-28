---
name: ci-cd-pipeline-and-deployment
description: Use this skill to design, implement, and optimize CI/CD pipelines and deployment strategies for applications.
---

# CI/CD Pipeline and Deployment

## Purpose
Design and implement continuous integration and deployment pipelines that automate building, testing, and deploying applications with quality gates and deployment strategies.

## When to Use
- Setting up new projects
- Automating deployment processes
- Implementing quality gates
- Configuring automated testing

## Key Capabilities
1. **Pipeline Design** - Structure multi-stage build/test/deploy workflows.
2. **Quality Gates** - Implement automated testing and code quality checks.
3. **Deployment Strategies** - Utilize blue-green, canary, and rolling deployments.

## Approach
1. Define pipeline stages (build, test, deploy).
2. Configure triggers (push, PR, schedule).
3. Add quality gates (tests must pass, coverage >80%).
4. Implement deployment strategies.
5. Add notifications and monitoring.

## CI/CD Platform Configuration

### Configuration Files
**Location**: Customize based on your CI/CD platform (e.g., `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`).

### Pipeline Stages
A typical CI/CD pipeline includes these stages:
```
Build -> Test -> Security -> Deploy (Staging) -> Deploy (Production)
```

### Trigger Events
- Push to main/develop
- Pull requests
- Merge requests

## Deployment Strategies

### Blue-Green Deployment
Maintain two identical environments to ensure zero-downtime deployments and easy rollback.

### Canary Deployment
Gradually roll out to a subset of users, monitoring metrics before full deployment.

### Rolling Deployment
Update instances incrementally, ensuring health checks determine rollout pace.

## Testing Strategies

### Test Pyramid
Focus on unit tests (many), integration tests (some), and end-to-end tests (few).

### Flaky Test Handling
Implement retry logic for flaky tests and quarantine them for investigation.

## Security in CI/CD

### Secrets Management
Utilize CI/CD secret variables to manage sensitive information securely.

### Dependency Security
Regularly scan for vulnerabilities in dependencies and implement security checks in the pipeline.

## Monitoring and Observability

### Pipeline Metrics
Track lead time, deployment frequency, change failure rate, and mean time to recovery.

### Health Checks
Implement readiness and liveness probes, along with smoke tests post-deployment.

## Rollback Strategies
Define automatic and manual rollback procedures to revert to previous stable states.

## Documentation
Maintain clear documentation of pipeline stages, required environment variables, and deployment procedures.

## Continuous Improvement
Regularly review pipeline performance, security assessments, and process improvements.

## Best Practices
- Automate everything that can be automated.
- Fail fast with quick feedback loops.
- Build once, deploy many times.
- Maintain security at every stage.

## Example CI/CD Configuration
```yaml
# Example GitHub Actions CI/CD Pipeline
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - run: npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          ./deploy.sh production
```

## Customization
Replace placeholders with project-specific details to tailor the CI/CD pipeline and deployment strategies to your needs.