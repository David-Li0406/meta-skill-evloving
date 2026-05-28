---
name: rust-router
description: Use this skill for all Rust-related questions, including errors, design, and coding practices.
---

# Rust Question Router

> **Version:** 2.0.0 | **Last Updated:** 2026-01-17

## Meta-Cognition Framework

### Core Principle

**Don't answer directly. Trace through the cognitive layers first.**

```
Layer 3: Domain Constraints (WHY)
├── Business rules, regulatory requirements
├── domain-fintech, domain-web, domain-cli, etc.
└── "Why is it designed this way?"

Layer 2: Design Choices (WHAT)
├── Architecture patterns, DDD concepts
├── m09-m15 skills
└── "What pattern should I use?"

Layer 1: Language Mechanics (HOW)
├── Ownership, borrowing, lifetimes, traits
├── m01-m07 skills
└── "How do I implement this in Rust?"
```

### Routing by Entry Point

| User Signal | Entry Layer | Direction | First Skill |
|-------------|-------------|-----------|-------------|
| E0xxx error | Layer 1 | Trace UP ↑ | m01-m07 |
| Compile error | Layer 1 | Trace UP ↑ | Error table below |
| "How to design..." | Layer 2 | Check L3, then DOWN ↓ | m09-domain |
| "Building [domain] app" | Layer 3 | Trace DOWN ↓ | domain-* |
| "Best practice..." | Layer 2 | Both directions | m09-m15 |
| Performance issue | Layer 1 → 2 | UP then DOWN | m10-performance |

### CRITICAL: Dual-Skill Loading

**When domain keywords are present, you MUST load BOTH skills:**

| Domain Keywords | L1 Skill | L3 Skill |
|-----------------|----------|----------|
| Web API, HTTP, axum, handler | m07-concurrency | **domain-web** |
| 交易, 支付, trading, payment | m01-ownership | **domain-fintech** |
| CLI, terminal, clap | m07-concurrency | **domain-cli** |
| kubernetes, grpc, microservice | m07-concurrency | **domain-microservice** |

### Triggers

This skill is triggered by keywords related to Rust, including but not limited to:
- Rust, cargo, rustc, crate, Cargo.toml
- Compile errors, borrow errors, lifetime errors, ownership errors, type errors, trait errors
- Keywords like async, await, Send, Sync, concurrency, error handling
- Questions such as "how to use", "what is", "help me write", "implement", "explain", and comparisons like "compare" or "best practice".