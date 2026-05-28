---
name: concurrency
description: Use this skill when dealing with concurrency and asynchronous programming in Rust, especially when encountering issues related to thread safety and data sharing.
---

# Concurrency

> **Layer 1: Language Mechanics**

## Core Question

**Is this CPU-bound or I/O-bound, and what's the sharing model?**

Before choosing concurrency primitives:
- What's the workload type?
- What data needs to be shared?
- What's the thread safety requirement?

---

## Error → Design Question

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| E0277 Send | "Add Send bound" | Should this type cross threads? |
| E0277 Sync | "Wrap in Mutex" | Is shared access really needed? |
| Future not Send | "Use spawn_local" | Is async the right choice? |
| Deadlock | "Reorder locks" | Is the locking design correct? |

---

## Thinking Prompt

Before adding concurrency:

1. **What's the workload?**
   - CPU-bound → threads (std::thread, rayon)
   - I/O-bound → async (tokio, async-std)
   - Mixed → hybrid approach

2. **What's the sharing model?**
   - No sharing → message passing (channels)
   - Immutable sharing → Arc<T>
   - Mutable sharing → Arc<Mutex<T>> or Arc<RwLock<T>>

3. **What are the Send/Sync requirements?**
   - Cross-thread ownership → Send
   - Cross-thread references → Sync
   - Single-thread async → spawn_local

---

## Trace Up ↑ (MANDATORY)

**CRITICAL**: Don't just fix the error. Trace UP to find domain constraints.

### Domain Detection Table

| Context Keywords | Load Domain Skill | Key Constraint |
|-----------------|-------------------|----------------|
| Web API, HTTP, axum, actix, handler | **domain-web** | Handlers run on any thread |
| 交易, 支付, trading, payment | **domain-fintech** | Audit + thread safety |
| gRPC, kubernetes, microservice | **domain-cloud-native** | Distributed tracing |
| CLI, terminal, clap | **domain-cli** | Usually single-thread OK |

### Example: Web API + Rc Error

```
"Rc cannot be sent between threads" in Web API context
    ↑ DETECT: "Web API" → Load domain-web
    ↑ FIND: domain-web says "Shared state must be thread-safe"
    ↑ FIND: domain-web says "Rc in state" is Common Mistake
    ↓ DESIGN: Use Arc<T> with State extractor
    ↓ IMPL: axum::extract::State<Arc<AppConfig>>
```

### Generic Trace

```
"Send not satisfied for my type"
    ↑ Ask: What domain is this? Load domain-* skill
```