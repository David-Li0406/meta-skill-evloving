---
name: plaidd
description: Access Plaid banking APIs - accounts, transactions, balances, insights, and more
metadata: {"clawdbot":{"requires":{"bins":["plaidd"],"env":["PLAID_CLIENT_ID","PLAID_SECRET"]}}}
---

# Plaidd - Plaid Banking CLI

Use the `plaidd` CLI to interact with Plaid banking APIs. All commands output JSON.

## Prerequisites

Requires environment variables:
- `PLAID_CLIENT_ID` - Your Plaid client ID
- `PLAID_SECRET` - Your Plaid secret key
- `PLAID_ENV` - Environment: `sandbox` (default) or `production`

Bank connections are stored in `~/.plaidd/config.json` (managed by plaidd).

## Command Selection Guide

### What command should I use?

| User Intent | Command | Notes |
|-------------|---------|-------|
| Current balance | `accounts list` | Use cached data (FREE) |
| Real-time balance | `accounts balance` | Only if user says "current" or "refresh" (COSTS) |
| Recent transactions | `transactions sync` | Incremental updates |
| Transactions by date | `transactions get --start-date --end-date` | Specific range |
| Spending breakdown | `insights spending` | Aggregated by category (FREE) |
| Unusual activity | `insights anomalies` | Statistical outliers (FREE) |
| Monthly overview | `insights cashflow` | Income vs expenses (FREE) |
| Subscriptions | `insights recurring` | Recurring expenses (FREE) |

### IMPORTANT: Cost Awareness

- **FREE**: `accounts list`, `transactions *`, `insights *`
- **COSTS EXTRA**: `accounts balance`, `auth get`

Default to FREE commands. Only use `accounts balance` when user explicitly asks for "current", "real-time", or "up-to-date" balance.

## Multi-Connection Usage

Users may have multiple bank connections:

```bash
# List all connections
plaidd connection list

# Use default connection (automatic)
plaidd accounts list

# Use specific connection
plaidd accounts list --connection chase

# Query all connections
plaidd accounts balance --all-connections
```

**When to use `--all-connections`:**
- "What's my total balance across all accounts?"
- "Show all my transactions"

**When to use specific `--connection`:**
- "How much is in my Chase account?"
- "Show transactions from Bank of America"

## Conversation Patterns

### Pattern 1: Balance Inquiry

**User**: "What's my checking account balance?"

**Agent workflow**:
```bash
plaidd accounts list --pretty
```
Filter for `type: "depository"` and `subtype: "checking"`, report available balance.

**Response**: "Your Chase Checking (***1234) has $2,450.67 available."

### Pattern 2: Spending Analysis

**User**: "How much did I spend on food this month?"

**Agent workflow**:
```bash
# Calculate first of month to today
plaidd insights spending --start-date YYYY-MM-01 --end-date YYYY-MM-DD --pretty
```
Find FOOD_AND_DRINK category in `by_category` array.

**Response**: "You've spent $423.15 on food this month: $285.40 at restaurants, $137.75 on groceries."

### Pattern 3: Subscription Review

**User**: "What subscriptions am I paying for?"

**Agent workflow**:
```bash
plaidd insights recurring --type outflow --pretty
```
Look at `outflow_streams` for recurring expenses.

**Response**: "Your recurring expenses total $892/month: Netflix ($15.99), Spotify ($9.99), Gym ($50)..."

### Pattern 4: Unusual Activity

**User**: "Any unusual charges this month?"

**Agent workflow**:
```bash
plaidd insights anomalies --pretty
```
Review anomalies array, explain each finding.

**Response**: "I found 2 unusual transactions: A $1,500 transfer on Jan 15 (higher than your average), and a new merchant 'XYZ Corp' for $89.99."

### Pattern 5: Cash Flow Summary

**User**: "How am I doing financially this month?"

**Agent workflow**:
```bash
plaidd insights cashflow --period month --pretty
```
Report summary: income, expenses, net, savings rate.

**Response**: "This month: Income $5,200, Expenses $3,450, Net +$1,750 (34% savings rate)."

## Data Interpretation

### Transaction Amounts
- **Positive** = Money OUT (expenses, purchases)
- **Negative** = Money IN (income, deposits, refunds)

### Account Types
- `depository` + `checking` = Checking account
- `depository` + `savings` = Savings account
- `credit` = Credit card
- `loan` = Loans (mortgage, auto, student)
- `investment` = Brokerage/retirement accounts

### Categories (personal_finance_category)
- `INCOME` - Salary, freelance
- `FOOD_AND_DRINK` - Restaurants, groceries
- `TRANSPORTATION` - Gas, rideshare, parking
- `SHOPPING` - Retail, online
- `ENTERTAINMENT` - Streaming, events
- `BILLS_AND_UTILITIES` - Rent, utilities
- `TRANSFER_OUT` - Transfers between accounts

## Error Handling

| Error Code | Meaning | Recovery |
|------------|---------|----------|
| `ITEM_LOGIN_REQUIRED` | Bank needs re-auth | "Run `plaidd connection add` to reconnect" |
| `INVALID_ACCESS_TOKEN` | Token expired | "Run `plaidd connection add` to reconnect" |
| `NO_ACCOUNTS` | No accounts found | Check connection is set up |

## All Commands

### Connection Management
| Command | Description |
|---------|-------------|
| `plaidd connection list` | List all bank connections |
| `plaidd connection add` | Connect a new bank |
| `plaidd connection add --sandbox` | Quick sandbox connection |
| `plaidd connection remove <alias>` | Remove a connection |
| `plaidd connection set-default <alias>` | Set default connection |
| `plaidd connection info [alias]` | Show connection details |

### Insights (FREE - use these!)
| Command | Description |
|---------|-------------|
| `plaidd insights spending` | Spending by category/merchant |
| `plaidd insights anomalies` | Detect unusual transactions |
| `plaidd insights cashflow` | Income vs expenses |
| `plaidd insights recurring` | Recurring transactions |

### Accounts
| Command | Description |
|---------|-------------|
| `plaidd accounts list` | List accounts (cached, FREE) |
| `plaidd accounts balance` | Real-time balances (COSTS) |

### Transactions
| Command | Description |
|---------|-------------|
| `plaidd transactions sync` | Sync transactions |
| `plaidd transactions get` | Get by date range |
| `plaidd transactions recurring` | Plaid-detected recurring |

### Other
| Command | Description |
|---------|-------------|
| `plaidd item get` | Get item metadata |
| `plaidd item remove` | Remove item |
| `plaidd auth get` | ACH/routing numbers |
| `plaidd identity get` | Account holder info |
| `plaidd institutions search` | Search institutions |

## Common Options

- `--connection <alias>` - Use specific bank connection
- `--all-connections` - Query all connections
- `--start-date <YYYY-MM-DD>` - Start date for range queries
- `--end-date <YYYY-MM-DD>` - End date for range queries
- `--pretty` - Format JSON output

## Output Format

Success:
```json
{"success": true, "accounts": [...], "request_id": "abc123"}
```

Error:
```json
{"success": false, "error": {"type": "INVALID_REQUEST", "code": "...", "message": "..."}}
```
