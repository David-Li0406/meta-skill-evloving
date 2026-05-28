---
name: mercury-api
description: Mercury Bank API reference for accounts, transactions, and recipients. Use when working with Mercury API integration, transaction queries, or payment operations.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Mercury API Reference

Mercury Bank API reference for the finance_plugins project.

## When to Use This Skill

- Creating Mercury tool plugins
- Querying accounts and transactions
- Implementing payment operations
- Setting up Mercury OAuth/API Token auth

## API Overview

| Type | Permission | Use Case | Auth |
|------|------------|----------|------|
| **Mercury MCP** | Read-only | AI tools, monitoring | OAuth2 |
| **Mercury API** | Read/Write | Payments, transfers | API Token / OAuth2 |

## Environments

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.mercury.com` |
| Sandbox | `https://sandbox.mercury.com` |

## Authentication

### API Token
```python
headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/json;charset=utf-8"
}
```

### OAuth2
```
Authorization URL: https://mercury.com/oauth/authorize
Token URL: https://api.mercury.com/oauth/token
Scopes: read, write
```

## Key Endpoints

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/accounts` | List all accounts |
| `GET` | `/api/v1/account/{id}` | Get account details |
| `GET` | `/api/v1/account/{id}/cards` | Get account cards |
| `GET` | `/api/v1/account/{id}/statements` | Get statements |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/transactions` | List all transactions |
| `GET` | `/api/v1/account/{id}/transactions` | Account transactions |
| `GET` | `/api/v1/account/{id}/transaction/{txnId}` | Transaction details |
| `POST` | `/api/v1/account/{id}/transactions` | Create transaction |
| `PATCH` | `/api/v1/transaction/{id}` | Update transaction |

### Query Parameters (Transactions)
| Param | Type | Description |
|-------|------|-------------|
| `limit` | integer | Result limit |
| `offset` | integer | Pagination offset |
| `start` | string | Start date (YYYY-MM-DD) |
| `end` | string | End date (YYYY-MM-DD) |
| `status` | string | Status filter |
| `search` | string | Search keyword |

### Recipients
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/recipients` | List recipients |
| `GET` | `/api/v1/recipient/{id}` | Get recipient |
| `POST` | `/api/v1/recipients` | Create recipient |
| `DELETE` | `/api/v1/recipient/{id}` | Delete recipient |

### Webhooks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/webhooks` | List webhooks |
| `POST` | `/api/v1/webhooks` | Create webhook |
| `DELETE` | `/api/v1/webhook/{id}` | Delete webhook |

## Response Structures

### Account
```json
{
  "id": "uuid",
  "accountNumber": "string",
  "routingNumber": "string",
  "name": "string",
  "kind": "string",
  "type": "mercury | external | recipient",
  "status": "active | deleted | pending | archived",
  "currentBalance": 0,
  "availableBalance": 0,
  "createdAt": "2025-01-01T00:00:00Z"
}
```

### Transaction
```json
{
  "id": "uuid",
  "amount": -150.00,
  "status": "pending | sent | completed | failed",
  "counterpartyName": "Vendor Name",
  "postedAt": "2025-01-01T00:00:00Z",
  "note": "string",
  "mercuryCategory": "string"
}
```

## Current Plugin Coverage

### mercury_tools_plugin (Implemented)
- `get_accounts` - List accounts
- `get_account` - Get account details
- `get_transactions` - Query transactions

### Planned Features
| Feature | Priority | Endpoint |
|---------|----------|----------|
| Create payment | High | `POST /account/{id}/transactions` |
| Internal transfer | Medium | `POST /transfer` |
| Manage recipients | Medium | Recipients CRUD |
| Account cards | Low | `GET /account/{id}/cards` |

## Reference

- Full docs: `mercury_tools_plugin/docs/Mercury_MCP_API_Reference.md`
- [Mercury API Docs](https://docs.mercury.com/reference)
- [Sandbox Guide](https://docs.mercury.com/docs/using-mercury-sandbox)
