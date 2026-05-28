---
name: ci-workflow
description: Generate GitHub Actions workflows that use devflow CLI for migrations, deployments, and validation
allowed-tools: Bash, Read, Write, Glob
disable-model-invocation: true
argument-hint: [pr-check|deploy-staging|deploy-production|migration-check]
---

# Generate CI/CD Workflow

Create GitHub Actions workflows that leverage devflow CLI for consistent CI/CD operations.

## Usage

- `/devflow-ci-workflow pr-check` - PR validation (lint, test, migration dry-run)
- `/devflow-ci-workflow deploy-staging` - Deploy to staging on merge to main
- `/devflow-ci-workflow deploy-production` - Deploy to production on release tag
- `/devflow-ci-workflow migration-check` - Validate migrations are safe
- `/devflow-ci-workflow full` - Generate all workflows

## Workflow Type

$ARGUMENTS

## Workflow Templates

### PR Check Workflow

**File:** `.github/workflows/pr-check.yml`

```yaml
name: PR Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install devflow
        run: pip install -e .

      - name: Validate configuration
        run: devflow config validate

      - name: Check migration status
        run: devflow db status --env staging --json
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Dry-run migrations
        run: devflow db migrate --env staging --dry-run --json
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests
        run: pytest --cov
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
```

### Deploy Staging Workflow

**File:** `.github/workflows/deploy-staging.yml`

```yaml
name: Deploy Staging

on:
  push:
    branches: [main]

concurrency:
  group: deploy-staging
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install devflow
        run: pip install -e .

      - name: Validate configuration
        run: devflow config validate

      - name: Apply migrations
        run: devflow db migrate --env staging --ci --json
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Deploy to staging
        run: devflow deploy staging --ci --json
        env:
          DOCKER_HOST: ${{ secrets.STAGING_DOCKER_HOST }}
          DOCKER_TLS_VERIFY: 1

      - name: Verify deployment
        run: devflow deploy status --env staging --json
        env:
          DOCKER_HOST: ${{ secrets.STAGING_DOCKER_HOST }}

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Staging deployment failed for ${{ github.repository }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Deploy Production Workflow

**File:** `.github/workflows/deploy-production.yml`

```yaml
name: Deploy Production

on:
  release:
    types: [published]

concurrency:
  group: deploy-production
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install devflow
        run: pip install -e .

      - name: Validate configuration
        run: devflow config validate

      - name: Check migration status
        id: migration-check
        run: |
          STATUS=$(devflow db status --env production --json)
          PENDING=$(echo $STATUS | jq '.pending_count')
          echo "pending=$PENDING" >> $GITHUB_OUTPUT
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}

      - name: Apply migrations
        if: steps.migration-check.outputs.pending > 0
        run: devflow db migrate --env production --ci --json
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}

      - name: Deploy to production
        run: devflow deploy production --ci --json
        env:
          DOCKER_HOST: ${{ secrets.PRODUCTION_DOCKER_HOST }}
          DOCKER_TLS_VERIFY: 1

      - name: Verify deployment
        run: devflow deploy status --env production --json
        env:
          DOCKER_HOST: ${{ secrets.PRODUCTION_DOCKER_HOST }}

      - name: Create deployment record
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: context.sha,
              environment: 'production',
              auto_merge: false,
              required_contexts: []
            });
```

### Migration Check Workflow

**File:** `.github/workflows/migration-check.yml`

```yaml
name: Migration Safety Check

on:
  pull_request:
    paths:
      - 'migrations/**'
      - 'supabase/migrations/**'

jobs:
  check-migrations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install devflow
        run: pip install -e .

      - name: Get changed migrations
        id: changed
        run: |
          MIGRATIONS=$(git diff --name-only origin/main...HEAD -- 'migrations/*.sql' 'supabase/migrations/*.sql')
          echo "files=$MIGRATIONS" >> $GITHUB_OUTPUT

      - name: Analyze migrations for safety
        run: |
          echo "Checking migrations for potentially dangerous operations..."
          for file in ${{ steps.changed.outputs.files }}; do
            echo "Analyzing: $file"

            # Check for destructive operations
            if grep -iE "DROP TABLE|DROP COLUMN|TRUNCATE" "$file"; then
              echo "::warning file=$file::Contains destructive operation"
            fi

            # Check for missing transactions
            if ! grep -iE "BEGIN|START TRANSACTION" "$file"; then
              echo "::notice file=$file::Consider wrapping in transaction"
            fi

            # Check for long-running operations
            if grep -iE "ALTER TABLE.*ADD COLUMN.*NOT NULL" "$file"; then
              echo "::warning file=$file::Adding NOT NULL column may lock table"
            fi
          done

      - name: Dry-run against staging
        run: devflow db migrate --env staging --dry-run --json
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
```

## Generation Workflow

### Step 1: Check Existing Workflows

```bash
ls -la .github/workflows/
```

Identify what already exists to avoid overwriting.

### Step 2: Read Project Configuration

```bash
devflow config show --format yaml
```

Understand:
- Database configuration
- Deployment targets
- Environment names

### Step 3: Generate Requested Workflow

Create the workflow file in `.github/workflows/`.

### Step 4: Identify Required Secrets

List secrets that need to be configured in GitHub:

```
Required GitHub Secrets:
------------------------
STAGING_DATABASE_URL    - PostgreSQL connection string for staging
PRODUCTION_DATABASE_URL - PostgreSQL connection string for production
STAGING_DOCKER_HOST     - Docker host for staging deployment
PRODUCTION_DOCKER_HOST  - Docker host for production deployment
SLACK_WEBHOOK           - (optional) Slack notification webhook
```

### Step 5: Validate Generated Workflow

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/<name>.yml'))"
```

## Customization Points

When generating, ask about:

1. **Branch names**: main vs master, develop branch?
2. **Python version**: 3.10, 3.11, 3.12?
3. **Test framework**: pytest, unittest?
4. **Notification**: Slack, Discord, email?
5. **Environments**: staging only, or staging + production?
6. **Manual approval**: Required for production?
