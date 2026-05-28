# Upstash Qstash - Sharp Edges

## Signature Verification Skip

### **Id**
signature-verification-skip
### **Summary**
Not verifying QStash webhook signatures
### **Severity**
critical
### **Situation**
  Endpoint accepts any POST request. Attacker discovers your callback URL.
  Fake messages flood your system. Malicious payloads processed as trusted.
  
### **Why**
  QStash endpoints are public URLs. Without signature verification, anyone
  can send requests. This is a direct path to unauthorized message processing
  and potential data manipulation.
  
### **Solution**
  # Always verify signatures with both keys:
  ```typescript
  import { Receiver } from '@upstash/qstash';
  
  const receiver = new Receiver({
    currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
    nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
  });
  
  export async function POST(req: NextRequest) {
    const signature = req.headers.get('upstash-signature');
    const body = await req.text();  // Raw body required
  
    const isValid = await receiver.verify({
      signature: signature!,
      body,
      url: req.url,
    });
  
    if (!isValid) {
      return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
    }
  
    // Safe to process
  }
  ```
  
  # Why two keys?
  - QStash rotates signing keys
  - nextSigningKey becomes current during rotation
  - Both must be checked for seamless key rotation
  
### **Symptoms**
  - No Receiver import in webhook handler
  - Missing upstash-signature header check
  - Processing request before verification
### **Detection Pattern**
Receiver|upstash-signature|verify\(

## Callback Timeout Exceeded

### **Id**
callback-timeout-exceeded
### **Summary**
Callback endpoint taking too long to respond
### **Severity**
high
### **Situation**
  Webhook handler does heavy processing. Takes 30+ seconds. QStash times out.
  Marks message as failed. Retries. Double processing begins.
  
### **Why**
  QStash has a 30-second timeout for callbacks. If your endpoint doesn't respond
  in time, QStash considers it failed and retries. Long-running handlers create
  duplicate message processing and wasted retries.
  
### **Solution**
  # Design for fast acknowledgment:
  ```typescript
  export async function POST(req: NextRequest) {
    // 1. Verify signature first (fast)
    // 2. Parse and validate message (fast)
    // 3. Queue for async processing (fast)
  
    const message = await parseMessage(req);
  
    // Don't do this:
    // await processHeavyWork(message);  // Could timeout!
  
    // Do this instead:
    await db.jobs.create({ data: message, status: 'pending' });
    // Or use another QStash message for the heavy work
  
    return NextResponse.json({ queued: true });  // Respond fast
  }
  ```
  
  # Alternative: Use QStash for the heavy work
  ```typescript
  // Webhook receives trigger
  await qstash.publishJSON({
    url: 'https://myapp.com/api/heavy-process',
    body: { jobId: message.id },
  });
  return NextResponse.json({ delegated: true });
  ```
  
  # For Vercel: Consider using Edge runtime for faster cold starts
  
### **Symptoms**
  - Webhook timeouts in QStash dashboard
  - Messages marked failed then retried
  - Duplicate processing of same message
### **Detection Pattern**


## Rate Limit Exhaustion

### **Id**
rate-limit-exhaustion
### **Summary**
Hitting QStash rate limits unexpectedly
### **Severity**
high
### **Situation**
  Burst of events triggers mass message publishing. QStash rate limit hit.
  Messages rejected. Users don't get notifications. Critical tasks delayed.
  
### **Why**
  QStash has plan-based rate limits. Free tier: 500 messages/day. Pro: higher
  but still limited. Bursts can exhaust limits quickly. Without monitoring,
  you won't know until users complain.
  
### **Solution**
  # Check your plan limits:
  - Free: 500 messages/day
  - Pay as you go: Check dashboard
  - Pro: Higher limits, check dashboard
  
  # Implement rate limit handling:
  ```typescript
  try {
    await qstash.publishJSON({ url, body });
  } catch (error) {
    if (error.message?.includes('rate limit')) {
      // Queue locally and retry later
      await localQueue.add('qstash-retry', { url, body });
    }
    throw error;
  }
  ```
  
  # Batch messages when possible:
  ```typescript
  // Instead of 100 individual publishes
  await qstash.batchJSON({
    messages: items.map(item => ({
      url: 'https://myapp.com/api/process',
      body: { itemId: item.id },
    })),
  });
  ```
  
  # Monitor in dashboard:
  Upstash Console shows usage and limits
  
### **Symptoms**
  - 429 errors from QStash
  - Messages not being delivered
  - Sudden drop in processing during peak times
### **Detection Pattern**


## Missing Idempotency Key

### **Id**
missing-idempotency-key
### **Summary**
Not using deduplication for critical operations
### **Severity**
high
### **Situation**
  Network hiccup during publish. SDK retries. Same message sent twice.
  Customer charged twice. Email sent twice. Data corrupted.
  
### **Why**
  Network failures and retries happen. Without deduplication, the same logical
  message can be sent multiple times. QStash provides deduplication, but you
  must use it for critical operations.
  
### **Solution**
  # Use deduplication for critical messages:
  ```typescript
  // Custom ID (best for business operations)
  await qstash.publishJSON({
    url: 'https://myapp.com/api/charge',
    body: { orderId: '123', amount: 5000 },
    deduplicationId: `charge-${orderId}`,  // Same ID = same message
  });
  
  // Content-based (good for notifications)
  await qstash.publishJSON({
    url: 'https://myapp.com/api/notify',
    body: { userId: '456', type: 'welcome' },
    contentBasedDeduplication: true,  // Hash of body
  });
  ```
  
  # Deduplication window:
  - Default: 60 seconds
  - Messages with same ID in window are deduplicated
  - Plan for this in your retry logic
  
  # Also make endpoints idempotent:
  Check if operation already completed before processing
  
### **Symptoms**
  - Duplicate charges or emails
  - Double processing of same event
  - User complaints about duplicates
### **Detection Pattern**
publishJSON\([^)]*\)(?!.*deduplicationId)

