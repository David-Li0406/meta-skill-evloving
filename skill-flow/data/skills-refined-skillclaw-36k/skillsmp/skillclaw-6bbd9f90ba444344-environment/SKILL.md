---
name: environment
description: Use this skill when you need to manage Railway environment configurations, including querying, modifying, or creating environments and their associated settings.
---

# Environment Configuration

Query, stage, and apply configuration changes for Railway environments.

## Quick Actions

**When user asks "what's the config" or "show configuration":**

Run `railway status --json` to get the environment ID, then **always** query the full config:
```bash
bash <<'SCRIPT'
scripts/railway-api.sh \
  'query envConfig($envId: String!) {
    environment(id: $envId) { id config }
  }' \
  '{"envId": "ENV_ID_FROM_STATUS"}'
SCRIPT
```
Present: source (repo/image), build settings, deploy settings, variables per service.

**When user asks "what variables" or "show env vars":**
Use the same environment config query above - it includes variables per service and shared variables.

For **rendered** (resolved) variable values: `railway variables --json`.

For mutations (add/change/delete), see sections below.

## Shell Escaping

**CRITICAL:** When running GraphQL queries via bash, you MUST wrap in heredoc to prevent shell escaping issues:

```bash
bash <<'SCRIPT'
scripts/railway-api.sh 'query ...' '{"var": "value"}'
SCRIPT
```

Without the heredoc wrapper, multi-line commands break and exclamation marks in GraphQL non-null types get escaped, causing query failures.

## When to Use

- User wants to create a new environment.
- User wants to duplicate an environment (e.g., "copy production to staging").
- User wants to switch to a different environment.
- User asks about current build/deploy settings, variables, replicas, health checks, domains.
- User asks to change service source (Docker image, branch, commit, root directory).
- User wants to connect a service to a GitHub repo.
- User wants to deploy from a GitHub repo (create empty service first via `new` skill, then use this).
- User asks to change build or start command.
- User wants to add/update/delete environment variables.
- User wants to change replica count or configure health checks.
- User asks to delete a service, volume, or bucket.
- User says "apply changes", "commit changes", "deploy changes".
- Auto-fixing build errors detected in logs.

## Create Environment

Create a new environment in the linked project:

```bash
railway env
```