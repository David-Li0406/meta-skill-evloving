---
name: prd-creator
description: Create comprehensive Product Requirements Documents (PRDs) with user stories, acceptance criteria, and technical specifications. Use this when planning new features, products, or major enhancements.
allowed-tools: Read,Write,Edit,Glob,Grep
---

# PRD Creator

Create clear, actionable Product Requirements Documents that align stakeholders and guide implementation.

## When to Use

- Planning a new feature or product
- Documenting requirements before development
- Aligning stakeholders on scope and priorities
- Creating technical specifications for handoff

## Discovery Phase

### 1. Understand the Request

**Ask clarifying questions:**

- What problem are we solving? For whom?
- What does success look like? How will we measure it?
- What are the constraints (time, budget, technical)?
- Who are the stakeholders? Who has final approval?
- Are there existing solutions or competitors to reference?

### 2. Research Context

**Check existing documentation:**
```bash
# Look for related docs
find . -name "*.md" | xargs grep -l "[feature-name]"

# Check existing PRDs
ls -la docs/prd/ 2>/dev/null || ls -la docs/ 2>/dev/null
```

**Review codebase for related features:**
- Similar implementations
- Existing data models
- Integration points

## PRD Structure

### Standard Template

```markdown
# [Feature Name] PRD

## Overview
**Author:** [Name]
**Status:** Draft | In Review | Approved
**Last Updated:** YYYY-MM-DD
**Target Release:** [Version/Quarter]

## Problem Statement
[2-3 sentences describing the problem]

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| Primary goal | How we measure | Success threshold |

## User Stories
### [Persona 1]
- As a [persona], I want to [action] so that [benefit]

## Requirements
### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | Description | P0/P1/P2 | |

### Non-Functional Requirements
- Performance: [targets]
- Security: [requirements]
- Accessibility: [standards]

## Design
[Link to designs or embed key screens]

## Technical Approach
[High-level architecture, key decisions]

## Out of Scope
- [Explicitly excluded items]

## Dependencies
- [External dependencies]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| | High/Med/Low | |

## Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| | | |

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

## Writing Guidelines

### Problem Statement

**✅ Good:**
> Enterprise customers cannot export usage reports, requiring manual data compilation that takes 4+ hours per customer quarterly. This delays renewals and increases churn risk.

**❌ Bad:**
> Users need an export feature.

### User Stories

**Format:** As a [persona], I want to [action] so that [benefit]

**✅ Good:**
> As an account manager, I want to export usage reports as PDF so that I can include them in quarterly business reviews without manual formatting.

**❌ Bad:**
> User can export reports.

### Acceptance Criteria

**Use Given-When-Then format:**

```gherkin
Given I am logged in as an account manager
And I have selected a customer account
When I click "Export Usage Report"
Then a PDF downloads containing:
  - Usage summary for selected period
  - Comparison to previous period
  - Top features by usage
```

### Requirements Prioritization

| Priority | Definition | Example |
|----------|------------|---------|
| **P0** | Must have for launch | Core functionality |
| **P1** | Should have, can follow fast | Important but not blocking |
| **P2** | Nice to have | Future enhancement |

## PRD Types

### Feature PRD
Standard new feature documentation.
→ Use full template above

### Enhancement PRD
Improvements to existing features.
→ Focus on: current state, proposed changes, migration plan

### Technical PRD
Infrastructure or architecture changes.
→ Add: system diagrams, API contracts, data migrations

### Spike/Research PRD
Investigation before committing to approach.
→ Focus on: questions to answer, success criteria, timebox

**For detailed templates, see:** `references/templates.md`

## Collaboration Workflow

### 1. Draft Phase
- Create initial PRD with known information
- Mark unknowns with `[TBD]` or `[QUESTION]`
- Share with immediate team for input

### 2. Review Phase
- Stakeholder review (PM, Eng, Design)
- Address feedback and open questions
- Update status to "In Review"

### 3. Approval Phase
- Final stakeholder sign-off
- Update status to "Approved"
- Create implementation tickets

### 4. Living Document
- Update as decisions are made
- Track changes in changelog section
- Archive after feature ships

## Output Checklist

Before marking PRD complete:

- [ ] Problem statement is clear and measurable
- [ ] Success metrics are defined and trackable
- [ ] User stories cover all personas
- [ ] Requirements are prioritized (P0/P1/P2)
- [ ] Acceptance criteria are testable
- [ ] Out of scope is explicitly stated
- [ ] Dependencies are identified
- [ ] Risks have mitigations
- [ ] Timeline is realistic
- [ ] Open questions are tracked

## File Organization

**Recommended structure:**
```
docs/
├── prd/
│   ├── 2025/
│   │   ├── feature-name-prd.md
│   │   └── another-feature-prd.md
│   └── templates/
│       └── prd-template.md
```

**Naming convention:** `[feature-name]-prd.md` (lowercase, hyphens)

## Important Reminders

- **ALWAYS** start with the problem, not the solution
- **ALWAYS** define measurable success criteria
- **ALWAYS** include "Out of Scope" section
- **ALWAYS** prioritize requirements (P0/P1/P2)
- **NEVER** skip user stories—they drive acceptance criteria
- **NEVER** leave open questions untracked
- **ASK** clarifying questions before drafting
- **CHECK** for existing related PRDs first

