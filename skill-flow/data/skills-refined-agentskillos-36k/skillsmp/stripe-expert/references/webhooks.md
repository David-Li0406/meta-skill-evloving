# Webhook Engineering (Stripe 2026)

Webhooks are the only reliable way to fulfill orders and update subscription states.

## 1. Security & Verification
Always verify the signature using your `STRIPE_WEBHOOK_SECRET`.

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from "next/headers";
import { NextResponse } from "next/server";
import Stripe from "stripe";

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get("Stripe-Signature") as string;
  
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  // Handle events...
}
```

## 2. Fulfillment Patterns
- **checkout.session.completed**: Order paid.
- **invoice.payment_succeeded**: Subscription recurring payment.
- **customer.subscription.deleted**: Subscription canceled.

## 3. Idempotency Check
Event IDs are unique. Store handled event IDs in your database to prevent processing the same event twice.

```typescript
const alreadyHandled = await db.processedEvents.findUnique({ where: { id: event.id } });
if (alreadyHandled) return NextResponse.json({ received: true });
```

---
*Updated: January 23, 2026*
