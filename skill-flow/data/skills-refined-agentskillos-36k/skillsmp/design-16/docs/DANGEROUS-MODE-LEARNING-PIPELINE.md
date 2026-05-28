# Dangerous Mode Learning Auto-Promotion Pipeline

Comprehensive guide to how dangerous mode integrates step execution, learning capture, invariant creation, and future PRP validation into a continuous improvement cycle.

---

## Executive Summary

**Dangerous Mode Fast-Track System:**
- Execute steps with learning capture enabled
- Confidence-based auto-promotion: high-confidence learnings → new system invariants
- New invariants constrain future PRPs at design time
- Future PRP compilation validates against learned + core invariants
- Feedback loop: PRP 1 → Learnings → Invariants → PRP 2 (constrained) → More Learnings

**Key insight:** Dangerous mode trades human review overhead for system learning velocity. Each execution teaches the system; future PRPs inherit that knowledge as hard constraints.

---

## 1. Learning → Invariant Promotion Pipeline

### 1.1 Step Execution with Learning Capture

When you run `/design run --dangerous`:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP EXECUTION WITH LEARNING CAPTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Execute step (e.g., "Implement auth handler")           │
│  2. Capture execution context:                              │
│     - Which PRP (e.g., PRP-2026-01-22-001)                │
│     - Which step (e.g., step 3 of 7)                       │
│     - Which phase (e.g., "implementation")                 │
│     - Start time, end time                                 │
│  3. During execution, extract learnings:                   │
│     - Technology facts discovered                          │
│     - Patterns applied successfully                        │
│     - Edge cases encountered                               │
│     - Assumptions that proved correct/incorrect            │
│  4. Assign confidence score (0.0-1.0) to each learning    │
│     - 0.8+: "I'm very sure this applies generally"        │
│     - 0.5-0.79: "This applies in my project context"      │
│     - <0.5: "I'm uncertain; need more evidence"           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Example Learning Captured During PRP Execution:**

```yaml
learning_id: LEARN-2026-01-23-001
source_prp: PRP-2026-01-22-001
source_step: 3 (Implement route handlers)
source_phase: implementation
timestamp: 2026-01-23T14:22:15Z

observation: |
  When building Dash apps with dynamic routes, every internal link (href)
  must have a corresponding route handler. If route doesn't exist, users
  see "Page not found" instead of the target page.

confidence: 0.95
confidence_reasoning: |
  Observed this in 2 Dash projects, tested with route verification,
  matches SPA framework patterns (React Router, Next.js also require this).

applies_to: ["consumer-product", "single-page-apps", "dash-apps"]
```

### 1.2 Dangerous Mode Auto-Decision

When learning is captured, dangerous mode evaluates automatically:

```
┌─────────────────────────────────────────────────────────────┐
│ DANGEROUS MODE AUTO-PROMOTION DECISION                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  confidence_score >= 0.80?                                 │
│    YES → PROMOTE (Create invariant task)                   │
│         └─ New system invariant INV-L001 created           │
│         └─ Task created: promote-invariant-INV-L001        │
│         └─ Log: "Learning promoted to system invariant"    │
│                                                              │
│  confidence_score 0.50-0.79?                               │
│    YES → ACCEPT (Add to project learnings)                 │
│         └─ Saved in project's learning-document.md         │
│         └─ Not system-wide (project-scoped)                │
│         └─ Log: "Learning accepted, project-local scope"   │
│                                                              │
│  confidence_score < 0.50?                                  │
│    YES → REJECT (Discard)                                  │
│         └─ Not captured permanently                        │
│         └─ Can be re-observed if pattern repeats           │
│         └─ Log: "Insufficient confidence, rejected"        │
│                                                              │
│  Human override (--promote-manual)?                        │
│    YES → Force promote regardless of score                 │
│         └─ Use for high-impact learnings you're confident in
│         └─ Still requires human review                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Decision Logic Implementation:**

```python
def auto_promote_learning(learning, confidence_score, mode='dangerous'):
    """
    Automatic promotion of learning to invariant (dangerous mode).
    """
    decision = {
        'learning_id': learning['id'],
        'confidence': confidence_score,
        'timestamp': now(),
        'mode': mode,
    }

    if confidence_score >= 0.80:
        # PROMOTE to system invariant
        decision['action'] = 'PROMOTE'
        decision['scope'] = 'SYSTEM'
        task = create_promotion_task(learning)
        decision['task_id'] = task['id']
        log_decision('PROMOTE', learning, confidence_score, task['id'])

    elif 0.50 <= confidence_score < 0.80:
        # ACCEPT to project learnings
        decision['action'] = 'ACCEPT'
        decision['scope'] = 'PROJECT'
        save_to_project_learnings(learning)
        log_decision('ACCEPT', learning, confidence_score, None)

    else:  # < 0.50
        # REJECT (no permanent record)
        decision['action'] = 'REJECT'
        decision['scope'] = 'EPHEMERAL'
        log_decision('REJECT', learning, confidence_score, None)

    return decision
```

### 1.3 Promoted Learning → New Invariant

When a learning is promoted (confidence >= 0.80):

```
┌──────────────────────────────────────────────────────────────┐
│ PROMOTION: LEARNING BECOMES SYSTEM INVARIANT                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Assign Invariant ID: INV-L001, INV-L002, ...            │
│     └─ Format: INV-L{sequence}, to distinguish from         │
│        core invariants (1-11) and domain invariants         │
│                                                               │
│  2. Create invariant metadata:                              │
│     ├─ Rule: Operational definition (what to check)        │
│     ├─ Source: Which PRP + step + phase                    │
│     ├─ Confidence: 0.95 (from learning)                    │
│     ├─ First observed: 2026-01-23 (from learning)          │
│     ├─ Domain: consumer-product, data-architecture, etc.   │
│     ├─ Scope: Which PRP types this applies to              │
│     ├─ Validation: How to check compliance                 │
│     └─ Enforcement: What happens if violated               │
│                                                               │
│  3. Add to learned-invariants.md:                           │
│     └─ Append to invariants list                            │
│     └─ Include all metadata above                           │
│                                                               │
│  4. Create task: promote-invariant-INV-L001                │
│     └─ Type: system-improvement                             │
│     └─ Owner: claude-haiku (auto-promotion)                 │
│     └─ Blocks: nothing                                      │
│     └─ Blocked by: none                                     │
│     └─ Description: Full invariant definition               │
│     └─ Status: completed (automatically)                    │
│                                                               │
│  5. Register invariant globally:                            │
│     └─ ~/.claude/design-ops/invariants/learned-invariants.md
│     └─ Update invariants index/registry                     │
│     └─ Future /design validate commands use new invariant  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Example: Route Coverage Learning → INV-L001**

