# Graphile Worker - Sharp Edges

## Listen Notify Disabled

### **Id**
listen-notify-disabled
### **Summary**
Polling instead of LISTEN/NOTIFY causes latency
### **Severity**
high
### **Situation**
Jobs not picked up immediately, seconds of delay
### **Why**
  Graphile Worker's speed comes from LISTEN/NOTIFY. When disabled,
  it falls back to polling which adds 1-5 seconds of latency per job.
  This defeats the main advantage of Graphile Worker.
  
### **Solution**
  1. Ensure LISTEN/NOTIFY is enabled (default):
     const runner = await run({
       connectionString: process.env.DATABASE_URL,
       // Don't set noHandleSignals or disable notify
     });
  
  2. If using connection pooler, ensure it supports LISTEN:
     - PgBouncer: Use session mode, not transaction mode
     - Supabase: Use direct connection, not pooler for worker
  
  3. Verify LISTEN is working:
     SELECT * FROM pg_stat_activity WHERE query LIKE '%LISTEN%';
  
### **Symptoms**
  - Jobs take seconds to start instead of milliseconds
  - Worker logs show polling messages
  - High CPU from frequent polling queries
### **Detection Pattern**
poll|noHandleSignals|LISTEN.*disabled

## Transaction Not Used

### **Id**
transaction-not-used
### **Summary**
Job queued outside data transaction causes inconsistency
### **Severity**
high
### **Situation**
Data saved but job not created, or vice versa
### **Why**
  If you insert data and queue a job in separate transactions, one can
  succeed while the other fails. You end up with orphaned data or
  missing jobs. The atomicity guarantee is lost.
  
### **Solution**
  1. Queue in same transaction as data:
     await db.transaction(async (tx) => {
       const order = await tx.orders.create({ ... });
       await tx.$queryRaw`
         SELECT graphile_worker.add_job(
           'process_order',
           ${JSON.stringify({ orderId: order.id })}::json
         )
       `;
     });
  
  2. Or use triggers for automatic queueing:
     CREATE TRIGGER on_order_created
       AFTER INSERT ON orders
       FOR EACH ROW
       EXECUTE FUNCTION queue_order_processing();
  
  3. Use quickAddJob with transaction connection:
     await quickAddJob({ pgPool: tx }, 'task', payload);
  
### **Symptoms**
  - Jobs reference data that doesn't exist
  - Data exists but job never ran
  - Inconsistent state after errors
### **Detection Pattern**
add_job.*outside.*transaction|separate.*commit

## Huge Payloads

### **Id**
huge-payloads
### **Summary**
Large job payloads bloat database and slow processing
### **Severity**
medium
### **Situation**
Job data contains full objects instead of references
### **Why**
  Job payloads are stored in PostgreSQL. Large payloads (files, full
  documents, arrays of thousands of items) bloat the jobs table,
  slow down queries, and increase backup sizes significantly.
  
### **Solution**
  1. Store references, not data:
     // Bad
     await addJob('process', { document: hugeDocument });
  
     // Good
     await addJob('process', { documentId: doc.id });
  
  2. For files, store in S3/R2 and pass URL:
     const url = await uploadToS3(file);
     await addJob('process-file', { fileUrl: url });
  
  3. Monitor payload sizes:
     SELECT pg_size_pretty(avg(length(payload::text)::int))
     FROM graphile_worker.jobs;
  
### **Symptoms**
  - Job table grows faster than expected
  - Slow job fetching and processing
  - Large database backups
### **Detection Pattern**
payload.*size|large.*data|blob.*job

## No Error Handling

### **Id**
no-error-handling
### **Summary**
Errors swallowed in task handler, retries don't work
### **Severity**
high
### **Situation**
Tasks fail silently, no retries triggered
### **Why**
  Graphile Worker retries failed jobs automatically, but only if the
  error propagates. If you catch and swallow errors, the job appears
  successful and won't retry. Silent failures accumulate.
  
