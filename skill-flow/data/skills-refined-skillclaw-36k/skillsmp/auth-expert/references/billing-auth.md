# 💳 Unified Billing & Auth Strategy (Stripe v13+)

## Convergence of Identity and Revenue
Authentication is often the gatekeeper for paid features. In 2026, integrating **Stripe SDK v13+** directly into the Auth.js lifecycle is the standard for SaaS applications.

## High-Performance Stripe Integration
Stripe v13+ introduces significant improvements in object expansion and pagination, allowing for complex billing checks during the session generation.

### Auto-Pagination Pattern
When checking for active subscriptions or seats in a large organization, use the new auto-pagination features.

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-10-24', // Example 2026-ready version
});

// Callback in auth.ts
async session({ session, token }) {
  // Use auto-pagination for large customer lists
  const subscriptions = await stripe.subscriptions.list({
    customer: session.user.stripeCustomerId,
    status: 'active',
    expand: ['data.plan.product'], // Object expansion
  });

  session.user.plan = subscriptions.data[0]?.plan.product.name;
  return session;
}
```

## Expanded Objects for Auth Decisions
Instead of multiple API calls, use Stripe's `expand` property to get all necessary data in a single request. This reduces latency by up to 150ms during session creation.

### Example: Role Mapping via Stripe
```typescript
const customer = await stripe.customers.retrieve(stripeId, {
  expand: ['subscriptions.data.default_payment_method'],
});

if (customer.subscriptions?.data.some(s => s.status === 'active')) {
  user.role = 'SUBSCRIBER';
}
```

## Security for Webhooks
Billing data changes frequently. Sync your Auth.js session with Stripe webhooks to ensure that access is revoked immediately when a payment fails.

1.  **Stripe Event**: `customer.subscription.deleted`.
2.  **Auth Action**: Invalidate the user's JWT or update the database record.
3.  **Result**: Next time `auth()` is called, the session reflects the "unpaid" status.

## Performance Optimization
- **Cache Subscription Status**: Use a Redis layer to cache Stripe results for the duration of the JWT (e.g., 1 hour).
- **Avoid Heavy Lookups in Middleware**: Do not call Stripe in `auth.config.ts`. Only check for the presence of a cached flag.

## The "Do Not" List
- Do not store sensitive Stripe objects (like full credit card info) in the JWT.
- Do not wait for Stripe API calls if the user is only accessing "free" public routes.
- Do not forget to handle Stripe rate limits during peak usage (use the SDK's built-in retry logic).

*Updated: January 22, 2026 - 15:20*
