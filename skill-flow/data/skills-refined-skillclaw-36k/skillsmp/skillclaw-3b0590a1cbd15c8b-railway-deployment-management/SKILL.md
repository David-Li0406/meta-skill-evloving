---
name: railway-deployment-management
description: Use this skill when you want to manage Railway deployments, including viewing logs, redeploying, restarting, or removing deployments.
---

# Railway Deployment Management

Manage existing Railway deployments: list, view logs, redeploy, or remove.

**Important:** "Remove deployment" (`railway down`) stops the current deployment but keeps the service. To delete a service entirely, use the `railway-environment` skill with `isDeleted: true`.

## When to Use

- User says "remove deploy", "take down service", "stop deployment", "railway down"
- User wants to "redeploy", "restart the service", "restart deployment"
- User asks to "list deployments", "show deployment history", "deployment status"
- User asks to "see logs", "show logs", "check errors", "debug issues"

## List Deployments

```bash
railway deployment list --limit 10 --json
```

Shows deployment IDs, statuses, and metadata. Use to find specific deployment IDs for logs or debugging.

### Specify Service

```bash
railway deployment list --service backend --limit 10 --json
```

## View Logs

### Deploy Logs

```bash
railway logs --lines 100 --json
```

In non-interactive mode, streaming is auto-disabled and CLI fetches logs then exits.

### Build Logs

```bash
railway logs --build --lines 100 --json
```

For debugging build failures or viewing build output.

### Logs for Failed/In-Progress Deployments

By default, `railway logs` shows the last successful deployment. Use `--latest` for current:

```bash
railway logs --latest --lines 100 --json
```

### Filter Logs

```bash
# Errors only
railway logs --lines 50 --filter "@level:error" --json

# Text search
railway logs --lines 50 --filter "connection refused" --json

# Combined
railway logs --lines 50 --filter "@level:error AND timeout" --json
```

### Time-Based Filtering

```bash
# Logs from last hour
railway logs --since 1h --lines 100 --json

# Logs between 30 and 10 minutes ago
railway logs --since 30m --until 10m --lines 100 --json

# Logs from specific timestamp
railway logs --since 2024-01-15T10:00:00Z --lines 100 --json
```