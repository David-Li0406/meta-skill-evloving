---
name: plaid-fintech
description: Use this skill for expert patterns in Plaid API integration, including Link token flows, transactions sync, identity verification, ACH authentication, balance checks, webhook handling, and fintech compliance best practices.
---

# Plaid Fintech

## Patterns

### Link Token Creation and Exchange

Create a `link_token` for Plaid Link and exchange `public_token` for `access_token`. Link tokens are short-lived and one-time use, while access tokens do not expire but may need updating when users change passwords.

### Transactions Sync

Utilize `/transactions/sync` for incremental transaction updates, which is more efficient than `/transactions/get`. Handle webhooks for real-time updates instead of polling.

### Item Error Handling and Update Mode

Manage `ITEM_LOGIN_REQUIRED` errors by guiding users through Link update mode. Listen for `PENDING_DISCONNECT` webhooks to proactively prompt users.

## Anti-Patterns

- ❌ Storing access tokens in plain text
- ❌ Polling instead of using webhooks
- ❌ Ignoring item errors

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |

## Core Products

| Product | Purpose |
|---------|---------|
| **Auth** | Bank account/routing numbers for ACH |
| **Transactions** | Transaction history (up to 24 months) |
| **Identity** | Verify user via bank account ownership |
| **Balance** | Real-time account balances |
| **Investments** | Holdings from investment accounts |
| **Liabilities** | Loan and credit card data |

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

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect Bank Account
    </button>
  );
}
```

### 5. Exchange Token (Server)

```typescript
// POST /api/plaid/exchange-token
export async function POST(req: Request) {
  const { public_token } = await req.json();

  const response = await client.itemPublicTokenExchange({
    public_token,
  });

  // Store access_token securely (encrypted in database)
  await db.users.update(userId, {
    plaid_access_token: response.data.access_token,
    plaid_item_id: response.data.item_id,
  });

  return Response.json({ success: true });
}
```

## Data Retrieval

### Get Auth (Account/Routing Numbers)

```typescript
const response = await client.authGet({ access_token });

const ach = response.data.numbers.ach[0];
console.log("Account:", ach.account);
console.log("Routing:", ach.routing);
```

### Get Transactions

```typescript
const response = await client.transactionsGet({
  access_token,
  start_date: "2024-01-01",
  end_date: "2024-12-31",
});

let transactions = response.data.transactions;

// Handle pagination
while (transactions.length < response.data.total_transactions) {
  const more = await client.transactionsGet({
    access_token,
    start_date: "2024-01-01",
    end_date: "2024-12-31",
    offset: transactions.length,
  });
  transactions = transactions.concat(more.data.transactions);
}
```

### Get Balance

```typescript
const response = await client.accountsBalanceGet({ access_token });

response.data.accounts.forEach((account) => {
  console.log(`${account.name}: $${account.balances.current}`);
});
```

### Get Identity

```typescript
const response = await client.identityGet({ access_token });

const owner = response.data.accounts[0].owners[0];
console.log("Name:", owner.names[0]);
console.log("Email:", owner.emails[0].data);
console.log("Phone:", owner.phone_numbers[0].data);
```

## Webhooks

### Setup Endpoint

```typescript
// POST /api/plaid/webhook
export async function POST(req: Request) {
  const { webhook_type, webhook_code, item_id } = await req.json();

  switch (webhook_type) {
    case "TRANSACTIONS":
      if (webhook_code === "DEFAULT_UPDATE") {
        // New transactions available - fetch them
        await syncTransactions(item_id);
      }
      break;

    case "ITEM":
      if (webhook_code === "ERROR") {
        // Connection issue - prompt user to re-authenticate
        await notifyUserReauth(item_id);
      }
      break;
  }

  return Response.json({ received: true });
}
```

## Security Best Practices

**DO:**
- Store access tokens encrypted in the database
- Use environment variables for credentials
- Verify webhook signatures
- Use HTTPS for all endpoints

**DON'T:**
- Expose secret keys client-side
- Log access tokens
- Store credentials in code

## Implementation Checklist

- [ ] Sign up for Plaid account
- [ ] Get client ID and secret
- [ ] Install `plaid` and `react-plaid-link`
- [ ] Set environment variables
- [ ] Create link token endpoint
- [ ] Implement token exchange endpoint
- [ ] Integrate Plaid Link on frontend
- [ ] Store access tokens securely
- [ ] Set up webhook endpoint
- [ ] Handle re-authentication errors
- [ ] Test with sandbox credentials

## Resources

- **Docs:** https://plaid.com/docs/
- **API Reference:** https://plaid.com/docs/api/
- **Quickstart:** https://github.com/plaid/quickstart