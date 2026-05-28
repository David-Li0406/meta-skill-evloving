# Bullmq Specialist - Validations

## Redis connection missing maxRetriesPerRequest

### **Id**
missing-maxretriesperrequest
### **Description**
BullMQ requires maxRetriesPerRequest null for proper reconnection handling
### **Severity**
error
### **Pattern**
new (Queue|Worker|FlowProducer)\s*\(
### **Negative Pattern**
maxRetriesPerRequest\s*:\s*null
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
BullMQ queue/worker created without maxRetriesPerRequest: null on Redis connection. This will cause workers to stop on Redis connection issues.
### **Fix Hint**
Create ioredis connection with maxRetriesPerRequest: null and pass it to Queue/Worker

## No stalled job event handler

### **Id**
missing-stalled-handler
### **Description**
Workers should handle stalled events to detect crashed workers
### **Severity**
warning
### **Pattern**
new Worker\s*\([^)]+\)
### **Negative Pattern**
\.on\(['"]stalled
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Worker created without 'stalled' event handler. Stalled jobs indicate worker crashes and should be monitored.
### **Fix Hint**
Add worker.on('stalled', (jobId) => { /* alert */ })

## No failed job event handler

### **Id**
missing-failed-handler
### **Description**
Workers should handle failed events for monitoring and alerting
### **Severity**
warning
### **Pattern**
new Worker\s*\([^)]+\)
### **Negative Pattern**
\.on\(['"]failed
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Worker created without 'failed' event handler. Failed jobs should be logged and monitored.
### **Fix Hint**
Add worker.on('failed', (job, err) => { /* log/alert */ })

## No graceful shutdown handling

### **Id**
missing-graceful-shutdown
### **Description**
Workers should gracefully shut down on SIGTERM/SIGINT
### **Severity**
warning
### **Pattern**
new Worker\s*\([^)]+\)
### **Negative Pattern**
SIGTERM|SIGINT|graceful|shutdown
### **File Patterns**
  - **/worker*.ts
  - **/worker*.js
  - **/queue*.ts
  - **/jobs/**/*.ts
### **Message**
Worker file without graceful shutdown handling. Jobs may be orphaned on deployment.
### **Fix Hint**
Add process.on('SIGTERM', async () => { await worker.close(); })

## Awaiting queue.add in request handler

### **Id**
sync-queue-add-in-request
### **Description**
Queue additions should be fire-and-forget in request handlers
### **Severity**
info
### **Pattern**
await\s+queue\.add\s*\(
### **File Patterns**
  - **/api/**/*.ts
  - **/routes/**/*.ts
  - **/pages/api/**/*.ts
  - **/app/**/route.ts
### **Message**
Queue.add awaited in request handler. Consider fire-and-forget for faster response.
### **Fix Hint**
Use queue.add() without await, or use void queue.add() to indicate intentional fire-and-forget

## Potentially large data in job payload

### **Id**
large-job-payload
### **Description**
Job data should be small - pass IDs not full objects
### **Severity**
warning
### **Pattern**
queue\.add\([^)]*\{[^}]{200,}\}
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Job appears to have large inline data. Pass IDs instead of full objects to keep Redis memory low.
### **Fix Hint**
Store large data in database/S3, pass only IDs: { documentId: id } instead of { document: {...} }

## Job without timeout configuration

### **Id**
missing-job-timeout
### **Description**
Jobs should have timeouts to prevent infinite execution
### **Severity**
info
### **Pattern**
queue\.add\s*\([^)]+\{[^}]*\}\s*\)
### **Negative Pattern**
timeout\s*:
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Job added without explicit timeout. Consider adding timeout to prevent stuck jobs.
### **Fix Hint**
Add { timeout: 60000 } to job options for 60 second timeout

## Retry without backoff strategy

### **Id**
missing-backoff-strategy
### **Description**
Retries should use exponential backoff to avoid thundering herd
### **Severity**
warning
### **Pattern**
attempts\s*:\s*[2-9]|attempts\s*:\s*\d{2,}
### **Negative Pattern**
backoff\s*:
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Job has retry attempts but no backoff strategy. Use exponential backoff to prevent thundering herd.
### **Fix Hint**
Add backoff: { type: 'exponential', delay: 1000 } to job options

## Repeatable job without explicit timezone

### **Id**
repeatable-without-timezone
### **Description**
Repeatable jobs should specify timezone to avoid DST issues
### **Severity**
warning
### **Pattern**
repeat\s*:\s*\{[^}]*pattern\s*:
### **Negative Pattern**
tz\s*:
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Repeatable job without explicit timezone. Will use server local time which can drift with DST.
### **Fix Hint**
Add tz: 'America/New_York' or tz: 'UTC' to repeat options

## Potentially high worker concurrency

