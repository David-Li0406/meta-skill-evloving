# Workflow: Setup CI/CD Pipeline

## Purpose
Establish automated continuous integration and deployment pipelines that test, build, and deploy code automatically. This workflow creates production-ready CI/CD configurations following DevOps best practices.

## When to Use
- Starting a new project that needs automated testing and deployment
- Adding CI/CD to an existing project
- Migrating from one CI/CD platform to another
- Improving an existing pipeline with better practices

## Prerequisites
- Git repository (GitHub, GitLab, etc.)
- Project with tests (or willingness to add them)
- Target deployment environment identified
- Understanding of deployment requirements

## Workflow Steps

### 1. Analyze Project Requirements

**Gather information:**
- What language/framework is the project using?
- What testing framework is in place?
- Where will the application be deployed? (AWS, GCP, Azure, Heroku, etc.)
- What are the build artifacts? (Docker images, npm packages, binaries)
- What environments exist? (dev, staging, production)
- What deployment strategy is preferred? (rolling, blue-green, canary)

**Ask clarifying questions if unclear:**
- "What cloud platform are you deploying to?"
- "Do you have staging and production environments?"
- "What testing frameworks are you using?"
- "Do you need manual approval gates for production?"

### 2. Select CI/CD Platform

**Based on repository:**
- **GitHub** → GitHub Actions (recommended)
- **GitLab** → GitLab CI
- **Bitbucket** → Bitbucket Pipelines
- **Other** → Jenkins, CircleCI, or cloud-native options

**Load appropriate configuration template:**
- For GitHub Actions: Load `context/configurations/github-actions.md`
- Customize template for project specifics

### 3. Design Pipeline Stages

**Standard multi-stage pipeline:**

```yaml
Stages:
1. Code Quality
   - Linting
   - Code formatting checks
   - Static analysis

2. Testing
   - Unit tests
   - Integration tests
   - E2E tests (if applicable)

3. Security
   - Dependency vulnerability scanning
   - SAST (Static Application Security Testing)
   - Container scanning (if using Docker)

4. Build
   - Compile/build application
   - Create Docker images
   - Version and tag artifacts

5. Deploy
   - Deploy to staging (automatic)
   - Deploy to production (with approval gate)

6. Verify
   - Health checks
   - Smoke tests
   - Monitoring validation
```

### 4. Implement Testing Stage

**Configure parallel test execution:**
```yaml
# Example structure (platform-agnostic)
- Run unit tests with coverage reporting
- Run integration tests against test database
- Run E2E tests with test fixtures
- Fail pipeline if coverage drops below threshold
- Upload test results and coverage reports
```

**Best practices:**
- Use test caching to speed up runs
- Run tests in parallel when possible
- Fail fast on test failures
- Generate coverage reports
- Store test artifacts for debugging

### 5. Implement Security Scanning

**Add security gates:**
```yaml
- Dependency audit (npm audit, pip audit, etc.)
- Container vulnerability scanning (Trivy, Snyk)
- SAST scanning (CodeQL, SonarQube)
- Secret scanning (prevent committed secrets)
- License compliance checking
```

**Security requirements:**
- Block deployment on critical vulnerabilities
- Create issues for medium/low vulnerabilities
- Scan every pull request
- Scan base images regularly

### 6. Implement Build Stage

**For containerized applications:**
```yaml
- Build Docker image with proper tags
- Use multi-stage builds to minimize size
- Scan image for vulnerabilities
- Push to container registry
- Tag with git SHA and version
```

**For non-containerized:**
```yaml
- Build application (npm build, maven package, etc.)
- Run post-build tests
- Create versioned artifacts
- Upload to artifact repository
```

**Best practices:**
- Use build caching effectively
- Version all artifacts (semantic versioning)
- Include git SHA in metadata
- Minimize build time with parallelization

### 7. Implement Deployment Stage

**Staging deployment (automatic):**
```yaml
- Trigger on: merge to main/develop branch
- Deploy to staging environment
- Run smoke tests
- Verify health checks
- Notify team of deployment
```

**Production deployment (gated):**
```yaml
- Trigger on: manual approval or release tag
- Require approval from authorized users
- Deploy using chosen strategy (blue-green, canary, rolling)
- Monitor deployment metrics
- Automated rollback on failure
- Notify stakeholders
```

