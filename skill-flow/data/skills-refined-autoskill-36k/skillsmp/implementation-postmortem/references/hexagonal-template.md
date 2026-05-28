# Hexagonal Architecture Postmortem Template

Use this template when reviewing implementations following the hexagonal (ports and adapters) pattern.

## Architecture-Specific Dimensions

### Domain Layer Integrity

**Examine:**
- Did business logic leak into adapters?
- Are domain entities anaemic (data bags) or do they encapsulate behaviour?
- Were domain concepts discovered that the spec didn't anticipate?
- Are domain operations expressed in ubiquitous language?

**Questions:**
- Can domain logic be tested without any infrastructure?
- Do domain types depend on adapter types? (violation)
- Are validation rules in the domain or scattered across adapters?

### Port Design

Ports are the interfaces the domain exposes (driven) or requires (driving).

**Driven ports (inbound):**
- Do port interfaces represent domain operations, not infrastructure operations?
- Are port method signatures stable across adapter changes?
- Could you add a new entry point (CLI, API, queue) without touching domain code?

**Driving ports (outbound):**
- Do ports represent domain needs abstractly? ("persist order" not "INSERT INTO orders")
- Are ports minimal? (No methods the domain doesn't actually need)
- Could you swap implementations without the domain knowing?

**Smell test:** Read a port interface. Does it mention any infrastructure concepts (HTTP, SQL, files)? If yes, it's leaking.

### Adapter Assessment

For each adapter:

| Adapter | Type | Lines | Boilerplate % | Logic % | Verdict |
|---------|------|-------|---------------|---------|---------|
| | in/out | | | | thin/concerning |

**Red flags:**
- Adapter > 200 lines (probably doing too much)
- Adapter contains business rules (should be in domain)
- Adapter imports domain internals (should only use ports)
- Multiple adapters duplicating logic (extract to shared infrastructure)

**Per-adapter questions:**
- How much is genuine translation vs ceremony?
- What would break if the external system changed its API?
- Are adapter-specific errors translated to domain errors?

### Dependency Direction

The fundamental rule: dependencies point inward (adapters → ports → domain).

**Check:**
- Domain crate/module has zero infrastructure dependencies?
- Ports defined in domain, implemented in adapters?
- No circular dependencies between layers?

**Visualise:** Draw the actual dependency graph. Compare to intended hexagonal structure. Explain every deviation.

### Application Service Layer

If present (orchestrating domain operations):

- Are services thin coordinators or growing their own logic?
- Transaction boundaries clear?
- Do services depend on ports (good) or concrete adapters (bad)?

## Hexagonal-Specific Smells

| Smell | Symptom | Likely Cause |
|-------|---------|--------------|
| Anaemic domain | Domain types are just data; all logic in services | Missing domain methods; procedural thinking |
| Fat adapter | Adapter > 300 lines with business logic | Domain responsibilities leaked outward |
| Port explosion | Many fine-grained ports | Over-abstraction; ports should represent capabilities |
| Adapter coupling | Changing one adapter requires changing another | Shared state or missing abstraction |
| Infrastructure in domain | Domain imports HTTP/SQL/file types | Dependency inversion violated |

## Testing Strategy Assessment

| Layer | Test Type | Coverage | Notes |
|-------|-----------|----------|-------|
| Domain | Unit (no mocks needed) | | |
| Ports | Contract tests | | |
| Adapters | Integration (real infra) | | |
| Application | Use-case tests (mocked ports) | | |

**Questions:**
- Can domain tests run without any test infrastructure?
- Are adapter tests isolated from each other?
- Do integration tests verify port contracts?