```yaml
# Learning captured during execution
learning_id: LEARN-2026-01-23-001
observation: |
  Every internal link (href) in UI components must have a corresponding
  route handler. If route doesn't exist, users see "Page not found".

# Auto-promoted to system invariant
invariant_id: INV-L001
name: Route Coverage
status: ACTIVE
created_date: 2026-01-23
source: PRP-2026-01-22-001 / Step 3 / implementation phase

rule: |
  Every internal link (href=...) in UI components must have a
  corresponding route handler that returns valid content.

confidence: 0.95
confidence_backing: |
  Observed in Dash projects (2), React Router examples (3),
  Next.js documentation. Matches SPA framework invariants.
  Tested with Playwright route coverage validation.

scope:
  applies_to: ["consumer-product", "single-page-apps"]
  phase_types: ["implementation", "validation"]
  frameworks: ["Dash", "React", "Next.js"]

validation: |
  1. Extract all href= values from component definitions
  2. Verify each has a matching route in router/callback
  3. Playwright test: click link → verify page loads (not 404)

enforcement: |
  PRPs targeting consumer-product domain must include route
  coverage test in their final validation gate. Violation:
  PRP rejected until route coverage test added.

version_history:
  - version: 1.0
    created: 2026-01-23
    source_prp: PRP-2026-01-22-001
```

---

## 2. Invariant Metadata Structure

### 2.1 Complete Invariant Schema

Every learned invariant stored in `learned-invariants.md` includes:

```yaml
INV-L001:

  # Identity
  id: INV-L001
  name: Route Coverage
  type: learned  # vs 'core' (1-11) or 'domain' (per domain file)
  status: ACTIVE  # ACTIVE, DEPRECATED, ARCHIVED

  # Source & Lineage
  source:
    origin_prp: PRP-2026-01-22-001
    origin_step: 3
    origin_phase: implementation
    discovered_date: 2026-01-23T14:22:15Z
    discovered_by: claude-haiku-4-5

  # Confidence
  confidence:
    score: 0.95  # 0.0-1.0
    backing: |
      - Observed in 2 Dash projects
      - Matches React Router + Next.js patterns
      - Playwright test validation
    calibrated: false  # Has this score been validated against PRPs?

  # Applicability
  scope:
    applies_to_domains:
      - consumer-product
      - single-page-apps  # Tag for cross-domain search
    applies_to_phases:
      - implementation
      - validation
    applies_to_frameworks:
      - Dash
      - React Router
      - Next.js
    explicitly_excludes:  # Edge cases where NOT applicable
      - static-site-generators
      - server-side-rendering-only

  # Operational Definition
  rule: |
    Every internal link (href=...) in UI components must have a
    corresponding route handler. Routes must return valid content.

  examples:
    violation:
      - href: /account/details
        issue: No route handler for /account/{id}
        consequence: Users see "Page not found"

    correct:
      - href: /account/details
        handler: dcc.Link(href="/account/..." target="/account/{id}")
        validation: click_test("finds element", "verifies page load")

  # Validation Strategy
  validation:
    method: |
      1. Extract all href= from component definitions
      2. Verify matching route in router/callback
      3. Playwright click test + page load verification
    acceptance_criteria:
      - All internal hrefs have routes
      - Playwright click test succeeds
      - No 404 or "Page not found" in response

  # Enforcement in Design System
  enforcement:
    applies_at: design-time  # When validating PRPs
    layer: validator  # Which layer detects violation
    consequence: |
      PRPs targeting consumer-product + implementation phase
      must include route coverage test. Violation: PRP
      rejected until test added.
    override_allowed: false  # Can't override in dangerous mode

  # Evolution Tracking
  versions:
    - version: 1.0
      created: 2026-01-23
      confidence: 0.95
      source_prp: PRP-2026-01-22-001
      changes: Initial capture
      status: active

    - version: 1.1
      created: 2026-01-26
      confidence: 0.98  # Increased after validation
      source_prp: PRP-2026-01-25-002
      changes: |
        Confidence increased: validated in 2 additional projects.
        Added explicit exclude: server-side-rendering-only.
      status: active
```

### 2.2 File Organization: learned-invariants.md

```markdown
# Learned Invariants

Automatically captured learnings from PRP executions, promoted from
project-local to system-wide scope when confidence >= 0.80.

Last updated: 2026-01-26
Total invariants: 12 (active), 2 (deprecated)

---

## Index

### By PRP Source
- PRP-2026-01-22-001: INV-L001, INV-L002
- PRP-2026-01-25-002: INV-L003, INV-L004
- PRP-2026-01-26-001: INV-L005

### By Domain
- consumer-product: INV-L001, INV-L003, INV-L005
- data-architecture: INV-L002, INV-L004
- integration: INV-L006

### By Confidence
- 0.95+: INV-L001, INV-L002, INV-L003
- 0.80-0.94: INV-L004, INV-L005, INV-L006
- 0.50-0.79: (ACCEPTED, not promoted)

---

## Active Invariants

### INV-L001: Route Coverage

**Source:** PRP-2026-01-22-001 / Step 3 / implementation
**Date:** 2026-01-23
**Confidence:** 0.95

**Rule:** Every internal link (href) in UI components must have
a corresponding route handler.

[Full definition from schema above]

---

### INV-L002: Filter Logic Must Handle Edge Cases

**Source:** PRP-2026-01-22-001 / Step 5 / implementation
**Date:** 2026-01-23
**Confidence:** 0.92

**Rule:** Date/time filters must explicitly handle negative values
and lifecycle states.

[Full definition]

---

## Deprecated Invariants

### INV-L010: DEPRECATED

**Source:** PRP-2026-01-15-001
**Status:** Deprecated 2026-01-25
**Reason:** Violated by PRP-2026-01-25-002; insufficient backing

[Deprecation history]

---

## Confidence Calibration Report

### Recent Calibration (2026-01-26)

After executing PRP-2026-01-25-002:
- INV-L001: Predicted 0.95, Actual 0.98 (+0.03)
- INV-L002: Predicted 0.92, Actual 0.91 (-0.01)
- INV-L003: Predicted 0.88, Actual 0.85 (-0.03)

**Calibration status:** Good. Predictions within ±0.05.
```

---

## 3. Future PRP Validation Loop

### 3.1 PRP Creation References Existing Invariants

When you create PRP-2 (after PRP-1 execution):

```
┌──────────────────────────────────────────────────────────────┐
│ PRP-2 CREATION WITH INVARIANT CONSTRAINTS                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Spec written for PRP-2                                  │
│                                                               │
│  2. /design validate PRP-2 spec                             │
│     ├─ Load core invariants (1-11)                          │
│     ├─ Load domain invariants (if specified)                │
│     ├─ Load learned invariants (INV-L001-L012 from PRP-1)  │
│     └─ Validate PRP-2 spec against ALL                      │
│                                                               │
│  3. Validation output:                                      │
│     ├─ "PRP-2 validates successfully"                       │
│     ├─ "Satisfies INV-L001 (route coverage): Yes"          │
│     ├─ "Satisfies INV-L002 (filter edge cases): Yes"       │
│     └─ "2 new invariants may be learned: INV-L013, L014"   │
│                                                               │
│  4. /design prp creates PRP-2                               │
│     ├─ References learned invariants in Meta section        │
│     ├─ Includes validation checksums                        │
│     └─ Documents which learned invariants constrain it      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Example: PRP-2 Meta Section Showing Invariant References**

```yaml
# PRP-2026-01-25-002
meta:
  prp_id: PRP-2026-01-25-002
  date: 2026-01-25
  domain: consumer-product

  validated_against_invariants:
    - invariant_id: INV-1 (Ambiguity is Invalid)
      status: PASS
      detail: "All steps have clear acceptance criteria"

    - invariant_id: INV-L001 (Route Coverage)
      status: PASS
      detail: "PRP includes route coverage test in gate 3"

    - invariant_id: INV-L002 (Filter Logic Edge Cases)
      status: PASS
      detail: "Filter step includes negative days test"

  inherited_constraints:
    - INV-L001: Must include route verification test
    - INV-L002: Must test filters with past dates + terminal states

  new_invariants_predicted: 2
  estimated_confidence:
    - INV-L013: 0.87 (new pattern discovered)
    - INV-L014: 0.91 (strong confidence)
