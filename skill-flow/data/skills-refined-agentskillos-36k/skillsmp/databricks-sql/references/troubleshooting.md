# Troubleshooting

## Table of Contents

1. [Connection Errors](#connection-errors)
2. [Authentication Errors](#authentication-errors)
3. [Timeouts](#timeouts)
4. [SQL Errors](#sql-errors)
5. [Performance Issues](#performance-issues)

---

## Connection Errors

### "Failed to connect to server" / "Connection refused"

**Cause**: Incorrect hostname or http_path

**Check**:
1. `server_hostname` / `host` matches workspace URL
   - Correct: `adb-1234567890123456.7.azuredatabricks.net`
   - Wrong: `https://adb-1234567890123456.7.azuredatabricks.net` (no protocol needed)
2. `http_path` is in correct format
   - SQL Warehouse: `/sql/1.0/warehouses/<warehouse_id>`
   - Cluster: `/sql/1.0/endpoints/<cluster_id>`

**How to find SQL Warehouse http_path**:
1. Open SQL Warehouse in Databricks workspace
2. Go to "Connection details" tab
3. Copy the "HTTP path" value

### "SSL: CERTIFICATE_VERIFY_FAILED"

**Cause**: SSL certificate verification failed

**Solution**:
- Check certificate settings if behind proxy
- Contact IT department for corporate networks

---

## Authentication Errors

### "Invalid access token" / "AUTHENTICATION_ERROR"

**Cause**: Token is invalid or expired

**Check**:
1. Token is copied correctly (watch for leading/trailing whitespace)
2. Token has not expired
3. For Databricks Apps, header name is correct

```typescript
// Correct header name
const token = request.headers["x-forwarded-access-token"];

// Common mistakes
const token = request.headers["x-access-token"];  // Wrong
const token = request.headers["authorization"];   // Wrong
```

### "User does not have permission"

**Cause**: Token user lacks SQL Warehouse access

**Solution**:
1. Check SQL Warehouse permissions in Databricks workspace
2. Grant "Can use" permission to user or group

---

## Timeouts

### "Read timed out" / "Socket timeout"

**Cause**: Query execution time exceeded timeout

**Solution**:

**Python**:
```python
connection = sql.connect(
    ...,
    _socket_timeout=300,  # Extend to 5 minutes
)
```

**Node.js**:
```typescript
await client.connect({
    ...,
    socketTimeout: 300000,  // 5 minutes (milliseconds)
});
```

---

## SQL Errors

### "Table or view not found"

**Cause**: Table doesn't exist or missing catalog/schema specification

**Solution**:
```sql
-- Use 3-level namespace
SELECT * FROM catalog.schema.table

-- Or set defaults at connection time
-- Python
connection = sql.connect(..., catalog="main", schema="default")

-- Node.js
const session = await client.openSession({
    initialCatalog: "main",
    initialSchema: "default",
});
```

### "PARSE_SYNTAX_ERROR"

**Cause**: SQL syntax error

**Common mistakes**:
```sql
-- Wrong: Backticks not supported
SELECT * FROM `my-table`

-- Correct: Use double quotes for identifiers
SELECT * FROM "my-table"
```

---

## Performance Issues

### Slow queries

**Check**:
1. SQL Warehouse size is appropriate
2. Review query plan (use `EXPLAIN`)
3. Proper filtering is applied

```sql
-- Check query plan
EXPLAIN SELECT * FROM large_table WHERE date = '2024-01-01'
```

### Out of memory

**Cause**: Fetching too much data at once

**Solution**:
```python
# Fetch in chunks
cursor.execute("SELECT * FROM large_table")
while True:
    rows = cursor.fetchmany(10000)
    if not rows:
        break
    process(rows)
```

```typescript
// Fetch in chunks
const operation = await session.executeStatement("SELECT * FROM large_table");
let chunk = await operation.fetchChunk({ maxRows: 10000 });
while (chunk.length > 0) {
    process(chunk);
    chunk = await operation.fetchChunk({ maxRows: 10000 });
}
```

---

## Debugging Tips

### Enable Logging

**Python**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("databricks.sql").setLevel(logging.DEBUG)
```

**Node.js**:
```typescript
import { DBSQLClient, DBSQLLogger, LogLevel } from "@databricks/sql";

const client = new DBSQLClient({
    logger: new DBSQLLogger({ level: LogLevel.debug }),
});
```

### Connection Test

Verify connection with minimal query:

```python
cursor.execute("SELECT 1")
print(cursor.fetchone())  # (1,) means success
```

```typescript
const operation = await session.executeStatement("SELECT 1");
console.log(await operation.fetchAll());  // [{ 1: 1 }] means success
```
