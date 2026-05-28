---
name: stripe-integration
description: Use this skill when implementing Stripe payment processing for secure, PCI-compliant payment flows, including checkout, subscriptions, webhooks, and customer management.
---

# Stripe Integration

This skill guides the implementation of Stripe payment processing, ensuring robust, PCI-compliant payment flows for applications.

## When to Use This Skill

Use this skill when:
- Integrating payment processing in web or mobile applications
- Setting up subscription billing systems
- Handling one-time payments and recurring charges
- Processing refunds and disputes
- Managing customer payment methods
- Implementing Strong Customer Authentication (SCA) for European payments
- Building marketplace payment flows with Stripe Connect

## Core Principles

### Security
- Never expose secret keys client-side
- Always use HTTPS in production
- Validate webhook signatures
- Use Stripe's client-side libraries for card handling

### User Experience
- Provide clear error messages and feedback
- Show loading states during payment processing
- Send email confirmations for transactions

## Implementation Workflow

### 1. Environment Setup

**Required Credentials**:
```
STRIPE_PUBLISHABLE_KEY_TEST=pk_test_...
STRIPE_SECRET_KEY_TEST=sk_test_...
STRIPE_WEBHOOK_SECRET_TEST=whsec_...

STRIPE_PUBLISHABLE_KEY_PROD=pk_live_...
STRIPE_SECRET_KEY_PROD=sk_live_...
STRIPE_WEBHOOK_SECRET_PROD=whsec_...
```

**Installation**:
```bash
# Node.js
npm install stripe @stripe/stripe-js

# Python
pip install stripe
```

### 2. Payment Flows

**Checkout Session (Hosted)**:
- Use Stripe-hosted payment pages for minimal PCI compliance burden.

**Payment Intents (Custom UI)**:
- Full control over payment UI, requires Stripe.js for PCI compliance.

### 3. Subscription Implementation

**Create Subscription**:
```javascript
async function createSubscription(customerId, priceId) {
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    payment_settings: {
      save_default_payment_method: 'on_subscription'
    },
    expand: ['latest_invoice.payment_intent']
  });

  return {
    subscriptionId: subscription.id,
    clientSecret: subscription.latest_invoice.payment_intent.client_secret
  };
}
```

### 4. Webhook Configuration

**Critical Events to Handle**:
- `payment_intent.succeeded`: Payment completed
- `payment_intent.payment_failed`: Payment failed
- `customer.subscription.updated`: Subscription changed
- `customer.subscription.deleted`: Subscription canceled

**Webhook Endpoint Example**:
```javascript
app.post('/webhook', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object);
      break;
    case 'payment_intent.payment_failed':
      await handlePaymentFailure(event.data.object);
      break;
    // Add more cases as needed
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({received: true});
});
```

### 5. Customer Management

**Create Customer**:
```javascript
const customer = await stripe.customers.create({
  email: user.email,
  name: user.name,
  metadata: {
    userId: user.id
  }
});
```

**Attach Payment Method**:
```javascript
await stripe.paymentMethods.attach(pm_id, { customer: customerId });
await stripe.customers.update(customerId, {
  invoice_settings: {
    default_payment_method: pm_id
  }
});
```

### 6. Testing

**Test Mode**:
- Use test keys (pk_test_, sk_test_)
- Test card numbers:
  - Success: `4242 4242 4242 4242`
  - Declined: `4000 0000 0000 0002`

### 7. Error Handling

**Common Errors to Handle**:
```javascript
try {
  const charge = await stripe.charges.create({...});
} catch (error) {
  console.error('Error:', error.message);
}
```

## Checklist for Production

Before going live:
- [ ] Use live API keys
- [ ] Enable HTTPS
- [ ] Configure webhook endpoint in Stripe Dashboard
- [ ] Implement webhook signature verification
- [ ] Handle all critical events
- [ ] Implement error handling for all payment flows

## Resources

- [Stripe Official Docs](https://stripe.com/docs)
- [Testing with Stripe](https://stripe.com/docs/testing)
- [Webhook Handling](https://stripe.com/docs/webhooks)

## Best Practices

1. Always use webhooks for payment confirmation.
2. Handle webhook events idempotently.
3. Test thoroughly with test keys before going live.
4. Monitor payment success rates and errors.