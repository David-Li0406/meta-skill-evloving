# Bullmq Specialist - Sharp Edges

## Connection Without Maxretriesperrequest

### **Id**
connection-without-maxretriesperrequest
### **Summary**
Missing maxRetriesPerRequest configuration
### **Severity**
critical
### **Situation**
  BullMQ workers stop processing after Redis connection blip. Queue appears
  frozen. Jobs pile up. No errors in logs. Eventually realize ioredis default
  retry behavior conflicts with BullMQ.
  
### **Why**
  ioredis defaults to maxRetriesPerRequest: 20 which throws after failed retries.
  BullMQ expects null (infinite retries) to handle transient Redis issues gracefully.
  Without this, any brief Redis hiccup stops all job processing permanently.
  
### **Solution**
  # Always configure ioredis for BullMQ:
  ```typescript
  import IORedis from 'ioredis';
  
  const connection = new IORedis(process.env.REDIS_URL, {
    maxRetriesPerRequest: null,  // REQUIRED for BullMQ
    enableReadyCheck: false,      // Recommended
    retryStrategy: (times) => {
      // Reconnect with exponential backoff
      return Math.min(times * 50, 2000);
    },
  });
  
  const queue = new Queue('my-queue', { connection });
  const worker = new Worker('my-queue', processor, { connection });
  ```
  
  # Common mistakes:
  - Using default ioredis configuration
  - Passing Redis URL string directly (creates default connection)
  - Different connection configs for Queue and Worker
  
### **Symptoms**
  - Workers stop processing without error
  - Jobs accumulate in 'waiting' state
  - Works locally, fails in production after Redis restart
  - "Max retries reached" in logs
### **Detection Pattern**
new (Queue|Worker)\([^)]*\)(?!.*maxRetriesPerRequest)

## Stalled Jobs Not Handled

### **Id**
stalled-jobs-not-handled
### **Summary**
Jobs stalling without recovery mechanism
### **Severity**
critical
### **Situation**
  Worker process crashes or restarts during job execution. Job stuck in 'active'
  state forever. No retry, no failure, just limbo. Queue processing stalls.
  
### **Why**
  When a worker dies mid-job, BullMQ marks the job as 'stalled' but only if
  stall detection is configured. By default, stalled jobs may not be recovered.
  Without stalledInterval and maxStalledCount, jobs can be lost.
  
### **Solution**
  # Configure stall detection on Worker:
  ```typescript
  const worker = new Worker('my-queue', processor, {
    connection,
    // Stall detection settings
    lockDuration: 30000,        // How long a job lock is held
    stalledInterval: 30000,     // Check for stalled jobs every 30s
    maxStalledCount: 2,         // Retry stalled job up to 2 times
    // Then it moves to failed with 'job stalled more than maxStalledCount'
  });
  
  // Handle stalled events
  worker.on('stalled', (jobId) => {
    console.error(`Job ${jobId} stalled - worker may have crashed`);
    // Alert operations team
  });
  ```
  
  # Job-level timeout protection:
  ```typescript
  await queue.add('process', data, {
    timeout: 60000,  // Job fails if takes longer than 60s
  });
  ```
  
  # Monitor active jobs age:
  Check for jobs stuck in 'active' for too long
  
### **Symptoms**
  - Jobs stuck in 'active' state after worker restart
  - "Stalled" events without recovery
  - Worker crash loses in-progress jobs
  - Queue gets "clogged" with phantom active jobs
### **Detection Pattern**
new Worker\([^)]*\)(?!.*stalledInterval)

## Missing Graceful Shutdown

### **Id**
missing-graceful-shutdown
### **Summary**
Worker killed without completing active jobs
### **Severity**
high
### **Situation**
  Deployment happens. SIGTERM sent. Worker immediately dies. Jobs in progress
  are orphaned. They eventually stall but data might be corrupted mid-operation.
  
### **Why**
  Node.js exits immediately on SIGTERM by default. Active jobs are abandoned
  mid-execution. Any database transactions, API calls, or file operations are
  left incomplete. Proper shutdown waits for jobs to finish.
  
