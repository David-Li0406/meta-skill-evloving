---
name: requirements-architect
description: "Generate implementation-ready documentation from PRD/FRD files including Functional Requirements Documents, Workflows, and Epics. Use when user needs to: (1) Create FRD from PRD with Odyssey-style structure, (2) Generate workflow specifications with full-stack technical details, (3) Create epic specifications with user stories. Framework-agnostic - adapts to any technology stack. Applies rigorous Socratic questioning and Devil's Advocate analysis to ensure comprehensive coverage. Reads ./docs/*.md files (PRD.md, FRD.md, supporting docs), produces YAML frontmatter, traceability matrices, Given/When/Then acceptance criteria, and Mermaid diagrams."
---

# Requirements Architect Skill

Transform PRD/FRD documents into implementation-ready specifications following Odyssey-style patterns with strict traceability. Applies rigorous analysis to ensure comprehensive, well-reasoned requirements.

## Workflow Overview

```
Phase 1: Discovery       → Read ./docs/*.md, extract context
Phase 2: Critical Analysis → Apply Socratic questioning + Devil's Advocate
Phase 3: Generation      → Create documents following templates
Phase 4: Validation      → Verify traceability, completeness, rigor
```

## Configuration

Parse from user request or extract from PRD/FRD:

- **output_type**: `frd` | `workflows` | `epic-spec`
- **overwrite**: `true` (regenerate) | `false` (merge/extend existing)
- **technology_stack**: Extract from PRD/FRD or user input (no default assumed)
- **rigor_level**: `standard` | `thorough` (applies full Socratic + Devil's Advocate)

## Phase 1: Document Discovery

1. List all `.md` files in `./docs/`
2. Always read:
   - `./docs/PRD.md` (required)
   - `./docs/FRD.md` (if exists)
3. Also check for: `*ERD*.md`, `*TRD*.md`, `*Epic*.md`, `*Workflow*.md`, `*Architecture*.md`

4. Extract and model:
   - **Business**: Vision, goals, metrics, constraints
   - **Users**: Personas, roles, journeys, pain points
   - **Functional**: Epics, FRs, NFRs, business rules
   - **Technical**: Stack (from docs), APIs, schemas, performance targets

## Phase 2: Critical Analysis (FRD Generation)

**Before generating any FRD, apply rigorous analysis to ensure completeness.**

### 2.1 Socratic Questioning

See [references/socratic-questions.md](references/socratic-questions.md) for complete framework.

For each major requirement/epic, systematically answer:

**Problem Space**:
- What specific job-to-be-done does this solve?
- What evidence exists that this is a real problem?
- How are users solving this today?

**Strategic Fit**:
- How does this align with product strategy?
- Why is NOW the right time?
- What must be true for this to succeed?

**Solution Space**:
- What alternative approaches were considered?
- What is explicitly out of scope?
- What are the key risks?

**Success Definition**:
- How will we know this succeeded?
- What does "good enough" for Phase 1 look like?

### 2.2 Devil's Advocate Challenges

See [references/devils-advocate-strategy.md](references/devils-advocate-strategy.md) for complete framework.

For each major decision in the FRD, challenge with:

**Strategic Decisions to Challenge**:
| Decision Type | Key Challenge |
|---------------|---------------|
| Target segment | What if another segment has higher value? |
| Build vs buy | What's the true total cost including opportunity cost? |
| Feature scope | Is MVP too minimal or too ambitious? |
| Technology choice | Are we choosing familiar over optimal? |
| Timeline | Is this realistic given historical velocity? |
| Priority | Are we avoiding hard but important work? |

**Document for each challenged decision**:
```markdown
## Decision: [Statement]
### Devil's Advocate Challenge: [Strongest counter-argument]
### Trade-offs Accepted: [What we're giving up]
### Mitigations: [How we address valid concerns]
```

### 2.3 Gap Analysis Checklist

Before generating FRD, verify PRD covers:

- [ ] Clear problem statement with quantitative evidence
- [ ] Defined personas with goals and pain points
- [ ] Success metrics with baselines and targets
- [ ] Explicit scope boundaries (in/out)
- [ ] Risk assessment with mitigations
- [ ] Technical constraints and assumptions
- [ ] Dependencies (internal and external)
- [ ] Phase 1 / MVP definition

**If gaps exist**: Flag them in FRD with `[CLARIFICATION NEEDED]` and specific questions.

## Technology Stack Detection

**Priority order for determining stack:**
1. User explicitly specifies in request
2. Extract from PRD technical requirements section
3. Extract from existing FRD or architecture docs
4. Ask user to specify before generating technical specs

**Common stack patterns** (adapt templates accordingly):

| Stack Type | Frontend | Backend | Database |
|------------|----------|---------|----------|
| MERN | React, Next.js | Node.js, Express | MongoDB |
| MEAN | Angular | Node.js, Express | MongoDB |
| Vue + Strapi | Vue 3, Nuxt 3 | Strapi v4 | PostgreSQL |
| Django | React/Vue/HTMX | Django, DRF | PostgreSQL |
| Rails | React/Hotwire | Ruby on Rails | PostgreSQL |
| Spring | React/Angular | Spring Boot | PostgreSQL/MySQL |
| .NET | React/Blazor | ASP.NET Core | SQL Server |
| Laravel | Vue/Livewire | Laravel | MySQL |
| Serverless | React/Next.js | AWS Lambda/Vercel | DynamoDB/Planetscale |

## Phase 3: Task Routing & Generation

| output_type | Output Location | Template Reference |
|-------------|-----------------|-------------------|
| `frd` | `./docs/FRD.md` | [references/frd-template.md](references/frd-template.md) |
| `workflows` | `./docs/workflows/README.md` + `WF-XX-XXX-*.md` | [references/workflow-template.md](references/workflow-template.md) |
| `epic-spec` | `./docs/Epics-[Name].md` | [references/epic-template.md](references/epic-template.md) |

### FRD Generation

See [references/frd-template.md](references/frd-template.md) for complete structure.

**Enhanced FRD sections with analysis**:

1. Introduction (Purpose, Scope, Conventions, References)
2. **Strategic Context** ← NEW: Socratic analysis summary
3. User Roles and Personas
4-9. Functional Requirements by Epic
10. Requirements Traceability Matrix
11. Non-Functional Requirements
12. **Assumptions & Risks** ← NEW: From Devil's Advocate analysis
13. Use Cases
14. **Open Questions** ← NEW: Gaps requiring clarification
15. Glossary
16. Revision History

### Workflow Generation

See [references/workflow-template.md](references/workflow-template.md) for complete structure.

### Epic-Spec Generation

See [references/epic-template.md](references/epic-template.md) for complete structure.

## ID Schemes

Maintain consistent IDs throughout:
- **Epic**: `EP-NN` (EP-01, EP-02)
- **Functional Requirement**: `FR-[ABBREV]-NNN` (FR-UP-001 for User Profile)
- **Workflow**: `WF-[Epic#]-[Seq]` (WF-02-001)
- **Test Case**: `TC-[ABBREV]-NNN` (TC-UP-001)

## Traceability Pattern

Every document must maintain bidirectional links:
```
Business Goals → Epics → FRs → Workflows → Test Cases
```

Include traceability matrix in FRD mapping:
| Req ID | Requirement | Priority | PRD Ref | Test Case ID |

## YAML Frontmatter (Required)

All generated documents include:
```yaml
---
title: [Document Title]
description: [One-line description]
document_id: [Unique ID]
epic: [Epic reference]
related_requirements: [FR-XXX-001, FR-XXX-002]
related_personas: [Persona names]
product: [Product name from PRD]
date: [DD/MM/YYYY]
version: 1.0
author: [From PRD or user]
status: Draft
technology_stack: [Extracted or specified array]
---
```

## Acceptance Criteria Format

Always use Given/When/Then:
```
GIVEN: [Precondition with specific state]
WHEN: [User/system action with parameters]
THEN: [Measurable, testable outcome with specific values]
```

## Requirement Language

Use RFC 2119 style:
- **SHALL**: Mandatory requirement (P0/P1)
- **SHOULD**: Recommended (P1/P2)
- **MAY**: Optional (P2)

## Phase 4: Validation Checklist

Before completing, verify:

**Structure & Syntax**:
- [ ] Valid YAML frontmatter (syntax, required fields, DD/MM/YYYY dates)
- [ ] Proper markdown (tables closed, code fences matched, headings nested)
- [ ] ID consistency (patterns match scheme, no duplicates)

**Traceability**:
- [ ] Every FR links to PRD section/goal
- [ ] Every workflow links to FRs
- [ ] Traceability matrix complete

**Quality**:
- [ ] No placeholders ([TBD], [TODO]) without justification
- [ ] All acceptance criteria in Given/When/Then format
- [ ] Persona references validated against PRD
- [ ] Technical specs match specified/detected technology stack

**Rigor** (for FRD):
- [ ] Socratic questions answered for each epic
- [ ] Major decisions challenged with Devil's Advocate
- [ ] Assumptions explicitly documented
- [ ] Risks identified with mitigations
- [ ] Open questions flagged for stakeholder review

## Output Summary

After completion, report:
1. **Documents Read**: Files processed with versions
2. **Technology Stack**: Detected or specified stack used
3. **Critical Analysis**: Key decisions challenged, trade-offs documented
4. **Files Created/Updated**: Paths and line counts
5. **Key Decisions**: Epic groupings, ID assignments
6. **Traceability**: FR count, workflow count, PRD coverage %
7. **Open Questions**: Items requiring stakeholder clarification
8. **Assumptions**: Any inferred details flagged

## Common Pitfalls

Avoid:
- Generic acceptance criteria ("System should work well")
- Missing traceability (FRs without PRD references)
- Inconsistent IDs (FR-001 vs FR-XXX-001)
- Vague technical specs without concrete details
- Ignoring personas in workflow design
- Assuming a technology stack not specified in docs
- **Skipping critical analysis** - always apply Socratic + Devil's Advocate for FRDs
- **Rubber-stamping PRD assumptions** - challenge everything
- **Hiding uncertainty** - flag gaps explicitly rather than guessing