### **Solution**
  1. Let errors propagate:
     // Bad
     export const myTask: Task = async (payload) => {
       try {
         await riskyOperation();
       } catch (e) {
         console.error(e); // Error swallowed, job "succeeds"
       }
     };
  
     // Good
     export const myTask: Task = async (payload, helpers) => {
       try {
         await riskyOperation();
       } catch (e) {
         helpers.logger.error('Failed', { error: e });
         throw e; // Error propagates, job retries
       }
     };
  
  2. Use helpers.logger for context:
     helpers.logger.info('Processing', { orderId: payload.id });
  
  3. Check failed jobs regularly:
     SELECT * FROM graphile_worker.jobs
     WHERE attempts >= max_attempts;
  
### **Symptoms**
  - Jobs marked complete but work not done
  - No retry attempts for failed operations
  - Silent failures in logs
### **Detection Pattern**
catch.*console|swallow.*error|no.*throw

## Long Running No Progress

### **Id**
long-running-no-progress
### **Summary**
Long-running tasks appear stuck, no visibility
### **Severity**
medium
### **Situation**
Task takes minutes, no progress updates, worker seems frozen
### **Why**
  Without progress reporting, monitoring is blind. The task might be
  working fine but looks stuck. Other systems might kill the worker
  thinking it's frozen. No way to estimate completion.
  
### **Solution**
  1. Report progress for long tasks:
     export const bigTask: Task = async (payload, helpers) => {
       const items = await fetchItems();
       for (let i = 0; i < items.length; i++) {
         await processItem(items[i]);
         await helpers.job.updateProgress(
           Math.round((i / items.length) * 100)
         );
       }
     };
  
  2. Break into smaller jobs for very long operations:
     // Instead of one 30-minute job
     // Create 100 smaller jobs and aggregate
  
  3. Set appropriate max_attempts and backoff:
     SELECT graphile_worker.add_job(
       'long_task',
       payload,
       max_attempts := 3,
       backoff := '10 minutes'
     );
  
### **Symptoms**
  - Workers appear frozen but are actually working
  - No progress visibility in monitoring
  - Premature task termination
### **Detection Pattern**
updateProgress|long.running|timeout

## Connection Pooler Listen

### **Id**
connection-pooler-listen
### **Summary**
LISTEN/NOTIFY doesn't work through connection pooler
### **Severity**
high
### **Situation**
Using PgBouncer in transaction mode, jobs delayed
### **Why**
  LISTEN requires a persistent connection. Connection poolers in
  transaction mode (PgBouncer default) don't maintain persistent
  connections. LISTEN commands are lost when connection returns to pool.
  
### **Solution**
  1. Use session mode for Graphile Worker:
     # PgBouncer config for worker connection
     [databases]
     worker = host=db port=5432 dbname=app pool_mode=session
  
  2. Or use direct connection for worker only:
     // App uses pooler
     const appPool = process.env.DATABASE_URL; // pooler
  
     // Worker uses direct
     const workerConn = process.env.DATABASE_URL_DIRECT; // direct
  
  3. For Supabase, use direct connection string:
     // Not the pooler URL (port 6543)
     // Use direct URL (port 5432)
  
### **Symptoms**
  - Jobs take seconds to pick up
  - LISTEN command has no effect
  - Worker falls back to polling
### **Detection Pattern**
PgBouncer|transaction.mode|pooler.*LISTEN

## Cron Timezone Confusion

### **Id**
cron-timezone-confusion
### **Summary**
Cron jobs run at wrong times due to timezone mismatch
### **Severity**
medium
### **Situation**
Scheduled jobs fire at unexpected hours
### **Why**
  Cron schedules default to UTC. If you expect 9am local time but
  the server is in UTC, the job runs at the wrong hour. Daylight
  saving time changes make this worse.
  
### **Solution**
  1. Always specify timezone in cron:
     // crontab file
     # 0 9 * * * {task} ?tz=America/New_York
  
     // Or programmatically
     parseCronItems([{
       task: 'daily_report',
       pattern: '0 9 * * *',
       options: { tz: 'America/New_York' }
     }]);
  
  2. Use UTC and convert in task if needed:
     # Always clear: 14:00 UTC
     0 14 * * * daily_report
  
  3. Test timezone handling:
     SELECT NOW() AT TIME ZONE 'America/New_York';
  
### **Symptoms**
  - Jobs run at wrong local time
  - Inconsistent timing during DST changes
  - Confusion about when jobs will run
### **Detection Pattern**
timezone|cron.*tz|schedule.*UTC