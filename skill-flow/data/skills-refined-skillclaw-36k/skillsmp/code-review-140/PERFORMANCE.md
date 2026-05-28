# Performance Review Checklist

Performance-focused code review patterns for Lambda and database operations.

**Principle:** Optimize for cold start, minimize external calls, cache aggressively.

---

## Lambda Performance

### 1. Cold Start Optimization

```python
# ❌ REJECT: Heavy imports inside handler
def lambda_handler(event, context):
    import pandas as pd  # 2-3 seconds import time!
    import yfinance as yf

    # Process...

# ✅ APPROVE: Module-level imports
import pandas as pd  # Import once at cold start
import yfinance as yf

def lambda_handler(event, context):
    # Fast execution
    pass
```

**Check:**
- [ ] Heavy imports at module level (not inside handler)
- [ ] Service singletons initialized at module level
- [ ] No initialization inside hot path

### 2. Connection Pooling

```python
# ❌ REJECT: New connection per invocation
def lambda_handler(event, context):
    conn = pymysql.connect(host=AURORA_HOST, ...)  # Slow!
    # Process...
    conn.close()

# ✅ APPROVE: Reuse connection across invocations
# Module level (survives across invocations)
_db_connection = None

def get_db_connection():
    global _db_connection
    if _db_connection is None or not _db_connection.open:
        _db_connection = pymysql.connect(host=AURORA_HOST, ...)
    return _db_connection

def lambda_handler(event, context):
    conn = get_db_connection()  # Reuses existing connection
    # Process...
```

**Check:**
- [ ] Database connections reused (not recreated)
- [ ] HTTP clients reused (requests.Session())
- [ ] Module-level singletons for stateful resources

### 3. Timeout Configuration

```python
# ❌ REJECT: Too short timeout
aws lambda update-function-configuration \
  --function-name worker \
  --timeout 3  # Default 3 seconds - often too short!

# ✅ APPROVE: Realistic timeout
aws lambda update-function-configuration \
  --function-name worker \
  --timeout 60  # 60 seconds for external API calls
```

**Check:**
- [ ] Timeout > average execution time
- [ ] Consider cold start time in timeout
- [ ] External API timeouts < Lambda timeout

---

## Database Performance

### 1. N+1 Query Problem

```python
# ❌ REJECT: N+1 queries
def get_reports_with_users(ticker_list):
    reports = []
    for ticker in ticker_list:  # Loop = N queries
        report = db.execute("SELECT * FROM reports WHERE ticker = %s", (ticker,))
        reports.append(report)
    return reports

# ✅ APPROVE: Single query with IN clause
def get_reports_with_users(ticker_list):
    placeholders = ','.join(['%s'] * len(ticker_list))
    query = f"SELECT * FROM reports WHERE ticker IN ({placeholders})"
    return db.execute(query, ticker_list)
```

**Check:**
- [ ] No loops with database queries inside
- [ ] Batch queries with IN clause
- [ ] JOINs used instead of multiple queries

### 2. Index Usage

```python
# ❌ REJECT: Query on non-indexed column
SELECT * FROM reports WHERE created_at > '2024-01-01'  # Full table scan!

# ✅ APPROVE: Query on indexed column
# Ensure index exists:
CREATE INDEX idx_created_at ON reports(created_at);

SELECT * FROM reports WHERE created_at > '2024-01-01'  # Uses index
```

**Check:**
- [ ] WHERE clauses use indexed columns
- [ ] Primary key used for lookups
- [ ] Composite indexes for multi-column queries

### 3. SELECT * Avoidance

```python
# ❌ REJECT: Fetches unnecessary data
SELECT * FROM reports  # Returns all columns (including large JSON)

# ✅ APPROVE: Fetch only needed columns
SELECT ticker, summary FROM reports  # Only what's needed
```

**Check:**
- [ ] SELECT lists specific columns (not *)
- [ ] Large BLOBs/TEXT fetched only when needed
- [ ] Pagination for large result sets

---

## Caching

### 1. Appropriate Caching

```python
# ❌ REJECT: No caching for expensive operation
def get_market_data(ticker):
    # Calls external API every time (slow + expensive)
    return yfinance.download(ticker, period='1y')

# ✅ APPROVE: Cache with TTL
import functools
import time

@functools.lru_cache(maxsize=128)
def _cached_market_data(ticker, cache_key):
    return yfinance.download(ticker, period='1y')

def get_market_data(ticker):
    # Cache key includes timestamp (5 minute TTL)
    cache_key = int(time.time() / 300)
    return _cached_market_data(ticker, cache_key)
```

**Check:**
- [ ] Expensive operations cached
- [ ] Cache TTL appropriate
- [ ] Cache invalidation strategy exists

### 2. DynamoDB for Caching

```python
# ✅ APPROVE: DynamoDB as cache layer
def get_cached_report(ticker: str) -> dict:
    """Check DynamoDB cache before generating"""

    # Try cache first
    response = dynamodb_table.get_item(Key={'ticker': ticker})

    if 'Item' in response:
        # Check if still fresh (< 1 day old)
        created = datetime.fromtimestamp(response['Item']['created_at'])
        if datetime.now() - created < timedelta(days=1):
            return response['Item']['report_json']

    # Cache miss or stale - generate fresh report
    report = generate_report(ticker)

    # Store in cache
    dynamodb_table.put_item(Item={
        'ticker': ticker,
        'report_json': report,
        'created_at': int(datetime.now().timestamp())
    })

    return report
```

**Check:**
- [ ] DynamoDB used for frequently accessed data
- [ ] TTL configured on DynamoDB table
- [ ] Cache hit/miss logged for monitoring

---

## External API Optimization

### 1. Parallel API Calls

```python
# ❌ REJECT: Sequential API calls
def fetch_all_data(tickers):
    results = []
    for ticker in tickers:  # Serial = slow!
        data = yfinance.download(ticker)
        results.append(data)
    return results

# ✅ APPROVE: Parallel API calls
import concurrent.futures

def fetch_all_data(tickers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(yfinance.download, ticker) for ticker in tickers]
        results = [future.result() for future in futures]
    return results
```

**Check:**
- [ ] Independent API calls made in parallel
- [ ] Thread pool or async for I/O-bound operations
- [ ] Max workers limited (avoid overwhelming API)

### 2. Request Batching

```python
# ❌ REJECT: One API call per item
for ticker in tickers:
    api.get_price(ticker)  # 46 API calls!

# ✅ APPROVE: Batch API call
api.get_prices_batch(tickers)  # 1 API call for all tickers
```

**Check:**
- [ ] Batch APIs used when available
- [ ] Fallback to individual calls if batch fails

---

## Quick Reference

| Pattern | Bad | Good | Speedup |
|---------|-----|------|---------|
| **Cold Start** | Imports in handler | Module-level imports | 2-3 seconds |
| **DB Connection** | New each invocation | Connection pooling | 100-200ms |
| **N+1 Queries** | Loop with queries | IN clause | 10-100x |
| **SELECT*** | Fetch all columns | Specific columns | 2-5x |
| **No Cache** | API every time | Cache layer | 10-100x |
| **Sequential API** | Loop calls | Parallel calls | Nx speedup |

---

## References

- [AWS Lambda Performance Optimization](https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/)
- [Database Query Optimization](https://use-the-index-luke.com/)
