# Dangerous Mode: Visual Diagrams

Flowcharts and timeline diagrams for dangerous mode learning auto-promotion system.

---

## 1. Learning → Invariant Promotion Flowchart

```
                    ┌─────────────────────┐
                    │  Step Execution    │
                    │  (PRP Running)      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Extract Learning    │
                    │ - Observation       │
                    │ - Context           │
                    │ - Framework         │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │ Calculate Confidence Score │
                    │ (0.0 - 1.0)                │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │ Dangerous Mode Decision   │
                    │ (Auto-Promotion)           │
                    └──────────┬──────────────────┘
                               │
                ┌──────────────┼──────────────────┐
                │              │                  │
         score>=0.80    0.50<=score<0.80   score<0.50
                │              │                  │
                ▼              ▼                  ▼
            ┌────────┐    ┌────────┐       ┌────────┐
            │PROMOTE │    │ACCEPT  │       │REJECT  │
            └────┬───┘    └────┬───┘       └────────┘
                 │             │
                 ▼             ▼
          ┌─────────────┐  ┌──────────────┐
          │System       │  │Project       │
          │Invariant    │  │Learning      │
          │(INV-L{N})   │  │(Local)       │
          └──────┬──────┘  └──────────────┘
                 │
                 ▼
          ┌─────────────────────────────┐
          │ Create Task:                │
          │ promote-invariant-INV-L{N}  │
          └──────┬──────────────────────┘
                 │
                 ▼
          ┌─────────────────────────────┐
          │ Register to                 │
          │ learned-invariants.md       │
          └──────┬──────────────────────┘
                 │
                 ▼
          ┌─────────────────────────────┐
          │ Future /design validate     │
          │ commands use INV-L{N}       │
          └─────────────────────────────┘
```

---

## 2. Three-PRP Execution Timeline with Learning Feedback

