---
name: shopify-billing
description: Use this skill when implementing Shopify's Billing API to enable app monetization through subscriptions and one-time charges.
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
      name: "<subscription_name>",
      returnUrl: "<return_url>",
      lineItems: [{
        plan: {
          appRecurringPricingDetails: {
            price: { amount: <amount>, currencyCode: "<currency_code>" },
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
    name: "<purchase_name>",
    returnUrl: "<return_url>",
    price: { amount: <amount>, currencyCode: "<currency_code>" }
  }
});
```

## 3. Checking Active Subscriptions

To gate features, check the `currentAppInstallation` for active subscriptions.

```javascript
/* app/shopify.server.ts (billing config) */
export const billing = {
  "<plan_name>": {
    amount: <amount>,
    currencyCode: "<currency_code>",
    interval: "EVERY_30_DAYS",
  },
};

/* Checking in loader */
const { billing } = await authenticate.admin(request);
const billingCheck = await billing.require({
  plans: ["<plan_name>"],
  isTest: true, // Use true for development stores
  onFailure: async () => billing.request({ plan: "<plan_name>", isTest: true }),
});
const subscription = billingCheck.appSubscriptions[0];
```

### Manual Query (if not using billing helper)

```graphql
query {
  currentAppInstallation {
    activeSubscriptions {
      id
      name
      status
      lineItems {
        plan {
          pricingDetails {
            ... on AppRecurringPricing {
              price { amount currencyCode }
            }
          }
        }
      }
    }
  }
}
```

## 4. Best Practices

-   **Test Mode**: Always set `test: true` (or `isTest`) when developing. Test charges do not bill the merchant.
-   **Confirmation URL**: You MUST redirect the user to the `confirmationUrl` returned by the mutation. The charge is not active until they approve it.
-   **Webhooks**: Listen for `app_subscriptions/update` to handle cancellations or status changes in real-time.