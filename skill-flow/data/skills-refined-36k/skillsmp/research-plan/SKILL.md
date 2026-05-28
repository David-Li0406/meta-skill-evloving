---
name: research-plan
description: Route the rough plan through targeted or deep research to gather verified facts.
---

# Research Plan

Route the rough plan through targeted or deep research to gather verified facts.

## When to use

Use after `/intake` determines that research is needed (Track M or L) and you have:
- A scored INTAKE.md with research mode recommendation
- Need to gather verified facts before detailed planning

## Role

You are a research coordinator spawning specialized sub-agents to gather evidence for the implementation plan.

## Required Inputs

- Project slug (e.g., "my-feature")
- INTAKE.md from Stage 0 (`docs/plans/<project>/INTAKE.md`)

## Research Modes

| Mode | When | Sub-agents |
|------|------|------------|
| `targeted` | Track M (2-4 points) | Codebase Analyst, API/SDK Researcher, Learnings Retriever |
| `deep` | Track L (5+ points) | All targeted + Best Practices Scout, Git History Analyzer |

## Sub-agent Responsibilities

1. **Codebase Analyst** - Existing patterns, similar implementations, helper functions, test patterns
2. **API/SDK Researcher** - External API contracts, SDK documentation, authentication flows
3. **Learnings Retriever** - Past decisions, ADRs, postmortems, relevant issues
4. **Best Practices Scout** (deep only) - Industry standards, security guidelines, performance patterns
5. **Git History Analyzer** (deep only) - Why code evolved, past attempts, refactoring context

## Evidence Rules (Locked)

These rules are non-negotiable:

| Rule | Requirement |
|------|-------------|
| Verified Facts | MUST include `Source:` with repo path or URL |
| UNVERIFIED Items | MUST include `How to verify:` with concrete steps |
| External API Calls | MUST have contract block (verified OR marked UNVERIFIED) |

## Output Schema

Create `docs/plans/<project>/RESEARCH_DOSSIER.md` with:

```yaml
---
schemaVersion: "1.0"
artifactType: RESEARCH_DOSSIER
project: <project-slug>
createdAt: <ISO8601>
researchMode: targeted|deep
sourceIntake: docs/plans/<project>/INTAKE.md
---
```

### Required Sections

1. **Verified Facts** - Facts with sources, grouped by category
2. **Repo Integration Findings** - Files to create/modify, patterns to follow, available helpers
3. **External APIs / Services** - Contracts (verified or UNVERIFIED), auth requirements
4. **Version & Dependency Notes** - Compatibility concerns, required upgrades
5. **Known Unknowns** - UNVERIFIED items with specific verification steps
6. **Decisions Required** - Conflicts or ambiguities surfaced during research

## Convergence Rules

Research is complete when ALL conditions are met:
- RESEARCH_DOSSIER.md passes schema validation
- Net-new research issues in current pass <= 1
- All targeted triggers from INTAKE.md are covered
- Regression count is 0

## Next Steps

| Track | Next Skill |
|-------|------------|
| Track M | `/plan-polish` (lite schema - skip detailed risk analysis) |
| Track L | `/plan-polish` (full schema - complete TDD) |
