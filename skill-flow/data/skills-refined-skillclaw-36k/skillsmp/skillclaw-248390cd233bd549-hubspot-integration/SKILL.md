---
name: hubspot-integration
description: Use this skill when integrating with HubSpot CRM, covering OAuth authentication, CRM object operations, and best practices for using the HubSpot API.
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
- ❌ Using Deprecated API Keys
- ❌ Individual Requests Instead of Batch
- ❌ Polling Instead of Webhooks

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
Always consult the provided reference files for guidance:
- **For Creation:** Refer to `references/patterns.md`.
- **For Diagnosis:** Use `references/sharp_edges.md` to explain risks.
- **For Review:** Validate inputs against `references/validations.md`.