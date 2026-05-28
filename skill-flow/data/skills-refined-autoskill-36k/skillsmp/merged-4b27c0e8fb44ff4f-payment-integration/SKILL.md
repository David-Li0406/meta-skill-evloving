---
name: payment-integration
description: Use this skill when implementing secure payment processing, including checkout flows, subscriptions, and webhook handling with Stripe, PayPal, and other payment processors.
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

1. **Security first** - never log sensitive card data.
2. **Implement idempotency** for all payment operations.
3. **Handle all edge cases** (failed payments, disputes, refunds).
4. **Test mode first**, with a clear migration path to production.
5. **Comprehensive webhook handling** for async events.

## Stripe Integration

### Setup

```javascript
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Create payment intent
async function createPayment(amount, currency = "usd") {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: amount * 100, // cents
    currency,
    automatic_payment_methods: { enabled: true },
    metadata: { order_id: "<order_id>" },
  });

  return {
    clientSecret: paymentIntent.client_secret,
    id: paymentIntent.id,
  };
}
```

### Subscriptions

```javascript
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

### Webhooks

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
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'usd',
    status VARCHAR(50) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    stripe_subscription_id VARCHAR(255) UNIQUE,
    stripe_customer_id VARCHAR(255),
    plan VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    canceled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
```

## Security Checklist

- [ ] Never log full card numbers
- [ ] Use HTTPS everywhere
- [ ] Validate webhook signatures
- [ ] Implement idempotency keys
- [ ] Store only necessary data
- [ ] Use Stripe.js for card collection
- [ ] Handle errors gracefully

## Common Failures

**Real-world examples:**
- Payment processor collapse during traffic spikes leading to webhook queue backups.
- Out-of-order webhooks breaking functions due to lack of idempotency.
- Malicious price manipulation on unencrypted payment buttons.
- Test cards accepted on live sites due to misconfiguration.
- Skipped webhook signature verification leading to system flooding with malicious requests.

## Output

- Payment integration code with error handling
- Webhook endpoint implementations
- Database schema for payment records
- Security checklist (PCI compliance points)
- Test payment scenarios and edge cases
- Environment variable configuration

Always use official SDKs. Include both server-side and client-side code where needed.