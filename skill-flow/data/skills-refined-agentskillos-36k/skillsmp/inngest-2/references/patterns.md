# Inngest Integration

## Patterns


---
  #### **Name**
Basic Function Setup
  #### **Description**
Inngest function with typed events in Next.js
  #### **When**
Starting with Inngest in any Next.js project
  #### **Example**
    // lib/inngest/client.ts
    import { Inngest } from 'inngest';
    
    export const inngest = new Inngest({
      id: 'my-app',
      schemas: new EventSchemas().fromRecord<Events>(),
    });
    
    // Define your events with types
    type Events = {
      'user/signed.up': { data: { userId: string; email: string } };
      'order/placed': { data: { orderId: string; total: number } };
    };
    
    // lib/inngest/functions.ts
    import { inngest } from './client';
    
    export const sendWelcomeEmail = inngest.createFunction(
      { id: 'send-welcome-email' },
      { event: 'user/signed.up' },
      async ({ event, step }) => {
        // Step 1: Get user details
        const user = await step.run('get-user', async () => {
          return await db.users.findUnique({ where: { id: event.data.userId } });
        });
    
        // Step 2: Send welcome email
        await step.run('send-email', async () => {
          await resend.emails.send({
            to: user.email,
            subject: 'Welcome!',
            template: 'welcome',
          });
        });
    
        // Step 3: Wait 24 hours, then send tips
        await step.sleep('wait-for-tips', '24h');
    
        await step.run('send-tips', async () => {
          await resend.emails.send({
            to: user.email,
            subject: 'Getting Started Tips',
            template: 'tips',
          });
        });
      }
    );
    
    // app/api/inngest/route.ts (Next.js App Router)
    import { serve } from 'inngest/next';
    import { inngest } from '@/lib/inngest/client';
    import { sendWelcomeEmail } from '@/lib/inngest/functions';
    
    export const { GET, POST, PUT } = serve({
      client: inngest,
      functions: [sendWelcomeEmail],
    });
    

---
  #### **Name**
Multi-Step Workflow
  #### **Description**
Complex workflow with parallel steps and error handling
  #### **When**
Processing that involves multiple services or long waits
  #### **Example**
    export const processOrder = inngest.createFunction(
      {
        id: 'process-order',
        retries: 3,
        concurrency: { limit: 10 },  // Max 10 orders processing at once
      },
      { event: 'order/placed' },
      async ({ event, step }) => {
        const { orderId } = event.data;
    
        // Parallel steps - both run simultaneously
        const [inventory, payment] = await Promise.all([
          step.run('check-inventory', () => checkInventory(orderId)),
          step.run('validate-payment', () => validatePayment(orderId)),
        ]);
    
        if (!inventory.available) {
          // Send event instead of direct call (fan-out pattern)
          await step.sendEvent('notify-backorder', {
            name: 'order/backordered',
            data: { orderId, items: inventory.missing },
          });
          return { status: 'backordered' };
        }
    
        // Process payment
        const charge = await step.run('charge-payment', async () => {
          return await stripe.charges.create({
            amount: event.data.total,
            customer: payment.customerId,
          });
        });
    
        // Ship order
        await step.run('ship-order', () => fulfillment.ship(orderId));
    
        return { status: 'completed', chargeId: charge.id };
      }
    );
    

---
  #### **Name**
Scheduled/Cron Functions
  #### **Description**
Functions that run on a schedule
  #### **When**
Recurring tasks like daily reports or cleanup jobs
  #### **Example**
    export const dailyDigest = inngest.createFunction(
      { id: 'daily-digest' },
      { cron: '0 9 * * *' },  // Every day at 9am UTC
      async ({ step }) => {
        // Get all users who want digests
        const users = await step.run('get-users', async () => {
          return await db.users.findMany({
            where: { digestEnabled: true },
          });
        });
    
        // Send to each user (creates child events)
        await step.sendEvent(
          'send-digests',
          users.map(user => ({
            name: 'digest/send',
            data: { userId: user.id },
          }))
        );
    
        return { sent: users.length };
      }
    );
    
    // Separate function handles individual digest sending
    export const sendDigest = inngest.createFunction(
      { id: 'send-digest', concurrency: { limit: 50 } },
      { event: 'digest/send' },
      async ({ event, step }) => {
        // ... send individual digest
      }
    );
    

