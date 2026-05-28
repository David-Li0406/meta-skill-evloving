# Databricks Apps Troubleshooting Guide

## Table of Contents

- [First Steps](#first-steps)
- [Deployment Issues](#deployment-issues)
- [Authorization Issues](#authorization-issues)
- [OBO Token Issues](#obo-token-issues)
- [SQL Execution Issues](#sql-execution-issues)
- [Runtime Issues](#runtime-issues)
- [app.yaml Reference](#appyaml-reference)

## First Steps

1. Check status with `mcp__apps__show_app`
2. Check logs in browser (**Compute** > **Apps** > Select app > **Logs** tab)
3. Check deployment history with `mcp__apps__list_deployments`

## Deployment Issues

### Deployment Failed

Direct user to check logs in browser: **Compute** > **Apps** > Select app > **Logs** tab.

| Cause | Solution |
|-------|----------|
| Invalid app.yaml | syntax と required fields を確認 |
| Missing dependencies | requirements.txt を確認 |
| Code errors | Python syntax, imports を確認 |
| Resource limits | memory/CPU 使用量を削減 |

## Authorization Issues

### Permission Errors

Check `user_api_scopes` and `resources` with `mcp__apps__show_app`.

### Table Access Denied

**All 4 scopes are required:**
- `sql`
- `catalog.schemas:read`
- `catalog.tables:read`
- `unity-catalog`

After configuring, restart with `mcp__apps__stop_app` → `mcp__apps__start_app`.

### Other Access Denied

| Resource | Required Scope |
|----------|---------------|
| SQL Warehouse | `sql` |
| Serving Endpoint | `serving` |
| Vector Search | `vector-search` |
| Genie Space | `genie` |
| Secrets | `secrets` |

### Common Mistakes

| Problem | Solution |
|---------|----------|
| `user_api_scopes` not configured | Add with `databricks apps update` CLI |
| Missing catalog scopes | Add `catalog.schemas:read`, `catalog.tables:read` |
| Configured in app.yaml | Not supported. Use `databricks apps update` CLI |
| User lacks permissions | GRANT directly to user |
| Cannot get environment variables | Configure `resources` |

## OBO Token Issues

### DATABRICKS_API_TOKEN is null

**Cause**: `user_api_scopes` not configured

**Solution**: Configure scopes with `databricks apps update` CLI and restart.

### Token Expired

- Apps runtime auto-refreshes tokens
- Don't hold connections for long periods
- Implement retry on errors

### User Not Logged In

OBO requires a user session. Verify user is accessing the Apps URL.

## SQL Execution Issues

### Error with mcp__databricks__run_sql

| Error | Cause | Solution |
|-------|-------|----------|
| `PERMISSION_DENIED` | User lacks table permissions | GRANT directly to user |
| `TABLE_OR_VIEW_NOT_FOUND` | Incorrect table name | Use fully qualified name |
| `RESOURCE_DOES_NOT_EXIST` | Warehouse not found | Verify Warehouse ID |
| `INVALID_SESSION` | Session invalid | Restart Apps |

### Check Permissions

Execute `SHOW GRANTS ON TABLE catalog.schema.table` with `mcp__databricks__run_sql`.

### Warehouse Not Started

Warehouse auto-starts on query execution, but first query may take time.

## Runtime Issues

### App Not Accessible

Check with `mcp__apps__show_app`:
- `compute_status.state` = `ACTIVE`
- `active_deployment.status.state` = `SUCCEEDED`

If not `ACTIVE`, run `mcp__apps__start_app`.

### App Crashes

Check logs in browser: **Compute** > **Apps** > Select app > **Logs** tab.

**Common causes:**
- Not binding to `APP_PORT` environment variable
- Missing environment variables
- Import errors

### Cannot Get Environment Variables

**Resource ID variables** (`DATABRICKS_RESOURCE_SQL_WAREHOUSE_ID`, etc.):
Configure `resources` with `databricks apps update` CLI.

**Auto-injected variables**:
- `DATABRICKS_HOST`
- `DATABRICKS_API_TOKEN` (when OBO enabled)
- `APP_PORT`

### Cannot Get Secrets

**Configure in app.yaml:**
```yaml
env:
  - name: API_KEY
    valueFrom:
      secretRef:
        key: api_key
        scope: my-scope
```

**Or retrieve via OBO:**
Add `secrets` to `user_api_scopes`.

## app.yaml Reference

**Note:** `user_api_scopes`, `resources` は app.yaml では設定不可。

```yaml
command:
  - "python"
  - "main.py"

env:
  - name: VAR_NAME
    value: "static_value"
  - name: SECRET_VAR
    valueFrom:
      secretRef:
        key: secret_key
        scope: secret_scope
```

**Important:** `APP_PORT` 環境変数のポート (default: 8000) でリッスンすること。
