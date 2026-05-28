# Stripe Integration - Sharp Edges

## Webhook Signature Skip

### **Id**
webhook-signature-skip
### **Summary**
Not verifying webhook signatures
### **Severity**
critical
### **Situation**
  Webhook endpoint accepts any POST request. Attacker sends fake "payment
  succeeded" webhooks. Users get premium access without paying.
  
### **Why**
  Anyone can POST to your webhook endpoint. Without signature verification,
  you're trusting random internet requests. This is a direct path to fraud.
  
### **Solution**
  # Always verify signatures:
  ```typescript
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(
    rawBody,  // Must be raw, not parsed JSON
    sig,
    process.env.STRIPE_WEBHOOK_SECRET
  );
  ```
  
  # Common mistakes:
  - Using parsed JSON body (must be raw)
  - Wrong secret (test vs live)
  - Missing signature header check
  
  # Test it:
  Try sending fake webhooks - they should fail
  
### **Symptoms**
  - No webhook signature verification
  - json() middleware before webhook route
  - "Works in development, fails in production"
### **Detection Pattern**
webhooks\.constructEvent.*body\)

## Raw Body Middleware

### **Id**
raw-body-middleware
### **Summary**
JSON middleware parsing body before webhook can verify
### **Severity**
critical
### **Situation**
  Express/Next.js parses JSON automatically. Webhook handler gets parsed
  body. Signature verification fails because it needs raw body.
  
### **Why**
  Stripe signatures are computed over the raw request body. Once parsed,
  the signature won't match. This causes silent webhook failures.
  
### **Solution**
  # Next.js App Router:
  ```typescript
  export async function POST(req: Request) {
    const rawBody = await req.text();  // Not req.json()
    const sig = req.headers.get('stripe-signature');
    const event = stripe.webhooks.constructEvent(
      rawBody,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  }
  ```
  
  # Express:
  ```javascript
  app.post('/webhook',
    express.raw({ type: 'application/json' }),
    (req, res) => { ... }
  );
  ```
  
  # Disable body parsing for webhook route only
  
### **Symptoms**
  - Signature verification fails
  - "No signatures found matching" error
  - Works locally, fails in production
### **Detection Pattern**
req\.json\(\)|bodyParser\.json\(\).*webhook

## Missing Idempotency

### **Id**
missing-idempotency
### **Summary**
Not using idempotency keys for payment operations
### **Severity**
high
### **Situation**
  User clicks pay twice. Network timeout causes retry. Two charges created.
  User angry, chargeback initiated, trust lost.
  
### **Why**
  Network failures happen. Retries happen. Without idempotency keys, you'll
  create duplicate charges, refunds, or subscriptions. Stripe handles this
  for you - if you use the keys.
  
### **Solution**
  # Always use idempotency keys:
  ```typescript
  const paymentIntent = await stripe.paymentIntents.create(
    {
      amount: 1000,
      currency: 'usd',
    },
    {
      idempotencyKey: `payment_${orderId}_${timestamp}`,
    }
  );
  ```
  
  # Key design:
  - Include order/user ID
  - Include timestamp or version
  - Same key = same result (no duplicate)
  
  # Critical operations:
  - Payment creation
  - Subscription creation
  - Refunds
  - Any state-changing operation
  
### **Symptoms**
  - Duplicate charges on retry
  - "Payment already exists" errors in production
  - Race conditions on subscribe button
### **Detection Pattern**
paymentIntents\.create(?!.*idempotencyKey)

## Api As Source Of Truth

### **Id**
api-as-source-of-truth
### **Summary**
Trusting API responses instead of webhooks for payment status
### **Severity**
critical
### **Situation**
  Check payment status via API after checkout. Network fails. Mark as unpaid.
  Webhook arrives later saying it succeeded. User didn't get access but was charged.
  
### **Why**
  API calls are point-in-time snapshots. Payments are asynchronous. The webhook
  is the authoritative notification of state change. Building on API responses
  creates race conditions.
  
