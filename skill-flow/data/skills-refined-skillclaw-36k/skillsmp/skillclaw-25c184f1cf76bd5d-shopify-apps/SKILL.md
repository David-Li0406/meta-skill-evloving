---
name: shopify-apps
description: Use this skill when developing Shopify apps, including embedded apps, to leverage best practices and avoid common pitfalls.
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
| High | Respond immediately, process asynchronously. |
| High | Check rate limit headers. |
| High | Request protected customer data access. |
| Medium | Use TOML only (recommended). |
| Medium | Handle both URL formats. |
| High | Use GraphQL for all new code. |
| High | Use latest App Bridge via script tag. |
| High | Implement all GDPR handlers. |