### **Solution**
  # Implement graceful shutdown:
  ```typescript
  const worker = new Worker('my-queue', processor, {
    connection,
    concurrency: 5,
  });
  
  let isShuttingDown = false;
  
  async function gracefulShutdown(signal: string) {
    if (isShuttingDown) return;
    isShuttingDown = true;
  
    console.log(`${signal} received, shutting down gracefully...`);
  
    // Stop accepting new jobs
    await worker.pause();
  
    // Wait for current jobs to complete (with timeout)
    const timeout = setTimeout(() => {
      console.error('Graceful shutdown timeout, forcing exit');
      process.exit(1);
    }, 30000);  // 30 second timeout
  
    await worker.close();
    clearTimeout(timeout);
  
    // Close queue connection
    await queue.close();
  
    console.log('Worker shut down successfully');
    process.exit(0);
  }
  
  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
  ```
  
  # Docker/Kubernetes considerations:
  - Set terminationGracePeriodSeconds appropriately
  - Make job timeout < graceful shutdown timeout
  - Use preStop hook for extra time if needed
  
### **Symptoms**
  - Jobs fail during deployments
  - Stalled jobs increase after restarts
  - Data inconsistency after worker restart
  - Duplicate processing after recovery
### **Detection Pattern**
new Worker\([^)]*\)(?!.*SIGTERM|SIGINT|graceful)

## Rate Limiter Redis Cluster Incompatible

### **Id**
rate-limiter-redis-cluster-incompatible
### **Summary**
Rate limiter not working in Redis Cluster mode
### **Severity**
high
### **Situation**
  Rate limiting works perfectly locally. Deploy to production with Redis Cluster.
  Rate limits not enforced. Jobs flood downstream services.
  
### **Why**
  BullMQ's rate limiter uses multiple Redis keys that must be on the same shard.
  In Cluster mode, different keys hash to different shards. The rate limiter
  becomes ineffective or throws CROSSSLOT errors.
  
### **Solution**
  # Use hash tags to force same shard:
  ```typescript
  // BullMQ 4.x+ handles this automatically with proper queue names
  // But verify your setup:
  
  const queue = new Queue('emails', {
    connection,
    prefix: '{myapp}',  // Hash tag ensures same shard
  });
  
  const worker = new Worker('emails', processor, {
    connection,
    prefix: '{myapp}',  // Must match queue prefix
    limiter: {
      max: 100,
      duration: 60000,  // 100 jobs per minute
    },
  });
  ```
  
  # Alternative: Use group-based rate limiting (BullMQ Pro):
  ```typescript
  // Rate limit per tenant/group
  await queue.add('send-email', data, {
    group: {
      id: tenantId,
      maxSize: 10,
      limit: { max: 5, duration: 1000 },
    },
  });
  ```
  
  # If cluster issues persist:
  - Use single Redis instance for rate-limited queues
  - Implement application-level rate limiting
  
### **Symptoms**
  - Rate limits work locally, fail in production
  - CROSSSLOT errors in logs
  - Downstream services overwhelmed despite limits
  - Inconsistent rate enforcement
