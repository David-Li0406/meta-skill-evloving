# Trigger Dev - Sharp Edges

## Task Timeout Silent

### **Id**
task-timeout-silent
### **Summary**
Task timeout kills execution without clear error
### **Severity**
critical
### **Situation**
  Long-running AI task or batch process suddenly stops. No error in logs.
  Task shows as failed in dashboard but no stack trace. Data partially processed.
  
### **Why**
  Trigger.dev has execution timeouts (defaults vary by plan). When exceeded, the
  task is killed mid-execution. If you're not logging progress, you won't know
  where it stopped. This is especially common with AI tasks that can take minutes.
  
### **Solution**
  # Configure explicit timeouts:
  ```typescript
  export const processDocument = task({
    id: 'process-document',
    machine: {
      preset: 'large-2x',  // More resources = longer allowed time
    },
    run: async (payload) => {
      logger.log('Starting document processing', { docId: payload.id });
  
      // Log progress at each step
      logger.log('Step 1: Extracting text');
      const text = await extractText(payload.fileUrl);
  
      logger.log('Step 2: Generating embeddings', { textLength: text.length });
      const embeddings = await generateEmbeddings(text);
  
      logger.log('Step 3: Storing vectors', { count: embeddings.length });
      await storeVectors(embeddings);
  
      logger.log('Completed successfully');
      return { processed: true };
    },
  });
  ```
  
  # For very long tasks, break into subtasks:
  - Use triggerAndWait for sequential steps
  - Each subtask has its own timeout
  - Progress is visible in dashboard
  
### **Symptoms**
  - Task fails with no error message
  - Partial data processing
  - Works locally, fails in production
  - "Task timed out" in dashboard
### **Detection Pattern**

### **Version Range**
>=3.0.0

## Payload Serialization Failure

### **Id**
payload-serialization-failure
### **Summary**
Non-serializable payload causes silent task failure
### **Severity**
critical
### **Situation**
  Passing Date objects, class instances, or circular references in payload.
  Task queued but never runs. Or runs with undefined/null values.
  
### **Why**
  Trigger.dev serializes payloads to JSON. Dates become strings, class instances
  lose methods, functions disappear, circular refs throw. Your task sees different
  data than you sent.
  
### **Solution**
  # Always use plain objects:
  ```typescript
  // WRONG - Date becomes string
  await myTask.trigger({ createdAt: new Date() });
  
  // RIGHT - ISO string
  await myTask.trigger({ createdAt: new Date().toISOString() });
  
  // WRONG - Class instance
  await myTask.trigger({ user: new User(data) });
  
  // RIGHT - Plain object
  await myTask.trigger({ user: { id: data.id, email: data.email } });
  
  // WRONG - Circular reference
  const obj = { parent: null };
  obj.parent = obj;
  await myTask.trigger(obj);  // Throws!
  ```
  
  # In task, reconstitute as needed:
  ```typescript
  run: async (payload: { createdAt: string }) => {
    const date = new Date(payload.createdAt);
    // ...
  }
  ```
  
### **Symptoms**
  - Payload values are undefined in task
  - Date objects become strings
  - Class methods not available
  - "Converting circular structure to JSON"
