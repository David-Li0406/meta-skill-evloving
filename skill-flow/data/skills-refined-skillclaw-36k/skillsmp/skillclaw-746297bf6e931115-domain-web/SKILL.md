---
name: domain-web
description: Use this skill when building web services with Rust, focusing on HTTP, REST APIs, and WebSocket implementations.
---

# Skill body

## Overview

This skill provides guidelines and best practices for building web services in Rust, covering essential concepts such as state management, concurrency, and security.

## Keywords

- web server
- HTTP
- REST API
- GraphQL
- WebSocket
- axum
- actix
- warp
- rocket
- tower
- hyper
- reqwest
- middleware
- router
- handler
- extractor
- state management
- authentication
- authorization
- JWT
- session
- cookie
- CORS
- rate limiting

## Domain Constraints → Design Implications

| Domain Rule         | Design Constraint          | Rust Implication                |
|---------------------|----------------------------|---------------------------------|
| Stateless HTTP      | No request-local globals    | State in extractors            |
| Concurrency         | Handle many connections     | Async, Send + Sync             |
| Latency SLA         | Fast response               | Efficient ownership             |
| Security            | Input validation            | Type-safe extractors           |
| Observability       | Request tracing             | tracing + tower layers         |

## Critical Constraints

### Async by Default

```
RULE: Web handlers must not block
WHY: Block one task = block many requests
RUST: async/await, spawn_blocking for CPU work
```

### State Management

```
RULE: Shared state must be thread-safe
WHY: Handlers run on any thread
RUST: Arc<T>, Arc<RwLock<T>> for mutable
```

### Request Lifecycle

```
RULE: Resources live only for request duration
WHY: Memory management, no leaks
RUST: Extractors, proper ownership
```

## Framework Comparison

| Framework   | Style                | Best For          |
|-------------|----------------------|-------------------|
| axum        | Functional, tower    | Modern APIs       |
| actix-web   | Actor-based          | High performance   |
| warp        | Filter composition    | Composable APIs    |
| rocket      | Macro-driven         | Rapid development  |

## Key Crates

| Purpose       | Crate               |
|---------------|---------------------|
| HTTP server   | axum, actix-web     |
| HTTP client   | reqwest             |
| JSON          | serde_json          |
| Auth/JWT      | jsonwebtoken        |
| Session       | tower-sessions      |
| Database      | sqlx, diesel        |
| Middleware    | tower               |

## Design Patterns

| Pattern          | Purpose            | Implementation                  |
|------------------|--------------------|---------------------------------|
| Extractors       | Request parsing     | `State(db)`, `Json(payload)`    |
| Error response    | Unified error handling | `IntoResponse for errors`     |