```
WEEK 1: PRP-001 (No constraints yet)
┌──────────────────────────────────────────────────────────────┐
│                                                                │
│  Mon: /design validate (core invariants only)               │
│       /design prp → PRP-001                                 │
│                                                                │
│  Tue-Wed: /design run --dangerous PRP-001                   │
│       Step 1: Design model [OK]                             │
│       Step 2: Implement API [OK]                            │
│       Step 3: Build UI routes                               │
│              └─ Learning: Routes need handlers              │
│              └─ Confidence: 0.95                            │
│              └─ Auto-promote → INV-L001 ✓                   │
│       Step 4: Add filters                                   │
│              └─ Learning: Filters need edge case tests      │
│              └─ Confidence: 0.92                            │
│              └─ Auto-promote → INV-L002 ✓                   │
│       Step 5: Test [OK]                                     │
│                                                                │
│  Thu: /design retrospective                                 │
│       Document INV-L001, INV-L002                           │
│                                                                │
│  Status: ✓ Complete (2 learned invariants created)         │
│                                                                │
└──────────────────────────────────────────────────────────────┘
         Invariant Registry After PRP-001:
         └─ INV-L001 (Routes): confidence 0.95
         └─ INV-L002 (Filters): confidence 0.92


WEEK 2: PRP-002 (Constrained by PRP-001 learnings)
┌──────────────────────────────────────────────────────────────┐
│                                                                │
│  Mon: Write spec for search feature                          │
│       /design validate specs/search.md --include-learned     │
│       └─ Checks against core + learned (INV-L001, L002)    │
│       └─ PRP-002 respects both ✓                             │
│       /design prp → PRP-002                                 │
│                                                                │
│  Tue-Wed: /design run --dangerous PRP-002                   │
│       Step 1: Design schema [OK]                            │
│       Step 2: Implement search API                          │
│              └─ Learning: Large result sets need pagination │
│              └─ Confidence: 0.91                            │
│              └─ Auto-promote → INV-L003 ✓                   │
│       Step 3: Build search UI                               │
│              └─ Validation: Routes tested (respects INV-L001) ✓
│       Step 4: Add filter/sort                               │
│              └─ Validation: Edge cases tested (respects INV-L002) ✓
│              └─ Learning: Cache invalidation patterns       │
│              └─ Confidence: 0.87                            │
│              └─ Auto-promote → INV-L004 ✓                   │
│       Step 5: E2E Testing [OK]                              │
│                                                                │
│  Thu: /design retrospective                                 │
│       Document INV-L003, INV-L004                           │
│                                                                │
│  Status: ✓ Complete (4 learned invariants total)            │
│                                                                │
└──────────────────────────────────────────────────────────────┘
         Invariant Registry After PRP-002:
         ├─ INV-L001 (Routes): confidence 0.95 [+1 validation]
         ├─ INV-L002 (Filters): confidence 0.92 [+1 validation]
         ├─ INV-L003 (Pagination): confidence 0.91
         └─ INV-L004 (Cache): confidence 0.87


WEEK 3: PRP-003 (Constrained by PRP-001 & PRP-002 learnings)
┌──────────────────────────────────────────────────────────────┐
│                                                                │
│  Mon: Write spec for admin dashboard                         │
│       /design validate specs/admin.md --include-learned      │
│       └─ Checks core + learned (INV-L001, L002, L003, L004) │
│       └─ All 4 constraints satisfied ✓                       │
│       /design prp → PRP-003                                 │
│                                                                │
│  Tue-Wed: /design run --dangerous PRP-003                   │
│       Step 1: Design admin model [OK]                       │
│       Step 2: Implement admin APIs                          │
│              └─ Validation: Routes tested (respects INV-L001) ✓
│              └─ Validation: Cache invalidation (respects INV-L004) ✓
│       Step 3: Build admin UI                                │
│              └─ Learning: RBAC patterns important           │
│              └─ Confidence: 0.88                            │
│              └─ Auto-promote → INV-L005 ✓                   │
│       Step 4: Add admin filters                             │
│              └─ Validation: Edge cases (respects INV-L002) ✓
│              └─ Validation: Pagination (respects INV-L003) ✓
│       Step 5: Audit logging                                 │
│              └─ Learning: Audit logs must be structured     │
│              └─ Confidence: 0.93                            │
│              └─ Auto-promote → INV-L006 ✓                   │
│       Step 6: E2E Testing [OK]                              │
│                                                                │
│  Thu: /design retrospective                                 │
│       Document INV-L005, INV-L006                           │
│                                                                │
│  Status: ✓ Complete (6 learned invariants total)            │
│                                                                │
└──────────────────────────────────────────────────────────────┘
         Invariant Registry After PRP-003:
         ├─ INV-L001 (Routes): confidence 0.95 [+2 validations]
         ├─ INV-L002 (Filters): confidence 0.92 [+2 validations]
         ├─ INV-L003 (Pagination): confidence 0.91 [+1 validation]
         ├─ INV-L004 (Cache): confidence 0.87 [+1 validation]
         ├─ INV-L005 (RBAC): confidence 0.88 [new]
         └─ INV-L006 (Audit): confidence 0.93 [new]


TREND: Each cycle learns while respecting prior learnings
       System grows smarter, execution gets faster
```

---

## 3. PRP Dependency Graph: Task Ordering

