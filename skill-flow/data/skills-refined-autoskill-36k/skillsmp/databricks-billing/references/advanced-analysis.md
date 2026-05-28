# Databricks Billing Advanced Analysis

Advanced queries for cost comparison, anomaly detection, and contributor analysis.

## Table of Contents

- [Month-over-Month Comparison](#month-over-month-comparison)
- [Top Cost Contributors](#top-cost-contributors)
- [Cost Anomaly Detection](#cost-anomaly-detection)
- [Cost Forecasting](#cost-forecasting)
- [SKU Category Analysis](#sku-category-analysis)

## Month-over-Month Comparison

Compare costs across months with change percentage:

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
monthly AS (
  SELECT
    DATE_TRUNC('month', u.usage_date) AS month,
    SUM(u.usage_quantity * p.pricing.default) AS total_cost
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL 6 MONTHS
  GROUP BY month
)
SELECT
  month,
  total_cost,
  LAG(total_cost) OVER (ORDER BY month) AS prev_month_cost,
  total_cost - LAG(total_cost) OVER (ORDER BY month) AS cost_change,
  CASE
    WHEN LAG(total_cost) OVER (ORDER BY month) IS NULL
         OR LAG(total_cost) OVER (ORDER BY month) = 0 THEN NULL
    ELSE ROUND((total_cost - LAG(total_cost) OVER (ORDER BY month))
         / LAG(total_cost) OVER (ORDER BY month) * 100, 2)
  END AS pct_change
FROM monthly
ORDER BY month DESC
```

### By SKU

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
monthly AS (
  SELECT
    DATE_TRUNC('month', u.usage_date) AS month,
    u.sku_name,
    SUM(u.usage_quantity * p.pricing.default) AS total_cost
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL 2 MONTHS
  GROUP BY ALL
)
SELECT
  sku_name,
  month,
  total_cost,
  LAG(total_cost) OVER (PARTITION BY sku_name ORDER BY month) AS prev_month,
  CASE
    WHEN LAG(total_cost) OVER (PARTITION BY sku_name ORDER BY month) IS NULL
         OR LAG(total_cost) OVER (PARTITION BY sku_name ORDER BY month) = 0 THEN NULL
    ELSE ROUND((total_cost - LAG(total_cost) OVER (PARTITION BY sku_name ORDER BY month))
         / LAG(total_cost) OVER (PARTITION BY sku_name ORDER BY month) * 100, 2)
  END AS pct_change
FROM monthly
ORDER BY sku_name, month DESC
```

## Top Cost Contributors

### Top Jobs by Cost

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
  u.usage_metadata.job_id,
  u.usage_metadata.job_name,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost,
  ROUND(SUM(u.usage_quantity * p.pricing.default) * 100.0 /
    SUM(SUM(u.usage_quantity * p.pricing.default)) OVER (), 2) AS pct_of_total
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_metadata.job_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
LIMIT 10
```

### Top Warehouses by Cost

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
  u.usage_metadata.warehouse_id,
  w.name AS warehouse_name,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost,
  ROUND(SUM(u.usage_quantity * p.pricing.default) * 100.0 /
    SUM(SUM(u.usage_quantity * p.pricing.default)) OVER (), 2) AS pct_of_total
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
LEFT JOIN system.compute.warehouses w
  ON u.usage_metadata.warehouse_id = w.warehouse_id
WHERE u.usage_metadata.warehouse_id IS NOT NULL
  AND u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
LIMIT 10
```

## Cost Anomaly Detection

### Daily Spike Detection (Z-Score)

Identify days with unusually high spending:

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
daily_costs AS (
  SELECT
    u.usage_date,
    SUM(u.usage_quantity * p.pricing.default) AS daily_cost
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
  GROUP BY u.usage_date
),
stats AS (
  SELECT
    AVG(daily_cost) AS avg_cost,
    STDDEV(daily_cost) AS stddev_cost
  FROM daily_costs
)
SELECT
  d.usage_date,
  d.daily_cost,
  s.avg_cost,
  CASE
    WHEN s.stddev_cost IS NULL OR s.stddev_cost = 0 THEN NULL
    ELSE ROUND((d.daily_cost - s.avg_cost) / s.stddev_cost, 2)
  END AS z_score,
  CASE
    WHEN s.stddev_cost IS NULL OR s.stddev_cost = 0 THEN 'INSUFFICIENT_DATA'
    WHEN (d.daily_cost - s.avg_cost) / s.stddev_cost > 3 THEN 'CRITICAL'
    WHEN (d.daily_cost - s.avg_cost) / s.stddev_cost > 2 THEN 'WARNING'
    ELSE 'NORMAL'
  END AS severity
FROM daily_costs d
CROSS JOIN stats s
WHERE s.stddev_cost > 0
  AND ABS((d.daily_cost - s.avg_cost) / s.stddev_cost) > 2
ORDER BY d.usage_date DESC
```

### SKU Anomaly Detection

Detect unusual SKU usage patterns:

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
daily_sku AS (
  SELECT
    u.usage_date,
    u.sku_name,
    SUM(u.usage_quantity * p.pricing.default) AS daily_cost
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
  GROUP BY ALL
),
stats AS (
  SELECT
    sku_name,
    AVG(daily_cost) AS avg_cost,
    STDDEV(daily_cost) AS stddev_cost
  FROM daily_sku
  GROUP BY sku_name
)
SELECT
  d.usage_date,
  d.sku_name,
  d.daily_cost,
  s.avg_cost,
  ROUND((d.daily_cost - s.avg_cost) / NULLIF(s.stddev_cost, 0), 2) AS z_score
FROM daily_sku d
JOIN stats s ON d.sku_name = s.sku_name
WHERE s.stddev_cost IS NOT NULL
  AND s.stddev_cost > 0
  AND ABS((d.daily_cost - s.avg_cost) / s.stddev_cost) > 2
ORDER BY d.usage_date DESC, z_score DESC
```

## Cost Forecasting

### Moving Average Forecast

Simple moving average projection:

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
daily_costs AS (
  SELECT
    u.usage_date,
    SUM(u.usage_quantity * p.pricing.default) AS daily_cost
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
  GROUP BY u.usage_date
)
SELECT
  usage_date,
  daily_cost,
  AVG(daily_cost) OVER (ORDER BY usage_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d,
  AVG(daily_cost) OVER () * DAY(LAST_DAY(CURRENT_DATE)) AS projected_monthly_cost
FROM daily_costs
ORDER BY usage_date DESC
```

### Month-to-Date Projection

```sql
WITH prices AS (
  SELECT
    sku_name,
    usage_unit,
    pricing,
    DATE(price_start_time) AS price_start_date,
    DATE(COALESCE(price_end_time, '9999-12-31')) AS price_end_date
  FROM system.billing.list_prices
),
mtd AS (
  SELECT
    SUM(u.usage_quantity * p.pricing.default) AS mtd_cost,
    COUNT(DISTINCT u.usage_date) AS days_elapsed,
    DAY(LAST_DAY(CURRENT_DATE)) AS days_in_month
  FROM system.billing.usage u
  LEFT JOIN prices p /*+ BROADCAST(p) */
    ON u.sku_name = p.sku_name
    AND u.usage_unit = p.usage_unit
    AND u.usage_date >= p.price_start_date
    AND u.usage_date < p.price_end_date
  WHERE u.usage_date >= DATE_TRUNC('month', CURRENT_DATE)
)
SELECT
  mtd_cost,
  days_elapsed,
  days_in_month,
  CASE
    WHEN days_elapsed = 0 THEN NULL
    ELSE ROUND(mtd_cost / days_elapsed * days_in_month, 2)
  END AS projected_month_total
FROM mtd
```

## SKU Category Analysis

Group and analyze costs by SKU category:

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
  CASE
    WHEN u.sku_name LIKE '%JOBS%' THEN 'Jobs Compute'
    WHEN u.sku_name LIKE '%SQL%' THEN 'SQL Warehouse'
    WHEN u.sku_name LIKE '%ALL_PURPOSE%' THEN 'All-Purpose Compute'
    WHEN u.sku_name LIKE '%DLT%' THEN 'Delta Live Tables'
    WHEN u.sku_name LIKE '%SERVERLESS%' THEN 'Serverless'
    WHEN u.sku_name LIKE '%MODEL%' OR u.sku_name LIKE '%SERVING%' THEN 'Model Serving'
    ELSE 'Other'
  END AS category,
  SUM(u.usage_quantity) AS total_dbu,
  SUM(u.usage_quantity * p.pricing.default) AS total_cost,
  ROUND(SUM(u.usage_quantity * p.pricing.default) * 100.0 /
    SUM(SUM(u.usage_quantity * p.pricing.default)) OVER (), 2) AS pct_of_total
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
HAVING SUM(u.usage_quantity) != 0
ORDER BY total_cost DESC
```

### Category Trend Over Time

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
  DATE_TRUNC('week', u.usage_date) AS week,
  CASE
    WHEN u.sku_name LIKE '%JOBS%' THEN 'Jobs'
    WHEN u.sku_name LIKE '%SQL%' THEN 'SQL'
    WHEN u.sku_name LIKE '%ALL_PURPOSE%' THEN 'Interactive'
    WHEN u.sku_name LIKE '%DLT%' THEN 'DLT'
    ELSE 'Other'
  END AS category,
  SUM(u.usage_quantity * p.pricing.default) AS weekly_cost
FROM system.billing.usage u
LEFT JOIN prices p /*+ BROADCAST(p) */
  ON u.sku_name = p.sku_name
  AND u.usage_unit = p.usage_unit
  AND u.usage_date >= p.price_start_date
  AND u.usage_date < p.price_end_date
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 12 WEEKS
GROUP BY ALL
ORDER BY week DESC, weekly_cost DESC
```
