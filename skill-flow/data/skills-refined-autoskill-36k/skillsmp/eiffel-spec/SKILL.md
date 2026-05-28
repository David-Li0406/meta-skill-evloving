---
name: eiffel-spec
description: Pre-Phase specification design. Transforms 7-step research into Eiffel specification using OOSC2 principles. Use after /eiffel.research, before /eiffel.intent.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.spec - Pre-Phase: Specification from Research

**Purpose:** Transform research output into a well-designed Eiffel specification using OOSC2 principles and Design by Contract.

## When to Use

- After completing `/eiffel.research`
- Before `/eiffel.intent`
- When you have research but need class design

## Usage

```
/eiffel.spec <project-path>
```

**Example:**
```
/eiffel.spec d:\prod\simple_cache
```

## Prerequisites

- Research complete: `<project-path>/.eiffel-workflow/research/07-RECOMMENDATION.md` exists

Verify:
```bash
test -f <project-path>/.eiffel-workflow/research/07-RECOMMENDATION.md && echo "Research complete" || echo "ERROR: Run /eiffel.research first"
```

## CRITICAL: Anti-Slop Rules

**This workflow requires ACTUAL:**
- Reading the research documents (Read tool)
- Generating specs in actual files (Write/Edit tools)
- Verification that design is complete

**FORBIDDEN:**
- Summarizing research without reading actual documents
- Generating specs without writing to files
- Claiming "spec complete" without deliverables

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   ├── research/           (input from /eiffel.research)
│   └── spec/               (output from this phase)
│       ├── 01-PARSED-REQUIREMENTS.md
│       ├── 02-DOMAIN-MODEL.md
│       ├── 03-CHALLENGED-ASSUMPTIONS.md
│       ├── 04-CLASS-DESIGN.md
│       ├── 05-CONTRACT-DESIGN.md
│       ├── 06-INTERFACE-DESIGN.md
│       ├── 07-SPECIFICATION.md
│       └── 08-VALIDATION.md
```

## Good Eiffel Design Principles

```
┌─────────────────────────────────────────────────────────────┐
│              OOSC2 DESIGN PRINCIPLES                        │
├─────────────────────────────────────────────────────────────┤
│  1. SINGLE CHOICE: Decisions made in one place              │
│  2. OPEN/CLOSED: Open for extension, closed for change      │
│  3. COMMAND/QUERY: Queries return, commands modify          │
│  4. UNIFORM ACCESS: Attribute and function interchangeable  │
│  5. DESIGN BY CONTRACT: Pre, post, invariant everywhere     │
│  6. INFORMATION HIDING: Implementation is private           │
│  7. GENERICITY: Parameterize over types                     │
│  8. REUSE: Inherit interface AND implementation             │
└─────────────────────────────────────────────────────────────┘
```

## The 8-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSIS PHASE                           │
├─────────────────────────────────────────────────────────────┤
│  R01: PARSE-RESEARCH       Extract requirements             │
│  R02: DOMAIN-ANALYSIS      Identify domain concepts         │
│  R03: CHALLENGE-ASSUMPTIONS Question everything             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DESIGN PHASE                             │
├─────────────────────────────────────────────────────────────┤
│  R04: CLASS-DESIGN         Design class structure           │
│  R05: CONTRACT-DESIGN      Define all contracts             │
│  R06: INTERFACE-DESIGN     Design public APIs               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    SYNTHESIS PHASE                          │
├─────────────────────────────────────────────────────────────┤
│  R07: SYNTHESIZE-SPEC      Create formal specification      │
│  R08: VALIDATE-DESIGN      Verify design quality            │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

### Step 1: Parse Research (ANALYSIS)

Read all research files and create `<project-path>/.eiffel-workflow/spec/01-PARSED-REQUIREMENTS.md`:

**Extract from research:**
- Scope boundaries (from 01-SCOPE.md)
- Functional requirements (from 03-REQUIREMENTS.md)
- Non-functional requirements (from 03-REQUIREMENTS.md)
- Decisions already made (from 04-DECISIONS.md)
- Innovations to implement (from 05-INNOVATIONS.md)
- Risks to mitigate (from 06-RISKS.md)

**Template:**
```markdown
# PARSED REQUIREMENTS: {project_name}

