---
name: architecture-decision-records
description: Use this skill to create and document Architecture Decision Records (ADRs) that capture significant architectural decisions, their context, alternatives, and consequences.
---

# Architecture Decision Records (ADR) - Comprehensive Guide

This skill provides a structured approach for creating high-quality Architecture Decision Records (ADRs) that document significant technical decisions made during a project's development. ADRs capture the decision context, rationale, alternatives considered, and consequences.

## What is an ADR?

An Architecture Decision Record documents a significant technical decision made during the project's development. ADRs capture:
- **What** decision was made
- **Why** it was made (problem context)
- **How** it's implemented (with code examples)
- **Trade-offs** (what was gained/lost)
- **Alternatives** considered

## When to Write an ADR

Write an ADR when making decisions that:
1. **Impact the entire system** (database choice, framework selection, deployment strategy)
2. **Are difficult to reverse** (DynamoDB single-table design, monorepo structure)
3. **Involve significant trade-offs** (tRPC vs REST, Remix vs Next.js)
4. **Set architectural patterns** (entity structure, error handling, authentication)
5. **Require future context** (why we chose this approach over alternatives)

### Examples of ADR-Worthy Decisions
- ✅ Choosing DynamoDB single-table design
- ✅ Selecting tRPC over REST
- ✅ Email blacklist management strategy
- ✅ Fresh user data from database vs JWT
- ✅ Monorepo with pnpm workspaces

### Examples of Non-ADR Decisions
- ❌ Adding a new field to an entity (routine change)
- ❌ Refactoring a component (implementation detail)
- ❌ Fixing a bug (not an architectural decision)
- ❌ Updating dependencies (maintenance task)

## ADR Format and Structure

### File Naming Convention
```
docs/architecture-decisions/adr-NNN-kebab-case-title.md
```

- **NNN**: Zero-padded 3-digit number (001, 002, 015, etc.)
- **kebab-case-title**: Descriptive, lowercase, hyphen-separated

### Document Structure

Every ADR follows this structure:

```markdown
# ADR-NNN: Title (Clear, Concise Description)

**Date:** YYYY-MM-DD
**Status:** Accepted | Proposed | Deprecated | Superseded
**Context:** One-line summary of when/why this decision was needed

---

## Problem

[Detailed problem description with 3-5 paragraphs]

### Option 1: [First Alternative]
[Code example or description]

**Problems:**
- List specific issues
- Technical limitations
- Business concerns

### Option 2: [Second Alternative]
[Code example or description]

**Problems:**
- List specific issues

### Option 3: [Chosen Approach]
[Code example or description]

**Benefits:**
- Why this is better
- Advantages over alternatives

---

## Decision

**Use [Chosen Approach] for [Purpose].**

[1-2 paragraph explanation of the decision]

**Why [Chosen Approach]:**
1. Reason 1
2. Reason 2
3. Reason 3

---

## Implementation

[Detailed implementation with code examples]

### 1. [First Implementation Aspect]
[Code examples with comments]

### 2. [Second Implementation Aspect]
[Code examples with comments]

[Continue for all major implementation aspects]

---

## Benefits

### 1. **[Benefit Name]**
[Explanation with code/metrics examples]

### 2. **[Benefit Name]**
[Explanation with code/metrics examples]

[Continue for all major benefits]

---

## Trade-offs

### What We Gained
- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

### What We Lost
- ❌ Limitation 1
- ❌ Limitation 2
- ❌ Limitation 3

### Why Trade-offs Are Acceptable
1. **Limitation 1**: Explanation of why it's acceptable
2. **Limitation 2**: Explanation
3. **Limitation 3**: Explanation

---

## Comparison

| Feature | Alternative 1 | Alternative 2 | Chosen Approach |
|---------|--------------|---------------|-----------------|
| **Metric 1** | Value | Value | Value |
| **Metric 2** | Value | Value | Value |

---

## Real-World Example

### Scenario: [Concrete Use Case]

**With [Alternative Approach]:**
```
[Step-by-step flow showing problems]
```

**With [Chosen Approach]:**
```
[Step-by-step flow showing benefits]
```

**Winner:** [Chosen Approach] ([quantified benefit])

---

## Future Considerations

### [Future Topic 1]
[Discussion of how this decision might evolve]

### [Future Topic 2]
[Potential extensions or modifications]

**Current Status:** [Current state and future plans]

---

## Related Files

### [Category 1]
- `path/to/file1.ts` - Description
- `path/to/file2.ts` - Description

### [Category 2]
- `path/to/file3.ts` - Description

---

## References

- **[Resource Name]**: [URL]
- **[Documentation]**: [URL]
- Related: [Cross-reference to other ADRs]
```

