# Dangerous Mode: Quick Reference

Fast lookup for dangerous mode learning auto-promotion pipeline.

---

## Auto-Promotion Decision Tree

```
Learning captured with confidence score:

confidence >= 0.80?
  ├─ YES → PROMOTE to system invariant
  │        Create INV-L{N}, add to learned-invariants.md
  │        Task: promote-invariant-INV-L{N} (auto-completed)
  │        Future PRPs will be constrained by this
  │
  ├─ 0.50-0.79 → ACCEPT (project-local)
  │              Saved in project-learnings.md
  │              NOT system-wide, needs more evidence
  │
  └─ < 0.50 → REJECT
             No permanent record
             Can be re-observed if pattern repeats
```

---

## Learning → Invariant Promotion

### Input: Learning

```yaml
learning_id: LEARN-2026-01-23-001
source_prp: PRP-2026-01-22-001
source_step: 3
source_phase: implementation

observation: |
  Every internal link (href) in UI components must have
  a corresponding route handler.

confidence: 0.95
confidence_reasoning: "Observed in 2 projects, matches patterns"

applies_to: ["consumer-product", "single-page-apps"]
```

### Output: Invariant (if confidence >= 0.80)

```yaml
INV-L001:
  source: PRP-2026-01-22-001 / Step 3
  rule: Every internal link must have route handler
  confidence: 0.95
  scope: consumer-product, single-page-apps
  validation: Extract hrefs, verify routes, Playwright test
  enforcement: PRPs must include route coverage test
```

### Task Created

```
Task: promote-invariant-INV-L001
Type: system-improvement
Owner: claude-haiku (auto)
Status: completed (immediately)
Blocks: nothing
Effect: INV-L001 registered globally
```

---

## Validation Pipeline

### PRP-1 Execution
```
Step 3: Build UI
  └─ Learning captured (routes need handlers)
  └─ Confidence: 0.95 → PROMOTE → INV-L001
```

### PRP-2 Spec Validation
```
/design validate specs/search.md --include-learned
  ├─ Core invariants (1-11): PASS
  ├─ Domain invariants: PASS
  ├─ Learned invariants (INV-L001): PASS
  │  └─ Spec includes route coverage test ✓
  └─ Ready for PRP compilation
```

### PRP-2 Execution
```
Respects INV-L001 (from PRP-1)
  └─ Step 2: Add route handler
  └─ Step 3: Include Playwright route test
  └─ Learns 2 new invariants: INV-L003, L004
```

### PRP-3 Validation
```
/design validate specs/admin.md --include-learned
  ├─ Learned invariants: [INV-L001, L002, L003, L004]
  │  ├─ Route test? ✓ (respects L001)
  │  ├─ Edge cases? ✓ (respects L002)
  │  ├─ Pagination? ✓ (respects L003)
  │  └─ Cache invalidation? ✓ (respects L004)
  └─ Ready for PRP compilation
```

---

## Confidence Scoring (0.0-1.0)

| Score | Action | Example |
|-------|--------|---------|
| 0.95-1.0 | PROMOTE immediately | "Observed in 2+ projects, matches patterns" |
| 0.80-0.94 | PROMOTE | "Pattern documented, not yet validated widely" |
| 0.50-0.79 | ACCEPT (project-local) | "Seems right, but needs more evidence" |
| < 0.50 | REJECT | "Uncertain, might be project-specific" |

---

## File Locations

| File | Purpose |
|------|---------|
| `~/.claude/design-ops/invariants/learned-invariants.md` | Global registry of learned invariants |
| `project-learnings.md` | Project-local learnings (confidence 0.50-0.79) |
| `PRP-YYYY-MM-DD-NNN.yaml` | Meta section references learned invariants |
| `retrospective-YYYY-MM-DD.md` | Documents which learnings promoted to invariants |

---

## Commands at a Glance

### Validate (includes learned invariants)
```bash
/design validate specs/myspec.md --include-learned
```

### Stress-test against learned invariants
```bash
/design stress-test PRP-2026-01-25-001.yaml --learned
```

### Run in dangerous mode
```bash
/design run --dangerous PRP-2026-01-25-001.yaml
```

### System learning status
```bash
/design-freshness --system-learning
```

---

## Three-PRP Learning Cycle

```
PRP-1 (0 constraints)
  ├─ Execution learns 2 invariants
  └─ Creates INV-L001, INV-L002

PRP-2 (2 constraints: INV-L001, L002)
  ├─ Validation respects L001, L002
  ├─ Execution learns 2 more invariants
  └─ Creates INV-L003, INV-L004

PRP-3 (4 constraints: L001, L002, L003, L004)
  ├─ Validation respects all 4
  ├─ Execution learns 2 more invariants
  └─ Creates INV-L005, INV-L006

Result: Each PRP constrained by learnings from prior work
```