```

### 3.2 /design validate Against Learned Invariants

Command: `/design validate specs/my-feature.md --include-learned`

```
┌──────────────────────────────────────────────────────────────┐
│ VALIDATION AGAINST LEARNED + CORE INVARIANTS                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ UNIVERSAL INVARIANTS (1-11):                                │
│   [1] Ambiguity is Invalid...................... PASS      │
│   [2] State Must Be Explicit.................... PASS      │
│   ...                                                        │
│   [10] Degradation Path Must Exist.............. PASS      │
│                                                               │
│ DOMAIN INVARIANTS (consumer-product):                        │
│   [D-1] UI Components Have Accessibility....... PASS      │
│   [D-2] Touch Targets >= 44px................... PASS      │
│                                                               │
│ LEARNED INVARIANTS (from PRP-1):                            │
│   [INV-L001] Route Coverage..................... PASS      │
│              └─ All 4 routes verified                      │
│              └─ Playwright tests included                  │
│                                                               │
│   [INV-L002] Filter Logic Edge Cases........... PASS      │
│              └─ Negative dates tested                      │
│              └─ Terminal states excluded                   │
│                                                               │
│ OVERALL: PASS                                               │
│ Spec ready for PRP compilation                            │
│ Learnings from PRP-1 successfully constrain PRP-2         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 /design stress-test Against Learned Invariants

Command: `/design stress-test prp-2026-01-25-002.yaml --learned`

Tests future PRPs against learned invariants:

```
Stress Testing PRP-2026-01-25-002 against Learned Invariants:

[INV-L001] Route Coverage
  Test: All internal hrefs have route handlers?
  Step 2: "Implement dashboard" references /users/{id}
  → FAIL: No route handler defined
  → IMPACT: Users will see 404

  FIX: Add route handler step OR remove /users/{id} reference

[INV-L002] Filter Logic Edge Cases
  Test: Date filters handle negative days?
  Step 4: "Filter by due date" - interval = days_until_close <= 14
  → FAIL: No validation for negative days

  FIX: Add explicit test for negative days in validation gate

[INV-L003] Lifecycle State Handling
  Test: Filters explicitly exclude terminal states?
  Step 4: Filter by stage, includes 'closed'
  → FAIL: 'closed' is terminal state, should be excluded

  FIX: Update filter to exclude TERMINAL_STATES

Stress test results: 0 PASS, 3 FAIL
PRP not ready for execution in dangerous mode.
Add fixes and re-validate.
```

---

## 4. Feedback Loop Visualization

### 4.1 Three-PRP Cycle: Learning → Invariant → Constraint

```
┌─────────────────────────────────────────────────────────────────┐
│                     CYCLE 1: PRP-1                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Spec: "Build forecast dashboard"                              │
│    ↓                                                             │
│  /design validate → PASS (no learned invariants yet)            │
│    ↓                                                             │
│  /design prp → Generate PRP-001                                 │
│    ↓                                                             │
│  /design run --dangerous PRP-001                                │
│    ├─ Step 1: Design data model        [Complete]              │
│    ├─ Step 2: Implement API            [Complete]              │
│    ├─ Step 3: Build UI routes          [Complete]              │
│    │  └─ Learning LEARN-001: Routes must have handlers        │
│    │     Confidence: 0.95               [AUTO-PROMOTE]         │
│    │     └─ Create INV-L001 task                              │
│    │     └─ Recorded to learned-invariants.md                 │
│    ├─ Step 4: Add filtering            [Complete]              │
│    │  └─ Learning LEARN-002: Filters must handle edge cases   │
│    │     Confidence: 0.92               [AUTO-PROMOTE]         │
│    │     └─ Create INV-L002 task                              │
│    ├─ Step 5: Test and validate        [Complete]              │
│    └─ Retrospective: Document learnings                        │
│                                                                   │
│  Learned Invariants Created: INV-L001, INV-L002                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
                      [Invariants Recorded]
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     CYCLE 2: PRP-2                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Spec: "Add account search feature"                            │
│    ↓                                                             │
│  /design validate specs/search.md --include-learned             │
│    ├─ Core invariants: [1-11] → PASS                            │
│    ├─ Domain invariants: [consumer-product] → PASS              │
│    ├─ Learned invariants: [INV-L001, L002] → PASS              │
│    │  └─ Step 2 includes route coverage test (L001)            │
│    │  └─ Step 3 filters handle edge cases (L002)               │
│    └─ Overall: PASS (spec respects learned constraints)         │
│    ↓                                                             │
│  /design prp specs/search.md → Generate PRP-002                │
│    Meta section documents:                                      │
│    └─ Validates against INV-L001, INV-L002                      │
│    └─ Routes implemented with test (L001)                       │
│    └─ Filter has edge case validation (L002)                    │
│    ↓                                                             │
│  /design run --dangerous PRP-002                                │
│    ├─ Step 1: Design search schema       [Complete]             │
│    ├─ Step 2: Implement search API      [Complete]             │
│    ├─ Step 3: Add search UI routes      [Complete]             │
│    │  └─ Route coverage test passes (respects INV-L001)        │
│    ├─ Step 4: Add filter controls       [Complete]             │
│    │  └─ Edge case tests pass (respects INV-L002)              │
│    ├─ Step 5: Testing                   [Complete]              │
│    │  └─ Learning LEARN-003: Cache invalidation requires...    │
│    │     Confidence: 0.87               [AUTO-PROMOTE]         │
│    │     └─ Create INV-L003 task                              │
│    │  └─ Learning LEARN-004: Search with large datasets...    │
│    │     Confidence: 0.91               [AUTO-PROMOTE]         │
│    │     └─ Create INV-L004 task                              │
│    └─ Retrospective: Learned invariants worked! Added 2 more   │
│                                                                   │
│  Learned Invariants Created: INV-L003, INV-L004                │
│  Total in System: INV-L001 through INV-L004                    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
                  [Invariants + Confidence Scores]
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     CYCLE 3: PRP-3                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Spec: "Build admin dashboard"                                 │
│    ↓                                                             │
│  /design validate specs/admin.md --include-learned              │
│    ├─ Core + Domain: PASS                                       │
│    ├─ Learned invariants: [INV-L001, L002, L003, L004]        │
│    │  ├─ L001 (Routes): Admin must have route tests ✓         │
│    │  ├─ L002 (Filters): Admin filters test edge cases ✓       │
│    │  ├─ L003 (Cache): Admin updates invalidate cache ✓        │
│    │  └─ L004 (Search): Pagination handles large sets ✓        │
│    └─ Overall: PASS                                             │
│    ↓                                                             │
│  /design prp specs/admin.md → Generate PRP-003                 │
│    Meta references all 4 learned invariants                     │
│    └─ PRP-003 inherits constraints from PRP-1 & PRP-2          │
│    ↓                                                             │
│  /design run --dangerous PRP-003                                │
│    ├─ All steps execute respecting INV-L001 through L004       │
│    ├─ Route test passes (respects L001)                        │
│    ├─ Filter tests pass (respects L002)                        │
│    ├─ Cache invalidation included (respects L003)              │
│    ├─ Pagination works (respects L004)                         │
│    └─ Step 6: Admin-specific features                           │
│       └─ Learning LEARN-005: Admin workflows differ from...    │
│          Confidence: 0.85               [AUTO-PROMOTE]         │
│          └─ Create INV-L005 task                              │
│       └─ Learning LEARN-006: Audit logging must track...       │
│          Confidence: 0.93               [AUTO-PROMOTE]         │
│          └─ Create INV-L006 task                              │
│                                                                   │
│  Learned Invariants Created: INV-L005, INV-L006                │
│  Total System Knowledge: INV-L001 through INV-L006              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

SUMMARY:
  PRP-1: 0 constraints → 2 learnings (INV-L001, L002)
  PRP-2: 2 constraints → 2 learnings (INV-L003, L004)
  PRP-3: 4 constraints → 2 learnings (INV-L005, L006)

  Each cycle learns WHILE respecting prior learnings.
  System grows smarter with each execution.
```

