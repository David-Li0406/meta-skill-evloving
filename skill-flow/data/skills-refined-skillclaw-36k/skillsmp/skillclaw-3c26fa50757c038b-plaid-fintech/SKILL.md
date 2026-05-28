---
name: plaid-fintech
description: Use this skill when integrating with the Plaid API for bank account linking, transactions, identity verification, and compliance best practices in fintech applications.
---

# Plaid Fintech Integration

## Patterns

### Link Token Creation and Exchange

1. Create a `link_token` for Plaid Link.
2. Exchange the `public_token` for an `access_token`.
   - Note: Link tokens are short-lived and one-time use. Access tokens do not expire but may need updating if users change their passwords.

### Transactions Sync

- Use the `/transactions/sync` endpoint for incremental transaction updates, which is more efficient than `/transactions/get`.
- Handle webhooks for real-time updates instead of relying on polling.

### Item Error Handling and Update Mode

- Handle `ITEM_LOGIN_REQUIRED` errors by guiding users through the Link update mode.
- Listen for the `PENDING_DISCONNECT` webhook to proactively prompt users for action.

## Anti-Patterns

- ❌ Storing access tokens in plain text.
- ❌ Polling instead of using webhooks.
- ❌ Ignoring item errors.

## Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See documentation for resolution. |
| Issue | high | See documentation for resolution. |
| Issue | medium | See documentation for resolution. |

## Quick Start

### 1. Install SDK

```bash
npm install plaid react-plaid-link
```

### 2. Create Plaid Client

```typescript
import { Configuration, PlaidApi, PlaidEnvironments } from "plaid";

const client = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments.sandbox,
    baseOptions: {
      headers: {
        "PLAID-CLIENT-ID": process.env.PLAID_CLIENT_ID,
        "PLAID-SECRET": process.env.PLAID_SECRET,
      },
    },
  })
);
```

### 3. Create Link Token (Server)

```typescript
// POST /api/plaid/create-link-token
export async function POST(req: Request) {
  const response = await client.linkTokenCreate({
    user: { client_user_id: userId },
    client_name: "Your App",
    products: ["auth", "transactions"],
    country_codes: ["US"],
    language: "en",
  });

  return Response.json({ link_token: response.data.link_token });
}
```

### 4. Plaid Link (Client)

```tsx
import { usePlaidLink } from "react-plaid-link";

function ConnectBank({ linkToken }) {
  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      // Exchange for access_token on server
      await fetch("/api/plaid/exchange-token", {
        method: "POST",
        body: JSON.stringify({ public_token }),
      });
    },
  });

  return <button onClick={open} disabled={!ready}>Connect a Bank Account</button>;
}
```