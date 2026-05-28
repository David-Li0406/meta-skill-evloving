---
name: product-development
description: Guides product development from requirements through design specifications. Covers product requirements, technical requirements, architecture, and interface contracts with iterative review loops. Use when planning new features, services, CLI tools, APIs, or infrastructure. Run software-engineering skill after to implement.
---

# Product Development Workflow

Requirements gathering and design with iterative review loops. Produces artifacts for implementation.

## When to Use

- Planning new backend services, APIs, or microservices
- Designing CLI tools or developer utilities
- Architecting frontend applications or components
- Planning infrastructure or platform capabilities
- Any project needing systematic requirements and design

## Role Boundaries

| Activity | Claude | User |
|----------|--------|------|
| Draft requirements | ✅ Proposes structure, asks questions | Provides domain knowledge |
| Write user stories | ✅ Drafts based on discussion | Reviews, corrects, approves |
| Technical decisions | ✅ Presents options with trade-offs | Selects option, approves |
| Create diagrams | ✅ Generates via `diagrams-kroki` | Reviews for accuracy |
| Approval gates | ✅ Summarizes, asks for approval | Approves / requests changes |

## Iteration Limits

Each phase allows **max 3 iterations** before escalation:

| Iteration | Action |
|-----------|--------|
| 1st | Initial draft → user feedback |
| 2nd | Revised draft → user feedback |
| 3rd | Final revision → must approve or descope |
| Blocked | Escalate: "Requirements may be infeasible. Options: (A) Reduce scope, (B) Accept risks, (C) Abandon" |

## Artifacts Location

All outputs go to `./planning/{YYYYMMDD}_{project}/`:

```
./planning/20260116_my-service/
├── PROJECT.md                    # Status dashboard
├── requirements/
│   ├── PRODUCT-REQUIREMENTS.md   # Phase 1 output
│   ├── TECHNICAL-REQUIREMENTS.md # Phase 2 output
│   └── TRACEABILITY.md           # Phase 3 output
├── diagrams/                     # Phase 4-5 outputs
│   ├── architecture/
│   ├── behavior/
│   └── data/
└── design/
    ├── ARCHITECTURE.md           # Phase 5 output
    └── INTERFACES.md             # Phase 6 output
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCT DEVELOPMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Product Requirements ←─── Clarify Loop ──→ Approved   │
│                                                                 │
│  Phase 2: Technical Requirements ←─ Clarify Loop ──→ Approved   │
│                                                                 │
│  Phase 3: Requirements Integration ← Review Loop ──→ Approved   │
│                    │                     ▲                      │
│                    └─────────────────────┘                      │
│                    (gaps found → back to Phase 1 or 2)          │
│                                                                 │
│  Phase 4: Diagrams & Artifacts ←──── Review Loop ──→ Approved   │
│                                                                 │
│  Phase 5: Architecture & Design ←─── Review Loop ──→ Approved   │
│                    │                     ▲                      │
│                    └─────────────────────┘                      │
│                    (issues found → back to earlier phase)       │
│                                                                 │
│  Phase 6: Interface Contracts ←───── Review Loop ──→ Approved   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Run `software-engineering` skill
                    to implement the design
```

## Product Type Guides

Select based on what you're building:

- **Backend Services/APIs**: See [product-types/BACKEND.md](product-types/BACKEND.md)
- **CLI Tools**: See [product-types/CLI.md](product-types/CLI.md)
- **Frontend Applications**: See [product-types/FRONTEND.md](product-types/FRONTEND.md)
- **Infrastructure**: See [product-types/INFRASTRUCTURE.md](product-types/INFRASTRUCTURE.md)

## Companion Skills

| Task | Skill | When |
|------|-------|------|
| Create diagrams | `diagrams-kroki` | Phases 4-5 |
| **Implement design** | `software-engineering` | After Phase 6 |
| Setup environment | `nix-devenv` | Before implementation |
| Documentation | `sphinx-docs` | Throughout |
| **Complexity scoring** | `dynamic-tasks` | For iteration planning |

