# Trigger.dev Integration

## Patterns


---
  #### **Name**
Basic Task Setup
  #### **Description**
Setting up Trigger.dev in a Next.js project
  #### **When**
Starting with Trigger.dev in any project
  #### **Example**
    // trigger.config.ts
    import { defineConfig } from '@trigger.dev/sdk/v3';
    
    export default defineConfig({
      project: 'my-project',
      runtime: 'node',
      logLevel: 'log',
      retries: {
        enabledInDev: true,
        default: {
          maxAttempts: 3,
          minTimeoutInMs: 1000,
          maxTimeoutInMs: 10000,
          factor: 2,
        },
      },
    });
    
    // src/trigger/tasks.ts
    import { task, logger } from '@trigger.dev/sdk/v3';
    
    export const helloWorld = task({
      id: 'hello-world',
      run: async (payload: { name: string }) => {
        logger.log('Processing hello world', { payload });
    
        // Simulate work
        await new Promise(resolve => setTimeout(resolve, 1000));
    
        return { message: `Hello, ${payload.name}!` };
      },
    });
    
    // Triggering from your app
    import { helloWorld } from '@/trigger/tasks';
    
    // Fire and forget
    await helloWorld.trigger({ name: 'World' });
    
    // Wait for result
    const handle = await helloWorld.trigger({ name: 'World' });
    const result = await handle.wait();
    

---
  #### **Name**
AI Task with OpenAI Integration
  #### **Description**
Using built-in OpenAI integration with automatic retries
  #### **When**
Building AI-powered background tasks
  #### **Example**
    import { task, logger } from '@trigger.dev/sdk/v3';
    import { openai } from '@trigger.dev/openai';
    
    // Configure OpenAI with Trigger.dev
    const openaiClient = openai.configure({
      id: 'openai',
      apiKey: process.env.OPENAI_API_KEY,
    });
    
    export const generateContent = task({
      id: 'generate-content',
      retry: {
        maxAttempts: 3,
      },
      run: async (payload: { topic: string; style: string }) => {
        logger.log('Generating content', { topic: payload.topic });
    
        // Uses Trigger.dev's OpenAI integration - handles retries automatically
        const completion = await openaiClient.chat.completions.create({
          model: 'gpt-4-turbo-preview',
          messages: [
            {
              role: 'system',
              content: `You are a ${payload.style} writer.`,
            },
            {
              role: 'user',
              content: `Write about: ${payload.topic}`,
            },
          ],
        });
    
        const content = completion.choices[0].message.content;
        logger.log('Generated content', { length: content?.length });
    
        return { content, tokens: completion.usage?.total_tokens };
      },
    });
    

---
  #### **Name**
Scheduled Task with Cron
  #### **Description**
Tasks that run on a schedule
  #### **When**
Periodic jobs like reports, cleanup, or syncs
  #### **Example**
    import { schedules, task, logger } from '@trigger.dev/sdk/v3';
    
    export const dailyCleanup = schedules.task({
      id: 'daily-cleanup',
      cron: '0 2 * * *',  // 2 AM daily
      run: async () => {
        logger.log('Starting daily cleanup');
    
        // Clean up old records
        const deleted = await db.logs.deleteMany({
          where: {
            createdAt: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) },
          },
        });
    
        logger.log('Cleanup complete', { deletedCount: deleted.count });
    
        return { deleted: deleted.count };
      },
    });
    
    // Weekly report
    export const weeklyReport = schedules.task({
      id: 'weekly-report',
      cron: '0 9 * * 1',  // Monday 9 AM
      run: async () => {
        const stats = await generateWeeklyStats();
        await sendReportEmail(stats);
        return stats;
      },
    });
    

---
  #### **Name**
Batch Processing
  #### **Description**
Processing large datasets in batches
  #### **When**
