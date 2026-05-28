---
name: viya-dev-environment
description: Manage viya-app local development environment. Use when setting up services from PRs, troubleshooting container issues, restarting Docker services, switching service versions, or debugging local dev environment problems.
---

# Viya Dev Environment Management

This skill helps manage the local development environment for viya-app, particularly when testing backend service PRs.

## Environment Overview

The viya-app dev environment uses Docker Compose with services defined in `dev/docker-compose.yaml`. Service versions are controlled via `dev/.env`:

```
AUDITOR_VERSION=latest
SHIPPING_VERSION=latest
AUTHORIZING_VERSION=latest
HOOKS_VERSION=latest
RATES_VERSION=latest
STITCH_VERSION=latest
STITCH_INTEGRATIONS_VERSION=latest
PRINTING_VERSION=latest
FTP_VERSION=latest
```

Images are pulled from ECR: `528239395291.dkr.ecr.eu-central-1.amazonaws.com/viya/images/<service>:<version>`

## Service to Repository Mapping

| Service | Repository | Image Name |
|---------|------------|------------|
| shipping | ShipitSmarter/shipping | shipping |
| auditor | ShipitSmarter/auditor | auditor |
| authorizing | ShipitSmarter/authorizing | authorizing |
| hooks | ShipitSmarter/hooks | hooks |
| rates | ShipitSmarter/rates | rates |
| stitch | ShipitSmarter/stitch | stitch |
| stitch-integrations | ShipitSmarter/stitch-integrations | stitch-integrations |
| printing | ShipitSmarter/printing | printing |
| ftp | ShipitSmarter/ftp | ftp |

## Version Formats

- **latest**: Most recent main branch build
- **vX.Y.Z**: Specific release version (e.g., `v4.1.138`)
- **0.0.0-pr.NUMBER.RUNID**: PR build (e.g., `0.0.0-pr.1277.21150237490`)

## Workflow: Test a PR Build Locally

When the user wants to test a PR from a backend service:

### Step 1: Get PR Build Info

```bash
# Get PR number and check if build succeeded
gh pr view <PR_NUMBER> --repo ShipitSmarter/<repo> --json number,headRefName,title

# Get the latest workflow run for this PR
gh run list --repo ShipitSmarter/<repo> --branch <branch_name> --limit 1 --json databaseId,conclusion,headBranch

# Check if Docker build succeeded
gh pr checks <PR_NUMBER> --repo ShipitSmarter/<repo>
```

The version format for PR builds is: `0.0.0-pr.<PR_NUMBER>.<RUN_ID>`

Example: For PR #1277 with run ID 21150237490, the version is `0.0.0-pr.1277.21150237490`

### Step 2: Update .env

Edit `/home/wouter/git/viya-app/dev/.env` and set the appropriate version:

```
SHIPPING_VERSION=0.0.0-pr.1277.21150237490
```

### Step 3: Restart the Service

```bash
cd /home/wouter/git/viya-app/dev

# Stop and remove the specific service
docker compose stop <service_name>
docker compose rm -f <service_name>

# Pull and start the new version
docker compose pull <service_name>
docker compose up -d <service_name>
```

Or restart everything:

```bash
docker compose stop
docker compose rm -f
docker compose pull
docker compose up -d
```

### Step 4: Verify

```bash
# Check container is running with correct image
docker compose ps <service_name>

# Check logs for startup issues
docker compose logs <service_name> --tail 50
```

## Workflow: Reset to Latest

To reset all services back to latest:

1. Edit `dev/.env` and set all versions back to `latest`
2. Run:
   ```bash
   cd /home/wouter/git/viya-app/dev
   docker compose stop && docker compose rm -f && docker compose pull && docker compose up -d
   ```

## Workflow: Check Current Versions

```bash
cd /home/wouter/git/viya-app/dev
docker compose ps --format "table {{.Name}}\t{{.Image}}\t{{.Status}}"
```

## Common Issues

### Token Expired

If you see "Token has expired and refresh failed":

```bash
aws sso login --profile ecr
aws ecr get-login-password --profile ecr | docker login --username AWS --password-stdin 528239395291.dkr.ecr.eu-central-1.amazonaws.com
```

### Image Not Found

If a PR build image doesn't exist:
1. Check if the PR build workflow completed successfully
2. Check if "Docker build" job passed (not just tests)
3. The image is only pushed after successful build

### Service Won't Start

Check logs:
```bash
docker compose logs <service_name> --tail 100
```

Common causes:
- Missing environment variables
- MongoDB connection issues
- Port conflicts

## Quick Reference Commands

```bash
# Check PR build status
gh pr checks <PR_NUMBER> --repo ShipitSmarter/<repo>

# Get run ID for version string
gh run list --repo ShipitSmarter/<repo> --branch <branch> --limit 1 --json databaseId

# Login to ECR (if expired)
aws sso login --profile ecr && aws ecr get-login-password --profile ecr | docker login --username AWS --password-stdin 528239395291.dkr.ecr.eu-central-1.amazonaws.com

# Restart single service
docker compose stop <svc> && docker compose rm -f <svc> && docker compose pull <svc> && docker compose up -d <svc>

# View running containers
docker compose ps

# View logs
docker compose logs <service> -f
```
