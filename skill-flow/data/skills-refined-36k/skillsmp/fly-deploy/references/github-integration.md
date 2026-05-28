# GitHub Integration

## GitHub Actions for Continuous Deployment

### Prerequisites

1. **Fly API Token:**
```bash
# Generate token
fly tokens create deploy

# Or use personal access token
fly auth token
```

2. **Add token to GitHub Secrets:**
- Go to your repository on GitHub
- Settings → Secrets and variables → Actions
- New repository secret: `FLY_API_TOKEN`
- Paste your token

### Basic Deployment Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to fly.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest

    # Ensure only one deployment runs at a time
    concurrency:
      group: ${{ github.ref }}
      cancel-in-progress: false

    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Workflow with Build Arguments

For apps that need build-time environment variables:

```yaml
name: Deploy to fly.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: |
          flyctl deploy --remote-only \
            --build-arg NEXT_PUBLIC_API_URL=${{ secrets.NEXT_PUBLIC_API_URL }}
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Multi-Environment Deployment

Deploy to different apps based on branch:

```yaml
name: Deploy

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - name: Deploy to Production
        if: github.ref == 'refs/heads/main'
        run: flyctl deploy --remote-only --app my-app-production
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

      - name: Deploy to Staging
        if: github.ref == 'refs/heads/staging'
        run: flyctl deploy --remote-only --app my-app-staging
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Workflow with Tests

Run tests before deploying:

```yaml
name: Test and Deploy

on:
  push:
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

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    concurrency:
      group: deploy-production
      cancel-in-progress: false

    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Manual Deployment Workflow

Add manual trigger option:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # Enable manual triggers
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - name: Set app name
        id: app
        run: |
          if [ "${{ github.event.inputs.environment }}" == "production" ]; then
            echo "name=my-app-production" >> $GITHUB_OUTPUT
          else
            echo "name=my-app-staging" >> $GITHUB_OUTPUT
          fi

      - run: flyctl deploy --remote-only --app ${{ steps.app.outputs.name }}
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## Review Apps (PR Preview Environments)

Review apps create temporary deployments for each pull request.

### Official fly-pr-review-apps Action

**See:** `assets/workflows/review-apps.yml` for complete template.

Create `.github/workflows/review-apps.yml`:

```yaml
name: Review Apps

on:
  pull_request:
    types: [opened, reopened, synchronize, closed]

env:
  FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
  FLY_REGION: ord
  FLY_ORG: personal

jobs:
  review-app:
    runs-on: ubuntu-latest

    # Only run for PRs from the same repository (not forks)
    if: github.event.pull_request.head.repo.full_name == github.repository

    steps:
      - uses: actions/checkout@v4

      - name: Deploy review app
        uses: superfly/fly-pr-review-apps@1.2.0
        with:
          region: ord
          org: personal
          secrets: |
            DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }}
            API_KEY=${{ secrets.STAGING_API_KEY }}
```

### How Review Apps Work

1. **PR opened** → New fly.io app created: `pr-{number}-{org}-{repo}`
2. **Commits pushed** → App automatically updated
3. **PR closed** → App automatically destroyed

### Review App URL

Apps are available at:
```
https://pr-{number}-{org}-{repo}.fly.dev
```

The action automatically comments on the PR with the URL.

### Custom Review App Configuration

**With custom fly.toml:**

```yaml
- uses: superfly/fly-pr-review-apps@1.2.0
  with:
    region: ord
    org: personal
    config: fly.review.toml  # Use custom config
    secrets: |
      DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }}
```

**With database per review app:**

```yaml
- uses: superfly/fly-pr-review-apps@1.2.0
  with:
    region: ord
    org: personal
    postgres: true  # Create postgres instance per PR
```

**Important:** This creates a new Postgres instance for each PR, which can get expensive.

**Better approach:** Share staging database:

```yaml
- uses: superfly/fly-pr-review-apps@1.2.0
  with:
    region: ord
    org: personal
    secrets: |
      DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }}
```

### Review App fly.toml

Create `fly.review.toml` optimized for review apps:

```toml
# Use environment variable for app name (set by action)
app = "${FLY_APP_NAME}"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "staging"
  LOG_LEVEL = "debug"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero to save costs