## Problem Summary
{Consolidated problem statement from research}

## Scope
### In Scope
- {capability from research}

### Out of Scope
- {excluded from research}

## Functional Requirements
| ID | Requirement | Priority | Source | Acceptance |
|----|-------------|----------|--------|------------|
| FR-001 | {req} | MUST | research/03 | {criteria} |

## Non-Functional Requirements
| ID | Requirement | Category | Measure | Target |
|----|-------------|----------|---------|--------|
| NFR-001 | {req} | PERFORMANCE | {measure} | {target} |

## Constraints (simple_* First)
| ID | Constraint | Type |
|----|------------|------|
| C-001 | Must use simple_* over ISE/Gobo where available | ECOSYSTEM |
| C-002 | Must be SCOOP-compatible | TECHNICAL |
| C-003 | Must be void-safe | TECHNICAL |

## Decisions Already Made
| ID | Decision | Rationale | From |
|----|----------|-----------|------|
| D-001 | {decision} | {why} | research/04 |

## Innovations to Implement
| ID | Innovation | Design Impact |
|----|------------|---------------|
| I-001 | {innovation} | {impact} |

## Risks to Address in Design
| ID | Risk | Mitigation Strategy |
|----|------|---------------------|
| RISK-001 | {risk} | {mitigation} |

## Use Cases
### UC-001: {Use Case Name}
**Actor:** {who}
**Precondition:** {what must be true}
**Main Flow:**
1. {step}
2. {step}
**Postcondition:** {what is true after}
```

### Step 2: Domain Analysis (ANALYSIS)

Create `<project-path>/.eiffel-workflow/spec/02-DOMAIN-MODEL.md`:

**Identify domain concepts that will become classes.**

**Template:**
```markdown
# DOMAIN MODEL: {project_name}

## Domain Concepts

### Concept: {Name}
**Definition:** {what it is in the domain}
**Attributes:** {properties it has}
**Behaviors:** {what it does}
**Related to:** {other concepts}
**Will become:** {CLASS_NAME}

## Concept Relationships
```
{Concept A} ──── has-a ────> {Concept B}
{Concept C} ──── is-a ────> {Concept D}
```

## Domain Rules
| Rule | Description | Enforcement |
|------|-------------|-------------|
| DR-001 | {rule} | {how enforced - invariant/precondition} |

## Glossary
| Term | Definition |
|------|------------|
| {term} | {definition} |
```

### Step 3: Challenge Assumptions (ANALYSIS)

Create `<project-path>/.eiffel-workflow/spec/03-CHALLENGED-ASSUMPTIONS.md`:

**Attack mindset - question everything from research.**

**Template:**
```markdown
# CHALLENGED ASSUMPTIONS: {project_name}

## Assumptions Challenged

### A-001: {Assumption from research}
**Challenge:** {why might this be wrong?}
**Evidence for:** {support}
**Evidence against:** {counter-evidence}
**Verdict:** VALID / INVALID / NEEDS_VALIDATION
**Action:** {what to do}

## Requirements Questioned

### FR-XXX: {Requirement}
**Challenge:** {is this really needed?}
**Verdict:** KEEP / MODIFY / REMOVE
**If MODIFY:** {new requirement}

## Missing Requirements Identified
| ID | Missing Requirement | How Discovered |
|----|---------------------|----------------|
| FR-NEW-001 | {requirement} | {how we found it} |

## Design Constraints Validated
| Constraint | Valid? | Notes |
|------------|--------|-------|
| simple_* first | YES | {which simple_* libs apply} |
| SCOOP-compatible | YES | {considerations} |
```

### Step 4: Class Design (DESIGN)

Create `<project-path>/.eiffel-workflow/spec/04-CLASS-DESIGN.md`:

**Apply OOSC2 principles to design classes.**

**Template:**
```markdown
# CLASS DESIGN: {project_name}

