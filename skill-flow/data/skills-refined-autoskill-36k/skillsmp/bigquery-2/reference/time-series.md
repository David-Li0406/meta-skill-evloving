# Advanced Time-Series Features

This guide covers time-series feature engineering patterns for recommendation systems.

## Lag and Rolling Windows

```sql
CREATE OR REPLACE TABLE `project.features.user_time_series` AS
SELECT
  user_id,
  event_date,
  daily_events,
  daily_revenue,
  -- Lag features (previous values)
  LAG(daily_events, 1) OVER w_user as events_yesterday,
  LAG(daily_events, 7) OVER w_user as events_last_week,
  LAG(daily_revenue, 1) OVER w_user as revenue_yesterday,
  LAG(daily_revenue, 30) OVER w_user as revenue_last_month,

  -- Rolling windows
  AVG(daily_events) OVER w7 as events_7day_avg,
  STDDEV(daily_events) OVER w7 as events_7day_stddev,
  SUM(daily_revenue) OVER w30 as revenue_30day_sum,
  AVG(daily_revenue) OVER w30 as revenue_30day_avg,

  -- Exponential moving average (approximate)
  AVG(daily_events) OVER (
    PARTITION BY user_id
    ORDER BY event_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as ema_7day,

  -- Trend detection with linear regression
  REGR_SLOPE(daily_events, DATE_DIFF(event_date, DATE('2024-01-01'), DAY))
    OVER w30 as trend_slope,
  REGR_INTERCEPT(daily_events, DATE_DIFF(event_date, DATE('2024-01-01'), DAY))
    OVER w30 as trend_intercept,

  -- Ratio features
  SAFE_DIVIDE(daily_events, LAG(daily_events, 7) OVER w_user) as events_wow_ratio,
  SAFE_DIVIDE(daily_revenue, LAG(daily_revenue, 7) OVER w_user) as revenue_wow_ratio

FROM user_daily_aggregates
WINDOW
  w7 AS (PARTITION BY user_id ORDER BY event_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),
  w30 AS (PARTITION BY user_id ORDER BY event_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),
  w_user AS (PARTITION BY user_id ORDER BY event_date);
```

## Seasonality Features

### Cyclical Encoding

```sql
SELECT
  user_id,
  event_date,
  -- Cyclical encoding for time features
  SIN(2 * ACOS(-1) * EXTRACT(DAYOFWEEK FROM event_date) / 7) as day_of_week_sin,
  COS(2 * ACOS(-1) * EXTRACT(DAYOFWEEK FROM event_date) / 7) as day_of_week_cos,
  SIN(2 * ACOS(-1) * EXTRACT(MONTH FROM event_date) / 12) as month_sin,
  COS(2 * ACOS(-1) * EXTRACT(MONTH FROM event_date) / 12) as month_cos,
  SIN(2 * ACOS(-1) * EXTRACT(HOUR FROM event_timestamp) / 24) as hour_sin,
  COS(2 * ACOS(-1) * EXTRACT(HOUR FROM event_timestamp) / 24) as hour_cos,

  -- Seasonal indicators
  CASE EXTRACT(DAYOFWEEK FROM event_date)
    WHEN 1 THEN 1 WHEN 7 THEN 1 ELSE 0
  END as is_weekend,

  CASE
    WHEN EXTRACT(MONTH FROM event_date) IN (11, 12) THEN 1 ELSE 0
  END as is_holiday_season,

  CASE
    WHEN EXTRACT(MONTH FROM event_date) IN (6, 7, 8) THEN 1 ELSE 0
  END as is_summer,

  -- Business hour indicator
  CASE
    WHEN EXTRACT(HOUR FROM event_timestamp) BETWEEN 9 AND 17
      AND EXTRACT(DAYOFWEEK FROM event_date) NOT IN (1, 7) THEN 1
    ELSE 0
  END as is_business_hours

FROM user_events;
```

### Holiday Detection

```sql
-- Create holiday calendar table
CREATE OR REPLACE TABLE `project.features.holiday_calendar` AS
SELECT
  holiday_date,
  holiday_name,
  holiday_type,
  country
FROM (
  SELECT DATE('2024-01-01') as holiday_date, 'New Year' as holiday_name, 'major' as holiday_type, 'US' as country
  UNION ALL SELECT DATE('2024-07-04'), 'Independence Day', 'major', 'US'
  UNION ALL SELECT DATE('2024-11-28'), 'Thanksgiving', 'major', 'US'
  UNION ALL SELECT DATE('2024-12-25'), 'Christmas', 'major', 'US'
  UNION ALL SELECT DATE('2024-02-14'), 'Valentine Day', 'shopping', 'US'
  UNION ALL SELECT DATE('2024-11-29'), 'Black Friday', 'shopping', 'US'
);

-- Add holiday features
SELECT
  e.user_id,
  e.event_date,
  COALESCE(h.holiday_name, 'none') as holiday,
  COALESCE(h.holiday_type, 'none') as holiday_type,

  -- Days until next major holiday
  MIN(DATE_DIFF(h2.holiday_date, e.event_date, DAY)) as days_to_next_holiday,

  -- Days since last major holiday
  MIN(DATE_DIFF(e.event_date, h3.holiday_date, DAY)) as days_since_last_holiday

FROM user_events e
LEFT JOIN `project.features.holiday_calendar` h
  ON e.event_date = h.holiday_date
LEFT JOIN `project.features.holiday_calendar` h2
  ON h2.holiday_date > e.event_date AND h2.holiday_type = 'major'
LEFT JOIN `project.features.holiday_calendar` h3
  ON h3.holiday_date < e.event_date AND h3.holiday_type = 'major'
GROUP BY e.user_id, e.event_date, h.holiday_name, h.holiday_type;
```

