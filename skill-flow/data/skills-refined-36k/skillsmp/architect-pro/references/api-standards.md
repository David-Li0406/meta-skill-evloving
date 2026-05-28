# API Standards & Integration (2026 Edition)

Modern API design focuses on **developer experience (DX)**, **automatic resilience**, and **efficient data fetching**. This guide covers the **Stripe SDK v13+** standards and general API best practices.

## 💳 Stripe SDK v13+ Standards
Stripe's 2026 SDK has moved toward full TypeScript-first design with built-in auto-pagination and deeper object expansion.

### 🔄 Auto-Pagination
No more manual `starting_after` loops. The v13+ SDK provides an async iterator for all list operations.

```typescript
// src/infrastructure/stripe/customer-service.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-12-01', // Target late 2025/2026 API
});

export async function getAllActiveCustomers() {
  const customers = [];
  // Auto-pagination in v13+
  for await (const customer of stripe.customers.list({ limit: 100 })) {
    if (!customer.deleted) {
      customers.push(customer);
    }
  }
  return customers;
}
```

### 📦 Expanded Objects
Request deeply nested data in a single call using the `expand` parameter, but be mindful of performance.

```typescript
const session = await stripe.checkout.sessions.retrieve(
  'cs_test_...',
  {
    expand: ['line_items', 'payment_intent.payment_method', 'subscription'],
  }
);
```

## 🏗️ Robust API Architecture

### 1. Error Handling & Idempotency
Always use idempotency keys for POST requests that modify state (charges, refunds, creates).

```typescript
const myCharge = await stripe.charges.create(
  {
    amount: 2000,
    currency: 'usd',
    source: 'tok_visa',
  },
  {
    idempotencyKey: 'user_unique_action_id_12345',
  }
);
```

### 2. Webhook Handling
Use a robust webhook handler that verifies signatures and handles retries gracefully.

```typescript
// src/app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe';
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
    
    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':
        // Handle logic
        break;
      default:
        console.log(`Unhandled event type ${event.type}`);
    }
  } catch (err) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }

  return new Response(null, { status: 200 });
}
```

## 🚫 Common Pitfalls
1. **Ignoring Rate Limits**: Even with auto-pagination, heavy bursts can trigger 429s. Implement exponential backoff.
2. **Synchronous Webhooks**: Never perform long-running tasks (like generating a PDF) inside a webhook handler. Queue the task and return 200 OK immediately.
3. **Hardcoding Version**: Always pin your API version to prevent breaking changes when the vendor updates their API.

*Updated: January 22, 2026 - 15:20*
