# Dangerous Mode Learning Pipeline: Complete Documentation Index

Navigate the comprehensive guide to dangerous mode learning auto-promotion and invariant integration.

---

## Overview

The dangerous mode learning pipeline integrates step execution, learning capture, and system invariant creation into a continuous improvement cycle:

```
Execute Step → Capture Learning → Auto-Decide (confidence-based)
    ↓              ↓                      ↓
Calculate      Assign              Promote (≥0.80)
Confidence    Confidence          Create Invariant
Score         Score               Register Globally
              ↓                      ↓
           0.80+?              Future PRPs
           PROMOTE              Constrained by
           |                    New Invariants
           v
        INV-L{N}
        (System)
```

---

## Documentation Files

### 1. DANGEROUS-MODE-LEARNING-PIPELINE.md
**Main comprehensive guide** — Read this first.

Contains:
- Learning → Invariant promotion pipeline (Section 1)
- Complete invariant metadata structure (Section 2)
- Future PRP validation loop (Section 3)
- Feedback loop visualization (Section 4)
- Cross-PRP invariant evolution (Section 5)
- Real example: 3 PRPs, 8 invariants (Section 6)
- Auto-promotion decision logic (Section 7)
- Invariant promotion task structure (Section 8)
- /design command interactions (Section 9)
- Summary and principles (Section 10)

**When to read:** Start here. Full context and implementation details.

**Key sections:**
- 1.3: How learnings become invariants
- 4.1: Three-PRP cycle visualization
- 8.1: Task creation during promotion
- 9.2: Stress-testing against learned invariants

---

### 2. DANGEROUS-MODE-QUICK-REFERENCE.md
**Fast lookup and decision trees** — Use during implementation.

Contains:
- Auto-promotion decision tree (confidence → action)
- Learning → Invariant conversion (input/output)
- Validation pipeline (PRP-1, PRP-2, PRP-3)
- Confidence scoring quick lookup (0.0-1.0)
- File locations reference
- Commands at a glance
- Three-PRP learning cycle
- Invariant version history patterns
- Task dependencies
- Common patterns
- Anti-patterns to avoid
- System health indicators
- Implementation checklist

**When to use:** During execution. Quick decisions and lookups.

**Key sections:**
- Auto-Promotion Decision Tree: Make confidence-based decisions
- Commands at a Glance: Copy-paste ready commands
- Common Patterns: Pattern matching for your observations

---

### 3. DANGEROUS-MODE-DIAGRAMS.md
**Visual flowcharts and timelines** — Reference during planning.

Contains:
- Flowchart: Learning → Invariant promotion (Diagram 1)
- Timeline: 3-PRP execution with learning (Diagram 2)
- Task dependency graph (Diagram 3)
- Invariant confidence evolution (Diagram 4)
- Stress-test violation detection (Diagram 5)
- System invariant maturity curve (Diagram 6)
- Confidence score distribution (Diagram 7)
- Validation gate coverage (Diagram 8)
- Promotion decision matrix (Diagram 9)
- System learning velocity graph (Diagram 10)

**When to use:** Planning cycles, explaining to others, understanding system state.

**Key diagrams:**
- Diagram 2: See how 3 PRPs compound learning
- Diagram 3: Understand task sequencing across PRPs
- Diagram 9: Matrix showing all promotion decisions

---

### 4. DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md
**Real step-by-step execution of 3 PRPs** — Study for deep understanding.

Contains:
- PRP-001 (Forecast Dashboard)
  - Spec & validation
  - Step-by-step execution
  - Two learnings captured (routes, filters)
  - Auto-promotion to INV-L001, INV-L002
  - Retrospective with system improvements

- PRP-002 (Search Features)
  - Spec with inherited constraints
  - Validation against INV-L001, L002
  - Two more learnings captured
  - Auto-promotion to INV-L003, INV-L004

- PRP-003 (Admin Dashboard)
  - Spec with 4 inherited constraints
  - Validation against all 4 learned invariants
  - Two more learnings captured
  - Auto-promotion to INV-L005, INV-L006

- System state after 3 PRPs
- Key insights

**When to use:** Understanding concrete execution flow. Learning pattern matching.

