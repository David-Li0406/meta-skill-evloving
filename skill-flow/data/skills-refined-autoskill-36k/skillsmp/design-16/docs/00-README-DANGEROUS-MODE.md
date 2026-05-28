# Dangerous Mode Learning Auto-Promotion Pipeline

Complete guide to integrating step execution, learning capture, and invariant creation into a continuous improvement system.

---

## What You Have

A comprehensive 5-document suite (135+ KB) covering every aspect of dangerous mode learning auto-promotion:

```
00-README-DANGEROUS-MODE.md (this file)
├── Quick orientation + file guide
│
├── DANGEROUS-MODE-INDEX.md
│   └── Navigation guide, learning paths, quick reference
│
├── DANGEROUS-MODE-LEARNING-PIPELINE.md (MAIN GUIDE)
│   ├── 10 detailed sections
│   ├── 63 KB comprehensive reference
│   ├── All implementation details
│   └── Complete JSON task schema
│
├── DANGEROUS-MODE-QUICK-REFERENCE.md (CHEAT SHEET)
│   ├── Decision trees
│   ├── Confidence scoring quick lookup
│   ├── Commands at a glance
│   └── Common patterns
│
├── DANGEROUS-MODE-DIAGRAMS.md (VISUAL FLOWS)
│   ├── 10 flowcharts and timelines
│   ├── Task dependencies
│   ├── Invariant evolution
│   └── Confidence distribution
│
└── DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (REAL EXECUTION)
    ├── 3 complete PRPs (PRP-001 through PRP-003)
    ├── 6 learned invariants created
    ├── Step-by-step learning capture
    └── Real confidence scores
```

---

## Core Concept (1 Minute)

**Dangerous mode fast-tracks system learning:**

```
Step executes → Learning captured → Confidence scored
                                         ↓
                            confidence >= 0.80?
                                    ↙        ↖
                                  YES        NO
                                   ↓          ↓
                            Promote to    Accept to
                            System        Project
                            Invariant     Learnings
                            (INV-L{N})    (Local)
                                 ↓
                      Future PRPs constrained
                      by learned invariants
                                 ↓
                      PRP-2 respects INV-L001
                      PRP-3 respects INV-L001,L002,L003,L004
                      (each learns new invariants)
```

---

## Key Sections by Use Case

### "Show me the decision logic"
→ **DANGEROUS-MODE-QUICK-REFERENCE.md** (top, decision tree)
→ **DANGEROUS-MODE-DIAGRAMS.md** (Diagram 9, decision matrix)

### "I need to implement this"
→ **DANGEROUS-MODE-LEARNING-PIPELINE.md** (Sections 1-8)
→ **Appendix** (JSON task schema)

### "Walk me through execution"
→ **DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md** (all sections)
→ **DANGEROUS-MODE-DIAGRAMS.md** (Diagram 2, timeline)

### "How do invariants grow?"
→ **DANGEROUS-MODE-LEARNING-PIPELINE.md** (Section 5, invariant evolution)
→ **DANGEROUS-MODE-DIAGRAMS.md** (Diagram 4, confidence evolution)

### "What commands do I use?"
→ **DANGEROUS-MODE-QUICK-REFERENCE.md** (Commands at a Glance)
→ **DANGEROUS-MODE-LEARNING-PIPELINE.md** (Section 9)

### "Visual overview"
→ **DANGEROUS-MODE-DIAGRAMS.md** (all 10 diagrams)
→ Best for explaining to others

### "Where do I start?"
→ **DANGEROUS-MODE-INDEX.md** (learning paths)
→ Choose: Executive / Implementer / Operator / Architect

---

## The Three-PRP Cycle

This is the core feedback loop — runs after PRP-001 and repeats:

```
WEEK 1: PRP-001 Execution
├─ Step 1-5: Execute with learning capture
├─ Learning 1: Routes need handlers → Confidence 0.95 → PROMOTE → INV-L001
├─ Learning 2: Filters need edge cases → Confidence 0.92 → PROMOTE → INV-L002
└─ Result: 2 system invariants created

WEEK 2: PRP-002 (Constrained by PRP-001)
├─ Spec validation checks: Core + INV-L001, L002
├─ Execution respects both learned constraints
├─ Learning 3: Large searches need pagination → PROMOTE → INV-L003
├─ Learning 4: Cache invalidation required → PROMOTE → INV-L004
└─ Result: 4 total system invariants

WEEK 3: PRP-003 (Constrained by PRP-001 & PRP-002)
├─ Spec validation checks: Core + INV-L001, L002, L003, L004
├─ Execution respects all 4 learned constraints
├─ Learning 5: RBAC needed for admin → PROMOTE → INV-L005
├─ Learning 6: Audit logs structured → PROMOTE → INV-L006
└─ Result: 6 total system invariants

PATTERN:
  PRP-1: Learn 2, constrained by 0
  PRP-2: Learn 2 more, constrained by 2
  PRP-3: Learn 2 more, constrained by 4
  PRP-4: Learn 2 more, constrained by 6
  (each cycle accelerates due to learned constraints)
```

