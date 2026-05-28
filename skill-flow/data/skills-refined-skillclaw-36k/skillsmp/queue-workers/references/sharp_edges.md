# Queue Workers - Sharp Edges

## No Idempotency Key

### **Id**
no-idempotency-key
### **Summary**
Jobs without idempotency cause duplicate side effects on retry
### **Severity**
critical
### **Situation**
  You add a job to send an email or charge a payment. The job fails after
  completing the action but before acknowledging completion. BullMQ retries.
  User receives duplicate email or is double-charged.
  
### **Why**
  Queues guarantee at-least-once delivery, not exactly-once:
  - Job runs, completes action, crashes before ack
  - Queue thinks job failed, retries
  - Action runs again
  
  Without idempotency checking, every retry repeats the action.
  
### **Solution**
  Use idempotency keys for all side-effect jobs:
  
  async function processPayment(job: Job) {
    const idempotencyKey = `payment:${job.id}`;
  
    // Check if already processed
    const existing = await redis.get(idempotencyKey);
    if (existing) {
      return JSON.parse(existing);  // Return cached result
    }
  
    // Process payment with Stripe's idempotency
    const result = await stripe.charges.create({
      amount: job.data.amount,
      currency: 'usd',
      idempotency_key: job.id,  // Stripe checks this
    });
  
    // Cache result for future retries
    await redis.setex(idempotencyKey, 86400, JSON.stringify(result));
  
    return result;
  }
  
  // For operations without built-in idempotency:
  async function sendEmail(job: Job) {
    const sentKey = `email:${job.id}`;
  
    // Atomic check-and-set
    const wasNew = await redis.set(sentKey, '1', 'NX', 'EX', 86400);
    if (!wasNew) {
      console.log(`Email ${job.id} already sent`);
      return { skipped: true };
    }
  
    try {
      await emailService.send(job.data);
      return { sent: true };
    } catch (error) {
      // Clear key so retry can attempt again
      await redis.del(sentKey);
      throw error;
    }
  }
  
### **Symptoms**
  - Duplicate emails sent
  - Customers charged multiple times
  - Duplicate database records created
  - "Why did this run twice?" in logs
### **Detection Pattern**
queue\\.add(?![\\s\\S]{0,300}idempotency|dedupe)

## No Dlq

### **Id**
no-dlq
### **Summary**
Failed jobs disappear without dead letter queue
### **Severity**
critical
### **Situation**
  Jobs fail after max retries. Without a dead letter queue, they're removed
  from the queue. You lose visibility into what failed and why. Critical
  operations fail silently.
  
### **Why**
  After exhausting retries, BullMQ marks jobs as failed but eventually
  removes them based on removeOnFail settings. If you don't:
  - Move them to a DLQ for investigation
  - Alert on failures
  - Log detailed error information
  
  Then failed jobs are just... gone.
  
### **Solution**
  Always implement a dead letter queue:
  
  const mainQueue = new Queue('orders', { connection: redis });
  const dlq = new Queue('orders-dlq', { connection: redis });
  
  const worker = new Worker('orders', async (job) => {
    try {
      await processOrder(job.data);
    } catch (error) {
      // Check if this is the final attempt
      const isLastAttempt = job.attemptsMade >= (job.opts.attempts || 3) - 1;
  
      if (isLastAttempt) {
        // Move to DLQ before failing
        await dlq.add('failed-order', {
          originalJob: {
            id: job.id,
            name: job.name,
            data: job.data,
            attemptsMade: job.attemptsMade + 1,
          },
          error: {
            name: error.name,
            message: error.message,
            stack: error.stack,
          },
          failedAt: new Date().toISOString(),
        });
  
        // Alert ops team
        await slack.send('#ops-alerts', {
          text: `Order ${job.data.orderId} failed after ${job.attemptsMade + 1} attempts`,
          color: 'danger',
        });
      }
  
      throw error;  // Re-throw to trigger retry or mark failed
    }
  }, { connection: redis });
  
  // DLQ processor for manual review or auto-remediation
  const dlqWorker = new Worker('orders-dlq', async (job) => {
    // Create ticket for investigation
    await jira.createIssue({
      type: 'Bug',
      priority: 'High',
      summary: `Failed order: ${job.data.originalJob.data.orderId}`,
      description: job.data.error.stack,
    });
  }, { connection: redis });
  
