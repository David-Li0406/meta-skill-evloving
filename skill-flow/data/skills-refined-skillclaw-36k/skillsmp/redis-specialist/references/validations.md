# Redis Specialist - Validations

## Redis SET Without TTL

### **Id**
missing-ttl
### **Severity**
error
### **Type**
regex
### **Pattern**
  - redis\.set\([^)]+\)(?!.*[Ee][Xx]|setex)
  - \.set\(['"][^'"]+['"],\s*[^,]+\)(?!.*[Ee][Xx])
### **Message**
Redis SET without TTL. Keys without expiration fill memory until eviction or OOM.
### **Fix Action**
Use setex() or set() with EX option to ensure keys expire
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## KEYS Command in Production Code

### **Id**
keys-command
### **Severity**
error
### **Type**
regex
### **Pattern**
  - redis\.keys\(
  - \.keys\(['"]\*
  - KEYS ['"]\*
### **Message**
KEYS command blocks Redis during scan. O(n) on entire keyspace.
### **Fix Action**
Use SCAN with cursor for non-blocking iteration
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Pub/Sub for Critical Messages

### **Id**
pubsub-for-critical-data
### **Severity**
error
### **Type**
regex
### **Pattern**
  - publish.*order|payment|transaction
  - subscribe.*order|payment|transaction
### **Message**
Using pub/sub for critical data. Messages lost if subscriber disconnects.
### **Fix Action**
Use Redis Streams with consumer groups for reliable messaging
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Cache Write Without Invalidation Plan

### **Id**
no-cache-invalidation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setex.*user|profile|settings(?!.*del|invalidate)
  - cache.*set(?!.*on.*update|invalidat)
### **Message**
Caching data without clear invalidation strategy leads to stale data.
### **Fix Action**
Implement explicit cache invalidation on data updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Distributed Lock Without Finally Block

### **Id**
lock-without-finally
### **Severity**
error
### **Type**
regex
### **Pattern**
  - acquire.*lock(?!.*finally.*release)
  - setnx.*lock(?!.*finally.*del)
  - redlock\.acquire(?!.*finally)
### **Message**
Lock acquired without guaranteed release in finally block.
### **Fix Action**
Always release locks in finally block to prevent deadlocks
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Large Object Serialization

### **Id**
large-json-stringify
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - JSON\.stringify.*\[.*\.map|filter|reduce
  - setex.*JSON\.stringify.*array|list|history
### **Message**
Storing large serialized arrays. Consider splitting or using Redis lists.
### **Fix Action**
Use Redis native data structures (LPUSH, ZADD) or split large objects
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## New Redis Connection Per Request

### **Id**
connection-per-request
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Redis\(.*\)(?=.*req|request|handler)
  - createClient\(\)(?=.*async.*req)
### **Message**
Creating new Redis connection per request. Use connection pool.
### **Fix Action**
Create single Redis client at module level and reuse
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## MULTI Without EXEC

### **Id**
multi-without-exec
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.multi\(\)(?!.*\.exec\()
### **Message**
MULTI transaction started but EXEC not called. Commands never execute.
### **Fix Action**
Always call exec() to execute transaction
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Naive Rate Limiting Implementation

### **Id**
rate-limit-naive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - incr.*expire(?!.*multi|pipeline)
  - incr.*ttl(?!.*multi|atomic)
### **Message**
Non-atomic rate limiting. INCR and EXPIRE should be in transaction.
### **Fix Action**
Use MULTI/EXEC or Lua script for atomic rate limiting
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## HGETALL on Potentially Large Hash

### **Id**
hgetall-large-hash
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - hgetall.*user|session|product|order
  - HGETALL ['"][^'"]+['"]
### **Message**
HGETALL returns entire hash. For large hashes, use HSCAN or HMGET.
### **Fix Action**
Use HMGET for specific fields or HSCAN for iteration
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## SMEMBERS on Potentially Large Set

### **Id**
smembers-large-set
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - smembers.*all|users|members|followers
  - SMEMBERS ['"][^'"]+['"]
### **Message**
SMEMBERS returns entire set. For large sets, use SSCAN.
### **Fix Action**
Use SSCAN for iteration or SISMEMBER for membership check
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Redis Client Without Error Handler

### **Id**
no-error-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Redis\((?!.*on.*error)
  - createClient\((?!.*on.*error)
### **Message**
Redis client without error handler. Unhandled errors crash Node process.
### **Fix Action**
Add redis.on('error', handler) to prevent process crash
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Blocking Operation Without Timeout

### **Id**
blocking-operation-no-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - blpop|brpop|brpoplpush(?!.*\d{3,})
  - BLPOP|BRPOP(?!.*TIMEOUT)
### **Message**
Blocking operation without timeout can hang indefinitely.
### **Fix Action**
Always specify timeout for blocking operations (0 means forever)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Lua Script Defined Inline

### **Id**
lua-script-inline
### **Severity**
info
### **Type**
regex
### **Pattern**
  - eval\(['"](?:local|redis\.call)
  - \.eval\(`.*redis\.call
### **Message**
Lua script defined inline. Consider loading scripts with SCRIPT LOAD for reuse.
### **Fix Action**
Use SCRIPT LOAD and EVALSHA for frequently used scripts
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx