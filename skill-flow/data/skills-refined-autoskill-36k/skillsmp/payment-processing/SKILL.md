---
name: payment-processing
description: "Use when implementing payment flows with Stripe or Polar. Covers checkout integration, webhooks, subscriptions, and error handling."
---

# Payment Processing

## Overview

Payment integration patterns for Stripe and Polar. Covers checkout flows, webhook handling, subscription management, and error handling for secure, reliable payment processing.

## When to Use

- Implementing checkout flow
- Setting up Stripe/Polar integration
- Handling payment webhooks
- Managing subscriptions
- Processing refunds

## Quick Reference

| Component | Key Considerations |
|-----------|-------------------|
| **Checkout** | Server-side session creation, redirect handling |
| **Webhooks** | Signature verification, idempotency, retry handling |
| **Subscriptions** | Lifecycle events, cancellation, upgrades |
| **Errors** | Graceful degradation, user messaging, logging |

---

## Stripe Integration

### Checkout Session (Server)

```typescript
// app/api/checkout/route.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export async function POST(req: Request) {
  const { priceId, userId } = await req.json();

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription', // or 'payment' for one-time
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
      customer_email: user.email, // Pre-fill email
      metadata: {
        userId, // Track in your system
      },
    });

    return Response.json({ url: session.url });
  } catch (error) {
    console.error('Checkout error:', error);
    return Response.json(
      { error: 'Failed to create checkout session' },
      { status: 500 }
    );
  }
}
```

### Client Redirect

```typescript
// components/CheckoutButton.tsx
async function handleCheckout(priceId: string) {
  setLoading(true);
  try {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priceId }),
    });

    const { url, error } = await res.json();
    if (error) throw new Error(error);

    window.location.href = url; // Redirect to Stripe
  } catch (error) {
    toast.error('Failed to start checkout');
  } finally {
    setLoading(false);
  }
}
```

---

## Webhook Handling

### Webhook Endpoint

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;

  let event: Stripe.Event;

  // 1. Verify signature (CRITICAL)
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed');
    return Response.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // 2. Handle event (with idempotency)
  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object);
        break;

      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        await handleSubscriptionChange(event.data.object);
        break;

      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data.object);
        break;

      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return Response.json({ received: true });
  } catch (error) {
    console.error('Webhook handler error:', error);
    return Response.json({ error: 'Handler failed' }, { status: 500 });
  }
}
```

### Webhook Handlers

```typescript
async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  const subscriptionId = session.subscription as string;

  // Idempotency check
  const existing = await db.subscription.findUnique({
    where: { stripeSubscriptionId: subscriptionId }
  });
  if (existing) return; // Already processed

  await db.subscription.create({
    data: {
      userId,
      stripeSubscriptionId: subscriptionId,
      stripeCustomerId: session.customer as string,
      status: 'active',
    },
  });
}

async function handleSubscriptionCanceled(subscription: Stripe.Subscription) {
  await db.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: { status: 'canceled', canceledAt: new Date() },
  });
}
```

---

## Polar Integration

### Setup

```typescript
// lib/polar.ts
import { Polar } from '@polar-sh/sdk';

export const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
});
```

### Checkout with Polar

```typescript
// app/api/polar/checkout/route.ts
export async function POST(req: Request) {
  const { productId, userId } = await req.json();

  const checkout = await polar.checkouts.create({
    productId,
    successUrl: `${process.env.NEXT_PUBLIC_URL}/success`,
    metadata: { userId },
  });

  return Response.json({ url: checkout.url });
}
```

### Polar Webhooks

```typescript
// app/api/webhooks/polar/route.ts
import { validateWebhookSignature } from '@polar-sh/sdk/webhooks';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('webhook-signature')!;

  // Verify signature
  const isValid = validateWebhookSignature(
    body,
    signature,
    process.env.POLAR_WEBHOOK_SECRET!
  );

  if (!isValid) {
    return Response.json({ error: 'Invalid signature' }, { status: 400 });
  }

  const event = JSON.parse(body);

  switch (event.type) {
    case 'subscription.created':
      await handlePolarSubscription(event.data);
      break;
    case 'subscription.canceled':
      await handlePolarCancellation(event.data);
      break;
  }

  return Response.json({ received: true });
}
```

---

## Error Handling

### Payment Errors

```typescript
const STRIPE_ERROR_MESSAGES: Record<string, string> = {
  card_declined: 'Your card was declined. Please try another card.',
  insufficient_funds: 'Insufficient funds. Please try another card.',
  expired_card: 'Your card has expired. Please update your payment method.',
  incorrect_cvc: 'Incorrect CVC. Please check and try again.',
  processing_error: 'Processing error. Please try again.',
  default: 'Payment failed. Please try again or contact support.',
};

function getPaymentErrorMessage(error: Stripe.StripeError): string {
  return STRIPE_ERROR_MESSAGES[error.code ?? 'default']
    ?? STRIPE_ERROR_MESSAGES.default;
}
```

### Graceful Degradation

```typescript
async function createCheckout(priceId: string) {
  try {
    const session = await stripe.checkout.sessions.create({...});
    return { success: true, url: session.url };
  } catch (error) {
    // Log for debugging
    console.error('Stripe checkout failed:', error);

    // Return user-friendly error
    return {
      success: false,
      error: 'Unable to process payment. Please try again later.',
    };
  }
}
```

---

## Security Checklist

- [ ] Webhook signatures verified
- [ ] Secret keys in environment variables only
- [ ] HTTPS for all payment endpoints
- [ ] Idempotency keys for critical operations
- [ ] No sensitive data in client-side code
- [ ] PCI compliance requirements met
- [ ] Rate limiting on payment endpoints

---

## Common Patterns

### Subscription Status Check

```typescript
async function hasActiveSubscription(userId: string): Promise<boolean> {
  const sub = await db.subscription.findFirst({
    where: {
      userId,
      status: { in: ['active', 'trialing'] },
    },
  });
  return !!sub;
}
```

### Customer Portal

```typescript
// Allow users to manage subscription
const portalSession = await stripe.billingPortal.sessions.create({
  customer: stripeCustomerId,
  return_url: `${process.env.NEXT_PUBLIC_URL}/account`,
});

return Response.json({ url: portalSession.url });
```

---

## Red Flags - STOP

**Never:**
- Log full card numbers or CVCs
- Store payment secrets in code
- Skip webhook signature verification
- Trust client-side payment data
- Process payments without idempotency

**Always:**
- Verify webhook signatures
- Use server-side session creation
- Handle all webhook event types
- Log payment events for debugging
- Test with Stripe/Polar test mode

---

## Integration

**Related skills:** api-design, nextjs-patterns
**Testing:** Use Stripe CLI for local webhook testing