## Class Inventory
| Class | Role | Single Responsibility |
|-------|------|----------------------|
| SIMPLE_{X} | Facade | Coordinate library use |
| {X}_ENGINE | Engine | Core algorithm |
| {X}_RESULT | Data | Hold results |
| {X}_CONFIG | Builder | Configuration |

## Facade Design: SIMPLE_{X}

**Purpose:** Single entry point for library functionality
**Responsibility:** Coordinate and delegate to engine classes

**Public Interface:**
```eiffel
class SIMPLE_{X}

create
    make

feature -- Configuration (Builder Pattern)

    set_{option} (a_value: {TYPE}): like Current
        -- Configure {option}. Returns Current for chaining.

feature -- Core Operations

    {operation}: {RESULT_TYPE}
        -- {what it does}

feature -- Status

    is_configured: BOOLEAN
        -- Is ready to execute?
```

**Hides:**
- {ENGINE_CLASS}: algorithm implementation
- {HELPER_CLASS}: utility functions

## Engine Design: {X}_ENGINE

**Purpose:** Implement core algorithm
**Responsibility:** {single responsibility}

```eiffel
class {X}_ENGINE

feature -- Execution

    execute (a_input: {INPUT}): {OUTPUT}
        -- Process input and produce output.
```

## Data Class Design: {X}_RESULT

**Purpose:** Hold operation results
**Immutable:** YES

```eiffel
class {X}_RESULT

feature -- Access

    is_success: BOOLEAN
    data: {DATA_TYPE}
    error: detachable {ERROR_TYPE}

invariant
    success_xor_error: is_success xor (error /= Void)
```

## Inheritance Hierarchy

```
{DEFERRED_BASE}
      │
  ┌───┴───┐
  │       │
{IMPL_A} {IMPL_B}
```

**Inheritance Justification:**
| Child | Parent | IS-A Valid? | Liskov OK? |
|-------|--------|-------------|------------|
| {child} | {parent} | {why IS-A} | YES |

## Generic Classes

| Class | Type Parameter | Constraint | Purpose |
|-------|----------------|------------|---------|
| {CLASS} [G] | G | detachable separate ANY | {why generic} |

## Class Diagram

```
┌─────────────────────────────────────────┐
│            SIMPLE_{X}                   │
│            (Facade)                     │
├─────────────────────────────────────────┤
│ + make                                  │
│ + set_{option}: like Current            │
│ + {operation}: {RESULT}                 │
├─────────────────────────────────────────┤
│ - engine: {X}_ENGINE                    │
└────────────────┬────────────────────────┘
                 │ delegates to
                 ▼
┌─────────────────────────────────────────┐
│            {X}_ENGINE                   │
├─────────────────────────────────────────┤
│ + execute: {X}_RESULT                   │
└────────────────┬────────────────────────┘
                 │ produces
                 ▼
┌─────────────────────────────────────────┐
│            {X}_RESULT                   │
├─────────────────────────────────────────┤
│ + is_success: BOOLEAN                   │
│ + data: {TYPE}                          │
└─────────────────────────────────────────┘
```
```

### Step 5: Contract Design (DESIGN)

Create `<project-path>/.eiffel-workflow/spec/05-CONTRACT-DESIGN.md`:

**Define all contracts using MML where appropriate.**

**Template:**
```markdown
# CONTRACT DESIGN: {project_name}

## MML Model Queries

For each collection, define model query:

| Attribute | Type | Model Query | MML Type |
|-----------|------|-------------|----------|
| items | HASH_TABLE | items_model | MML_MAP |
| list | ARRAYED_LIST | list_model | MML_SEQUENCE |

## Class Contracts

### SIMPLE_{X}

**Creation Contract:**
```eiffel
make
    ensure
        not_configured: not is_configured
        {initial state}
```

**Command Contracts:**
```eiffel
set_{option} (a_value: {TYPE}): like Current
    require
        valid_value: {precondition}
    ensure
        option_set: {option} = a_value
        others_unchanged: {frame condition using MML |=|}
        result_is_current: Result = Current
```

**Query Contracts:**
```eiffel
{query}: {TYPE}
    require
        configured: is_configured
    ensure
        result_valid: {postcondition}
```

**Invariant:**
```eiffel
invariant
    {class invariant}
```

