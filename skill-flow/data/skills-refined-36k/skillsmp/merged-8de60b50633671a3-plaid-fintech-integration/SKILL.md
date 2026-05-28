---
name: plaid-fintech-integration
description: Use this skill when integrating with the Plaid API for bank account linking, transactions, identity verification, and webhook handling.
---

# Plaid Fintech Integration

## Patterns

### Link Token Creation and Exchange

Create a link_token for Plaid Link and exchange a public_token for an access_token. Link tokens are short-lived and one-time use, while access tokens do not expire but may need updating when users change passwords.

### Transactions Sync

Utilize the `/transactions/sync` endpoint for incremental transaction updates, which is more efficient than `/transactions/get`. Handle webhooks for real-time updates instead of relying on polling.

### Item Error Handling and Update Mode

Manage `ITEM_LOGIN_REQUIRED` errors by guiding users through Link update mode. Listen for the `PENDING_DISCONNECT` webhook to proactively prompt users for action.

## Anti-Patterns

### ❌ Storing Access Tokens in Plain Text

### ❌ Polling Instead of Webhooks

### ❌ Ignoring Item Errors

## Reference System Usage

Always consult the following reference files for guidance:

* **For Creation:** Refer to **`references/patterns.md`** for specific building patterns.
* **For Diagnosis:** Use **`references/sharp_edges.md`** to understand critical failures and their causes.
* **For Review:** Check **`references/validations.md`** for strict rules and constraints to validate user inputs.

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