### **Symptoms**
  - Where did that job go?
  - Silent failures in critical paths
  - No way to investigate past failures
  - Users report issues but no logs found
### **Detection Pattern**
attempts.*[3-9](?![\\s\\S]{0,500}dlq|dead.?letter)

## No Graceful Shutdown

### **Id**
no-graceful-shutdown
### **Summary**
Worker shutdown kills jobs mid-processing
### **Severity**
critical
### **Situation**
  Your process receives SIGTERM during a deploy. The worker is killed
  immediately, leaving jobs in an inconsistent state. Some jobs appear
  as "active" forever because they never completed or failed.
  
### **Why**
  Default Node.js behavior on SIGTERM is immediate exit:
  - Active jobs are interrupted mid-processing
  - Redis still thinks they're active (lock held)
  - Jobs stuck until lock expires
  - Data may be partially processed
  
### **Solution**
  Implement graceful shutdown:
  
  const worker = new Worker('orders', processOrder, { connection: redis });
  
  let isShuttingDown = false;
  
  async function gracefulShutdown(signal: string) {
    if (isShuttingDown) return;
    isShuttingDown = true;
  
    console.log(`Received ${signal}, starting graceful shutdown...`);
  
    // Stop accepting new jobs
    await worker.pause();
  
    // Wait for active jobs to complete
    console.log('Waiting for active jobs to complete...');
  
    // Close worker (waits for active jobs)
    await worker.close();
  
    console.log('Worker closed gracefully');
    process.exit(0);
  }
  
  // Handle shutdown signals
  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
  
  // Timeout for long-running jobs
  const SHUTDOWN_TIMEOUT = 30000;  // 30 seconds
  
  async function gracefulShutdownWithTimeout(signal: string) {
    if (isShuttingDown) return;
    isShuttingDown = true;
  
    const timeout = setTimeout(() => {
      console.error('Shutdown timeout - forcing exit');
      process.exit(1);
    }, SHUTDOWN_TIMEOUT);
  
    await worker.close();
    clearTimeout(timeout);
    process.exit(0);
  }
  
### **Symptoms**
  - Jobs stuck in "active" state after deploy
  - "Lock expired" errors
  - Partial data processing
  - Zombie jobs in queue
### **Detection Pattern**
new Worker(?![\\s\\S]{0,1000}SIGTERM|graceful)

## Job Data Mutation

### **Id**
job-data-mutation
### **Summary**
Mutating job data causes race conditions and debugging nightmares
### **Severity**
critical
### **Situation**
  Worker modifies job.data during processing. If the job is retried,
  the modified data is used. Or worse, with concurrency > 1, multiple
  workers read/modify the same job data reference.
  
### **Why**
  Job data should be immutable during processing:
  - Retries should use original data
  - Debugging needs original state
  - Concurrent access may cause races
  
### **Solution**
  Treat job data as immutable:
  
  // BAD - mutating job data
  async function process(job: Job) {
    job.data.processedAt = new Date();  // Don't do this!
    job.data.items = job.data.items.filter(x => x.valid);  // Mutation!
    await save(job.data);
  }
  
  // GOOD - work with copies
  async function process(job: Job) {
    const data = {
      ...job.data,
      processedAt: new Date(),
      items: job.data.items.filter(x => x.valid),
    };
    await save(data);
  }
  
  // Store processing metadata separately
  async function processWithMetadata(job: Job) {
    const startTime = Date.now();
    const result = await doWork(job.data);
  
    // Store processing info in result, not job.data
    return {
      result,
      processingTime: Date.now() - startTime,
      workerId: process.env.WORKER_ID,
    };
  }
  
### **Symptoms**
  - Retry uses wrong data
  - Debugging shows modified state
  - Race conditions with concurrent workers
  - Data was different on retry
### **Detection Pattern**
job\\.data\\.[a-zA-Z]+\\s*=

## No Job Timeout

### **Id**
no-job-timeout
### **Summary**
Jobs without timeout can hang forever and block workers
### **Severity**
high
### **Situation**
  A job calls an external API that hangs. The worker waits forever.
  With limited concurrency, this blocks the entire queue. Eventually
  all workers are stuck on hung jobs.
  
