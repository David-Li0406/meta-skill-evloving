---
name: data-fetcher-integration
description: Guidelines for integrating new data series (FRED, CoinGecko) into background workers. Use this when expanding the dashboard's data coverage with new economic or crypto indicators.
---

# Data Fetcher Integration

## Overview
This skill provides step-by-step guidance for adding new data indicators to the Cycle Navigator's background worker system. It ensures that new data integrations respect rate limits, caching logic, database constraints, and Celery task patterns.

## When to Use This Skill
- Adding a new FRED (Federal Reserve Economic Data) series to macro indicators
- Integrating a new CoinGecko cryptocurrency metric
- Expanding data coverage without breaking existing rate limit budgets
- Ensuring two-tier data architecture (PostgreSQL + Redis cache) consistency

## Instructions

### Setup

#### 1. Verify Rate Limit Budget
Before adding a new data source, check your current usage:

**FRED Rate Limits:**
- Safe threshold: 800 requests/day
- Check existing tasks in `backend/tasks/fred_tasks.py` to estimate cumulative daily calls
- Calculate: (number_of_series × calls_per_series × 365 days) ÷ 800

**CoinGecko Rate Limits:**
- Demo tier: 30 calls/minute (soft limit)
- Production tier: 50 calls/minute
- Check `backend/tasks/crypto_tasks.py` for existing tasks

#### 2. Understand the Data Flow Architecture
New data must follow this two-tier pattern:
```
External API (FRED/CoinGecko)
    ↓
PostgreSQL (source of truth)
    ↓
Redis Cache (24-hour TTL)
    ↓
API Response to Frontend
```

### Implementation

#### Step 1: Create the Celery Task

Add your task to the appropriate file:
- **FRED data**: `backend/tasks/fred_tasks.py`
- **Crypto data**: `backend/tasks/crypto_tasks.py`

**Example FRED Task:**
```python
from celery import shared_task
from backend.services.macro import fetch_and_store_fred_series
from backend.utils import get_redis_client
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def fetch_unemployment_rate(self):
    """Fetch monthly unemployment rate from FRED."""
    series_id = "UNRATE"
    redis_client = get_redis_client()
    lock_key = f"fred:fetch:{series_id}"
    
    try:
        # Acquire distributed lock to prevent concurrent API calls
        lock_acquired = redis_client.set(
            lock_key, 
            "locked", 
            nx=True, 
            ex=300  # 5-minute lock timeout
        )
        
        if not lock_acquired:
            logger.info(f"Lock held for {series_id}, skipping this run")
            return
        
        # Fetch from FRED API and store in PostgreSQL
        data = fetch_and_store_fred_series(series_id)
        
        # Update Redis cache (24-hour TTL)
        cache_key = f"macro:fred:{series_id}"
        redis_client.setex(cache_key, 86400, json.dumps(data))
        
        logger.info(f"Successfully updated {series_id}")
        
    except Exception as exc:
        # Exponential backoff: 2s, 4s, 8s, 16s, 32s
        retry_delay = 2 ** self.request.retries
        self.retry(exc=exc, countdown=retry_delay)
    finally:
        # Always release the lock
        redis_client.delete(lock_key)
```

**Example Crypto Task:**
```python
@shared_task(bind=True, max_retries=3)
def fetch_bitcoin_market_cap(self):
    """Fetch Bitcoin market cap from CoinGecko."""
    crypto_id = "bitcoin"
    redis_client = get_redis_client()
    lock_key = f"crypto:fetch:{crypto_id}"
    
    try:
        lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=60)
        
        if not lock_acquired:
            logger.info(f"Lock held for {crypto_id}, skipping")
            return
        
        # Fetch from CoinGecko
        data = fetch_and_store_crypto_series(crypto_id)
        
        # Cache with 24-hour TTL
        cache_key = f"crypto:coingecko:{crypto_id}"
        redis_client.setex(cache_key, 86400, json.dumps(data))
        
        logger.info(f"Updated {crypto_id}")
        
    except Exception as exc:
        retry_delay = 2 ** self.request.retries
        self.retry(exc=exc, countdown=retry_delay)
    finally:
        redis_client.delete(lock_key)
```

#### Step 2: Register the Task in Celery Beat
Edit `backend/celery_app.py` to schedule the new task:

```python
from celery.schedules import crontab

# In app.conf.beat_schedule dictionary:
beat_schedule = {
    # ... existing tasks ...
    'fetch-unemployment-rate': {
        'task': 'backend.tasks.fred_tasks.fetch_unemployment_rate',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight UTC
    },
    'fetch-bitcoin-market-cap': {
        'task': 'backend.tasks.crypto_tasks.fetch_bitcoin_market_cap',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}
```

#### Step 3: Update Database Schema (if needed)
If adding a new metric requires a new PostgreSQL table or column:

1. Check `backend/models.py` for existing schemas
2. Add the new model if it doesn't exist
3. Create a migration: `python scripts/run_timescale_migrations.py`
4. ⚠️ **WARNING**: TimescaleDB hypertables are **irreversible** — test migrations in development first

#### Step 4: Update the Service Layer
Add a function to `backend/services/macro.py` or `backend/services/crypto.py`:

```python
def fetch_and_store_fred_series(series_id: str) -> dict:
    """
    Fetch from FRED API and store in PostgreSQL.
    Returns: dict with latest data point
    """
    # Call FRED API
    fred = fredapi.FRED(api_key=settings.FRED_API_KEY)
    data = fred.get(series_id)
    
    # Store in PostgreSQL
    # (Implementation depends on your ORM)
    store_to_db(series_id, data)
    
    return {
        "series_id": series_id,
        "latest_value": data.iloc[-1],
        "timestamp": data.index[-1]
    }
```

