---
name: resource-lifecycle
description: Use this skill when designing resource lifecycles to ensure efficient management of resource creation, usage, and cleanup.
---

# Resource Lifecycle

> **Layer 2: Design Choices**

## Core Question

**When should this resource be created, used, and cleaned up?**

Before implementing lifecycle:
- What's the resource's scope?
- Who owns the cleanup responsibility?
- What happens on error?

---

## Lifecycle Pattern → Implementation

| Pattern | When | Implementation |
|---------|------|----------------|
| RAII | Auto cleanup | `Drop` trait |
| Lazy init | Deferred creation | `OnceLock`, `LazyLock` |
| Pool | Reuse expensive resources | `r2d2`, `deadpool` |
| Guard | Scoped access | `MutexGuard` pattern |
| Scope | Transaction boundary | Custom struct + Drop |

---

## Thinking Prompt

Before designing lifecycle:

1. **What's the resource cost?**
   - Cheap → create per use
   - Expensive → pool or cache
   - Global → lazy singleton

2. **What's the scope?**
   - Function-local → stack allocation
   - Request-scoped → passed or extracted
   - Application-wide → static or Arc

3. **What about errors?**
   - Cleanup must happen → Drop
   - Cleanup is optional → explicit close
   - Cleanup can fail → Result from close

---

## Trace Up ↑

To domain constraints (Layer 3):

```
"How should I manage database connections?"
    ↑ Ask: What's the connection cost?
    ↑ Check: domain-* (latency requirements)
    ↑ Check: Infrastructure (connection limits)
```

| Question | Trace To | Ask |
|----------|----------|-----|
| Connection pooling | domain-* | What's acceptable latency? |
| Resource limits | domain-* | What are infra constraints? |
| Transaction scope | domain-* | What must be atomic? |

---

## Trace Down ↓

To implementation (Layer 1):

```
"Need automatic cleanup"
    ↓ m02-resource: Implement Drop
    ↓ m01-ownership: Clear owner for cleanup

"Need lazy initialization"
    ↓ m03-mutability: OnceLock for thread-safe
    ↓ m07-concurrency: LazyLock for sync

"Need connection pool"
    ↓ m07-concurrency: Thread-safe pool
    ↓ m02-resource: Arc for sharing
```

---

## Quick Reference

| Pattern | Type | Use Case |
|---------|------|----------|
| RAII | `Drop` trait | Auto cleanup on scope exit |
| Lazy init | `OnceLock` | Deferred resource creation |
| Pool | `r2d2` | Efficient resource reuse |
| Guard | `MutexGuard` | Scoped resource access |
| Scope | Custom struct | Manage transaction boundaries |