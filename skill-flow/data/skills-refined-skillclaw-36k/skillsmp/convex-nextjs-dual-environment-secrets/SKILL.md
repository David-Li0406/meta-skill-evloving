---
name: convex-nextjs-dual-environment-secrets
description: |
  Fix for "Unauthorized" errors in Convex mutations called from Next.js API routes when using
  internal API secrets for authentication. Use when: (1) Convex mutation throws "Unauthorized"
  even though secret is set in .env.local, (2) webhook handlers fail with 500 status and
  "Unauthorized" in Convex function, (3) internal API calls work locally in Next.js but fail
  when calling Convex mutations. The fix is to set the secret in BOTH Next.js .env.local AND
  Convex environment variables.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# Convex + Next.js Dual-Environment Secret Configuration

## Problem

When using Convex with Next.js and internal API authentication (e.g., for webhook handlers),
setting `INTERNAL_API_SECRET` only in `.env.local` is insufficient. Convex mutations that
verify this secret will fail with "Unauthorized" because Convex runs in a separate environment
and doesn't have access to Next.js environment variables.

## Context / Trigger Conditions

- Webhook handler returns 500 with "Unauthorized" error
- Error stack trace points to a Convex mutation/query that checks `process.env.INTERNAL_API_SECRET`
- The secret IS correctly set in `.env.local` for Next.js
- Next.js API route successfully reads the secret and passes it to Convex
- Convex mutation fails because `process.env.INTERNAL_API_SECRET` is undefined in Convex runtime

Example error:
```
Webhook error: Error: [Request ID: xxx] Server Error
Uncaught Error: Unauthorized
    at handler (../convex/webhooks.ts:40:21)
```

## Solution

Set the secret in BOTH environments:

1. **Next.js (.env.local)**:
   ```
   INTERNAL_API_SECRET=your-secret-value
   ```

2. **Convex environment**:
   ```bash
   npx convex env set INTERNAL_API_SECRET "your-secret-value"
   ```

The Next.js API route reads the secret from `.env.local`, passes it to Convex in the mutation
arguments, and Convex compares it against its own environment variable.

## Verification

After setting the Convex environment variable:

1. Trigger the webhook again
2. Check the dev server logs - should show `200` instead of `500`
3. Verify the mutation/query completes successfully

```bash
# Verify the secret is set in Convex
npx convex env list | grep INTERNAL_API_SECRET
```

## Example

**Convex mutation that verifies the secret:**
```typescript
// convex/webhooks.ts
export const markEventProcessed = mutation({
  args: {
    eventId: v.string(),
    provider: v.string(),
    secret: v.string(),  // Passed from Next.js
  },
  handler: async (ctx, args) => {
    const expectedSecret = process.env.INTERNAL_API_SECRET;  // Read from Convex env
    if (!expectedSecret || args.secret !== expectedSecret) {
      throw new Error("Unauthorized");
    }
    // ... rest of handler
  },
});
```

**Next.js API route that calls it:**
```typescript
// app/api/webhook/route.ts
const internalSecret = process.env.INTERNAL_API_SECRET;  // Read from .env.local

await client.mutation(api.webhooks.markEventProcessed, {
  eventId,
  provider: "polar",
  eventType: event.type,
  secret: internalSecret,  // Pass to Convex
});
```

## Notes

- This pattern applies to ANY shared secret between Next.js and Convex, not just webhooks
- The same issue occurs with `BETTER_AUTH_SECRET`, `SITE_URL`, or any env var that Convex
  needs to access
- Convex environment variables can be set via CLI (`npx convex env set`) or the Convex dashboard
- In production, ensure both Vercel/hosting environment AND Convex production have the secrets
- Use `npx convex env list` to audit which variables are set in Convex

## Related Environment Variables to Check

When setting up Convex + Next.js with authentication/webhooks, ensure these are set in
BOTH environments:

| Variable | Next.js | Convex |
|----------|---------|--------|
| `INTERNAL_API_SECRET` | `.env.local` | `npx convex env set` |
| `BETTER_AUTH_SECRET` | `.env.local` | `npx convex env set` |
| `SITE_URL` | `.env.local` | `npx convex env set` |
| `REQUIRE_EMAIL_VERIFICATION` | `.env.local` | `npx convex env set` |
