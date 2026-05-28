# pg-boss Specialist

## Patterns


---
  #### **Name**
Basic Setup
  #### **Description**
Setting up pg-boss with PostgreSQL
  #### **When**
Starting with pg-boss in any Node.js project
  #### **Example**
    import PgBoss from 'pg-boss';
    
    // Initialize with connection string
    const boss = new PgBoss({
      connectionString: process.env.DATABASE_URL,
      // Archive completed jobs after 7 days
      archiveCompletedAfterSeconds: 60 * 60 * 24 * 7,
      // Delete archived jobs after 30 days
      deleteAfterSeconds: 60 * 60 * 24 * 30,
    });
    
    // Start the boss
    await boss.start();
    
    // Define a worker
    await boss.work('send-email', async (job) => {
      const { to, subject, body } = job.data;
      await sendEmail(to, subject, body);
      // Job automatically completed on success
      // Throw to fail and trigger retry
    });
    
    // Queue a job
    await boss.send('send-email', {
      to: 'user@example.com',
      subject: 'Welcome!',
      body: 'Thanks for signing up.',
    });
    
    // Graceful shutdown
    process.on('SIGTERM', async () => {
      await boss.stop();
      process.exit(0);
    });
    

---
  #### **Name**
Delayed and Scheduled Jobs
  #### **Description**
Jobs that run at specific times
  #### **When**
Reminders, scheduled tasks, or delayed processing
  #### **Example**
    import PgBoss from 'pg-boss';
    
    const boss = new PgBoss(process.env.DATABASE_URL);
    await boss.start();
    
    // Delayed job - run after 1 hour
    await boss.send('reminder', { userId: '123' }, {
      startAfter: 60 * 60,  // seconds from now
    });
    
    // Specific time
    await boss.send('scheduled-report', { type: 'weekly' }, {
      startAfter: new Date('2025-01-01T09:00:00Z'),
    });
    
    // Cron schedule - daily at 9am
    await boss.schedule('daily-digest', '0 9 * * *', {
      tz: 'America/New_York',
    });
    
    // Worker for scheduled jobs
    await boss.work('daily-digest', async () => {
      await generateAndSendDigest();
    });
    

---
  #### **Name**
Job Options and Retries
  #### **Description**
Configuring job behavior
  #### **When**
Need specific retry, timeout, or priority settings
  #### **Example**
    import PgBoss from 'pg-boss';
    
    const boss = new PgBoss(process.env.DATABASE_URL);
    await boss.start();
    
    // Job with full options
    await boss.send('critical-task', { orderId: '456' }, {
      // Retry configuration
      retryLimit: 5,
      retryDelay: 60,  // seconds between retries
      retryBackoff: true,  // exponential backoff
    
      // Timeout - fail if not completed
      expireInSeconds: 300,  // 5 minutes
    
      // Priority (higher = sooner)
      priority: 10,
    
      // Singleton - only one active job with this key
      singletonKey: 'order-456',
    
      // Dead letter queue
      deadLetter: 'failed-critical-tasks',
    });
    
    // Worker with concurrency
    await boss.work('critical-task', {
      teamSize: 5,  // concurrent workers
      teamConcurrency: 2,  // jobs per worker
    }, async (job) => {
      await processCriticalTask(job.data);
    });
    

---
  #### **Name**
Batch Processing
  #### **Description**
Fetching and processing multiple jobs at once
  #### **When**
Need to process jobs in batches for efficiency
  #### **Example**
    import PgBoss from 'pg-boss';
    
    const boss = new PgBoss(process.env.DATABASE_URL);
    await boss.start();
    
    // Batch worker - receives array of jobs
    await boss.work('bulk-import', {
      batchSize: 100,  // fetch up to 100 jobs
    }, async (jobs) => {
      // jobs is an array
      const records = jobs.map(j => j.data);
    
      // Bulk insert for efficiency
      await db.records.createMany({ data: records });
    
      // All jobs marked complete on success
    });
    
    // Queue many jobs
    const items = await fetchItemsToImport();
    await boss.insert(
      items.map(item => ({
        name: 'bulk-import',
        data: item,
      }))
    );
    