### **Why**
  Network calls, database queries, and external APIs can hang:
  - TCP connection established but no response
  - API stuck in processing
  - Database deadlock
  
  Without timeout, the job never fails, just waits.
  
### **Solution**
  Always add timeouts:
  
  // Worker-level timeout
  const worker = new Worker('api-calls', async (job) => {
    return callApi(job.data);
  }, {
    connection: redis,
    lockDuration: 60000,       // Lock expires after 60s
    stalledInterval: 30000,   // Check for stalled jobs every 30s
  });
  
  // Job-level timeout with AbortController
  async function process(job: Job) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
  
    try {
      const result = await fetch(job.data.url, {
        signal: controller.signal,
      });
      return result.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Job timed out after 30 seconds');
      }
      throw error;
    } finally {
      clearTimeout(timeout);
    }
  }
  
  // Promise.race for operations without AbortController
  async function processWithRaceTimeout(job: Job) {
    const result = await Promise.race([
      doWork(job.data),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout')), 30000)
      ),
    ]);
    return result;
  }
  
### **Symptoms**
  - Workers stuck on same job for hours
  - Queue depth keeps growing
  - "All workers busy" but nothing processing
  - Metrics show jobs active but not completing
### **Detection Pattern**
new Worker(?![\\s\\S]{0,500}lockDuration|timeout)

## Thundering Herd Reconnect

### **Id**
thundering-herd-reconnect
### **Summary**
All workers reconnect simultaneously after Redis restart
### **Severity**
high
### **Situation**
  Redis restarts. All 100 workers try to reconnect at the same instant.
  Redis is overwhelmed by connection storm. Connections fail.
  Exponential backoff kicks in but all workers are synchronized.
  
### **Why**
  When Redis goes down and comes back:
  - All workers detect failure at ~same time
  - All workers retry at ~same time
  - This repeats with backoff (2s, 4s, 8s...)
  - But they're all synchronized!
  
### **Solution**
  Add jitter to reconnection:
  
  import Redis from 'ioredis';
  
  // ioredis with jitter
  const redis = new Redis({
    host: process.env.REDIS_HOST,
    port: 6379,
    retryStrategy: (times) => {
      // Base delay with exponential backoff
      const baseDelay = Math.min(times * 1000, 30000);
  
      // Add random jitter (0-50% of delay)
      const jitter = Math.random() * baseDelay * 0.5;
  
      return baseDelay + jitter;
    },
    maxRetriesPerRequest: null,  // Required for BullMQ
  });
  
  // Worker startup with staggered delay
  async function startWorker(workerId: number, totalWorkers: number) {
    // Stagger startup over 10 seconds
    const delay = (workerId / totalWorkers) * 10000;
    await sleep(delay);
  
    const worker = new Worker('queue', process, {
      connection: redis,
    });
  }
  
  // Start workers with stagger
  for (let i = 0; i < NUM_WORKERS; i++) {
    startWorker(i, NUM_WORKERS);
  }
  
### **Symptoms**
  - Redis CPU spike on restart
  - "Connection refused" bursts
  - All workers reconnect at same second
  - Cascading failures
### **Detection Pattern**
retryStrategy(?![\\s\\S]{0,200}jitter|random)

## No Backpressure

### **Id**
no-backpressure
### **Summary**
Workers accept jobs faster than they can process
### **Severity**
high
### **Situation**
  Jobs arrive at 1000/second. Workers can process 100/second. Queue
  grows unbounded. Memory fills up. Eventually Redis OOM or workers
  crash trying to process the backlog.
  
### **Why**
  Without backpressure:
  - Producers add jobs without limits
  - Queue grows unbounded
  - Memory/disk exhausted
  - System collapses under load
  
