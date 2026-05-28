---
name: clickhouse-io
description: ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads.
---

# ClickHouse Analytics Patterns

ClickHouse-specific patterns for high-performance analytics and data engineering.

## Overview

ClickHouse is a column-oriented database management system (DBMS) for online analytical processing (OLAP). It's optimized for fast analytical queries on large datasets.

**Key Features:**
- Column-oriented storage
- Data compression
- Parallel query execution
- Distributed queries
- Real-time analytics

## Table Design Patterns

### MergeTree Engine (Most Common)

```sql
CREATE TABLE markets_analytics (
    date Date,
    market_id String,
    market_name String,
    volume UInt64,
    trades UInt32,
    unique_traders UInt32,
    avg_trade_size Float64,
    created_at DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, market_id)
SETTINGS index_granularity = 8192;
```

### ReplacingMergeTree (Deduplication)

```sql
-- For data that may have duplicates (e.g., from multiple sources)
CREATE TABLE user_events (
    event_id String,
    user_id String,
    event_type String,
    timestamp DateTime,
    properties String
) ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, event_id, timestamp)
PRIMARY KEY (user_id, event_id);
```

### AggregatingMergeTree (Pre-aggregation)

```sql
-- For maintaining aggregated metrics
CREATE TABLE market_stats_hourly (
    hour DateTime,
    market_id String,
    total_volume AggregateFunction(sum, UInt64),
    total_trades AggregateFunction(count, UInt32),
    unique_users AggregateFunction(uniq, String)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, market_id);

-- Query aggregated data
SELECT
    hour,
    market_id,
    sumMerge(total_volume) AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users) AS users
FROM market_stats_hourly
WHERE hour >= toStartOfHour(now() - INTERVAL 24 HOUR)
GROUP BY hour, market_id
ORDER BY hour DESC;
```

## Query Optimization Patterns

### Efficient Filtering

```sql
-- ✅ GOOD: Use indexed columns first
SELECT *
FROM markets_analytics
WHERE date >= '2025-01-01'
  AND market_id = 'market-123'
  AND volume > 1000
ORDER BY date DESC
LIMIT 100;

-- ❌ BAD: Filter on non-indexed columns first
SELECT *
FROM markets_analytics
WHERE volume > 1000
  AND market_name LIKE '%election%'
  AND date >= '2025-01-01';
```

### Aggregations

```sql
-- ✅ GOOD: Use ClickHouse-specific aggregation functions
SELECT
    toStartOfDay(created_at) AS day,
    market_id,
    sum(volume) AS total_volume,
    count() AS total_trades,
    uniq(trader_id) AS unique_traders,
    avg(trade_size) AS avg_size
FROM trades
WHERE created_at >= today() - INTERVAL 7 DAY
GROUP BY day, market_id
ORDER BY day DESC, total_volume DESC;

-- ✅ Use quantile for percentiles (more efficient than percentile)
SELECT
    quantile(0.50)(trade_size) AS median,
    quantile(0.95)(trade_size) AS p95,
    quantile(0.99)(trade_size) AS p99
FROM trades
WHERE created_at >= now() - INTERVAL 1 HOUR;
```

### Window Functions

```sql
-- Calculate running totals
SELECT
    date,
    market_id,
    volume,
    sum(volume) OVER (
        PARTITION BY market_id
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_volume
FROM markets_analytics
WHERE date >= today() - INTERVAL 30 DAY
ORDER BY market_id, date;
```

## Data Insertion Patterns

### Bulk Insert (Recommended)

```python
from clickhouse_connect import get_client
from typing import List
from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class Trade:
    id: str
    market_id: str
    user_id: str
    amount: float
    timestamp: datetime

clickhouse = get_client(
    host=os.getenv('CLICKHOUSE_URL'),
    port=8123,
    username=os.getenv('CLICKHOUSE_USER'),
    password=os.getenv('CLICKHOUSE_PASSWORD')
)

# ✅ Batch insert (efficient)
async def bulk_insert_trades(trades: List[Trade]) -> None:
    data = [
        {
            'id': trade.id,
            'market_id': trade.market_id,
            'user_id': trade.user_id,
            'amount': trade.amount,
            'timestamp': trade.timestamp
        }
        for trade in trades
    ]

    clickhouse.insert('trades', data)

# ❌ Individual inserts (slow)
async def insert_trade(trade: Trade) -> None:
    # Don't do this in a loop!
    clickhouse.insert('trades', [{
        'id': trade.id,
        'market_id': trade.market_id,
        'user_id': trade.user_id,
        'amount': trade.amount,
        'timestamp': trade.timestamp
    }])
```

### Streaming Insert

```python
# For continuous data ingestion
from typing import AsyncIterator

async def stream_inserts(data_source: AsyncIterator[List[dict]]) -> None:
    batch = []
    batch_size = 1000

    async for items in data_source:
        batch.extend(items)

        if len(batch) >= batch_size:
            clickhouse.insert('trades', batch)
            batch = []

    if batch:
        clickhouse.insert('trades', batch)
```

## Materialized Views

### Real-time Aggregations

```sql
-- Create materialized view for hourly stats
CREATE MATERIALIZED VIEW market_stats_hourly_mv
TO market_stats_hourly
AS SELECT
    toStartOfHour(timestamp) AS hour,
    market_id,
    sumState(amount) AS total_volume,
    countState() AS total_trades,
    uniqState(user_id) AS unique_users
FROM trades
GROUP BY hour, market_id;

-- Query the materialized view
SELECT
    hour,
    market_id,
    sumMerge(total_volume) AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users) AS users
FROM market_stats_hourly
WHERE hour >= now() - INTERVAL 24 HOUR
GROUP BY hour, market_id;
```

