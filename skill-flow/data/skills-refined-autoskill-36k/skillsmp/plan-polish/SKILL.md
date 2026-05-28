---
name: plan-polish
description: Convert rough plans into implementation-grade Technical Design Documents for autonomous agent execution
---

# Plan Polish Workflow

Convert rough plans into implementation-ready Technical Design Documents that multiple autonomous agents can execute with minimal guesswork.

## When to use

Use when you have:
- A rough plan or idea from Stage 1
- An INTAKE.md specifying the track (S/M/L) and research mode
- RESEARCH_DOSSIER.md (required when `researchMode != none`)
- Need to create a detailed, implementation-grade design document
- Want to prepare work for autonomous coding agents

## Role

You are a Principal Software Architect tasked with converting rough plans into air-tight design documents.

## Required inputs

- **INTAKE.md** from Stage 0 (determines track and schema)
- **Rough plan** from Stage 1
- **RESEARCH_DOSSIER.md** (required when `researchMode: targeted` or `researchMode: deep`)
- **Relevant repo context**: file tree, key files, conventions, existing patterns
- **Current dependency manifest**: `package.json`, `requirements.txt`, `pyproject.toml`
- **External APIs/services**: documentation links if available

## Track-Aware Schema Selection

Read `track` from INTAKE.md to determine output schema:

