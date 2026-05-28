# Inngest - Sharp Edges

## Step Function Timeout

### **Id**
step-function-timeout
### **Summary**
Step functions have execution time limits
### **Severity**
critical
### **Situation**
  Long-running step takes 2+ hours. Inngest kills the function mid-execution.
  Work is lost. No partial progress saved. User sees mysterious failure.
  
### **Why**
  Inngest step functions have execution limits (varies by plan: 1hr free, 2hr Pro).
  A single step that exceeds this limit gets terminated. Unlike traditional
  serverless, the timeout applies to total execution, not individual requests.
  
### **Solution**
  # Break long work into smaller steps:
  ```typescript
  // WRONG - single long step
  await step.run('process-all', async () => {
    for (const item of items) {  // 10,000 items = hours
      await processItem(item);
    }
  });
  
  // RIGHT - batch into steps
  const BATCH_SIZE = 100;
  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    await step.run(`process-batch-${i}`, async () => {
      for (const item of batch) {
        await processItem(item);
      }
    });
  }
  ```
  
  # For truly long work:
  - Fan out to child events
  - Use step.sendEvent() to spawn parallel workers
  - Each worker handles a chunk
  
### **Symptoms**
  - Function terminated without error
  - "Exceeded maximum duration" in logs
  - Partial work completed, rest lost
  - Works locally, fails in production
