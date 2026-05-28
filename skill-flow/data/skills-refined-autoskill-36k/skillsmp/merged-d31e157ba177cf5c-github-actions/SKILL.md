---
name: github-actions
description: Use this skill when creating GitHub Actions workflows for CI/CD, including testing, building, publishing npm packages, and automating repository tasks.
---

# GitHub Actions Skill

This skill helps you create and maintain GitHub Actions workflows for continuous integration and deployment.

## When to Use This Skill

- Setting up CI/CD pipelines
- Automating tests and builds
- Configuring deployment workflows
- Creating release automation
- Running scheduled jobs
- Automating dependency updates
- Setting up code quality checks

## Directory Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Continuous integration
│   ├── deploy.yml          # Deployment
│   ├── release.yml         # Release automation
│   └── cron-jobs.yml       # Scheduled tasks
└── dependabot.yml          # Dependency updates
```

## Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npm test
```

## Deployment Workflows

### Deploy to Cloudflare Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: my-project
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

### Deploy to DigitalOcean

```yaml
# .github/workflows/deploy-do.yml
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
      - name: Deploy to App Platform
        run: doctl apps create-deployment ${{ secrets.DO_APP_ID }}
```

## Release Automation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Matrix Testing

Test across multiple Node.js versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

## Caching Dependencies

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

## Secrets Management

### Required Secrets

Set in repository Settings > Secrets and variables > Actions:

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API token with Pages edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |
| `DIGITALOCEAN_ACCESS_TOKEN` | DigitalOcean API token |
| `NODE_AUTH_TOKEN` | NPM token for publishing |

### Using Secrets

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}

# Or per-step
- name: Deploy
  run: ./deploy.sh
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Notifications

### Slack Notifications

```yaml
- name: Notify Slack on success
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "✅ Deployment successful",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Deployment Successful*\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}"
            }
          }
        ]
      }
```

## Best Practices

1. **Use Specific Versions**: Pin action versions to avoid breaking changes.
2. **Cache Dependencies**: Use caching to speed up builds.
3. **Fail Fast**: Use `fail-fast` in matrix strategies to stop on the first failure.
4. **Secrets Management**: Use GitHub Secrets for sensitive data.
5. **Notifications**: Alert team on deployment status.

## Troubleshooting

### Common Issues

- **Command not found**: Ensure all dependencies are installed and in PATH.
- **Permission errors**: Check file permissions and run with appropriate privileges.
- **Unexpected behavior**: Enable verbose logging with `--verbose` flag.

## References

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Workflow Syntax: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- Actions Marketplace: https://github.com/marketplace?type=actions