## Planning Structure

See [planning/STRUCTURE.md](planning/STRUCTURE.md) for templates.

```
./planning/{YYYYMMDD}_{project}/
├── PROJECT.md              # Status & overview
├── requirements/           # Phase 1-3 outputs
├── diagrams/               # Phase 4-5 outputs
├── design/                 # Phase 5-6 outputs
└── epics/                  # Work breakdown
```

---

## Phase 1: Product Requirements

**Goal**: Define WHO uses the product and WHAT they expect.

### Clarify Loop

```
Draft Requirements → Review with User → Gaps/Issues?
        ▲                                    │
        │              Yes                   │ No
        └────────────────┘                   ▼
                                         Approved
```

### Key Activities

1. **Identify personas**: Who are the users? What are their goals?
2. **Write user stories**: "As a [X], I expect to [Y] so that [Z]"
3. **Define boundaries**: What's in/out of scope?
4. **Success criteria**: How do we know it works?

### Critical Questions

- Who is NOT a user?
- What happens when expectations aren't met?
- Are there conflicting user needs?

### Approval Gate

```markdown
## Phase 1: Product Requirements

**Personas Defined**: X
**User Stories**: Y
**Boundaries**: Documented

**Gaps or Issues?**
- [ ] Any personas missing?
- [ ] Any user stories unclear?
- [ ] Scope concerns?

If gaps → Clarify and iterate
If clear → **Approve to proceed**
```

See [phases/01-PRODUCT-REQUIREMENTS.md](phases/01-PRODUCT-REQUIREMENTS.md) for details.

---

## Phase 2: Technical Requirements

**Goal**: Define WHAT the technology must do to meet user needs.

### Clarify Loop

```
Draft Tech Reqs → Review with User → Feasible? Complete?
        ▲                                    │
        │              No                    │ Yes
        └────────────────┘                   ▼
                                         Approved
```

### Key Activities

1. **Translate stories** to technical capabilities
2. **Define NFRs**: Performance, security, scalability
3. **Identify constraints**: Tech stack, integrations, resources
4. **Specify data**: Models, storage, retention

### Critical Questions

- Can we actually build this?
- What are the failure modes?
- What technical debt are we accepting?

### Approval Gate

```markdown
## Phase 2: Technical Requirements

**Capabilities**: X technical requirements
**NFRs**: Performance, security, scalability defined
**Constraints**: Documented

**Feasibility Issues?**
- [ ] Any requirements unbuildable?
- [ ] Resource constraints?
- [ ] Technical risks?

If issues → Clarify and iterate
If feasible → **Approve to proceed**
```

See [phases/02-TECHNICAL-REQUIREMENTS.md](phases/02-TECHNICAL-REQUIREMENTS.md) for details.

---

## Phase 3: Requirements Integration

**Goal**: Link product ↔ technical requirements, identify gaps.

### Review Loop

```
Create Traceability → Review Mapping → Gaps Found?
        ▲                                  │
        │         Yes (go back)            │ No
        └─── to Phase 1 or 2 ──────────────▼
                                       Approved
```

### Key Activities

1. **Traceability matrix**: User story → technical requirement
2. **Find orphans**: Technical reqs without product justification
3. **Find gaps**: User needs without technical solutions
4. **Prioritize**: By user impact

### Critical Questions

- Does every technical requirement serve a user need?
- Are all user stories technically addressed?
- What's the minimum viable scope?

### Approval Gate

```markdown
## Phase 3: Requirements Integration

**Traceability**: All stories mapped to technical reqs
**Orphans**: X technical reqs without user justification
**Gaps**: Y user needs without technical solutions

**Action Required?**
- If orphans → Remove or justify (back to Phase 2)
- If gaps → Add technical solution (back to Phase 1/2)
- If complete → **Approve to proceed**
```

See [phases/03-REQUIREMENTS-INTEGRATION.md](phases/03-REQUIREMENTS-INTEGRATION.md) for details.

---

