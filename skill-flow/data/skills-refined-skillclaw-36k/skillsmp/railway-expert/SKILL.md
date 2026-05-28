---
name: railway-expert
description: Complete toolset for Railway project management. Manage services, deployments, variables, and environments directly from the CLI. Use this skill to deploy apps, troubleshoot issues, view logs, and configure infrastructure without leaving the terminal.
compatibility: Requires railway-cli
---

# Railway Expert

## Tools Overview

| Category | Commands | Use Case |
|----------|----------|----------|
| **Setup** | `init`, `link`, `login`, `logout` | project initialization and authentication |
| **Services** | `add`, `service`, `domain` | Managing services and custom domains |
| **Deploy** | `up`, `deploy`, `redeploy`, `down` | Deploying code and managing active deployments |
| **Env Vars** | `variables` | Managing environment variables and secrets |
| **Observability** | `logs`, `status` | Monitoring service health and build/deploy logs |
| **Environments** | `environment` | Creating and deleting environments |
| **Access** | `ssh`, `run`, `shell`, `connect` | Interactive access to containers and databases |

## Common Workflows

### 1. Project Setup & Linking
Before working, ensure you are authenticated and linked to the correct project:

```bash
# Login to Railway
railway login

# Link via interactive menu or project ID
railway link

# Check what you are linked to
railway status
```

### 2. Deployment Management
Deploy code and manage versions:

```bash
# Deploy current directory
railway up

# Deploy to a specific service
railway up --service my-service

# Detach from build logs (fire and forget)
railway up -d

# Redeploy latest version (useful for restarting)
railway redeploy --service my-service
```

### 3. Variable Management
Configure secrets and settings:

```bash
# List all variables
railway variables

# Set multiple variables
railway variables --set "PORT=8080" --set "NODE_ENV=production"

# Get variables in JSON format
railway variables --json
```

### 4. Troubleshooting & Inspection
Diagnose issues in production:

```bash
# View deployment logs
railway logs

# View build logs (if deployment failed)
railway logs --build

# SSH into the running container
railway ssh

# Run a command in the environment context
railway run -- dotnet --info
```

### 5. Environment Management
Work with multiple environments (Production, Staging, etc.):

```bash
# Create a new environment
railway environment new staging

# Link local directory to staging
railway link --environment staging

# Delete an environment
railway environment delete dev-test
```

## Best Practices

- **Use JSON Output**: When parsing output in scripts, always use the `--json` flag (e.g., `railway variables --json`).
- **Service Scoping**: Explicitly specify `--service` when working in a monorepo to avoid ambiguity.
- **Detached Deploys**: Use `railway up -d` for CI pipelines to avoid hanging on log streaming.
- **Environment Context**: Always verify your active environment with `railway status` before making destructive changes.
