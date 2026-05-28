---
name: game-backend-api-design
description: "Design server-authoritative REST and real-time API contracts for a multiplayer hacking game, focused on commands, events, and deterministic state."
---

# Game Backend API Design Principles

This skill defines **how APIs and real-time contracts MUST be designed** for a **server-authoritative, real-time multiplayer hacking game**.

It is not a generic API guide.
It exists to prevent:

- state leaks
- client trust
- overengineering
- CRUD-driven game logic

---

## When to Use This Skill

Use this skill when:

- Designing backend APIs for the game
- Defining real-time (WebSocket/SSE) event contracts
- Reviewing API or event schemas
- Validating backend–frontend communication
- Preventing security or consistency issues in multiplayer flows
- Creating `/docs/backend-engineer/api-contracts.md`
- Creating `/docs/backend-engineer/realtime-events.md`

Do **NOT** use this skill for:

- Enterprise SaaS APIs
- Microservices design
- SDK generation
- Public platform APIs

---

## Core Philosophy (NON-NEGOTIABLE)

### 1. Server Authority First

- The client is **untrusted**
- The server owns **all game state**
- APIs accept **intent**, never **state**
- The server computes outcomes

> If the client can influence game state directly, the design is wrong.

---

### 2. Commands, Not CRUD

Game APIs are **not CRUD interfaces**.

- Commands express **player intent**
- Events express **authoritative outcomes**
- Queries are **read-only projections**

| Type    | Direction       | Purpose                      |
| ------- | --------------- | ---------------------------- |
| Command | Client → Server | “I want to do X”             |
| Event   | Server → Client | “X happened”                 |
| Query   | Client → Server | “What is the current state?” |

---

### 3. Real-Time Is the Primary Channel

- REST is **supporting infrastructure**
- Real-time channel is **core gameplay**
- No gameplay logic hidden in REST

---

## API Channel Responsibilities

### REST APIs (Secondary)

REST is used ONLY for:

- Authentication
- Session bootstrap
- Initial data snapshots
- Account metadata
- Non-real-time operations

#### REST Rules

- Resource-oriented URLs
- Correct HTTP semantics
- Idempotent where applicable
- Strict input validation

Example:

```http
POST /api/sessions
POST /api/auth/login
GET  /api/player/profile
GET  /api/game/bootstrap
```

REST endpoints **MUST NOT:**

- resolve hacks
- update game state
- apply damage
- execute exploits

### Real-Time Channel (Primary)

The real-time channel handles:

- Player commands
- State updates
- Timers
- Continuous hacking flows

#### Real-Time Rules

- Client sends **commands only**
- Server broadcasts **events only**
- No client-side state authority
- All events are deterministic

Example command:

```json
{
  "type": "START_HACK",
  "payload": {
    "targetNodeId": "node-42",
    "toolId": "bruteforce-v1"
  }
}
```

Example server event:

```json
{
  "type": "HACK_PROGRESS_UPDATED",
  "payload": {
    "hackSessionId": "hs-123",
    "progress": 0.42,
    "detected": false
  }
}
```

## Command Design Rules

Commands MUST:

- Represent player intent
- Be validated server-side
- Be idempotent where possible
- Never include derived state

### Command Naming

- Use imperative verbs
- Describe intention, not result

Good:

- `START_HACK`
- `CANCEL_HACK`
- `DEPLOY_TOOL`

Bad:

- `UPDATE_NODE`
- `SET_PROGRESS`
- `APPLY_DAMAGE`

## Event Design Rules

Events MUST:

- Represent facts that already happened
- Be generated only by the server
- Be immutable
- Be replay-safe

### Event Naming

- Past tense
- Descriptive

Good:

- `HACK_STARTED`
- `HACK_FAILED`
- `NODE_COMPROMISED`

Bad:

- `START_HACK`
- `UPDATE_STATE`
- `PROCESS_HACK`

## Error Handling Model

### REST Errors

Use a **consistent error envelope**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid command payload",
    "details": {
      "field": "toolId"
    },
    "timestamp": "2026-01-20T12:00:00Z",
    "path": "/api/game/bootstrap"
  }
}
```

### Real-Time Errors

Errors are **events**, not HTTP responses:

```json
{
  "type": "COMMAND_REJECTED",
  "payload": {
    "command": "START_HACK",
    "reason": "INSUFFICIENT_SKILL_LEVEL"
  }
}
```

## Validation & Security Rules

- Validater all inputs
- Enforce rate limits
- Never trust client timers
- Never trust client progress
- Detect replay attempts
- Reject malformed commands early

## Versioning Strategy (MVP)

- Not versioning during MVP
- Break changes only with ADR
- Prefer additive changes
- Deprecate via documentation, not flags

## Anti-PAtterns (STRICTLY FORBIDDEN)

- ✖️ CRUD over WebSockets
- ✖️ Client-driven state updates
- ✖️ Game rules in frontend
- ✖️ API shaped like database tables
- ✖️ Multiple sources of truth
- ✖️ Hidden side effects in queries

## Documentation Requirements

This skill MUST produce or validate:

- `/docs/backend-engineer/api-contracts.md`
- `/docs/backend-engineer/realtime-events.md`

Each document must include:

- Purpose
- Schemas
- Direction
- Error scenarios

## MVP Checklist

Before implementing or approving any API or event:

- [] Does this accept intent, not state?
- [] Is the server authoritative?
- [] Can this be exploited by a malicious client?
- [] Is this required to validate gameplay?
- [] Is the real-time channel used correctly?
- [] IS the contract deterministic?

IF any answer is **no**, redesign.

## Final Rule

- **If the API amkes cheating easier, it is wrong.**
- **If the API makes the game harder to reason about, it is wrong.**
- **If the API does not serve the core gameplay loop, it does not exist.**

## Resources

- **references/rest-best-practices.md**: Comprehensive REST API design guide
- **references/graphql-schema-design.md**: GraphQL schema patterns and anti-patterns
- **assets/api-design-checklist.md**: Pre-implementation review checklist