## Time-Based Aggregations

### Different Time Granularities

```sql
CREATE OR REPLACE TABLE `project.features.user_temporal_features` AS
WITH hourly_agg AS (
  SELECT
    user_id,
    TIMESTAMP_TRUNC(event_timestamp, HOUR) as hour,
    COUNT(*) as hourly_events
  FROM user_events
  GROUP BY user_id, hour
),
daily_agg AS (
  SELECT
    user_id,
    DATE(event_timestamp) as day,
    COUNT(*) as daily_events,
    SUM(purchase_amount) as daily_revenue
  FROM user_events
  GROUP BY user_id, day
),
weekly_agg AS (
  SELECT
    user_id,
    DATE_TRUNC(DATE(event_timestamp), WEEK) as week,
    COUNT(*) as weekly_events,
    SUM(purchase_amount) as weekly_revenue
  FROM user_events
  GROUP BY user_id, week
)
SELECT
  d.user_id,
  d.day,
  d.daily_events,
  d.daily_revenue,

  -- Average hourly events for this day
  AVG(h.hourly_events) as avg_hourly_events,
  MAX(h.hourly_events) as peak_hourly_events,

  -- Weekly context
  w.weekly_events,
  w.weekly_revenue,

  -- Day of week comparison
  AVG(d.daily_events) OVER (
    PARTITION BY d.user_id, EXTRACT(DAYOFWEEK FROM d.day)
  ) as avg_events_this_weekday

FROM daily_agg d
LEFT JOIN hourly_agg h
  ON d.user_id = h.user_id
  AND DATE(h.hour) = d.day
LEFT JOIN weekly_agg w
  ON d.user_id = w.user_id
  AND DATE_TRUNC(d.day, WEEK) = w.week
GROUP BY d.user_id, d.day, d.daily_events, d.daily_revenue, w.weekly_events, w.weekly_revenue;
```

## Recency, Frequency, Monetary (RFM) Features

```sql
CREATE OR REPLACE TABLE `project.features.user_rfm` AS
SELECT
  user_id,
  -- Recency: days since last activity
  DATE_DIFF(CURRENT_DATE(), MAX(DATE(event_timestamp)), DAY) as recency_days,

  -- Frequency: activity metrics
  COUNT(DISTINCT DATE(event_timestamp)) as frequency_visit_days,
  COUNT(*) as frequency_total_events,

  -- Monetary: spending metrics
  SUM(purchase_amount) as monetary_total_spent,
  AVG(purchase_amount) as monetary_avg_order_value,
  COUNTIF(event_type = 'purchase') as monetary_purchase_count,

  -- Time-based RFM segments
  CASE
    WHEN DATE_DIFF(CURRENT_DATE(), MAX(DATE(event_timestamp)), DAY) <= 7 THEN 5
    WHEN DATE_DIFF(CURRENT_DATE(), MAX(DATE(event_timestamp)), DAY) <= 30 THEN 4
    WHEN DATE_DIFF(CURRENT_DATE(), MAX(DATE(event_timestamp)), DAY) <= 90 THEN 3
    WHEN DATE_DIFF(CURRENT_DATE(), MAX(DATE(event_timestamp)), DAY) <= 180 THEN 2
    ELSE 1
  END as recency_score,

  CASE
    WHEN COUNT(DISTINCT DATE(event_timestamp)) >= 50 THEN 5
    WHEN COUNT(DISTINCT DATE(event_timestamp)) >= 20 THEN 4
    WHEN COUNT(DISTINCT DATE(event_timestamp)) >= 10 THEN 3
    WHEN COUNT(DISTINCT DATE(event_timestamp)) >= 5 THEN 2
    ELSE 1
  END as frequency_score,

  CASE
    WHEN SUM(purchase_amount) >= 10000 THEN 5
    WHEN SUM(purchase_amount) >= 5000 THEN 4
    WHEN SUM(purchase_amount) >= 1000 THEN 3
    WHEN SUM(purchase_amount) >= 100 THEN 2
    ELSE 1
  END as monetary_score

FROM user_events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
GROUP BY user_id;
```

## Best Practices

- Use window functions for lag and rolling features
- Encode cyclical time features (hour, day, month) with sin/cos transformations
- Create RFM scores for user segmentation
- Track seasonal patterns and holidays
- Compute features at multiple time granularities (hourly, daily, weekly)
- Use DATE_TRUNC for consistent weekly/monthly aggregations
- Add ratio features (week-over-week, month-over-month) for trend detection
- Consider timezone when working with timestamps