## Private Endpoint Assumption

### **Id**
private-endpoint-assumption
### **Summary**
Expecting QStash to reach private/localhost endpoints
### **Severity**
critical
### **Situation**
  Development works with local server. Deploy to production with internal URL.
  QStash can't reach it. All messages fail silently. No processing happens.
  
### **Why**
  QStash runs in Upstash's cloud. It can only reach public, internet-accessible
  URLs. localhost, internal IPs, and private networks are unreachable. This is
  a fundamental architecture requirement, not a configuration issue.
  
### **Solution**
  # Production requirements:
  - URL must be publicly accessible
  - HTTPS required (HTTP will fail)
  - No localhost, 127.0.0.1, or private IPs
  
  # Local development options:
  
  # Option 1: ngrok/localtunnel
  ```bash
  ngrok http 3000
  # Use the ngrok URL for QStash testing
  ```
  
  # Option 2: QStash local development mode
  ```typescript
  // In development, skip QStash and call directly
  if (process.env.NODE_ENV === 'development') {
    await fetch('http://localhost:3000/api/process', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  } else {
    await qstash.publishJSON({ url, body: data });
  }
  ```
  
  # Option 3: Use Vercel preview URLs
  Preview deploys give you public URLs for testing
  
### **Symptoms**
  - Messages show "failed" in QStash dashboard
  - Works locally but fails in "production"
  - Using http:// instead of https://
### **Detection Pattern**
localhost|127\.0\.0\.1|http://

## Missing Retry Configuration

### **Id**
missing-retry-configuration
### **Summary**
Using default retry behavior for all message types
### **Severity**
medium
### **Situation**
  Critical payment webhook uses defaults. 3 retries over minutes. Payment
  processor is temporarily down for 15 minutes. Message marked as failed.
  Payment reconciliation manual work required.
  
