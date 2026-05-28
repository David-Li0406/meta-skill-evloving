---
name: api-endpoint-development
description: Standards for developing FastAPI routers and Pydantic schemas. Use this when creating new API endpoints or modifying response schemas.
---

# API Endpoint Development

## Overview
This skill provides standardized patterns for building FastAPI endpoints in the Cycle Navigator project. It ensures consistency across response schemas, data freshness tracking, caching logic, and type safety between backend and frontend.

## When to Use This Skill
- Creating a new FastAPI endpoint in `backend/routers/`
- Adding a new response schema to `backend/schemas.py`
- Implementing Redis caching for API responses
- Exposing macro, crypto, or risk data from background workers
- Ensuring frontend TypeScript interfaces match backend Pydantic schemas
- Troubleshooting staleness or caching issues

## Instructions

### Setup

#### 1. Understand the Response Architecture
All Cycle Navigator API responses follow this pattern:
```json
{
  "metadata": {
    "last_updated": "2026-01-23T15:30:00Z",
    "is_stale": false
  },
  "data": {
    // Actual endpoint-specific data
  }
}
```

**Why this matters:**
- Frontend displays a warning if data is stale
- Metadata includes ISO 8601 timestamp for cache validation
- Staleness is calculated as: current_time - last_updated > 25 hours

#### 2. Review Existing Patterns
Check existing endpoints for consistency:
- Macro endpoints: `backend/routers/macro.py`
- Crypto endpoints: `backend/routers/crypto.py`
- Risk endpoints: `backend/routers/risk.py`
- Schemas: `backend/schemas.py`

#### 3. Know Your Cache Layer
Response data flows through:
1. Redis cache (fast, 100ms response)
2. PostgreSQL database (source of truth)
3. Frontend TypeScript interfaces (type-safe consumption)

### Implementation

#### Step 1: Create the Pydantic Schema

Add your response schema to `backend/schemas.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class MetadataResponse(BaseModel):
    """Standard metadata included in all API responses."""
    last_updated: datetime = Field(..., description="ISO 8601 timestamp of last data update")
    is_stale: bool = Field(..., description="True if data older than 25 hours")

class MacroDataPoint(BaseModel):
    """Single macro indicator data point."""
    date: datetime
    value: float
    series_id: str

class MacroIndicatorResponse(BaseModel):
    """Response for individual macro indicator endpoint."""
    series_id: str = Field(..., description="FRED series ID (e.g., 'UNRATE')")
    name: str = Field(..., description="Human-readable name (e.g., 'Unemployment Rate')")
    unit: str = Field(..., description="Unit of measurement (e.g., 'Percent')")
    data_points: List[MacroDataPoint] = Field(..., description="Historical data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "series_id": "UNRATE",
                "name": "Unemployment Rate",
                "unit": "Percent",
                "data_points": [
                    {"date": "2026-01-15", "value": 3.7, "series_id": "UNRATE"}
                ]
            }
        }

class MacroIndicatorWithMetadata(BaseModel):
    """Wrapper with metadata for API response."""
    metadata: MetadataResponse
    data: MacroIndicatorResponse
```

**Key conventions:**
- `*Response` suffix for schemas returned by endpoints
- `*WithMetadata` wrapper for full API responses
- `MetadataResponse` always included in every endpoint
- Use `Field()` with descriptions for OpenAPI documentation
- Include `json_schema_extra` examples for clarity

#### Step 2: Implement the Staleness Utility

Create or verify `backend/utils.py` has the `is_data_stale()` function:

```python
from datetime import datetime, timedelta
from typing import Optional

def is_data_stale(last_updated: datetime, stale_threshold_hours: int = 25) -> bool:
    """
    Determine if data is stale based on last update time.
    
    Args:
        last_updated: ISO 8601 datetime when data was last fetched
        stale_threshold_hours: Hours before data is considered stale (default: 25)
    
    Returns:
        True if (now - last_updated) > threshold, else False
    
    Example:
        >>> last_updated = datetime.utcnow() - timedelta(hours=26)
        >>> is_data_stale(last_updated)
        True
    """
    if last_updated is None:
        return True
    
    time_elapsed = datetime.utcnow() - last_updated
    stale_threshold = timedelta(hours=stale_threshold_hours)
    
    return time_elapsed > stale_threshold
```

