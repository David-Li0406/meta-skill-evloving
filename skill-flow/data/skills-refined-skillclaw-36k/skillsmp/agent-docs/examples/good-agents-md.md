# Example: Well-Written AGENTS.md

This example demonstrates best practices for AGENTS.md documentation.

```markdown
# components/billing/ - Agent Instructions

Stripe billing integration components for Zo Computer. Handles subscriptions, payment methods, and credit purchases.

## Commands

\`\`\`bash
# From ts-packages/web
pnpm test components/billing
pnpm typecheck
\`\`\`

## Key Components

| Component | Purpose |
|-----------|---------|
| `PlanCard` | Displays plan details with pricing |
| `SubscriptionModal` | Stripe checkout modal |
| `PaymentMethodForm` | Add/update payment methods |
| `CreditPurchaseDialog` | One-time credit purchases |

## usePlanSubscribe Hook

Primary hook for managing subscription flow:

\`\`\`typescript
import { usePlanSubscribe } from "@/components/billing/use-plan-subscribe";

const { beginSubscribe, modalUI, loadingPlan, footerStatus } = usePlanSubscribe({
  isDev: boolean,              // Use Stripe test mode
  isFreePlan: boolean,         // Current plan status
  discountCode?: string,       // Optional promo code
  plansList?: Plan[],          // Available plans
});

// CRITICAL: Must render modalUI in component
return (
  <>
    <button onClick={() => beginSubscribe(planId)}>Subscribe</button>
    {modalUI}
  </>
);
\`\`\`

**Critical:** `modalUI` must be rendered or Stripe modal won't appear.

## Plan Data Structure

\`\`\`typescript
interface Plan {
  id: string;
  name: string;
  price: number;
  interval: "month" | "year";
  features: string[];
  stripePriceId: string;
}
\`\`\`

## Stripe Integration

Uses `@stripe/stripe-js` for client-side checkout:

\`\`\`typescript
import { loadStripe } from "@stripe/stripe-js";

// Initialized in use-plan-subscribe.ts
const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY);
\`\`\`

## Payment Flow

1. User clicks subscribe button
2. `beginSubscribe(planId)` called
3. Creates Stripe checkout session via API
4. Opens Stripe modal with `modalUI`
5. On success, webhook updates subscription status
6. Modal closes, UI reflects new plan

## Testing

\`\`\`bash
# Run billing tests
pnpm test use-plan-subscribe.test.ts

# Test with Stripe test mode
NEXT_PUBLIC_STRIPE_TEST_MODE=true pnpm dev
\`\`\`

Use Stripe test card: `4242 4242 4242 4242`

## IMPORTANT

- Never commit real Stripe keys to git
- Always use test mode in development
- Webhook secrets must match Stripe dashboard
- Price IDs differ between test and live mode

## Related Context

See also:
- `context/payment-method.tsx` - Payment method context
- `api/stripe.ts` - Server-side Stripe utilities
- `CLAUDE.md` in project root for general Stripe setup
\`\`\`

## Why This Example Is Good

✅ **Clear header** - Describes purpose immediately
✅ **Commands** - Shows how to test
✅ **Component table** - Quick reference
✅ **Hook documentation** - Complete signature with types
✅ **Code examples** - Concrete, runnable code
✅ **Critical warnings** - Highlights gotchas (modalUI rendering)
✅ **Type definitions** - Shows data structures
✅ **Integration details** - Explains Stripe setup
✅ **Testing guidance** - How to test with Stripe test mode
✅ **Security warnings** - Don't commit keys
✅ **Cross-references** - Links to related files