### 4.2 Task Dependencies Across Cycles

```
PRP-1 Execution Tasks:
  ├─ prp-001-step-1 (design model)
  ├─ prp-001-step-2 (implement API)
  ├─ prp-001-step-3 (build routes)
  │  └─ generate-learning-LEARN-001
  │     └─ promote-invariant-INV-L001  [dependency]
  ├─ prp-001-step-4 (add filters)
  │  └─ generate-learning-LEARN-002
  │     └─ promote-invariant-INV-L002  [dependency]
  ├─ prp-001-step-5 (test)
  └─ prp-001-retrospective

PRP-2 Execution Tasks (Blocked by PRP-1 learnings):
  ├─ [WAIT] validate-prp-002-against-learned-invariants
  │         └─ blocks: prp-002-generation
  │         └─ blocked-by: promote-invariant-INV-L001, INV-L002
  │
  ├─ prp-002-generation
  │  └─ depends: validate-prp-002-against-learned-invariants
  │
  ├─ prp-002-step-1 (design schema)
  ├─ prp-002-step-2 (implement API)
  │  └─ respects-INV-L001 (route tests)
  ├─ prp-002-step-3 (add UI)
  │  └─ generate-learning-LEARN-003
  │     └─ promote-invariant-INV-L003  [dependency]
  └─ ...

PRP-3 Execution Tasks (Blocked by PRP-1 & PRP-2 learnings):
  ├─ [WAIT] validate-prp-003-against-learned-invariants
  │         └─ blocks: prp-003-generation
  │         └─ blocked-by: INV-L001, L002, L003, L004
  │
  ├─ prp-003-generation
  ├─ prp-003-step-1 through step-6
  │  └─ all steps validate against 4 learned invariants
  └─ ...
```

---

## 5. Cross-PRP Invariant Evolution

### 5.1 Tracking Invariant Changes Across Projects

**Invariant Version History Example:**

```yaml
INV-L001: Route Coverage

version_history:

  - version: 1.0
    created: 2026-01-23T14:22:15Z
    source_prp: PRP-2026-01-22-001
    source_step: 3
    confidence: 0.95
    status: ACTIVE

    rule: |
      Every internal link (href) in UI components must have a
      corresponding route handler.

    validation: |
      1. Extract all href from component definitions
      2. Verify route handler exists
      3. Playwright test: click link → verify page loads

    changelog: "Initial capture from Dash project"

    events:
      - date: 2026-01-23
        event: Created
        detail: "Learned from PRP-001 step 3"

      - date: 2026-01-25
        event: Validated
        detail: "PRP-002 respects constraint, +1 confirmation"

      - date: 2026-01-26
        event: Validated
        detail: "PRP-003 respects constraint, +1 confirmation"

    validation_count: 3  # How many PRPs successfully used it
    violation_count: 0   # How many PRPs violated it

  - version: 1.1
    created: 2026-01-26T09:15:00Z
    source_prp: PRP-2026-01-25-002
    confidence: 0.98  # Increased from 0.95
    status: ACTIVE

    changes_from_v1_0: |
      - Confidence increased from 0.95 to 0.98 (validated by 2 more PRPs)
      - Added explicit domain scoping (SPA only)
      - Added exclusion: "not applicable to server-side-rendered apps"

    rule: |
      [Same as v1.0, but with domain scoping clarified]

    scope:
      applies_to_domains: ["consumer-product", "single-page-apps"]
      applies_to_frameworks: ["Dash", "React Router", "Next.js"]
      explicitly_excludes: ["server-side-rendering-only", "static-sites"]

    changelog: |
      Refined scope after observing that SSR apps don't need this
      invariant (routes are server-resolved). Confidence increased
      due to successful validation in 2 additional projects.

    events:
      - date: 2026-01-23
        event: Created
        detail: "From PRP-001"
      - date: 2026-01-25
        event: Validated
        detail: "PRP-002 respects, +1"
      - date: 2026-01-26
        event: Validated + Refined
        detail: "PRP-003 respects, confidence ↑ 0.98, scope refined"

    validation_count: 3
    violation_count: 0
```

### 5.2 Invariant Deprecation Path

When a learned invariant is violated or outgrown:

```yaml
INV-L007: DEPRECATED (Example)

version_history:

  - version: 1.0
    created: 2026-01-20
    confidence: 0.88
    status: ACTIVE

  - version: DEPRECATED
    deprecated_date: 2026-01-27
    deprecated_reason: |
      PRP-2026-01-27-001 discovered that this invariant doesn't apply
      to async operations. Rule was too broad. Instead of fixing,
      recommending removal in favor of more specific INV-L008.

    deprecation_events:
      - date: 2026-01-27
        event: Violation detected
        source_prp: PRP-2026-01-27-001
        detail: "Invariant doesn't apply to async code paths"

      - date: 2026-01-27
        event: Confidence lowered
        from: 0.88
        to: 0.45  # Below threshold, deprecated

      - date: 2026-01-27
        event: Marked deprecated
        replacement: "Use INV-L008 (more specific async version)"

    status: DEPRECATED
    successor: INV-L008

    note: |
      This invariant will be removed from system validation after
      all existing PRPs have been reviewed and migrated to INV-L008.
```

