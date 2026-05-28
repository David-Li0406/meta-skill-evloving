---
name: github-actions-ci-cd
description: Use this skill to create and maintain GitHub Actions workflows for continuous integration and deployment, including testing, building, and automating releases.
---

# Skill Body

## When to Use This Skill

Activate this skill when:
- Setting up CI/CD pipelines
- Automating tests and builds
- Configuring deployment workflows
- Creating release automation
- Running scheduled jobs
- Automating dependency updates
- Setting up code quality checks

## Quick Start Workflow

Create `.github/workflows/ci.yml`:

```yaml
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

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Workflow Structure

```
.github/
└── workflows/
    ├── ci.yml              # Continuous Integration
    ├── deploy.yml          # Deployment
    ├── release.yml         # Release automation
    └── cron-jobs.yml       # Scheduled tasks
```

## Common Triggers

```yaml
# Every push and PR
on: [push, pull_request]

# Specific branches
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Manual trigger
on: workflow_dispatch

# Scheduled (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
```

## Multi-Environment Testing

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: ['14', '16', '18']

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test
```

## Deployment Workflow Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: ./deploy.sh
```