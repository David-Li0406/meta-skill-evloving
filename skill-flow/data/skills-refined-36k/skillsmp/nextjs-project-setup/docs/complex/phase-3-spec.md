# Phase 3: Product Specification (Complex Path)

**Duration**: 1-2 hours
**Prerequisites**: Phase 2 (Template selected and installed)
**Next Phase**: Phase 4 (Design System)

---

## Overview

**Purpose**: Create technology-agnostic product specification following Constitution Article IV (Specification-First Development)

**Inputs**:
- User requirements and goals
- Template constraints from Phase 2
- Project vision and success criteria

**Outputs**:
- `/docs/product-spec.md` (WHAT/WHY, technology-agnostic)
- `/docs/constitution.md` (Project principles, optional)
- `/docs/plan.md` (HOW with tech, via auto-chain)
- `/docs/tasks.md` (User-story tasks, via auto-chain)

---

## Constitution Compliance

**Article IV: Specification-First Development** (MANDATORY)

**Phase 1: Specification (WHAT/WHY)** - Technology-agnostic
**Phase 2: Clarification** - Resolve ambiguities
**Phase 3: Planning (HOW with Tech)** - Implementation approach

**Separation**:
```
Specification := {problem, user_stories, requirements, success_criteria}
  ∧ ¬{tech_stack, architecture, implementation_details}

Planning := {tech_stack, architecture, file_structure, dependencies}
  ∧ depends_on(Specification)
```

---

## Tools Required

- **specify-feature skill** (invoked automatically)
- **create-implementation-plan skill** (auto-invoked after spec)
- **generate-tasks skill** (auto-invoked after plan)
- **File System**: Document creation

---

## Workflow (CoD^Σ with SDD Integration)

```
User_Requirements → specify-feature_skill
  ↓
spec.md[WHAT/WHY] → clarification_loop
  ↓
Approved_Spec → /plan (auto-invoked)
  ↓
plan.md[HOW] + research.md + data-model.md
  ↓
/tasks (auto-invoked)
  ↓
tasks.md[User_Stories]
  ↓
/audit (auto-invoked)
  ↓ [if PASS]
Ready_for_Implementation
```

---

## SDD Workflow Integration

**CRITICAL**: This phase integrates with Intelligence Toolkit's Specification-Driven Development (SDD) workflow

### Automation Chain (85% automated)

**User Actions** (manual):
1. This phase gathers requirements
2. Later: `/implement plan.md` when ready to code

**Automatic Actions** (no user intervention):
- specify-feature creates `spec.md`
- specify-feature invokes `/plan`
- create-implementation-plan creates `plan.md`, `research.md`, `data-model.md`
- create-implementation-plan invokes `generate-tasks`
- generate-tasks creates `tasks.md`
- generate-tasks invokes `/audit`
- `/audit` validates all artifacts for consistency

**Result**: spec → plan → tasks → audit (all automatic after initial requirements gathering)

---

## Detailed Steps

### Step 1: Gather Requirements

**Interview Questions**:

**Problem & Vision**:
- What problem are you solving?
- Who are your target users?
- What's the core value proposition?
- What does success look like?

**User Stories** (prioritize):
- What can users do? (P1: Must have)
- What should users be able to do? (P2: Should have)
- What could users do? (P3: Nice to have)

**Constraints**:
- Timeline or deadlines?
- Budget constraints?
- Technical constraints? (already have: template from Phase 2)
- Compliance requirements? (GDPR, HIPAA, etc.)

**Non-Functional Requirements**:
- Performance targets? (page load, response time)
- Scale expectations? (concurrent users, data volume)
- Security requirements? (authentication, authorization, data protection)
- Accessibility standards? (WCAG 2.1 AA minimum)

### Step 2: Invoke specify-feature Skill

**AUTOMATIC INVOCATION**:

The orchestrator (main SKILL.md) should now invoke the specify-feature skill:

```typescript
// Conceptual - actual invocation via Skill tool
invoke_skill("specify-feature", {
  context: requirements_gathered,
  template: template_name_from_phase_2,
  constraints: template_constraints
})
```

**What specify-feature Does**:
1. Creates technology-agnostic specification
2. Enforces Article IV separation (no tech details in spec)
3. Defines user stories with priorities (P1, P2, P3...)
4. Establishes acceptance criteria for each story
5. Documents success criteria (measurable outcomes)
6. **Auto-invokes** `/plan` command

**Output**: `/docs/spec.md`

