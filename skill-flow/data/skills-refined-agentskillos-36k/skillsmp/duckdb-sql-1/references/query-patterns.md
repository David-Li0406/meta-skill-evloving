# Query Patterns Reference

## Table of Contents

- [Multi-File Queries](#multi-file-queries)
- [Common Query Patterns](#common-query-patterns)
- [CSV File Considerations](#csv-file-considerations)

---

## Multi-File Queries

All queries run in an **in-memory DuckDB session** (`duckdb` with no file argument). Use these patterns:

### Single .ddb File

```sql
ATTACH IF NOT EXISTS 'data/sales.ddb' AS _db_sales (READ_ONLY);

SELECT * FROM _db_sales.customers;
```

### Multiple .ddb Files

```sql
ATTACH IF NOT EXISTS 'data/sales.ddb' AS _db_sales (READ_ONLY);
ATTACH IF NOT EXISTS 'data/inventory.ddb' AS _db_inventory (READ_ONLY);

SELECT c.name, o.total_amount, p.name AS product_name
FROM _db_sales.customers c
JOIN _db_sales.orders o ON c.customer_id = o.customer_id
JOIN _db_inventory.products p ON o.product_id = p.product_id;
```

### CSV/Parquet Files (no ATTACH needed)

CSV and Parquet files are queried directly by file path:

```sql
-- Join two CSV files
SELECT o.*, c.name AS customer_name
FROM 'data/orders.csv' o
JOIN 'data/customers.csv' c ON o.customer_id = c.customer_id;

-- Join CSV to Parquet
SELECT *
FROM 'data/events.parquet' e
JOIN 'data/metadata.csv' m ON e.event_type = m.type_code;
```

### Mixed: .ddb + CSV/Parquet

```sql
ATTACH IF NOT EXISTS 'data/sales.ddb' AS _db_sales (READ_ONLY);

SELECT
    c.name,
    t.amount,
    t.transaction_date
FROM _db_sales.customers c
JOIN 'data/transactions.csv' t ON c.customer_id = t.customer_id;
```

### Glob Patterns (multiple files as one table)

```sql
-- All CSV files in directory
SELECT * FROM 'logs/*.csv';

-- With column alignment for varying schemas
SELECT * FROM read_csv('data/*.csv', union_by_name=true);

-- Multiple Parquet files
SELECT * FROM 'data/partitions/*.parquet';
```

---

## Common Query Patterns

### Optional Filters Pattern

Use `WHERE 1=1` when building queries with multiple optional filters:

```sql
SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.name AS customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE 1=1
  AND o.order_date >= '2024-01-01'     -- required filter
  AND o.order_date < '2024-02-01'       -- required filter
  -- Add optional filters below as needed:
  -- AND o.status = 'pending'
  -- AND c.customer_id = 123
ORDER BY o.order_date DESC;
```

### Soft Delete Handling

If a table has a `deleted` or `is_deleted` column:

```sql
-- Include only non-deleted records
WHERE deleted IS NULL OR deleted = false

-- Or using COALESCE
WHERE COALESCE(deleted, false) = false
```

### Date Range Best Practices

```sql
-- GOOD: Use >= and < (half-open interval)
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01'

-- AVOID: BETWEEN is inclusive on both ends
-- This includes all of Jan 1 AND all of Feb 1
WHERE created_at BETWEEN '2024-01-01' AND '2024-02-01'

-- Relative date ranges
WHERE order_date >= current_date - INTERVAL '30 days'
WHERE order_date >= date_trunc('month', current_date)
```

### Aggregation with Filters

```sql
-- Filter before aggregating for performance
SELECT
    status,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY status
ORDER BY order_count DESC;
```

### Counting with Conditions

```sql
-- Count specific conditions within groups
SELECT
    customer_id,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_orders,
    COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled_orders
FROM orders
GROUP BY customer_id;
```

### Safe Division (Avoid Divide by Zero)

```sql
-- Using NULLIF to avoid division by zero
SELECT
    customer_id,
    completed_orders * 100.0 / NULLIF(total_orders, 0) as completion_rate
FROM customer_stats;
```

### Finding Duplicates

```sql
-- Find duplicate values
SELECT column_name, COUNT(*) as count
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1
ORDER BY count DESC;
```

### Latest Record Per Group

```sql
-- Using window function
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
  FROM orders
)
SELECT * FROM ranked WHERE rn = 1;

-- Using DISTINCT ON (DuckDB supports this)
SELECT DISTINCT ON (customer_id) *
FROM orders
ORDER BY customer_id, order_date DESC;
```

---

## CSV File Considerations

DuckDB auto-detects CSV file properties (delimiter, header row, column types) in most cases. No configuration is typically needed.

### Auto-Detection (Default Behavior)

DuckDB automatically detects:
- **Delimiter**: comma, tab, pipe, semicolon, etc.
- **Header row**: presence of column names
- **Column types**: INTEGER, VARCHAR, DATE, etc.
- **Quote character**: double quotes, single quotes
- **Null values**: empty strings, "NULL", etc.

### When Auto-Detection Fails

If DuckDB produces unexpected results (wrong types, mangled data), the user can request explicit options conversationally:
- "Use tab delimiter for this file"
- "The CSV uses semicolon as delimiter"
- "Skip the first 2 rows"
- "Treat empty strings as NULL"

**Explicit options syntax:**
```sql
SELECT * FROM read_csv('/path/to/file.csv',
  header=true,           -- First row contains headers
  delim='\t',            -- Tab-delimited
  skip=2,                -- Skip first N rows
  nullstr='NA',          -- Treat 'NA' as NULL
  columns={'id': 'INTEGER', 'name': 'VARCHAR'}  -- Force column types
);
```

### Large CSV Files

For large CSV files:
- DuckDB streams data efficiently, but queries may be slower than indexed .ddb files
- Consider converting to .parquet or .ddb for frequently-queried data
- Use `LIMIT` when exploring to avoid loading entire file
