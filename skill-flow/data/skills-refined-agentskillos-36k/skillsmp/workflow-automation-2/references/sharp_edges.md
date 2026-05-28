# Workflow Automation - Sharp Edges

## Non-Idempotent Steps in Durable Workflows

### **Id**
step-not-idempotent
### **Severity**
critical
### **Situation**
Writing workflow steps that modify external state
### **Symptom**
  Customer charged twice. Email sent three times. Database record
  created multiple times. Workflow retries cause duplicate side effects.
  
### **Why**
  Durable execution replays workflows from the beginning on restart.
  If step 3 crashes and the workflow resumes, steps 1 and 2 run again.
  Without idempotency keys, external services don't know these are retries.
  
### **Solution**
  # ALWAYS use idempotency keys for external calls:
  
  ## Stripe example:
  await stripe.paymentIntents.create({
    amount: 1000,
    currency: 'usd',
    idempotency_key: `order-${orderId}-payment`  # Critical!
  });
  
  ## Email example:
  await step.run("send-confirmation", async () => {
    const alreadySent = await checkEmailSent(orderId);
    if (alreadySent) return { skipped: true };
    return sendEmail(customer, orderId);
  });
  
  ## Database example:
  await db.query(`
    INSERT INTO orders (id, ...) VALUES ($1, ...)
    ON CONFLICT (id) DO NOTHING
  `, [orderId]);
  
  # Generate idempotency key from stable inputs, not random values
  
### **Detection Pattern**
  - step.run
  - stripe
  - sendEmail
  - INSERT INTO

## Workflow Runs for Hours/Days Without Checkpoints

### **Id**
workflow-too-long
### **Severity**
high
### **Situation**
Long-running workflows with infrequent steps
### **Symptom**
  Memory consumption grows. Worker timeouts. Lost progress after
  crashes. "Workflow exceeded maximum duration" errors.
  
### **Why**
  Workflows hold state in memory until checkpointed. A workflow that
  runs for 24 hours with one step per hour accumulates state for 24h.
  Workers have memory limits. Functions have execution time limits.
  
### **Solution**
  # Break long workflows into checkpointed steps:
  
  ## WRONG - one long step:
  await step.run("process-all", async () => {
    for (const item of thousandItems) {
      await processItem(item);  // Hours of work, one checkpoint
    }
  });
  
  ## CORRECT - many small steps:
  for (const item of thousandItems) {
    await step.run(`process-${item.id}`, async () => {
      return processItem(item);  // Checkpoint after each
    });
  }
  
  ## For very long waits, use sleep:
  await step.sleep("wait-for-trial", "14 days");
  // Doesn't consume resources while waiting
  
  ## Consider child workflows for long processes:
  await step.invoke("process-batch", {
    function: batchProcessor,
    data: { items: batch }
  });
  
### **Detection Pattern**
  - for.*step
  - while.*await
  - setTimeout

## Activities Without Timeout Configuration

### **Id**
no-timeout-on-activities
### **Severity**
high
### **Situation**
Calling external services from workflow activities
### **Symptom**
  Workflows hang indefinitely. Worker pool exhausted. Dead workflows
  that never complete or fail. Manual intervention needed to kill stuck
  workflows.
  
### **Why**
  External APIs can hang forever. Without timeout, your workflow waits
  forever. Unlike HTTP clients, workflow activities don't have default
  timeouts in most platforms.
  
### **Solution**
  # ALWAYS set timeouts on activities:
  
  ## Temporal:
  const activities = proxyActivities<typeof activitiesType>({
    startToCloseTimeout: '30 seconds',  # Required!
    scheduleToCloseTimeout: '5 minutes',
    heartbeatTimeout: '10 seconds',  # For long activities
    retry: {
      maximumAttempts: 3,
      initialInterval: '1 second',
    }
  });
  
  ## Inngest:
  await step.run("call-api", { timeout: "30s" }, async () => {
    return fetch(url, { signal: AbortSignal.timeout(25000) });
  });
  
  ## AWS Step Functions:
  {
    "Type": "Task",
    "TimeoutSeconds": 30,
    "HeartbeatSeconds": 10,
    "Resource": "arn:aws:lambda:..."
  }
  
  # Rule: Activity timeout < Workflow timeout
  
### **Detection Pattern**
  - proxyActivities
  - step.run
  - Task.*Resource