### **Why**
  Default retry behavior (3 attempts, short backoff) works for many cases but
  not all. Some endpoints need more attempts, longer backoff, or different
  strategies. One size doesn't fit all.
  
### **Solution**
  # Configure retries per message:
  ```typescript
  // Critical operations: more retries, longer backoff
  await qstash.publishJSON({
    url: 'https://myapp.com/api/payment-webhook',
    body: { paymentId: '123' },
    retries: 5,
    // Backoff: 10s, 30s, 1m, 5m, 30m
  });
  
  // Non-critical notifications: fewer retries
  await qstash.publishJSON({
    url: 'https://myapp.com/api/analytics',
    body: { event: 'pageview' },
    retries: 1,  // Fail fast, not critical
  });
  ```
  
  # Consider your endpoint's recovery time:
  - Database down: May need 5+ minutes
  - Third-party API: May need hours
  - Internal service: Usually quick
  
  # Use failure callbacks for dead letter handling:
  ```typescript
  await qstash.publishJSON({
    url: 'https://myapp.com/api/critical',
    body: data,
    failureCallback: 'https://myapp.com/api/dead-letter',
  });
  ```
  
### **Symptoms**
  - Critical messages marked failed
  - Manual intervention needed for retries
  - Temporary outages causing permanent failures
### **Detection Pattern**


## Large Message Body

### **Id**
large-message-body
### **Summary**
Sending large payloads instead of references
### **Severity**
medium
### **Situation**
  Message contains entire document (5MB). QStash rejects - body too large.
  Even if accepted, slow to transmit. Expensive. Wastes bandwidth.
  
### **Why**
  QStash has message size limits (around 500KB body). Large payloads slow
  delivery, increase costs, and can fail entirely. Messages should be
  lightweight triggers, not data carriers.
  
### **Solution**
  # Send references, not data:
  ```typescript
  // BAD: Large payload
  await qstash.publishJSON({
    url: 'https://myapp.com/api/process',
    body: { document: largeDocumentContent },  // 5MB!
  });
  
  // GOOD: Reference only
  await qstash.publishJSON({
    url: 'https://myapp.com/api/process',
    body: { documentId: 'doc_123' },  // Fetch in handler
  });
  ```
  
  # In your handler:
  ```typescript
  export async function POST(req: NextRequest) {
    const { documentId } = await req.json();
    const document = await storage.get(documentId);  // Fetch actual data
    await processDocument(document);
  }
  ```
  
  # Large data storage options:
  - S3/R2/Blob storage for files
  - Database for structured data
  - Redis for temporary data (Upstash Redis pairs well)
  
### **Symptoms**
  - Message publish failures
  - Slow message delivery
  - High bandwidth costs
### **Detection Pattern**


## Callback Response Ignored

### **Id**
callback-response-ignored
### **Summary**
Not using callback/failureCallback for critical flows
### **Severity**
medium
### **Situation**
  Important task published. QStash delivers. Endpoint processes. But your
  system doesn't know it succeeded. User stuck waiting. No feedback loop.
  
### **Why**
  QStash is fire-and-forget by default. Without callbacks, you don't know
  if messages were delivered successfully. For critical flows, you need
  the feedback loop to update state and handle failures.
  
