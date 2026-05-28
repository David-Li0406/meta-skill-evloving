# GitHub Actions Skill

A comprehensive GitHub Actions workflow generator and template library for Claude Code. This skill provides intelligent project analysis, security-hardened templates, and production-ready CI/CD patterns.

## Features

- **Intelligent Project Detection** - Automatically analyzes your project structure
- **20+ Workflow Templates** - Covering common CI/CD patterns
- **Security-First Design** - All templates follow security best practices
- **Performance Optimized** - Built-in caching and parallelization strategies
- **Production Ready** - Tested patterns for real-world deployments

## Quick Start

### Basic Usage

Simply ask Claude to create a workflow:

```
"Create GitHub Actions workflow for my Node.js API"
"Set up CI/CD for my Python project"
"Add Docker build automation"
```

### Manual Workflow Generation

1. **Detect your project type:**
   ```bash
   bash .claude/skills/github-actions/scripts/detect-project.sh
   ```

2. **Copy a relevant template:**
   ```bash
   cp .claude/skills/github-actions/assets/workflows/basic/nodejs-ci.yml .github/workflows/ci.yml
   ```

3. **Customize for your project:**
   - Update branch names
   - Configure environment variables
   - Add required secrets

4. **Validate the workflow:**
   ```bash
   bash .claude/skills/github-actions/scripts/validate-yaml.sh .github/workflows/ci.yml
   ```

5. **Commit and push:**
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "Add CI workflow"
   git push
   ```

## Available Templates

### Basic CI Workflows
- `nodejs-ci.yml` - Node.js/TypeScript testing and linting
- `python-ci.yml` - Python testing with multiple versions
- `go-ci.yml` - Go build and test pipeline
- `java-ci.yml` - Java/Maven/Gradle builds

### Docker Workflows
- `docker-build-push.yml` - Container builds and registry pushes
- `docker-multi-arch.yml` - Multi-architecture builds (amd64/arm64)
- `docker-scan.yml` - Container security scanning with Trivy

### Kubernetes Workflows
- `k8s-deploy.yml` - Standard K8s deployments
- `k8s-approval-workflow.yml` - Production deployments with manual approval
- `k8s-multi-env.yml` - Multi-environment deployments (dev/staging/prod)

### Monorepo Workflows
- `monorepo-path-filter.yml` - Path-based change detection
- `monorepo-turbo.yml` - Turborepo optimization
- `monorepo-nx.yml` - Nx workspace integration

### Scheduled Workflows
- `daily-security-scan.yml` - Automated security scanning
- `weekly-dependency-update.yml` - Dependency update automation
- `monthly-report.yml` - Monthly report generation

### Security Workflows
- `codeql-analysis.yml` - Static code analysis
- `dependency-review.yml` - Dependency vulnerability scanning
- `trivy-scan.yml` - Container and filesystem scanning

### Advanced Patterns
- `matrix-build.yml` - Multi-version/OS testing
- `performance-test.yml` - Performance and load testing
- `release-workflow.yml` - Automated release management
- `cache-optimization.yml` - Advanced caching strategies

## Directory Structure

```
.github-actions-skill/
├── SKILL.md                          # Main skill documentation
├── plugin.json                       # Plugin metadata
├── README.md                         # This file
├── assets/
│   ├── workflows/                    # Workflow templates
│   │   ├── basic/                    # Language-specific CI
│   │   ├── docker/                   # Docker workflows
│   │   ├── kubernetes/               # K8s deployments
│   │   ├── monorepo/                 # Monorepo patterns
│   │   ├── scheduled/                # Scheduled jobs
│   │   ├── security/                 # Security scanning
│   │   └── advanced/                 # Advanced patterns
│   └── examples/                     # Complete examples
├── scripts/
│   ├── detect-project.sh             # Project type detection
│   ├── generate-workflow.sh          # Workflow generation
│   └── validate-yaml.sh              # YAML validation
└── references/
    ├── caching-strategies.md         # Caching patterns
    ├── security-hardening.md         # Security guidelines
    ├── performance-optimization.md   # Performance tuning
    └── troubleshooting.md            # Troubleshooting guide
