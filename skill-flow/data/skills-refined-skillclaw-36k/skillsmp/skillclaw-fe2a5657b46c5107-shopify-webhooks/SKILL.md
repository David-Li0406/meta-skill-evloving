---
name: shopify-webhooks
description: Use this skill when you need to set up webhook subscriptions, verify authentic requests, or handle event payloads from Shopify.
---

# Shopify Webhooks Skill

Webhooks are the preferred way to stay in sync with Shopify data. They allow your app to receive real-time notifications when events occur in a shop (e.g., `orders/create`, `app/uninstalled`).

## 1. Verification (CRITICAL)

**ALL** webhook requests must be verified to ensure they came from Shopify.

### HMAC Verification

Shopify includes an `X-Shopify-Hmac-Sha256` header in every webhook request. This is a base64-encoded HMAC-SHA256 digest of the request body, using your **Client Secret** (API Secret Key) as the signing key.

> [!IMPORTANT]
> Always use the **raw request body** (Buffer) for verification. Parsed JSON bodies may have subtle differences that cause verification to fail.

#### Node.js Example (Generic)

```javascript
const crypto = require('crypto');

function verifyWebhook(rawBody, hmacHeader, apiSecret) {
  const digest = crypto
    .createHmac('sha256', apiSecret)
    .update(rawBody, 'utf8')
    .digest('base64');

  return crypto.timingSafeEqual(
    Buffer.from(digest),
    Buffer.from(hmacHeader)
  );
}
```

#### Remix / Shopify App Template (Recommended)

If using `@shopify/shopify-app-remix`, verification is handled automatically by the `authenticate.webhook` helper.

```typescript
/* app/routes/webhooks.tsx */
import { authenticate } from "../shopify.server";

export const action = async ({ request }) => {
  const { topic, shop, session, admin, payload } = await authenticate.webhook(request);

  if (!admin) {
    // The webhook request was not valid.
    return new Response();
  }

  switch (topic) {
    case "APP_UNINSTALLED":
      if (session) {
        await db.session.deleteMany({ where: { shop } });
      }
      break;
    case "ORDERS_CREATE":
      console.log(`Order created: ${payload.id}`);
      break;
  }

  return new Response();
};
```

## 2. Registration

### App-specific Webhooks (Recommended)

These are configured in `shopify.app.toml`. They are automatically registered when the app is deployed and are easier to manage. Best for topics that apply to the app in general (e.g., `app/uninstalled`).

```toml
[webhooks]
api_version = "2025-10"

  [[webhooks.subscriptions]]
  topics = [ "app/uninstalled", "orders/create" ]
  uri = "/webhooks"
```