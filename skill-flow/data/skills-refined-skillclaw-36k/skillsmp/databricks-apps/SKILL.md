---
name: databricks-apps
description: Databricks Apps deployment, debugging, and configuration management. Use when working with Databricks Apps issues including deployment failures, app configuration (app.yaml), granting permissions to SQL warehouses or Unity Catalog resources, troubleshooting app errors, or managing app state (start/stop). Triggered by mentions of SESSION_APP_NAME, app.yaml, deployment errors, or permission issues with Apps.
metadata:
  version: 1.0.0
---

# Databricks Apps

## Tools

**Primary**: Use `mcp__apps__*` tools (create, deploy, show, list_deployments, start, stop)
**SQL Execution**: `mcp__databricks__run_sql` executes SQL with user permissions
**Fallback**: CLI (`databricks apps ...`) only when MCP tools cannot handle the operation

## Logs

**App logs are not available via API.** Users must check logs in the browser:
1. Open Databricks workspace
2. Navigate to **Compute** > **Apps**
3. Select the app and view **Logs** tab

## Environment

- App name: `$SESSION_APP_NAME`
- Auto deploy: `APP_AUTO_DEPLOY=true` triggers automatic deployment on session end

## Core Workflow

1. **Check Status**: `mcp__apps__show_app` → Check `compute_status.state`, `user_api_scopes`, `resources`
2. **Check Logs**: Direct user to check logs in browser (see Logs section above)
3. **After Config Change**: `mcp__apps__stop_app` → `mcp__apps__start_app` to restart

## Authorization (OBO)

**Cannot be configured in app.yaml.** Use `mcp__apps__update` to set `user_api_scopes`.

### 4 Scopes Required for Unity Catalog Table Access

| scope | Purpose |
|-------|---------|
| `sql` | SQL Warehouse |
| `catalog.schemas:read` | Schema metadata |
| `catalog.tables:read` | Table metadata |
| `unity-catalog` | Data access |

### All Scopes

`sql`, `catalog.schemas:read`, `catalog.tables:read`, `unity-catalog`, `serving`, `vector-search`, `genie`, `jobs`, `secrets`

### Security Best Practices

**Principle of Least Privilege**: Only grant scopes that the app actually needs.

- For read-only table access: `sql`, `catalog.schemas:read`, `catalog.tables:read`, `unity-catalog`
- For Model Serving only: `serving`
- For Vector Search only: `vector-search`

**Avoid granting all scopes at once.** Start with minimal scopes and add more only when errors indicate they are needed.

### Resource Environment Variables

When you need `DATABRICKS_RESOURCE_SQL_WAREHOUSE_ID` etc., also configure `resources`:

```json
{
  "name": "sql_warehouse",
  "sql_warehouse": { "id": "WAREHOUSE_ID", "permission": "CAN_USE" }
}
```

## SQL Execution with OBO Token

### SQL Execution from Session

Use `mcp__databricks__run_sql`. Executed with user's OBO token.

### SQL Execution in Apps Code

```python
from databricks import sql
import os

connection = sql.connect(
    server_hostname=os.environ["DATABRICKS_HOST"],
    http_path=f"/sql/1.0/warehouses/{os.environ['DATABRICKS_RESOURCE_SQL_WAREHOUSE_ID']}",
    access_token=os.environ["DATABRICKS_API_TOKEN"]
)
```

**Auto-injected Environment Variables**:
- `DATABRICKS_HOST`: Workspace URL
- `DATABRICKS_API_TOKEN`: OBO token (only when `user_api_scopes` is configured)
- `APP_PORT`: Port the app should bind to

## Troubleshooting Quick Reference

| Issue | Action |
|-------|--------|
| Deployment failed | Direct user to check logs in browser |
| Permission error | Check `user_api_scopes` with `mcp__apps__show_app` |
| Table access denied | Verify all 4 scopes are configured |
| App not accessible | Check if `compute_status.state` is ACTIVE |
| OBO token is null | Check if `user_api_scopes` is not empty |
| SQL permission error | Verify user has table permissions |

Details: [troubleshooting.md](references/troubleshooting.md)

## Service Principal

Use only when user context is unavailable (e.g., background jobs).
Details: [cli-reference.md](references/cli-reference.md#service-principal-resource-configuration)
