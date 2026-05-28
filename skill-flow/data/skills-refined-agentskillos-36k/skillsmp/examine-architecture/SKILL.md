---
name: examine-architecture
description: Audit codebase, assess technical debt, analyze architecture, find structural problems. Use when evaluating code health, planning refactors, or need architectural review. Covers brittleness, coupling, complexity.
argument-hint: Area to focus on (optional)
disable-model-invocation: true
context: fork
---

# Architecture Examination

You are examining a codebase's architecture to identify structural problems. Follow a systematic approach: identify architectural surfaces, analyze each in parallel, consolidate findings, then validate with plan-refiner.

## Core Principles

- **Analyze, don't fix**: This command identifies problems and creates implementation plans, but doesn't make changes
- **Parallel analysis**: Launch multiple agents to examine different surfaces simultaneously
- **Validate recommendations**: Use plan-refiner to eliminate over-engineering from proposed fixes
- **Use TodoWrite**: Track all progress throughout

---

## Phase 1: Surface Identification

**Goal**: Identify which architectural surfaces to examine

Focus area: $ARGUMENTS

**Actions**:

1. Create todo list with all phases
2. If $ARGUMENTS specified, focus surfaces on that area
3. Identify 4-8 architectural surfaces based on project characteristics

**Surface Categories**:

- **Vertical**: Auth flow, data persistence, API request/response, error handling
- **Horizontal**: UI/presentation, business logic, data access, integrations
- **Cross-cutting**: State management, testing, configuration, logging
- **Structural**: Component organization, dependencies, build/deployment

4. Present selected surfaces and confirm with user before proceeding

---

## Phase 2: Parallel Analysis

**Goal**: Examine each surface for architectural problems

**Actions**:

1. Launch architecture-reviewer agents in parallel (one per surface)
2. Each agent should:
   - Analyze the surface for brittleness, complexity, and coupling
   - Output findings with severity, effort, and suggested approach
   - Include a list of key files examined
3. Wait for all agents to complete
4. Read key files identified by agents to build context

---

## Phase 3: Consolidation

**Goal**: Merge findings into prioritized, actionable issues

**Actions**:

1. Review all agent findings
2. Merge overlapping issues across surfaces
3. Identify root causes that span multiple areas
4. Create step-by-step implementation plans for each issue
5. Prioritize by impact (severity × breadth)

---

## Phase 4: Validation

**Goal**: Ensure recommendations aren't over-engineered

**Actions**:

1. Launch plan-refiner agent to review implementation plans
2. Plan-refiner should:
   - Eliminate over-engineering
   - Validate tractability
   - Suggest simpler approaches
   - Flag anything too complex to be worth fixing
3. Incorporate plan-refiner feedback
4. Present validated findings to user

---

## Phase 5: Summary

**Goal**: Present actionable findings

**Actions**:

1. Mark all todos complete
2. Present findings in this format:

```
ARCHITECTURE EXAMINATION COMPLETE

Surfaces examined: X
Raw findings: Y
Consolidated issues: Z

ACTIONABLE FIXES (ready to implement):

1. [Issue Title] - Severity: high|medium|low | Effort: small|medium|large

   Problem: [What's architecturally wrong]
   Impact: [What's hard because of this]
   Root cause: [Why this exists]

   Implementation Plan:
   1. [Step with file references]
   2. [Step with file references]

   Plan-refiner notes: [Simplifications applied]

2. [...]

DEFERRED:

- [Issue] - Why: [Too complex / Low impact / Not worth fixing]
```

3. **Use AskUserQuestion** to ask which issues they want to address (multiSelect: true)