**Spec Structure**:
```markdown
# [Project Name] - Feature Specification

## Problem Statement
[What problem are we solving?]

## User Stories

### P1: [Must Have - Highest Priority]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] AC1: [Testable criterion]
- [ ] AC2: [Testable criterion]

### P2: [Should Have]
[Same structure]

### P3: [Nice to Have]
[Same structure]

## Success Criteria
- Metric 1: [Measurable outcome]
- Metric 2: [Measurable outcome]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Out of Scope
[Explicitly excluded features]
```

### Step 3: Clarification Phase

**specify-feature skill handles this automatically**:
- Scans specification for ambiguities
- Generates max 5 high-impact clarification questions
- Presents recommendations (not open-ended questions)
- Iterates with user until clear
- Updates spec incrementally (no contradictions)
- Marks remaining unknowns as [NEEDS CLARIFICATION]

**Ambiguity Categories Covered**:
- Functional scope and behavior
- Domain and data model
- User interaction and UX flow
- Non-functional requirements
- Integration and dependencies
- Edge cases and failure scenarios
- Constraints and tradeoffs

**Output**: Updated `/docs/spec.md` with clarifications

### Step 4: Auto-Chain to Planning

**AUTOMATIC**: specify-feature invokes `/plan` command

**create-implementation-plan skill creates**:
1. `/docs/plan.md` - Implementation approach with tech stack
2. `/docs/research.md` - Research notes and decisions
3. `/docs/data-model.md` - Database schema (if applicable)

**Planning Contents (HOW with Tech)**:
```markdown
# Implementation Plan

## Tech Stack
- Framework: Next.js 14+ (from template)
- Database: Supabase (from template)
- Auth: Supabase Auth (from template)
- Components: Shadcn UI (@ui registry)
- Styling: Tailwind CSS

## Architecture Decisions
[Key technical decisions with rationale]

## File Structure
[Project organization]

## Component Hierarchy
[UI component organization]

## Data Flow
[How data moves through the system]

## Integration Points
[External services, APIs, etc.]

## Implementation Phases
[Story-by-story implementation order]
```

**Evidence Required** (Constitution Article II):
- All decisions traced to spec requirements
- Research backing for technology choices
- Template constraints acknowledged

### Step 5: Auto-Chain to Tasks

**AUTOMATIC**: create-implementation-plan invokes generate-tasks

**generate-tasks skill creates**:
- `/docs/tasks.md` - User-story-organized task breakdown

**Task Structure** (Constitution Article VII):
```markdown
# Implementation Tasks

## Phase 1: Setup
- [ ] T001: Infrastructure setup
- [ ] T002: Environment configuration

## Phase 2: Foundational
- [ ] T003: Database schema creation
- [ ] T004: Authentication flow setup

## Phase 3: User Story P1 - [Title]
- [ ] T005: Write tests for P1 ACs
- [ ] T006: [P] Implement feature 1
- [ ] T007: [P] Implement feature 2
- [ ] T008: Integration for P1
- [ ] T009: Verify P1 (independent test)

## Phase 4: User Story P2 - [Title]
[Same structure - independently testable]
```

**Key Principles**:
- Tasks grouped by user story (NOT by technical layer)
- Each story independently testable
- Parallel tasks marked with [P]
- Minimum 2 acceptance criteria per task

### Step 6: Auto-Chain to Audit

**AUTOMATIC**: generate-tasks invokes `/audit`

**Audit validates**:
- ✅ Constitution compliance (all 7 articles)
- ✅ Spec→plan consistency
- ✅ Plan→tasks mapping complete
- ✅ No missing requirements
- ✅ All ACs have ≥1 test
- ✅ No ambiguities remaining ([NEEDS CLARIFICATION] ≤3)
- ✅ Tasks follow Article VII (user-story-centric)

**Audit Results**:
```
PASS ✅: All checks passed, ready for /implement
FAIL ❌: [List of violations] - must fix before proceeding
```

---

## Constitution Integration (Optional)

**If project needs principles/constraints**, create `/docs/constitution.md`:

**Use case**: When project has:
- Specific technical constraints
- Architectural patterns to enforce
- Team conventions
- Performance requirements
- Security standards

**Invoke**: `generate-constitution` skill (optional)

**Output**: `/docs/constitution.md` with project-specific principles derived from user needs

---

## Sub-Agents

**None required** - Skills handle the workflow automatically

Optional: If domain-specific expertise needed, dispatch specialist research agents

---

## Quality Checks

### Pre-Planning Checklist
- [ ] Specification is technology-agnostic
- [ ] All user stories have priorities (P1, P2, P3)
- [ ] Every story has ≥2 acceptance criteria
- [ ] Success criteria are measurable
- [ ] Constraints are documented
- [ ] Out of scope is explicit