**Key sections:**
- Step 3: Build UI Routes: How LEARN-001 gets promoted to INV-L001
- Step 4: Add Filtering: How filter bugs create INV-L002
- PRP-002 Phase 1: See spec referencing inherited constraints
- PRP-003 Phase 1: See 4 constraints affecting design

---

## Usage Patterns by Role/Task

### I'm implementing a feature with dangerous mode

1. **Before execution:** Read DANGEROUS-MODE-QUICK-REFERENCE.md (Decision Tree)
2. **During execution:** Check file locations and validation commands
3. **When learning captured:** Use Decision Tree to decide: promote/accept/reject
4. **After execution:** Read retrospective section of DANGEROUS-MODE-LEARNING-PIPELINE.md

### I'm designing the next PRP

1. **Check existing invariants:** DANGEROUS-MODE-QUICK-REFERENCE.md (Three-PRP cycle)
2. **Validate spec:** Use `/design validate --include-learned` command
3. **Understand constraints:** DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (PRP-2 Phase 1)
4. **Stress-test:** Reference DANGEROUS-MODE-LEARNING-PIPELINE.md (Section 3.3)

### I'm explaining dangerous mode to someone

1. **Overview:** DANGEROUS-MODE-INDEX.md (this file)
2. **Visual:** DANGEROUS-MODE-DIAGRAMS.md (Diagram 2 or 9)
3. **Concrete example:** DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md
4. **Decisions:** DANGEROUS-MODE-QUICK-REFERENCE.md (Matrix)

### I'm debugging why a learning wasn't promoted

1. **Decision logic:** DANGEROUS-MODE-LEARNING-PIPELINE.md (Section 7.1)
2. **Confidence threshold:** DANGEROUS-MODE-QUICK-REFERENCE.md (Confidence Scoring)
3. **Log audit trail:** DANGEROUS-MODE-LEARNING-PIPELINE.md (Section 7.2)
4. **Override:** DANGEROUS-MODE-LEARNING-PIPELINE.md (Section 8.1 task override field)

### I'm building the system (implementation)

1. **Full pipeline:** DANGEROUS-MODE-LEARNING-PIPELINE.md (all sections)
2. **Task schema:** DANGEROUS-MODE-LEARNING-PIPELINE.md (Appendix)
3. **Execution flow:** DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md
4. **Validation gates:** DANGEROUS-MODE-DIAGRAMS.md (Diagram 8)

### I'm calibrating confidence scores

1. **Rubric:** DANGEROUS-MODE-QUICK-REFERENCE.md (Confidence Scoring)
2. **History:** DANGEROUS-MODE-DIAGRAMS.md (Diagram 4 - Confidence Evolution)
3. **System health:** DANGEROUS-MODE-QUICK-REFERENCE.md (System Health Indicators)
4. **Calibration details:** DANGEROUS-MODE-LEARNING-PIPELINE.md (Section 5.1)

---

## Key Concepts Cross-Reference

### Confidence Score Thresholds

| Score | Action | Documents |
|-------|--------|-----------|
| >= 0.80 | PROMOTE (system invariant) | Quick-Ref: Scoring / Pipeline: 1.2 |
| 0.50-0.79 | ACCEPT (project-local) | Quick-Ref: Scoring / Diagrams: 9 |
| < 0.50 | REJECT (no record) | Pipeline: 1.2 / Quick-Ref: Scoring |

### Auto-Promotion Decision

| Component | Location |
|-----------|----------|
| Decision algorithm | Pipeline: Section 7.1 |
| Decision tree | Quick-Ref: Top |
| Decision matrix | Diagrams: Diagram 9 |
| Decision logging | Pipeline: Section 7.2 |

### Invariant Metadata

| Metadata | Location |
|----------|----------|
| Full schema | Pipeline: Section 2.1 |
| File organization | Pipeline: Section 2.2 |
| Version tracking | Pipeline: Section 5 |
| Deprecation | Pipeline: Section 5.2 |

### Validation & Constraints

| Topic | Location |
|-------|----------|
| Future PRP validation | Pipeline: Section 3 |
| Stress-testing | Pipeline: Section 3.3 |
| Validation gates | Diagrams: Diagram 8 |
| Constraints inheritance | Walkthrough: PRP-002 Phase 1 |