#### Step 3: Create the FastAPI Router

Create a new router file (e.g., `backend/routers/new_indicator.py`):

```python
from fastapi import APIRouter, HTTPException, Query
from backend.schemas import MacroIndicatorWithMetadata, MetadataResponse, MacroIndicatorResponse
from backend.utils import get_redis_client, is_data_stale
from backend.models import MacroIndicator  # Your SQLAlchemy model
from datetime import datetime
import json
import logging

router = APIRouter(prefix="/new-indicator", tags=["indicators"])
logger = logging.getLogger(__name__)

@router.get("/unemployment-rate", response_model=MacroIndicatorWithMetadata)
async def get_unemployment_rate(
    days: int = Query(365, ge=30, le=1825, description="Days of historical data")
):
    """
    Fetch unemployment rate with metadata.
    
    Returns:
        MacroIndicatorWithMetadata: Response with metadata and unemployment data
    
    Raises:
        HTTPException: 404 if data not found, 503 if cache/DB unavailable
    """
    series_id = "UNRATE"
    redis_client = get_redis_client()
    
    # Step 1: Try Redis cache first (100ms response)
    cache_key = f"macro:fred:{series_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        logger.info(f"Cache hit for {series_id}")
        cached_data = json.loads(cached)
        
        # Parse last_updated from cached data
        last_updated = datetime.fromisoformat(cached_data["last_updated"])
        stale = is_data_stale(last_updated)
        
        return MacroIndicatorWithMetadata(
            metadata=MetadataResponse(
                last_updated=last_updated,
                is_stale=stale
            ),
            data=MacroIndicatorResponse(**cached_data["data"])
        )
    
    # Step 2: Cache miss - query PostgreSQL
    try:
        logger.info(f"Cache miss for {series_id}, querying database")
        
        # Query database for latest data points
        db_data = (
            db.query(MacroIndicator)
            .filter(MacroIndicator.series_id == series_id)
            .order_by(MacroIndicator.date.desc())
            .limit(days)
            .all()
        )
        
        if not db_data:
            logger.warning(f"No data found for {series_id}")
            raise HTTPException(status_code=404, detail=f"Data not found for {series_id}")
        
        # Build response
        last_updated = db_data[0].date
        data_points = [
            {"date": record.date, "value": record.value, "series_id": series_id}
            for record in reversed(db_data)
        ]
        
        response_data = MacroIndicatorResponse(
            series_id=series_id,
            name="Unemployment Rate",
            unit="Percent",
            data_points=data_points
        )
        
        # Step 3: Update Redis cache (24-hour TTL)
        cache_payload = {
            "last_updated": last_updated.isoformat(),
            "data": response_data.dict()
        }
        redis_client.setex(cache_key, 86400, json.dumps(cache_payload))
        logger.info(f"Updated cache for {series_id}")
        
        return MacroIndicatorWithMetadata(
            metadata=MetadataResponse(
                last_updated=last_updated,
                is_stale=is_data_stale(last_updated)
            ),
            data=response_data
        )
    
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error fetching {series_id}: {exc}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Database or cache service unavailable"
        )
```

#### Step 4: Register the Router

Add the router to `backend/main.py`:

```python
from backend.routers import (
    macro,
    crypto,
    risk,
    new_indicator  # Add this import
)

app = FastAPI(
    title="Cycle Navigator API",
    version="1.0.0"
)

# Register routers
app.include_router(macro.router)
app.include_router(crypto.router)
app.include_router(risk.router)
app.include_router(new_indicator.router)  # Add this line
```

#### Step 5: Generate TypeScript Types

Use Pydantic's JSON schema to generate TypeScript interfaces:

