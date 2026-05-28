---
name: payment-integration
description: Use this skill when implementing secure payment processing solutions, including checkout flows, subscriptions, and webhook handling for various payment processors like Stripe and PayPal.
---

# Payment Integration

Integrate payment processors securely and efficiently.

## When to use

- Payment gateway integration
- Subscription billing
- Checkout flows
- Webhook handling
- PCI compliance

## Focus Areas

- Stripe, PayPal, and Square API integration
- Checkout flows and payment forms
- Subscription billing and recurring payments
- Webhook handling for payment events
- PCI compliance and security best practices
- Payment error handling and retry logic

## Approach

1. **Security First**: Never log sensitive card data.
2. **Idempotency**: Implement idempotency for all payment operations.
3. **Edge Cases**: Handle all edge cases (failed payments, disputes, refunds).
4. **Testing**: Start in test mode with a clear migration path to production.
5. **Webhook Handling**: Comprehensive handling for asynchronous events.

## Webhook Security & Idempotency

- **Signature Verification**: Always verify webhook signatures using official SDK libraries (e.g., Stripe, PayPal). Never process unverified webhooks.
- **Raw Body Preservation**: Do not modify the webhook request body before verification; JSON middleware can break signature validation.
- **Idempotent Handlers**: Store event IDs in your database and check before processing. Webhooks may retry on failure, and providers do not guarantee single delivery.
- **Quick Response**: Return a `2xx` status within 200ms, before performing expensive operations (like database writes). Timeouts can trigger retries and duplicate processing.
- **Server Validation**: Always re-fetch payment status from the provider API. Do not trust webhook payloads or client responses alone.

## PCI Compliance Essentials

- **Tokenization**: Use tokenization APIs (e.g., Stripe Elements, PayPal SDK) that handle card data in the provider's iframe. Never store, process, or transmit raw card numbers.
- **Server-Side Validation**: All payment verification must occur server-side via direct API calls to the payment provider.
- **Environment Separation**: Ensure test credentials fail in production. Misconfigured gateways may accept test cards on live sites.

## Example Implementations

### Stripe Integration

#### Setup

```javascript
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Create payment intent
async function createPayment(amount, currency = "usd") {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: amount * 100, // cents
    currency,
    automatic_payment_methods: { enabled: true },
    metadata: { order_id: "order_123" },
  });

  return {
    clientSecret: paymentIntent.client_secret,
    id: paymentIntent.id,
  };
}

// Create subscription
async function createSubscription(customerId, priceId) {
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: "default_incomplete",
    expand: ["latest_invoice.payment_intent"],
  });

  return {
    subscriptionId: subscription.id,
    clientSecret: subscription.latest_invoice.payment_intent.client_secret,
  };
}

// Cancel subscription
async function cancelSubscription(subscriptionId) {
  return await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });
}
```

### Webhook Handling

```javascript
import { buffer } from "micro";

export async function handleWebhook(req, res) {
  const sig = req.headers["stripe-signature"];
  const body = await buffer(req);

  let event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET,
    );
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case "payment_intent.succeeded":
      await handlePaymentSuccess(event.data.object);
      break;
    case "payment_intent.payment_failed":
      await handlePaymentFailure(event.data.object);
      break;
    case "customer.subscription.deleted":
      await handleSubscriptionCanceled(event.data.object);
      break;
  }

  res.json({ received: true });
}
```

## Database Schema

```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    stripe_payment_id VARCHAR(255) UNIQUE,
    amount NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```