### Learning Examples

| Learning | Location |
|----------|----------|
| Route Coverage (INV-L001) | Walkthrough: Step 3 |
| Filter Edge Cases (INV-L002) | Walkthrough: Step 4 |
| Pagination (INV-L003) | Walkthrough: PRP-2 Step 2 |
| Cache Invalidation (INV-L004) | Walkthrough: PRP-2 Step 4 |
| RBAC (INV-L005) | Walkthrough: PRP-3 Step 3 |
| Audit Logging (INV-L006) | Walkthrough: PRP-3 Step 5 |

### Command Reference

| Command | Location |
|---------|----------|
| /design validate --include-learned | Pipeline: 3.2 / Quick-Ref: Commands |
| /design stress-test --learned | Pipeline: 3.3 / Quick-Ref: Commands |
| /design run --dangerous | Quick-Ref: Commands / Walkthrough |
| /design retrospective | Quick-Ref: Commands / Walkthrough |

---

## Learning Path (Recommended Reading Order)

### Path 1: Executive Understanding (30 minutes)
1. DANGEROUS-MODE-INDEX.md (this file) - Overview
2. DANGEROUS-MODE-DIAGRAMS.md (Diagram 2) - Timeline visualization
3. DANGEROUS-MODE-QUICK-REFERENCE.md - Decision tree
4. DANGEROUS-MODE-DIAGRAMS.md (Diagram 9) - Decision matrix

**Result:** Understand what dangerous mode is, how decisions are made, and how PRPs compound learning.

---

### Path 2: Implementer Deep Dive (2 hours)
1. DANGEROUS-MODE-LEARNING-PIPELINE.md (full) - Complete system
2. DANGEROUS-MODE-DIAGRAMS.md (all) - Visual reference
3. DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (full) - Concrete execution
4. DANGEROUS-MODE-QUICK-REFERENCE.md - Fast lookup

**Result:** Full understanding of pipeline, ready to implement all components.

---

### Path 3: Operator/Practitioner (1.5 hours)
1. DANGEROUS-MODE-LEARNING-PIPELINE.md (Sections 1-4) - Pipeline overview
2. DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md - Real execution
3. DANGEROUS-MODE-QUICK-REFERENCE.md - Decision making
4. DANGEROUS-MODE-DIAGRAMS.md (Diagrams 2, 9) - Visual reference

**Result:** Ready to execute PRPs with dangerous mode, understand decisions, use invariants.

---

### Path 4: Decision-Maker/Architect (1 hour)
1. DANGEROUS-MODE-INDEX.md (this file) - Overview
2. DANGEROUS-MODE-DIAGRAMS.md (Diagrams 2, 6, 9) - System growth and decisions
3. DANGEROUS-MODE-LEARNING-PIPELINE.md (Sections 1, 7, 10) - Pipeline and principles
4. DANGEROUS-MODE-QUICK-REFERENCE.md - System health indicators

**Result:** Understand system growth rate, decision quality, when to enable dangerous mode.

---

## File Locations Reference

```
~/.claude/design-ops/docs/

├── DANGEROUS-MODE-INDEX.md (you are here)
├── DANGEROUS-MODE-LEARNING-PIPELINE.md (main comprehensive guide)
├── DANGEROUS-MODE-QUICK-REFERENCE.md (fast lookup)
├── DANGEROUS-MODE-DIAGRAMS.md (visual flows)
└── DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md (concrete execution)

~/.claude/design-ops/invariants/

└── learned-invariants.md (system registry, grows with each PRP)

~/.claude/design-ops/

├── system-invariants.md (core + domain invariants)
└── design.md (skill documentation, references dangerous mode)
```

---

## Commands Quick Lookup

### Validate (with learned invariants)
```bash
/design validate specs/myspec.md --include-learned
```
Reference: Pipeline Section 3.2 / Quick-Ref: Commands

### Stress-test against learned invariants
```bash
/design stress-test PRP-2026-01-25-001.yaml --learned
```
Reference: Pipeline Section 3.3 / Quick-Ref: Commands

