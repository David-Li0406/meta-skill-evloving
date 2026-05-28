---
name: railway-integration
description: |
  Railway deployment and configuration skill following Railway official patterns.
  Use when deploying to Railway, managing Railway services, or configuring Railway environments.
tags: [railway, deployment, infrastructure, platform-integration]
allowed-tools:
  - Bash(railway:*)
  - Bash(curl:*)
  - Read
  - Write
  - Edit
---

# Railway Integration Skill

Railway deployment and configuration management using GraphQL API + CLI patterns.

## Purpose

Automate Railway operations with GraphQL API + CLI pattern following Railway's official skill architecture.

**Time to complete:** <5 minutes for typical operations

## When to Use This Skill

**Trigger phrases:**
- "deploy to railway"
- "railway up"
- "create railway service"
- "manage railway environment"
- "railway deployment"

**Use when:**
- Deploying code to Railway
- Creating/managing Railway services
- Configuring environments and variables
- Managing deployments and domains
- Querying Railway metrics

## Workflow

### 1. Check Prerequisites

- Railway CLI installed (`railway --version`)
- Railway authenticated (`railway status`)
- Project linked or project ID available
- Skills plane lib scripts available

### 2. Execute Operation

**For deployments:**
```bash
# Pre-flight check
~/.agent/skills/railway-doctor/check.sh

# Deploy
railway up --detach

# Monitor
railway logs --build --lines 50
```

**For configuration (GraphQL pattern):**
```bash
# Always use heredoc for shell safety
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"

bash <<'SCRIPT'
${SKILLS_ROOT}/lib/railway-api.sh \
  'query envConfig($envId: String!) {
    environment(id: $envId) { id config }
  }' \
  '{"envId": "ENV_ID"}'
SCRIPT
```

### 3. Validate Results

- Check deployment status
- Verify configuration applied
- Test service health

## GraphQL Pattern (from Railway official skills)

Railway's official skills use GraphQL for reliable operations:

```bash
# Environment variable fallback for agent compatibility
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
LIB_SCRIPT="$SKILLS_ROOT/lib/railway-api.sh"

# Always use heredoc for shell safety
bash <<'SCRIPT'
${LIB_SCRIPT} \
  'query envConfig($envId: String!) {
    environment(id: $envId) {
      id
      config(decryptVariables: false)
    }
  }' \
  '{"envId": "ENV_ID"}'
SCRIPT
```

**Benefits:**
- More reliable than CLI parsing
- Better error handling
- Works for complex mutations
- Cross-agent compatible

**Common Queries:**

| Query | Purpose |
|-------|---------|
| `environment(id)` | Get full config |
| `project(id)` | List services |
| `currentUser` | Verify auth |
| `environmentStagedChanges` | Check pending changes |

## Common Operations

### Deploy Code

```bash
# Detach mode (default)
railway up --detach

# CI mode (stream logs)
railway up --ci

# Specific service
railway up --service backend --detach
```

### Manage Environment Variables

```bash
# Query current variables
railway variables --json

# Set variable
railway variables set API_KEY=secret_value

# Bulk set via GraphQL
bash <<'SCRIPT'
${SKILLS_ROOT}/lib/railway-api.sh \
  'mutation stageChanges($envId: String!, $input: EnvironmentConfig!, $merge: Boolean) {
    environmentStageChanges(
      environmentId: $envId
      input: $input
      merge: $merge
    ) { id }
  }' \
  '{
    "envId": "ENV_ID",
    "input": {
      "services": {
        "SERVICE_ID": {
          "variables": {
            "API_KEY": {"value": "secret"}
          }
        }
      }
    },
    "merge": true
  }'
SCRIPT
```

### Create Service

```bash
# From template
railway new --template=python

# Custom configuration
railway new
# Follow prompts to configure
```

### View Deployment Status

```bash
# List deployments
railway deployments

# View logs
railway logs --build --lines 100

# Redeploy
railway up --detach --service backend
```

## Integration Points

### With railway-doctor

Run pre-flight checks before deploy:
```bash
~/.agent/skills/railway-doctor/check.sh
```

### With devops-dx

Sync env vars to GitHub:
```bash
~/.agent/skills/devops-dx/scripts/sync_env_to_github.sh <environment>
```

### With Beads

Track Railway work:
```typescript
mcp__plugin_beads_beads__create({
  title: "Railway deployment: backend",
  issue_type: "task",
  priority: 2
})
```

## Agent Compatibility

| Agent | Type | GraphQL Support | Notes |
|-------|------|-----------------|-------|
| Claude Code | Skills-Native | ✅ Full | `${CLAUDE_PLUGIN_ROOT}` available |
| Codex CLI | Skills-Native | ✅ Full | Via skills plane |
| OpenCode | Skills-Native | ✅ Full | Via skills plane |
| Gemini CLI | MCP-Dependent | ✅ Via skills plane | `${HOME}/.agent/skills` fallback |
| Antigravity | MCP-Dependent | ✅ Via skills plane | `${HOME}/.agent/skills` fallback |

## What This Does

- Deploy code to Railway
- Manage services and environments
- Configure variables and domains
- Query deployment status and logs
- Validate Railway configuration

## What This Doesn't Do

- ❌ Pre-flight validation (use railway-doctor)
- ❌ GitHub env sync (use devops-dx)
- ❌ Local development (use Railway CLI directly)
- ❌ Service creation outside Railway

## Troubleshooting

### "railway-api.sh not found"

```bash
# Verify skills plane lib
ls -la ~/.agent/skills/lib/railway-api.sh

# If missing, copy from Railway skills
git clone https://github.com/railwayapp/railway-skills.git /tmp/railway-skills
cp /tmp/railway-skills/plugins/railway/skills/lib/*.sh ~/.agent/skills/lib/
```

### "Railway token invalid"

```bash
# Re-authenticate
railway login

# Verify
railway status
```

### "Deployment fails"

```bash
# Run pre-flight check
~/.agent/skills/railway-doctor/check.sh

# Fix issues
~/.agent/skills/railway-doctor/fix.sh

# Re-check
~/.agent/skills/railway-doctor/check.sh
```

## Related Skills

- **railway-doctor**: Pre-flight validation
- **devops-dx**: Environment management
- **multi-agent-dispatch**: Railway as dispatch target

## Resources

- [Railway Official Skills](https://github.com/railwayapp/railway-skills)
- [Railway Documentation](https://docs.railway.com)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Railway Changelog #0272](https://railway.com/changelog/2026-01-09-railway-agent-skill)

## Version History

- **v1.0.0** (2025-01-12): Initial Railway integration template
  - GraphQL pattern documentation
  - Cross-agent compatibility
  - Railway official skills integration