### {X}_RESULT

**Invariant (XOR pattern):**
```eiffel
invariant
    success_xor_error: is_success xor (error /= Void)
    success_has_data: is_success implies data /= Void
```

## Contract Completeness Checklist

Every postcondition must answer:
- [ ] **What changed?** (direct effect)
- [ ] **How did it change?** (relationship to `old` state)
- [ ] **What did NOT change?** (frame conditions via MML `|=|`)
```

### Step 6: Interface Design (DESIGN)

Create `<project-path>/.eiffel-workflow/spec/06-INTERFACE-DESIGN.md`:

**Design the public API following Eiffel idioms.**

**Template:**
```markdown
# INTERFACE DESIGN: {project_name}

## Public API Summary

### Creation
| Feature | Purpose | Typical Use |
|---------|---------|-------------|
| make | Default creation | `create obj.make` |
| make_with_{x} | Creation with config | `create obj.make_with_x (val)` |

### Configuration (Builder Pattern)
| Feature | Returns | Purpose |
|---------|---------|---------|
| set_{option} | like Current | Configure {option} |
| with_{option} | like Current | Fluent alias |

### Core Operations
| Feature | Returns | Purpose |
|---------|---------|---------|
| {operation} | {RESULT} | {what it does} |

### Status Queries
| Feature | Returns | Purpose |
|---------|---------|---------|
| is_configured | BOOLEAN | Ready to use? |
| is_{state} | BOOLEAN | In {state}? |

## Fluent API Example

```eiffel
result := create {SIMPLE_{X}}.make
    .set_option_a (value_a)
    .set_option_b (value_b)
    .execute (input)
```

## Error Handling Pattern

```eiffel
result := obj.execute (input)
if result.is_success then
    process (result.data)
else
    handle_error (result.error)
end
```

## Command-Query Separation

| Feature | Type | Modifies State? | Returns Value? |
|---------|------|-----------------|----------------|
| set_{x} | Command | YES | like Current (for chaining) |
| {query} | Query | NO | YES |
| execute | Command | YES | {RESULT} (exception to CQS) |
```

### Step 7: Synthesize Specification (SYNTHESIS)

Create `<project-path>/.eiffel-workflow/spec/07-SPECIFICATION.md`:

**Combine all design into formal specification.**

**Template:**
```markdown
# SPECIFICATION: {project_name}

## Overview
{Brief description from research recommendation}

## Class Specifications

### SIMPLE_{X} (Facade)

```eiffel
note
    description: "{description}"
    author: "Larry Rix"

class
    SIMPLE_{X}

create
    make

feature {NONE} -- Initialization

    make
            -- Create unconfigured instance.
        do
            {initialization}
        ensure
            not_configured: not is_configured
        end

feature -- Configuration

    set_{option} (a_value: {TYPE}): like Current
            -- Set {option} to `a_value`.
        require
            valid: {precondition}
        do
            {option} := a_value
            Result := Current
        ensure
            set: {option} = a_value
            result_current: Result = Current
        end

feature -- Model Queries

    {items}_model: MML_{TYPE}
            -- Mathematical model of {items}.
        do
            create Result
            across {items} as ic loop
                Result := Result.{operation} (@ic.key, @ic.item)
            end
        end

feature -- Core Operations

    {operation}: {RESULT_TYPE}
            -- {description}
        require
            configured: is_configured
        do
            {implementation stub}
        ensure
            {postcondition}
        end

feature -- Status

    is_configured: BOOLEAN
            -- Is ready for operation?
        do
            Result := {condition}
        end

feature {NONE} -- Implementation

    {private_attribute}: {TYPE}

invariant
    {invariant}

end
```

### {X}_RESULT (Data)

```eiffel
{full class specification}
```

## Dependencies

| Library | Purpose | Version |
|---------|---------|---------|
| simple_mml | MML postconditions | 1.0.1+ |
| {simple_*} | {purpose} | {version} |

## File Structure

