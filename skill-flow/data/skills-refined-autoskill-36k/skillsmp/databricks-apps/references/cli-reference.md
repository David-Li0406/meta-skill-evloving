# Databricks Apps CLI Reference

> **Note:** Use CLI as fallback only when `mcp__apps__*` tools cannot handle the operation.

## MCP vs CLI

| Operation | MCP (Primary) | CLI (Fallback) |
|-----------|---------------|----------------|
| Create app | `mcp__apps__create_app` | `databricks apps create` |
| Get app | `mcp__apps__show_app` | `databricks apps get` |
| Start/Stop | `mcp__apps__start_app/stop_app` | `databricks apps start/stop` |
| Deploy | `mcp__apps__deploy_app` | `databricks apps deploy` |
| List deployments | `mcp__apps__list_deployments` | `databricks apps list-deployments` |
| Logs | Check in browser | Check in browser |
| Update | - | `databricks apps update` |
| List | - | `databricks apps list` |
| Permissions | - | `databricks apps get-permissions` |

> **Note:** App logs are not available via MCP tools. Users must check logs in the Databricks workspace browser UI.

## Resource Types

### SQL Warehouse

```json
{
  "name": "sql_warehouse",
  "sql_warehouse": { "id": "warehouse_id", "permission": "CAN_USE" }
}
```
Env: `DATABRICKS_RESOURCE_SQL_WAREHOUSE_ID`

### Unity Catalog Schema

```json
{
  "name": "catalog_data",
  "unity_catalog_schema": {
    "catalog_name": "catalog_name",
    "schema_name": "schema_name",
    "permission": "SELECT"
  }
}
```
Permissions: `SELECT`, `MODIFY`, `ALL_PRIVILEGES`

### Serving Endpoint

```json
{
  "name": "ml_endpoint",
  "serving_endpoint": { "name": "endpoint_name", "permission": "CAN_QUERY" }
}
```

### Vector Search Index

```json
{
  "name": "vector_index",
  "vector_search_index": { "name": "catalog.schema.index_name", "permission": "CAN_USE" }
}
```

### Genie Space

```json
{
  "name": "genie_space",
  "genie_space": { "id": "genie_space_id", "permission": "CAN_VIEW" }
}
```
Permissions: `CAN_VIEW`, `CAN_EDIT`, `CAN_MANAGE`

### Job

```json
{
  "name": "my_job",
  "job": { "id": "job_id", "permission": "CAN_MANAGE_RUN" }
}
```
Permissions: `CAN_VIEW`, `CAN_MANAGE_RUN`, `CAN_MANAGE`

### Secret Scope

```json
{
  "name": "app_secrets",
  "secret_scope": { "scope": "my_scope", "permission": "READ" }
}
```

## CLI Commands (Fallback)

### App Management

```bash
databricks apps get APP_NAME
databricks apps list
databricks apps update APP_NAME '{...}'
databricks apps start APP_NAME
databricks apps stop APP_NAME --no-wait
```

### Deployment

```bash
databricks apps deploy APP_NAME --source-code-path /Workspace/path
databricks apps list-deployments APP_NAME
databricks apps get-deployment APP_NAME DEPLOYMENT_ID
```

### Logs

> **Note:** App logs are not available via API (PAT not supported). Direct users to check logs in the browser:
> **Compute** > **Apps** > Select app > **Logs** tab

### Permissions

```bash
databricks apps get-permissions APP_NAME
databricks apps set-permissions APP_NAME --json '{
  "access_control_list": [
    { "service_principal_name": "SP_NAME", "permission_level": "CAN_MANAGE" }
  ]
}'
```

## Service Principal Resource Configuration

Use only when user-on-behalf-of is unavailable (e.g., background jobs).

### 1. Bind Resources

```bash
databricks apps update $SESSION_APP_NAME --json '{
  "resources": [
    { "name": "sql_warehouse", "sql_warehouse": { "id": "WAREHOUSE_ID", "permission": "CAN_USE" } }
  ]
}'
```

### 2. Get Service Principal Name

```bash
databricks apps get $SESSION_APP_NAME | jq -r '.service_principal_name'
```

### 3. Grant Permissions

**SQL Warehouse:**
```bash
databricks warehouses update-permissions WAREHOUSE_ID --json '{
  "access_control_list": [
    { "service_principal_name": "SP_NAME", "permission_level": "CAN_USE" }
  ]
}'
```

**Unity Catalog (SQL):**
```sql
GRANT USE CATALOG ON CATALOG catalog_name TO `service_principal_name`;
GRANT USE SCHEMA ON SCHEMA catalog_name.schema_name TO `service_principal_name`;
GRANT SELECT ON TABLE catalog_name.schema_name.table_name TO `service_principal_name`;
```

## App Object Structure

```json
{
  "name": "app-name",
  "service_principal_id": 123456,
  "service_principal_name": "app-name-sp",
  "user_api_scopes": ["sql", "catalog.schemas:read", "catalog.tables:read", "unity-catalog"],
  "resources": [...],
  "compute_status": { "state": "ACTIVE|STOPPED|ERROR" },
  "active_deployment": {
    "deployment_id": "...",
    "status": { "state": "SUCCEEDED|FAILED|IN_PROGRESS" }
  },
  "url": "https://app-name.cloud.databricks.com"
}
```