### **Detection Pattern**
trigger\(.*new Date\(|trigger\(.*new [A-Z][a-zA-Z]+\(
### **Version Range**
>=3.0.0

## Env Var Missing Production

### **Id**
env-var-missing-production
### **Summary**
Environment variables not synced to Trigger.dev cloud
### **Severity**
critical
### **Situation**
  Task works locally but fails in production. Env var that exists in Vercel
  is undefined in Trigger.dev. API calls fail, database connections fail.
  
### **Why**
  Trigger.dev runs tasks in its own cloud, separate from your Vercel/Railway
  deployment. Environment variables must be configured in BOTH places. They
  don't automatically sync.
  
### **Solution**
  # Sync env vars to Trigger.dev:
  1. Go to Trigger.dev dashboard
  2. Project Settings > Environment Variables
  3. Add ALL required env vars
  
  # Or use CLI:
  ```bash
  # Create .env.trigger file
  DATABASE_URL=postgres://...
  OPENAI_API_KEY=sk-...
  STRIPE_SECRET_KEY=sk_live_...
  
  # Push to Trigger.dev
  npx trigger.dev@latest env push
  ```
  
  # Common missing vars:
  - DATABASE_URL
  - OPENAI_API_KEY / ANTHROPIC_API_KEY
  - STRIPE_SECRET_KEY
  - Service API keys
  - Internal service URLs
  
  # Test in staging:
  Trigger.dev has separate envs - configure staging too
  
### **Symptoms**
  - "Environment variable not found"
  - API calls return 401 in production tasks
  - Works in dev, fails in production
  - Database connection errors in tasks
### **Detection Pattern**

### **Version Range**
>=3.0.0

## Sdk Version Mismatch

### **Id**
sdk-version-mismatch
### **Summary**
SDK version mismatch between CLI and package
### **Severity**
high
### **Situation**
  Updated @trigger.dev/sdk but forgot to update CLI. Or vice versa.
  Tasks fail to register. Weird type errors. Dev server crashes.
  
### **Why**
  The Trigger.dev SDK and CLI must be on compatible versions. Breaking changes
  between versions cause registration failures. The CLI generates types that
  must match the SDK.
  
### **Solution**
  # Always update together:
  ```bash
  # Update both SDK and CLI
  npm install @trigger.dev/sdk@latest
  npx trigger.dev@latest dev
  
  # Or pin to same version
  npm install @trigger.dev/sdk@3.3.0
  npx trigger.dev@3.3.0 dev
  ```
  
  # Check versions:
  ```bash
  npx trigger.dev@latest --version
  npm list @trigger.dev/sdk
  ```
  
  # In CI/CD:
  ```yaml
  - run: npm install @trigger.dev/sdk@${{ env.TRIGGER_VERSION }}
  - run: npx trigger.dev@${{ env.TRIGGER_VERSION }} deploy
  ```
  
### **Symptoms**
  - Tasks not appearing in dashboard
  - Type errors in trigger.config.ts
  - "Failed to register task"
  - Dev server crashes on start
### **Detection Pattern**

### **Version Range**
>=3.0.0

## Retry Not Idempotent

### **Id**
retry-not-idempotent
### **Summary**
Task retries cause duplicate side effects
### **Severity**
high
### **Situation**
  Task sends email, then fails on next step. Retry sends email again.
  Customer gets 3 identical emails. Or 3 Stripe charges. Or 3 Slack messages.
  
### **Why**
  Trigger.dev retries failed tasks from the beginning. If your task has side
  effects before the failure point, those execute again. Without idempotency,
  you create duplicates.
  
### **Solution**
  # Use idempotency keys:
  ```typescript
  import { task, idempotencyKeys } from '@trigger.dev/sdk/v3';
  
  export const sendOrderEmail = task({
    id: 'send-order-email',
    run: async (payload: { orderId: string }) => {
      // Check if already sent
      const key = await idempotencyKeys.create(`email-${payload.orderId}`);
  
      if (!key.isNew) {
        logger.log('Email already sent, skipping');
        return { skipped: true };
      }
  
      await sendEmail(payload.orderId);
      return { sent: true };
    },
  });
  ```
  
  # Alternative: Track in database
  ```typescript
  const existing = await db.emailLogs.findUnique({
    where: { orderId_type: { orderId, type: 'order_confirmation' } }
  });
  
  if (existing) {
    logger.log('Already sent');
    return;
  }
  
  await sendEmail(orderId);
  await db.emailLogs.create({ data: { orderId, type: 'order_confirmation' } });
  ```
  
### **Symptoms**
  - Duplicate emails on retry
  - Multiple charges for same order
  - Duplicate webhook deliveries
  - Data inserted multiple times
### **Detection Pattern**

### **Version Range**
>=3.0.0

## Concurrency Overwhelming Apis

### **Id**
concurrency-overwhelming-apis
### **Summary**
High concurrency overwhelms downstream services
### **Severity**
high
### **Situation**
  Burst of 1000 tasks triggered. All hit OpenAI API simultaneously.
  Rate limited. All fail. Retry. Rate limited again. Vicious cycle.
  
### **Why**
  Trigger.dev scales to handle many concurrent tasks. But your downstream
  APIs (OpenAI, databases, external services) have rate limits. Without
  concurrency control, you overwhelm them.
  
### **Solution**
  # Set queue concurrency limits:
  ```typescript
  export const callOpenAI = task({
    id: 'call-openai',
    queue: {
      concurrencyLimit: 10,  // Only 10 running at once
    },
    run: async (payload) => {
      // Protected by concurrency limit
      return await openai.chat.completions.create(payload);
    },
  });
  ```
  
  # For rate-limited APIs:
  ```typescript
  export const callRateLimitedAPI = task({
    id: 'call-api',
    queue: {
      concurrencyLimit: 5,
    },
    retry: {
      maxAttempts: 5,
      minTimeoutInMs: 5000,  // Wait before retry
      factor: 2,  // Exponential backoff
    },
    run: async (payload) => {
      // Add delay between calls
      await wait.for({ milliseconds: 200 });
      return await externalAPI.call(payload);
    },
  });
  ```
  
  # Start conservative:
  - 5-10 for external APIs
  - 20-50 for databases
  - Increase based on monitoring
  
### **Symptoms**
  - Rate limit errors (429)
  - Database connection pool exhausted
  - API returns "too many requests"
  - Mass task failures
### **Detection Pattern**
queue:\s*\{[^}]*concurrencyLimit:\s*[5-9][0-9]|[1-9][0-9]{2,}
### **Version Range**
>=3.0.0

## Trigger Config Not Found

### **Id**
trigger-config-not-found
### **Summary**
trigger.config.ts not at project root
### **Severity**
high
### **Situation**
  Running npx trigger.dev dev but CLI can't find config.
  Or config exists but in wrong location (monorepo issue).
  
### **Why**
  The CLI looks for trigger.config.ts at the current working directory.
  In monorepos, you must run from the package directory, not the root.
  Wrong location = tasks not discovered.
  
### **Solution**
  # Config must be at package root:
  ```
  my-app/
  ├── trigger.config.ts  <- Here
  ├── package.json
  ├── src/
  │   └── trigger/
  │       └── tasks.ts
  ```
  
  # In monorepos:
  ```
  monorepo/
  ├── apps/
  │   └── web/
  │       ├── trigger.config.ts  <- Here, not at monorepo root
  │       ├── package.json
  │       └── src/trigger/
  
  # Run from package directory
  cd apps/web && npx trigger.dev dev
  ```
  
  # Specify config location:
  ```bash
  npx trigger.dev dev --config ./apps/web/trigger.config.ts
  ```
  
### **Symptoms**
  - "Could not find trigger.config.ts"
  - Tasks not discovered
  - Empty task list in dashboard
  - Works for one package, not another
### **Detection Pattern**

### **Version Range**
>=3.0.0

## Wait For Memory Leak

### **Id**
wait-for-memory-leak
### **Summary**
wait.for in loops causes memory issues
### **Severity**
medium
### **Situation**
  Processing thousands of items with wait.for between each.
  Task memory grows. Eventually killed for memory.
  
### **Why**
  Each wait.for creates checkpoint state. In a loop with thousands of
  iterations, this accumulates. The task's state blob grows until it
  hits memory limits.
  
### **Solution**
  # Batch instead of individual waits:
  ```typescript
  // WRONG - Wait per item
  for (const item of items) {
    await processItem(item);
    await wait.for({ milliseconds: 100 });  // 1000 waits = bloated state
  }
  
  // RIGHT - Batch processing
  const chunks = chunkArray(items, 50);
  for (const chunk of chunks) {
    await Promise.all(chunk.map(processItem));
    await wait.for({ milliseconds: 500 });  // Only 20 waits
  }
  ```
  
  # For very large datasets, use subtasks:
  ```typescript
  export const processAll = task({
    id: 'process-all',
    run: async (payload: { items: string[] }) => {
      const chunks = chunkArray(payload.items, 100);
  
      // Each chunk is a separate task
      await Promise.all(
        chunks.map(chunk =>
          processChunk.triggerAndWait({ items: chunk })
        )
      );
    },
  });
  ```
  
### **Symptoms**
  - Task killed for memory
  - Slow task execution
  - State blob too large error
  - Works for small batches, fails for large
### **Detection Pattern**
for.*\{[\s\S]*wait\.for|while.*\{[\s\S]*wait\.for
### **Version Range**
>=3.0.0

## Integration Not Configured

### **Id**
integration-not-configured
### **Summary**
Using raw SDK instead of Trigger.dev integrations
### **Severity**
medium
### **Situation**
  Using OpenAI SDK directly. API call fails. No automatic retry.
  Rate limits not handled. Have to implement all resilience manually.
  
### **Why**
  Trigger.dev integrations wrap SDKs with automatic retries, rate limit
  handling, and proper logging. Using raw SDKs means you lose these
  features and have to implement them yourself.
  
### **Solution**
  # Use integrations when available:
  ```typescript
  // WRONG - Raw SDK
  import OpenAI from 'openai';
  const openai = new OpenAI();
  
  // RIGHT - Trigger.dev integration
  import { openai } from '@trigger.dev/openai';
  
  const openaiClient = openai.configure({
    id: 'openai',
    apiKey: process.env.OPENAI_API_KEY,
  });
  
  // Now has automatic retries and rate limiting
  export const generateContent = task({
    id: 'generate-content',
    run: async (payload) => {
      const response = await openaiClient.chat.completions.create({
        model: 'gpt-4-turbo-preview',
        messages: [{ role: 'user', content: payload.prompt }],
      });
      return response;
    },
  });
  ```
  
  # Available integrations:
  - @trigger.dev/openai
  - @trigger.dev/anthropic
  - @trigger.dev/resend
  - @trigger.dev/slack
  - @trigger.dev/stripe
  
### **Symptoms**
  - Manual retry logic in tasks
  - Rate limit errors not handled
  - No automatic logging of API calls
  - Inconsistent error handling
### **Detection Pattern**
import.*from\s*['"]openai['"]|import.*from\s*['"]@anthropic
### **Version Range**
>=3.0.0

## Local Dev Not Running

### **Id**
local-dev-not-running
### **Summary**
Triggering tasks without dev server running
### **Severity**
medium
### **Situation**
  Called task.trigger() but nothing happens. No errors either.
  Task just disappears into void. Dev server wasn't running.
  
### **Why**
  In development, tasks run through the local dev server (npx trigger.dev dev).
  If it's not running, triggers queue up or fail silently depending on
  configuration. Production works differently.
  
### **Solution**
  # Always run dev server during development:
  ```bash
  # Terminal 1: Your app
  npm run dev
  
  # Terminal 2: Trigger.dev dev server
  npx trigger.dev dev
  ```
  
  # Check dev server is connected:
  - Should show "Connected to Trigger.dev"
  - Tasks should appear in console
  - Dashboard shows task registrations
  
  # In package.json:
  ```json
  {
    "scripts": {
      "dev": "next dev",
      "trigger:dev": "trigger.dev dev",
      "dev:all": "concurrently \"npm run dev\" \"npm run trigger:dev\""
    }
  }
  ```
  
### **Symptoms**
  - Triggers don't run
  - No task in dashboard
  - No errors, just silence
  - Works in production, not dev
### **Detection Pattern**

### **Version Range**
>=3.0.0