### Post-Planning Checklist
- [ ] Plan references all spec requirements
- [ ] Tech stack aligns with template
- [ ] Architecture decisions have rationale
- [ ] Data model defined (if database used)
- [ ] Integration points identified

### Post-Tasks Checklist
- [ ] Tasks grouped by user story
- [ ] Each story independently testable
- [ ] Parallel tasks identified with [P]
- [ ] Foundation tasks separate from story tasks

### Audit Checklist
- [ ] /audit command completed
- [ ] All validation checks passed
- [ ] Constitution violations: NONE
- [ ] Ready for implementation: YES

---

## Outputs

### 1. Product Specification
**Location**: `/docs/spec.md`
**Created by**: specify-feature skill
**Content**: Technology-agnostic WHAT/WHY

### 2. Implementation Plan
**Location**: `/docs/plan.md`
**Created by**: create-implementation-plan skill (auto-invoked)
**Content**: Technical HOW with architecture

### 3. Supporting Documents
**Locations**:
- `/docs/research.md` - Research notes
- `/docs/data-model.md` - Database schema
- `/docs/constitution.md` - Project principles (optional)

### 4. Task Breakdown
**Location**: `/docs/tasks.md`
**Created by**: generate-tasks skill (auto-invoked)
**Content**: User-story-organized tasks

### 5. Audit Report
**Location**: Console output (not persisted)
**Created by**: /audit command (auto-invoked)
**Status**: PASS or FAIL with violations

---

## Next Phase Handover

**Prerequisites for Phase 4 (Design System)**:
- ✅ Specification complete and approved
- ✅ Implementation plan created
- ✅ Tasks breakdown complete
- ✅ Audit passed (PASS status)
- ✅ All artifacts consistent

**Handover Context**:
- User stories with priorities
- Technical architecture defined
- Database schema (if applicable)
- Component structure outlined
- Integration requirements identified

**Continue with**: `phase-4-design.md`

---

## User Decision Point

**After audit passes**, ask user:

> "✅ Specification complete with plan and tasks ready.
>
> **Options**:
> 1. Continue with design system ideation (Phase 4)
> 2. Skip to implementation now (`/implement plan.md`)
> 3. Review and refine specification first
>
> **Recommendation**: Continue with design system for complex projects, or skip to implementation if design is straightforward."

Most users should continue with Phase 4 for optimal results.

---

## Common Issues & Solutions

### Issue: Specification too technical
**Cause**: Including implementation details in spec phase
**Solution**: Remove all tech-specific content. Move to plan.md. Spec should be understandable by non-technical stakeholders.

### Issue: User stories too vague
**Cause**: Poorly defined acceptance criteria
**Solution**: Each AC must be testable. Ask "How do we know this is done?" for each story.

### Issue: Audit fails
**Cause**: Constitution violation, missing requirements, inconsistencies
**Solution**: Read audit report carefully. Fix specific violations. Re-run `/audit`.

### Issue: Auto-chain doesn't trigger
**Cause**: Skills not properly invoked
**Solution**: Manually invoke: `/plan spec.md`, then `/tasks plan.md`, then `/audit`

---

## Success Criteria

- ✅ Specification created (technology-agnostic)
- ✅ Clarification complete (ambiguities resolved)
- ✅ Implementation plan generated (tech-specific)
- ✅ Task breakdown complete (user-story-organized)
- ✅ Audit passed (constitution compliant)
- ✅ All artifacts consistent and traceable
- ✅ Ready to proceed with design or implementation

---

## Evidence Requirements

**All specifications MUST document** (Constitution Article II):
- **User needs**: Traced from conversation or requirements doc
- **Priorities**: Rationale for P1 vs P2 vs P3
- **Acceptance criteria**: Testable, specific, measurable
- **Success metrics**: How we measure project success
- **Constraints**: Why they exist and impact on design

**Example Good Evidence**:
"User Story P1: Authentication (conversation:line 12) requires email/password login (requirement:line 3) because 80% of target users prefer email over social login (research:line 45). AC1: User can log in with email+password and see dashboard within 2 seconds (performance target:line 67)."

---

## 85% Automation Summary

**Manual Steps** (2):
1. Gather requirements (this phase)
2. `/implement plan.md` (later, Phase 6)

**Automatic Steps** (6):
1. specify-feature creates spec.md
2. specify-feature invokes `/plan`
3. create-implementation-plan creates plan.md + supporting docs
4. create-implementation-plan invokes generate-tasks
5. generate-tasks creates tasks.md
6. generate-tasks invokes `/audit`

**Result**: User provides requirements once, system generates spec → plan → tasks → audit automatically. Only 15% manual work required!
