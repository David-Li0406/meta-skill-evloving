---
name: segment-cdp
description: Use this skill when working with Segment Customer Data Platform for analytics, tracking plans, and data governance best practices.
---

# Segment CDP

## Patterns

### Analytics.js Browser Integration

Implement client-side tracking with Analytics.js, including track, identify, page, and group calls. Anonymous IDs persist until an identify call merges with the user.

### Server-Side Tracking with Node.js

Utilize high-performance server-side tracking using `@segment/analytics-node`. This method is non-blocking with internal batching, making it essential for backend events, webhooks, and handling sensitive data.

### Tracking Plan Design

Design event schemas using the Object + Action naming convention. Define required properties, types, and validation rules, and connect to Protocols for enforcement.

## Anti-Patterns

### ❌ Dynamic Event Names

### ❌ Tracking Properties as Events

### ❌ Missing Identify Before Track

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | low | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |

## Reference System Usage

Always consult the provided reference files as the source of truth for this domain:

* **For Creation:** Refer to **`references/patterns.md`** for specific building patterns.
* **For Diagnosis:** Use **`references/sharp_edges.md`** to identify critical failures and their causes.
* **For Review:** Check **`references/validations.md`** for strict rules and constraints to validate user inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.