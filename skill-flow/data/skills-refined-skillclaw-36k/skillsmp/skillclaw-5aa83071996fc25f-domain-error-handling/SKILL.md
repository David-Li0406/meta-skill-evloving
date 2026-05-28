---
name: domain-error-handling
description: Use this skill when designing a strategy for handling domain errors, including categorization, recovery strategies, and user experience considerations.
---

# Domain Error Strategy

> **Layer 2: Design Choices**

## Core Question

**Who needs to handle this error, and how should they recover?**

Before designing error types:
- Is this user-facing or internal?
- Is recovery possible?
- What context is needed for debugging?

---

## Error Categorization

| Error Type | Audience | Recovery | Example |
|------------|----------|----------|---------|
| User-facing | End users | Guide action | `InvalidEmail`, `NotFound` |
| Internal | Developers | Debug info | `DatabaseError`, `ParseError` |
| System | Ops/SRE | Monitor/alert | `ConnectionTimeout`, `RateLimited` |
| Transient | Automation | Retry | `NetworkError`, `ServiceUnavailable` |
| Permanent | Human | Investigate | `ConfigInvalid`, `DataCorrupted` |

---

## Thinking Prompt

Before designing error types:

1. **Who sees this error?**
   - End user → friendly message, actionable
   - Developer → detailed, debuggable
   - Ops → structured, alertable

2. **Can we recover?**
   - Transient → retry with backoff
   - Degradable → fallback value
   - Permanent → fail fast, alert

3. **What context is needed?**
   - Call chain → `anyhow::Context`
   - Request ID → structured logging
   - Input data → error payload

---

## Trace Up ↑

To domain constraints (Layer 3):

```
"How should I handle payment failures?"
    ↑ Ask: What are the business rules for retries?
    ↑ Check: domain-fintech (transaction requirements)
    ↑ Check: SLA (availability requirements)
```

| Question | Trace To | Ask |
|----------|----------|-----|
| Retry policy | domain-* | What's acceptable latency for retry? |
| User experience | domain-* | What message should users see? |
| Compliance | domain-* | What must be logged for audit? |

---

## Trace Down ↓

To implementation (Layer 1):

```
"Need typed errors"
    ↓ m06-error-handling: thiserror for library
    ↓ m04-zero-cost: Error enum design

"Need error context"
    ↓ m06-error-handling: anyhow::Context
    ↓ Logging: tracing with fields

"Need retry logic"
    ↓ m07-concurrency: async retry patterns
    ↓ Crates: tokio-retry, ba
```