## Writing Guidelines

### 1. Title and Header

**Title Format:**
```markdown
# ADR-NNN: Clear, Concise Description
```

### 2. Problem Section

The Problem section should:
- **Explain the context** (3-5 paragraphs minimum)
- **Show code examples** of the problem or alternatives
- **List 2-4 alternatives** considered
- **Explain trade-offs** for each alternative

### 3. Decision Section

**Format:**
```markdown
## Decision

**Use [Technology/Pattern] for [Purpose].**

[1-2 paragraph justification]

**Why [Chosen Approach]:**
1. Reason 1 (with evidence)
2. Reason 2 (with evidence)
3. Reason 3 (with evidence)
```

### 4. Implementation Section

The Implementation section should:
- **Show working code examples** (not pseudocode)
- **Include file paths** in code comments
- **Explain key patterns** with inline comments
- **Cover all major aspects** of implementation

### 5. Benefits Section

**Format:**
```markdown
## Benefits

### 1. **[Concrete Benefit]**
[Explanation with evidence]

### 2. **[Concrete Benefit]**
[Explanation with evidence]
```

### 6. Trade-offs Section

**Format:**
```markdown
## Trade-offs

### What We Gained
- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

### What We Lost
- ❌ Limitation 1
- ❌ Limitation 2
- ❌ Limitation 3

### Why Trade-offs Are Acceptable

1. **Limitation 1**: Detailed explanation of why this is acceptable
2. **Limitation 2**: Explanation with context
3. **Limitation 3**: Explanation
```

### 7. Comparison Section

Use tables to compare alternatives across multiple dimensions:

```markdown
## Comparison

| Feature | Alternative 1 | Alternative 2 | Chosen Approach |
|---------|--------------|---------------|-----------------|
| **Feature 1** | ❌ No | ⚠️ Partial | ✅ Yes |
| **Feature 2** | Value | Value | Value |
| **Cost** | $X/month | $Y/month | $Z/month |
| **Performance** | Metric | Metric | Metric |
```

### 8. Real-World Example

Provide a concrete scenario showing the decision in action:

```markdown
## Real-World Example

### Scenario: Add "dateOfBirth" field to User

**With Polyrepo (Multi-Repository):**
```bash
# 1. Update core
cd vedaghosham-core
# Edit User entity
git commit -m "Add dateOfBirth"
npm version patch      # 1.2.0 → 1.2.1
npm publish

# 2. Update API
cd ../vedaghosham-api
npm install @vedaghosham/core@1.2.1  # Wait for npm registry propagation
# Update API code
git commit -m "Support dateOfBirth"

# 3. Update Web
cd ../vedaghosham-web
npm install @vedaghosham/core@1.2.1
# Update web code
git commit -m "Show dateOfBirth in profile"

# Total time: 30-60 minutes
```

**With Monorepo (Chosen Approach):**
```bash
# 1. Update core
cd packages/core/src/user
# Edit entity.ts and types.ts

# 2. Update functions (TypeScript error guides you!)
cd packages/functions/src/user
# Update router.ts

# 3. Update web (TypeScript error guides you!)
cd packages/web/app/routes
# Update profile route