### **Detection Pattern**
limiter.*max.*duration(?!.*prefix.*\{)

## Large Job Data Memory Bloat

### **Id**
large-job-data-memory-bloat
### **Summary**
Storing large payloads in job data
### **Severity**
high
### **Situation**
  Jobs contain full documents, images as base64, or large arrays. Redis memory
  grows rapidly. Jobs slow to serialize/deserialize. Eventually OOM.
  
### **Why**
  Job data is stored in Redis and serialized on every operation (add, get,
  complete, fail). Large payloads multiply memory usage (active jobs, completed
  history, failed history). Redis is memory, not storage.
  
### **Solution**
  # Store references, not data:
  ```typescript
  // BAD: Large payload in job
  await queue.add('process', {
    document: fs.readFileSync('large.pdf'),  // 10MB
    images: [base64Image1, base64Image2],    // 5MB each
  });
  
  // GOOD: Store data elsewhere, pass reference
  const documentId = await uploadToS3(document);
  await queue.add('process', {
    documentId,        // Just an ID
    userId: user.id,   // Just an ID
  });
  
  // In worker, fetch what you need:
  async function processor(job) {
    const document = await downloadFromS3(job.data.documentId);
    // Process...
  }
  ```
  
  # Set job data size limits:
  ```typescript
  const MAX_JOB_SIZE = 1024 * 10;  // 10KB max
  
  async function addJob(data: any) {
    const serialized = JSON.stringify(data);
    if (serialized.length > MAX_JOB_SIZE) {
      throw new Error(`Job data too large: ${serialized.length} bytes`);
    }
    return queue.add('process', data);
  }
  ```
  
  # Configure aggressive cleanup:
  ```typescript
  defaultJobOptions: {
    removeOnComplete: { count: 100 },   // Keep only last 100
    removeOnFail: { count: 500 },       // Keep more failures for debugging
  }
  ```
  
### **Symptoms**
  - Redis memory grows continuously
  - Job add/complete operations slow
  - "OOM command not allowed" errors
  - Serialization errors for very large objects
### **Detection Pattern**
queue\.add\([^)]*JSON\.stringify|queue\.add\([^)]*Buffer|queue\.add\([^)]*readFile

## No Dead Letter Queue

### **Id**
no-dead-letter-queue
### **Summary**
Failed jobs disappear after max retries
### **Severity**
high
### **Situation**
  Job fails 3 times (default retry). It's removed from queue. No record of
  what failed or why. Bug discovered weeks later with no way to replay.
  
### **Why**
  By default, BullMQ can remove failed jobs based on removeOnFail. Without
  a DLQ strategy, you lose failed job data and cannot debug or replay.
  Failed jobs often indicate bugs that need investigation.
  
### **Solution**
  # Strategy 1: Keep failed jobs longer
  ```typescript
  const queue = new Queue('critical-jobs', {
    connection,
    defaultJobOptions: {
      attempts: 3,
      backoff: { type: 'exponential', delay: 1000 },
      removeOnComplete: { count: 1000 },
      removeOnFail: { count: 5000, age: 604800 },  // Keep 7 days
    },
  });
  ```
  
  # Strategy 2: Move to dedicated DLQ
  ```typescript
  const dlq = new Queue('dead-letter-queue', { connection });
  
  worker.on('failed', async (job, err) => {
    if (job && job.attemptsMade >= job.opts.attempts) {
      // Max retries exhausted - move to DLQ
      await dlq.add('failed-job', {
        originalQueue: 'my-queue',
        originalData: job.data,
        error: err.message,
        stack: err.stack,
        failedAt: new Date().toISOString(),
        jobId: job.id,
      });
      console.error(`Job ${job.id} moved to DLQ after ${job.attemptsMade} attempts`);
    }
  });
  ```
  
  # Strategy 3: Alert on failures
  ```typescript
  worker.on('failed', async (job, err) => {
    await alerting.send({
      channel: 'queue-failures',
      message: `Job failed: ${job?.id}`,
      error: err.message,
    });
  });
  ```
  
### **Symptoms**
  - Cannot find failed jobs to debug
  - No visibility into failure patterns
  - Cannot replay failed jobs
  - Bugs discovered with no reproduction data
### **Detection Pattern**
new Queue\([^)]*\)(?!.*removeOnFail|failed.*event)

## Repeatable Job Timezone Drift

### **Id**
repeatable-job-timezone-drift
### **Summary**
Repeatable jobs drift or miss executions
### **Severity**
medium
### **Situation**
  Scheduled job runs at 9am EST. Daylight saving happens. Now runs at 8am or
  10am. Or server timezone different from expected. Jobs fire at wrong times.
  
### **Why**
  Cron patterns are timezone-sensitive. Without explicit timezone, BullMQ uses
  server local time. Container restarts can change effective timezone. DST
  transitions cause 1-hour shifts.
  
### **Solution**
  # Always specify timezone explicitly:
  ```typescript
  await queue.add('daily-report', {}, {
    repeat: {
      pattern: '0 9 * * *',        // 9am
      tz: 'America/New_York',      // Explicit timezone
    },
  });
  
  // For UTC-based systems:
  await queue.add('hourly-sync', {}, {
    repeat: {
      pattern: '0 * * * *',
      tz: 'UTC',
    },
  });
  ```
  
  # Avoid server-local assumptions:
  ```typescript
  // BAD: Relies on server timezone
  await queue.add('backup', {}, {
    repeat: { pattern: '0 3 * * *' },  // What timezone?
  });
  
  // GOOD: Explicit and documented
  await queue.add('backup', {}, {
    repeat: {
      pattern: '0 3 * * *',
      tz: 'UTC',  // 3am UTC regardless of server location
    },
  });
  ```
  
  # Track execution times:
  Log actual execution time vs expected to detect drift
  
