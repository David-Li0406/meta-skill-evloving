# Phases 2-3: Foundation & Specification (Complex Path)

**Duration**: 1.5-2.5 hours total
**Prerequisites**: Phase 1 research complete
**Next Phase**: Phase 4 (Design System)

---

## Overview

This combined phase establishes the project foundation by selecting an optimal template and creating a comprehensive product specification. These phases flow together naturally: template selection informs technical constraints, which feed into specification planning.

**What You'll Accomplish**:
1. Select and install appropriate Next.js template
2. Create technology-agnostic product specification
3. Generate implementation plan with tech stack
4. Break down into user-story-organized tasks
5. Validate all artifacts with audit

**Outputs**:
- Installed Next.js template
- `/docs/spec.md` (WHAT/WHY)
- `/docs/plan.md` (HOW with tech)
- `/docs/tasks.md` (implementation tasks)
- Audit validation (PASS)

---

## Tools Required

- **Vercel MCP**: Template discovery
- **Bash**: Installation commands
- **specify-feature skill**: Auto-invoked for specification
- **create-implementation-plan skill**: Auto-invoked after spec
- **generate-tasks skill**: Auto-invoked after plan
- **/audit command**: Auto-invoked for validation

---

## Workflow (CoD^Σ)

```
Research_Reports → Template_Selection → Install
  ↓
User_Requirements → specify-feature_skill
  ↓
spec.md[WHAT/WHY] → /plan (auto)
  ↓
plan.md + research.md + data-model.md → /tasks (auto)
  ↓
tasks.md → /audit (auto)
  ↓ [if PASS]
Ready_for_Phase_4
```

---

## Phase 2: Template Selection (20-30 minutes)

### Step 1: Analyze Requirements

Review user requirements against template features using the decision matrix:

| Requirement | Template Candidates |
|-------------|-------------------|
| Auth + DB | Supabase Starter |
| SaaS + Payments | Stripe Subscription Starter |
| E-commerce | Next.js Commerce |
| Blog/Content | Blog Starter, Portfolio |
| Enterprise | Enterprise Boilerplate |
| Multi-tenant | Custom on Supabase base |

### Step 2: Load Research Report

Read `/reports/foundation-research.md` for template comparison and recommendations.

### Step 3: Present Options

Use Vercel MCP to present top 3 template options:

```markdown
### Option 1: [Template Name]
**Best for**: [Use case]
**Features**: [Key features]
**Tech Stack**: [Core technologies]
**Pros**: [Advantages]
**Cons**: [Limitations]
**Setup Time**: [Estimate]
```

### Step 4: Install Template

```bash
# Install selected template
npx create-next-app@latest project-name --example [template-url]
cd project-name

# Verify
npm install
npm run dev
```

**Verification**:
- [ ] Template installed successfully
- [ ] Dependencies resolved
- [ ] Development server running
- [ ] Environment variables template exists

### Step 5: Environment Setup

Create `.env.local` based on template requirements:

**Supabase Example**:
```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-anon-key
```

**⚠️ Security**: Verify `.gitignore` includes `.env.local`

### Step 6: Document Selection

Create `/docs/template-selection.md`:
```markdown
# Template Selection: [Name]

## Decision Rationale
[Why chosen]

## Key Features
- [Feature list]

## Tech Stack
- Framework: Next.js [version]
- Database: [Supabase | None]
- Auth: [Method]
- Styling: Tailwind CSS
- Language: TypeScript

## Setup Notes
[Configuration steps]

## Known Limitations
[Constraints identified]
```

---

## Phase 3: Product Specification (1-2 hours)

### Step 1: Gather Requirements

**Interview Questions**:

**Problem & Vision**:
- What problem are you solving?
- Who are your target users?
- What's the core value proposition?
- What does success look like?

**User Stories** (prioritize):
- P1: Must have (highest priority)
- P2: Should have
- P3: Nice to have

**Constraints**:
- Timeline or deadlines?
- Technical constraints from template?
- Compliance requirements? (GDPR, HIPAA)

**Non-Functional Requirements**:
- Performance targets?
- Scale expectations?
- Security requirements?
- Accessibility standards? (WCAG 2.1 AA minimum)

### Step 2: Invoke specify-feature Skill

**AUTOMATIC INVOCATION**: The skill orchestrator invokes specify-feature with gathered requirements.

**What specify-feature Does**:
1. Creates technology-agnostic specification
2. Enforces separation (no tech details in spec)
3. Defines user stories with priorities
4. Establishes acceptance criteria (minimum 2 per story)
5. Documents success criteria
6. **Auto-invokes** `/plan` command

**Output**: `/docs/spec.md`

### Step 3: Clarification Phase

**Handled automatically by specify-feature**:
- Scans for ambiguities
- Generates max 5 clarification questions
- Presents recommendations
- Updates spec incrementally
- Marks unknowns as [NEEDS CLARIFICATION]

**Ambiguity Categories**:
- Functional scope
- Data model
- UX flow
- Non-functional requirements
- Integrations
- Edge cases
- Tradeoffs

### Step 4: Auto-Chain to Planning

**AUTOMATIC**: specify-feature invokes `/plan`

**create-implementation-plan creates**:
- `/docs/plan.md` - Tech stack and architecture
- `/docs/research.md` - Research notes
- `/docs/data-model.md` - Database schema (if applicable)

