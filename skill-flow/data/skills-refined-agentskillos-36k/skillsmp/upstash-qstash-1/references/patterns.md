# Upstash QStash

## Patterns


---
  #### **Name**
Basic Message Publishing
  #### **Description**
Sending messages to be delivered to endpoints
  #### **When**
Need reliable async HTTP calls
  #### **Example**
    import { Client } from '@upstash/qstash';
    
    const qstash = new Client({
      token: process.env.QSTASH_TOKEN!,
    });
    
    // Simple message to endpoint
    await qstash.publishJSON({
      url: 'https://myapp.com/api/process',
      body: {
        userId: '123',
        action: 'welcome-email',
      },
    });
    
    // With delay (process in 1 hour)
    await qstash.publishJSON({
      url: 'https://myapp.com/api/reminder',
      body: { userId: '123' },
      delay: 60 * 60,  // seconds
    });
    
    // With specific delivery time
    await qstash.publishJSON({
      url: 'https://myapp.com/api/scheduled',
      body: { report: 'daily' },
      notBefore: Math.floor(Date.now() / 1000) + 86400,  // tomorrow
    });
    

---
  #### **Name**
Scheduled Cron Jobs
  #### **Description**
Setting up recurring scheduled tasks
  #### **When**
Need periodic background jobs without infrastructure
  #### **Example**
    import { Client } from '@upstash/qstash';
    
    const qstash = new Client({
      token: process.env.QSTASH_TOKEN!,
    });
    
    // Create a scheduled job
    const schedule = await qstash.schedules.create({
      destination: 'https://myapp.com/api/cron/daily-report',
      cron: '0 9 * * *',  // Every day at 9 AM UTC
      body: JSON.stringify({ type: 'daily' }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    console.log('Schedule created:', schedule.scheduleId);
    
    // List all schedules
    const schedules = await qstash.schedules.list();
    
    // Delete a schedule
    await qstash.schedules.delete(schedule.scheduleId);
    

---
  #### **Name**
Signature Verification
  #### **Description**
Verifying QStash message signatures in your endpoint
  #### **When**
Any endpoint receiving QStash messages (always!)
  #### **Example**
    // app/api/webhook/route.ts (Next.js App Router)
    import { Receiver } from '@upstash/qstash';
    import { NextRequest, NextResponse } from 'next/server';
    
    const receiver = new Receiver({
      currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
      nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
    });
    
    export async function POST(req: NextRequest) {
      const signature = req.headers.get('upstash-signature');
      const body = await req.text();
    
      // ALWAYS verify signature
      const isValid = await receiver.verify({
        signature: signature!,
        body,
        url: req.url,
      });
    
      if (!isValid) {
        return NextResponse.json(
          { error: 'Invalid signature' },
          { status: 401 }
        );
      }
    
      // Safe to process
      const data = JSON.parse(body);
      await processMessage(data);
    
      return NextResponse.json({ success: true });
    }
    

---
  #### **Name**
Callback for Delivery Status
  #### **Description**
Getting notified when messages are delivered or fail
  #### **When**
Need to track delivery status for critical messages
  #### **Example**
    import { Client } from '@upstash/qstash';
    
    const qstash = new Client({
      token: process.env.QSTASH_TOKEN!,
    });
    
    // Publish with callback
    await qstash.publishJSON({
      url: 'https://myapp.com/api/critical-task',
      body: { taskId: '456' },
      callback: 'https://myapp.com/api/qstash-callback',
      failureCallback: 'https://myapp.com/api/qstash-failed',
    });
    
    // Callback endpoint receives delivery status
    // app/api/qstash-callback/route.ts
    export async function POST(req: NextRequest) {
      // Verify signature first!
      const data = await req.json();
    
      // data contains:
      // - sourceMessageId: original message ID
      // - url: destination URL
      // - status: HTTP status code
      // - body: response body
    
      if (data.status >= 200 && data.status < 300) {
        await markTaskComplete(data.sourceMessageId);
      }
    
      return NextResponse.json({ received: true });
    }
    

---
  #### **Name**
URL Groups (Fan-out)
  #### **Description**
Sending messages to multiple endpoints at once
  #### **When**
Need to notify multiple services about an event
  #### **Example**
    import { Client } from '@upstash/qstash';
    
    const qstash = new Client({
      token: process.env.QSTASH_TOKEN!,
    });
    
    // Create a URL group
    await qstash.urlGroups.addEndpoints({
      name: 'order-processors',
      endpoints: [
        { url: 'https://inventory.myapp.com/api/process' },
        { url: 'https://shipping.myapp.com/api/process' },
        { url: 'https://analytics.myapp.com/api/track' },
      ],
    });
    
    // Publish to the group - all endpoints receive the message
    await qstash.publishJSON({
      urlGroup: 'order-processors',
      body: {
        orderId: '789',
        event: 'order.placed',
      },
    });
    

---
  #### **Name**
Message Deduplication
  #### **Description**
Preventing duplicate message processing
  #### **When**
Idempotency is critical (payments, notifications)
  #### **Example**
    import { Client } from '@upstash/qstash';
    
    const qstash = new Client({
      token: process.env.QSTASH_TOKEN!,
    });
    
    // Deduplicate by custom ID (within deduplication window)
    await qstash.publishJSON({
      url: 'https://myapp.com/api/charge',
      body: { orderId: '123', amount: 5000 },
      deduplicationId: 'charge-order-123',  // Won't send again within window
    });
    
    // Content-based deduplication
    await qstash.publishJSON({
      url: 'https://myapp.com/api/notify',
      body: { userId: '456', message: 'Hello' },
      contentBasedDeduplication: true,  // Hash of body used as ID
    });
    

## Anti-Patterns


---
  #### **Name**
Skipping Signature Verification
  #### **Description**
Processing QStash messages without verifying signatures
  #### **Why**
    Anyone could send fake messages to your endpoint. Without verification,
    you're processing potentially malicious or spoofed data.
    
  #### **Instead**
    ALWAYS use the Receiver to verify signatures. No exceptions.
    Return 401 for invalid signatures.
    

---
  #### **Name**
Using Private Endpoints
  #### **Description**
Expecting QStash to reach localhost or private IPs
  #### **Why**
    QStash runs in the cloud. It can only reach public URLs. Private
    endpoints will always fail delivery.
    
  #### **Instead**
    Use public URLs. For local dev, use ngrok or similar tunneling.
    Or use QStash's local development mode.
    

---
  #### **Name**
No Error Handling in Endpoints
  #### **Description**
Endpoints that don't return proper status codes
  #### **Why**
    QStash uses HTTP status codes to determine success. 500 triggers
    retries, 200 means success. Silent failures cause confusion.
    
  #### **Instead**
    Return 200 only on success. Return 4xx/5xx on failures.
    Be explicit about what went wrong.
    

---
  #### **Name**
Giant Message Bodies
  #### **Description**
Sending large payloads in messages
  #### **Why**
    QStash has message size limits. Large payloads slow delivery
    and increase costs. Messages should be pointers, not data.
    
  #### **Instead**
    Send IDs and references. Fetch actual data in your endpoint.
    Store large data in S3/database.
    

---
  #### **Name**
Ignoring Retries
  #### **Description**
Not configuring retry behavior for your use case
  #### **Why**
    Default retries may not match your needs. Some endpoints need
    more attempts, others need faster failure.
    
  #### **Instead**
    Configure retries explicitly. Set appropriate retry counts
    and backoff strategies for each message type.
    