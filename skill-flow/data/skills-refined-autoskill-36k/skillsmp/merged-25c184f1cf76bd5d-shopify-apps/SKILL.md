---
name: shopify-apps
description: Use this skill when developing Shopify apps, including embedded apps, webhook handling, and utilizing GraphQL and Polaris components.
---

# Shopify Apps

## Patterns

### React Router App Setup

Modern Shopify app template with React Router.

### Embedded App with App Bridge

Render app embedded in Shopify Admin.

### Webhook Handling

Secure webhook processing with HMAC verification.

## Anti-Patterns

### ❌ REST API for New Apps

### ❌ Webhook Processing Before Response

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | Respond immediately, process asynchronously. |
| Issue | high | Check rate limit headers. |
| Issue | high | Request protected customer data access. |
| Issue | medium | Use TOML only (recommended). |
| Issue | medium | Handle both URL formats. |
| Issue | high | Use GraphQL for all new code. |
| Issue | high | Use latest App Bridge via script tag. |
| Issue | high | Implement all GDPR handlers. |

## Reference System Usage

Ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.