---

## 6. Real Example: 3 PRPs, 8 Invariants

### 6.1 PRP-001 Execution & Learning

**Project:** SA Intelligence Dashboard v1.0

```yaml
PRP-2026-01-22-001:
  name: "Build forecast dashboard"
  domain: consumer-product

  execution_timeline:

    Step 1: Design data model
      duration: 2 hours
      status: COMPLETED
      learnings: None

    Step 2: Implement API endpoints
      duration: 3 hours
      status: COMPLETED
      learnings: None

    Step 3: Build UI routes
      duration: 3 hours
      status: COMPLETED
      learning_1:
        id: LEARN-2026-01-23-001
        title: "Internal links must have route handlers"
        observation: |
          When building Dash SPA, each href in Link components
          requires a matching route callback. If missing, user
          sees "Page not found" instead of target page.
        confidence: 0.95
        decision: PROMOTE → INV-L001

    Step 4: Add filtering
      duration: 2 hours
      status: COMPLETED
      learning_2:
        id: LEARN-2026-01-23-002
        title: "Filters must handle negative dates and terminal states"
        observation: |
          Date filters like "days_until_close <= 14" include
          negative values (past dates). Lifecycle filters must
          explicitly exclude terminal states (closed, live, etc).
        confidence: 0.92
        decision: PROMOTE → INV-L002

    Step 5: Test and validate
      duration: 4 hours
      status: COMPLETED
      learnings: None

INVARIANTS CREATED:
  → INV-L001: Route Coverage (confidence: 0.95)
  → INV-L002: Filter Logic Edge Cases (confidence: 0.92)
```

### 6.2 PRP-002 Execution & Learning (Constrained by PRP-001)

**Project:** Search Features v1.0

```yaml
PRP-2026-01-25-002:
  name: "Add account search"
  domain: consumer-product

  validation_against_learned_invariants:
    - INV-L001: Route Coverage
      status: PASS
      detail: |
        Step 2 includes route handler for /search/{query}.
        Step 3 includes Playwright test to verify route.

    - INV-L002: Filter Logic Edge Cases
      status: PASS
      detail: |
        Step 4 filter has explicit test for:
        - Negative days (past dates)
        - Terminal states (closed items)

  execution_timeline:

    Step 1: Design search schema
      duration: 1 hour
      status: COMPLETED
      learnings: None

    Step 2: Implement search API
      duration: 3 hours
      status: COMPLETED
      learning_3:
        id: LEARN-2026-01-25-003
        title: "Search with large result sets needs pagination"
        observation: |
          Search on 100K+ records needs pagination or users
          experience slow queries. Pagination must be eager
          (loaded before rendering) for good UX.
        confidence: 0.91
        decision: PROMOTE → INV-L003

    Step 3: Add search UI
      duration: 2 hours
      status: COMPLETED
      validation_check:
        - INV-L001: Routes tested ✓
        - INV-L002: Filters edge-case tested ✓

    Step 4: Add filter/sort controls
      duration: 2 hours
      status: COMPLETED
      learning_4:
        id: LEARN-2026-01-25-004
        title: "Cache invalidation on data updates"
        observation: |
          Search results cached for performance. When data
          updates (user created, status changed), cache must
          be invalidated. Without this, users see stale results.
        confidence: 0.87
        decision: PROMOTE → INV-L004

    Step 5: End-to-end testing
      duration: 3 hours
      status: COMPLETED
      learnings: None

INVARIANTS CREATED:
  → INV-L003: Large Result Set Pagination (confidence: 0.91)
  → INV-L004: Cache Invalidation on Update (confidence: 0.87)

TOTAL SYSTEM INVARIANTS: 4 (INV-L001 through INV-L004)
```

### 6.3 PRP-003 Execution & Learning (Constrained by PRP-001 & PRP-002)

**Project:** Admin Dashboard v1.0

```yaml
PRP-2026-01-26-001:
  name: "Build admin dashboard"
  domain: consumer-product

  validation_against_learned_invariants:
    - INV-L001: Route Coverage
      status: PASS
      detail: "Routes for admin/{section} all tested"

    - INV-L002: Filter Logic Edge Cases
      status: PASS
      detail: "Admin filters exclude closed items"

    - INV-L003: Pagination
      status: PASS
      detail: "User list paginated, 1000+ users supported"

    - INV-L004: Cache Invalidation
      status: PASS
      detail: "Admin actions (ban, promote) invalidate caches"

  execution_timeline:

    Step 1: Design admin data model
      duration: 1.5 hours
      status: COMPLETED
      learnings: None

    Step 2: Implement admin APIs
      duration: 3 hours
      status: COMPLETED
      validation_check:
        - INV-L001: Route tests ✓
        - INV-L004: Cache invalidation ✓

    Step 3: Build admin UI
      duration: 2.5 hours
      status: COMPLETED
      learning_5:
        id: LEARN-2026-01-26-005
        title: "Admin UIs need role-based access control"
        observation: |
          Admin dashboard must check user.role before rendering
          sections. Users without admin role should not see
          admin links. This is different from data filters.
        confidence: 0.88
        decision: PROMOTE → INV-L005

    Step 4: Add admin filters/controls
      duration: 2 hours
      status: COMPLETED
      validation_check:
        - INV-L002: Filter edge cases ✓
        - INV-L003: Pagination ✓

    Step 5: Add audit logging
      duration: 3 hours
      status: COMPLETED
      learning_6:
        id: LEARN-2026-01-26-006
        title: "Audit logging must capture user + action + timestamp"
        observation: |
          Admin actions (delete user, change settings) must log:
          who did it (user_id), what they did (action), when
          (timestamp), and what changed (before/after state).
          This is regulatory requirement for HLS apps.
        confidence: 0.93
        decision: PROMOTE → INV-L006

    Step 6: Testing and validation
      duration: 4 hours
      status: COMPLETED
      validation_check:
        - INV-L001: Routes ✓
        - INV-L002: Filters ✓
        - INV-L003: Pagination ✓
        - INV-L004: Cache ✓
        - INV-L005: RBAC ✓ (newly created)
        - INV-L006: Audit ✓ (newly created)

INVARIANTS CREATED:
  → INV-L005: Role-Based Access Control (confidence: 0.88)
  → INV-L006: Audit Logging Structure (confidence: 0.93)

TOTAL SYSTEM INVARIANTS: 6 (INV-L001 through INV-L006)
```

---

## 7. Dangerous Mode Auto-Promotion Decision Logic

### 7.1 Decision Algorithm

