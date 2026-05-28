# Performance Optimization for Remote Parquet Queries

Best practices for minimizing bandwidth and latency when querying remote Parquet files via DuckDB httpfs.

## Core Principles

**Remote queries are efficient when**:
1. **Column pruning** - Only SELECT columns you need
2. **Row filtering** - Use WHERE clauses (predicate pushdown)
3. **Parquet structure** - Columnar storage enables partial reads
4. **HTTP range requests** - DuckDB reads only required row groups/column chunks

**Avoid**:
- `SELECT *` (downloads all columns)
- Full table scans without filters
- Repeated identical queries (cache locally instead)
- Very large result sets over HTTP (export filtered subset first)

## Optimization Patterns

### Pattern 1: Column Pruning

**Bad** (downloads all columns):
```sql
SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE symbol = 'BTCUSDT'
```

**Good** (downloads only 3 columns):
```sql
SELECT date, symbol, close_price
FROM read_parquet('https://example.com/data.parquet')
WHERE symbol = 'BTCUSDT'
```

**Impact**: 80-95% bandwidth reduction for wide tables (20+ columns)

### Pattern 2: Predicate Pushdown (WHERE Filtering)

DuckDB pushes filters to Parquet reader, skipping irrelevant row groups.

**Example**:
```sql
-- Only reads row groups containing dates >= 2024-01-01
SELECT date, symbol, volume
FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01'
  AND symbol IN ('BTCUSDT', 'ETHUSDT')
```

**Best Filters** (high selectivity):
- Date ranges (if Parquet sorted/partitioned by date)
- Equality filters (symbol = 'BTCUSDT')
- IN clauses with few values

**Worst Filters** (low selectivity):
- `WHERE volume > 0` (matches most rows)
- Complex string operations (no pushdown)

### Pattern 3: Aggregation Before Export

**Bad** (downloads 1M rows):
```sql
SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01'
-- Then aggregate locally
```

**Good** (downloads 365 rows):
```sql
SELECT date, AVG(close_price) as avg_price, SUM(volume) as total_volume
FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01'
GROUP BY date
```

**Impact**: Remote aggregation reduces network transfer by 100-1000x

### Pattern 4: Local Caching for Repeated Queries

**Bad** (hits network every time):
```sql
-- Query 1
SELECT COUNT(*) FROM read_parquet('https://example.com/data.parquet')

-- Query 2 (re-downloads same data)
SELECT MAX(date) FROM read_parquet('https://example.com/data.parquet')
```

**Good** (download once, query locally):
```sql
-- Download filtered subset once
CREATE TABLE local_cache AS
SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01';

-- Run multiple queries on local table
SELECT COUNT(*) FROM local_cache;
SELECT MAX(date) FROM local_cache;
SELECT symbol, AVG(volume) FROM local_cache GROUP BY symbol;
```

**Impact**: 10-100x faster for repeated queries

### Pattern 5: Schema Inspection Before Queries

Check available columns/types without reading data:

```sql
DESCRIBE SELECT * FROM read_parquet('https://example.com/data.parquet');
```

**Benefit**: Avoid trial-and-error queries, plan optimal SELECT statement

### Pattern 6: LIMIT with ORDER BY (Dangerous)

**Warning**: `LIMIT` does NOT reduce remote reads if combined with ORDER BY:

```sql
-- BAD: Downloads entire file to sort, then returns 10 rows
SELECT * FROM read_parquet('https://example.com/data.parquet')
ORDER BY date DESC
LIMIT 10;
```

**Better**: Filter first, then sort:
```sql
SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-11-01'  -- Reduces scan to ~17 days
ORDER BY date DESC
LIMIT 10;
```

**Best**: If data is pre-sorted, use WHERE with known range instead of ORDER BY.

## Performance Benchmarks

**Typical performance** (20 MB Parquet file, 327 symbols, 2019-2025 history):

| Query Type | Network Transfer | Time | Speedup |
|------------|------------------|------|---------|
| Full scan (`SELECT *`) | ~20 MB | 3.0s | 1x |
| Column pruning (3 of 20 columns) | ~3 MB | 1.2s | 2.5x |
| Filtered query (WHERE symbol = 'BTCUSDT') | ~60 KB | 0.3s | 10x |
| Aggregation (daily counts) | ~10 KB | 0.2s | 15x |