```

## Common Workflows

### Node.js API with Docker

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
```

### Python ML Pipeline

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly training

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python train.py
```

### Monorepo with Nx

```yaml
# .github/workflows/monorepo.yml
name: Monorepo CI

on:
  push:
    branches: [main]

jobs:
  affected:
    uses: ./.github/workflows/monorepo/monorepo-nx.yml
    with:
      affected-only: true
```

## Best Practices

### Security

1. **Principle of least privilege**
   ```yaml
   permissions:
     contents: read
   ```

2. **Use pinned action versions**
   ```yaml
   - uses: actions/checkout@v4  # Not @main
   ```

3. **Never hardcode secrets**
   ```yaml
   password: ${{ secrets.MY_SECRET }}
   ```

### Performance

1. **Enable caching**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: ~/.npm
       key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
   ```

2. **Parallelize jobs**
   ```yaml
   jobs:
     lint:
     test:
     build:
       needs: [lint, test]
   ```

3. **Use matrix strategy**
   ```yaml
   strategy:
     matrix:
       node-version: [16, 18, 20]
   ```

## Troubleshooting

### Workflow not triggering

Check branch names and paths:
```yaml
on:
  push:
    branches: [main]  # Must match exactly
```

### Permission denied

Add required permissions:
```yaml
permissions:
  contents: write
  packages: write
```

### Cache not working

Verify cache key format:
```yaml
key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

## Scripts

### detect-project.sh

Analyzes your project and detects:
- Programming language
- Package manager
- Container configuration
- Kubernetes manifests
- Monorepo setup

Usage:
```bash
bash .claude/skills/github-actions/scripts/detect-project.sh
```

### generate-workflow.sh

Generates a custom workflow based on your project.

Usage:
```bash
bash .claude/skills/github-actions/scripts/generate-workflow.sh [options]
```

### validate-yaml.sh

Validates YAML syntax for workflow files.

Usage:
```bash
bash .claude/skills/github-actions/scripts/validate-yaml.sh <workflow-file>
```

## Contributing

To add new templates:

1. Create workflow in `assets/workflows/<category>/`
2. Follow security best practices
3. Add inline comments
4. Update this README
5. Test with `validate-yaml.sh`

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

## Documentation

**Complete Documentation Suite:**

- **[SKILL.md](./SKILL.md)** (1,103 lines) - Complete skill documentation with examples, best practices, and troubleshooting
- **[SUMMARY.md](./SUMMARY.md)** - Quick reference and navigation guide
- **[DELIVERY.md](./DELIVERY.md)** - Final delivery summary with file inventory
- **[TESTING.md](./TESTING.md)** - Comprehensive testing guide with 16 test scenarios
- **[README.md](./README.md)** - This file (quick overview and catalog)

**Reference Documentation:**

- **[references/caching-strategies.md](./references/caching-strategies.md)** - Advanced caching patterns (200+ lines)
- **[references/security-hardening.md](./references/security-hardening.md)** - Security best practices (250+ lines)
- **[references/performance-optimization.md](./references/performance-optimization.md)** - Performance tuning (180+ lines)
- **[references/troubleshooting.md](./references/troubleshooting.md)** - Detailed troubleshooting guide (220+ lines)

**Quick Start:**

```bash
# 1. Analyze your project
bash .claude/skills/github-actions/scripts/detect-project.sh

# 2. Copy recommended workflow
cp .claude/skills/github-actions/assets/workflows/[template].yml .github/workflows/ci.yml

# 3. Customize and deploy
# Edit the workflow for your needs, then:
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
git push
```

## License

MIT License - See LICENSE file for details

---

**Delivery Status:** Complete ✅
**Version:** 1.0.0
**Last Updated:** December 23, 2025
**Total Files:** 37 (22 templates, 3 examples, 3 scripts, 9 docs)
**Total Lines:** 7,800+