---
  #### **Name**
Webhook Handler with Idempotency
  #### **Description**
Safely process webhooks with deduplication
  #### **When**
Handling Stripe, GitHub, or other webhooks
  #### **Example**
    export const handleStripeWebhook = inngest.createFunction(
      {
        id: 'stripe-webhook',
        // Deduplicate by Stripe event ID
        idempotency: 'event.data.stripeEventId',
      },
      { event: 'stripe/webhook.received' },
      async ({ event, step }) => {
        const { type, data } = event.data;
    
        switch (type) {
          case 'checkout.session.completed':
            await step.run('fulfill-order', async () => {
              await fulfillOrder(data.session.id);
            });
            break;
    
          case 'customer.subscription.deleted':
            await step.run('cancel-subscription', async () => {
              await cancelSubscription(data.subscription.id);
            });
            break;
        }
      }
    );
    

---
  #### **Name**
AI Pipeline with Long Processing
  #### **Description**
Multi-step AI processing with chunked work
  #### **When**
AI workflows that may take minutes to complete
  #### **Example**
    export const processDocument = inngest.createFunction(
      {
        id: 'process-document',
        retries: 2,
        concurrency: { limit: 5 },  // Limit API usage
      },
      { event: 'document/uploaded' },
      async ({ event, step }) => {
        // Step 1: Extract text (may take a while)
        const text = await step.run('extract-text', async () => {
          return await extractTextFromPDF(event.data.fileUrl);
        });
    
        // Step 2: Chunk for embedding
        const chunks = await step.run('chunk-text', async () => {
          return chunkText(text, { maxTokens: 500 });
        });
    
        // Step 3: Generate embeddings (API rate limited)
        const embeddings = await step.run('generate-embeddings', async () => {
          return await openai.embeddings.create({
            model: 'text-embedding-3-small',
            input: chunks,
          });
        });
    
        // Step 4: Store in vector DB
        await step.run('store-vectors', async () => {
          await vectorDb.upsert({
            vectors: embeddings.data.map((e, i) => ({
              id: `${event.data.documentId}-${i}`,
              values: e.embedding,
              metadata: { chunk: chunks[i] },
            })),
          });
        });
    
        return { chunks: chunks.length, status: 'indexed' };
      }
    );
    

## Anti-Patterns


---
  #### **Name**
Not Using Steps
  #### **Description**
Doing all work in a single block without step boundaries
  #### **Why**
    Without steps, there are no checkpoints. If the function fails halfway
    through, it restarts from the beginning. Steps give you resume capability.
    
  #### **Instead**
    Wrap each logical unit of work in step.run(). Even fast operations
    benefit from being steps - they become visible in the dashboard.
    

---
  #### **Name**
Huge Event Payloads
  #### **Description**
Sending large data in event payload
  #### **Why**
    Events are stored and transmitted. Large payloads slow everything down
    and hit size limits. Events should describe what happened, not carry data.
    
  #### **Instead**
    Send IDs and references. Fetch data inside step.run() where it's needed.
    

---
  #### **Name**
Ignoring Concurrency
  #### **Description**
Not setting concurrency limits for resource-intensive functions
  #### **Why**
    Without limits, a burst of events can overwhelm databases, APIs, or
    downstream services. Serverless scales fast - sometimes too fast.
    
  #### **Instead**
    Set concurrency limits based on what downstream services can handle.
    Start conservative, increase based on monitoring.
    

---
  #### **Name**
Not Using Idempotency Keys
  #### **Description**
Processing duplicate events as if they were unique
  #### **Why**
    Events can be delivered more than once. Without idempotency, you might
    charge customers twice, send duplicate emails, or corrupt data.
    
  #### **Instead**
    Use idempotency option with a unique key from the event data.
    

---
  #### **Name**
Blocking in Functions
  #### **Description**
Using long-running synchronous operations
  #### **Why**
    Serverless functions have timeouts. Long blocking operations hit limits.
    Inngest functions should be broken into resumable steps.
    
  #### **Instead**
    Break long operations into steps. Use step.sleep() for delays.
    Step boundaries are timeout boundaries.
    