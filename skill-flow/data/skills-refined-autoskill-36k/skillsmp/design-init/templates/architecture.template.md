---
status: stub | draft | current | needs-review | archived
module: {module-name}
category: architecture
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-synced: never | YYYY-MM-DD
completeness: 0
related:
  - path/to/related-doc.md
dependencies:
  - path/to/dependency-doc.md
---

# {System/Component Name} - Architecture

Brief one-sentence description of the architectural system or component.

## Table of Contents

1. [Overview](#overview)
2. [Current State](#current-state)
3. [Rationale](#rationale)
4. [System Architecture](#system-architecture)
5. [Data Flow](#data-flow)
6. [Integration Points](#integration-points)
7. [Testing Strategy](#testing-strategy)
8. [Future Enhancements](#future-enhancements)
9. [Related Documentation](#related-documentation)

---

## Overview

Describe the architectural system at a high level (2-4 paragraphs).

- What problem does this architecture solve?
- What are the key design principles?
- Why is this architecture appropriate for the use case?

**Key Design Principles:**

- Principle 1: Description
- Principle 2: Description
- Principle 3: Description

**When to reference this document:**

- When adding new components to the system
- When modifying core architectural patterns
- When integrating with external systems
- When debugging cross-component issues

---

## Current State

### System Components

List and describe all major components in the architecture.

#### Component 1: {Name}

**Location:** `src/path/to/component/`

**Purpose:** What this component does in the overall architecture

**Responsibilities:**

- Responsibility 1
- Responsibility 2
- Responsibility 3

**Key interfaces/APIs:**

```typescript
// Example of public API
interface ComponentAPI {
  mainMethod(params: Type): ReturnType;
}
```

**Dependencies:**

- Depends on: Component X, Component Y
- Used by: Component A, Component B

#### Component 2: {Name}

...

### Architecture Diagram

```text
┌─────────────────────────────────────────────────────┐
│                   Application Layer                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Component  │  │  Component  │  │  Component  │ │
│  │      A      │  │      B      │  │      C      │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
└─────────┼─────────────────┼─────────────────┼───────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────┐
│                    Service Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Service   │  │   Service   │  │   Service   │ │
│  │      X      │  │      Y      │  │      Z      │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
└─────────┼─────────────────┼─────────────────┼───────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────┐
│                    Data Layer                        │
└─────────────────────────────────────────────────────┘
```

### Current Limitations

Known limitations of the current architecture:

- Limitation 1: Description and workaround
- Limitation 2: Description and workaround

---

## Rationale

### Architectural Decisions

#### Decision 1: {Pattern/Technology Choice}

**Context:** What problem needed solving

**Options considered:**

1. **Option A (Chosen):**
   - Pros: Benefit 1, Benefit 2
   - Cons: Drawback 1, Drawback 2
   - Why chosen: Reasoning

2. **Option B:**
   - Pros: Benefit 1, Benefit 2
   - Cons: Drawback 1, Drawback 2
   - Why rejected: Reasoning

3. **Option C:**
   - Pros: Benefit 1, Benefit 2
   - Cons: Drawback 1, Drawback 2
   - Why rejected: Reasoning

#### Decision 2: {Component Boundaries}

...

### Design Patterns Used

#### Pattern 1: {Pattern Name}

- **Where used:** Component/Layer name
- **Why used:** Reasoning
- **Implementation:** Brief description

#### Pattern 2: {Pattern Name}

...

### Constraints and Trade-offs

#### Constraint 1: {Name}

- **Description:** What the constraint is
- **Impact:** How it affects the architecture
- **Mitigation:** How we work within the constraint

#### Trade-off 1: {Name}

- **What we gained:** Benefit
- **What we sacrificed:** Cost
- **Why it's worth it:** Justification

---

## System Architecture

### Layered Architecture

Describe the layers and their responsibilities.

#### Layer 1: {Name}

**Responsibilities:**

- Responsibility 1
- Responsibility 2

**Components:**

- Component A
- Component B

**Communication:** How this layer communicates with others

#### Layer 2: {Name}

...

### Component Interactions

Describe how components interact with each other.

#### Interaction 1: {Scenario}

**Participants:** Component A, Component B, Component C

**Flow:**

1. Component A initiates by calling `methodX()`
2. Component B processes and calls `methodY()`
3. Component C returns result
4. Component B aggregates and returns to Component A

**Sequence diagram:**

```text
A          B          C
│          │          │
├──────────>│          │  1. methodX()
│          ├──────────>│  2. methodY()
│          │<──────────┤  3. result
│<─────────┤          │  4. aggregated result
│          │          │
```

#### Interaction 2: {Scenario}

...

### Error Handling Strategy

How errors propagate through the architecture.

- Error type 1: Handling strategy
- Error type 2: Handling strategy

---

## Data Flow

### Data Model

Key data structures and their relationships.

```typescript
interface PrimaryEntity {
  id: string;
  field1: Type;
  field2: Type;
}

interface RelatedEntity {
  id: string;
  primaryId: string; // Foreign key
  field1: Type;
}
```

### Data Flow Diagrams

#### Flow 1: {Scenario}

```text
[Input Source]
      │
      ▼
[Validation Layer]
      │
      ▼
[Processing Layer]
      │
      ▼
[Storage Layer]
```

**Steps:**

1. Data arrives from source
2. Validation ensures data integrity
3. Processing transforms data
4. Storage persists data

#### Flow 2: {Scenario}

...

### State Management

How state is managed across the architecture.

- **Where state lives:** Component/Layer name
- **How state is updated:** Process description
- **State consistency:** How consistency is maintained

---

## Integration Points

### Internal Integrations

#### Integration 1: {System Name}

**How it integrates:** Description

**Interface:**

```typescript
// Integration API
interface IntegrationAPI {
  method(params: Type): ReturnType;
}
```

**Data exchange:** What data is exchanged

#### Integration 2: {System Name}

...

### External Integrations

#### Integration 1: {External System}

**Purpose:** Why we integrate

**Protocol:** HTTP REST / GraphQL / WebSocket / etc.

**Authentication:** How authentication works

**Error handling:** How errors are handled

#### Integration 2: {External System}

...

---

## Testing Strategy

### Architecture Testing

How to test the architecture itself.

**Component isolation:**

- Each component should be testable in isolation
- Mock dependencies at component boundaries
- Verify component contracts

**Integration testing:**

- Test interaction between layers
- Test cross-component workflows
- Verify data flow integrity

### Unit Tests

**Location:** `src/**/*.test.ts`

**Coverage target:** X%

**What to test:**

- Component APIs
- Error handling
- State management
- Data transformations

### Integration Tests

**Location:** `src/**/*.integration.test.ts`

**What to test:**

- End-to-end workflows
- Cross-layer communication
- External integrations
- Data consistency

---

## Future Enhancements

### Phase 1: Short-term (next release)

- Enhancement 1: Description and benefit
- Enhancement 2: Description and benefit

### Phase 2: Medium-term (2-3 releases)

- Enhancement 3: Description and benefit
- Enhancement 4: Description and benefit

### Phase 3: Long-term (future consideration)

- Enhancement 5: Description and benefit
- Enhancement 6: Description and benefit

### Potential Refactoring

Areas that may need refactoring in the future:

- Area 1: Why and when
- Area 2: Why and when

---

## Related Documentation

**Internal Design Docs:**

- [Component 1 Details](./component-1.md) - Detailed implementation
- [Component 2 Details](./component-2.md) - Detailed implementation

**Package Documentation:**

- `pkgs/{module}/README.md` - Package overview
- `pkgs/{module}/CLAUDE.md` - Development guide

**External Resources:**

- [Design Pattern Reference](url) - Pattern documentation
- [Architecture Style Guide](url) - Best practices

---

**Document Status:** {Explain current status if stub/draft/needs-review}

**Next Steps:** {What needs to be documented next}