---

## Invariant Version History

```yaml
INV-L001:

  version: 1.0 (2026-01-23)
    confidence: 0.95
    source: PRP-001
    status: active

  version: 1.1 (2026-01-26)
    confidence: 0.98  # ↑ Increased
    source: PRP-003 validated it
    changes: |
      Added domain scoping
      Excluded server-side rendering
    status: active

  # Invariants can be deprecated if violated later
  version: DEPRECATED (2026-02-01)
    reason: "Doesn't apply to async code paths"
    successor: "Use INV-L008 instead"
    status: deprecated
```

---

## Task Dependencies

```
Step execution:
  Step 3 (Build routes)
    └─ generate-learning-LEARN-001
       └─ promote-invariant-INV-L001
          ├─ Register to learned-invariants.md
          ├─ Task marked completed
          └─ Future validations use INV-L001

Next PRP:
  validate-next-prp
    └─ blocked-by: [promote-invariant-INV-L001]
    └─ Must respect INV-L001 in spec
       └─ Unblocks next-prp-generation
```

---

## Common Patterns

### Pattern 1: Routes Need Tests
```yaml
Observation: Links without route handlers → 404
Confidence: 0.95 (clear pattern)
Decision: PROMOTE → INV-L001
Applied in: PRP-1, PRP-2, PRP-3
```

### Pattern 2: Filters Need Edge Cases
```yaml
Observation: Date filters include past dates
Confidence: 0.92 (observed multiple times)
Decision: PROMOTE → INV-L002
Applied in: PRP-1, PRP-2, PRP-3
```

### Pattern 3: Uncertain Implementation Detail
```yaml
Observation: Caching strategy might need refresh?
Confidence: 0.62 (project context, needs more evidence)
Decision: ACCEPT (project-local)
Applied in: Current project only
```

---

## Conflict Resolution

**If PRP violates learned invariant:**

```bash
$ /design stress-test PRP-NEW.yaml --learned

[INV-L001] Route Coverage
  Step 2 references /users/{id}
  → FAIL: No route handler
  IMPACT: Users see 404

FIX OPTIONS:
  1. Add route handler to PRP
  2. Override invariant (requires justification)
  3. Deprecate invariant (if no longer valid)
```

---

## Decision Audit Trail

Every promotion is logged:

```
LEARN-2026-01-23-001:
  decision: PROMOTE
  confidence: 0.95
  timestamp: 14:22:30
  mode: dangerous
  action: Created INV-L001
  log: "Dangerous mode >= 0.80. Promoted to system invariant."

LEARN-2026-01-25-005:
  decision: ACCEPT
  confidence: 0.62
  timestamp: 12:10:00
  mode: dangerous
  action: Saved to project-learnings.md
  log: "Below 0.80. Accepted project-local (needs validation)."

LEARN-2026-01-20-099:
  decision: REJECT
  confidence: 0.38
  timestamp: 09:00:00
  mode: dangerous
  action: Discarded
  log: "Below 0.50. Rejected (no permanent record)."
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Over-promoting low confidence | Pollutes system | Stick to >= 0.80 rule |
| Ignoring learned invariants | PRPs violate system rules | Run `--include-learned` |
| Stale confidence scores | Scores become wrong | Annual re-calibration |
| Not promoting obvious insights | Learnings lost | Default to promote >= 0.80 |
| Missing source documentation | Can't trace back | Always record origin PRP + step |

---

## System Health Indicators

Check `/design-freshness --system-learning`:

```
✅ Good Signals:
  - Learned invariants growing each week
  - Confidence scores stable (±0.04 accuracy)
  - Recent PRPs respect learned invariants
  - No high-confidence invariants deprecated

⚠️ Warning Signs:
  - Confidence inflation (predicted > actual)
  - Invariants frequently violated
  - Stale invariants (not validated in 30 days)
  - PRPs failing stress-test against learned invariants
```

---

## Implementation Checklist

- [ ] Step execution captures observations (learning_id, confidence)
- [ ] Confidence >= 0.80 → auto-promote (dangerous mode)
- [ ] Create promotion task (promote-invariant-INV-L{N})
- [ ] Register invariant to learned-invariants.md
- [ ] Future /design validate includes new invariant
- [ ] PRP meta section documents inherited constraints
- [ ] Stress-test catches invariant violations early
- [ ] Retrospective documents learned invariants

---

*Quick Reference v1.0*
*See DANGEROUS-MODE-LEARNING-PIPELINE.md for full documentation*
