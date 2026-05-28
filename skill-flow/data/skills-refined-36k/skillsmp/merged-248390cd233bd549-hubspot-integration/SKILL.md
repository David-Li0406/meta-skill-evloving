---
name: hubspot-integration
description: Use this skill for expert patterns in HubSpot CRM integration, including OAuth authentication, CRM object operations, and webhooks.
---

# HubSpot Integration

## Patterns

### OAuth 2.0 Authentication

Secure authentication for public apps.

### Private App Token

Authentication for single-account integrations.

### CRM Object CRUD Operations

Create, read, update, and delete CRM records.

## Anti-Patterns

### ❌ Using Deprecated API Keys

### ❌ Individual Requests Instead of Batch

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |

## Reference System Usage

Ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`** for specific building patterns.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`** for critical failures and their explanations.
* **For Review:** Always consult **`references/validations.md`** for strict rules and constraints to validate user inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.