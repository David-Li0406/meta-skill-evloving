# Decision Types: ADR vs DES

Guidance on when to create Architecture Decision Records (ADRs) vs Design Patterns (DES).

## Overview

| Document | Purpose | Scope | When to Create |
|----------|---------|-------|----------------|
| **ADR** | Hard-to-change architectural choices | Project-wide | Once, when making the decision |
| **DES** | Repeatable cross-cutting patterns | Project-wide | When pattern is used 2+ times |

## Architecture Decision Records (ADRs)

### What They Document

- **Technology choices**: Database, framework, language, libraries
- **Architectural patterns**: Monolith vs microservices, sync vs async
- **Integration approaches**: API design, message queues, event sourcing
- **Infrastructure decisions**: Hosting, CI/CD, deployment strategy

### Characteristics

- **Hard to change**: Reversing the decision is expensive
- **One-time**: The decision is made once
- **Consequential**: Affects many parts of the system
- **Context-dependent**: The choice depends on project constraints

### Status Lifecycle

```
Proposed → Accepted → [Superseded]
```

- **Proposed**: Under discussion
- **Accepted**: Decision made and in effect
- **Superseded**: Replaced by a newer ADR (reference the new one)

### File Naming

```
docs/architecture/ADR-XXX-short-title.md
```

Example: `ADR-007-logging-library.md`

## Design Patterns (DES)

### What They Document

- **Code patterns**: How to structure specific types of code
- **Conventions**: Naming, file organization, error handling
- **Cross-cutting concerns**: Logging, configuration, testing
- **Reusable solutions**: Patterns that apply across features

### Characteristics

- **Repeatable**: Used in multiple places
- **Evolving**: Can be refined as better approaches emerge
- **Prescriptive**: Tells developers HOW to do something
- **Consistent**: Ensures uniform approach across codebase

### Version History

DES documents can evolve. Keep a version history:

```markdown
## Version History
- v1.0: Initial pattern
- v1.1: Added edge case handling
- v2.0: Major revision for async support
```

### File Naming

```
docs/design/DES-XXX-pattern-name.md
```

Example: `DES-003-testing-patterns.md`

## Decision Tree

```
Is this about WHAT technology/approach to use?
├─ Yes → Is it hard to reverse?
│        ├─ Yes → ADR
│        └─ No → Consider if it's even worth documenting
└─ No → Is this about HOW to implement something?
         ├─ Yes → Is it used in 2+ places?
         │        ├─ Yes → DES
         │        └─ No → Document in feature design instead
         └─ No → Probably doesn't need documentation
```

## Examples

### ADR Examples

| Topic | Why ADR |
|-------|---------|
| Use PostgreSQL for database | Changing DB later is very expensive |
| Adopt microservices architecture | Fundamental structural decision |
| Use OAuth2 for authentication | Security architecture choice |
| Choose Kubernetes for orchestration | Infrastructure commitment |

### DES Examples

| Topic | Why DES |
|-------|---------|
| Logging conventions | Applied throughout codebase |
| Error handling patterns | Cross-cutting concern |
| Test organization | Consistency across all tests |
| Configuration loading | Used by multiple modules |

## Creating Decisions

### When to Create an ADR

1. You're choosing between competing technologies
2. The choice will affect multiple features
3. Reversing the choice would require significant rework
4. Future developers need to understand why this choice was made

### When to Create a DES

1. You've implemented the same pattern twice
2. You want all future implementations to be consistent
3. The pattern solves a cross-cutting concern
4. Onboarding developers need to learn "how we do X here"

## Referencing Decisions

### In Code

```python
# See ADR-007: Why we chose loguru for logging
logger = loguru.logger

# See DES-003: Test organization patterns
class TestFeatureX:
    ...
```

### In Feature Designs

```markdown
## Key Decisions

- **Logging**: Follows DES-001 logging conventions
- **Database**: Uses PostgreSQL per ADR-003
```

## Updating Decisions

### ADR Updates

- **Minor clarification**: Edit the existing ADR
- **Major change**: Create new ADR that supersedes the old one

### DES Updates

- **Refinement**: Update the existing DES, add version history
- **Complete overhaul**: Create new version in same file, document migration