#### Step 5: Add API Endpoint (if exposing new data)
Add a route to `backend/routers/macro.py` or `backend/routers/crypto.py`:

```python
@router.get("/unemployment-rate")
async def get_unemployment_rate():
    """Fetch cached unemployment rate data."""
    redis_client = get_redis_client()
    cached = redis_client.get("macro:fred:UNRATE")
    
    if cached:
        return json.loads(cached)
    
    # Fallback to database if cache miss
    return db_query_latest("UNRATE")
```

### Verification

#### Test Rate Limits
```bash
# Run a test fetch locally
podman-compose exec backend python -c "
from backend.tasks.fred_tasks import fetch_unemployment_rate
result = fetch_unemployment_rate()
print(result)
"
```

#### Verify PostgreSQL Storage
```bash
# Check data was written to database
podman-compose exec db psql -U postgres -d cycle_navigator -c "
SELECT * FROM macro_indicators WHERE series_id = 'UNRATE' LIMIT 5;
"
```

#### Verify Redis Cache
```bash
# Check cache entry
podman-compose exec redis redis-cli GET "macro:fred:UNRATE"
```

#### Monitor Celery Task Execution
```bash
# Watch Celery worker logs
podman-compose logs -f celery-worker | grep fetch_unemployment_rate
```

## Examples

### Example 1: Adding FRED Employment Level
You want to track monthly employment level (`PAYEMS`):

1. Add task to `backend/tasks/fred_tasks.py`
2. Set schedule in `backend/celery_app.py`: daily at 01:00 UTC (after FRED updates)
3. Verify in PostgreSQL: rate limit budget is 801/day (still safe at 800)
4. Test locally, then deploy with `podman-compose up -d`

### Example 2: Adding CoinGecko Ethereum Metrics
You want to track Ethereum daily volume:

1. Create task in `backend/tasks/crypto_tasks.py`
2. Set schedule: every 4 hours (6 calls/day = safe within 30/min limit)
3. Add to `/crypto/ethereum-volume` endpoint
4. Verify cache hits with `redis-cli MONITOR`

## Safety/Verification

### ⚠️ Critical Warnings

**Database Migrations:**
- TimescaleDB hypertables are **irreversible**
- Always test schema changes in development first
- Run migrations during maintenance windows only
- Backup PostgreSQL before schema modifications

**Rate Limit Overages:**
- Exceeding rate limits will cause API bans (FRED: 24-hour cooldown, CoinGecko: 1-hour)
- Calculate total daily API calls across all tasks before deploying
- Monitor actual usage in production with logs

**Redis Lock Failures:**
- If Redis is down, locks fail silently and multiple workers will call the API
- Ensure Redis is monitored and configured with persistence
- Use `redis:fetch:{series_id}` naming convention consistently

**Concurrent Updates:**
- Without distributed locks, multiple Celery workers cause duplicate API calls
- Always acquire lock before external API call
- Release lock in `finally` block to prevent stuck locks

### Pre-Deployment Checklist

- [ ] Rate limit budget verified (FRED ≤ 800/day, CoinGecko ≤ 30/min)
- [ ] Exponential backoff configured (base 2: 2s, 4s, 8s, 16s, 32s)
- [ ] Redis lock pattern matches existing tasks
- [ ] Two-tier update implemented (DB first, then cache)
- [ ] Task registered in `backend/celery_app.py` beat schedule
- [ ] Tested locally with `podman-compose`
- [ ] PostgreSQL data verified with `psql`
- [ ] Redis cache verified with `redis-cli`
- [ ] Celery logs monitored during first production run
- [ ] API response tested from frontend

## Troubleshooting

### Issue: "Task not found" error
**Cause**: Task not registered in Celery app
**Solution**: Verify task is in `backend/celery_app.py` beat schedule and imported correctly
```bash
podman-compose exec backend celery -A backend.celery_app inspect active
```

### Issue: Rate limit exceeded (429 error)
**Cause**: Total daily API calls exceed service limits
**Solution**: Reduce task frequency or remove lower-priority data
```bash
# Calculate current usage
grep "fetch_" backend/celery_app.py | wc -l
```

### Issue: Redis cache not updating
**Cause**: Lock held for too long or cache key mismatch
**Solution**: Check lock TTL and cache key naming
```bash
redis-cli KEYS "fred:fetch:*"  # Find stuck locks
redis-cli TTL "fred:fetch:UNRATE"  # Check lock timeout
```

### Issue: PostgreSQL constraint violation
**Cause**: Duplicate data insertion or missing foreign keys
**Solution**: Review schema and check for `UNIQUE` or `FOREIGN KEY` constraints
```bash
podman-compose exec db psql -U postgres -d cycle_navigator -c "
SELECT constraint_name FROM information_schema.table_constraints 
WHERE table_name = 'macro_indicators';
"
```

### Issue: Exponential backoff causing late updates
**Cause**: Task failing repeatedly and retrying with long delays
**Solution**: Check API credentials, network connectivity, rate limits
```bash
# Review error logs
podman-compose logs celery-worker | grep "Retry"
```

## Related Skills

- **skill-creator**: For creating new skills following project standards
- **celery-task-builder** (future): Detailed Celery task development patterns
- **postgres-migration-guide** (future): Safe database schema changes

## References

- [TECHNICAL_ARCHITECTURE.md](../../documents/TECHNICAL_ARCHITECTURE.md)
- [DEVELOPER_SETUP.md](../../documents/DEVELOPER_SETUP.md)
- FRED API Documentation: https://fred.stlouisfed.org/docs/api
- CoinGecko API Documentation: https://www.coingecko.com/en/api
