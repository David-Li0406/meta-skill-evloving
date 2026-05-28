---
name: polar-sdk-cancel-subscription
description: |
  Fix for Polar SDK subscription cancellation. Use when: (1) TypeScript error "Property 'cancel'
  does not exist on type 'Subscriptions'", (2) trying to cancel a Polar subscription via SDK,
  (3) build failure with polar.subscriptions.cancel(). The correct method is revoke() not cancel().
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Polar SDK Subscription Cancellation

## Problem
When trying to cancel a subscription using the Polar SDK, you might try:
```typescript
await polar.subscriptions.cancel({ id: subscriptionId });
```

This causes a TypeScript/build error:
```
Type error: Property 'cancel' does not exist on type 'Subscriptions'.
```

## Context / Trigger Conditions
- TypeScript error about `cancel` not existing on `Subscriptions`
- Build failure in code that cancels Polar subscriptions
- Following outdated examples or documentation

## Solution
The correct method is `revoke()`, not `cancel()`:

```typescript
// WRONG
await polar.subscriptions.cancel({ id: subscriptionId });

// CORRECT
await polar.subscriptions.revoke({ id: subscriptionId });
```

## Full Example
```typescript
import { Polar } from "@polar-sh/sdk";

const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN,
});

export async function cancelSubscription(subscriptionId: string) {
  const result = await polar.subscriptions.revoke({
    id: subscriptionId,
  });
  return result;
}
```

## Verification
- TypeScript compiles without errors
- Subscription is canceled immediately in Polar
- Returns the revoked subscription object

## Notes
- `revoke()` cancels the subscription immediately
- For canceling at period end, use a different approach (update subscription)
- The Polar SDK also has `polar.customerPortal.subscriptions.cancel()` for customer-initiated cancellation (different use case)

## References
- Polar JS SDK docs: https://github.com/polarsource/polar-js