### **Solution**
  # Webhook-first architecture:
  1. Create checkout session/payment intent
  2. Wait for webhook (don't poll API)
  3. Update your database from webhook
  4. User sees result from your database
  
  # Never:
  - Grant access based on API response
  - Assume payment succeeded without webhook
  - Poll for status (use webhooks)
  
  # Handle late webhooks:
  - Webhooks can be delayed
  - Your system must handle out-of-order
  - Idempotent handlers are essential
  
### **Symptoms**
  - Checking payment status via API after checkout
  - "Succeeded in Stripe but user doesn't have access"
  - Polling for payment status
### **Detection Pattern**
paymentIntents\.retrieve.*status

## Checkout Session Missing Metadata

### **Id**
checkout-session-missing-metadata
### **Summary**
Not passing metadata through checkout session
### **Severity**
high
### **Situation**
  User completes checkout. Webhook arrives. No way to know which user or
  order this payment is for. Manually matching payments to users.
  
### **Why**
  Checkout sessions create their own payment intents. Without metadata,
  you lose the connection to your user/order. You're left guessing or
  doing expensive lookups.
  
### **Solution**
  # Always include metadata:
  ```typescript
  const session = await stripe.checkout.sessions.create({
    // ...
    metadata: {
      userId: user.id,
      orderId: order.id,
      planId: plan.id,
    },
    subscription_data: {
      metadata: {
        userId: user.id,  // Also on subscription!
      },
    },
  });
  ```
  
  # Metadata flows:
  - Session metadata → webhook
  - subscription_data.metadata → subscription
  - payment_intent_data.metadata → payment intent
  
  # In webhook:
  ```typescript
  const { userId, orderId } = event.data.object.metadata;
  ```
  
### **Symptoms**
  - Can't identify user from webhook
  - Manual payment reconciliation
  - Missing metadata on subscription object
### **Detection Pattern**
checkout\.sessions\.create(?!.*metadata)

## Subscription State Mismatch

### **Id**
subscription-state-mismatch
### **Summary**
Local subscription state drifting from Stripe state
### **Severity**
high
### **Situation**
  User's subscription in your database says "active." Stripe says "canceled."
  User getting free access. Or worse: user can't access what they paid for.
  
### **Why**
  Subscription state changes in Stripe (upgrades, downgrades, cancellations,
  payment failures). If you don't sync via webhooks, your state drifts.
  This is how you lose money or lose customers.
  
### **Solution**
  # Handle ALL subscription webhooks:
  - customer.subscription.created
  - customer.subscription.updated
  - customer.subscription.deleted
  - invoice.paid
  - invoice.payment_failed
  
  # Sync strategy:
  ```typescript
  async function handleSubscriptionUpdate(subscription) {
    await db.subscriptions.upsert({
      stripeId: subscription.id,
      status: subscription.status,
      currentPeriodEnd: subscription.current_period_end,
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
      priceId: subscription.items.data[0].price.id,
    });
  }
  ```
  
  # Never trust local state:
  Always check Stripe or sync from webhooks
  
### **Symptoms**
  - Users with access they shouldn't have
  - Users without access they should have
  - "Active" in DB but "canceled" in Stripe
### **Detection Pattern**


## Payment Failure Ignorance

### **Id**
payment-failure-ignorance
### **Summary**
Not handling failed payments and dunning
### **Severity**
high
### **Situation**
  Payment fails. Stripe retries. Eventually gives up. User churns. You never
  reached out. Could have saved the customer with a simple email.
  
### **Why**
  Payment failures are recoverable. 30-40% of failed payments can be recovered
  with proper dunning. Without handling, you're leaving revenue on the table.
  
### **Solution**
  # Handle invoice.payment_failed:
  ```typescript
  case 'invoice.payment_failed':
    const invoice = event.data.object;
    // Send email to customer
    // Log for follow-up
    // Maybe pause service (carefully)
    break;
  ```
  
  # Dunning flow:
  1. First failure: Email with update card link
  2. 3 days later: Reminder email
  3. 7 days later: Warning of service pause
  4. Final: Service paused, recovery email
  
  # Customer portal:
  Let users self-serve update payment methods
  https://stripe.com/docs/billing/subscriptions/integrating-customer-portal
  
### **Symptoms**
  - No invoice.payment_failed handler
  - Users churning after payment failure
  - No dunning emails
  - Can't see payment failure rate
### **Detection Pattern**


## Test Mode To Live Mismatch

### **Id**
test-mode-to-live-mismatch
### **Summary**
Different code paths or behavior between test and live mode
### **Severity**
high
### **Situation**
  Works perfectly in test mode. Goes live. Webhook signatures fail. Different
  webhook secret. Different API key. Different behavior.
  
### **Why**
  Test and live mode are separate environments. Different keys, different
  webhooks, different customers. Code that works in test must work identically
  in live - but with different configuration.
  
### **Solution**
  # Separate all keys:
  ```env
  STRIPE_SECRET_KEY=sk_test_xxx  # or sk_live_xxx
  STRIPE_PUBLISHABLE_KEY=pk_test_xxx  # or pk_live_xxx
  STRIPE_WEBHOOK_SECRET=whsec_xxx  # Different per environment
  ```
  
  # Per-environment webhooks:
  - Set up separate webhook endpoints in Stripe
  - Test: points to localhost/ngrok
  - Live: points to production URL
  
  # Test with real flow:
  - Use Stripe CLI for local testing
  - Test complete flows, not just API calls
  - Use test card numbers that simulate failures
  
### **Symptoms**
  - "Works in test, fails in live"
  - Using test keys in production
  - Single webhook endpoint for both modes
### **Detection Pattern**
sk_test_|pk_test_

## Currency Assumption

### **Id**
currency-assumption
### **Summary**
Assuming all payments are in one currency
### **Severity**
medium
### **Situation**
  Hard-coded USD everywhere. International customer pays. Currency mismatch.
  Incorrect amounts displayed. Legal issues in some countries.
  
### **Why**
  Stripe handles multi-currency, but your code must too. Hard-coding USD
  breaks for international customers and can create legal compliance issues.
  
### **Solution**
  # Store and display currency:
  ```typescript
  const price = await stripe.prices.retrieve(priceId);
  const amount = price.unit_amount;
  const currency = price.currency;
  
  // Format properly
  new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount / 100);
  ```
  
  # In database:
  Store currency alongside amount
  Don't assume, always check
  
  # Multi-currency pricing:
  Create prices in different currencies
  Let Stripe handle conversion
  
### **Symptoms**
  - Hard-coded "USD" or "$"
  - Amount without currency stored
  - International customers seeing wrong currency
### **Detection Pattern**
currency.*['"]usd['"]|\$.*amount

## Refund Without Check

### **Id**
refund-without-check
### **Summary**
Processing refunds without proper validation
### **Severity**
high
### **Situation**
  Admin panel has refund button. No confirmation. No audit log. Employee
  refunds themselves. Or attacker finds endpoint and mass-refunds.
  
### **Why**
  Refunds are irreversible money movement. They need protection - authorization,
  confirmation, audit logging, rate limiting. Treating them casually is
  how you lose money.
  
### **Solution**
  # Refund checklist:
  - [ ] Authorization check (who can refund?)
  - [ ] Amount validation (not more than paid)
  - [ ] Confirmation step
  - [ ] Audit logging (who, when, why)
  - [ ] Rate limiting
  - [ ] Reason required
  
  # Implementation:
  ```typescript
  async function processRefund(
    paymentIntentId: string,
    amount: number,
    reason: string,
    adminUserId: string
  ) {
    // 1. Verify admin has permission
    // 2. Verify amount <= original charge
    // 3. Create refund
    // 4. Log with full audit trail
  }
  ```
  
  # Partial refunds:
  Track total refunded per payment
  Prevent over-refunding
  
### **Symptoms**
  - Refund endpoint without auth check
  - No refund audit log
  - Can refund more than paid
  - No refund reason tracked
### **Detection Pattern**
refunds\.create(?!.*reason)

## Connect Account Confusion

### **Id**
connect-account-confusion
### **Summary**
Mixing platform and connected account operations in Stripe Connect
### **Severity**
high
### **Situation**
  Using Stripe Connect. Sometimes charges go to platform, sometimes to
  connected account. Confusion about who gets paid. Incorrect fee splits.
  
### **Why**
  Stripe Connect has three parties: platform, connected account, customer.
  Operations can be on behalf of platform or connected account. Mixing them
  up means money goes to wrong place.
  
### **Solution**
  # Clear mental model:
  - Platform = you
  - Connected account = your seller/provider
  - Customer = end buyer
  
  # Stripe-Account header:
  ```typescript
  // Operation on connected account:
  const charge = await stripe.charges.create(
    { amount: 1000, currency: 'usd' },
    { stripeAccount: connectedAccountId }
  );
  ```
  
  # Destination charges (common pattern):
  ```typescript
  const paymentIntent = await stripe.paymentIntents.create({
    amount: 1000,
    currency: 'usd',
    transfer_data: {
      destination: connectedAccountId,
      amount: 800,  // Connected account gets 800
    },
    // Platform gets 200 (application_fee)
  });
  ```
  
  # Test both sides:
  Platform dashboard AND connected account dashboard
  
### **Symptoms**
  - Money going to wrong account
  - "Account not found" errors
  - Confused about fee splits
  - Testing only platform side
### **Detection Pattern**
