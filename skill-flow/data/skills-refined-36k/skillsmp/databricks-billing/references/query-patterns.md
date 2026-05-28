# Databricks Billing Query Patterns

Detailed query examples for various cost analysis scenarios.

## Table of Contents

- [Workspace Cost Breakdown](#workspace-cost-breakdown)
- [Daily Cost Trend](#daily-cost-trend)
- [Cluster Cost Analysis](#cluster-cost-analysis)
- [Model Serving Cost](#model-serving-cost)
- [DLT Pipeline Cost](#dlt-pipeline-cost)
- [SKU Price History](#sku-price-history)

## Workspace Cost Breakdown

Analyze costs by workspace:

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
  u.workspace_id,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY u.workspace_id
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
```

## Daily Cost Trend

Track daily spending:

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
  SUM(u.usage_quantity) AS daily_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS daily_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY u.usage_date
ORDER BY u.usage_date
```

## Cluster Cost Analysis

Cost breakdown by cluster:

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
  u.usage_metadata.cluster_id,
  c.cluster_name,
  u.sku_name,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
LEFT JOIN system.compute.clusters c
  ON u.usage_metadata.cluster_id = c.cluster_id
WHERE u.usage_metadata.cluster_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
LIMIT 20
```

## Model Serving Cost

Costs for model serving endpoints:

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
  u.usage_metadata.endpoint_name,
  u.usage_metadata.endpoint_id,
  u.sku_name,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_metadata.endpoint_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
```

## DLT Pipeline Cost

Delta Live Tables pipeline costs:

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
  u.usage_metadata.dlt_pipeline_id,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_metadata.dlt_pipeline_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY u.usage_metadata.dlt_pipeline_id
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
```

## SKU Price History

View SKU pricing changes over time:

```sql
SELECT
  sku_name,
  usage_unit,
  pricing.default AS price,
  price_start_time,
  price_end_time,
  currency_code
FROM system.billing.list_prices
ORDER BY sku_name, price_start_time DESC
```

### Current Prices Only

```sql
SELECT
  sku_name,
  usage_unit,
  pricing.default AS price,
  currency_code
FROM system.billing.list_prices
WHERE price_end_time IS NULL
ORDER BY sku_name
```

### Price by SKU Category

```sql
SELECT
  CASE
    WHEN sku_name LIKE '%JOBS%' THEN 'Jobs Compute'
    WHEN sku_name LIKE '%SQL%' THEN 'SQL Warehouse'
    WHEN sku_name LIKE '%ALL_PURPOSE%' THEN 'All-Purpose Compute'
    WHEN sku_name LIKE '%DLT%' THEN 'Delta Live Tables'
    WHEN sku_name LIKE '%SERVERLESS%' THEN 'Serverless'
    WHEN sku_name LIKE '%MODEL%' OR sku_name LIKE '%SERVING%' THEN 'Model Serving'
    ELSE 'Other'
  END AS category,
  sku_name,
  pricing.default AS price,
  currency_code
FROM system.billing.list_prices
WHERE price_end_time IS NULL
ORDER BY category, price DESC
```
