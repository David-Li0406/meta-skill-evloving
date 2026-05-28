# Graphile Worker

## Patterns


---
  #### **Name**
Basic Setup
  #### **Description**
Setting up Graphile Worker with TypeScript tasks
  #### **When**
Starting with Graphile Worker
  #### **Example**
    // tasks/send-email.ts
    import type { Task } from 'graphile-worker';
    
    interface SendEmailPayload {
      to: string;
      subject: string;
      body: string;
    }
    
    export const send_email: Task = async (payload, helpers) => {
      const { to, subject, body } = payload as SendEmailPayload;
    
      helpers.logger.info(`Sending email to ${to}`);
    
      await sendEmail(to, subject, body);
    
      helpers.logger.info('Email sent successfully');
    };
    
    // Run the worker
    // npx graphile-worker -c postgres://... --watch
    
    // Or programmatically
    import { run } from 'graphile-worker';
    
    async function main() {
      const runner = await run({
        connectionString: process.env.DATABASE_URL,
        taskDirectory: './tasks',
        concurrency: 5,
      });
    
      // Graceful shutdown
      process.on('SIGTERM', () => runner.stop());
    }
    

---
  #### **Name**
Adding Jobs from SQL
  #### **Description**
Queue jobs directly from SQL or triggers
  #### **When**
Need to queue from database triggers or procedures
  #### **Example**
    -- Simple job addition
    SELECT graphile_worker.add_job(
      'send_email',
      json_build_object(
        'to', 'user@example.com',
        'subject', 'Welcome!',
        'body', 'Thanks for signing up.'
      )
    );
    
    -- With options
    SELECT graphile_worker.add_job(
      'process_order',
      json_build_object('order_id', 123),
      run_at := NOW() + INTERVAL '1 hour',
      max_attempts := 5,
      priority := 10
    );
    
    -- From a trigger (the magic!)
    CREATE OR REPLACE FUNCTION notify_new_user()
    RETURNS TRIGGER AS $$
    BEGIN
      PERFORM graphile_worker.add_job(
        'send_welcome_email',
        json_build_object(
          'user_id', NEW.id,
          'email', NEW.email
        )
      );
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER on_user_created
      AFTER INSERT ON users
      FOR EACH ROW
      EXECUTE FUNCTION notify_new_user();
    

---
  #### **Name**
Transactional Job Creation
  #### **Description**
Queue jobs in the same transaction as data changes
  #### **When**
Need atomic consistency between data and jobs
  #### **Example**
    // The job is only visible if the transaction commits
    await db.transaction(async (tx) => {
      // Insert the order
      const order = await tx.orders.create({
        data: { userId, items, total },
      });
    
      // Queue processing job - same transaction!
      await tx.$queryRaw`
        SELECT graphile_worker.add_job(
          'process_order',
          ${JSON.stringify({ orderId: order.id })}::json
        )
      `;
    
      // If anything fails, both the order AND job are rolled back
      // No orphaned jobs, no missing jobs
    });
    
    // Alternatively with quick_add_job for TypeScript
    import { quickAddJob } from 'graphile-worker';
    
    await db.transaction(async (tx) => {
      const order = await tx.orders.create({ ... });
    
      await quickAddJob(
        { pgPool: tx },  // Uses transaction connection
        'process_order',
        { orderId: order.id }
      );
    });
    

---
  #### **Name**
Cron Scheduling
  #### **Description**
Recurring jobs using built-in cron
  #### **When**
Need periodic tasks like reports or cleanup
  #### **Example**
    // In your crontab file or programmatically
    import { run, parseCronItems } from 'graphile-worker';
    
    const runner = await run({
      connectionString: process.env.DATABASE_URL,
      taskDirectory: './tasks',
      crontabFile: './crontab',
    });
    
    // crontab file:
    // # Daily cleanup at 3am
    // 0 3 * * * cleanup_old_records
    //
    // # Hourly stats update
    // 0 * * * * update_stats ?max_attempts=3
    //
    // # Every 5 minutes with payload
    // */5 * * * * health_check {"notify": true}
    
    // Or programmatic cron
    const runner = await run({
      connectionString: process.env.DATABASE_URL,
      taskDirectory: './tasks',
      parsedCronItems: parseCronItems([
        { task: 'cleanup_old_records', pattern: '0 3 * * *' },
        { task: 'update_stats', pattern: '0 * * * *', options: { maxAttempts: 3 } },
      ]),
    });
    