## Phase 4: Diagrams & Artifacts

**Goal**: Visualize user journeys and system behavior.

### Review Loop

```
Create Diagrams → Review Coverage → All Paths Covered?
        ▲                                  │
        │              No                  │ Yes
        └──────────────┘                   ▼
                                       Approved
```

### Key Artifacts

- Use case diagrams (actor → system)
- State diagrams (system states/transitions)
- User flow diagrams (step-by-step journeys)
- Error/edge case mappings

Use `diagrams-kroki` skill for diagram generation.

### Approval Gate

```markdown
## Phase 4: Diagrams & Artifacts

**Diagrams Created**:
- [ ] Use cases: X diagrams
- [ ] State machines: Y diagrams
- [ ] User flows: Z diagrams
- [ ] Error cases: Documented

**Coverage Complete?**
If missing paths → Add diagrams and iterate
If complete → **Approve to proceed**
```

See [phases/04-DIAGRAMS-ARTIFACTS.md](phases/04-DIAGRAMS-ARTIFACTS.md) for details.

---

## Phase 5: Architecture & Design

**Goal**: Define system structure and component relationships.

### Review Loop

```
Create Architecture → Review Design → Sound & Complete?
        ▲                                  │
        │              No                  │ Yes
        │    (may need earlier phase)      │
        └──────────────────────────────────▼
                                       Approved
```

### Key Artifacts

- C4 diagrams (context, container, component)
- Class/module diagrams
- Sequence diagrams (key interactions)
- Data models and schemas

### Approval Gate

```markdown
## Phase 5: Architecture & Design

**Architecture Defined**:
- [ ] C4 Context diagram
- [ ] C4 Container diagram
- [ ] Component diagrams
- [ ] Data models

**Design Sound?**
- [ ] Meets NFRs?
- [ ] Addresses all use cases?
- [ ] No major risks?

If issues → Iterate (may need Phase 1-4 changes)
If sound → **Approve to proceed**
```

See [phases/05-ARCHITECTURE-DESIGN.md](phases/05-ARCHITECTURE-DESIGN.md) for details.

---

## Phase 6: Interface Contracts

**Goal**: Define all interaction boundaries.

### Review Loop

```
Define Contracts → Review Completeness → All Interfaces Covered?
        ▲                                       │
        │                  No                   │ Yes
        └──────────────────┘                    ▼
                                            Approved
```

### Interface Types

| Product Type | Interfaces |
|--------------|------------|
| **API** | OpenAPI spec, request/response schemas |
| **CLI** | Command syntax, flags, I/O formats |
| **Frontend** | Component props, state shapes |
| **Infrastructure** | Config schemas, resource definitions |

### Approval Gate

```markdown
## Phase 6: Interface Contracts

**Contracts Defined**:
- [ ] API endpoints: X with full specs
- [ ] CLI commands: Y with syntax
- [ ] Events/messages: Z with schemas

**All Interfaces Covered?**
If missing → Add contracts and iterate
If complete → **Approve and proceed to implementation**
```

See [phases/06-INTERFACE-CONTRACTS.md](phases/06-INTERFACE-CONTRACTS.md) for details.

---

## Completion & Handoff

```markdown
## Product Development Complete

**Artifacts Produced**:
- [ ] Product requirements (personas, stories, boundaries)
- [ ] Technical requirements (capabilities, NFRs, constraints)
- [ ] Traceability matrix
- [ ] Diagrams (use case, state, flow, architecture)
- [ ] Interface contracts

**Ready for Implementation**:
Run `software-engineering` skill with these artifacts.

**Planning Location**: ./planning/{project}/
```

---

## Interaction Style

1. **Iterate**: Use review loops, don't assume first draft is final
2. **Clarify**: Ask questions, surface assumptions
3. **Show Trade-offs**: Every decision has pros/cons
4. **Recommend Clearly**: Mark recommended option with **
5. **Wait for Approval**: Never proceed without user confirmation
6. **Link to Users**: Connect every decision to user impact
