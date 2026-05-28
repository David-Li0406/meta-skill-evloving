# Stripe Integration

## Patterns


---
  #### **Name**
Idempotency Key Everything
  #### **Description**
Use idempotency keys on all payment operations to prevent duplicate charges
  #### **When**
Any operation that creates or modifies financial data
  #### **Example**
    import { v4 as uuid } from 'uuid';
    
    const idempotencyKey = `charge_${userId}_${orderId}`;
    
    const charge = await stripe.charges.create({
      amount: 5000,
      currency: 'usd',
      customer: customerId
    }, {
      idempotencyKey
    });
    

---
  #### **Name**
Webhook State Machine
  #### **Description**
Handle webhooks as state transitions, not triggers
  #### **When**
Processing subscription lifecycle events
  #### **Example**
    // Store webhook events before processing
    const event = await db.webhookEvents.create({ ... });
    
    switch (event.type) {
      case 'customer.subscription.created':
        await transition(subscription, 'active');
        break;
      case 'invoice.payment_failed':
        await transition(subscription, 'past_due');
        break;
    }
    

---
  #### **Name**
Test Mode Throughout Development
  #### **Description**
Use Stripe test mode with real test cards for all development
  #### **When**
Building any Stripe integration
  #### **Example**
    # Environment setup
    STRIPE_SECRET_KEY=sk_test_...
    STRIPE_PUBLISHABLE_KEY=pk_test_...
    
    # Use Stripe test cards
    4242 4242 4242 4242 - Success
    4000 0000 0000 0002 - Declined
    4000 0000 0000 9995 - Insufficient funds
    

---
  #### **Name**
Sync Before Act
  #### **Description**
Always fetch latest state from Stripe before making decisions
  #### **When**
User-triggered operations on existing Stripe objects
  #### **Example**
    // Don't trust local state for financial decisions
    const subscription = await stripe.subscriptions.retrieve(subId);
    
    if (subscription.status === 'active') {
      // Safe to proceed with upgrade
    }
    

---
  #### **Name**
Separate Webhook Receiver from Processor
  #### **Description**
Receive webhook, verify signature, queue for processing, return 200
  #### **When**
Implementing webhook handlers
  #### **Example**
    // Webhook endpoint (fast, synchronous)
    export async function POST(req: Request) {
      const payload = await req.text();
      const sig = req.headers.get('stripe-signature')!;
    
      const event = stripe.webhooks.constructEvent(payload, sig, secret);
    
      // Queue for processing
      await queue.add('stripe-webhook', event);
    
      return new Response(null, { status: 200 });
    }
    

---
  #### **Name**
Dunning with Grace Periods
  #### **Description**
Give customers time to fix payment failures before degrading service
  #### **When**
Handling failed subscription payments
  #### **Example**
    # Stripe's Smart Retries handle initial failures
    # Add grace period before action:
    # Day 0: Payment fails, email sent
    # Day 3: Reminder email
    # Day 7: Final warning
    # Day 10: Downgrade or suspend
    

## Anti-Patterns


---
  #### **Name**
Trust the API Response
  #### **Description**
Assuming the API call succeeded means the operation completed
  #### **Why**
API might return success but webhook reveals the real outcome
  #### **Instead**
    Webhooks are source of truth. API responses are optimistic.
    Wait for webhook confirmation before showing success to user.
    

---
  #### **Name**
Webhook Without Signature Verification
  #### **Description**
Processing webhook events without verifying they came from Stripe
  #### **Why**
Attackers can forge webhook payloads to credit accounts or trigger actions
  #### **Instead**
    Always verify webhook signature:
    const event = stripe.webhooks.constructEvent(
      payload,
      signature,
      webhookSecret
    );
    

---
  #### **Name**
Subscription Status Checks Without Refresh
  #### **Description**
Checking subscription.status from database without fetching from Stripe
  #### **Why**
Local state goes stale, payment failures happen between checks
  #### **Instead**
    await stripe.subscriptions.retrieve(subId) before any financial decision.
    Cache with short TTL (minutes, not hours).
    

---
  #### **Name**
Synchronous Webhook Processing
  #### **Description**
Doing slow work in webhook handler before returning 200
  #### **Why**
Stripe times out at 5 seconds and retries, causing duplicate processing
  #### **Instead**
    Verify signature → Queue event → Return 200 immediately.
    Process asynchronously with retry logic.
    

---
  #### **Name**
Customer Creation Without Error Handling
  #### **Description**
Creating customers without handling duplicate errors
  #### **Why**
Race conditions cause duplicate customer records
  #### **Instead**
    Use idempotency keys. Check for existing customer by email first.
    Handle resource_already_exists error gracefully.
    

---
  #### **Name**
Hardcoded Prices
  #### **Description**
Hardcoding price IDs or amounts in code
  #### **Why**
Price changes require code deployment, A/B testing is impossible
  #### **Instead**
    Store price IDs in database or config. Use Stripe's Price objects.
    Support multiple active prices per product.
    