**See full timeline:** DANGEROUS-MODE-DIAGRAMS.md Diagram 2

---

## Confidence Thresholds (Decision Point)

This is where learning becomes (or doesn't become) a system invariant:

| Score | Decision | System Impact | Document |
|-------|----------|---------------|----------|
| **≥ 0.80** | PROMOTE | Creates INV-L{N} in learned-invariants.md | Quick-Ref: Scoring |
| **0.50-0.79** | ACCEPT | Saved locally (project-learnings.md), not system-wide | Quick-Ref: Scoring |
| **< 0.50** | REJECT | Discarded (no permanent record) | Quick-Ref: Scoring |

**Decision matrix:** DANGEROUS-MODE-DIAGRAMS.md Diagram 9

---

## Invariant Metadata (What Gets Created)

When a learning is promoted (confidence ≥ 0.80), this structure is created:

```yaml
INV-L001:
  id: INV-L001
  name: Route Coverage
  source: PRP-2026-01-22-001 / Step 3
  confidence: 0.95

  rule: |
    Every internal link (href) must have a route handler

  applies_to:
    domains: [consumer-product]
    frameworks: [Dash, React Router]

  validation: |
    1. Extract all href from components
    2. Verify matching route exists
    3. Playwright test: click → verify page loads

  enforcement: |
    PRPs must include route coverage test.
    Violation: PRP rejected until test added.

  versions:
    - version: 1.0
      created: 2026-01-23
      confidence: 0.95
      status: active
```

**Full schema:** DANGEROUS-MODE-LEARNING-PIPELINE.md Section 2.1

---

## Task Creation During Promotion

When learning is promoted, this task is created (and immediately completed):

```json
{
  "task_id": "promote-invariant-INV-L001",
  "type": "system-improvement",
  "owner": "claude-haiku-4-5",
  "status": "completed",

  "blocks": [],  // Doesn't block execution
  "blockedBy": ["generate-learning-LEARN-001"],

  "effects": {
    "file_updated": "learned-invariants.md",
    "invariant_registered": "INV-L001",
    "future_impact": "All /design validate commands check INV-L001"
  }
}
```

**Task structure:** DANGEROUS-MODE-LEARNING-PIPELINE.md Section 8

---

## Validation of Future PRPs

New PRPs validate against learned + core invariants:

```bash
# PRP-2 Validation (after PRP-1)
/design validate specs/search.md --include-learned

Checking Universal (1-11).......... PASS
Checking Learned:
  [INV-L001] Route Coverage....... PASS
    └─ Spec includes route test ✓
  [INV-L002] Filter Edge Cases.... PASS
    └─ Spec tests negative dates ✓

RESULT: PASS ✓ (PRP respects learned constraints)
```

**See examples:** DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (all PRP phases)

---

## Stress-Testing Against Learned Invariants

Before execution, catch violations early:

```bash
/design stress-test PRP-NEW.yaml --learned

[INV-L001] Route Coverage
  Step 2 references /users/{id}
  ✗ FAIL: No route handler
  FIX: Add route handler step

[INV-L002] Filter Logic
  Step 3: days_until_close <= 14
  ✗ FAIL: No negative date test
  FIX: Add test for negative days

Result: 2 violations found
Status: Fix violations before execution
```

**Full example:** DANGEROUS-MODE-LEARNING-PIPELINE.md Section 3.3

---

## File Locations

```
~/.claude/design-ops/docs/
├── 00-README-DANGEROUS-MODE.md ← you are here
├── DANGEROUS-MODE-INDEX.md ← navigation guide
├── DANGEROUS-MODE-LEARNING-PIPELINE.md ← main reference (read first)
├── DANGEROUS-MODE-QUICK-REFERENCE.md ← fast lookup
├── DANGEROUS-MODE-DIAGRAMS.md ← visual flows
└── DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md ← real execution

~/.claude/design-ops/invariants/
└── learned-invariants.md ← grows with each dangerous mode PRP

~/.claude/design-ops/
├── system-invariants.md ← core + domain invariants
└── design.md ← skill documentation
```

---

## Reading Recommendations by Role

### Executive / Decision-Maker (30 min)
1. This file (overview)
2. DANGEROUS-MODE-DIAGRAMS.md - Diagram 2 (timeline)
3. DANGEROUS-MODE-DIAGRAMS.md - Diagram 9 (decision matrix)
4. DANGEROUS-MODE-INDEX.md - Key Principles

→ Understand: What is it? How fast does it learn? How confident are decisions?

### Implementer / Engineer (2 hours)
1. DANGEROUS-MODE-LEARNING-PIPELINE.md (full)
2. DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (full)
3. DANGEROUS-MODE-DIAGRAMS.md (all)
4. DANGEROUS-MODE-QUICK-REFERENCE.md (for later use)

→ Understand: How to implement every component. Task creation, validation, promotion.

### Operator / Practitioner (90 min)
1. DANGEROUS-MODE-LEARNING-PIPELINE.md (Sections 1, 3, 7)
2. DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (PRP execution steps)
3. DANGEROUS-MODE-QUICK-REFERENCE.md (decision tree + commands)
4. DANGEROUS-MODE-DIAGRAMS.md (Diagrams 2, 9)

→ Understand: How to execute PRPs. How to decide on learnings. What commands to use.

---

## Core Principles

1. **Learn while executing** — Every step captures observations
2. **Confidence-based promotion** — ≥0.80 becomes system invariant
3. **No human bottleneck** — Auto-promotion in dangerous mode
4. **Future constraints** — New invariants guide next PRPs
5. **Feedback loop** — Each PRP learns while respecting priors
6. **Version invariants** — Track evolution across projects
7. **Audit everything** — Every decision logged

---

## Command Reference

```bash
# Validate spec against learned invariants
/design validate specs/myspec.md --include-learned

# Stress-test PRP against learned invariants
/design stress-test PRP-2026-01-25-001.yaml --learned

# Run PRP in dangerous mode (auto-promote learnings)
/design run --dangerous PRP-2026-01-25-001.yaml

# Check system learning status
/design-freshness --system-learning

# Document learnings and system improvements
/design retrospective PRP-2026-01-25-001
```

**All commands explained:** DANGEROUS-MODE-QUICK-REFERENCE.md (Commands section)

---

## Quick Decision Tree

```
Learning captured with confidence score X:

Is X >= 0.80?
├─ YES → PROMOTE
│       ├─ Create invariant ID (INV-L{N})
│       ├─ Add to learned-invariants.md
│       ├─ Create promotion task (auto-completed)
│       └─ Future PRPs validate against it
│
├─ Is 0.50 <= X < 0.80?
│  YES → ACCEPT
│       ├─ Save to project-learnings.md
│       ├─ Project-local scope only
│       └─ Can be promoted later with more evidence
│
└─ Is X < 0.50?
   YES → REJECT
        ├─ No permanent record
        └─ Can be re-observed if pattern repeats
```

**Full decision logic:** DANGEROUS-MODE-LEARNING-PIPELINE.md Section 7.1

---

## System Learning Growth

Typical learning curve (number of invariants over time):

```
Learned Invariants
        ^
      8 |          PRP-3 creates L5-L6
        |        ╱╲
      6 |      ╱    PRP-2 creates L3-L4
        |    ╱    ╱╲
      4 |  ╱    ╱    ...plateau (system mature)
        | ╱ PRP-1 creates L1-L2
      2 |●
        |
      0 └─────────────────────────
        W1  W2  W3  W4  W5  W6...

Pattern:
  - Early PRPs: Rapid learning (2-3 new/week)
  - Later PRPs: Steady refinement (fewer new)
  - Asymptotic: System reaches saturation (domain knowledge complete)

ROI:
  - PRP-1: 20 hours (baseline)
  - PRP-2: 18 hours (-2 hours from learned constraints)
  - PRP-3: 16 hours (-4 hours cumulative)
  - PRP-4: 14 hours (-6 hours cumulative)
```

**See full growth curve:** DANGEROUS-MODE-DIAGRAMS.md Diagram 6 & 10

---

## Example: Real 3-PRP Cycle

All 6 invariants created in 3 weeks:

| PRP | When | Invariants Created | Total | Constraints Respected |
|-----|------|-------------------|-------|----------------------|
| PRP-001 | W1 | INV-L001, L002 | 2 | 0 (first) |
| PRP-002 | W2 | INV-L003, L004 | 4 | 2 (L001, L002) |
| PRP-003 | W3 | INV-L005, L006 | 6 | 4 (L001-L004) |

**See real example:** DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (all sections)

---

## Integration with Design System

Dangerous mode integrates with existing components:

```
system-invariants.md (core + domain)
            ↓
/design validate (checks core, domain, learned)
            ↓
learned-invariants.md (grows with dangerous mode)
            ↓
/design stress-test (catches invariant violations)
            ↓
/design run --dangerous (captures learnings, promotes)
            ↓
retrospective (documents new invariants)
            ↓
Cycle repeats with more constraints
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Learning not promoted | Check confidence score (Pipeline 7.1) |
| Invariant violated by valid PRP | Deprecate invariant (Pipeline 5.2) |
| Too many invariants | Review and consolidate (Annual audit) |
| System learning plateaued | Review domain coverage (Diagrams 6) |
| Confidence not matching reality | Re-calibrate (Pipeline 5.1) |

---

## Status & Readiness

| Component | Status |
|-----------|--------|
| Documentation | ✅ Complete (135+ KB, 5 guides) |
| Diagrams | ✅ Complete (10 flowcharts) |
| Example walkthroughs | ✅ Complete (3 full PRPs) |
| Decision matrices | ✅ Complete |
| Command reference | ✅ Complete |
| Implementation schema | ✅ Complete (Appendix) |
| Integration points | ✅ Mapped |

**Ready for:** Implementation, training, production use.

---

## Next Steps

1. **Read DANGEROUS-MODE-INDEX.md** → Choose your learning path
2. **Read DANGEROUS-MODE-LEARNING-PIPELINE.md** → Deep dive on pipeline
3. **Study DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md** → See real execution
4. **Use DANGEROUS-MODE-QUICK-REFERENCE.md** → Fast lookup during work
5. **Reference DANGEROUS-MODE-DIAGRAMS.md** → Explain to others

---

## Document Structure

```
00-README-DANGEROUS-MODE.md (this file)
  └─ Quick orientation, file guide, core concepts

DANGEROUS-MODE-INDEX.md
  └─ Navigation, learning paths, cross-reference

DANGEROUS-MODE-LEARNING-PIPELINE.md (MAIN)
  ├─ Section 1: Learning → Invariant Promotion Pipeline
  ├─ Section 2: Invariant Metadata Structure
  ├─ Section 3: Future PRP Validation Loop
  ├─ Section 4: Feedback Loop Visualization
  ├─ Section 5: Cross-PRP Invariant Evolution
  ├─ Section 6: Real Example: 3 PRPs, 8 Invariants
  ├─ Section 7: Dangerous Mode Auto-Promotion Decision Logic
  ├─ Section 8: Invariant Promotion Task Structure
  ├─ Section 9: /design Commands Interaction
  ├─ Section 10: Summary
  └─ Appendix: Complete JSON Task Schema

DANGEROUS-MODE-QUICK-REFERENCE.md (CHEAT SHEET)
  └─ Decision trees, scoring, commands, patterns

DANGEROUS-MODE-DIAGRAMS.md (VISUAL)
  ├─ Diagram 1: Learning → Invariant flowchart
  ├─ Diagram 2: 3-PRP timeline with learning
  ├─ Diagram 3: Task dependency graph
  ├─ Diagram 4: Invariant confidence evolution
  ├─ Diagram 5: Stress-test violation detection
  ├─ Diagram 6: System maturity curve
  ├─ Diagram 7: Confidence distribution
  ├─ Diagram 8: Validation gate coverage
  ├─ Diagram 9: Promotion decision matrix
  └─ Diagram 10: Learning velocity graph

DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (REAL)
  ├─ PRP-001 (Forecast Dashboard)
  ├─ PRP-002 (Search Features)
  ├─ PRP-003 (Admin Dashboard)
  ├─ System state after 3 PRPs
  └─ Key insights
```

---

## Version & Maintenance

| Item | Value |
|------|-------|
| Suite Version | 1.0 |
| Created | 2026-01-24 |
| Status | Production-ready |
| Documents | 5 main + 1 index |
| Total Size | 135+ KB |
| Diagrams | 10 flowcharts |
| Example PRPs | 3 full walkthroughs |

---

## Start Here

**New to dangerous mode?** Read in this order:

1. **This file** (5 min) — Get oriented
2. **DANGEROUS-MODE-INDEX.md** (5 min) — Choose your path
3. **Based on role:**
   - Executive → Diagrams 2, 9 (10 min)
   - Implementer → Full Pipeline guide (90 min)
   - Operator → Sections 1, 3, 7 + Example (60 min)
   - Architect → Sections 1, 7, 10 + Diagrams 2, 6, 9 (30 min)

---

*Dangerous Mode Learning Auto-Promotion Pipeline*
*Documentation Suite v1.0*
*Status: Ready for production implementation*
