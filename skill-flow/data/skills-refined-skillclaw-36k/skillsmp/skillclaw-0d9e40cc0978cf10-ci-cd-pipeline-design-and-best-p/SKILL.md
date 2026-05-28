---
name: ci-cd-pipeline-design-and-best-practices
description: Use this skill when designing and implementing CI/CD pipelines to automate testing, building, and deployment processes while adhering to industry best practices.
---

# Skill body

## Purpose
Design robust CI/CD pipelines that automate building, testing, and deploying applications with quality gates and deployment strategies.

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
1. **Define Pipeline Stages**: Identify the stages of your pipeline (build, test, deploy).
2. **Configure Triggers**: Set up triggers for pipeline execution (e.g., on push, pull request).
3. **Add Quality Gates**: Ensure tests must pass and coverage meets a specified threshold (e.g., >80%).
4. **Implement Deployment Strategies**: Choose and configure deployment strategies based on your needs.
5. **Add Notifications and Monitoring**: Set up alerts for pipeline status and performance.

## Example CI/CD Pipeline Configuration
```yaml
# .github/workflows/ci-cd.yml
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

## Best Practices
- ✅ Automate everything that can be automated.
- ✅ Fail fast with quick feedback loops.
- ✅ Use caching to speed up builds.
- ✅ Separate build and deploy stages.
- ✅ Require code review before merging.
- ❌ Avoid skipping tests to deploy faster.
- ❌ Avoid deploying without quality gates.

## Additional Considerations
- **Security**: Integrate security checks into your pipeline (e.g., SAST, DAST).
- **Parallelization**: Run tests in parallel to reduce overall pipeline execution time.
- **Rollback Plans**: Always have a rollback strategy in place for deployments.