### **Detection Pattern**
step\.run\([^)]+for\s*\(
### **Version Range**
>=1.0.0

## Event Payload Size Limit

### **Id**
event-payload-size-limit
### **Summary**
Event payloads have a 512KB limit
### **Severity**
high
### **Situation**
  Sending large document content in event payload. Event rejected.
  Or worse: payload accepted but causes slow processing and memory issues.
  
### **Why**
  Inngest stores events and replays them for retries. Large payloads consume
  storage, slow down the dashboard, and hit the 512KB limit. Events should
  describe what happened, not carry data.
  
### **Solution**
  # Store data externally, pass references:
  ```typescript
  // WRONG - data in payload
  await inngest.send({
    name: 'document/uploaded',
    data: {
      content: largeDocumentString,  // 2MB of text
      metadata: { ... }
    }
  });
  
  // RIGHT - reference in payload
  await inngest.send({
    name: 'document/uploaded',
    data: {
      documentId: doc.id,  // Just the ID
      storageUrl: doc.url, // Where to fetch it
    }
  });
  
  // In function, fetch when needed:
  const document = await step.run('fetch-document', async () => {
    return await storage.get(event.data.documentId);
  });
  ```
  
  # Use step.run() to fetch large data:
  - Data fetched in step is not stored in event
  - Only the step result is checkpointed
  - Keep step results small too
  
### **Symptoms**
  - "Payload too large" error
  - Slow event ingestion
  - Dashboard loads slowly
  - Memory pressure on workers
### **Detection Pattern**
inngest\.send\([^)]+content:|inngest\.send\([^)]+body:
### **Version Range**
>=1.0.0

## Retry Not Idempotent

### **Id**
retry-not-idempotent
### **Summary**
Step operations not safe for retry
### **Severity**
critical
### **Situation**
  Step sends email. Function fails later. Retry runs. Email sent again.
  User gets duplicate emails. Or worse: duplicate charges.
  
### **Why**
  Inngest retries the entire function from the last checkpoint. If a step
  succeeded but wasn't checkpointed (crash right after), it runs again.
  Any side effects happen twice unless you handle idempotency.
  
### **Solution**
  # Use Inngest's built-in idempotency:
  ```typescript
  export const processPayment = inngest.createFunction(
    {
      id: 'process-payment',
      // Deduplicate by order ID
      idempotency: 'event.data.orderId',
    },
    { event: 'order/created' },
    async ({ event, step }) => { ... }
  );
  ```
  
  # For step-level idempotency:
  ```typescript
  await step.run('charge-card', async () => {
    // Use Stripe's idempotency
    return await stripe.charges.create(
      { amount: 1000 },
      { idempotencyKey: `order_${event.data.orderId}` }
    );
  });
  ```
  
  # For emails/notifications:
  ```typescript
  await step.run('send-email', async () => {
    // Check if already sent
    const sent = await db.emailLog.findFirst({
      where: { orderId: event.data.orderId, type: 'confirmation' }
    });
    if (sent) return { skipped: true };
  
    await resend.emails.send({ ... });
    await db.emailLog.create({ orderId: event.data.orderId, type: 'confirmation' });
  });
  ```
  
### **Symptoms**
  - Duplicate emails sent
  - Duplicate charges created
  - Duplicate database records
  - Side effects happen multiple times
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Step Result Too Large

### **Id**
step-result-too-large
### **Summary**
Step results are stored and have size limits
### **Severity**
high
### **Situation**
  Step fetches 50MB of data and returns it. Function slows to a crawl.
  Eventually hits memory limits or storage quotas.
  
### **Why**
  Every step result is durably stored for resume capability. Large results
  consume storage, slow serialization, and can exceed limits. Step results
  should be minimal - IDs, status, small summaries.
  
### **Solution**
  # Return minimal data from steps:
  ```typescript
  // WRONG - returning large data
  const data = await step.run('fetch-data', async () => {
    return await db.records.findMany();  // 100K records
  });
  
  // RIGHT - return IDs, fetch later
  const recordIds = await step.run('get-record-ids', async () => {
    const records = await db.records.findMany({ select: { id: true } });
    return records.map(r => r.id);
  });
  
  // Process in batches with small results
  for (const batchIds of chunk(recordIds, 100)) {
    await step.run(`process-${batchIds[0]}`, async () => {
      const records = await db.records.findMany({
        where: { id: { in: batchIds } }
      });
      // Process and return status only
      return { processed: batchIds.length };
    });
  }
  ```
  
  # Use external storage for large intermediate data:
  - Store in S3/database
  - Pass reference between steps
  
### **Symptoms**
  - Function runs slowly
  - High memory usage
  - "Step output too large" error
  - Dashboard shows large step data
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Cold Start On Vercel

### **Id**
cold-start-on-vercel
### **Summary**
Vercel function cold starts can delay Inngest execution
### **Severity**
medium
### **Situation**
  Inngest function on Vercel has 2-5 second cold start. User expects
  near-instant processing. Perceived as slow or broken.
  
### **Why**
  Inngest invokes your function via HTTP. If your Vercel function is cold,
  the first step has cold start latency. For time-sensitive operations,
  this matters. Heavy dependencies make it worse.
  
### **Solution**
  # Reduce cold start time:
  ```typescript
  // 1. Use edge runtime if possible
  export const runtime = 'edge';
  
  // 2. Minimize dependencies
  // Don't import heavy libs at top level
  // Use dynamic imports inside steps
  
  // 3. Keep function bundles small
  // Check with: npx @next/bundle-analyzer
  
  // 4. Warm functions with cron
  export const warmUp = inngest.createFunction(
    { id: 'warm-up' },
    { cron: '*/5 * * * *' },  // Every 5 minutes
    async ({ step }) => {
      // Just return - keeps function warm
      return { status: 'warm' };
    }
  );
  ```
  
  # Accept cold starts for background work:
  - Background jobs don't need instant response
  - 2-second delay on a 10-minute job is fine
  - Only optimize if user-facing latency matters
  
### **Symptoms**
  - First execution slow, subsequent fast
  - Function took 3 seconds to start
  - Timeout on functions that should be quick
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Missing Serve Handler

### **Id**
missing-serve-handler
### **Summary**
Forgot to export the serve handler or register functions
### **Severity**
critical
### **Situation**
  Functions defined but never execute. Events sent, nothing happens.
  Dashboard shows events but no function runs.
  
### **Why**
  Inngest functions must be registered with serve() and exported as HTTP
  handlers. Missing the serve export means Inngest can't invoke your
  functions. Missing function registration means it won't run.
  
### **Solution**
  # Complete setup for Next.js App Router:
  ```typescript
  // lib/inngest/client.ts
  import { Inngest } from 'inngest';
  export const inngest = new Inngest({ id: 'my-app' });
  
  // lib/inngest/functions.ts
  import { inngest } from './client';
  export const myFunction = inngest.createFunction(...);
  
  // app/api/inngest/route.ts - THE CRITICAL FILE
  import { serve } from 'inngest/next';
  import { inngest } from '@/lib/inngest/client';
  import { myFunction } from '@/lib/inngest/functions';
  
  export const { GET, POST, PUT } = serve({
    client: inngest,
    functions: [myFunction],  // Must list ALL functions!
  });
  ```
  
  # Common mistakes:
  - Forgot to create app/api/inngest/route.ts
  - Created file but didn't export GET, POST, PUT
  - Exported but forgot to include function in array
  - Function in array but wrong import path
  
### **Symptoms**
  - Events sent but no function executes
  - "Function not found" in Inngest dashboard
  - Dev server shows no Inngest routes
  - inngest dev shows 0 functions
### **Detection Pattern**
export const \{ GET, POST, PUT \} = serve
### **Version Range**
>=1.0.0

## Dev Server Not Running

### **Id**
dev-server-not-running
### **Summary**
Inngest dev server not running during local development
### **Severity**
medium
### **Situation**
  Sending events in local dev. Nothing happens. Check logs - nothing.
  Events go to production Inngest cloud instead of local.
  
### **Why**
  Inngest needs its dev server (inngest dev) running locally to receive
  events. Without it, events either fail or go to cloud (depending on
  config). Functions never execute locally.
  
### **Solution**
  # Always run inngest dev alongside your app:
  ```bash
  # Terminal 1: Your app
  npm run dev
  
  # Terminal 2: Inngest dev server
  npx inngest-cli@latest dev
  ```
  
  # Or use concurrently:
  ```json
  // package.json
  {
    "scripts": {
      "dev": "concurrently \"next dev\" \"inngest-cli dev\""
    }
  }
  ```
  
  # Inngest dev dashboard:
  - Open http://localhost:8288
  - See registered functions
  - View event history
  - Replay events for debugging
  
### **Symptoms**
  - Events sent, nothing happens locally
  - No function logs in terminal
  - Works in production but not locally
  - "Connection refused" errors
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Step Sleep In Loop

### **Id**
step-sleep-in-loop
### **Summary**
Using step.sleep() inside a loop creates many sleep operations
### **Severity**
medium
### **Situation**
  Processing 1000 items with sleep between each. Function creates 1000
  sleep checkpoints. Slow, expensive, and hits limits.
  
### **Why**
  Each step.sleep() is a separate checkpoint stored by Inngest. In a loop,
  this creates N checkpoints. High checkpoint count slows the function
  and can hit plan limits.
  
### **Solution**
  # Batch operations, sleep once per batch:
  ```typescript
  // WRONG - sleep per item
  for (const item of items) {
    await step.run(`process-${item.id}`, () => processItem(item));
    await step.sleep(`wait-${item.id}`, '1s');  // 1000 sleeps!
  }
  
  // RIGHT - batch with single sleep
  const BATCH_SIZE = 50;
  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
  
    await step.run(`batch-${i}`, async () => {
      for (const item of batch) {
        await processItem(item);
        await delay(100);  // In-step delay, not checkpoint
      }
    });
  
    // Only sleep between batches if needed
    if (i + BATCH_SIZE < items.length) {
      await step.sleep(`batch-wait-${i}`, '5s');
    }
  }
  ```
  
  # Use fan-out for parallel processing:
  ```typescript
  await step.sendEvent(
    'spawn-workers',
    items.map(item => ({
      name: 'item/process',
      data: { itemId: item.id }
    }))
  );
  ```
  
### **Symptoms**
  - Function has thousands of steps
  - Slow function execution
  - High step count in dashboard
  - Hitting plan limits
### **Detection Pattern**
for.*step\.sleep|while.*step\.sleep
### **Version Range**
>=1.0.0

## Waitforevent Timeout Infinite

### **Id**
waitForEvent-timeout-infinite
### **Summary**
step.waitForEvent without timeout waits forever
### **Severity**
high
### **Situation**
  Waiting for user action with waitForEvent. User never acts. Function
  waits forever. Resources tied up. No visibility into stalled functions.
  
### **Why**
  step.waitForEvent waits until matching event arrives or timeout.
  Without timeout, it waits indefinitely. These zombie functions consume
  resources and are hard to find.
  
### **Solution**
  # Always set a timeout:
  ```typescript
  // WRONG - waits forever
  const response = await step.waitForEvent('user-response', {
    event: 'user/responded',
    match: 'data.userId',
  });
  
  // RIGHT - timeout with handling
  const response = await step.waitForEvent('user-response', {
    event: 'user/responded',
    match: 'data.userId',
    timeout: '24h',  // Maximum wait time
  });
  
  if (!response) {
    // Handle timeout case
    await step.run('send-reminder', () => sendReminder(userId));
    // Or cancel the workflow
    return { status: 'timed_out' };
  }
  ```
  
  # Common timeout patterns:
  - User action: 24h-7d
  - Payment confirmation: 1h
  - External webhook: 15m-1h
  - Always handle null (timeout) case
  
### **Symptoms**
  - Functions stuck in "waiting" state
  - Resource usage grows over time
  - Dashboard shows old running functions
  - No way to know what's stalled
### **Detection Pattern**
waitForEvent\([^)]+\)(?!.*timeout)
### **Version Range**
>=1.0.0