```
src/
├── simple_{x}.e         (Facade)
├── {x}_engine.e         (Engine)
├── {x}_result.e         (Result)
└── {x}_config.e         (Config if needed)

test/
├── test_{x}.e           (Unit tests)
└── test_app.e           (Test runner)
```
```

### Step 8: Validate Design (SYNTHESIS)

Create `<project-path>/.eiffel-workflow/spec/08-VALIDATION.md`:

**Verify the design meets all criteria.**

**Template:**
```markdown
# DESIGN VALIDATION: {project_name}

## OOSC2 Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| Single Responsibility | ✓/✗ | {each class has one job} |
| Open/Closed | ✓/✗ | {extensible without modification} |
| Liskov Substitution | ✓/✗ | {inheritance is proper IS-A} |
| Interface Segregation | ✓/✗ | {interfaces are focused} |
| Dependency Inversion | ✓/✗ | {depends on abstractions} |

## Eiffel Excellence

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Command-Query Separation | ✓/✗ | {CQS followed} |
| Uniform Access | ✓/✗ | {attributes vs functions} |
| Design by Contract | ✓/✗ | {full contract coverage} |
| Genericity | ✓/✗ | {appropriate use} |
| Inheritance | ✓/✗ | {IS-A only} |
| Information Hiding | ✓/✗ | {implementation private} |

## Practical Quality

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Void-safe | ✓/✗ | {detachable handled} |
| SCOOP-compatible | ✓/✗ | {separate where needed} |
| simple_* first | ✓/✗ | {ecosystem compliance} |
| MML postconditions | ✓/✗ | {frame conditions} |
| Testable | ✓/✗ | {can be tested} |

## Requirements Traceability

| Requirement | Addressed By | Status |
|-------------|--------------|--------|
| FR-001 | SIMPLE_{X}.{feature} | ✓ |
| NFR-001 | {design decision} | ✓ |

## Risk Mitigations Implemented

| Risk | Mitigation in Design |
|------|---------------------|
| RISK-001 | {how design addresses it} |

## Open Issues
{Any unresolved design questions}

## Ready for Implementation
- [ ] All requirements traced
- [ ] All risks mitigated
- [ ] All principles satisfied
- [ ] Design is complete

**VERDICT:** READY / NEEDS_WORK
```

### Step 9: Save Evidence

Create `<project-path>/.eiffel-workflow/evidence/pre-phase-spec.txt`:
```
# Pre-Phase Specification Evidence
# Project: <project-path>
# Date: [timestamp]

Specification completed: [yes/no]
Steps completed: 8/8
Classes designed: [count]
Contracts defined: [count]
Requirements traced: [count]

OOSC2 compliance: [PASS/FAIL]
Eiffel excellence: [PASS/FAIL]
Ready for implementation: [yes/no]

# Status: COMPLETE
```

## Completion

```
Pre-Phase SPEC COMPLETE: Specification designed.
Project: <project-path>

Files:
  - .eiffel-workflow/spec/01-PARSED-REQUIREMENTS.md
  - .eiffel-workflow/spec/02-DOMAIN-MODEL.md
  - .eiffel-workflow/spec/03-CHALLENGED-ASSUMPTIONS.md
  - .eiffel-workflow/spec/04-CLASS-DESIGN.md
  - .eiffel-workflow/spec/05-CONTRACT-DESIGN.md
  - .eiffel-workflow/spec/06-INTERFACE-DESIGN.md
  - .eiffel-workflow/spec/07-SPECIFICATION.md
  - .eiffel-workflow/spec/08-VALIDATION.md

Classes designed: {count}

Next: Run /eiffel.intent <project-path> to capture refined intent from specification.
```

## Context Management (RLM Pattern)

**DO:**
- Read all research files before designing
- Write spec files as you complete each step
- Use Task tool with Explore agent for ecosystem patterns

**DO NOT:**
- Skip reading research documents
- Generate specs without writing to files
- Claim completion without validation

## Anti-Drift

- **Research drives design** - Don't invent requirements not in research
- **OOSC2 principles enforced** - Every design choice must follow principles
- **Contracts are complete** - What changed, how, what didn't
- **simple_* first** - Check ecosystem before adding ISE/Gobo dependencies
- **Traceability required** - Every requirement must map to design