### **Solution**
  Implement backpressure:
  
  // 1. Limit queue size
  async function addWithBackpressure(queue: Queue, name: string, data: any) {
    const waitingCount = await queue.getWaitingCount();
  
    if (waitingCount > 10000) {
      // Reject new jobs when queue is full
      throw new Error('Queue full - try again later');
    }
  
    return queue.add(name, data);
  }
  
  // 2. Rate limit producers
  import { RateLimiterRedis } from 'rate-limiter-flexible';
  
  const limiter = new RateLimiterRedis({
    storeClient: redis,
    points: 100,        // 100 jobs
    duration: 1,        // Per second
    keyPrefix: 'queue-limiter',
  });
  
  async function addWithRateLimit(queue: Queue, name: string, data: any) {
    await limiter.consume('producer');  // Throws if rate exceeded
    return queue.add(name, data);
  }
  
  // 3. Use flow control
  const queue = new Queue('jobs', {
    connection: redis,
    limiter: {
      max: 100,          // Max 100 jobs
      duration: 1000,    // Per second
    },
  });
  
  // 4. Monitor and alert
  async function monitorQueueDepth() {
    const depth = await queue.getWaitingCount();
  
    if (depth > 5000) {
      await alerting.send('Queue depth critical', { depth });
    }
  }
  
### **Symptoms**
  - Queue depth growing unbounded
  - Redis memory exhausted
  - Workers can't keep up
  - System slowdown under load
### **Detection Pattern**
queue\\.add(?![\\s\\S]{0,500}waiting|depth|backpressure)

## Unbounded Retries

### **Id**
unbounded-retries
### **Summary**
Jobs retry forever, creating zombie jobs
### **Severity**
high
### **Situation**
  Job fails due to permanent error (invalid data, deleted resource).
  With attempts: Infinity or high retry count, it retries forever.
  These zombie jobs consume resources and generate noise.
  
### **Why**
  Not all errors are transient:
  - ValidationError: Data will never be valid
  - NotFoundError: Resource deleted
  - AuthorizationError: Permissions won't change
  
  Retrying these is pointless and wasteful.
  
### **Solution**
  Classify errors and handle appropriately:
  
  // Error classification
  function isRetryable(error: Error): boolean {
    // Never retry these
    const permanentErrors = [
      'ValidationError',
      'NotFoundError',
      'AuthorizationError',
      'PaymentDeclinedError',
    ];
  
    if (permanentErrors.includes(error.name)) {
      return false;
    }
  
    // Always retry these
    const transientPatterns = [
      'ECONNRESET',
      'ETIMEDOUT',
      'rate limit',
      '503',
      '429',
    ];
  
    return transientPatterns.some(p =>
      error.message.toLowerCase().includes(p.toLowerCase())
    );
  }
  
  // Worker with smart retry
  const worker = new Worker('jobs', async (job) => {
    try {
      await process(job.data);
    } catch (error) {
      if (!isRetryable(error)) {
        // Move to DLQ immediately, don't retry
        await dlq.add('permanent-failure', {
          job: job.data,
          error: error.message,
        });
        return;  // Don't throw - job completes (failed but not retried)
      }
      throw error;  // Throw to trigger retry
    }
  }, {
    connection: redis,
    defaultJobOptions: {
      attempts: 5,  // Reasonable limit
    },
  });
  
### **Symptoms**
  - Jobs failing for days
  - High retry count in logs
  - Wasted compute on hopeless jobs
  - Noise in monitoring
### **Detection Pattern**
attempts.*Infinity|attempts.*[2-9][0-9]

## No Job Progress

### **Id**
no-job-progress
### **Summary**
Long jobs show no progress, appear stuck
### **Severity**
medium
### **Situation**
  A job takes 10 minutes to process. There's no progress updates.
  Operators can't tell if it's stuck or working. Monitoring shows
  "job active for 10 minutes" which could be normal or a hang.
  
### **Why**
  Without progress updates:
  - Can't distinguish stuck from slow
  - No visibility into large batch jobs
  - Users see "processing" with no feedback
  - Operators may kill healthy jobs
  
### **Solution**
  Report progress for long jobs:
  
  const worker = new Worker('batch-process', async (job) => {
    const items = job.data.items;
    const total = items.length;
  
    for (let i = 0; i < total; i++) {
      await processItem(items[i]);
  
      // Update progress (0-100)
      await job.updateProgress(Math.round((i + 1) / total * 100));
  
      // Or detailed progress
      await job.updateProgress({
        current: i + 1,
        total,
        lastProcessed: items[i].id,
      });
    }
  }, { connection: redis });
  
  // Check progress from API
  app.get('/job/:id/progress', async (req, res) => {
    const job = await queue.getJob(req.params.id);
    const progress = await job?.progress;
  
    res.json({
      id: job?.id,
      state: await job?.getState(),
      progress,
    });
  });
  
  // Real-time progress via events
  const queueEvents = new QueueEvents('batch-process', { connection: redis });
  
  queueEvents.on('progress', ({ jobId, data }) => {
    io.to(`job:${jobId}`).emit('progress', data);
  });
  