**Plan Contents**:
```markdown
# Implementation Plan

## Tech Stack
- Framework: Next.js 14+ (from template)
- Database: [from template]
- Auth: [from template]
- Components: Shadcn UI
- Styling: Tailwind CSS

## Architecture Decisions
[Key decisions with rationale]

## File Structure
[Project organization]

## Data Flow
[How data moves]

## Implementation Phases
[Story-by-story order]
```

### Step 5: Auto-Chain to Tasks

**AUTOMATIC**: create-implementation-plan invokes generate-tasks

**Output**: `/docs/tasks.md`

**Task Structure** (user-story-centric):
```markdown
# Implementation Tasks

## Phase 1: Setup
- [ ] T001: Infrastructure
- [ ] T002: Environment config

## Phase 2: Foundational
- [ ] T003: Database schema
- [ ] T004: Auth flow

## Phase 3: User Story P1 - [Title]
- [ ] T005: Write tests for P1
- [ ] T006: [P] Implement feature 1
- [ ] T007: [P] Implement feature 2
- [ ] T008: Integration
- [ ] T009: Verify P1 (independent)

## Phase 4: User Story P2 - [Title]
[Same structure]
```

**Key Principles**:
- Tasks grouped by user story (NOT by layer)
- Each story independently testable
- Parallel tasks marked with [P]
- Minimum 2 ACs per task

### Step 6: Auto-Chain to Audit

**AUTOMATIC**: generate-tasks invokes `/audit`

**Audit Validates**:
- ✅ Constitution compliance (7 articles)
- ✅ Spec→plan consistency
- ✅ Plan→tasks complete mapping
- ✅ No missing requirements
- ✅ All ACs have ≥1 test
- ✅ Ambiguities resolved ([NEEDS CLARIFICATION] ≤3)
- ✅ User-story-centric organization

**Result**: PASS ✅ or FAIL ❌ with violations list

---

## Quality Checks

### Template Selection
- [ ] Requirements documented
- [ ] Research reports reviewed
- [ ] Template matches ≥80% requirements
- [ ] No deal-breaker limitations
- [ ] Development server operational

### Specification
- [ ] Technology-agnostic (no tech in spec)
- [ ] All user stories prioritized
- [ ] Every story has ≥2 ACs
- [ ] Success criteria measurable
- [ ] Constraints documented

### Planning
- [ ] Plan references all spec requirements
- [ ] Tech stack aligns with template
- [ ] Architecture decisions have rationale
- [ ] Data model defined (if DB)

### Tasks
- [ ] Grouped by user story
- [ ] Each story independently testable
- [ ] Parallel tasks identified [P]

### Audit
- [ ] /audit completed
- [ ] All checks passed
- [ ] Constitution violations: NONE
- [ ] Ready for implementation: YES

---

## Outputs Summary

**Phase 2 Outputs**:
1. Installed Next.js template (running on localhost:3000)
2. `/docs/template-selection.md`
3. Environment setup (`.env.local` configured)

**Phase 3 Outputs**:
1. `/docs/spec.md` (technology-agnostic)
2. `/docs/plan.md` (technical implementation)
3. `/docs/research.md` (supporting notes)
4. `/docs/data-model.md` (if database used)
5. `/docs/tasks.md` (user-story tasks)
6. Audit validation (PASS status)

---

## Next Phase Handover

**Prerequisites for Phase 4 (Design System)**:
- ✅ Template installed and running
- ✅ Specification complete
- ✅ Implementation plan created
- ✅ Tasks breakdown complete
- ✅ Audit passed

**Handover Context**:
- Template name and tech stack
- User stories with priorities
- Technical architecture defined
- Database schema (if applicable)
- Component structure outlined

**Continue with**: `design-and-wireframes.md`

---

## User Decision Point

After audit passes, ask user:

> "✅ Foundation complete with template, spec, plan, and tasks ready.
>
> **Options**:
> 1. Continue with design system (Phase 4) - Recommended
> 2. Skip to implementation (`/implement plan.md`)
> 3. Review and refine artifacts first

Most complex projects should continue with Phase 4 for optimal results.

---

## Common Issues

### Template Installation Fails
- Check npm version ≥8.0
- Try alternative installation method
- Verify template URL correct

### Dependencies Won't Install
```bash
rm -rf node_modules package-lock.json
npm install
```

### Development Server Won't Start
- Check port 3000: `lsof -i :3000`
- Verify env vars in `.env.local`
- Review console errors

### Specification Too Technical
- Remove all tech-specific content
- Move to plan.md instead
- Spec should be non-technical

### Audit Fails
- Read audit report carefully
- Fix specific violations
- Re-run `/audit`

---

## 85% Automation

**Manual Steps** (2):
1. Gather requirements (this phase)
2. `/implement plan.md` (Phase 6)

**Automatic Steps** (6):
1. specify-feature creates spec.md
2. specify-feature invokes `/plan`
3. create-implementation-plan creates plan.md + docs
4. create-implementation-plan invokes generate-tasks
5. generate-tasks creates tasks.md
6. generate-tasks invokes `/audit`

**Result**: User provides requirements once, system generates spec → plan → tasks → audit automatically!

---

## Success Criteria

- ✅ Template installed successfully
- ✅ Selection rationale documented
- ✅ Specification created (technology-agnostic)
- ✅ Implementation plan generated (tech-specific)
- ✅ Task breakdown complete (user-story-organized)
- ✅ Audit passed (constitution compliant)
- ✅ All artifacts consistent and traceable
- ✅ Ready for design system or implementation
