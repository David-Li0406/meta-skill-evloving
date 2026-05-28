# Performance Hunter - Validations

## Synchronous I/O in Async Function

### **Id**
sync-in-async
### **Severity**
error
### **Type**
regex
### **Pattern**
  - async def.*:.*requests\\.get
  - async def.*:.*open\\(.*\\)\\.read
  - async def.*:.*time\\.sleep
  - async def[^:]+:[^$]*(?<!await )psycopg2\\.
### **Message**
Synchronous I/O in async function. Blocks event loop.
### **Fix Action**
Use async version: aiohttp, aiofiles, asyncio.sleep
### **Applies To**
  - **/*.py

## Database Query in Loop

### **Id**
n-plus-one-loop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - for.*in.*:.*await.*db\\.
  - for.*in.*:.*await.*fetch
  - for.*in.*:.*await.*execute
  - \\[await.*db.*for.*in
### **Message**
Database query inside loop. Likely N+1 pattern.
### **Fix Action**
Batch queries with WHERE IN or use DataLoader pattern
### **Applies To**
  - **/*.py

## Creating Connections Without Pool

### **Id**
no-connection-pool
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - asyncpg\\.connect\\(
  - psycopg2\\.connect\\(
  - redis\\.Redis\\((?!.*connection_pool)
### **Message**
Creating individual connections instead of using pool.
### **Fix Action**
Use connection pool: asyncpg.create_pool(), ConnectionPool
### **Applies To**
  - **/*.py

## Cache Without TTL

### **Id**
cache-no-ttl
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cache\\.set\\([^)]*\\)(?!.*ttl|.*ex=|.*expire)
  - redis\\.set\\([^)]*\\)(?!.*ex=|.*px=)
### **Message**
Cache set without TTL. Data may become stale indefinitely.
### **Fix Action**
Add TTL: cache.set(key, value, ttl=3600)
### **Applies To**
  - **/*.py

## External Call Without Timeout

### **Id**
no-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - aiohttp.*get\\([^)]*\\)(?!.*timeout)
  - httpx.*get\\([^)]*\\)(?!.*timeout)
  - requests\\.get\\([^)]*\\)(?!.*timeout)
### **Message**
External HTTP call without timeout. May hang indefinitely.
### **Fix Action**
Add timeout: session.get(url, timeout=30)
### **Applies To**
  - **/*.py

## Unbounded Collection Growth

### **Id**
unbounded-memory
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - results\\.append.*while True
  - cache\\[.*\\].*=(?!.*if len)
  - list\\.append.*for.*in.*yield
### **Message**
Collection may grow unbounded. Potential memory leak.
### **Fix Action**
Add size limits or use generators for large data
### **Applies To**
  - **/*.py

## Embedding Without Caching

### **Id**
embed-no-cache
### **Severity**
info
### **Type**
regex
### **Pattern**
  - embed\\(.*\\)(?!.*cache)
  - embedder\\.embed(?!.*cached)
### **Message**
Embedding without cache check. Same content re-embedded.
### **Fix Action**
Cache embeddings by content hash
### **Applies To**
  - **/embedding/**/*.py
  - **/retrieval/**/*.py

## Sequential Processing Without Batching

### **Id**
no-batch-processing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*in.*:.*await.*embed
  - for.*in.*:.*await.*llm
  - for.*in.*:.*await.*api
### **Message**
Sequential API calls. Consider batching for efficiency.
### **Fix Action**
Use asyncio.gather() or batch APIs
### **Applies To**
  - **/*.py

## Database Query Without LIMIT

### **Id**
query-no-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - SELECT.*FROM(?!.*LIMIT|.*TOP|.*FETCH)
  - fetch\\([^)]*\\)(?!.*limit)
### **Message**
Query without LIMIT. May return unbounded results.
### **Fix Action**
Add LIMIT or implement pagination
### **Applies To**
  - **/*.py

## Expensive Logging in Hot Path

### **Id**
log-in-hot-path
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*:.*logger\\.debug
  - while.*:.*logger\\.info
  - logger.*json\\.dumps
### **Message**
Logging in tight loop. String formatting adds overhead.
### **Fix Action**
Use lazy logging: logger.debug('%s', value)
### **Applies To**
  - **/*.py

## Query On Unindexed Column

### **Id**
no-index-hint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - WHERE.*content.*=
  - WHERE.*description.*LIKE
### **Message**
Query on potentially unindexed text column. May be slow.
### **Fix Action**
Verify index exists or use full-text search
### **Applies To**
  - **/*.py

## JSON Serialization in Loop

### **Id**
json-in-loop
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*:.*json\\.dumps
  - for.*:.*json\\.loads
### **Message**
JSON serialization in loop. Consider batch processing.
### **Fix Action**
Serialize outside loop or use streaming JSON parser
### **Applies To**
  - **/*.py