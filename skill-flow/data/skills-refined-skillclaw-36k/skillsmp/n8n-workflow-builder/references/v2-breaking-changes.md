# n8n v2.0 Breaking Changes

Key breaking changes in n8n 2.0.

## Workflow Execution

### Save & Publish Model

**Before (v1.x):** Save = immediately live
**After (v2.0):** Save = saved locally, Publish = live

```
Save Button → Saves draft
Publish Button → Makes changes live (new in v2.0)
```

## Security Changes

### Code Node ENV Access

**Blocked by default.** Set `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` to restore.

```javascript
// Does not work in v2.0
process.env.MY_VAR

// Use n8n's $env instead
$env.MY_VAR
```

### Disabled Nodes

These nodes are disabled by default:

| Node | Enable With |
|------|-------------|
| ExecuteCommand | `N8N_ALLOW_EXECUTE_COMMAND_NODE=true` |
| LocalFileTrigger | `N8N_ALLOW_LOCAL_FILE_TRIGGER=true` |

## Database Changes

### MySQL/MariaDB Removed

**Must migrate to PostgreSQL or SQLite before upgrading.**

```bash
# Export data before v2.0 upgrade
n8n export:workflow --all --output=workflows.json
n8n export:credentials --all --output=credentials.json
```

## Removed Features

### Start Node

```javascript
// Removed
{ "type": "n8n-nodes-base.start" }

// Use instead
{ "type": "n8n-nodes-base.manualTrigger" }
{ "type": "n8n-nodes-base.executeWorkflowTrigger" }
```

### Docker Tags

| Old | New |
|-----|-----|
| `latest` | `stable` |
| `next` | `beta` |

## Migration Checklist

1. Check Migration Report: Settings → Migration Report
2. Export all workflows and credentials
3. Test with v2.0 in staging
4. Update .env files if needed
5. Migrate database if using MySQL
6. Update Code nodes using `process.env`
7. Review disabled nodes
8. Update CI/CD scripts for new Docker tags

## Sources

- [n8n 2.0 Blog Post](https://blog.n8n.io/introducing-n8n-2-0/)
- [v2.0 Breaking Changes Docs](https://docs.n8n.io/2-0-breaking-changes/)
