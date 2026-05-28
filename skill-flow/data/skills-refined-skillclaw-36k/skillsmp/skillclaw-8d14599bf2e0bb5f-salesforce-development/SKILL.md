---
name: salesforce-development
description: Use this skill when developing on the Salesforce platform, including Lightning Web Components (LWC), Apex triggers, and Salesforce DX.
---

# Salesforce Development

## Patterns

### Lightning Web Component with Wire Service
Use the `@wire` decorator for reactive data binding with Lightning Data Service or Apex methods. This fits LWC's reactive architecture and enables Salesforce performance optimizations.

### Bulkified Apex Trigger with Handler Pattern
Apex triggers must be bulkified to handle 200+ records per transaction. Use the handler pattern for separation of concerns, testability, and recursion prevention.

### Queueable Apex for Async Processing
Use Queueable Apex for asynchronous processing with support for non-primitive types, monitoring via `AsyncApexJob`, and job chaining. Limit: 50 jobs per transaction, 1 child job when chaining.

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
Always consult the provided reference files for guidance on creation, diagnosis, and review. If a user's request conflicts with the guidance, politely correct them using the information provided in the references.