```bash
# Generate OpenAPI schema
podman-compose exec backend python -c "
from backend.main import app
import json
schema = app.openapi()
with open('openapi.json', 'w') as f:
    json.dump(schema, f, indent=2)
"

# Use a tool like openapi-typescript to convert:
# npx openapi-typescript openapi.json -o web/src/types/api.ts
```

Or manually create `web/src/types/api.ts`:

```typescript
export interface MetadataResponse {
  last_updated: string;  // ISO 8601 timestamp
  is_stale: boolean;
}

export interface MacroDataPoint {
  date: string;
  value: number;
  series_id: string;
}

export interface MacroIndicatorResponse {
  series_id: string;
  name: string;
  unit: string;
  data_points: MacroDataPoint[];
}

export interface MacroIndicatorWithMetadata {
  metadata: MetadataResponse;
  data: MacroIndicatorResponse;
}
```

### Verification

#### Test Schema Validation
```bash
# Verify Pydantic schema compiles
podman-compose exec backend python -c "
from backend.schemas import MacroIndicatorWithMetadata
print(MacroIndicatorWithMetadata.model_json_schema())
"
```

#### Test Endpoint with cURL
```bash
# Test endpoint locally
curl http://localhost:8000/new-indicator/unemployment-rate?days=90

# Check response includes metadata
curl http://localhost:8000/new-indicator/unemployment-rate | jq '.metadata'
```

#### Test Cache Behavior
```bash
# First call (cache miss - slower)
time curl http://localhost:8000/new-indicator/unemployment-rate

# Second call (cache hit - faster)
time curl http://localhost:8000/new-indicator/unemployment-rate

# Verify cache entry
podman-compose exec redis redis-cli GET "macro:fred:UNRATE"
```

#### Test Staleness Logic
```bash
# Insert old data into database (26 hours old)
podman-compose exec db psql -U postgres -d cycle_navigator -c "
INSERT INTO macro_indicators (series_id, date, value)
VALUES ('UNRATE', NOW() - INTERVAL '26 hours', 3.7);
"

# Call endpoint - should return is_stale: true
curl http://localhost:8000/new-indicator/unemployment-rate | jq '.metadata.is_stale'
```

#### Validate TypeScript Compilation
```bash
# In web/ directory
npm run type-check
```

## Examples

### Example 1: Macro Indicator Endpoint (Daily)
Adding a new FRED series endpoint (`/macro/gdp-growth`):

1. Add schema to `backend/schemas.py`: `GDPGrowthResponse`
2. Create endpoint in `backend/routers/macro.py`
3. Cache with 24-hour TTL
4. Schedule Celery task to update daily at 08:00 UTC (after FRED updates)
5. Generate TypeScript type: `GDPGrowthWithMetadata`
6. Test: `curl http://localhost:8000/macro/gdp-growth | jq`

### Example 2: Crypto Endpoint (Real-time)
Adding a new CoinGecko metric (`/crypto/market-dominance`):

1. Add schema: `CryptoDominanceResponse` with market-cap percentages
2. Create endpoint with shorter cache TTL (1 hour instead of 24)
3. Update Celery task to run every 4 hours (respects rate limits)
4. Generate TypeScript type with array of crypto holdings
5. Test: Verify `is_stale` remains false for < 1 hour
6. Frontend displays dominance chart updating every 4 hours

## Safety/Verification

### ⚠️ Critical Warnings

**Type Safety:**
- Pydantic schema in `backend/schemas.py` must match TypeScript interface in `web/src/types/api.ts`
- Mismatches break frontend type checking and cause runtime errors
- Use `npm run type-check` after schema changes

**Staleness Threshold (25 hours):**
- Hardcoded globally for consistency
- If you need different thresholds per endpoint, override in the endpoint, not in `is_data_stale()`
- Frontend assumes 25-hour threshold for warning logic

