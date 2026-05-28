---
name: databricks-sql
description: |
  A skill for using Databricks SQL (SQL Warehouse) via SDK. Supports both Python (databricks-sql-connector) and Node.js (@databricks/sql).

  Use when:
  - Connecting to SQL Warehouse from Databricks Apps to execute queries
  - Running queries from Python/Node.js scripts against SQL Warehouse
  - Troubleshooting SQL Warehouse connection errors
  - Learning SDK usage and best practices

  Triggers:
  - "SQL Warehouse", "Databricks SQL", "databricks-sql-connector", "@databricks/sql"
  - "connect to warehouse", "execute SQL query", "query Databricks"
  - "SQL connection error", "warehouse connection issue"
metadata:
  version: 1.0.0
---

# Databricks SQL SDK

Guide for connecting to Databricks SQL Warehouse via SDK and executing queries.

**Note**: This skill assumes Serverless SQL Warehouse. Serverless warehouses spin up in seconds, so no need to handle startup wait times.

## SDK Selection

| Language | Package | Use Cases |
|----------|---------|-----------|
| Python | `databricks-sql-connector` | Scripts, data processing, ML pipelines |
| Node.js | `@databricks/sql` | Databricks Apps (Fastify/Express), Web APIs |

## Finding SQL Warehouses

Use Databricks CLI to list available SQL Warehouses:

```bash
# List all SQL Warehouses
databricks warehouses list

# Get details of a specific warehouse
databricks warehouses get <warehouse_id>
```

The `http_path` for connection is: `/sql/1.0/warehouses/<warehouse_id>`

## Authentication

Use token authentication. For Databricks Apps, OAuth token is available from `x-forwarded-access-token` header.

```python
# Python - Getting token in Databricks Apps
access_token = request.headers.get("x-forwarded-access-token")
```

```typescript
// Node.js (Fastify) - Getting token in Databricks Apps
const accessToken = request.headers["x-forwarded-access-token"];
```

## Quick Start

### Python

```python
from databricks import sql

with sql.connect(
    server_hostname="<workspace>.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/<warehouse_id>",
    access_token="<token>"
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM catalog.schema.table LIMIT 10")
        rows = cursor.fetchall()
```

### Node.js

```typescript
import { DBSQLClient } from "@databricks/sql";

const client = new DBSQLClient();
await client.connect({
  host: "<workspace>.cloud.databricks.com",
  path: "/sql/1.0/warehouses/<warehouse_id>",
  token: "<token>",
});

const session = await client.openSession();
const operation = await session.executeStatement("SELECT * FROM catalog.schema.table LIMIT 10");
const rows = await operation.fetchAll();

await operation.close();
await session.close();
await client.close();
```

## Detailed Guides

- **Python SDK Details**: [references/python-sdk.md](references/python-sdk.md) - Connection options, parameter binding, large data processing
- **Node.js SDK Details**: [references/nodejs-sdk.md](references/nodejs-sdk.md) - Async processing, streaming, Fastify integration
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md) - Connection errors, timeouts, authentication issues
- **SQL Tips**: [references/sql-tips.md](references/sql-tips.md) - Query optimization, best practices
