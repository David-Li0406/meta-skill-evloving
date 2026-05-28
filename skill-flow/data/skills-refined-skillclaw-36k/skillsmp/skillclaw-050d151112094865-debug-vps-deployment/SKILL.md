---
name: debug-vps-deployment
description: Use this skill when deploying to a VPS and debugging deployment failures, investigating container issues, checking health endpoints, or fixing OtterStack errors.
---

# Debug VPS Deployment

Deploy to the production VPS (archivist@194.163.189.144) and iteratively debug failures until successful deployment.

## Objective

This skill connects to the specific VPS, triggers OtterStack deployments, monitors output for failures, diagnoses root causes, applies fixes, and redeploys until the application is successfully running and healthy.

## Orchestration Modes

This skill can be used in two modes:

1. **Standalone Mode** - Invoked directly by the user for manual VPS debugging.
2. **Orchestrated Mode** - Invoked automatically by the `/deploy-otterstack` command during the debug loop.

### VPS Connection Details

```bash
# SSH Connection
SSH_HOST="archivist@194.163.189.144"
SSH_USER="archivist"
OTTERSTACK_PATH="~/OtterStack/otterstack"

# Verify connection
ssh ${SSH_HOST} "echo 'Connection successful'"
```

## Quick Start Deployment

```bash
# 1. Verify OtterStack is available
ssh ${SSH_HOST} "${OTTERSTACK_PATH} --help"

# 2. Check project exists
ssh ${SSH_HOST} "${OTTERSTACK_PATH} status <project-name>"

# 3. Deploy with verbose output
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"

# 4. If it succeeds, verify endpoints. If it fails, proceed to debugging.
```

## Deployment Workflow

### Stage 1: Pre-Flight Checks

Before deploying, verify the environment is ready:

```bash
# Check SSH access
ssh ${SSH_HOST} "echo 'SSH OK'"

# Check OtterStack installation
ssh ${SSH_HOST} "${OTTERSTACK_PATH} --version" || \
  ssh ${SSH_HOST} "ls -l ~/OtterStack/otterstack"

# List existing projects
ssh ${SSH_HOST} "${OTTERSTACK_PATH} project list"

# Check current deployment status
ssh ${SSH_HOST} "${OTTERSTACK_PATH} status <project-name>"
```

### Stage 2: Trigger Deployment

Deploy with verbose output to see all stages:

```bash
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"
```

### Stage 3: Monitor Deployment Stages

Watch the output for these sequential stages:

1. **"Fetching latest changes..."** → Git operations (only for remote repos)
2. **"Validating compose file..."** → Syntax and env var validation
3. **"Pulling images..."** → Docker image downloads
4. **"Starting services..."** → Container creation and startup
5. **"Waiting for containers to be healthy..."** → Health check polling
6. **"Applying Traefik priority labels..."** → Traffic routing setup (if Traefik enabled)
7. **"Deployment successful!"** 

### Orchestrated Mode Operation

When invoked from the `/deploy-otterstack` command, this skill operates in **iterative debug mode**:

**Workflow:**
1. Receives deployment error context from the orchestration command.
2. Diagnoses failure type using a decision tree.
3. Applies appropriate fix (automatic or guided).
4. Returns fix status to the orchestration command.
5. Orchestration command retries deployment.
6. Repeats until successful (max 6 attempts by default).

**Context Passed from Orchestration:**
- `ERROR_MESSAGE` - Full error output from failed deployment.
- `DEPLOYMENT_STAGE` - Which stage failed (validation, startup, health_check, lock_conflict, traefik, unknown).
- `PROJECT_NAME` - Name of the project being deployed.
- `ATTEMPT_NUMBER` - Current debug iteration (1-6).
- `DEPLOYMENT_TARGET` - Always "vps" when this skill is invoked.

**Fix Determination:**
Based on `DEPLOYMENT_STAGE`, the skill uses the corresponding decision tree section to determine the fix.

| Fix Type | Fixable Via | Orchestration Action |
|----------|-------------|----------------------|
| Missing env vars | SSH command | Auto-fix: `ssh ...` |
| ... | ... | ... |