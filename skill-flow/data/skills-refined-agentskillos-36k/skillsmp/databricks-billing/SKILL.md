---
name: databricks-billing
description: |
  Databricks billing data analysis and cost calculation using system.billing tables.
  Triggers: cost analysis, billing report, DBU usage, SKU costs, monthly expenses, job costs, warehouse costs, spending breakdown.
  Uses mcp__databricks__run_sql for queries. Cost calculations require joining usage with list_prices.
metadata:
  version: 1.0.0
---

# Databricks Billing

## Quick Reference

| Analysis Type | Table | Key Columns |
|---------------|-------|-------------|
| DBU consumption | `system.billing.usage` | `usage_date`, `sku_name`, `usage_quantity` |
| SKU pricing | `system.billing.list_prices` | `sku_name`, `pricing.default`, `price_start_time` |
| Job costs | `usage` + `usage_metadata.job_id` | `job_name` available in `usage_metadata` |
| Warehouse costs | `usage` + `usage_metadata.warehouse_id` | Join with `system.compute.warehouses` |
| Cluster costs | `usage` + `usage_metadata.cluster_id` | Join with `system.compute.clusters` |

## Cost Calculation Pattern

Always use this CTE pattern for accurate cost calculations:

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
)
SELECT
  u.usage_date,
  u.sku_name,
  u.usage_quantity AS dbu,
  p.pricing.default AS unit_price,
  u.usage_quantity * p.pricing.default AS cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
```

**Key points:**
- Use `BROADCAST` hint for efficient join (prices table is small)
- Handle `price_end_time` NULL with `COALESCE`
- Filter by date range to limit scan
- Use `HAVING SUM(usage_quantity) != 0` to handle correction records (see below)

## Table Schemas

### system.billing.usage

| Column | Type | Description |
|--------|------|-------------|
| `record_id` | STRING | Unique record identifier |
| `workspace_id` | STRING | Workspace ID |
| `sku_name` | STRING | SKU (e.g., `JOBS_COMPUTE`, `SQL_COMPUTE`) |
| `usage_date` | DATE | Usage date |
| `usage_quantity` | DECIMAL | DBU amount |
| `record_type` | STRING | `ORIGINAL`, `RETRACTION`, `RESTATEMENT` |
| `usage_metadata` | STRUCT | Detailed context (see below) |

**usage_metadata fields:**
- `cluster_id`, `warehouse_id`, `job_id`, `job_run_id`, `job_name`
- `notebook_id`, `dlt_pipeline_id`, `endpoint_id`, `endpoint_name`

### system.billing.list_prices

| Column | Type | Description |
|--------|------|-------------|
| `sku_name` | STRING | SKU identifier |
| `pricing.default` | DECIMAL | Default unit price |
| `currency_code` | STRING | Currency (USD, JPY, etc.) |
| `price_start_time` | TIMESTAMP | Price effective start |
| `price_end_time` | TIMESTAMP | Price effective end (NULL = current) |

## Correction Records

Billing data includes corrections:
- `ORIGINAL` - Initial record
- `RETRACTION` - Cancels previous (negative quantity)
- `RESTATEMENT` - Corrected replacement

For accurate totals, filter zero-sum corrections:

```sql
SELECT sku_name, SUM(usage_quantity) AS net_dbu
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY sku_name
HAVING SUM(usage_quantity) != 0
```

## Common Queries

### Monthly Cost by SKU

```sql
WITH prices AS (
  SELECT sku_name, usage_unit, pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
)
SELECT
  DATE_TRUNC('month', u.usage_date) AS month,
  u.sku_name,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date AND u.usage_date < p.price_end_date
WHERE u.usage_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL 3 MONTHS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY month DESC, total_cost DESC
```

### Job Cost (Top 20)

```sql
WITH prices AS (
  SELECT sku_name, usage_unit, pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
)
SELECT
  u.usage_metadata.job_id,
  u.usage_metadata.job_name,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date AND u.usage_date < p.price_end_date
WHERE u.usage_metadata.job_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
LIMIT 20
```

### SQL Warehouse Cost

```sql
WITH prices AS (
  SELECT sku_name, usage_unit, pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
)
SELECT
  u.usage_metadata.warehouse_id,
  w.name AS warehouse_name,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date AND u.usage_date < p.price_end_date
LEFT JOIN system.compute.warehouses w
  ON u.usage_metadata.warehouse_id = w.warehouse_id
WHERE u.usage_metadata.warehouse_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
```

## Query Optimization Tips

System tables can contain large volumes of data. Follow these practices to minimize query cost and improve performance:

- **Always filter by date range**: Use `WHERE usage_date >= CURRENT_DATE - INTERVAL N DAYS` to limit scans
- **Use BROADCAST hint**: The `list_prices` table is small; use `/*+ BROADCAST(p) */` for efficient joins
- **Avoid SELECT ***: Only select columns you need from `usage_metadata` struct
- **Use LIMIT for exploration**: Add `LIMIT` when exploring data patterns before running full aggregations

**For recurring reports**, consider:

```sql
-- Create a Materialized View for frequently accessed cost summaries
CREATE MATERIALIZED VIEW billing.daily_costs AS
SELECT
  usage_date,
  sku_name,
  SUM(usage_quantity) AS total_dbu
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 90 DAYS
GROUP BY usage_date, sku_name;

-- Refresh periodically
REFRESH MATERIALIZED VIEW billing.daily_costs;
```

## Notes & Limitations

1. **Data Latency**: Billing data is not real-time; updated throughout the day
2. **Price Changes**: Use time-aware joins for accurate historical costs
3. **Currency**: Check `currency_code` in `list_prices` for billing currency
4. **Interactive Cluster**: Shared cluster usage cannot be attributed to individual users

## Permissions

```sql
GRANT USE CATALOG ON CATALOG system TO <principal>;
GRANT USE SCHEMA ON SCHEMA system.billing TO <principal>;
GRANT SELECT ON SCHEMA system.billing TO <principal>;
```

## References

- [Query Patterns](references/query-patterns.md): Workspace, cluster, DLT, model serving cost queries
- [Advanced Analysis](references/advanced-analysis.md): Month-over-month comparison, anomaly detection, top contributors
