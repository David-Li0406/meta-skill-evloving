# Performance Thinker - Validations

## Potential N+1 Query Pattern

### **Id**
n-plus-one-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*await.*find
  - for.*await.*query
  - \.forEach.*await.*get
  - map.*async.*fetch
### **Message**
Database query inside loop suggests N+1 problem. Consider eager loading.
### **Fix Action**
Use batch query or eager loading: findAll with IDs instead of find in loop
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Query Without Limit

### **Id**
unbounded-query
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.find\(\{\}\)
  - \.all\(\)
  - SELECT\s+\*\s+FROM(?!.*LIMIT)
  - findMany\(\{\s*\}\)
### **Message**
Query without limit can return unbounded results. Add pagination.
### **Fix Action**
Add .limit() or LIMIT clause to prevent loading entire table
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - \.limit\(
  - LIMIT\s+\d
  - \.take\(

## Synchronous I/O in Loop

### **Id**
sync-io-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*readFileSync
  - for.*writeFileSync
  - while.*readFileSync
### **Message**
Sync I/O in loop blocks event loop. Consider async or batching.
### **Fix Action**
Use async methods: readFile with Promise.all for parallel reads
### **Applies To**
  - **/*.ts
  - **/*.js

## Sequential Awaits That Could Be Parallel

### **Id**
sequential-awaits
### **Severity**
info
### **Type**
regex
### **Pattern**
  - await\s+\w+\([^)]*\);\s*await\s+\w+\([^)]*\);\s*await\s+\w+\([^)]*\)
### **Message**
Multiple sequential awaits may be parallelizable. Consider Promise.all.
### **Fix Action**
If independent: const [a,b,c] = await Promise.all([fetchA(), fetchB(), fetchC()])
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## In-Memory Cache Without Size Limit

### **Id**
unbounded-cache
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - const\s+cache\s*=\s*new\s+Map\(\)
  - const\s+cache\s*=\s*\{\}
  - let\s+cache\s*=\s*\{\}
### **Message**
In-memory cache without size limit can cause memory leak.
### **Fix Action**
Use LRU cache with size limit or add periodic cleanup
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - LRU
  - maxSize
  - max:

## String Concatenation in Loop

### **Id**
string-concat-loop
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*\+=.*['"`]
  - while.*\+=.*['"`]
### **Message**
String concatenation in loop is O(n²). Use array join or StringBuilder.
### **Fix Action**
Collect in array, then join: parts.push(x); return parts.join('')
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## JSON Parse in Hot Loop

### **Id**
json-parse-in-loop
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*JSON\.parse
  - \.forEach.*JSON\.parse
  - \.map.*JSON\.parse
### **Message**
JSON.parse in loop is expensive. Consider parsing once outside loop.
### **Fix Action**
Parse the collection once before iterating if possible
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Returning Entire Objects

### **Id**
large-payload-return
### **Severity**
info
### **Type**
regex
### **Pattern**
  - return\s+.*\.toJSON\(\)
  - return\s+.*\.toObject\(\)
  - res\.json\(\s*await.*\.find
### **Message**
Returning entire object may include unnecessary fields. Consider selecting fields.
### **Fix Action**
Select only needed fields or use DTOs to limit response size
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Query on Likely Unindexed Column

### **Id**
missing-index-hint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - WHERE.*created_at\s*[<>]
  - WHERE.*status\s*=
  - ORDER BY.*created_at
  - WHERE.*email\s*=
### **Message**
Query pattern suggests index might help. Verify index exists for this column.
### **Fix Action**
Check EXPLAIN plan; add index if sequential scan on large table
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.sql

## Potentially Inefficient Regex

### **Id**
inefficient-regex
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new RegExp\([^)]*\+[^)]*\)
  - \.match\(/.*\*.*\*/\)
  - \.test\(/.*\+.*\+.*\+.*/
### **Message**
Complex regex can be slow. Consider if simpler string operations work.
### **Fix Action**
For simple patterns, use indexOf/includes instead of regex
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Array.includes on Large Arrays

### **Id**
array-includes-large
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.includes\(.*\)\s*//.*large
  - for.*\.includes\(
### **Message**
Array.includes is O(n). For large arrays or frequent lookups, use Set.
### **Fix Action**
const lookup = new Set(array); lookup.has(x) is O(1)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Synchronous Crypto Operations

### **Id**
sync-crypto
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - crypto\.pbkdf2Sync
  - crypto\.scryptSync
  - bcrypt\.hashSync
  - bcrypt\.compareSync
### **Message**
Sync crypto blocks event loop. Use async versions in web servers.
### **Fix Action**
Use async: crypto.pbkdf2, bcrypt.hash (without Sync)
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - cli
  - script
  - build

## setTimeout/setInterval in Request Handler

### **Id**
timeout-in-hot-path
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.get.*setTimeout
  - app\.post.*setTimeout
  - router\.get.*setTimeout
### **Message**
Timeout in request handler suggests async work. Use queue instead.
### **Fix Action**
Queue background work instead of setTimeout: queue.enqueue(job)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Reading Entire File Into Memory

### **Id**
loading-entire-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - readFileSync\([^)]+\)
  - readFile\([^)]+\)
  - fs\.promises\.readFile
### **Message**
Reading entire file may be problematic for large files. Consider streaming.
### **Fix Action**
For large files, use createReadStream with pipeline
### **Applies To**
  - **/*.ts
  - **/*.js

## Database Connection Without Pooling

### **Id**
no-connection-pooling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Client\(\)
  - createConnection\(
  - mysql\.createConnection
### **Message**
Creating connection per request is expensive. Use connection pool.
### **Fix Action**
Use pool: createPool() instead of createConnection()
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Excessive Logging in Hot Path

### **Id**
logging-in-hot-path
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log.*req\.
  - logger\.debug.*for\s*\(
### **Message**
Logging in hot path adds latency. Consider sampling or log level guards.
### **Fix Action**
Use log level guards: if (logger.isDebugEnabled()) logger.debug(...)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx