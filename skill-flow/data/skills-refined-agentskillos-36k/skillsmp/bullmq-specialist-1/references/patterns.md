# BullMQ Specialist

## Patterns


---
  #### **Name**
Basic Queue Setup
  #### **Description**
Production-ready BullMQ queue with proper configuration
  #### **When**
Starting any new queue implementation
  #### **Example**
    import { Queue, Worker, QueueEvents } from 'bullmq';
    import IORedis from 'ioredis';
    
    // Shared connection for all queues
    const connection = new IORedis(process.env.REDIS_URL, {
      maxRetriesPerRequest: null,  // Required for BullMQ
      enableReadyCheck: false,
    });
    
    // Create queue with sensible defaults
    const emailQueue = new Queue('emails', {
      connection,
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 1000,
        },
        removeOnComplete: { count: 1000 },
        removeOnFail: { count: 5000 },
      },
    });
    
    // Worker with concurrency limit
    const worker = new Worker('emails', async (job) => {
      await sendEmail(job.data);
    }, {
      connection,
      concurrency: 5,
      limiter: {
        max: 100,
        duration: 60000,  // 100 jobs per minute
      },
    });
    
    // Handle events
    worker.on('failed', (job, err) => {
      console.error(`Job ${job?.id} failed:`, err);
    });
    

---
  #### **Name**
Delayed and Scheduled Jobs
  #### **Description**
Jobs that run at specific times or after delays
  #### **When**
Scheduling future tasks, reminders, or timed actions
  #### **Example**
    // Delayed job - runs once after delay
    await queue.add('reminder', { userId: 123 }, {
      delay: 24 * 60 * 60 * 1000,  // 24 hours
    });
    
    // Repeatable job - runs on schedule
    await queue.add('daily-digest', { type: 'summary' }, {
      repeat: {
        pattern: '0 9 * * *',  // Every day at 9am
        tz: 'America/New_York',
      },
    });
    
    // Remove repeatable job
    await queue.removeRepeatable('daily-digest', {
      pattern: '0 9 * * *',
      tz: 'America/New_York',
    });
    

---
  #### **Name**
Job Flows and Dependencies
  #### **Description**
Complex multi-step job processing with parent-child relationships
  #### **When**
Jobs depend on other jobs completing first
  #### **Example**
    import { FlowProducer } from 'bullmq';
    
    const flowProducer = new FlowProducer({ connection });
    
    // Parent waits for all children to complete
    await flowProducer.add({
      name: 'process-order',
      queueName: 'orders',
      data: { orderId: 123 },
      children: [
        {
          name: 'validate-inventory',
          queueName: 'inventory',
          data: { orderId: 123 },
        },
        {
          name: 'charge-payment',
          queueName: 'payments',
          data: { orderId: 123 },
        },
        {
          name: 'notify-warehouse',
          queueName: 'notifications',
          data: { orderId: 123 },
        },
      ],
    });
    

---
  #### **Name**
Graceful Shutdown
  #### **Description**
Properly close workers without losing jobs
  #### **When**
Deploying or restarting workers
  #### **Example**
    const shutdown = async () => {
      console.log('Shutting down gracefully...');
    
      // Stop accepting new jobs
      await worker.pause();
    
      // Wait for current jobs to finish (with timeout)
      await worker.close();
    
      // Close queue connection
      await queue.close();
    
      process.exit(0);
    };
    
    process.on('SIGTERM', shutdown);
    process.on('SIGINT', shutdown);
    

---
  #### **Name**
Bull Board Dashboard
  #### **Description**
Visual monitoring for BullMQ queues
  #### **When**
Need visibility into queue status and job states
  #### **Example**
    import { createBullBoard } from '@bull-board/api';
    import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
    import { ExpressAdapter } from '@bull-board/express';
    
    const serverAdapter = new ExpressAdapter();
    serverAdapter.setBasePath('/admin/queues');
    
    createBullBoard({
      queues: [
        new BullMQAdapter(emailQueue),
        new BullMQAdapter(orderQueue),
      ],
      serverAdapter,
    });
    
    app.use('/admin/queues', serverAdapter.getRouter());
    

## Anti-Patterns


---
  #### **Name**
Giant Job Payloads
  #### **Description**
Storing large data directly in job data
  #### **Why**
    Redis stores job data in memory. Large payloads bloat memory usage,
    slow serialization, and can cause Redis OOM. Jobs also get logged,
    stored in completion records, etc.
    
  #### **Instead**
    Store large data in database/S3, pass only IDs in job data.
    job.data = { documentId: 123 } not { document: <100KB blob> }
    

---
  #### **Name**
No Dead Letter Queue
  #### **Description**
Letting failed jobs disappear after max retries
  #### **Why**
    Failed jobs contain valuable debugging info. Without a DLQ, you lose
    visibility into what's failing and why. Can't replay or investigate.
    
  #### **Instead**
    Configure removeOnFail to keep failed jobs, or implement custom
    DLQ logic that moves failed jobs to a separate queue for analysis.
    

---
  #### **Name**
Infinite Concurrency
  #### **Description**
Not setting concurrency limits on workers
  #### **Why**
    Unbounded concurrency can overwhelm downstream services, exhaust
    database connections, or cause memory pressure. One slow job type
    can starve others.
    
  #### **Instead**
    Start with conservative concurrency (5-10), measure, then increase.
    Use rate limiters for external API calls.
    

---
  #### **Name**
Ignoring Worker Events
  #### **Description**
Not handling failed, stalled, or error events
  #### **Why**
    Silent failures mean problems go unnoticed until users complain.
    Stalled jobs indicate worker crashes. Error events reveal connection issues.
    
  #### **Instead**
    Always attach handlers for 'failed', 'stalled', 'error' events.
    Send to monitoring/alerting system.
    

---
  #### **Name**
Sync Processing in Workers
  #### **Description**
Blocking the event loop with CPU-intensive work
  #### **Why**
    BullMQ workers are single-threaded. Blocking operations stop all
    job processing. CPU work should be in separate processes.
    
  #### **Instead**
    Use sandboxed processors for CPU-intensive work, or spawn child
    processes. Keep workers async and I/O focused.
    