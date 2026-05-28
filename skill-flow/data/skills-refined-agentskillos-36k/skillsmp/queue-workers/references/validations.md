# Queue Workers - Validations

## Job Without Idempotency Check

### **Id**
queue-no-idempotency
### **Severity**
error
### **Type**
regex
### **Pattern**
  - queue\.add\([^)]+\)(?![\s\S]{0,500}idempotency)
  - async.*job.*\{(?![\s\S]{0,300}redis\.get|redis\.exists|setnx)
### **Message**
Job processing should check for idempotency to prevent duplicate side effects on retry.
### **Fix Action**
Add idempotency check using Redis SETNX before processing
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/workers/**
  - **/jobs/**

## Mutating Job Data

### **Id**
queue-data-mutation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - job\.data\.[a-zA-Z]+\s*=
  - job\.data\s*=\s*\{
### **Message**
Job data should be treated as immutable. Mutating it causes issues on retry.
### **Fix Action**
Create a copy of job.data instead of mutating it
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/workers/**

## No Dead Letter Queue

### **Id**
queue-no-dlq
### **Severity**
error
### **Type**
regex
### **Pattern**
  - attempts.*[3-9](?![\s\S]{0,800}dlq|dead.?letter|failed.?queue)
  - maxAttempts(?![\s\S]{0,800}dlq|dead.?letter)
### **Message**
Jobs with retry limits should have a dead letter queue for failed jobs.
### **Fix Action**
Add DLQ handling for jobs that exhaust retries
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing Graceful Shutdown

### **Id**
queue-no-graceful-shutdown
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Worker\([^)]+\)(?![\s\S]{0,2000}SIGTERM|SIGINT|graceful)
### **Message**
Worker needs graceful shutdown to prevent job loss on deploy/restart.
### **Fix Action**
Add SIGTERM/SIGINT handlers that call worker.close()
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/workers/**

## Job Without Timeout

### **Id**
queue-no-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Worker\([^)]+\)(?![\s\S]{0,500}lockDuration|timeout)
  - async.*job.*\{(?![\s\S]{0,300}AbortController|setTimeout|Promise\.race)
### **Message**
Jobs should have timeout to prevent hanging workers.
### **Fix Action**
Add lockDuration to worker options or use AbortController for operations
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/workers/**

## Unbounded Retry Count

### **Id**
queue-unbounded-retries
### **Severity**
error
### **Type**
regex
### **Pattern**
  - attempts.*Infinity
  - attempts.*999
  - maxRetries.*Infinity
### **Message**
Jobs with infinite retries can become zombies. Set a reasonable limit.
### **Fix Action**
Set attempts to 3-5 and handle permanent failures with DLQ
### **Applies To**
  - **/*.ts
  - **/*.js

## Worker Without Error Handling

### **Id**
queue-no-error-handling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Worker\([^,]+,\s*async.*\{(?![\s\S]{0,500}try|catch)
### **Message**
Worker processor should have error handling for proper failure tracking.
### **Fix Action**
Add try/catch and handle errors appropriately
### **Applies To**
  - **/*.ts
  - **/*.js

## Fixed Retry Delay Without Backoff

### **Id**
queue-no-backoff
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backoff.*fixed
  - retryDelay.*[0-9]+(?![\s\S]{0,100}exponential|Math\.pow)
### **Message**
Fixed retry delay can overwhelm services. Use exponential backoff.
### **Fix Action**
Use backoff: { type: 'exponential', delay: 1000 }
### **Applies To**
  - **/*.ts
  - **/*.js

## Backoff Without Jitter

### **Id**
queue-no-jitter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - exponential(?![\s\S]{0,200}jitter|random)
  - retryStrategy(?![\s\S]{0,200}random|Math\.random)
### **Message**
Exponential backoff without jitter causes thundering herd on reconnect.
### **Fix Action**
Add random jitter to retry delays
### **Applies To**
  - **/*.ts
  - **/*.js

## No Concurrency Limit

### **Id**
queue-no-concurrency-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Worker\([^)]+\)(?![\s\S]{0,300}concurrency)
### **Message**
Worker should have concurrency limit to control resource usage.
### **Fix Action**
Add concurrency option: concurrency: 5
### **Applies To**
  - **/*.ts
  - **/*.js

## No Rate Limiting for External APIs

### **Id**
queue-no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - queue.*api|api.*queue(?![\s\S]{0,500}limiter|rateLimit)
  - fetch\([^)]+\)(?![\s\S]{0,300}limiter)
### **Message**
Jobs calling external APIs should have rate limiting.
### **Fix Action**
Add limiter option or use rate-limiter-flexible
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/workers/**

## Long Job Without Progress Updates

### **Id**
queue-no-progress
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*items(?![\s\S]{0,500}updateProgress|progress)
  - forEach(?![\s\S]{0,500}updateProgress)
### **Message**
Long-running batch jobs should report progress.
### **Fix Action**
Add job.updateProgress() in processing loop
### **Applies To**
  - **/*.ts
  - **/*.js

## No Correlation ID in Jobs

### **Id**
queue-no-correlation-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - queue\.add\([^)]+\)(?![\s\S]{0,200}correlationId|requestId|traceId)
### **Message**
Jobs should include correlation ID for distributed tracing.
### **Fix Action**
Include correlationId in job data from request context
### **Applies To**
  - **/*.ts
  - **/*.js

## Worker Without Event Logging

### **Id**
queue-no-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Worker(?![\s\S]{0,1000}on\(['"]completed|on\(['"]failed)
### **Message**
Worker should log job completion and failure events.
### **Fix Action**
Add worker.on('completed') and worker.on('failed') handlers with logging
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Redis Connection

### **Id**
queue-hardcoded-connection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Redis\(['"]redis://localhost
  - host.*['"]localhost['"]
  - port.*6379
### **Message**
Redis connection should use environment variables.
### **Fix Action**
Use process.env.REDIS_URL or REDIS_HOST/REDIS_PORT
### **Applies To**
  - **/*.ts
  - **/*.js

## No Job Cleanup Configuration

### **Id**
queue-no-job-removal
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Queue(?![\s\S]{0,500}removeOnComplete|removeOnFail)
### **Message**
Queue should configure job removal to prevent memory growth.
### **Fix Action**
Add removeOnComplete and removeOnFail options
### **Applies To**
  - **/*.ts
  - **/*.js

## Synchronous Operations in Worker

### **Id**
queue-sync-in-worker
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - readFileSync|writeFileSync|execSync
  - JSON\.parse\(fs\.readFileSync
### **Message**
Avoid synchronous operations in workers - they block the event loop.
### **Fix Action**
Use async versions: readFile, writeFile, exec
### **Applies To**
  - **/workers/**
  - **/jobs/**

## Delayed Jobs Without Scheduler

### **Id**
queue-no-scheduler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - delay.*[0-9]+(?![\s\S]{0,500}QueueScheduler)
### **Message**
Delayed jobs require QueueScheduler for reliable execution.
### **Fix Action**
Create QueueScheduler for the queue
### **Applies To**
  - **/*.ts
  - **/*.js

## In-Memory Queue for Important Jobs

### **Id**
queue-memory-storage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Queue.*memory
  - bull.*connection.*null
### **Message**
In-memory queues lose jobs on restart. Use Redis for persistence.
### **Fix Action**
Connect to Redis for job persistence
### **Applies To**
  - **/*.ts
  - **/*.js

## No Worker Health Check

### **Id**
queue-no-health-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Worker(?![\s\S]{0,2000}/health|healthCheck)
### **Message**
Workers should expose health check endpoint for orchestration.
### **Fix Action**
Add /health endpoint that checks worker status and queue depth
### **Applies To**
  - **/*.ts
  - **/*.js