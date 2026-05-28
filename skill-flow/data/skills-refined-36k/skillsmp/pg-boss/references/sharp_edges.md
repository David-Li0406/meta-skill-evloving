# Pg Boss - Sharp Edges

## No Expiration

### **Id**
no-expiration
### **Summary**
Jobs without expiration can get stuck forever
### **Severity**
high
### **Situation**
Worker crashes mid-job, job stays "active" indefinitely
### **Why**
  Without expireInSeconds, a job taken by a crashed worker stays in
  "active" state forever. No other worker can pick it up. It never
  retries. It just sits there blocking progress.
  
### **Solution**
  1. Always set expireInSeconds for jobs:
     await boss.send('task', data, {
       expireInSeconds: 300,  // 5 minutes
       retryLimit: 3,
     });
  
  2. Set default at boss level:
     const boss = new PgBoss({
       connectionString: process.env.DATABASE_URL,
       expireInDefault: 300,
     });
  
  3. Monitor stuck jobs:
     SELECT * FROM pgboss.job
     WHERE state = 'active'
     AND startedon < NOW() - INTERVAL '1 hour';
  
### **Symptoms**
  - Jobs stuck in "active" state
  - Worker crashed but job never retried
  - Growing backlog with no errors
### **Detection Pattern**
expireInSeconds|expireIn|stuck.*active

## Connection Exhaustion

### **Id**
connection-exhaustion
### **Summary**
Too many workers exhaust database connections
### **Severity**
high
### **Situation**
"FATAL: too many connections" during high load
### **Why**
  Each pg-boss worker maintains database connections. With teamSize=10
  and multiple worker processes, you quickly exhaust max_connections.
  Supabase has strict connection limits (20-60 depending on plan).
  
### **Solution**
  1. Size workers based on available connections:
     // If max_connections = 50, reserve 30 for app, 20 for workers
     await boss.work('queue', { teamSize: 5 }, handler);
  
  2. Use connection pooler (PgBouncer/Supavisor):
     const boss = new PgBoss({
       connectionString: process.env.POOLER_URL,
       // Pooler handles connection limits
     });
  
  3. Monitor connection usage:
     SELECT count(*) FROM pg_stat_activity
     WHERE application_name LIKE '%pg-boss%';
  
  4. Set pool limits in pg-boss:
     const boss = new PgBoss({
       connectionString: process.env.DATABASE_URL,
       max: 10,  // Max connections in internal pool
     });
  
### **Symptoms**
  - "too many connections" errors
  - Workers failing to start
  - App connections rejected
### **Detection Pattern**
max_connections|teamSize|pool.*size

## No Dead Letter

### **Id**
no-dead-letter
### **Summary**
Failed jobs disappear after retries, no visibility
### **Severity**
medium
### **Situation**
Jobs fail repeatedly and vanish, can't investigate
### **Why**
  Without a dead letter queue, jobs that exhaust retries just go to
  "failed" state and eventually archive. You lose the ability to
  investigate, replay, or alert on persistent failures.
  
### **Solution**
  1. Configure dead letter queue:
     await boss.send('important-task', data, {
       retryLimit: 3,
       deadLetter: 'failed-important-tasks',
     });
  
  2. Process dead letter queue for alerting:
     await boss.work('failed-important-tasks', async (job) => {
       // Send to Slack/PagerDuty
       await alertTeam({
         queue: job.data.originalQueue,
         error: job.data.error,
       });
       // Optionally store for later replay
     });
  
  3. Monitor dead letter queue:
     SELECT name, COUNT(*) FROM pgboss.job
     WHERE name LIKE 'failed-%'
     AND state = 'created'
     GROUP BY name;
  
### **Symptoms**
  - Failed jobs just disappear
  - No alerting on persistent failures
  - Can't replay failed jobs
### **Detection Pattern**
deadLetter|failed.*queue|DLQ

## Huge Job Data

### **Id**
huge-job-data
### **Summary**
Large payloads bloat database and slow queries
### **Severity**
medium
### **Situation**
Job table grows huge, queries become slow
### **Why**
  Job data is stored in PostgreSQL jsonb column. Large payloads
  (files, full documents, arrays of thousands) bloat the table,
  slow down job fetching, and increase backup sizes.
  