```
PRP-001: Step Execution + Learning Capture

  prp-001-step-1 [Design model]
          │
          ▼
  prp-001-step-2 [API endpoints]
          │
     ┌────┴────┐
     │         │
     ▼         ▼
 step-3    step-4 [Filters]
 [Routes]  │
 │         ├─ generate-learning-LEARN-002
 │         │  │
 │         │  └─ promote-invariant-INV-L002
 │         │     │
 │         │     └─ register INV-L002
 │         │
 │         ▼
 ├─ generate-learning-LEARN-001
 │  │
 │  └─ promote-invariant-INV-L001
 │     │
 │     └─ register INV-L001
 │
 └─────────────┬────────────────┘
               │
               ▼
        prp-001-step-5 [Test]
               │
               ▼
     prp-001-retrospective
               │
               └─ blocked-by: [promote-invariant-INV-L001, INV-L002]
               └─ documents learned invariants


PRP-002: Validation + Execution (Constrained)

  validate-prp-002-against-learned
       │
       └─ blocked-by: [promote-invariant-INV-L001, INV-L002]
               │
               ▼
       prp-002-generation
               │
               ├─ meta: respects INV-L001, L002
               │
               ▼
       prp-002-step-1
           │
           ▼
       prp-002-step-2 [Search API]
       │ │ respects INV-L001 ✓
       │ └─ generate-learning-LEARN-003
       │    │
       │    └─ promote-invariant-INV-L003
       │
       └─ prp-002-step-4 [Filters]
           │ respects INV-L002 ✓
           └─ generate-learning-LEARN-004
              │
              └─ promote-invariant-INV-L004


PRP-003: Validation + Execution (Fully Constrained)

  validate-prp-003-against-learned
       │
       └─ blocked-by: [promote-invariant-INV-L001, L002, L003, L004]
               │
               ▼
       prp-003-generation
               │
               ├─ meta: respects INV-L001, L002, L003, L004
               │
               ▼
       prp-003-step-1 through step-6
               │ Each step validates against 4 learned invariants
               │
               └─ prp-003-step-3 [RBAC]
                  └─ generate-learning-LEARN-005
                     └─ promote-invariant-INV-L005

               └─ prp-003-step-5 [Audit]
                  └─ generate-learning-LEARN-006
                     └─ promote-invariant-INV-L006
```

---

## 4. Invariant Confidence Evolution

```
INVARIANT: INV-L001 (Route Coverage)

v1.0 - Initial Creation (Week 1, PRP-001)
┌────────────────────────────────┐
│ Created: 2026-01-23            │
│ Source: PRP-001 Step 3         │
│ Confidence: 0.95               │
│ Status: ACTIVE                 │
│ Validations: 0                 │
│ Violations: 0                  │
└────────────────────────────────┘
           │
           │ (PRP-002 respects invariant)
           ▼
v1.0+ - First Validation (Week 2, PRP-002)
┌────────────────────────────────┐
│ Same rule, same confidence     │
│ BUT: Validated in PRP-002      │
│ Confidence still: 0.95         │
│ Validations: 1                 │
│ Violations: 0                  │
└────────────────────────────────┘
           │
           │ (PRP-003 respects invariant)
           ▼
v1.0+ - Second Validation (Week 3, PRP-003)
┌────────────────────────────────┐
│ Same rule                      │
│ Validated in PRP-003           │
│ Confidence still: 0.95         │
│ Validations: 2                 │
│ Violations: 0                  │
│ Status: Ready for v1.1         │
└────────────────────────────────┘
           │
           │ (Confident enough to refine)
           ▼
v1.1 - Refined (Week 4, Retrospective)
┌────────────────────────────────┐
│ Updated: 2026-01-27            │
│ Source: PRP-001/002/003        │
│ Confidence: 0.98 (↑ from 0.95) │
│ Changes:                       │
│  - Added domain scoping        │
│  - Excluded SSR apps           │
│  - Better validation method    │
│ Validations: 3                 │
│ Violations: 0                  │
│ Status: ACTIVE (refined)       │
└────────────────────────────────┘

Timeline:
  Day 1:  0.95 (initial, confident)
  Day 4:  0.95 (validated, still confident)
  Day 8:  0.95 (validated again, ready to refine)
  Day 12: 0.98 (refined with more context)

Calibration: Predictions accurate to ±0.03 ✓
```

---

## 5. Stress-Test Violation Detection

