---
name: spec-authoring
description: Author ADR, PRD, and SDS specifications following SEA™ templates with full traceability. Use when creating architecture decision records (ADRs), product requirement documents (PRDs), or software design specifications (SDS) that require proper spec-to-code traceability and document relationships.
---

# Specification Authoring Skill

Creates properly structured ADR, PRD, and SDS documents with full traceability.

## Document Types

### ADR (Architecture Decision Record)
**Purpose**: Capture architecture decisions with context, options, and consequences.

**Template Fields**:
- ADR-ID (e.g., ADR-031)
- Status (Proposed, Accepted, Deprecated)
- Context & Problem Statement
- Decision Drivers
- Considered Options
- Decision Outcome
- Consequences (positive, negative, neutral)
- Links to follow-up PRDs/SDS

### PRD (Product Requirement Document)
**Purpose**: Define product requirements and acceptance criteria.

**Template Fields**:
- PRD-ID (e.g., PRD-020)
- Problem Statement
- User Stories (EARS format)
- Functional Requirements (FR-###)
- Non-Functional Requirements (NFR-###)
- Acceptance Criteria
- Traceability to ADRs

### SDS (Software Design Specification)
**Purpose**: Detailed technical design with SEA-DSL flows.

**Format**: YAML frontmatter + Markdown content

**Template Fields**:
- SDS-ID (e.g., SDS-045)
- Bounded Context
- Service/Component name
- Implements (ADR/PRD references)
- SEA-DSL specification
- API contracts
- Invariants

## Traceability Chain

```
ADR → PRD → SDS → SEA-DSL → Generated Code
```

Each document MUST reference its upstream documents:
- SDS must reference PRD and/or ADR it implements
- PRD must reference ADR it satisfies

## Workflow

1. Identify what decision/requirement/design to document
2. Choose appropriate document type (ADR/PRD/SDS)
3. Use `/spec` workflow to create from template
4. Fill in all required fields
5. Add traceability links
6. Validate with `just spec-guard`

## File Locations

| Type | Path Pattern |
|------|--------------|
| ADR | `docs/specs/<context>/adr/<###>-<name>.md` |
| PRD | `docs/specs/<context>/prd/<###>-<name>.md` |
| SDS | `docs/specs/<context>/sds/<###>-<name>.sds.yaml` or `.md` |

## Related Skills

- [sea-dsl-authoring](../sea-dsl-authoring/SKILL.md)
- [governance-validation](../governance-validation/SKILL.md)