- **Track S**: Skip this skill entirely (simple tasks don't need TDD)
- **Track M**: Use **Lite Schema** (8 sections)
- **Track L**: Use **Full Schema** (14 sections)

## Critical constraints

- **Do NOT write implementation code yet**
- Add detail aggressively; resolve ambiguities where possible
- If something depends on ecosystem/version/library behavior, call it out
- If you cannot verify a fact (no access to docs), explicitly mark it **UNVERIFIED**
- Optimize for correctness and zero-guesswork over brevity

## Mandatory verification

### V1. Dependency & Version Audit
For each external package/library mentioned:
- Current version in this project (if known)
- Recommended stable version (if you can verify)
- Breaking changes / migration concerns
- Correct import / usage style (if you can verify)
- Potential conflicts with other dependencies

### V2. API / SDK Surface Verification
For each external API/SDK call you expect to use:
- Endpoint / method name
- Required vs optional parameters
- Return shape (fields/types)
- Error cases and how they present
- Rate limits / quotas (if applicable)

### V3. Codebase Integration Check
- Existing patterns to follow (and where)
- Files that will be **modified**
- Files that will be **created**
- Helpers/utilities to reuse
- Naming, error-handling, testing conventions

### V4. Edge Case Enumeration
For each major component:
- Happy path
- Empty/null inputs
- Malformed inputs
- Timeout/failure cases
- Concurrency/state issues (if applicable)
- First-run / re-run / partial completion behavior

### V5. Integration Point Analysis
For each boundary between components:
- Data format crossing the boundary
- Validation requirements
- Error propagation strategy
- Logging/observability needs

## Output: TECHNICAL_DESIGN.md

Create `docs/plans/<project>/TECHNICAL_DESIGN.md` with YAML frontmatter:

```yaml
---
schemaVersion: 1
artifactType: technical_design
project: "<project-slug>"
createdAt: "YYYY-MM-DD"
track: M|L
detailLevel: lite|full
sourceIntake: "docs/plans/<project-slug>/INTAKE.md"
sourceResearch: "docs/plans/<project-slug>/RESEARCH_DOSSIER.md"  # if applicable
---
```

---

## Lite Schema (Track M) - EXACTLY 8 Sections

Use for Track M plans. Focused on essentials for moderate complexity work.

### 1. Executive Summary
- What we're building and why
- What changes (high level)

### 2. Context & Constraints
- Repo constraints, runtime constraints, security/compliance, performance
- **Required:** At least 3 best-practice/pitfall bullets relevant to this work
  - If best practices cannot be verified, mark as UNVERIFIED with "How to verify:"

### 3. Assumptions
- **Validated:** (with source)
- **Invalidated:** (with source)
- **Unverified:** (with "How to verify:")

### 4. Architecture
- Components and responsibilities
- Key flows (short)

### 5. Component Design
For each component:
- **Purpose**
- **Dependencies:** external + internal
- **Interface Contract:** inputs/outputs/errors (types/schemas)
- **Behavior:** step-by-step logic flow
- **Files affected:** create/modify (with brief notes)

### 6. Error Handling
- Error taxonomy (what can go wrong)
- User-visible vs internal errors
- Retry/backoff decisions (if relevant)

### 7. Testing Strategy
- Unit tests (what to cover)
- Integration tests (what boundaries)
- Commands to run

### 8. Open Questions
Split into:
- **Blocking:** (must resolve before implementation)
- **Non-blocking:** (can defer)

---

## Full Schema (Track L) - EXACTLY 14 Sections

Use for Track L plans. Comprehensive coverage for complex, high-risk work.

### 1. Executive Summary
- What we're building and why
- What changes (high level)

### 2. Context & Constraints
- Repo constraints, runtime constraints, security/compliance, performance

### 3. Assumptions
- **Validated:** (with source)
- **Invalidated:** (with source)
- **Unverified:** (with "How to verify:")

### 4. Architecture
- Components and responsibilities
- Key flows (short)

### 5. Data Structures
Define the exact shape of data passing between modules:
- Schemas / types
- Serialization formats
- Validation rules

### 6. Component Design
For each component:
- **Purpose**
- **Dependencies:** external + internal
- **Interface Contract:** inputs/outputs/errors (types/schemas)
- **Behavior:** step-by-step logic flow (including "if X fails, then Y happens")
- **Edge cases:** expected behavior
- **Files affected:** create/modify (with brief notes)

### 7. Dependency Notes
- Package versions / docs URLs assumed
- Any known version-sensitive gotchas

### 8. Error Handling
- Error taxonomy (what can go wrong)
- User-visible vs internal errors
- Retry/backoff/circuit-breaking decisions (if relevant)

### 9. Testing Strategy
- Unit tests (what to cover)
- Integration/E2E tests (what boundaries)
- Test data/fixtures
- Commands to run (if known)

### 10. Operational Concerns
- Logging/metrics/tracing
- Config/feature flags
- Rollout/migrations
- Backward compatibility
- **Required:** At least 3 best-practice/pitfall bullets relevant to this work
  - If best practices cannot be verified, mark as UNVERIFIED with "How to verify:"

### 11. Dependency Graph
Mermaid or ASCII diagram of component dependencies.

### 12. Implementation Order
Ordered steps with reasoning.

### 13. Tradeoffs
List decisions and what you chose *not* to do.

### 14. Open Questions
Split into:
- **Blocking:** (must resolve before implementation)
- **Non-blocking:** (can defer)

## Quality Gate

Before finishing, confirm:

### Schema compliance
- [ ] Correct schema used (lite for Track M, full for Track L)
- [ ] YAML frontmatter includes all required fields (schemaVersion, artifactType, project, track, detailLevel)
- [ ] All required sections present (8 for lite, 14 for full)

### Content quality
- [ ] Every external call signature is specified or marked **UNVERIFIED** with "How to verify:"
- [ ] Every edge case has an explicit expected behavior (full schema only)
- [ ] Every file touched is listed in Component Design
- [ ] No "TODO / figure out later" remains outside Open Questions section
- [ ] At least 3 best-practice/pitfall bullets in:
  - Context & Constraints (lite schema)
  - Operational Concerns (full schema)

### Research integration (when researchMode != none)
- [ ] All Verified Facts from RESEARCH_DOSSIER.md are incorporated
- [ ] All UNVERIFIED items either resolved or carried forward with "How to verify:"
- [ ] Decisions Required from dossier addressed or moved to Open Questions

## Next Steps

After TECHNICAL_DESIGN.md is complete:
- **Track M**: Proceed to `/write-beads`
- **Track L**: Proceed to `/review-design` first, then `/write-beads` after approval