### **Solution**
  # Use callbacks for critical operations:
  ```typescript
  await qstash.publishJSON({
    url: 'https://myapp.com/api/send-email',
    body: { userId: '123', template: 'welcome' },
    callback: 'https://myapp.com/api/email-callback',
    failureCallback: 'https://myapp.com/api/email-failed',
  });
  ```
  
  # Handle the callback:
  ```typescript
  // app/api/email-callback/route.ts
  export async function POST(req: NextRequest) {
    // Verify signature first!
    const data = await req.json();
  
    // data.sourceMessageId - original message
    // data.status - HTTP status code
    // data.body - response from endpoint
  
    await db.emailLogs.update({
      where: { messageId: data.sourceMessageId },
      data: { status: 'delivered' },
    });
  
    return NextResponse.json({ received: true });
  }
  ```
  
  # Failure callback for alerting:
  ```typescript
  // app/api/email-failed/route.ts
  export async function POST(req: NextRequest) {
    const data = await req.json();
    await alerting.notify(`Email failed: ${data.sourceMessageId}`);
    await db.emailLogs.update({
      where: { messageId: data.sourceMessageId },
      data: { status: 'failed', error: data.body },
    });
  }
  ```
  
### **Symptoms**
  - No visibility into message delivery
  - Users waiting for actions that completed
  - No alerting on failures
### **Detection Pattern**


## Schedule Timezone Confusion

### **Id**
schedule-timezone-confusion
### **Summary**
Cron schedules using wrong timezone
### **Severity**
medium
### **Situation**
  Scheduled daily report at "9am". But 9am in which timezone? QStash uses UTC.
  Report runs at 4am local time. Users confused. Support tickets filed.
  
### **Why**
  QStash cron schedules run in UTC. If you think in local time but configure
  in UTC, schedules will run at unexpected times. This is especially tricky
  with daylight saving time changes.
  
### **Solution**
  # QStash uses UTC:
  ```typescript
  // This runs at 9am UTC, not local time
  await qstash.schedules.create({
    destination: 'https://myapp.com/api/daily-report',
    cron: '0 9 * * *',  // 9am UTC
  });
  ```
  
  # Convert to UTC:
  - 9am EST = 2pm UTC (winter) / 1pm UTC (summer)
  - 9am PST = 5pm UTC (winter) / 4pm UTC (summer)
  
  # Document timezone in schedule name:
  ```typescript
  await qstash.schedules.create({
    destination: 'https://myapp.com/api/daily-report',
    cron: '0 14 * * *',  // 9am EST (14:00 UTC)
    body: JSON.stringify({
      timezone: 'America/New_York',
      localTime: '9:00 AM',
    }),
  });
  ```
  
  # Handle DST programmatically if needed:
  Update schedules when DST changes, or accept UTC timing
  
### **Symptoms**
  - Schedules running at unexpected times
  - Off-by-one-hour issues during DST
  - User complaints about report timing
### **Detection Pattern**


## Url Group Stale Endpoints

### **Id**
url-group-stale-endpoints
### **Summary**
URL groups with dead or outdated endpoints
### **Severity**
medium
### **Situation**
  URL group has 5 endpoints. One service deprecated months ago. Messages
  still fan out to it. Failures in dashboard. Wasted attempts. Slower delivery.
  
### **Why**
  URL groups persist until explicitly updated. When services change, endpoints
  become stale. QStash tries to deliver to dead URLs, wastes retries, and
  the failure noise obscures real issues.
  
### **Solution**
  # Audit URL groups regularly:
  ```typescript
  const groups = await qstash.urlGroups.list();
  for (const group of groups) {
    console.log(`Group: ${group.name}`);
    for (const endpoint of group.endpoints) {
      // Check if endpoint is still valid
      try {
        await fetch(endpoint.url, { method: 'HEAD' });
        console.log(`  OK: ${endpoint.url}`);
      } catch {
        console.log(`  DEAD: ${endpoint.url}`);
      }
    }
  }
  ```
  
  # Update groups when services change:
  ```typescript
  // Remove dead endpoint
  await qstash.urlGroups.removeEndpoints({
    name: 'order-processors',
    endpoints: [{ url: 'https://old-service.myapp.com/api/process' }],
  });
  ```
  
  # Automate in CI/CD:
  Check URL group health as part of deployment
  
### **Symptoms**
  - Failed deliveries in URL groups
  - Messages to deprecated services
  - Slow fan-out due to timeouts
### **Detection Pattern**