### **Id**
high-concurrency-warning
### **Description**
High concurrency can overwhelm downstream services
### **Severity**
info
### **Pattern**
concurrency\s*:\s*(50|[6-9]\d|[1-9]\d{2,})
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Worker concurrency is high. Ensure downstream services can handle this load (DB connections, API rate limits).
### **Fix Hint**
Start with concurrency: 5-10, measure, then scale up. Use rate limiter for external APIs.

## No removeOnComplete configuration

### **Id**
missing-remove-on-complete
### **Description**
Completed jobs should be cleaned up to prevent memory bloat
### **Severity**
warning
### **Pattern**
new Queue\s*\([^)]+\)
### **Negative Pattern**
removeOnComplete
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Queue without removeOnComplete configuration. Completed jobs will accumulate in Redis.
### **Fix Hint**
Add defaultJobOptions: { removeOnComplete: { count: 1000 } } to queue options

## No removeOnFail configuration

### **Id**
missing-remove-on-fail
### **Description**
Failed jobs cleanup should be configured for visibility
### **Severity**
info
### **Pattern**
new Queue\s*\([^)]+\)
### **Negative Pattern**
removeOnFail
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Queue without removeOnFail configuration. Consider keeping failed jobs for debugging.
### **Fix Hint**
Add defaultJobOptions: { removeOnFail: { count: 5000, age: 604800 } } to keep 7 days of failures

## Queue without prefix in cluster mode

### **Id**
queue-without-prefix
### **Description**
Redis Cluster requires hash tag prefix for rate limiting to work
### **Severity**
warning
### **Pattern**
Redis\.Cluster|cluster\s*:
### **Negative Pattern**
prefix\s*:\s*['"]\{
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Using Redis Cluster but queue may not have hash tag prefix. Rate limiting may not work correctly.
### **Fix Hint**
Add prefix: '{myapp}' to queue options for cluster compatibility

## Event listener added in request handler

### **Id**
event-listener-in-handler
### **Description**
Adding listeners in request handlers causes memory leaks
### **Severity**
error
### **Pattern**
(queue|worker)\.on\s*\(['"]
### **File Patterns**
  - **/api/**/*.ts
  - **/routes/**/*.ts
  - **/pages/api/**/*.ts
  - **/app/**/route.ts
### **Exclude Patterns**
  - **/*.test.*
  - **/*.spec.*
### **Message**
Event listener added in request handler. This causes memory leaks - listeners accumulate per request.
### **Fix Hint**
Move event listeners to module-level initialization, not inside request handlers

## Job processor without try-catch

### **Id**
job-processor-no-error-handling
### **Description**
Job processors should handle errors explicitly
### **Severity**
warning
### **Pattern**
new Worker\s*\([^,]+,\s*async\s*\([^)]*\)\s*=>\s*\{
### **Negative Pattern**
try\s*\{|catch\s*\(
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Job processor without apparent error handling. Wrap in try-catch for proper error context.
### **Fix Hint**
Add try-catch in processor to log errors with job context before rethrowing

## Hardcoded Redis connection URL

### **Id**
hardcoded-redis-url
### **Description**
Redis URLs should come from environment variables
### **Severity**
warning
### **Pattern**
new (Redis|IORedis)\s*\(['"]redis://|localhost:\d+
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Exclude Patterns**
  - **/*.test.*
  - **/*.spec.*
  - **/*.example.*
### **Message**
Redis URL appears hardcoded. Use environment variable for flexibility.
### **Fix Hint**
Use process.env.REDIS_URL or similar

## Using job.waitUntilFinished without QueueEvents

### **Id**
missing-queue-events
### **Description**
waitUntilFinished requires QueueEvents instance
### **Severity**
error
### **Pattern**
waitUntilFinished\s*\(
### **Negative Pattern**
QueueEvents|queueEvents
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Using waitUntilFinished but QueueEvents not visible. Ensure QueueEvents is instantiated.
### **Fix Hint**
Create QueueEvents instance: const queueEvents = new QueueEvents('my-queue', { connection })

## FlowProducer without queue name validation

### **Id**
flow-producer-without-proper-setup
### **Description**
FlowProducer jobs must reference existing queues
### **Severity**
info
### **Pattern**
FlowProducer.*add\s*\(
### **Negative Pattern**
queueName.*Queue|queue.*name
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
FlowProducer used - ensure all queueName references match actual Queue instances.
### **Fix Hint**
Verify each child job's queueName has a corresponding Queue and Worker

## Potentially blocking operation in job processor

### **Id**
blocking-operation-in-processor
### **Description**
Avoid sync operations that block the event loop
### **Severity**
warning
### **Pattern**
readFileSync|writeFileSync|execSync|spawnSync|JSON\.parse\([^)]{500,}
### **File Patterns**
  - **/worker*.ts
  - **/processor*.ts
  - **/jobs/**/*.ts
### **Message**
Potentially blocking operation in worker. Use async variants to avoid blocking other jobs.
### **Fix Hint**
Use async fs methods, child_process with promises, or spawn separate process for CPU work