### **Symptoms**
  - Jobs run at wrong time after DST change
  - Different execution times in different environments
  - Jobs run hour early or late twice a year
  - Why did this run at 3am instead of 4am?
### **Detection Pattern**
repeat.*pattern(?!.*tz)

## Worker Concurrency Thundering Herd

### **Id**
worker-concurrency-thundering-herd
### **Summary**
High concurrency overwhelming downstream services
### **Severity**
high
### **Situation**
  Set concurrency to 100 for maximum throughput. All workers start. 100 * N
  workers hit database simultaneously. Database connections exhausted.
  Everything slows to crawl.
  
### **Why**
  Worker concurrency is per-worker. Multiple workers multiply the effect.
  Database connections, external APIs, and memory are shared resources.
  100 concurrent jobs per worker * 10 workers = 1000 concurrent operations.
  
### **Solution**
  # Calculate total system concurrency:
  ```typescript
  // If you have 5 worker processes, each with concurrency 10 = 50 total
  const WORKERS_COUNT = parseInt(process.env.WORKERS || '1');
  const TOTAL_DESIRED_CONCURRENCY = 50;
  const PER_WORKER_CONCURRENCY = Math.ceil(TOTAL_DESIRED_CONCURRENCY / WORKERS_COUNT);
  
  const worker = new Worker('my-queue', processor, {
    connection,
    concurrency: PER_WORKER_CONCURRENCY,
  });
  ```
  
  # Use rate limiter for external APIs:
  ```typescript
  const worker = new Worker('api-calls', processor, {
    connection,
    concurrency: 20,
    limiter: {
      max: 100,          // Max 100 jobs
      duration: 1000,    // Per second
    },
  });
  ```
  
  # Database connection pooling:
  ```typescript
  // Ensure pool size >= total concurrency
  const pool = new Pool({
    max: 50,  // Must handle all concurrent workers
  });
  ```
  
  # Start conservative, scale up:
  Begin with concurrency: 5, measure, then increase
  
### **Symptoms**
  - Database connection pool exhausted
  - External API rate limits hit immediately
  - Memory spikes when workers start
  - Timeouts under load
### **Detection Pattern**
concurrency:\s*(50|[6-9]\d|[1-9]\d{2,})

## Job Progress Not Persisted

### **Id**
job-progress-not-persisted
### **Summary**
Job progress lost on worker restart
### **Severity**
medium
### **Situation**
  Long-running job reports progress (50% complete). Worker restarts. Job
  retries from beginning. All previous work wasted. User sees progress
  reset to 0%.
  
### **Why**
  job.updateProgress() stores progress in Redis, but if job retries, it
  starts from scratch. Progress is informational, not checkpointing.
  For resumable jobs, you need application-level checkpointing.
  
### **Solution**
  # Implement checkpointing for long jobs:
  ```typescript
  async function processLargeDataset(job) {
    const { datasetId } = job.data;
  
    // Load checkpoint from database
    let checkpoint = await db.getCheckpoint(datasetId);
    let processedCount = checkpoint?.processedCount || 0;
  
    const items = await getItemsAfter(datasetId, checkpoint?.lastItemId);
    const total = await getTotalCount(datasetId);
  
    for (const item of items) {
      await processItem(item);
      processedCount++;
  
      // Save checkpoint every 100 items
      if (processedCount % 100 === 0) {
        await db.saveCheckpoint(datasetId, {
          lastItemId: item.id,
          processedCount,
        });
        await job.updateProgress((processedCount / total) * 100);
      }
    }
  
    // Clean up checkpoint on completion
    await db.deleteCheckpoint(datasetId);
    return { processed: processedCount };
  }
  ```
  
  # Make operations idempotent:
  ```typescript
  // BAD: Can't safely retry
  await db.insert('results', { value: calculated });
  
  // GOOD: Idempotent with unique key
  await db.upsert('results', {
    jobId: job.id,
    itemId: item.id,
    value: calculated,
  });
  ```
  
### **Symptoms**
  - Long jobs restart from beginning on retry
  - Users see progress reset
  - Wasted computation on retries
  - Jobs take longer than expected due to retries
