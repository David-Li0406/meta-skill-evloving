---
name: mastering-github-cli
description: Use this skill for GitHub CLI (gh) operations including repository search, code discovery, CI/CD monitoring, workflow authoring, and automation.
---

# Mastering GitHub CLI

Command-line interface for GitHub operations: search, monitoring, resource creation, workflow authoring, and automation.

## Contents

- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Workflow Authoring](#workflow-authoring)
- [Scripts](#scripts)
- [Validation Checklist](#validation-checklist)
- [When Not to Use](#when-not-to-use)

---

## Quick Start

### Find repos with specific files/directories

```bash
gh search code "path:.skilz" --json repository --jq '.[].repository.fullName'
gh search code --filename <filename>
gh search code --filename <filename> --language <language>
```

### Monitor CI/CD

```bash
gh run list --workflow=<workflow_name> --status=failure --limit 10
gh run watch <run_id> --exit-status      # Block until complete
gh run view <run_id> --log-failed        # Failed logs only
gh pr checks <pr_id> --watch              # PR CI status
```

### Create resources

```bash
gh pr create --title "<title>" --body "<description>" --reviewer @user
gh issue create --title "<title>" --label <labels> --assignee @me
gh repo fork <owner>/<repo> --clone
```

### Trigger and monitor workflow

```bash
gh workflow run <workflow_name>.yml -f environment=<environment>
sleep 5
RUN_ID=$(gh run list --workflow=<workflow_name>.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
```

---

## Command Reference

| Task | Command | Reference |
|------|---------|-----------|
| Find repos with file | `gh search code --filename <file>` | [search.md](references/search.md) |
| Find repos with directory | `gh search code "path:<dir>"` | [search.md](references/search.md) |
| List failed runs | `gh run list --status=failure` | [monitoring.md](references/monitoring.md) |
| Watch run | `gh run watch <id> --exit-status` | [monitoring.md](references/monitoring.md) |
| Download artifacts | `gh run download <id> -n <name>` | [monitoring.md](references/monitoring.md) |
| Create PR | `gh pr create --fill` | [resources.md](references/resources.md) |
| Check PR CI | `gh pr checks --watch` | [monitoring.md](references/monitoring.md) |
| Trigger workflow | `gh workflow run <name>.yml` | [automation.md](references/automation.md) |
| Fork repo | `gh repo fork <repo> --clone` | [resources.md](references/resources.md) |
| REST/GraphQL API | `gh api repos/{owner}/{repo}` | [api.md](references/api.md) |

### JSON Output

```bash
gh pr list --json                              # Discover fields
gh pr list --json number,title,author,labels   # Select fields
gh run list --json status --jq '.[] | select(.status=="completed")'
```

### Environment & Auth

| Variable | Purpose |
|----------|---------|
| `GH_TOKEN` | Authentication token |
| `GH_REPO` | Default owner/repo |
| `GH_HOST` | GitHub Enterprise host |
| `GH_PROMPT_DISABLED=1` | Disable prompts (CI) |

### Rate Limits

| Endpoint | Limit | Notes |
|----------|-------|-------|
| REST API | 5,000/hour | Per authenticated user |
| Search API | 30/minute | All search endpoints |
| Code Search | 10/minute | More restrictive |
| Search results | 1,000 max | Use date partitioning for more |

---

## Workflow Authoring

GitHub Actions workflow YAML patterns for CI/CD pipelines.

### Basic Structure

```yaml
name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make build
      - run: make test
```

### Caching Patterns

```yaml
# Python/Poetry
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
- uses: actions/cache@v4
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ hashFiles('poetry.lock') }}

# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### Matrix Builds

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
  fail-fast: false
```

### OIDC Authentication (AWS/GCP)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: us-east-1
```

**Full reference:** [references/workflow-authoring.md](references/workflow-authoring.md)

### Advanced Patterns

For enterprise CI/CD pipelines:

- **Ephemeral PR Environments** - Auto-create/destroy per PR
- **Release Please** - Automated semantic versioning
- **PR Cleanup** - Resource cleanup on close
- **Testing Patterns** - pytest, Gradle, Jest with coverage
- **Deployment Status Checks** - Wait for stack readiness
- **Separate Build/Deploy Roles** - Fine-grained OIDC permissions
- **Multi-Stack Ordering** - Foundation → Schemas → Application

**Additional References:**
- **Workflow Summaries** - Rich markdown output with $GITHUB_STEP_SUMMARY
- **Container Security** - Multi-stage builds, Trivy scanning, image tagging
- **Security Scanning** - CodeQL, Dependabot, IaC scanning (Checkov, tfsec)
- **Troubleshooting** - Debug mode, flaky tests, common issues
- **Performance** - Limits, runner specs, optimization tips

---

## Scripts

Pre-built automation scripts with error handling and rate limit awareness.

| Script | Purpose | Usage |
|--------|---------|-------|
| `find-repos-with-path.sh` | Find repos containing specific paths | `./scripts/find-repos-with-path.sh .skilz [owner]` |
| `wait-for-run.sh` | Block until workflow completes | `./scripts/wait-for-run.sh <run_id> [timeout]` |
| `batch-search.sh` | Search >1000 results via date partitioning | `./scripts/batch-search.sh "query" <start> <end>` |

### Exit Codes

| Script | 0 | 1 | 2 | 3 |
|--------|---|---|---|---|
| `wait-for-run.sh` | success | failure | cancelled | timeout |
| `find-repos-with-path.sh` | success | error | - | - |
| `batch-search.sh` | success | error | - | - |

---

## Validation Checklist

Before completing a GitHub CLI task, verify:

```
- [ ] gh authenticated (`gh auth status`)
- [ ] Command syntax matches documentation
- [ ] Exit codes checked and handled appropriately
- [ ] Rate limits considered (code search: 10/min, repo search: 30/min)
- [ ] JSON output parsed correctly (if using --json)
- [ ] Artifacts downloaded to correct directory (if applicable)
- [ ] PR/Issue created with proper labels and assignees (if applicable)
- [ ] Workflow triggered and monitored to completion (if applicable)
```

---

## When Not to Use

This skill covers `gh` CLI and GitHub Actions workflow authoring. Do **not** use for:

- **Git commands**: `git push`, `git commit`, `git pull` (use git directly)
- **GitHub web UI**: Questions about github.com interface navigation
- **GitHub Desktop**: Different application entirely
- **Direct curl/HTTP**: API calls without `gh` wrapper
- **GitHub mobile app**: Mobile-specific features