```
Future PRP Created
        │
        ▼
  /design stress-test --learned
        │
        ├─ Check INV-L001 (Route Coverage)
        │  ├─ Specification references /users/{id}
        │  ├─ Check: Does route handler exist?
        │  ├─ Result: ✗ NO HANDLER FOUND
        │  │
        │  └─ VIOLATION DETECTED
        │     ├─ Severity: HIGH
        │     ├─ Impact: Users see 404
        │     ├─ Fix: Add route handler step
        │     └─ Block: PRP cannot execute until fixed
        │
        ├─ Check INV-L002 (Filter Edge Cases)
        │  ├─ Specification has date filter: days <= 14
        │  ├─ Check: Negative days handled?
        │  ├─ Result: ✗ NO TEST FOR NEGATIVE
        │  │
        │  └─ VIOLATION DETECTED
        │     ├─ Severity: HIGH
        │     ├─ Impact: Filters include past dates
        │     ├─ Fix: Add negative date test
        │     └─ Block: PRP cannot execute until fixed
        │
        └─ Check INV-L003 (Pagination)
           ├─ Specification fetches user list
           ├─ Check: Pagination implemented?
           ├─ Result: ✓ YES, paginated
           │
           └─ PASS
              ├─ Severity: N/A
              ├─ Impact: None (good)
              └─ Result: Constraint satisfied

Stress Test Summary:
  ├─ Passed: 1/3
  ├─ Failed: 2/3
  ├─ Blocking issues: 2
  └─ Status: NOT READY
     Fix violations and re-stress-test before execution
```

---

## 6. System Invariant Maturity Curve

```
Learned Invariants Over Time

Count
  │
 8│                        ●
  │                       ●
 7│                      ●
  │                     ●
 6│                   ●
  │                 ●
 5│              ●
  │            ●
 4│          ●
  │        ●
 3│      ●
  │    ●
 2│  ●
  │●
 1│
  └─────────────────────────────────────────────
    W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 Week

Growth Pattern:
  ├─ Week 1-3: Rapid learning (2-3 invariants/week)
  ├─ Week 4-6: Steady learning (2 invariants/week)
  ├─ Week 7+:  Plateau (fewer new learnings, refining existing)
  │
  └─ Indicator of system maturity:
     ├─ ✓ Good: Growth rate decreases (reaching saturation)
     ├─ ✓ Good: Confidence increasing (better validation)
     ├─ ⚠️ Caution: Growth stalled (might miss patterns)
     └─ ✗ Bad: Confidence inflation (predictions > actual)
```

---

## 7. Confidence Score Distribution

```
Learned Invariants by Confidence Level

0.95-1.0 ░░░░░░░░░░ (5 invariants)
         INV-L001, L002, L006, L007, L008

0.90-0.94 ░░░░░░░░ (3 invariants)
         INV-L003, L004, L005

0.80-0.89 ░░░░░░░░░░░░ (4 invariants)
         INV-L009, L010, L011, L012

0.70-0.79 ░░░░ (0 invariants - these would be ACCEPT only)
         (empty)

0.50-0.69 ░░░ (3 project-local learnings, not promoted)
         (in project-learnings.md)

< 0.50   ░ (rejected - no record)

Distribution Analysis:
  └─ 12 promoted (avg confidence: 0.91)
  └─ 3 project-local (avg confidence: 0.63)
  └─ Many rejected (confidence < 0.50)

System Health: Good
  ├─ Most promoted invariants have high confidence
  ├─ Few false positives (low-confidence promoted)
  └─ Clear separation between promote/accept thresholds
```

---

## 8. Validation Gate Coverage

