# Caching Patterns - Validations

## Cache Set Without TTL

### **Id**
cache-no-ttl
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - redis\\.set\\([^)]+\\)(?!.*EX|ex|setex|expire)
  - cache\\.set\\([^)]+\\)(?!.*ttl|expire)
  - \\.set\\(["'][^,]+,\\s*JSON
### **Message**
Cache set without TTL. Data may become stale indefinitely.
### **Fix Action**
Use setex or add EX option: redis.setex(key, ttl, value)
### **Applies To**
  - **/*.ts
  - **/*.js

## Redis KEYS Command Usage

### **Id**
cache-keys-command
### **Severity**
error
### **Type**
regex
### **Pattern**
  - redis\\.keys\\(
  - \.keys\(["'].*\*
  - KEYS \\*
  - KEYS .*\\*
### **Message**
KEYS command blocks Redis. Use SCAN for iteration in production.
### **Fix Action**
Replace with SCAN: redis.scan(cursor, 'MATCH', pattern, 'COUNT', 100)
### **Applies To**
  - **/*.ts
  - **/*.js

## Cache Write Before Database

### **Id**
cache-before-db
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - redis\\.set.*\\n.*db\\.
  - cache\\.set.*\\n.*save
  - setex.*\\n.*create
  - setex.*\\n.*insert
### **Message**
Cache written before database. Data inconsistency if database fails.
### **Fix Action**
Write to database first, then update cache
### **Applies To**
  - **/*.ts
  - **/*.js

## Database Update Without Cache Invalidation

### **Id**
cache-no-invalidation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.update\\([^)]+\\)(?![\\s\\S]*?redis\\.del|cache\\.del|invalidate)
  - \\.delete\\([^)]+\\)(?![\\s\\S]*?redis\\.del|cache\\.del|invalidate)
### **Message**
Database update without cache invalidation. May serve stale data.
### **Fix Action**
Add cache invalidation after database update
### **Applies To**
  - **/*.ts
  - **/*.js

## Caching Error Responses

### **Id**
cache-caching-errors
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch.*setex|catch.*\\.set\\(
  - error.*cache.*set
  - null.*setex|setex.*null
### **Message**
May be caching error/null results. Will serve errors after recovery.
### **Fix Action**
Only cache successful results, use short TTL for negative cache
### **Applies To**
  - **/*.ts
  - **/*.js

## Cache Miss Without Stampede Protection

### **Id**
cache-no-stampede-protection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - if.*cache\\.get.*\\n.*db\\.
  - if.*redis\\.get.*\\n.*db\\.
### **Message**
Cache-aside pattern without stampede protection.
### **Fix Action**
Add lock-based or probabilistic stampede prevention for hot keys
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Cache TTL

### **Id**
cache-hardcoded-ttl
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setex\\([^,]+,\\s*\\d{4,}
  - ttl:\\s*\\d{4,}
  - expire:\\s*\\d{4,}
### **Message**
Hardcoded TTL value. Consider using named constants.
### **Fix Action**
Extract to constant: const USER_CACHE_TTL = 3600
### **Applies To**
  - **/*.ts
  - **/*.js

## Large Object Serialization

### **Id**
cache-json-large-object
### **Severity**
info
### **Type**
regex
### **Pattern**
  - JSON\\.stringify\\(.*\\).*setex
  - setex.*JSON\\.stringify
### **Message**
JSON serialization for cache. Consider compression for large objects.
### **Fix Action**
For large objects, use compression or MessagePack
### **Applies To**
  - **/*.ts
  - **/*.js

## Cache Operation Without Error Handling

### **Id**
cache-missing-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await redis\\.[a-z]+\\([^)]+\\)(?!\\s*\\.catch|try)
### **Message**
Cache operation without error handling. Should handle cache failures gracefully.
### **Fix Action**
Wrap in try-catch, continue without cache on failure
### **Applies To**
  - **/*.ts
  - **/*.js

## Unsanitized User Input in Cache Key

### **Id**
cache-dynamic-key-unsanitized
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - redis\\.[a-z]+\\(`[^`]*\\$\\{.*req\\.
  - redis\\.[a-z]+\\(`[^`]*\\$\\{.*params\\.
  - cache\\..*\\$\\{.*user[Ii]nput
### **Message**
User input in cache key. May cause key injection or excessive key creation.
### **Fix Action**
Sanitize and validate user input before using in cache keys
### **Applies To**
  - **/*.ts
  - **/*.js

## Redis FLUSHALL/FLUSHDB Usage

### **Id**
cache-flushall-usage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - redis\\.flushall
  - redis\\.flushdb
  - FLUSHALL
  - FLUSHDB
### **Message**
FLUSHALL/FLUSHDB clears entire database. Extremely dangerous in production.
### **Fix Action**
Use pattern-based deletion with SCAN instead
### **Applies To**
  - **/*.ts
  - **/*.js

## Redis Client Without Retry

### **Id**
cache-no-connection-retry
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Redis\\([^)]*\\)(?!.*retry)
  - createClient\\((?!.*retry)
### **Message**
Redis client may not have retry logic configured.
### **Fix Action**
Configure retry strategy for connection resilience
### **Applies To**
  - **/*.ts
  - **/*.js

## Synchronous Cache Operations

### **Id**
cache-sync-operations
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.getSync\\(
  - \\.setSync\\(
  - Sync\\(.*cache
### **Message**
Synchronous cache operation may block event loop.
### **Fix Action**
Use async operations: await cache.get()
### **Applies To**
  - **/*.ts
  - **/*.js

## HTTP Cache Without Vary Header

### **Id**
cache-http-no-vary
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Cache-Control.*public(?!.*Vary)
  - max-age.*(?!.*Vary)
### **Message**
Public cache without Vary header. May serve wrong content to users.
### **Fix Action**
Add Vary header for content that differs by request headers
### **Applies To**
  - **/*.ts
  - **/*.js

## Private Data with Public Cache

### **Id**
cache-private-data-public
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - user.*Cache-Control.*public
  - profile.*max-age.*(?!.*private)
  - account.*Cache-Control.*public
### **Message**
User-specific data may be cached publicly. Use private cache.
### **Fix Action**
Use 'Cache-Control: private' for user-specific data
### **Applies To**
  - **/*.ts
  - **/*.js