---
name: game-backend-architecture-patterns
description: Define clean, hexagonal, and DDD-based architecture patterns for a server-authoritative real-time multiplayer game backend implemented in TypeScript.
---

# Game Backend Architecture Patterns

This skill defines **how the backend of a real-time multiplayer hacking game MUST be structured**.

It exists to ensure:
- deterministic behavior
- testability
- clear boundaries
- long-term maintainability

This is **not** a generic enterprise architecture guide.

---

## When to Use This Skill

Use this skill when:

- Defining backend architecture for the game
- Structuring backend folders and modules
- Designing domain models and aggregates
- Creating use cases / application services
- Reviewing backend code for architectural violations
- Refactoring backend logic

This skill is **mandatory** for:
- `software-architect`
- `backend-engineer`

---

## Core Architectural Principles (NON-NEGOTIABLE)

### 1. Modular Monolith First

- Single deployable backend
- Clear internal module boundaries
- No microservices during MVP
- Communication via in-process interfaces

---

### 2. Clean Architecture (Pragmatic)

Dependency rule:
- Domain → Application → Infrastructure
- Never the opposite

Domain code:
- Has zero framework dependencies
- Is fully testable in isolation

---

### 3. Hexagonal Architecture (Ports & Adapters)

- Domain defines **ports**
- Infrastructure implements **adapters**
- Transport (HTTP / WebSocket) is an adapter
- Persistence is an adapter

---

### 4. Domain-Driven Design (DDD – Pragmatic)

Use DDD where it adds clarity, not ceremony.

Focus on:
- Aggregates
- Domain events
- Explicit invariants
- Ubiquitous language (game terminology)

Avoid:
- Over-modeling
- Artificial bounded contexts

---

## Layer Responsibilities

### Domain Layer

Contains:
- Entities
- Value Objects
- Aggregates
- Domain Events
- Domain Services (if needed)

Must NOT contain:
- Framework imports
- HTTP / WebSocket logic
- Persistence logic

---

### Application Layer

Contains:
- Use cases (application services)
- Command handlers
- Orchestration logic

Responsibilities:
- Validate intent
- Invoke domain logic
- Coordinate persistence
- Emit domain events

---

### Infrastructure Layer

Contains:
- Database adapters
- HTTP controllers
- WebSocket gateways
- External integrations

Responsibilities:
- Translate I/O to application commands
- Handle serialization
- Manage framework concerns

---

## Reference Folder Structure (TypeScript)

```txt
src/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   ├── events/
│   ├── repositories/
│   └── services/
│
├── application/
│   ├── commands/
│   ├── use-cases/
│   └── ports/
│
├── infrastructure/
│   ├── http/
│   ├── realtime/
│   ├── persistence/
│   └── config/
│
└── bootstrap/
```

### TypeScript Examples

#### Domain Entity (Game-Oriented)

```ts
// domain/entities/HackSession.ts
export class HackSession {
    constructor(
        readonly id: string,
        private progress: number,
        private readonly difficulty: number
    ) {}

    advance(delta: number): void {
        const next = this.progress + delta / this.difficulty;
        this.progress = Math.min(1, next);
    }

    isCompleted(): boolean {
        return this.progress >= 1;
    }
}
```

#### Application Use Case

```ts
// application/use-cases/StartHack.ts
import { HackSession } from '../../domain/entities/HackSession'

export class StartHack {
    execute(input: {
        sessionId: string;
        difficulty: number;
    }): HackSession {
        return new HackSession(input.sessionId, 0, input.difficulty);
    }
}
```

#### Port Definition

```ts
// application/ports/HackSessionRepository.ts
import { HackSession } from '../../domain/entities/HackSession';

export interface HackSessionRepository {
  save(session: HackSession): Promise<void>;
  findById(id: string): Promise<HackSession | null>;
}
```

#### Infrastructure Adapter

```ts
// infrastructure/persistence/InMemoryHackSessionRepository.ts
import { HackSessionRepository } from '../../application/ports/HackSessionRepository';
import { HackSession } from '../../domain/entities/HackSession';

export class InMemoryHackSessionRepository implements HackSessionRepository {
  private store = new Map<string, HackSession>();

  async save(session: HackSession): Promise<void> {
    this.store.set(session.id, session);
  }

  async findById(id: string): Promise<HackSession | null> {
    return this.store.get(id) ?? null;
  }
}

```

#### WebSocket Adapter (Real-Time)

```ts
// infrastructure/realtime/HackGateway.ts
import { StartHack } from '../../application/use-cases/StartHack';

export class HackGateway {
  constructor(private readonly startHack: StartHack) {}

  handleCommand(command: any) {
    if (command.type === 'START_HACK') {
      return this.startHack.execute(command.payload);
    }
  }
}

```

## Architectural Rules

- Domain must compile without infrastructure
- Application must not depend on frameworks
- Infrastructure may depend on everything
- No business logic in controllers/gateways
- No shared mutable state across aggregates

## Anti-Patterns (FORBIDDEN)

- ✖️ Fat controllers
- ✖️ Frameworks imports in domain
- ✖️ Anemic domain models
- ✖️ God services
- ✖️ Cross-module direct dependencies
- ✖️ "Just this once" shortcuts

## MVP Checklist

Before approving backend code:
- [] Does this respect layer boundaries?
- [] Is the domain framework-free?
- [] Is the logic deterministic?
- [] Is this testable in isolation?
- [] Does this belong in this layer?

If not, refactor.

## Final Rule

**Architecture exists to protect the game logic from entropy**.
If it makes iteration harder instead of safer, it is wrong.