**Cache Invalidation:**
- Redis cache TTL must align with Celery task frequency
- If task runs every 4 hours, set cache TTL to at least 4 hours (14400s)
- Manual cache invalidation: `redis-cli DEL "macro:fred:*"`

**Error Handling:**
- Return 404 if data not found (not 500)
- Return 503 if cache/database unavailable
- Log all errors with context for debugging
- Never expose raw database errors to frontend

**Response Size:**
- Limit historical data points (e.g., max 1825 days = 5 years)
- Use pagination for large datasets
- Paginated responses need different metadata handling

### Pre-Deployment Checklist

- [ ] Pydantic schema added to `backend/schemas.py`
- [ ] Router created and registered in `backend/main.py`
- [ ] `is_data_stale()` utility imported and used correctly
- [ ] Redis cache key follows pattern: `{category}:{source}:{identifier}`
- [ ] Cache TTL matches Celery task frequency
- [ ] TypeScript interface matches Pydantic schema exactly
- [ ] Endpoint tested locally with cURL
- [ ] Cache behavior verified (hit/miss)
- [ ] Staleness logic tested with old data
- [ ] Error cases tested (404, 503)
- [ ] OpenAPI documentation generated (`/docs`)
- [ ] Frontend type-check passes: `npm run type-check`
- [ ] Endpoint documented with docstring and examples

## Troubleshooting

### Issue: "Validation error" on response
**Cause**: Pydantic schema doesn't match returned data structure
**Solution**: Check data types match schema definition
```bash
# Log actual response before wrapping
import json
logger.debug(f"Response data: {json.dumps(response_data.dict(), default=str)}")
```

### Issue: Frontend type error: "is_stale is not a boolean"
**Cause**: TypeScript interface missing `metadata` object
**Solution**: Ensure TypeScript interface matches Pydantic response wrapper
```typescript
// Wrong - missing metadata
interface Response {
  data: MacroIndicatorResponse;
}

// Correct
interface Response {
  metadata: MetadataResponse;
  data: MacroIndicatorResponse;
}
```

### Issue: Cache always returns stale data
**Cause**: `last_updated` in cache not updating
**Solution**: Verify Celery task writes correct timestamp to Redis
```bash
redis-cli GET "macro:fred:UNRATE" | jq '.last_updated'
```

### Issue: Endpoint returns 503 "service unavailable"
**Cause**: Redis or PostgreSQL connection failed
**Solution**: Check service health
```bash
# Check Redis
podman-compose exec redis redis-cli ping

# Check PostgreSQL
podman-compose exec db psql -U postgres -c "SELECT 1"

# Check logs
podman-compose logs backend | tail -50
```

### Issue: Query slow (database hit takes > 1 second)
**Cause**: Missing database index on series_id or date columns
**Solution**: Verify indexes exist
```bash
podman-compose exec db psql -U postgres -d cycle_navigator -c "
CREATE INDEX idx_macro_series_date ON macro_indicators(series_id, date DESC);
"
```

### Issue: TypeScript compilation fails after schema change
**Cause**: Generated types out of sync with Pydantic schema
**Solution**: Regenerate OpenAPI schema and types
```bash
# Regenerate OpenAPI
podman-compose exec backend python -c "
from backend.main import app
import json
schema = app.openapi()
with open('openapi.json', 'w') as f:
    json.dump(schema, f)
"

# Regenerate TypeScript
npx openapi-typescript openapi.json -o web/src/types/api.ts
```

## Related Skills

- **skill-creator**: For creating new skills following project standards
- **data-fetcher-integration**: For background workers that populate cache and database
- **postgres-migration-guide** (future): For database schema changes
- **redis-caching-patterns** (future): For advanced caching strategies

## References

- [TECHNICAL_ARCHITECTURE.md](../../documents/TECHNICAL_ARCHITECTURE.md)
- [DEVELOPER_SETUP.md](../../documents/DEVELOPER_SETUP.md)
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic Documentation: https://docs.pydantic.dev/
- FastAPI Response Model: https://fastapi.tiangolo.com/tutorial/response-model/