**Reference deployment strategies:**
- Load `context/patterns/deployment-strategies.md` for strategy details

### 8. Implement Observability

**Add monitoring to pipeline:**
```yaml
- Collect build metrics (duration, success rate)
- Log aggregation for pipeline runs
- Deployment tracking (what, when, who)
- Alert on pipeline failures
- Dashboard for pipeline health
```

**Pipeline monitoring:**
- Track build duration trends
- Monitor success/failure rates
- Alert on repeated failures
- Track deployment frequency

### 9. Optimize for Speed

**Performance optimizations:**
- **Caching**: Cache dependencies, build artifacts, Docker layers
- **Parallelization**: Run independent jobs in parallel
- **Matrix builds**: Test multiple versions concurrently
- **Incremental builds**: Only rebuild changed components
- **Efficient Docker layers**: Order layers by change frequency

**Target metrics:**
- CI feedback in < 10 minutes
- Full pipeline in < 30 minutes
- Parallel job execution where possible

### 10. Document Pipeline

**Create pipeline documentation:**
```markdown
# CI/CD Pipeline Documentation

## Overview
[Brief description of pipeline stages and flow]

## Triggers
- Push to main: Runs full pipeline, deploys to staging
- Pull request: Runs tests and security scans
- Release tag: Deploys to production (requires approval)

## Stages
[Document each stage and what it does]

## Secrets and Configuration
[List required secrets and environment variables]

## Troubleshooting
[Common issues and solutions]

## Emergency Procedures
- Rollback: [How to rollback a deployment]
- Skip CI: [When and how to skip CI (rarely)]
- Manual deployment: [Emergency manual deployment procedure]
```

## Deliverables

**Configuration files created:**
- `.github/workflows/ci.yml` (or equivalent for chosen platform)
- `.dockerignore` (if using Docker)
- `Dockerfile` (if not already present and needed)
- Pipeline documentation in `docs/CI_CD.md`

**Pipeline features:**
- Multi-stage pipeline with parallel execution
- Comprehensive testing (unit, integration, security)
- Security scanning at multiple points
- Automated staging deployment
- Gated production deployment
- Monitoring and alerting
- Fast feedback (< 10 min for basic checks)

## Validation Checklist

Before completing this workflow, verify:
- [ ] Pipeline configuration file is valid (syntax check)
- [ ] All required secrets are documented
- [ ] Tests run successfully in CI
- [ ] Security scans are configured
- [ ] Build stage produces correct artifacts
- [ ] Staging deployment works automatically
- [ ] Production deployment requires approval
- [ ] Health checks validate deployments
- [ ] Rollback procedure is documented
- [ ] Team is notified of pipeline status
- [ ] Pipeline documentation is complete
- [ ] Common troubleshooting scenarios documented

## Common Patterns

**Reference these context files:**
- `context/patterns/ci-cd-patterns.md` - Pipeline patterns and best practices
- `context/configurations/github-actions.md` - GitHub Actions templates
- `context/patterns/deployment-strategies.md` - Deployment approaches

## Troubleshooting

**Pipeline fails on first run:**
- Check secret configuration
- Verify environment variables
- Ensure test database is available
- Check dependency installation

**Tests pass locally but fail in CI:**
- Environment differences (Node version, dependencies)
- Missing environment variables
- Database configuration issues
- Timezone/locale differences

**Build too slow:**
- Implement caching for dependencies
- Parallelize test execution
- Use matrix builds for multi-version testing
- Optimize Docker layer caching

**Security scans block deployment:**
- Review vulnerability severity
- Update dependencies with fixes
- Add exceptions for false positives (with justification)
- Create remediation plan for findings

## Next Steps

After CI/CD setup:
1. Test the pipeline with a pull request
2. Verify staging deployment works
3. Set up monitoring (use `workflows/monitor.md`)
4. Document runbooks for common operations
5. Train team on pipeline usage
6. Establish deployment schedule and practices

## Success Metrics

A successful CI/CD pipeline achieves:
- **Fast feedback**: Basic checks complete in < 10 minutes
- **Comprehensive coverage**: Unit, integration, security tests
- **Automated deployment**: Staging deploys on every merge
- **Safe production**: Gated deployments with approval
- **High reliability**: > 95% success rate
- **Quick recovery**: Rollback in < 5 minutes
