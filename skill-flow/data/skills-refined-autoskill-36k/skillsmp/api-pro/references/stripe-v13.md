# Stripe SDK v13+: Modern Financial Engineering

Optimized patterns for the latest Stripe SDK, focusing on auto-pagination, expanded objects, and type-safe financial operations.

## Auto-Pagination (v13+)

No more manual looping through cursors. The v13 SDK provides native async iterators for all list resources.

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-10-14', // 2026 Recommended Version
});

async function processAllCustomers() {
  const customers = stripe.customers.list({
    limit: 100,
  });

  // Native auto-pagination handles the cursor internally
  for await (const customer of customers) {
    await syncToLocalDB(customer);
  }
}
```

## Expanded Objects & Depth Control

The `expand` parameter is now more robust, allowing for deep nesting with full TypeScript support.

```typescript
const paymentIntent = await stripe.paymentIntents.retrieve('pi_123', {
  expand: ['customer', 'payment_method', 'latest_charge.balance_transaction'],
});

// paymentIntent.customer is now typed as a Customer object instead of just an ID
if (typeof paymentIntent.customer !== 'string') {
  console.log(paymentIntent.customer?.email);
}
```

## Robust Webhook Handling

Stripe v13 introduces `webhookEndpoints` management and improved signature verification for Edge environments.

```typescript
import { headers } from 'next/headers';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object as Stripe.Checkout.Session;
        await handleSuccessfulCheckout(session);
        break;
      // Handle other events
    }

    return new Response(JSON.stringify({ received: true }), { status: 200 });
  } catch (err: any) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }
}
```

## Financial Standards (2026)
- **Idempotency**: Always use `idempotencyKey` for mutations to prevent double-charging.
- **Connect Platforms**: Use `stripeAccount` header for multi-tenant integrations.
- **Reporting**: Utilize the `reporting` API for autonomous financial reconciliation.

## Common Pitfalls
- **API Version Drift**: Hard-code the `apiVersion` in the client constructor to avoid breaking changes when updating the dashboard settings.
- **Memory Leaks**: When using auto-pagination on very large sets (>100k), ensure you are not accumulating objects in an array.

*Updated: January 22, 2026 - 15:18
