# Python SDK (databricks-sql-connector)

## Installation

```bash
pip install databricks-sql-connector
```

## Connection Options

```python
from databricks import sql

connection = sql.connect(
    server_hostname="<workspace>.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/<warehouse_id>",
    access_token="<token>",
    # Optional
    catalog="main",           # Default catalog
    schema="default",         # Default schema
    _socket_timeout=60,       # Socket timeout (seconds)
)
```

## Parameter Binding

Always use parameter binding to prevent SQL injection.

```python
# Positional parameters
cursor.execute(
    "SELECT * FROM users WHERE id = %s AND status = %s",
    [user_id, "active"]
)

# Named parameters
cursor.execute(
    "SELECT * FROM users WHERE id = %(user_id)s AND status = %(status)s",
    {"user_id": user_id, "status": "active"}
)
```

## Fetching Results

```python
# Fetch all rows
rows = cursor.fetchall()

# Fetch one row
row = cursor.fetchone()

# Fetch N rows
rows = cursor.fetchmany(100)

# Get column names
columns = [desc[0] for desc in cursor.description]

# Get results as dict
rows = cursor.fetchall()
result = [dict(zip(columns, row)) for row in rows]
```

## Large Data Processing

### Chunk Processing

```python
cursor.execute("SELECT * FROM large_table")
while True:
    rows = cursor.fetchmany(1000)
    if not rows:
        break
    process_batch(rows)
```

### Arrow Format

Use Arrow format for efficient large data processing.

```python
cursor.execute("SELECT * FROM large_table")
arrow_table = cursor.fetchall_arrow()

# Convert to Pandas DataFrame
df = arrow_table.to_pandas()
```

## Context Manager

Use `with` statement to prevent resource leaks.

```python
with sql.connect(...) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
# Automatically closed
```

## Databricks Apps Implementation Example

```python
from fastapi import FastAPI, Request, HTTPException
from databricks import sql
import os

app = FastAPI()

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
SQL_WAREHOUSE_PATH = os.environ.get("SQL_WAREHOUSE_HTTP_PATH")

@app.get("/api/users")
async def get_users(request: Request):
    access_token = request.headers.get("x-forwarded-access-token")
    if not access_token:
        raise HTTPException(status_code=401, detail="No access token")

    with sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=SQL_WAREHOUSE_PATH,
        access_token=access_token
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM catalog.schema.users LIMIT 100")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
```

## Error Handling

```python
from databricks.sql.exc import (
    Error,
    DatabaseError,
    OperationalError,
    ProgrammingError,
)

try:
    with sql.connect(...) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM nonexistent_table")
except ProgrammingError as e:
    # SQL syntax error, table not found, etc.
    print(f"SQL Error: {e}")
except OperationalError as e:
    # Connection error, timeout, etc.
    print(f"Connection Error: {e}")
except DatabaseError as e:
    # Other database errors
    print(f"Database Error: {e}")
except Error as e:
    # All databricks-sql-connector errors
    print(f"Error: {e}")
```
