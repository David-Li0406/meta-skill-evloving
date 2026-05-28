---
name: architecture
description: Architecture principles for module boundaries, design patterns, and migration strategies
user-invocable: false
---

# Architecture Skill

**Version:** 2.0
**Source:** Architecture Principles

> These guidelines are optional extensions to core standards. Use what fits your project's complexity.

---

## North Star

**Goal:** Small changes stay local.

**Definition:** A typical feature should touch 1-2 modules, ship quickly, and not require coordinated edits across the system.

**Smell:** If you find yourself editing 5+ files across multiple layers for a simple change, that's a design smell.

---

## Core Principles

### 1. Explicit Over Magic

Prefer readable wiring over convention-heavy frameworks. When someone reads your code, the control flow should be obvious.

```typescript
// ❌ Magic - What does this do?
@AutoInject()
class UserService {}

// ✅ Explicit - Control flow is clear
class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}
}
```

### 2. Boundaries Are Sacred

Modules communicate only through contracts (APIs, props, events). No reaching into another module's internals.

```typescript
// ❌ Reaching into internals
const user = orderModule.database.users.find(id);

// ✅ Through the contract
const user = orderModule.getUserForOrder(orderId);
```

### 3. Own Your Data

Each module owns its schema/state. Other modules read via APIs or props, never direct access.

```
UserModule owns: users table, user state
OrderModule owns: orders table, cart state

UserModule reads orders via: OrderModule.getOrdersForUser(userId)
OrderModule reads users via: UserModule.getUserById(userId)
```

### 4. Optimize for Refactoring

If code is hard to move or rename, it's a design smell. Loose coupling enables safe refactoring.

---

## The 3 Layers

```
01-presentation/  →  02-logic/  →  03-data/
```

| Layer | Responsibility | Examples |
|-------|----------------|----------|
| **Presentation** | What users see and interact with | Components, pages, styles |
| **Logic** | How it's built, business rules | Services, use cases, validation |
| **Data** | How it persists, external sources | Repositories, models, adapters |

### Valid Dependency Flow

```
Presentation → Logic → Data ✅
Data → Logic ❌ (blocked)
Logic → Presentation ❌ (blocked)
```

---

## Folder Structure

### Organize by Feature, Not Layer

**Prefer:**
```
src/
├── users/
│   ├── user.model.ts
│   ├── user.service.ts
│   └── user.controller.ts
├── orders/
│   └── ...
└── shared/
    └── utils/
```

**Avoid:**
```
src/
├── models/
│   ├── user.model.ts
│   └── order.model.ts
├── services/
│   └── ...
```

**Why:** Feature-based keeps related code together. When you work on "users," everything is in one place.

### Depth Limit

Maximum 4 levels deep. If deeper, the structure is probably wrong.

---

## Module Boundaries

### What is a Module?

A cohesive unit with:
- Clear public API (exports)
- Hidden implementation (internals)
- Defined dependencies (imports)

### Module Rules

**Single Entry Point:** Each module exposes its API through an index file.

```
users/
├── index.ts             # Public API
├── user.service.ts      # Internal
└── user.repository.ts   # Internal
```

**No Reaching Into Modules:**

```typescript
// ✅ Yes
import { UserService } from '@/users';

// ❌ No
import { UserService } from '@/users/user.service';
```

### Coupling Guidelines

| Coupling Type | OK? |
|--------------|-----|
| Type import | ✓ Always |
| Function call | ✓ Usually |
| Direct instantiation | ⚠ Carefully |
| Shared mutable state | ✗ Avoid |

---

## Testing Strategy

| Type | Purpose | Scope | Volume |
|------|---------|-------|--------|
| **Unit** | Fast, deterministic, domain-heavy | Single function/component | Heavy |
| **Integration** | DB, APIs, external services | Module boundaries | Moderate |
| **E2E** | Critical user paths only | Full stack | Minimal |

### Guidance

- Heavy unit tests, moderate integration, minimal E2E
- E2E sprawl leads to brittle, slow test suites
- Contract tests recommended for API boundaries

---

## Red Flags

Stop and reconsider when you see:

| Smell | Problem | Fix |
|-------|---------|-----|
| `shared/common/utils` dumping ground | Ownership unclear, grows forever | Move to owning module or create focused package |
| Cross-module direct imports | Tight coupling, breaks independently | Use APIs, events, or props |
| Direct database access across modules | Hidden dependencies | Build a read API or service |
| "Quick helper" in wrong module | Boundary violation | Move to correct owner |
| Framework magic hiding control flow | Hard to debug, hard to refactor | Make it explicit |
| Feature touching 5+ unrelated files | Poor separation | Refactor boundaries |

---

## When to Extract

Start with a modular monolith (single deployable, clean internal boundaries).

**Extract to separate services only when:**

| Reason | Example |
|--------|---------|
| **Scale** | One part needs independent scaling |
| **Team** | Separate teams need independent deploy cycles |
| **Technology** | A component needs a different runtime/language |

**Don't extract for "cleanliness"** — that adds operational complexity without benefit.

---

## Observability Basics

### Structured Logging

```typescript
// ❌ String concatenation
console.log('User ' + userId + ' logged in at ' + new Date());

// ✅ Structured JSON
logger.info('User logged in', { userId, timestamp: new Date() });
```

### Correlation IDs

Track requests across async operations.

### Error Boundaries

Catch and report, don't swallow silently.

---

## Decision Records

For significant architectural choices, document:

1. **Context:** What problem are we solving?
2. **Decision:** What did we choose?
3. **Alternatives:** What else did we consider?
4. **Consequences:** What trade-offs are we accepting?

**Location:** `Documentation/decisions/`

---

## Pattern Selection

| Pattern | Use When |
|---------|----------|
| Pure functions | Stateless transformations |
| Module with functions | Grouping related functions |
| Class | State or DI needed |
| Factory | Complex object creation |
| Repository | Data access abstraction |

**Default to simplicity:** Function → Module → Class → Pattern

---

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| **God Object** | >500 lines, >10 public exports | Extract cohesive submodules |
| **Anemic Domain Model** | Getters/setters only, services do all work | Move behavior to entities |
| **Shotgun Surgery** | Adding a field requires 5+ file changes | Better encapsulation |

---

## Scaling Principles

| Project Size | Focus On |
|--------------|----------|
| **Small** | North Star, Red Flags |
| **Growing** | Add Testing Strategy, Observability |
| **Team** | Add Decision Records, Module Ownership |

---

## References

- `references/design-patterns.md` — Factory, Repository, Adapter, etc.
- `references/migration-patterns.md` — Strangler Fig, Branch by Abstraction, etc.
- `references/module-boundaries.md` — Detailed boundary guidelines

## Assets

- `assets/decision-record-template.md` — ADR template
- `assets/architecture-checklist.md` — Full architecture review checklist

## Scripts

- `scripts/analyze_dependencies.py` — Map circular dependencies and detect layer violations
