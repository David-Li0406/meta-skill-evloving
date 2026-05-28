---
name: salesforce-development
description: Use this skill for expert patterns in Salesforce platform development, including Lightning Web Components (LWC), Apex triggers, REST/Bulk APIs, and Salesforce DX.
---

# Salesforce Development

## Patterns

### Lightning Web Component with Wire Service

Use the `@wire` decorator for reactive data binding with Lightning Data Service or Apex methods. This approach fits LWC's reactive architecture and enables Salesforce performance optimizations.

### Bulkified Apex Trigger with Handler Pattern

Apex triggers must be bulkified to handle 200+ records per transaction. Use the handler pattern for separation of concerns, testability, and recursion prevention.

### Queueable Apex for Async Processing

Utilize Queueable Apex for asynchronous processing, supporting non-primitive types, monitoring via AsyncApexJob, and job chaining. Note the limit of 50 jobs per transaction and 1 child job when chaining.

## Anti-Patterns

- ❌ SOQL Inside Loops
- ❌ DML Inside Loops
- ❌ Hardcoding IDs

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |

## Reference System Usage

Ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation:** Always consult **`references/patterns.md`** for specific building patterns.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`** for critical failures and their explanations.
- **For Review:** Always consult **`references/validations.md`** for strict rules and constraints to validate user inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.