### **Solution**
  1. Store references instead of data:
     // Bad
     await boss.send('process', { document: hugeBlob });
  
     // Good
     await boss.send('process', { documentId: doc.id });
  
  2. For files, use external storage:
     const url = await uploadToS3(file);
     await boss.send('process', { fileUrl: url });
  
  3. Check payload sizes:
     SELECT pg_size_pretty(avg(length(data::text)::int))
     FROM pgboss.job
     WHERE name = 'my-queue';
  
  4. Set up archiving to keep table lean:
     const boss = new PgBoss({
       archiveCompletedAfterSeconds: 7 * 24 * 3600,  // 7 days
       deleteAfterSeconds: 30 * 24 * 3600,  // 30 days
     });
  
### **Symptoms**
  - Job table gigabytes in size
  - Slow job fetching
  - Large database backups
### **Detection Pattern**
payload.*size|data.*large|jsonb.*size

## Archive Not Configured

### **Id**
archive-not-configured
### **Summary**
Completed jobs accumulate forever
### **Severity**
medium
### **Situation**
Jobs table grows unbounded, queries slow down
### **Why**
  Without archiving, completed jobs stay in the main table forever.
  The table grows linearly with job volume. Indexes become inefficient.
  Even simple status queries slow down.
  
### **Solution**
  1. Configure archiving in constructor:
     const boss = new PgBoss({
       connectionString: process.env.DATABASE_URL,
       archiveCompletedAfterSeconds: 7 * 24 * 3600,  // 7 days
       deleteAfterSeconds: 30 * 24 * 3600,  // 30 days
     });
  
  2. Monitor table size:
     SELECT pg_size_pretty(pg_total_relation_size('pgboss.job'));
     SELECT state, COUNT(*) FROM pgboss.job GROUP BY state;
  
  3. For existing bloat, manual cleanup:
     DELETE FROM pgboss.job
     WHERE state IN ('completed', 'cancelled')
     AND completedon < NOW() - INTERVAL '30 days';
     VACUUM pgboss.job;
  
### **Symptoms**
  - Jobs table millions of rows
  - Slow queue status queries
  - Growing disk usage
### **Detection Pattern**
archiveCompleted|deleteAfter|archive.*config

## Supabase Connection Mode

### **Id**
supabase-connection-mode
### **Summary**
Wrong Supabase connection mode causes issues
### **Severity**
high
### **Situation**
Jobs not processing or connections failing with Supabase
### **Why**
  Supabase offers two connection modes: session (port 5432) and
  transaction (port 6543). pg-boss needs session mode for proper
  connection handling. Transaction mode causes subtle issues.
  
### **Solution**
  1. Use session mode connection string:
     # Session mode (correct)
     postgresql://user:pass@host:5432/db
  
     # Transaction mode (problems)
     postgresql://user:pass@host:6543/db
  
  2. Or use direct connection (bypasses pooler):
     const boss = new PgBoss({
       connectionString: process.env.SUPABASE_DB_URL,  // Direct
     });
  
  3. If using Supavisor pooler:
     // Append ?pgbouncer=true for some ORMs
     // But pg-boss works better with direct connection
  
### **Symptoms**
  - Intermittent connection failures
  - Jobs not picked up
  - prepared statement already exists
### **Detection Pattern**
Supabase|port.*6543|connection.*mode

## Singleton Race Condition

### **Id**
singleton-race-condition
### **Summary**
Singleton key doesn't prevent concurrent execution
### **Severity**
medium
### **Situation**
Same singleton job runs multiple times simultaneously
### **Why**
  singletonKey prevents multiple jobs from being QUEUED, not from
  running simultaneously. If job A is active and you queue job B
  with same key, B waits. But if two workers grab the same job
  before state updates, both run.
  
### **Solution**
  1. Understand singleton semantics:
     // singletonKey: Only one job with this key in queue
     // Does NOT prevent concurrent execution of same work
  
  2. For true mutual exclusion, use singletonKey + useSingletonQueue:
     await boss.send('exclusive-task', data, {
       singletonKey: 'my-exclusive-work',
       useSingletonQueue: true,
     });
  
  3. Or implement locking in your task:
     await boss.work('task', async (job) => {
       const lock = await acquireLock(job.data.resourceId);
       if (!lock) {
         throw new Error('Could not acquire lock');
       }
       try {
         await doWork();
       } finally {
         await releaseLock(lock);
       }
     });
  
### **Symptoms**
  - Same work done multiple times
  - Race conditions in task logic
  - Duplicate side effects
### **Detection Pattern**
singletonKey|singleton.*concurrent|mutex