### **Detection Pattern**
updateProgress(?!.*checkpoint|save|persist)

## Redis Cluster Key Migration

### **Id**
redis-cluster-key-migration
### **Summary**
Keys migrating during Redis Cluster resharding
### **Severity**
medium
### **Situation**
  Redis Cluster rebalancing or node added. Queue keys being migrated between
  nodes. Jobs fail with MOVED or ASK errors. Queue processing disrupted.
  
### **Why**
  Redis Cluster reshards by moving hash slots between nodes. During migration,
  keys in those slots may need redirection. ioredis handles this, but
  operations may fail temporarily during heavy resharding.
  
### **Solution**
  # Configure ioredis for Cluster resilience:
  ```typescript
  import Redis from 'ioredis';
  
  const connection = new Redis.Cluster([
    { host: 'node1', port: 6379 },
    { host: 'node2', port: 6379 },
    { host: 'node3', port: 6379 },
  ], {
    redisOptions: {
      maxRetriesPerRequest: null,
    },
    clusterRetryStrategy: (times) => {
      return Math.min(times * 100, 3000);
    },
    enableReadyCheck: true,
    scaleReads: 'slave',  // Read from replicas when possible
  });
  
  const queue = new Queue('my-queue', { connection });
  ```
  
  # Use hash tags for related keys:
  ```typescript
  // Ensures all keys for a queue are on same shard
  const queue = new Queue('my-queue', {
    connection,
    prefix: '{queue}',  // Hash tag
  });
  ```
  
  # Handle errors gracefully:
  ```typescript
  worker.on('error', (err) => {
    if (err.message.includes('MOVED') || err.message.includes('ASK')) {
      console.warn('Cluster resharding in progress, retrying...');
      // ioredis should auto-handle, but log for visibility
    }
  });
  ```
  
### **Symptoms**
  - MOVED/ASK errors during cluster operations
  - Jobs fail during node additions/removals
  - Temporary queue unavailability during rebalancing
  - Higher latency during resharding
### **Detection Pattern**
Redis\.Cluster(?!.*clusterRetryStrategy)

## Event Listener Memory Leak

### **Id**
event-listener-memory-leak
### **Summary**
Event listeners accumulating causing memory leak
### **Severity**
medium
### **Situation**
  Application running for days. Memory slowly growing. Eventually OOM.
  Investigation reveals thousands of event listeners on Queue/Worker.
  
### **Why**
  Each queue.on() or worker.on() adds a listener. If listeners are added
  in request handlers or loops without removal, they accumulate. Node's
  default MaxListeners warning is just a warning, not prevention.
  
### **Solution**
  # Attach listeners once at startup:
  ```typescript
  // GOOD: Attach once globally
  const worker = new Worker('my-queue', processor, { connection });
  
  worker.on('completed', (job) => {
    metrics.increment('jobs.completed');
  });
  
  worker.on('failed', (job, err) => {
    metrics.increment('jobs.failed');
    logger.error({ jobId: job?.id, error: err });
  });
  
  // Export worker, don't create per-request
  export { worker };
  ```
  
  # DON'T add listeners in request handlers:
  ```typescript
  // BAD: Adds new listener on every request
  app.post('/enqueue', async (req, res) => {
    const job = await queue.add('task', req.body);
  
    // This adds a NEW listener every request!
    worker.on('completed', (completedJob) => {
      if (completedJob.id === job.id) {
        // Handle completion
      }
    });
  });
  
  // GOOD: Use job waitUntilFinished or QueueEvents
  app.post('/enqueue', async (req, res) => {
    const job = await queue.add('task', req.body);
    const result = await job.waitUntilFinished(queueEvents, 30000);
    res.json(result);
  });
  ```
  
  # Monitor listener counts:
  ```typescript
  setInterval(() => {
    console.log({
      workerListeners: worker.listenerCount('completed'),
      queueListeners: queue.listenerCount('waiting'),
    });
  }, 60000);
  ```
  
### **Symptoms**
  - Memory grows slowly over time
  - MaxListenersExceededWarning in logs
  - Performance degrades over uptime
  - Restart temporarily fixes memory issues
### **Detection Pattern**
\.on\(['"]completed['"].*\)(?=.*app\.(get|post|put)|router\.|handle)