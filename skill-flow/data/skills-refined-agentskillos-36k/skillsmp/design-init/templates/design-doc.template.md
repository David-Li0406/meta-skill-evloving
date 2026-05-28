---
status: stub | draft | current | needs-review | archived
module: {module-name}
category: architecture | performance | observability | testing | integration | other
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-synced: never | YYYY-MM-DD
completeness: 0
related:
  - path/to/related-doc.md
dependencies:
  - path/to/dependency-doc.md
---

# {Document Title}

Brief one-sentence description of what this document covers.

## Table of Contents

1. [Overview](#overview)
2. [Current State](#current-state)
3. [Rationale](#rationale)
4. [Implementation Details](#implementation-details)
5. [Testing Strategy](#testing-strategy)
6. [Future Enhancements](#future-enhancements)
7. [Related Documentation](#related-documentation)

---

## Overview

Brief description of what this document covers (2-4 paragraphs).

Explain the problem being solved, the solution approach, and why it matters.

**Key Features:**

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

**When to reference this document:**

- Scenario 1: When working on X
- Scenario 2: When debugging Y
- Scenario 3: When implementing Z

---

## Current State

### What Exists Now

Describe the current implementation state. What's been built, what works,
what's in production.

**Key Components:**

1. **Component Name** (`src/path/to/file.ts`)
   - Purpose: What it does
   - Status: Implemented/Planned/Deprecated
   - Key methods: `methodName()`, `propertyName`

2. **Component Name** (`src/path/to/file.ts`)
   - Purpose: What it does
   - Status: Implemented/Planned/Deprecated

### Current Metrics/Status

If applicable, include current performance metrics, coverage, usage stats,
etc.

- Metric 1: Value
- Metric 2: Value
- Metric 3: Value

---

## Rationale

### Why This Approach

Explain the reasoning behind design decisions. What alternatives were
considered and why this approach was chosen.

#### Decision 1: {Decision Name}

- **Context:** What problem needed solving
- **Options considered:**
  1. Option A: Pros and cons
  2. Option B: Pros and cons
  3. Option C: Pros and cons
- **Decision:** Which option was chosen
- **Reasoning:** Why this option was best

#### Decision 2: {Decision Name}

...

### Constraints and Trade-offs

What constraints influenced the design? What trade-offs were made?

- Constraint 1: Description and impact
- Constraint 2: Description and impact
- Trade-off 1: What was sacrificed and why

---

## Implementation Details

### Architecture

High-level architecture with diagrams if helpful.

```text
┌─────────────────┐
│   Component A   │
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Component B   │
└─────────────────┘
```

### Key Components

#### Component 1: {Name}

**Location:** `src/path/to/component.ts`

**Purpose:** What this component does

**Key APIs:**

```typescript
// Example code showing key interfaces/methods
interface ComponentAPI {
  method1(param: Type): ReturnType;
  method2(param: Type): ReturnType;
}
```

**Implementation notes:**

- Note 1: Important detail
- Note 2: Important detail

#### Component 2: {Name}

...

### Integration Points

How this system integrates with other parts of the codebase.

#### Integration 1: {System Name}

- **Location:** Where integration happens
- **How it works:** Description
- **Dependencies:** What it depends on

#### Integration 2: {System Name}

...

### Configuration

If applicable, describe configuration options.

```typescript
// Configuration interface or example
interface Config {
  option1: Type; // Description
  option2: Type; // Description
}
```

### Error Handling

How errors are handled in this system.

- Error type 1: How it's handled
- Error type 2: How it's handled

---

## Testing Strategy

### Unit Tests

**Location:** `src/path/to/*.test.ts`

**Coverage:** X% (target: Y%)

**What to test:**

1. Component A behavior
   - Test case 1
   - Test case 2
2. Component B behavior
   - Test case 1
   - Test case 2

**Running tests:**

```bash
pnpm test -- path/to/tests
```

### Integration Tests

If applicable, describe integration test strategy.

**What to test:**

1. End-to-end scenario 1
2. End-to-end scenario 2

**Running integration tests:**

```bash
pnpm test:integration
```

### Manual Testing

If manual testing is needed, describe the process.

---

## Future Enhancements

### Phase 1: Short-term (next release)

- Enhancement 1: Description
- Enhancement 2: Description

### Phase 2: Medium-term (2-3 releases)

- Enhancement 3: Description
- Enhancement 4: Description

### Phase 3: Long-term (future consideration)

- Enhancement 5: Description
- Enhancement 6: Description

---

## Related Documentation

**Internal Design Docs:**

- [Related Doc 1](./related-doc-1.md) - Brief description
- [Related Doc 2](../other-module/related-doc-2.md) - Brief description

**Package Documentation:**

- `pkgs/{module}/README.md` - Package overview
- `pkgs/{module}/CLAUDE.md` - Development guide

**External Resources:**

- [External Resource 1](url) - Description
- [External Resource 2](url) - Description

---

**Document Status:** {Explain current status if stub/draft/needs-review}

**Next Steps:** {What needs to be done - required for stubs/drafts}