```python
def auto_promote_learning(
    learning: dict,
    confidence_score: float,
    mode: str = 'dangerous',
    override_promote: bool = False
) -> dict:
    """
    Dangerous mode auto-promotion decision logic.

    Args:
        learning: Captured learning dict with observation, context
        confidence_score: 0.0-1.0 (output from confidence calculator)
        mode: 'dangerous' or 'safe'
        override_promote: Human force-promote even if low confidence

    Returns:
        Decision dict with action, invariant_id, task_id
    """

    decision = {
        'learning_id': learning['id'],
        'timestamp': now(),
        'confidence': confidence_score,
        'mode': mode,
    }

    # Check override first
    if override_promote:
        decision['action'] = 'PROMOTE_OVERRIDE'
        decision['scope'] = 'SYSTEM'
        decision['reason'] = 'Human override'
        task = create_task(
            id=f"promote-invariant-{generate_invariant_id()}",
            type='system-improvement',
            description='Human-promoted learning'
        )
        decision['task_id'] = task['id']
        save_to_learned_invariants(learning)
        log_promotion(learning, 'OVERRIDE', decision)
        return decision

    # Dangerous mode >= 0.80: PROMOTE
    if mode == 'dangerous' and confidence_score >= 0.80:
        decision['action'] = 'PROMOTE'
        decision['scope'] = 'SYSTEM'
        decision['reason'] = f'Dangerous mode + confidence {confidence_score:.2f}'

        # Create new invariant
        inv_id = generate_invariant_id()
        invariant = learning_to_invariant(learning, inv_id, confidence_score)

        # Create promotion task
        task = create_task(
            id=f'promote-invariant-{inv_id}',
            type='system-improvement',
            owner='claude-haiku',  # Auto-promotion
            description=f'Auto-promote learning {learning["id"]} to {inv_id}',
            blocks=[],  # Doesn't block execution
            blockedBy=[]
        )

        # Save globally
        save_to_learned_invariants(invariant)
        register_invariant_id(inv_id)

        # Mark task completed
        task['status'] = 'completed'

        decision['task_id'] = task['id']
        decision['invariant_id'] = inv_id
        decision['metadata'] = {
            'source_prp': learning['source_prp'],
            'source_step': learning['source_step'],
            'applies_to': learning.get('applies_to', []),
        }

        log_promotion(learning, 'PROMOTE', decision)
        return decision

    # Dangerous mode 0.50-0.79: ACCEPT (project-local)
    elif 0.50 <= confidence_score < 0.80:
        decision['action'] = 'ACCEPT'
        decision['scope'] = 'PROJECT'
        decision['reason'] = f'Moderate confidence {confidence_score:.2f}'

        # Save to project learnings (not system-wide)
        save_to_project_learnings(learning)

        decision['file'] = 'project-learnings.md'
        log_promotion(learning, 'ACCEPT', decision)
        return decision

    # All modes < 0.50: REJECT
    else:
        decision['action'] = 'REJECT'
        decision['scope'] = 'EPHEMERAL'
        decision['reason'] = f'Low confidence {confidence_score:.2f} (< 0.50)'

        # No permanent record
        log_promotion(learning, 'REJECT', decision)
        return decision


def learning_to_invariant(
    learning: dict,
    invariant_id: str,
    confidence: float
) -> dict:
    """Convert learning to system invariant with full metadata."""

    return {
        'id': invariant_id,
        'name': learning.get('title', 'Unnamed'),
        'type': 'learned',
        'status': 'ACTIVE',

        'source': {
            'origin_prp': learning['source_prp'],
            'origin_step': learning['source_step'],
            'origin_phase': learning['source_phase'],
            'discovered_date': now(),
            'discovered_by': 'claude-haiku'
        },

        'confidence': {
            'score': confidence,
            'backing': learning.get('confidence_reasoning', ''),
            'calibrated': False
        },

        'scope': {
            'applies_to_domains': learning.get('applies_to', []),
            'applies_to_phases': [learning.get('source_phase', 'implementation')],
            'applies_to_frameworks': learning.get('applies_to_frameworks', []),
            'explicitly_excludes': learning.get('excludes', [])
        },

        'rule': learning['observation'],

        'examples': {
            'violation': learning.get('violation_example'),
            'correct': learning.get('correct_example')
        },

        'validation': {
            'method': learning.get('validation_method', ''),
            'acceptance_criteria': learning.get('acceptance_criteria', [])
        },

        'enforcement': {
            'applies_at': 'design-time',
            'layer': 'validator',
            'consequence': f'PRPs targeting {learning["applies_to"][0]} must '
                          f'include test for {invariant_id}',
            'override_allowed': False
        },

        'versions': [
            {
                'version': '1.0',
                'created': now(),
                'confidence': confidence,
                'source_prp': learning['source_prp'],
                'changes': 'Initial capture',
                'status': 'active'
            }
        ]
    }
```

### 7.2 Decision Logging

Every decision is logged for auditability:

```yaml
promotion_log:

  LEARN-2026-01-23-001:
    decision: PROMOTE
    confidence: 0.95
    timestamp: 2026-01-23T14:22:30Z
    mode: dangerous
    action: Created INV-L001
    task_id: promote-invariant-INV-L001
    justified: true
    log: |
      Learning LEARN-001 (routes) scored 0.95 confidence.
      Dangerous mode >= 0.80 threshold. PROMOTED to system invariant.
      Task promote-invariant-INV-L001 created and completed.

  LEARN-2026-01-23-002:
    decision: PROMOTE
    confidence: 0.92
    timestamp: 2026-01-23T16:45:00Z
    mode: dangerous
    action: Created INV-L002
    task_id: promote-invariant-INV-L002
    justified: true
    log: |
      Learning LEARN-002 (filters) scored 0.92 confidence.
      Dangerous mode >= 0.80 threshold. PROMOTED to system invariant.

  LEARN-2026-01-25-005:
    decision: ACCEPT
    confidence: 0.62
    timestamp: 2026-01-25T12:10:00Z
    mode: dangerous
    action: Saved to project-learnings.md
    justified: true
    log: |
      Learning LEARN-005 (caching strategy) scored 0.62 confidence.
      Below 0.80 threshold. ACCEPTED to project-local scope only.
      Not system-wide (needs more validation).

  LEARN-2026-01-20-099:
    decision: REJECT
    confidence: 0.38
    timestamp: 2026-01-20T09:00:00Z
    mode: dangerous
    action: Discarded
    justified: true
    log: |
      Learning LEARN-099 scored 0.38 confidence. Below 0.50 threshold.
      REJECTED (no permanent record). Can be re-observed if pattern repeats.
```

---

## 8. Invariant Promotion Task Structure

### 8.1 Task Created During Promotion

When a learning is promoted (confidence >= 0.80):