# 4. Commit everything
git commit -m "Add dateOfBirth field"

# Total time: 5-10 minutes ✅
```

**Winner:** Monorepo (6× faster, no versioning hassle)
```

### 9. Future Considerations

Discuss how the decision might evolve:

```markdown
## Future Considerations

### Adding Public API
If we need a public API (for mobile apps, third-party integrations):
- **Option A**: Keep tRPC for internal use; add separate REST API for public
- **Option B**: Use tRPC + tRPC-OpenAPI adapter (generates OpenAPI from tRPC)

**Current Status:** Internal API only; no public API needed yet.

### Non-TypeScript Clients
If we need Python/Go clients:
- **Option A**: Create thin REST wrapper around tRPC backend
- **Option B**: Use HTTP directly (tRPC is just JSON-RPC over HTTP)

**Current Status:** Full TypeScript stack; no other languages planned.
```

### 10. Related Files

List all files implementing the decision:

```markdown
## Related Files

### Backend
- `packages/functions/src/shared/trpc.ts` - tRPC initialization
- `packages/functions/src/shared/middleware.ts` - Auth middleware
- `packages/functions/src/{entity}/router.ts` - Entity routers

### Frontend
- `packages/web/app/lib/trpc.ts` - tRPC client factory
- `packages/web/app/routes/_app.*.tsx` - Usage in Remix routes

### Schemas
- `packages/core/src/{entity}/schema.ts` - Zod schemas used by tRPC
```

### 11. References

Include all relevant resources:

```markdown
## References

- **tRPC Documentation**: https://trpc.io/
- **tRPC vs REST**: https://trpc.io/docs/concepts
- **ElectricSQL tRPC Talk**: https://www.youtube.com/watch?v=2LYM8gf184U
- **Zod Validation**: https://zod.dev/
- Related: ADR-004 (Single-Table DynamoDB)
- Related: ADR-010 (Zod Shared Validation)
```

## Additional Guidelines for Layer 5 ADRs

### Purpose

Create **Architecture Decision Records (ADR)** - Layer 5 artifact in the SDD workflow that documents architectural decisions with rationale, alternatives, and consequences.

**Layer**: 5

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4)

**Downstream Artifacts**: SYS (Layer 6), REQ (Layer 7), Code (Execution Layer)

### Prerequisites

Before creating an ADR, ensure the following:
1. Verify existing upstream artifacts.
2. Reference only existing documents in traceability tags.
3. Use `null` only when upstream artifact type genuinely doesn't exist.
4. Never use placeholders like `BRD-XXX` or `TBD`.

### ADR Document Categories

| Category | Filename Pattern | Validation Level | Description |
|----------|------------------|------------------|-------------|
| **Standard ADR** | `ADR-NN_{decision_topic}.md` | Full (7 checks) | Architecture decision records |
| **ADR-REF** | `ADR-REF-NN_{slug}.md` | Reduced (4 checks) | Supplementary reference documents |

### ADR Lifecycle States

- **Proposed**: Decision under consideration.
- **Accepted**: Decision approved and active.
- **Deprecated**: Decision no longer recommended.
- **Superseded by ADR-XXX**: Replaced by newer decision.

### SYS-Ready Scoring System

**Purpose**: Measures ADR maturity and readiness for progression to System Requirements (SYS) phase.

**Format in Document Control**:
```markdown
| **SYS-Ready Score** | ✅ 95% (Target: ≥90%) |
```

### Element ID Format (MANDATORY)

**Pattern**: `ADR.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Decision | 10 | ADR.02.10.01 |
| Alternative | 12 | ADR.02.12.01 |
| Consequence | 13 | ADR.02.13.01 |

## Conclusion

Use this skill to create comprehensive ADRs that document architectural decisions effectively, ensuring clarity and traceability throughout the project lifecycle. Follow the structured guidelines to maintain high-quality documentation that serves as a valuable resource for current and future team members.