[[vm]]
  memory = "256mb"  # Minimal resources for review apps
  cpus = 1
```

Update action:
```yaml
- uses: superfly/fly-pr-review-apps@1.2.0
  with:
    config: fly.review.toml
```

### Filtering Which PRs Get Review Apps

**Only for specific labels:**

```yaml
jobs:
  review-app:
    runs-on: ubuntu-latest
    if: |
      github.event.pull_request.head.repo.full_name == github.repository &&
      contains(github.event.pull_request.labels.*.name, 'deploy-preview')

    steps:
      # ... deployment steps
```

**Exclude draft PRs:**

```yaml
if: |
  github.event.pull_request.head.repo.full_name == github.repository &&
  github.event.pull_request.draft == false
```

### Managing Review App Resources

**Set resource limits:**

```yaml
- uses: superfly/fly-pr-review-apps@1.2.0
  with:
    vm-size: shared-cpu-1x
    vm-memory: 256
```

**Auto-destroy after inactivity:**

The action automatically destroys apps when PRs are closed. For additional cleanup:

```bash
# List all review apps
fly apps list | grep "pr-"

# Destroy old review apps manually
fly apps destroy pr-123-org-repo
```

---

## Advanced GitHub Actions Patterns

### Notify Slack on Deployment

```yaml
- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Deployed to production: ${{ github.sha }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Run Migrations in Workflow

```yaml
- name: Run migrations
  run: |
    flyctl ssh console --command "npm run migrate"
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Deploy Multiple Apps from Monorepo

```yaml
jobs:
  deploy-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --config apps/api/fly.toml
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

  deploy-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --config apps/web/fly.toml
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Cache Docker Layers

Speed up builds with Docker layer caching:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-

- run: |
    flyctl deploy --remote-only \
      --build-arg BUILDKIT_INLINE_CACHE=1
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## Security Best Practices

### 1. Use Secrets for Tokens

Never hardcode tokens in workflows:

**❌ Bad:**
```yaml
env:
  FLY_API_TOKEN: fly_abc123...  # Never do this
```

**✅ Good:**
```yaml
env:
  FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### 2. Limit Token Permissions

Create deploy-only tokens:

```bash
# Create token with limited scope
fly tokens create deploy -x 999999h
```

Use different tokens for different apps:
- `FLY_API_TOKEN_STAGING` for staging
- `FLY_API_TOKEN_PRODUCTION` for production

### 3. Protect Branches

- Require PR reviews before merging to main
- Enable status checks (tests must pass)
- Restrict who can push to main

### 4. Review App Security

**Don't use production secrets:**

```yaml
# ❌ Bad: Using production secrets
secrets: |
  DATABASE_URL=${{ secrets.PROD_DATABASE_URL }}

# ✅ Good: Using staging/test secrets
secrets: |
  DATABASE_URL=${{ secrets.STAGING_DATABASE_URL }}
```

**Block forked PRs:**

```yaml
if: github.event.pull_request.head.repo.full_name == github.repository
```

This prevents attackers from creating PRs that access your secrets.

---

## Troubleshooting

### Deployment Fails in CI but Works Locally

**Check flyctl version:**
```yaml
- run: flyctl version
```

Ensure CI uses same version as local.

**Check secrets are set:**
```yaml
- run: |
    if [ -z "$FLY_API_TOKEN" ]; then
      echo "FLY_API_TOKEN is not set"
      exit 1
    fi
```

### Review App Not Created

**Check if PR is from fork:**
Review apps don't run for forked PRs by default (security).

**Check workflow trigger:**
```yaml
on:
  pull_request:
    types: [opened, reopened, synchronize, closed]
```

**Check action logs** for specific error messages.

### Concurrent Deployments Conflict

Use concurrency groups:

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

This ensures only one deployment per branch at a time.

---

## Example Templates

Complete workflow templates are available in:
- `assets/workflows/deploy.yml` - Basic deployment
- `assets/workflows/review-apps.yml` - PR review apps
- `assets/workflows/test-and-deploy.yml` - Testing + deployment

Copy these templates and customize for your app.