## Concurrency Not Set

### **Id**
concurrency-not-set
### **Summary**
No concurrency limits allowing downstream service overload
### **Severity**
high
### **Situation**
  Burst of 10,000 events. 10,000 functions start simultaneously. Database
  connection pool exhausted. External API rate limited. Everything fails.
  
### **Why**
  Inngest scales fast - that's the point. But downstream services don't
  scale infinitely. Without concurrency limits, you can DDoS your own
  database or hit external API rate limits.
  
### **Solution**
  # Set appropriate concurrency limits:
  ```typescript
  export const processOrder = inngest.createFunction(
    {
      id: 'process-order',
      concurrency: {
        limit: 10,  // Max 10 concurrent executions
      },
    },
    { event: 'order/placed' },
    async ({ event, step }) => { ... }
  );
  ```
  
  # Per-key concurrency (per user/tenant):
  ```typescript
  {
    concurrency: {
      limit: 5,
      key: 'event.data.userId',  // 5 per user
    },
  }
  ```
  
  # Guidelines for limits:
  - Database: Match connection pool size
  - External APIs: Match rate limit
  - Email: 50-100/minute typically
  - Payments: Start at 5-10
  - Start conservative, increase with monitoring
  
### **Symptoms**
  - Database connection exhausted
  - "Too many requests" from external APIs
  - Cascading failures
  - All functions fail simultaneously
### **Detection Pattern**
createFunction\([^)]+\)(?!.*concurrency)
### **Version Range**
>=1.0.0