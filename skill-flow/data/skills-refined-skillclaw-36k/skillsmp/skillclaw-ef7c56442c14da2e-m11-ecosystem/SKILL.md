---
name: m11-ecosystem
description: Use this skill when integrating crates or addressing ecosystem-related questions in Rust development.
---

# Ecosystem Integration

> **Layer 2: Design Choices**

## Core Question

**What's the right crate for this job, and how should it integrate?**

Before adding dependencies:
- Is there a standard solution?
- What's the maintenance status?
- What's the API stability?

---

## Integration Decision → Implementation

| Need | Choice | Crates |
|------|--------|--------|
| Serialization | Derive-based | serde, serde_json |
| Async runtime | tokio or async-std | tokio (most popular) |
| HTTP client | Ergonomic | reqwest |
| HTTP server | Modern | axum, actix-web |
| Database | SQL or ORM | sqlx, diesel |
| CLI parsing | Derive-based | clap |
| Error handling | App vs lib | anyhow, thiserror |
| Logging | Facade | tracing, log |

---

## Thinking Prompt

Before adding a dependency:

1. **Is it well-maintained?**
   - Recent commits?
   - Active issue response?
   - Breaking changes frequency?

2. **What's the scope?**
   - Do you need the full crate or just a feature?
   - Can feature flags reduce bloat?

3. **How does it integrate?**
   - Trait-based or concrete types?
   - Sync or async?
   - What bounds does it require?

---

## Trace Up ↑

To domain constraints (Layer 3):

```
"Which HTTP framework should I use?"
    ↑ Ask: What are the performance requirements?
    ↑ Check: domain-web (latency, throughput needs)
    ↑ Check: Team expertise (familiarity with framework)
```

| Question | Trace To | Ask |
|----------|----------|-----|
| Framework choice | domain-* | What constraints matter? |
| Library vs build | domain-* | What's the deployment model? |
| API design | domain-* | Who are the consumers? |

---

## Trace Down ↓

To implementation (Layer 1):

```
"Integrate external crate"
    ↓ m04-zero-cost: Trait bounds and generics
    ↓ m06-error-handling: Error type compatibility

"FFI integration"
    ↓ unsafe-checker: Safety requirements
    ↓ m12-lifecycle: Resource cleanup
```

---

## Quick Reference

### Language Interop

| Integration | Crate/Tool | Use Case |
|-------------|------------|----------|
| C/C++ → Rust | `bindgen` | Auto-generate Rust FFI bindings to C/C++ libraries |
| Python → Rust | `PyO3` | Create Python extensions in Rust |
| WebAssembly | `wasm-bindgen` | Interact with JavaScript from Rust |
| Node.js | `napi-rs` | Build native Node.js modules in Rust |