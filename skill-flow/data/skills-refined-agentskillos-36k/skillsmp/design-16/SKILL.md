---
name: design
description: Design Ops v2.2 gold standard. Transform intent → validated specs → executable PRPs through 11-step invariant-enforced pipeline. USE WHEN design, spec, PRP, validate, requirements, init project, review implementation.
---

# Design Ops v2.2 Skill

**THIS IS THE PRODUCTION GOLD STANDARD.** You MUST follow the 11-step validated pipeline exactly as written. Each step is non-negotiable.

## The 11-Step Pipeline (You Must Follow This)

Design Ops v2.2 enforces a single, non-negotiable workflow:

```
0. /design spec {journey}              ← Create spec FROM journey
1. /design stress-test {spec}          ← Check COMPLETENESS
2. /design validate {spec}             ← Check CLARITY
3. /design prp {spec}                  ← Compile to PRP (alias: generate)
4. /design check {prp}                 ← Verify PRP QUALITY
5. /design implement {prp}             ← Generate TESTS (TDD)
6. /design test-validate {tests}       ← Validate TEST SUITE
7. /design test-cohesion {tests}       ← Check TEST INTERACTIONS
8. /design ralph-check {prp}           ← Verify PRP COMPLIANCE
9. /design run {prp}                   ← AI IMPLEMENTS
10. Retrospective (learning loop)      ← Extract LEARNINGS
```

**Why This Order Matters:**

| Steps | Purpose | Catches |
|-------|---------|---------|
| 0-2   | Specification validation | Incompleteness, ambiguity, vague terms |
| 3-4   | PRP compilation & QA | Incomplete extraction, structural issues |
| 5-8   | Test preparation & verification | Test design gaps, coverage issues |
| 9-10  | Implementation & learning | Edge cases, retrospective patterns |

**Critical Rule**: You may not skip steps. Each catches different problems. Skipping will cause preventable failures.

## Context Architecture

Design Ops splits heavy operations into forked context to keep main conversation clean:

```
Main (shared)           Forked (isolated)
─────────────           ─────────────────
/design spec            /design stress-test
/design init            /design validate
/design dashboard       /design check
                        /design test-validate
                        /design test-cohesion
```

Forked operations return concise summaries; full analysis stays isolated.

## Command Reference (v2.2 Pipeline)

### Step 0: Spec Creation

#### `/design spec {journey-file}`
Generate a specification from a user journey.
- **Input**: Journey markdown file with steps, pain points, goals
- **Output**: Structured spec (problem, requirements, success criteria)
- **Next**: `/design stress-test`

### Steps 1-2: Validation Gates (Must Both Pass)

#### `/design stress-test {spec}`
Check spec COMPLETENESS against domain invariants.
- Detects: Missing error cases, null states, external failures, concurrency issues
- Returns: PASS or REVIEW REQUIRED with specific blockers
- **Next**: Fix blockers, then `/design validate`

#### `/design validate {spec}`
Check spec CLARITY (invariants 1-11).
- Detects: Ambiguity, implicit assumptions, untestable criteria, silent failures
- Returns: PASS or REJECTED with fixes
- **Next**: `/design prp`

### Step 3: PRP Compilation

#### `/design prp {spec}` (alias: `/design generate`)
Compile validated spec into executable PRP.
- Extracts: confidence, thinking level, verbatim content, patterns
- Runs dependency-trace (INV-L010/L011)
- **Next**: `/design check`

### Steps 4-8: Quality Assurance Pipeline

#### `/design check {prp}`
Verify PRP quality and extraction completeness.
- Compares source spec vs generated PRP content
- Detects: Missing sections, unfilled placeholders, LLM artifacts
- **Next**: Human review, then `/design implement`

#### `/design implement {prp}`
Generate test suite (TDD mode).
- Creates: test_NN.py, gate_N.py, conftest.py
- No step files — tests ARE the contract
- **Next**: `/design test-validate`

#### `/design test-validate {test-files}`
Validate test suite (syntax, coverage, integration).
- **Next**: `/design test-cohesion`

#### `/design test-cohesion {test-directory}`
Verify test interactions (no duplicates, fixtures, imports).
- **Next**: `/design ralph-check`

#### `/design ralph-check {prp}`
Verify PRP compliance with schema and routes.
- **Next**: `/design run`

### Step 9: AI Implementation

#### `/design run {prp}`
AI implements code to pass test suite.
- Iterates until all tests pass
- Uses test feedback as oracle

### Step 10: Learning

Retrospective → Extract learnings → Propose invariants → System improves

## Multi-Agent Architecture (v2.2)

Design Ops v2.2 runs specialized agents in parallel during compilation:

| Agent | Role | Runs During |
|-------|------|-------------|
| **spec-analyst** | Completeness & complexity analysis | stress-test |
| **validator** | Invariant enforcement (1-43) | validate |
| **CONVENTIONS-checker** | Codebase pattern alignment | check |
| **prp-generator** | Spec → PRP transformation | prp |
| **reviewer** | Quality gate enforcement | check |
| **ralph-checker** | PRP schema compliance | ralph-check |

Each agent has specific expertise. Parallel execution is automatic.

## Key Files

```
design-ops/
├── SKILL.md                 # This file (command reference)
├── design.md                # Full skill definition (v2.2)
├── README.md                # Overview & architecture
├── system-invariants.md     # Invariants 1-11
├── domains/                 # Domain-specific invariants (12-43)
│   ├── consumer-product.md
│   ├── physical-construction.md
│   ├── data-architecture.md
│   ├── integration.md
│   ├── remote-management.md
│   └── skill-gap-transcendence.md
├── enforcement/
│   ├── design-ops-v3.sh     # Main orchestrator
│   ├── validator.sh
│   ├── stress-test.sh
│   └── ... (all 11 steps)
├── templates/               # PRP & spec templates
├── examples/                # Complete working examples
└── tools/                   # Automation & utilities
```

## Typical Usage

```bash
# Journey → Spec → Validate → PRP → Tests → Implement
/design spec journeys/user-flow.md
/design stress-test specs/feature.md
/design validate specs/feature.md
/design prp specs/feature.md
/design check PRPs/feature.md
/design implement PRPs/feature.md
# ... steps 6-10 ...
```

---

**Version**: 2.2 (Production Gold Standard)
**Requirement**: Claude Code 2.1.0+
**Last updated**: 2026-01-26