```json
{
  "task_id": "promote-invariant-INV-L001",
  "type": "system-improvement",
  "parent_prp": "PRP-2026-01-22-001",
  "parent_step": 3,

  "title": "Promote Learning: Route Coverage → INV-L001",
  "description": "Learning LEARN-2026-01-23-001 auto-promoted from PRP-001 Step 3. Rule: Every internal link (href) in UI components must have a corresponding route handler. Confidence: 0.95",

  "meta": {
    "learning_source": "LEARN-2026-01-23-001",
    "invariant_id": "INV-L001",
    "invariant_name": "Route Coverage",
    "confidence": 0.95,
    "promotion_mode": "dangerous",
    "promotion_timestamp": "2026-01-23T14:22:30Z"
  },

  "status": "completed",  # Auto-promotion completes immediately
  "owner": "claude-haiku-4-5",  # Automated
  "created_at": "2026-01-23T14:22:31Z",

  "blocks": [],  # Doesn't block other execution
  "blockedBy": [],  # Doesn't wait on anything

  "effects": {
    "file_updated": "~/.claude/design-ops/invariants/learned-invariants.md",
    "invariant_registered": "INV-L001",
    "future_impact": "All future /design validate commands will check against this invariant"
  },

  "audit_trail": [
    {
      "timestamp": "2026-01-23T14:22:30Z",
      "event": "Learning captured",
      "detail": "LEARN-2026-01-23-001 scored 0.95 confidence"
    },
    {
      "timestamp": "2026-01-23T14:22:31Z",
      "event": "Auto-promotion triggered",
      "detail": "Dangerous mode + confidence >= 0.80"
    },
    {
      "timestamp": "2026-01-23T14:22:32Z",
      "event": "Invariant created",
      "detail": "INV-L001 registered in learned-invariants.md"
    },
    {
      "timestamp": "2026-01-23T14:22:33Z",
      "event": "Task marked complete",
      "detail": "Promotion pipeline finished"
    }
  ]
}
```

### 8.2 Task List for Full Cycle

```
PROJECT: PRP-001 Execution + Learning Pipeline

Tasks (by PRP/Phase):

┌─ PRP-001 EXECUTION TASKS
│
├─ prp-001-step-1
│  id: task-001
│  title: "Design data model"
│  status: completed
│  blocks: [prp-001-step-2]
│
├─ prp-001-step-2
│  id: task-002
│  title: "Implement API endpoints"
│  status: completed
│  blocks: [prp-001-step-3, prp-001-step-4]
│  blockedBy: [task-001]
│
├─ prp-001-step-3
│  id: task-003
│  title: "Build UI routes"
│  status: completed
│  blocks: [prp-001-step-5, generate-learning-LEARN-001]
│  blockedBy: [task-002]
│
├─ generate-learning-LEARN-001
│  id: task-003-learn
│  title: "Extract learning: Routes need handlers"
│  status: completed
│  blocks: [promote-invariant-INV-L001]
│  confidence_score: 0.95
│
├─ promote-invariant-INV-L001
│  id: task-003-promote
│  title: "Promote LEARN-001 → INV-L001"
│  type: system-improvement
│  status: completed  # Auto-completed
│  owner: claude-haiku
│  blocks: []  # Doesn't block
│  blockedBy: [task-003-learn]
│  effects: [updated learned-invariants.md, registered INV-L001]
│
├─ prp-001-step-4
│  id: task-004
│  title: "Add filtering"
│  status: completed
│  blocks: [prp-001-step-5, generate-learning-LEARN-002]
│  blockedBy: [task-002]
│
├─ generate-learning-LEARN-002
│  id: task-004-learn
│  title: "Extract learning: Filters need edge case handling"
│  status: completed
│  blocks: [promote-invariant-INV-L002]
│  confidence_score: 0.92
│
├─ promote-invariant-INV-L002
│  id: task-004-promote
│  title: "Promote LEARN-002 → INV-L002"
│  type: system-improvement
│  status: completed  # Auto-completed
│  owner: claude-haiku
│  blocks: []
│  blockedBy: [task-004-learn]
│  effects: [updated learned-invariants.md, registered INV-L002]
│
├─ prp-001-step-5
│  id: task-005
│  title: "Test and validate"
│  status: completed
│  blocks: [prp-001-retrospective]
│  blockedBy: [task-003, task-004]
│
└─ prp-001-retrospective
   id: task-006
   title: "Document learnings and system improvements"
   status: completed
   blockedBy: [promote-invariant-INV-L001, promote-invariant-INV-L002]
   output: RETRO-2026-01-23-PRP-001.md

┌─ PRP-002 VALIDATION & EXECUTION (Depends on PRP-001 learnings)
│
├─ validate-prp-002-against-learned-invariants
│  id: task-100
│  title: "Validate PRP-002 spec against INV-L001, INV-L002"
│  status: completed
│  blocks: [prp-002-generation]
│  blockedBy: [promote-invariant-INV-L001, promote-invariant-INV-L002]
│  result: PASS (PRP-002 respects learned invariants)
│
├─ prp-002-generation
│  id: task-101
│  title: "Generate PRP-002 from validated spec"
│  status: completed
│  blocks: [prp-002-step-1]
│  blockedBy: [task-100]
│
├─ prp-002-step-1
│  ...
│
└─ [Additional steps and promotion tasks for PRP-002]
```

---

## 9. /design Commands Interaction with Promotion System

### 9.1 Command Workflow

**Creating and Running a Dangerous Mode PRP:**

```bash
# Step 1: Write spec
$ cat > specs/dashboard.md << 'EOF'
# Dashboard Spec
...
EOF

# Step 2: Validate against core + learned invariants
$ /design validate specs/dashboard.md --include-learned

# Output:
# Checking Universal Invariants (1-11)... PASS
# Checking Learned Invariants (INV-L001-L006)... PASS
# Ready for PRP compilation

# Step 3: Generate PRP
$ /design prp specs/dashboard.md

# Output: PRP-2026-01-26-001.yaml
# Meta section documents:
#   - Validates against core invariants [1-11]
#   - Validates against learned invariants [INV-L001-L006]
#   - Inherits constraints from all 6 learned invariants

# Step 4: Run in dangerous mode
$ /design run --dangerous PRP-2026-01-26-001.yaml

# Output during execution:
# Step 1: Design model [COMPLETE]
# Step 2: Implement API [COMPLETE]
#   Learning LEARN-007 captured (confidence: 0.78)
#   → ACCEPT (project-local, < 0.80)
# Step 3: Build UI [COMPLETE]
#   Learning LEARN-008 captured (confidence: 0.89)
#   → PROMOTE to INV-L007 ✓
#   → Task promote-invariant-INV-L007 created
# Step 4: Testing [COMPLETE]
#   Learning LEARN-009 captured (confidence: 0.91)
#   → PROMOTE to INV-L008 ✓
# ...
# Execution complete
# Learned 2 system invariants: INV-L007, INV-L008

# Step 5: Retrospective
$ /design retrospective PRP-2026-01-26-001

# Captures:
#   - What worked (pattern matches)
#   - What didn't work
#   - New invariants INV-L007, INV-L008
#   - Confidence calibration (predicted vs actual)
```

### 9.2 Stress Testing Against Learned Invariants

```bash
# Test future PRP against learned invariants
$ /design stress-test PRP-2026-02-01-001.yaml --learned

# Output:
# Stress Testing PRP-2026-02-01-001 Against Learned Invariants:
#
# [INV-L001] Route Coverage
#   Test: All internal hrefs have route handlers?
#   Step 2 references /users/{id}
#   → FAIL: No route handler defined
#   IMPACT: Users will see 404
#   FIX: Add route handler step
#
# [INV-L002] Filter Logic Edge Cases
#   Test: Date filters handle negative values?
#   Step 3 filter: days_until_close <= 14
#   → FAIL: No validation for negative days
#   FIX: Add test for negative days in validation gate
#
# [INV-L003] Pagination
#   Test: Large result sets paginated?
#   Step 2: search() returns paginated results
#   → PASS
#
# Result: 2 FAIL, 1 PASS
# PRP not ready for execution
# Fix 2 violations and re-stress-test
```