### Run in dangerous mode
```bash
/design run --dangerous PRP-2026-01-25-001.yaml
```
Reference: Walkthrough / Quick-Ref: Commands

### Check system learning status
```bash
/design-freshness --system-learning
```
Reference: Pipeline Section 9.3 / Quick-Ref: Commands

---

## Key Principles (One-Liners)

1. **Learn while executing** — Step execution captures learnings
2. **Confidence-based promotion** — Score >= 0.80 → system invariant
3. **No human bottleneck** — Auto-promotion in dangerous mode
4. **Future constraints** — New invariants constrain next PRP
5. **Feedback loop** — Each PRP learns; next PRP respects those learnings
6. **Version invariants** — Track confidence/scope evolution
7. **Audit everything** — Every promotion logged for accountability

Reference: Pipeline Section 10.1 / Quick-Ref: Summary

---

## Troubleshooting

### "Why wasn't my learning promoted?"
- Check confidence score: Pipeline Section 7.1
- Verify thresholds: Quick-Ref Confidence Scoring
- Review decision log: Pipeline Section 7.2

### "How do I know if my invariant is correct?"
- Check calibration: Diagrams Diagram 4
- Look at validations: Pipeline Section 5.1
- Review violations: Pipeline Section 5.2

### "Can I override the decision?"
- Yes: Pipeline Section 8.1, field: override_promote
- When: Only for high-confidence learnings you're sure about
- Cost: Requires human review, can lower system confidence

### "How do I deprecate an invariant?"
- When: Invariant violated by valid PRP, not worth keeping
- How: Pipeline Section 5.2, deprecation path
- Effect: Future PRPs don't need to respect it

### "Why is execution slower/faster?"
- Check: Diagrams Diagram 10 (velocity graph)
- Reason: More constraints = more design-time validation
- Timeline: Early PRPs slower, later PRPs faster

---

## Version Information

| Document | Version | Updated | Author |
|----------|---------|---------|--------|
| DANGEROUS-MODE-INDEX.md | 1.0 | 2026-01-24 | Design Ops System |
| DANGEROUS-MODE-LEARNING-PIPELINE.md | 1.0 | 2026-01-24 | Design Ops System |
| DANGEROUS-MODE-QUICK-REFERENCE.md | 1.0 | 2026-01-24 | Design Ops System |
| DANGEROUS-MODE-DIAGRAMS.md | 1.0 | 2026-01-24 | Design Ops System |
| DANGEROUS-MODE-EXAMPLE-WALKTHROUGH.md | 1.0 | 2026-01-24 | Design Ops System |

---

## Integration Points

- **System Invariants:** system-invariants.md (core + domain invariants)
- **Learned Invariants:** learned-invariants.md (grows with dangerous mode)
- **Confidence Rubric:** templates/confidence-rubric.md
- **PRP Template:** templates/prp-base.md (includes learned invariant references)
- **Retrospective:** templates/retrospective-template.md (Section 5: System Improvements)
- **Design Skill:** design.md (references dangerous mode workflows)
- **Validation:** skills/validate.md (checks learned + core invariants)

---

## Additional Resources

### Within Design Ops
- `templates/confidence-rubric.md` — Detailed confidence scoring
- `examples/` — Pattern library
- `skills/validate.md` — Validation skill documentation
- `docs/ralph-methodology.md` — Execution methodology

### External
- `CLAUDE.md` — Project instructions and context
- `System/TELOS/` — Goal framework for learning application

---

## Quick Decision Table

| Scenario | Action | Reference |
|----------|--------|-----------|
| Learning captures with high confidence | PROMOTE to INV-L{N} | Quick-Ref: Decision Tree |
| Learning with moderate confidence | ACCEPT to project-local | Quick-Ref: Confidence Scoring |
| PRP with inherited constraints | Validate, then execute | Walkthrough: PRP-2 Phase 1 |
| Stress-test finds violation | Fix or override | Pipeline: Section 3.3 |
| Invariant frequently violated | Deprecate + create new | Pipeline: Section 5.2 |
| System learning is plateauing | Review and refine existing | Diagrams: Diagram 6 |

---

*Complete Documentation Index v1.0*
*Last Updated: 2026-01-24*
*Status: Ready for production use*
