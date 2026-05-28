---
name: shopify-billing
description: Use this skill when you need to implement Shopify's Billing API for app monetization through subscriptions and one-time charges.
---

# Shopify Billing Skill

The Billing API allows you to charge merchants for your app using recurring subscriptions or one-time purchases.

> [!IMPORTANT]
> **GraphQL Only**: The REST Billing API is deprecated. Always use the GraphQL Admin API for billing operations.

## 1. Recurring Subscriptions (`appSubscriptionCreate`)

Use this mutation to create a recurring charge (e.g., monthly plan).

### Example (Remix / Shopify App Template)

```javascript
/* app/routes/app.upgrade.tsx */
import { authenticate } from "../shopify.server";

export const action = async ({ request }) => {
  const { admin } = await authenticate.admin(request);
  const shop = await admin.graphql(`
    mutation AppSubscriptionCreate($name: String!, $lineItems: [AppSubscriptionLineItemInput!]!, $returnUrl: URL!) {
      appSubscriptionCreate(name: $name, returnUrl: $returnUrl, lineItems: $lineItems) {
        userErrors {
          field
          message
        }
        appSubscription {
          id
        }
        confirmationUrl
      }
    }
  `,
  {
    variables: {
      name: "Pro Plan",
      returnUrl: "https://myapp.com/app",
      lineItems: [{
        plan: {
          appRecurringPricingDetails: {
            price: { amount: 10.00, currencyCode: "USD" },
            interval: "EVERY_30_DAYS"
          }
        }
      }]
    }
  });

  const response = await shop.json();
  const confirmationUrl = response.data.appSubscriptionCreate.confirmationUrl;
  
  // Redirect merchant to approve charge
  return redirect(confirmationUrl);
};
```

## 2. One-Time Purchases (`appPurchaseOneTimeCreate`)

Use this mutation for non-recurring charges (e.g., specific service, lifetime access).

```javascript
const response = await admin.graphql(`
  mutation AppPurchaseOneTimeCreate($name: String!, $price: MoneyInput!, $returnUrl: URL!) {
    appPurchaseOneTimeCreate(name: $name, returnUrl: $returnUrl, price: $price) {
      userErrors { field message }
      confirmationUrl
    }
  }
`, {
  variables: {
    name: "Concierge Setup",
    returnUrl: "https://myapp.com/app",
    price: { amount: 50.00, currencyCode: "USD" }
  }
});
```

## 3. Checking Active Subscriptions

To gate features, check the `currentAppSubscription` status to ensure the merchant has an active subscription.