```
PRP Validation Layers

Layer 1: Core Invariants (1-11)
┌──────────────────────────────────┐
│ Ambiguity, State, Emotion,       │
│ No Irreversible, Fail Loudly,    │
│ Bounded Scope, Executable Tests, │
│ Cost Limits, Blast Radius,       │
│ Degradation, Accessibility       │
└────────────┬─────────────────────┘
             │ ALL SPECS MUST PASS
             ▼
Layer 2: Domain Invariants
┌──────────────────────────────────┐
│ consumer-product: UI, A11y, etc  │
│ data-architecture: Scale, etc    │
│ integration: API contracts, etc  │
└────────────┬─────────────────────┘
             │ (if domain specified)
             ▼
Layer 3: Learned Invariants (INV-L001+)
┌──────────────────────────────────┐
│ Routes, Filters, Pagination,     │
│ Cache Invalidation, RBAC,        │
│ Audit Logging, ...               │
└────────────┬─────────────────────┘
             │ (dynamic, grows with PRPs)
             ▼
PASS: Ready for PRP compilation
FAIL: Fix violations, re-validate

Example: PRP-003 Validation
  ├─ Layer 1 (core): 11/11 PASS ✓
  ├─ Layer 2 (domain): 5/5 PASS ✓
  ├─ Layer 3 (learned): 4/4 PASS ✓
  │  ├─ INV-L001: Routes have tests ✓
  │  ├─ INV-L002: Filters test edge cases ✓
  │  ├─ INV-L003: Pagination implemented ✓
  │  └─ INV-L004: Cache invalidation included ✓
  └─ OVERALL: PASS (ready for execution)
```

---

## 9. Promotion Decision Matrix

```
         Confidence Score
            ↓
        0   0.5  0.8   1.0
        │────┼────┼────→
        │    │    │
REJECT  │ ■  │    │      No permanent record
        │    │    │
────────────────────────────────────────────
        │    │    │
ACCEPT  │    │ ■  │      Project-local learning
        │    │    │      (in project-learnings.md)
────────────────────────────────────────────
        │    │    │
PROMOTE │    │    │ ■    System invariant
        │    │    │      (in learned-invariants.md)
        │    │    │      Affects future PRPs
        │    │    │

Decision Rules:
┌─────────────────────────────────────────────────────┐
│ confidence >= 0.80 → PROMOTE (system invariant)    │
│ 0.50 <= confidence < 0.80 → ACCEPT (project-local) │
│ confidence < 0.50 → REJECT (discard)               │
│                                                     │
│ Override: --promote-manual flag allows manual      │
│           promotion regardless of score            │
└─────────────────────────────────────────────────────┘
```

---

## 10. System Learning Velocity Graph

```
Dangerous Mode: System Learning Efficiency

     Invariants
     Created    ┌─── PRP-1
  Per Week   5  │      (2 learned)
              4  │
              3  │     ┌─── PRP-2
              2  │ ╱╲  │   (2 learned)
              1  │╱  ╲ │  ╱╲
              0  └────╲│╱──┴───────── Plateau
                      (System mature)
              ├──┴──┬──┴──┬────┬────┤
              W1    W2    W3   W4  W5

Execution Time Per PRP

  PRP-1: 20 hours
    ├─ Slow (learning, no constraints)
    └─ Creates 2 invariants
         │
         ▼
  PRP-2: 18 hours (2 hour savings)
    ├─ Faster (respects 2 constraints)
    └─ Creates 2 more invariants
         │
         ▼
  PRP-3: 16 hours (4 hour savings vs PRP-1)
    ├─ Even faster (respects 4 constraints)
    ├─ Design-time catches edge cases
    └─ Creates 2 more invariants

Cumulative Learning Effect:
  └─ Each cycle executes faster
  └─ Fewer surprises (learned constraints prevent issues)
  └─ System knowledge compounds (network effect)

ROI Comparison:
  ├─ Without dangerous mode:
  │  └─ Each PRP re-discovers patterns
  │  └─ Execution time constant (20 hours)
  │
  └─ With dangerous mode:
     └─ Execution time decreases (20 → 18 → 16 hours)
     └─ Compounding savings (4 + 2 + 2... hours saved)
     └─ By PRP-10, each saves 30% time vs PRP-1
```

---

*Diagrams v1.0*
*All flows integrated into dangerous mode learning pipeline*