Need to process many items with rate limiting
  #### **Example**
    import { task, logger, wait } from '@trigger.dev/sdk/v3';
    
    export const processBatch = task({
      id: 'process-batch',
      queue: {
        concurrencyLimit: 5,  // Only 5 running at once
      },
      run: async (payload: { items: string[] }) => {
        const results = [];
    
        for (const item of payload.items) {
          logger.log('Processing item', { item });
    
          const result = await processItem(item);
          results.push(result);
    
          // Respect rate limits
          await wait.for({ seconds: 1 });
        }
    
        return { processed: results.length, results };
      },
    });
    
    // Trigger batch processing
    export const startBatchJob = task({
      id: 'start-batch',
      run: async (payload: { datasetId: string }) => {
        const items = await fetchDataset(payload.datasetId);
    
        // Split into chunks of 100
        const chunks = chunkArray(items, 100);
    
        // Trigger parallel batch tasks
        const handles = await Promise.all(
          chunks.map(chunk => processBatch.trigger({ items: chunk }))
        );
    
        logger.log('Started batch processing', {
          totalItems: items.length,
          batches: chunks.length,
        });
    
        return { batches: handles.length };
      },
    });
    

---
  #### **Name**
Webhook Handler
  #### **Description**
Processing webhooks reliably with deduplication
  #### **When**
Handling webhooks from Stripe, GitHub, etc.
  #### **Example**
    import { task, logger, idempotencyKeys } from '@trigger.dev/sdk/v3';
    
    export const handleStripeEvent = task({
      id: 'handle-stripe-event',
      run: async (payload: {
        eventId: string;
        type: string;
        data: any;
      }) => {
        // Idempotency based on Stripe event ID
        const idempotencyKey = await idempotencyKeys.create(payload.eventId);
    
        if (idempotencyKey.isNew === false) {
          logger.log('Duplicate event, skipping', { eventId: payload.eventId });
          return { skipped: true };
        }
    
        logger.log('Processing Stripe event', {
          type: payload.type,
          eventId: payload.eventId,
        });
    
        switch (payload.type) {
          case 'checkout.session.completed':
            await handleCheckoutComplete(payload.data);
            break;
          case 'customer.subscription.updated':
            await handleSubscriptionUpdate(payload.data);
            break;
        }
    
        return { processed: true, type: payload.type };
      },
    });
    

## Anti-Patterns


---
  #### **Name**
Giant Monolithic Tasks
  #### **Description**
Putting too much logic in a single task
  #### **Why**
    Large tasks are hard to retry partially. If step 8 of 10 fails, you
    restart from step 1. Break tasks into composable pieces.
    
  #### **Instead**
    Create focused tasks that do one thing. Chain them together.
    Use subtasks for complex workflows.
    

---
  #### **Name**
Ignoring Built-in Integrations
  #### **Description**
Using raw SDKs instead of Trigger.dev integrations
  #### **Why**
    Raw SDKs don't get automatic retries, rate limit handling, or proper
    logging. Trigger.dev integrations handle all of this for you.
    
  #### **Instead**
    Use @trigger.dev/openai, @trigger.dev/resend, etc. They wrap the
    official SDKs with reliability features built in.
    

---
  #### **Name**
No Logging
  #### **Description**
Tasks without logger.log calls
  #### **Why**
    When tasks fail in production, you need to know what happened.
    Silent tasks are impossible to debug. The dashboard shows logs.
    
  #### **Instead**
    Log at the start, at key decision points, and at completion.
    Include relevant context in log payloads.
    

---
  #### **Name**
Unbounded Concurrency
  #### **Description**
Not setting queue concurrency limits
  #### **Why**
    A sudden burst of triggers can overwhelm databases and APIs.
    Trigger.dev scales fast - your dependencies might not.
    
  #### **Instead**
    Set concurrencyLimit based on what downstream services can handle.
    Start with 5-10 and increase based on monitoring.
    

---
  #### **Name**
Skipping Local Dev
  #### **Description**
Only testing in production/staging
  #### **Why**
    The Trigger.dev CLI provides local dev that matches production.
    Finding bugs locally is much faster than debugging in production.
    
  #### **Instead**
    Use `npx trigger.dev@latest dev` for local development.
    Test retry behavior and edge cases locally.
    