## Side Effects Outside Step/Activity Boundaries

### **Id**
side-effects-in-workflow-code
### **Severity**
critical
### **Situation**
Writing code that runs during workflow replay
### **Symptom**
  Random failures on replay. "Workflow corrupted" errors. Different
  behavior on replay than initial run. Non-determinism errors.
  
### **Why**
  Workflow code runs on EVERY replay. If you generate a random ID in
  workflow code, you get a different ID each replay. If you read the
  current time, you get a different time. This breaks determinism.
  
### **Solution**
  # WRONG - side effects in workflow code:
  export async function orderWorkflow(order) {
    const orderId = uuid();  // Different every replay!
    const now = new Date();  // Different every replay!
    await activities.process(orderId, now);
  }
  
  # CORRECT - side effects in activities:
  export async function orderWorkflow(order) {
    const orderId = await activities.generateOrderId();  # Recorded
    const now = await activities.getCurrentTime();       # Recorded
    await activities.process(orderId, now);
  }
  
  # Also CORRECT - Temporal workflow.now() and sideEffect:
  import { sideEffect } from '@temporalio/workflow';
  
  const orderId = await sideEffect(() => uuid());
  const now = workflow.now();  # Deterministic replay-safe time
  
  # Side effects that are safe in workflow code:
  # - Reading function arguments
  # - Simple calculations (no randomness)
  # - Logging (usually)
  
### **Detection Pattern**
  - Math.random
  - Date.now
  - uuid()
  - new Date()

## Retry Configuration Without Exponential Backoff

### **Id**
retry-without-backoff
### **Severity**
medium
### **Situation**
Configuring retry behavior for failing steps
### **Symptom**
  Overwhelming failing services. Rate limiting. Cascading failures.
  Retry storms causing outages. Being blocked by external APIs.
  
### **Why**
  When a service is struggling, immediate retries make it worse.
  100 workflows retrying instantly = 100 requests hitting a service
  that's already failing. Backoff gives the service time to recover.
  
### **Solution**
  # ALWAYS use exponential backoff:
  
  ## Temporal:
  const activities = proxyActivities({
    retry: {
      initialInterval: '1 second',
      backoffCoefficient: 2,       # 1s, 2s, 4s, 8s, 16s...
      maximumInterval: '1 minute',  # Cap the backoff
      maximumAttempts: 5,
    }
  });
  
  ## Inngest (built-in backoff):
  {
    id: "my-function",
    retries: 5,  # Uses exponential backoff by default
  }
  
  ## Manual backoff:
  const backoff = (attempt) => {
    const base = 1000;
    const max = 60000;
    const delay = Math.min(base * Math.pow(2, attempt), max);
    const jitter = delay * 0.1 * Math.random();
    return delay + jitter;
  };
  
  # Add jitter to prevent thundering herd
  
### **Detection Pattern**
  - retry
  - maximumAttempts
  - initialInterval

## Storing Large Data in Workflow State

### **Id**
workflow-state-too-large
### **Severity**
high
### **Situation**
Passing large payloads between workflow steps
### **Symptom**
  Slow workflow execution. Memory errors. "Payload too large" errors.
  Expensive storage costs. Slow replays.
  
### **Why**
  Workflow state is persisted and replayed. A 10MB payload is stored,
  serialized, and deserialized on every step. This adds latency and
  cost. Some platforms have hard limits (e.g., Step Functions 256KB).
  
### **Solution**
  # WRONG - large data in workflow:
  await step.run("fetch-data", async () => {
    const largeDataset = await fetchAllRecords();  // 100MB!
    return largeDataset;  // Stored in workflow state
  });
  
  # CORRECT - store reference, not data:
  await step.run("fetch-data", async () => {
    const largeDataset = await fetchAllRecords();
    const s3Key = await uploadToS3(largeDataset);
    return { s3Key };  // Just the reference
  });
  
  const processed = await step.run("process-data", async () => {
    const data = await downloadFromS3(fetchResult.s3Key);
    return processData(data);
  });
  
  # For Step Functions, use S3 for large payloads:
  {
    "Type": "Task",
    "Resource": "arn:aws:states:::s3:putObject",
    "Parameters": {
      "Bucket": "my-bucket",
      "Key.$": "$.outputKey",
      "Body.$": "$.largeData"
    }
  }
  