---
  #### **Name**
Batch Processing by Key
  #### **Description**
Process related jobs together efficiently
  #### **When**
Many jobs for same entity should be batched
  #### **Example**
    // Queue many jobs for same user
    await quickAddJob(pool, 'sync_user_data', { userId: 123, field: 'email' },
      { jobKey: 'sync-user-123' });
    await quickAddJob(pool, 'sync_user_data', { userId: 123, field: 'name' },
      { jobKey: 'sync-user-123' });
    await quickAddJob(pool, 'sync_user_data', { userId: 123, field: 'avatar' },
      { jobKey: 'sync-user-123' });
    
    // With jobKeyMode: 'preserve_run_at', only one job runs
    // and receives all the payloads
    
    // Or use batch helper in task
    import type { Task } from 'graphile-worker';
    
    export const sync_user_data: Task = async (payload, helpers) => {
      // payload might be single object or array if batched
      const payloads = Array.isArray(payload) ? payload : [payload];
    
      const userId = payloads[0].userId;
      const fields = payloads.map(p => p.field);
    
      helpers.logger.info(`Syncing ${fields.length} fields for user ${userId}`);
    
      // Sync all fields in one operation
      await syncUserFields(userId, fields);
    };
    

---
  #### **Name**
Job Deduplication
  #### **Description**
Prevent duplicate jobs for same work
  #### **When**
Same job might be queued multiple times
  #### **Example**
    -- Using job_key for deduplication
    SELECT graphile_worker.add_job(
      'send_reminder',
      json_build_object('user_id', 123),
      job_key := 'reminder-user-123',
      job_key_mode := 'replace'  -- or 'preserve_run_at'
    );
    
    -- 'replace': New job replaces existing (resets run_at)
    -- 'preserve_run_at': Keeps earliest run_at
    -- 'unsafe_dedupe': Silently ignores if job exists
    
    // TypeScript
    import { quickAddJob } from 'graphile-worker';
    
    await quickAddJob(pool, 'send_reminder', { userId: 123 }, {
      jobKey: 'reminder-user-123',
      jobKeyMode: 'preserve_run_at',
    });
    
    // Queue as many times as you want - only one job will exist
    

## Anti-Patterns


---
  #### **Name**
Polling Instead of LISTEN/NOTIFY
  #### **Description**
Disabling LISTEN/NOTIFY and using polling
  #### **Why**
    Graphile Worker's speed comes from LISTEN/NOTIFY. Polling adds
    latency (seconds) and unnecessary database load.
    
  #### **Instead**
    Keep LISTEN/NOTIFY enabled (the default). If you need polling
    for edge cases, use a hybrid approach.
    

---
  #### **Name**
Long-Running Tasks Without Heartbeat
  #### **Description**
Tasks that take minutes without progress reporting
  #### **Why**
    Without progress updates, the worker might be considered stuck.
    Other workers won't take over, and monitoring is blind.
    
  #### **Instead**
    Use helpers.job.updateProgress() for long tasks.
    Break very long tasks into smaller jobs.
    

---
  #### **Name**
Not Using Transactions for Consistency
  #### **Description**
Queuing jobs outside the data transaction
  #### **Why**
    If you insert data and queue a job separately, one might succeed
    while the other fails. You get inconsistent state.
    
  #### **Instead**
    Queue jobs in the same transaction as related data changes.
    Use triggers for automatic, consistent job creation.
    

---
  #### **Name**
Huge Payloads
  #### **Description**
Passing large data in job payloads
  #### **Why**
    Payloads are stored in PostgreSQL. Large payloads slow everything
    and bloat the jobs table.
    
  #### **Instead**
    Pass IDs and references. Fetch data in the task.
    Store large data in appropriate storage (S3, etc.).
    

---
  #### **Name**
Not Handling Errors Properly
  #### **Description**
Swallowing errors or not logging failures
  #### **Why**
    Failed jobs retry, but without proper error info, debugging is
    impossible. Silent failures accumulate.
    
  #### **Instead**
    Let errors propagate (they trigger retries). Use helpers.logger
    to record context. Check failed jobs regularly.
    