## Performance Monitoring

### Query Performance

```sql
-- Check slow queries
SELECT
    query_id,
    user,
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND query_duration_ms > 1000
  AND event_time >= now() - INTERVAL 1 HOUR
ORDER BY query_duration_ms DESC
LIMIT 10;
```

### Table Statistics

```sql
-- Check table sizes
SELECT
    database,
    table,
    formatReadableSize(sum(bytes)) AS size,
    sum(rows) AS rows,
    max(modification_time) AS latest_modification
FROM system.parts
WHERE active
GROUP BY database, table
ORDER BY sum(bytes) DESC;
```

## Common Analytics Queries

### Time Series Analysis

```sql
-- Daily active users
SELECT
    toDate(timestamp) AS date,
    uniq(user_id) AS daily_active_users
FROM events
WHERE timestamp >= today() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date;

-- Retention analysis
SELECT
    signup_date,
    countIf(days_since_signup = 0) AS day_0,
    countIf(days_since_signup = 1) AS day_1,
    countIf(days_since_signup = 7) AS day_7,
    countIf(days_since_signup = 30) AS day_30
FROM (
    SELECT
        user_id,
        min(toDate(timestamp)) AS signup_date,
        toDate(timestamp) AS activity_date,
        dateDiff('day', signup_date, activity_date) AS days_since_signup
    FROM events
    GROUP BY user_id, activity_date
)
GROUP BY signup_date
ORDER BY signup_date DESC;
```

### Funnel Analysis

```sql
-- Conversion funnel
SELECT
    countIf(step = 'viewed_market') AS viewed,
    countIf(step = 'clicked_trade') AS clicked,
    countIf(step = 'completed_trade') AS completed,
    round(clicked / viewed * 100, 2) AS view_to_click_rate,
    round(completed / clicked * 100, 2) AS click_to_completion_rate
FROM (
    SELECT
        user_id,
        session_id,
        event_type AS step
    FROM events
    WHERE event_date = today()
)
GROUP BY session_id;
```

### Cohort Analysis

```sql
-- User cohorts by signup month
SELECT
    toStartOfMonth(signup_date) AS cohort,
    toStartOfMonth(activity_date) AS month,
    dateDiff('month', cohort, month) AS months_since_signup,
    count(DISTINCT user_id) AS active_users
FROM (
    SELECT
        user_id,
        min(toDate(timestamp)) OVER (PARTITION BY user_id) AS signup_date,
        toDate(timestamp) AS activity_date
    FROM events
)
GROUP BY cohort, month, months_since_signup
ORDER BY cohort, months_since_signup;
```

## Data Pipeline Patterns

### ETL Pattern

```python
# Extract, Transform, Load
import asyncio
from datetime import datetime
from typing import List, Dict, Any

async def etl_pipeline() -> None:
    # 1. Extract from source
    raw_data = await extract_from_postgres()

    # 2. Transform
    transformed = [
        {
            'date': datetime.fromisoformat(row['created_at']).date().isoformat(),
            'market_id': row['market_slug'],
            'volume': float(row['total_volume']),
            'trades': int(row['trade_count'])
        }
        for row in raw_data
    ]

    # 3. Load to ClickHouse
    await bulk_insert_to_clickhouse(transformed)

# Run periodically
async def run_etl_scheduler():
    while True:
        await etl_pipeline()
        await asyncio.sleep(3600)  # Every hour

# Start scheduler
# asyncio.create_task(run_etl_scheduler())
```

### Change Data Capture (CDC)

```python
# Listen to PostgreSQL changes and sync to ClickHouse
import psycopg2
import psycopg2.extensions
import json
from datetime import datetime

pg_client = psycopg2.connect(os.getenv('DATABASE_URL'))
pg_client.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor = pg_client.cursor()
cursor.execute('LISTEN market_updates')

def handle_notification(notify):
    update = json.loads(notify.payload)

    clickhouse.insert('market_updates', [{
        'market_id': update['id'],
        'event_type': update['operation'],  # INSERT, UPDATE, DELETE
        'timestamp': datetime.now(),
        'data': json.dumps(update['new_data'])
    }])

# Set up notification handler
psycopg2.extensions.set_wait_callback(psycopg2.extensions.make_async_callback())
pg_client.add_notify_handler(handle_notification)

# Poll for notifications
while True:
    pg_client.poll()
    if pg_client.notifies:
        notify = pg_client.notifies.pop(0)
        handle_notification(notify)
```

## Best Practices

### 1. Partitioning Strategy
- Partition by time (usually month or day)
- Avoid too many partitions (performance impact)
- Use DATE type for partition key

### 2. Ordering Key
- Put most frequently filtered columns first
- Consider cardinality (high cardinality first)
- Order impacts compression

### 3. Data Types
- Use smallest appropriate type (UInt32 vs UInt64)
- Use LowCardinality for repeated strings
- Use Enum for categorical data

### 4. Avoid
- SELECT * (specify columns)
- FINAL (merge data before query instead)
- Too many JOINs (denormalize for analytics)
- Small frequent inserts (batch instead)

### 5. Monitoring
- Track query performance
- Monitor disk usage
- Check merge operations
- Review slow query log

**Remember**: ClickHouse excels at analytical workloads. Design tables for your query patterns, batch inserts, and leverage materialized views for real-time aggregations.