### **Detection Pattern**
  - return.*data
  - step.run
  - workflow

## Missing Dead Letter Queue or Failure Handler

### **Id**
no-dead-letter-handling
### **Severity**
high
### **Situation**
Workflows that exhaust all retries
### **Symptom**
  Failed workflows silently disappear. No alerts when things break.
  Customer issues discovered days later. Manual recovery impossible.
  
### **Why**
  Even with retries, some workflows will fail permanently. Without
  dead letter handling, you don't know they failed. The customer
  waits forever, you're unaware, and there's no data to debug.
  
### **Solution**
  # Inngest onFailure handler:
  export const myFunction = inngest.createFunction(
    {
      id: "process-order",
      onFailure: async ({ error, event, step }) => {
        // Log to error tracking
        await step.run("log-error", () =>
          sentry.captureException(error, { extra: { event } })
        );
  
        // Alert team
        await step.run("alert", () =>
          slack.postMessage({
            channel: "#alerts",
            text: `Order ${event.data.orderId} failed: ${error.message}`
          })
        );
  
        // Queue for manual review
        await step.run("queue-review", () =>
          db.insert(failedOrders, { orderId, error, event })
        );
      }
    },
    { event: "order/created" },
    async ({ event, step }) => { ... }
  );
  
  # n8n Error Trigger:
  [Error Trigger]  →  [Log to DB]  →  [Slack Alert]  →  [Create Ticket]
  
  # Temporal: Use workflow.failed or workflow signals
  
### **Detection Pattern**
  - onFailure
  - Error Trigger
  - dead.?letter

## n8n Workflow Without Error Trigger

### **Id**
n8n-missing-error-workflow
### **Severity**
medium
### **Situation**
Building production n8n workflows
### **Symptom**
  Workflow fails silently. Errors only visible in execution logs.
  No alerts, no recovery, no visibility until someone notices.
  
### **Why**
  n8n doesn't notify on failure by default. Without an Error Trigger
  node connected to alerting, failures are only visible in the UI.
  Production failures go unnoticed.
  
### **Solution**
  # Every production n8n workflow needs:
  
  1. Error Trigger node
     - Catches any node failure in the workflow
     - Provides error details and context
  
  2. Connected error handling:
     [Error Trigger]
         ↓
     [Set: Extract Error Details]
         ↓
     [HTTP: Log to Error Service]
         ↓
     [Slack/Email: Alert Team]
  
  3. Consider dead letter pattern:
     [Error Trigger]
         ↓
     [Redis/Postgres: Store Failed Job]
         ↓
     [Separate Recovery Workflow]
  
  # Also use:
  - Retry on node failures (built-in)
  - Node timeout settings
  - Workflow timeout
  
### **Detection Pattern**
  - n8n
  - workflow
  - Error Trigger

## Long-Running Temporal Activities Without Heartbeat

### **Id**
temporal-missing-heartbeat
### **Severity**
medium
### **Situation**
Activities that run for more than a few seconds
### **Symptom**
  Activity timeouts even when work is progressing. Lost work when
  workers restart. Can't cancel long-running activities.
  
### **Why**
  Temporal detects stuck activities via heartbeat. Without heartbeat,
  Temporal can't tell if activity is working or stuck. Long activities
  appear hung, may timeout, and can't be gracefully cancelled.
  
### **Solution**
  # For any activity > 10 seconds, add heartbeat:
  
  import { heartbeat, activityInfo } from '@temporalio/activity';
  
  export async function processLargeFile(fileUrl: string): Promise<void> {
    const chunks = await downloadChunks(fileUrl);
  
    for (let i = 0; i < chunks.length; i++) {
      // Check for cancellation
      const { cancelled } = activityInfo();
      if (cancelled) {
        throw new CancelledFailure('Activity cancelled');
      }
  
      await processChunk(chunks[i]);
  
      // Report progress
      heartbeat({ progress: (i + 1) / chunks.length });
    }
  }
  
  # Configure heartbeat timeout:
  const activities = proxyActivities({
    startToCloseTimeout: '10 minutes',
    heartbeatTimeout: '30 seconds',  # Must heartbeat every 30s
  });
  
  # If no heartbeat for 30s, activity is considered stuck
  
### **Detection Pattern**
  - startToCloseTimeout
  - proxyActivities
  - for.*await