**Variables affecting performance**:
- **Network speed**: 10 Mbps → 3s, 100 Mbps → 0.5s for 20 MB file
- **Parquet row group size**: Smaller row groups enable better filtering (default: 122,880 rows)
- **CDN caching**: First query cold (3s), subsequent queries warm (0.5s) if CDN caches ranges
- **Filter selectivity**: `WHERE symbol = 'X'` (1 of 327) → 99.7% rows skipped

## Troubleshooting Slow Queries

### Issue: Query takes 10+ seconds

**Diagnose**:
1. Check if using `SELECT *` → Add explicit column list
2. Check if using `ORDER BY` without `WHERE` → Add date range filter
3. Check network speed → Test with `curl -w "@curl-format.txt" URL`

### Issue: High bandwidth usage

**Diagnose**:
```sql
-- Add EXPLAIN to see query plan
EXPLAIN SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01';
```

Look for:
- **Projection pushdown**: Only listed columns read
- **Filter pushdown**: WHERE clause pushed to Parquet reader

### Issue: DuckDB doesn't use range requests

**Symptoms**: Downloads full file even with filters

**Causes**:
1. **Server doesn't support range requests**: Check HTTP headers with `curl -I URL`
   - Needs: `Accept-Ranges: bytes`
2. **Using HTTP instead of HTTPS**: Some CDNs require HTTPS for range support
3. **Parquet file not properly structured**: Check with `parquet-tools meta file.parquet`

**Solutions**:
- Use CDN proxy (jsDelivr, Cloudflare) if server doesn't support ranges
- Switch to HTTPS URL
- Re-export Parquet with smaller row groups

## CDN Proxy for Range Request Support

**Problem**: GitHub Releases doesn't support HTTP range requests directly.

**Solution**: Use jsDelivr CDN proxy:

```python
# Original URL (no range requests)
github_url = "https://github.com/org/repo/releases/download/v1.0.0/data.parquet"

# jsDelivr proxy URL (supports range requests)
jsdelivr_url = "https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet"
```

**Benefits**:
- Automatic HTTP range request support
- Global CDN caching (faster subsequent queries)
- 95% reliability (backed by Cloudflare)

**Limitations**:
- Files must be in GitHub public repository
- Max file size: 50 MB (jsDelivr limit)
- 24-hour cache delay for new releases

## Configuration Tuning

### HTTP Timeout and Retries

```sql
-- Increase timeout for slow networks
SET http_timeout = 60000;  -- 60 seconds (default: 30s)

-- Enable retries for transient failures
SET http_retries = 5;  -- Retry up to 5 times (default: 3)
```

### Memory Settings

```sql
-- Limit memory usage for large remote queries
SET memory_limit = '2GB';

-- Adjust threads (default: # CPU cores)
SET threads = 4;
```

### Connection Pooling

```python
# Reuse connection for multiple queries (avoids httpfs reload)
import duckdb

conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs")
conn.execute("LOAD httpfs")

# Run many queries on same connection
for symbol in symbols:
    result = conn.execute(f"SELECT ... WHERE symbol = '{symbol}'").fetchall()
```

## Example: Optimized Workflow

**Scenario**: Analyze availability trends for 10 specific symbols from 20 MB database.

```python
import duckdb

# 1. Setup (once)
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

url = "https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/availability.parquet"

# 2. Cache filtered subset locally (run once)
conn.execute(f"""
CREATE TABLE local_cache AS
SELECT date, symbol, is_available, volume
FROM read_parquet('{url}')
WHERE symbol IN ('BTCUSDT', 'ETHUSDT', ...)
  AND date >= '2024-01-01'
""")
# Network transfer: ~200 KB (vs 20 MB full file)

# 3. Run multiple local queries (fast, no network)
trends = conn.execute("""
SELECT symbol, AVG(CASE WHEN is_available THEN 1.0 ELSE 0.0 END) as uptime
FROM local_cache
GROUP BY symbol
ORDER BY uptime DESC
""").fetchall()

# 4. Export results
conn.execute("COPY trends TO '/tmp/availability_trends.csv' (HEADER, DELIMITER ',')")
```

**Performance**:
- Initial cache load: 1.5 seconds
- Subsequent queries: <50 ms each
- Total time: <2 seconds (vs 30+ seconds with naive approach)