### **Symptoms**
  - Long jobs appear stuck
  - Operators kill healthy jobs
  - Users have no feedback
  - Can't estimate completion time
### **Detection Pattern**
new Worker(?![\\s\\S]{0,1000}updateProgress)

## Single Point Of Failure

### **Id**
single-point-of-failure
### **Summary**
Single worker instance means queue stops on crash
### **Severity**
medium
### **Situation**
  You run one worker. It crashes. Queue backs up. You don't notice
  for hours because there's no redundancy or alerting.
  
### **Why**
  Single worker = single point of failure:
  - Crash stops all processing
  - Deploy causes processing gap
  - No load distribution
  - No failover
  
### **Solution**
  Run multiple workers with proper monitoring:
  
  // Run at least 2 workers (different processes/containers)
  // Each can have internal concurrency
  
  const worker = new Worker('queue', process, {
    connection: redis,
    concurrency: 5,  // 5 concurrent jobs per worker
  });
  
  // Health check endpoint
  let lastJobCompleted = Date.now();
  
  worker.on('completed', () => {
    lastJobCompleted = Date.now();
  });
  
  app.get('/health', async (req, res) => {
    const waiting = await queue.getWaitingCount();
    const timeSinceJob = Date.now() - lastJobCompleted;
  
    // Unhealthy if jobs waiting but none completed recently
    if (waiting > 0 && timeSinceJob > 60000) {
      return res.status(503).json({
        status: 'unhealthy',
        waiting,
        lastJobAgo: timeSinceJob,
      });
    }
  
    res.json({ status: 'healthy' });
  });
  
  // Alert on worker count
  async function monitorWorkers() {
    const workers = await queue.getWorkers();
  
    if (workers.length < 2) {
      await alerting.send('Low worker count', {
        count: workers.length,
        expected: 2,
      });
    }
  }
  
### **Symptoms**
  - Queue backs up during deploys
  - Single crash stops processing
  - No redundancy
  - Processing gaps in metrics
### **Detection Pattern**
replicas.*1\\b|instances.*1\\b

## Missing Correlation Id

### **Id**
missing-correlation-id
### **Summary**
Can't trace job through distributed system
### **Severity**
medium
### **Situation**
  User reports "my order failed." You check logs. No way to connect
  the HTTP request to the queued job to the downstream services.
  Debugging is a guessing game.
  
### **Why**
  Without correlation IDs:
  - Can't follow request through system
  - Can't correlate logs across services
  - Debugging requires guesswork
  - Incident response is slow
  
### **Solution**
  Pass correlation ID through the entire flow:
  
  import { randomUUID } from 'crypto';
  
  // Middleware to set correlation ID
  app.use((req, res, next) => {
    req.correlationId = req.headers['x-correlation-id'] as string || randomUUID();
    res.setHeader('x-correlation-id', req.correlationId);
    next();
  });
  
  // Add correlation ID to jobs
  app.post('/orders', async (req, res) => {
    const job = await queue.add('process-order', {
      ...req.body,
      correlationId: req.correlationId,  // Include in job data
    });
  
    res.json({ orderId: job.id, correlationId: req.correlationId });
  });
  
  // Worker logs with correlation ID
  const worker = new Worker('orders', async (job) => {
    const { correlationId, ...data } = job.data;
  
    logger.info('Processing order', {
      jobId: job.id,
      correlationId,  // Always include
    });
  
    // Pass to downstream calls
    await inventoryService.reserve(data.productId, {
      headers: { 'x-correlation-id': correlationId },
    });
  }, { connection: redis });
  
  // Search logs by correlation ID
  // In Datadog/Kibana: correlationId:"abc-123"
  
### **Symptoms**
  - Can't trace requests through system
  - Debugging requires guesswork
  - Incident response is slow
  - Which request caused this job?
### **Detection Pattern**
queue\\.add(?![\\s\\S]{0,300}correlationId|requestId|traceId)