---
  #### **Name**
Supabase Integration
  #### **Description**
Using pg-boss with Supabase
  #### **When**
Building on Supabase platform
  #### **Example**
    import PgBoss from 'pg-boss';
    
    // Use Supabase connection pooler for pg-boss
    const boss = new PgBoss({
      connectionString: process.env.SUPABASE_DB_URL,
      // Use session mode for long-running workers
      // Or transaction mode with proper settings
    });
    
    await boss.start();
    
    // Worker that uses Supabase client
    await boss.work('sync-user', async (job) => {
      const { userId } = job.data;
    
      // Fetch from Supabase
      const { data: user } = await supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single();
    
      // Sync to external service
      await externalApi.syncUser(user);
    });
    
    // Queue from Supabase Edge Function
    // (or use database trigger to insert directly)
    

---
  #### **Name**
Monitoring with SQL
  #### **Description**
Querying job state directly in PostgreSQL
  #### **When**
Need visibility into queue status
  #### **Example**
    -- Active jobs by queue
    SELECT name, state, COUNT(*)
    FROM pgboss.job
    WHERE state IN ('created', 'active', 'retry')
    GROUP BY name, state
    ORDER BY name;
    
    -- Failed jobs in last 24 hours
    SELECT id, name, data, output, completedon
    FROM pgboss.job
    WHERE state = 'failed'
      AND completedon > NOW() - INTERVAL '24 hours'
    ORDER BY completedon DESC;
    
    -- Stuck jobs (active too long)
    SELECT id, name, startedon, data
    FROM pgboss.job
    WHERE state = 'active'
      AND startedon < NOW() - INTERVAL '1 hour';
    
    -- Queue depth over time (for Grafana)
    SELECT
      date_trunc('minute', createdon) as minute,
      name,
      COUNT(*) as jobs
    FROM pgboss.job
    WHERE createdon > NOW() - INTERVAL '1 hour'
    GROUP BY 1, 2
    ORDER BY 1;
    

## Anti-Patterns


---
  #### **Name**
Not Setting Expiration
  #### **Description**
Jobs without expireInSeconds
  #### **Why**
    Jobs that never expire can get stuck forever if a worker crashes
    mid-processing. They block the queue and cause confusion.
    
  #### **Instead**
    Always set expireInSeconds appropriate for your job type.
    Timed out jobs go to retry or failed state.
    

---
  #### **Name**
Huge Job Data
  #### **Description**
Storing large payloads in job data
  #### **Why**
    Job data is stored in PostgreSQL. Large payloads bloat the jobs table,
    slow queries, and increase backup sizes.
    
  #### **Instead**
    Store references (IDs, URLs) in job data. Fetch actual data in worker.
    

---
  #### **Name**
Not Archiving
  #### **Description**
Letting completed jobs accumulate indefinitely
  #### **Why**
    The jobs table grows forever. Queries slow down. Disk usage increases.
    Indexes become inefficient.
    
  #### **Instead**
    Configure archiveCompletedAfterSeconds and deleteAfterSeconds.
    Keep the active jobs table lean.
    

---
  #### **Name**
Ignoring Connection Pooling
  #### **Description**
Not considering database connections
  #### **Why**
    Each worker needs database connections. Too many workers exhaust
    the connection pool. Supabase has connection limits.
    
  #### **Instead**
    Size teamSize based on available connections. Use PgBouncer or
    Supabase connection pooler. Monitor connection usage.
    

---
  #### **Name**
No Dead Letter Queue
  #### **Description**
Failed jobs just disappear after retries
  #### **Why**
    Without a dead letter queue, you lose visibility into persistent
    failures. Can't investigate or replay failed jobs.
    
  #### **Instead**
    Configure deadLetter option. Monitor and process DLQ regularly.
    