### 9.3 Freshness Check: System Learning Status

```bash
$ /design-freshness --system-learning

# Output:
# Design Ops System Freshness Report
#
# Learned Invariants: 8 active
# ├─ INV-L001 (Route Coverage): Last validated 2026-01-26, confidence 0.95
# ├─ INV-L002 (Filter Edge Cases): Last validated 2026-01-26, confidence 0.92
# ├─ INV-L003 (Pagination): Last validated 2026-01-26, confidence 0.91
# ├─ INV-L004 (Cache Invalidation): Last validated 2026-01-26, confidence 0.87
# ├─ INV-L005 (RBAC): Last validated 2026-01-26, confidence 0.88
# ├─ INV-L006 (Audit Logging): Last validated 2026-01-26, confidence 0.93
# ├─ INV-L007 (New): Created 2026-01-26, confidence 0.89, needs validation
# └─ INV-L008 (New): Created 2026-01-26, confidence 0.91, needs validation
#
# Confidence Calibration:
# ├─ Accuracy: ±0.04 (good)
# ├─ Recent confidence inflation? No
# ├─ Invariants needing recalibration: None
#
# Learning Velocity:
# ├─ Week of 2026-01-19: 2 invariants created
# ├─ Week of 2026-01-26: 6 invariants created
# ├─ Trend: Accelerating (good, system learning faster)
#
# Recommendations:
# ├─ INV-L007, L008 need validation in 2+ future PRPs
# ├─ No deprecated invariants (system is improving)
# └─ Consider documenting patterns that work consistently
```

---

## 10. Summary: Dangerous Mode Learning Integration

### 10.1 Key Principles

| Principle | Implementation |
|-----------|-----------------|
| **Learn while executing** | Step execution captures observations → learnings |
| **Confidence-based promotion** | Score >= 0.80 → system invariant; 0.50-0.79 → project; < 0.50 → reject |
| **No human bottleneck** | Auto-promotion in dangerous mode (overrideable) |
| **Future constraints** | New invariants constrain next PRP at design time |
| **Feedback loop** | Each PRP learns; next PRP respects those learnings |
| **Version invariants** | Track confidence/scope evolution across projects |
| **Audit trail** | Every promotion logged for system accountability |

### 10.2 Timeline: Single PRP to System Knowledge

```
T0: PRP-001 Created
  └─ No learned invariants exist yet

T1: PRP-001 Step 3 (Build Routes)
  └─ Learning LEARN-001: Routes need handlers
  └─ Confidence: 0.95 → PROMOTE → INV-L001 created

T2: PRP-001 Step 4 (Filters)
  └─ Learning LEARN-002: Filters need edge case handling
  └─ Confidence: 0.92 → PROMOTE → INV-L002 created

T3: PRP-001 Complete
  └─ System now has 2 new constraints

T4: PRP-002 Spec Validation
  └─ /design validate respects INV-L001, INV-L002
  └─ PRP-002 generation includes constraint references

T5: PRP-002 Execution
  └─ PRP-002 respects INV-L001 (routes tested)
  └─ PRP-002 respects INV-L002 (filters validated)
  └─ Learns 2 new invariants: INV-L003, INV-L004

T6: PRP-003 Spec Validation
  └─ /design validate respects INV-L001, L002, L003, L004
  └─ 4 learned constraints inherited from PRP-1 & PRP-2

T7: System Reaches Maturity
  └─ Each PRP executes faster (respects 4+ constraints)
  └─ Edge cases caught at design time (before implementation)
  └─ Dangerous mode compounds learning velocity
```

### 10.3 Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Over-promoting** | Promoting low-confidence learnings pollutes system | Only promote >= 0.80 unless override justified |
| **Ignoring learned invariants** | Writing PRP that violates learned rules | Run `--include-learned` validation |
| **Stale confidence** | Never recalibrating scores as you learn more | Annual re-score learned invariants |
| **Hoarding learnings** | Not promoting obvious learnings to system | Default to promote if confidence >= 0.80 |
| **Forgetting context** | Creating invariant without source PRP link | Always record origin_prp + origin_step |

---

## Appendix: Complete JSON Task Schema

```json
{
  "task_id": "promote-invariant-INV-L001",
  "task_type": "system-improvement",
  "prp_context": {
    "source_prp": "PRP-2026-01-22-001",
    "source_step": 3,
    "source_phase": "implementation"
  },
  "learning_context": {
    "learning_id": "LEARN-2026-01-23-001",
    "observation": "Every internal link (href) in UI components must have a corresponding route handler",
    "confidence_score": 0.95
  },
  "invariant_context": {
    "invariant_id": "INV-L001",
    "invariant_name": "Route Coverage",
    "invariant_type": "learned"
  },
  "task_lifecycle": {
    "created_at": "2026-01-23T14:22:31Z",
    "started_at": "2026-01-23T14:22:31Z",
    "completed_at": "2026-01-23T14:22:33Z",
    "status": "completed",
    "owner": "claude-haiku-4-5",
    "mode": "dangerous"
  },
  "task_dependencies": {
    "blocks": [],
    "blockedBy": ["generate-learning-LEARN-2026-01-23-001"]
  },
  "task_effects": {
    "files_modified": [
      "~/.claude/design-ops/invariants/learned-invariants.md"
    ],
    "invariants_registered": ["INV-L001"],
    "future_validations_affected": "All /design validate commands targeting consumer-product domain"
  },
  "metadata": {
    "decision": "PROMOTE",
    "decision_reason": "Dangerous mode + confidence 0.95 >= 0.80 threshold",
    "applies_to_domains": ["consumer-product"],
    "applies_to_frameworks": ["Dash", "React Router"],
    "version_history": {
      "initial_version": "1.0",
      "created": "2026-01-23T14:22:30Z",
      "confidence": 0.95
    }
  },
  "audit": {
    "events": [
      {
        "timestamp": "2026-01-23T14:22:30Z",
        "event": "LEARNING_CAPTURED",
        "detail": "LEARN-2026-01-23-001 extracted from Step 3"
      },
      {
        "timestamp": "2026-01-23T14:22:31Z",
        "event": "PROMOTION_TRIGGERED",
        "detail": "Auto-promotion decision: confidence 0.95 >= 0.80"
      },
      {
        "timestamp": "2026-01-23T14:22:32Z",
        "event": "INVARIANT_CREATED",
        "detail": "INV-L001 registered in learned-invariants.md"
      },
      {
        "timestamp": "2026-01-23T14:22:33Z",
        "event": "TASK_COMPLETED",
        "detail": "Promotion pipeline finished successfully"
      }
    ]
  }
}
```

---

*Last updated: 2026-01-24*
*Dangerous Mode Learning Pipeline v1.0*
*Author: Design Ops System*
