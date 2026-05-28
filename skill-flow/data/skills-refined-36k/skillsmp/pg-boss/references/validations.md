# Pg Boss - Validations

## Job Without Expiration

### **Id**
no-expiration-set
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - boss\.send\([^)]+\)(?!.*expireIn)
  - \.send\([^,]+,[^,]+\)(?!.*expire)
### **Message**
Job without expiration. Stuck jobs won't retry if worker crashes.
### **Fix Action**
Add expireInSeconds: await boss.send('q', data, { expireInSeconds: 300 })
### **Applies To**
  - **/*.ts
  - **/*.js

## Job Without Retry Limit

### **Id**
no-retry-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - boss\.send\([^)]+\)(?!.*retryLimit)
  - \.send\([^,]+,[^,]+\)(?!.*retry)
### **Message**
Job without retry limit. Default is 2, consider setting explicitly.
### **Fix Action**
Add retryLimit: await boss.send('q', data, { retryLimit: 5 })
### **Applies To**
  - **/*.ts
  - **/*.js

## Critical Job Without Dead Letter Queue

### **Id**
no-dead-letter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - send\(["'](?:payment|order|critical)[^"']*["'][^)]+\)(?!.*deadLetter)
### **Message**
Critical job without dead letter queue. Failed jobs will be lost.
### **Fix Action**
Add deadLetter: { deadLetter: 'failed-critical-jobs' }
### **Applies To**
  - **/*.ts
  - **/*.js

## Team Size Too Large for Connection Pool

### **Id**
large-team-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - teamSize\s*:\s*([2-9]\d|\d{3,})
  - teamSize\s*:\s*[5-9][0-9]
### **Message**
Large teamSize may exhaust database connections.
### **Fix Action**
Keep teamSize reasonable (5-10), use connection pooler
### **Applies To**
  - **/*.ts
  - **/*.js

## pg-boss Without Archive Configuration

### **Id**
no-archive-config
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new PgBoss\(\{[^}]+\}\)(?!.*archiveCompleted)
  - PgBoss\([^)]+\)(?!.*archive)
### **Message**
pg-boss without archive config. Completed jobs will accumulate.
### **Fix Action**
Add archiveCompletedAfterSeconds and deleteAfterSeconds
### **Applies To**
  - **/*.ts
  - **/*.js

## Error Swallowed in Job Handler

### **Id**
error-swallowed
### **Severity**
error
### **Type**
regex
### **Pattern**
  - boss\.work.*catch\s*\([^)]*\)\s*\{[^}]*console
  - work.*async.*catch.*\}(?!.*throw)
### **Message**
Error swallowed in job handler. Job won't retry on failure.
### **Fix Action**
Re-throw error after logging: catch (e) { log(e); throw e; }
### **Applies To**
  - **/*.ts
  - **/*.js

## Worker Without Graceful Shutdown

### **Id**
no-graceful-shutdown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - boss\.start\(\)(?!.*SIGTERM|stop)
  - await boss\.work(?!.*stop)
### **Message**
Worker without graceful shutdown. In-flight jobs may be lost.
### **Fix Action**
Add: process.on('SIGTERM', async () => { await boss.stop(); })
### **Applies To**
  - **/*.ts
  - **/*.js

## Synchronous Blocking in Job Handler

### **Id**
sync-in-handler
### **Severity**
error
### **Type**
regex
### **Pattern**
  - boss\.work.*fs\.readFileSync
  - work.*execSync
  - work.*\.forEach\(async
### **Message**
Blocking operation in async handler. Use async alternatives.
### **Fix Action**
Use fs.promises, promisified exec, for...of with await
### **Applies To**
  - **/*.ts
  - **/*.js

## Supabase Transaction Mode Connection

### **Id**
supabase-wrong-port
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - PgBoss.*:6543
  - DATABASE_URL.*pooler.*supabase
### **Message**
Using Supabase transaction mode (6543). Use session mode or direct connection.
### **Fix Action**
Use direct connection (port 5432) or session mode pooler
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/.env*

## Multiple Insert Calls Instead of Batch

### **Id**
insert-without-batch
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*boss\.send\(
  - forEach.*await.*\.send\(
  - map.*boss\.send
### **Message**
Multiple send calls in loop. Use boss.insert for batch efficiency.
### **Fix Action**
Use boss.insert([{ name, data }, ...]) for batch inserts
### **Applies To**
  - **/*.ts
  - **/*.js

## pg-boss Without Connection Limits

### **Id**
missing-connection-config
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new PgBoss\([^)]+\)(?!.*max\s*:)
### **Message**
pg-boss without max connection limit. May create too many connections.
### **Fix Action**
Add max: 10 to limit internal connection pool
### **Applies To**
  - **/*.ts
  - **/*.js